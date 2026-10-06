import hashlib,json,pathlib,tempfile,unittest
import science_archive_search as relay
class Response:
    status=200
    headers={"Content-Type":"application/json"}
    def __init__(self,raw,url):self.raw=raw;self.url=url
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self,n):return self.raw[:n]
    def geturl(self):return self.url
class Client:
    def __init__(self,raw):self.raw=raw;self.request=None
    def open(self,request,timeout):self.request=request;return Response(self.raw,request.full_url)
class Tests(unittest.TestCase):
    def test_transient_retry_preserves_attempt_and_exact_body(self):
        from urllib.error import HTTPError
        from unittest.mock import patch
        class Flaky(Client):
            calls=0
            def open(self,request,timeout):
                self.calls+=1
                if self.calls==1:raise HTTPError(request.full_url,503,"unavailable",{},None)
                return super().open(request,timeout)
        with tempfile.TemporaryDirectory() as d,patch.object(relay.time,"sleep"):
            c=Flaky(b'#Table1\nspecObjID,ra,dec,z\n123,1,2,0.1\n')
            x=relay.acquire("sdss","","",3,d,opener=c)
            self.assertEqual(x["status"],"acquired");self.assertEqual(c.calls,2)
            self.assertTrue(x["attempts"][0]["retryable"])
    def test_permanent_failure_and_retry_cap(self):
        from urllib.error import HTTPError
        from unittest.mock import patch
        for code,calls in [(403,1),(503,3)]:
            class Broken(Client):
                count=0
                def open(self,request,timeout):
                    self.count+=1;raise HTTPError(request.full_url,code,"failed",{},None)
            with tempfile.TemporaryDirectory() as d,patch.object(relay.time,"sleep"):
                c=Broken(b'');x=relay.acquire("sdss","","",3,d,opener=c)
                self.assertEqual(x["status"],"failed");self.assertEqual(c.count,calls)
    def test_snapshot_identity_and_degraded_scope(self):
        for record,status in [(17496685,"acquired"),(999,"failed")]:
            with tempfile.TemporaryDirectory() as d:
                raw=json.dumps({"id":record,"metadata":{"title":"GWOSC Event Portal Snapshots"},"files":[{"key":"file.tar"}]}).encode()
                x=relay.acquire("gwosc-snapshot","","",3,d,opener=Client(raw))
                self.assertEqual(x["status"],status)
                if status=="acquired":self.assertFalse(x["live_api_healthy"]);self.assertIn("2025-10-31",x["scope"])

    def test_pds_identifier_and_mission_scope(self):
        with tempfile.TemporaryDirectory() as d:
            x=relay.acquire("pds","","urn:nasa:pds:mars2020.spice",3,d,opener=Client(b'{"id":"urn:nasa:pds:mars2020.spice::16.0"}'))
            self.assertEqual(x["status"],"acquired")
        with tempfile.TemporaryDirectory() as d:
            x=relay.acquire("pds","","urn:nasa:pds:mars2020.spice::15.0",3,d,opener=Client(b'{"id":"urn:nasa:pds:mars2020.spice::16.0"}'))
            self.assertEqual(x["status"],"failed")
        with self.assertRaises(ValueError):relay.route("pds","bad/mission","",3)
        with self.assertRaises(ValueError):relay.route("pds","mars2020","urn:nasa:pds:test",3)
    def test_sdss_table_marker_and_identifiers(self):
        with tempfile.TemporaryDirectory() as d:
            raw=b'#Table1\nspecObjID,ra,dec,z\n123,1.0,2.0,0.1\n'
            x=relay.acquire("sdss","","",3,d,opener=Client(raw))
            self.assertEqual(x["sample"][0]["specObjID"],"123")
            self.assertEqual(x["sha256"],hashlib.sha256(raw).hexdigest())
        with self.assertRaises(ValueError):relay.route("sdss","arbitrary SQL","",3)
    def test_openneuro_matching_metadata_and_exact_hash(self):
        raw=b'{"data":{"dataset":{"id":"ds000224","name":"MSC"}}}'
        with tempfile.TemporaryDirectory() as d:
            c=Client(raw);x=relay.acquire("openneuro","","ds000224",3,d,opener=c)
            self.assertEqual(x["status"],"acquired");self.assertEqual(x["sample"][0]["id"],"ds000224")
            self.assertEqual(x["sha256"],hashlib.sha256(raw).hexdigest());self.assertEqual((pathlib.Path(d)/"provider.raw").read_bytes(),raw)
            self.assertNotIn("mutation",json.loads(c.request.data)["query"])
    def test_doi_metadata_scope_and_wrong_prefix(self):
        for doi,status in [("10.17182/hepdata.123.v1","acquired"),("10.99999/unrelated","failed")]:
            with tempfile.TemporaryDirectory() as d:
                x=relay.acquire("hepdata-doi","Higgs","",3,d,opener=Client(json.dumps({"data":[{"id":doi}]}).encode()))
                self.assertEqual(x["status"],status)
                if status=="acquired":self.assertFalse(x["measurement_tables_available"]);self.assertEqual(x["provider"],"DataCite")
    def test_unsupported_search_is_rejected(self):
        for source in ("gwosc","gaia-archive","eso","alma","desi"):
            with self.assertRaises(ValueError):relay.route(source,"brain","",3)
        with self.assertRaises(ValueError):relay.route("dandi","","ds000224",3)
    def test_http_200_graphql_error_is_failure(self):
        with tempfile.TemporaryDirectory() as d:
            x=relay.acquire("openneuro","","ds000224",3,d,opener=Client(b'{"errors":[{"message":"bad"}]}'))
            self.assertEqual(x["status"],"failed");self.assertTrue((pathlib.Path(d)/"provider.raw").exists())
    def test_size_cap(self):
        with tempfile.TemporaryDirectory() as d:
            x=relay.acquire("gwosc","","",3,d,opener=Client(b'x'*(relay.MAX_BYTES+1)))
            self.assertEqual(x["status"],"failed")
    def test_limit_and_record_bounds(self):
        with self.assertRaises(ValueError):relay.route("openneuro","","../../secret",3)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):relay.acquire("gwosc","","",11,d)
    def test_cross_host_redirect_rejected(self):
        gate=relay.CheckedRedirect({"gwosc.org"})
        with self.assertRaises(ValueError):gate.redirect_request(None,None,302,"",{},"https://other.invalid/")
    def test_tap_error_not_csv_pass(self):
        with tempfile.TemporaryDirectory() as d:
            x=relay.acquire("eso","","",3,d,opener=Client(b'<VOTABLE>error</VOTABLE>'))
            self.assertEqual(x["status"],"failed")
if __name__=="__main__":unittest.main()
