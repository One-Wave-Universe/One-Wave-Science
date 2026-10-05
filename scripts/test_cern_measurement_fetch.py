import json,tempfile,unittest,zlib
import cern_measurement_fetch as fetch
from test_science_archive_search import Response
class Client:
    def __init__(self,manifest,raw):self.manifest=manifest;self.raw=raw;self.calls=0
    def open(self,request,timeout):
        self.calls+=1;return Response(json.dumps(self.manifest).encode() if self.calls==1 else self.raw,request.full_url)
class Tests(unittest.TestCase):
    def fixture(self):
        raw=b'Run,Event,E1\n1,2,3.5\n';entry={'key':'events.csv','size':len(raw),'checksum':'adler32:'+format(zlib.adler32(raw)&0xffffffff,'08x')}
        return {'id':'5200','metadata':{'title':'source','_files':[entry]}},raw
    def test_verified_rows_and_identity(self):
        doc,raw=self.fixture()
        with tempfile.TemporaryDirectory() as d:
            x=fetch.acquire('5200','events.csv',d,client=Client(doc,raw));self.assertEqual(x['status'],'acquired');self.assertEqual(x['row_count'],1);self.assertTrue(x['checksum_verified'])
    def test_corruption_is_failure(self):
        doc,raw=self.fixture()
        with tempfile.TemporaryDirectory() as d:self.assertEqual(fetch.acquire('5200','events.csv',d,client=Client(doc,raw.replace(b'3.5',b'9.9')))['status'],'failed')
    def test_wrong_record_and_missing_file(self):
        for wrong in ('record','file'):
            doc,raw=self.fixture()
            if wrong=='record':doc['id']='999'
            else:doc['metadata']['_files']=[]
            with tempfile.TemporaryDirectory() as d:self.assertEqual(fetch.acquire('5200','events.csv',d,client=Client(doc,raw))['status'],'failed')
    def test_unsafe_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):fetch.acquire('5200','../events.csv',d)
if __name__=='__main__':unittest.main()
