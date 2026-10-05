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
