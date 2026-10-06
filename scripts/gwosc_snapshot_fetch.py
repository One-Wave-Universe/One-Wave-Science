#!/usr/bin/env python3
"""Checksum-verified dated GWOSC fallback. Never marks the live API healthy."""
import argparse,hashlib,json,re,tarfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request,build_opener
from science_archive_search import acquire,CheckedRedirect
CAP=16*1024*1024

def verify(raw,entry):
    if len(raw)>CAP or len(raw)!=entry['size']:raise ValueError('Snapshot size mismatch or cap exceeded')
    if entry['checksum']!='md5:'+hashlib.md5(raw).hexdigest():raise ValueError('Provider checksum mismatch')
    return hashlib.sha256(raw).hexdigest()

def inspect(path,event):
    records=[];selected=None
    with tarfile.open(path) as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.endswith('.json'):continue
            if member.size>2*1024*1024:raise ValueError('JSON member exceeds cap')
            raw=archive.extractfile(member).read();doc=json.loads(raw)
            records.append({'member':member.name,'sha256':hashlib.sha256(raw).hexdigest()})
            if member.name==f'snapshot-2025-10-31/GWTC/{event}.json':
                if event not in doc.get('events',{}):raise ValueError('Event identity mismatch')
                selected=raw
    if not records or selected is None:raise ValueError('Snapshot lacks requested event')
    return records,selected

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--event',default='GW150914-v3');a=p.parse_args()
    if not re.fullmatch(r'GW[0-9_]+-v[0-9]+',a.event):p.error('Event must be a versioned GW identifier')
    a.output.mkdir(parents=True,exist_ok=True)
    receipt={'source':'gwosc-snapshot','release_id':17496685,'snapshot_date':'2025-10-31','live_api_healthy':False,'scope':'Historical event metadata, not live run inventory or downloaded strain'}
    try:
        manifest=acquire('gwosc-snapshot','','',3,a.output/'manifest')
        if manifest['status']!='acquired':raise ValueError(manifest['error'])
        doc=json.loads((a.output/'manifest/provider.raw').read_bytes());entry=next(x for x in doc['files'] if x['key']=='IGWN-GWOSC-snapshot-2025-10-31.tar')
        url=entry['links']['self']
        if urlparse(url).scheme!='https' or urlparse(url).hostname!='zenodo.org':raise ValueError('Unexpected download host')
        path=a.output/entry['key']
        if path.exists():raw=path.read_bytes()
        else:
            with build_opener(CheckedRedirect({'zenodo.org'})).open(Request(url),timeout=30) as r:raw=r.read(CAP+1)
        sha=verify(raw,entry);path.write_bytes(raw)
        records,selected=inspect(path,a.event);(a.output/(a.event+'.json')).write_bytes(selected)
        receipt.update(status='verified',download_url=url,bytes=len(raw),provider_checksum=entry['checksum'],sha256=sha,json_members=len(records),members=records,event=a.event,event_sha256=hashlib.sha256(selected).hexdigest(),manifest_sha256=manifest['sha256'])
    except Exception as e:receipt.update(status='failed',error=f'{type(e).__name__}: {e}')
    (a.output/'snapshot-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='members'}))
    return int(receipt['status']!='verified')
if __name__=='__main__':raise SystemExit(main())
