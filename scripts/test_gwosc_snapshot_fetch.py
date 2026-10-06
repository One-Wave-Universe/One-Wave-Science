import hashlib,io,json,tarfile,tempfile,unittest
from pathlib import Path
from gwosc_snapshot_fetch import verify,inspect,CAP
class Tests(unittest.TestCase):
    def test_corruption_and_size_mismatch_are_rejected(self):
        raw=b'provider archive';entry={'size':len(raw),'checksum':'md5:'+hashlib.md5(raw).hexdigest()}
        self.assertEqual(verify(raw,entry),hashlib.sha256(raw).hexdigest())
        for broken in [b'Provider archive',raw+b'x']:
            with self.assertRaises(ValueError):verify(broken,entry)
    def test_event_identity_and_no_archive_path_extraction(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'snapshot.tar'
            with tarfile.open(p,'w') as t:
                for name,doc in [('snapshot-2025-10-31/GWTC/GW150914-v3.json',{'events':{'GW150914-v3':{'GPS':1126259462.4}}}),('../untrusted.json',{'metadata':True})]:
                    raw=json.dumps(doc).encode();m=tarfile.TarInfo(name);m.size=len(raw);t.addfile(m,io.BytesIO(raw))
            records,raw=inspect(p,'GW150914-v3');self.assertEqual(len(records),2)
            self.assertFalse((Path(d).parent/'untrusted.json').exists())
            with self.assertRaises(ValueError):inspect(p,'GW150914-v99')
if __name__=='__main__':unittest.main()
