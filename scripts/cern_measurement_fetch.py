#!/usr/bin/env python3
"""Acquire manifest-verified CERN CSV measurement products without changing their units."""
import argparse,csv,hashlib,io,json,pathlib,re,zlib
from urllib.parse import quote,urlparse
from urllib.request import Request,build_opener
from science_archive_search import CheckedRedirect,MAX_BYTES
from open_data_fetch import utc_now
HOSTS={'opendata.cern.ch'}
def read(client,url,timeout):
    with client.open(Request(url,headers={'User-Agent':'One-Wave-Science/measurement-acquisition'}),timeout=timeout) as r:
        final=urlparse(r.geturl())
        if final.scheme!='https' or final.hostname not in HOSTS:raise ValueError('Unexpected provider host')
        raw=r.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:raise ValueError('Response exceeded 2 MiB cap')
        return raw

def verify(raw,entry):
    if len(raw)!=entry['size']:raise ValueError('CERN manifest size mismatch')
    expected=entry.get('checksum','')
    actual='adler32:'+format(zlib.adler32(raw)&0xffffffff,'08x')
    if not expected.startswith('adler32:') or actual!=expected:raise ValueError('CERN manifest checksum mismatch or unsupported checksum')
    rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    if not rows or any(None in x or any(v is None for v in x.values()) for x in rows):raise ValueError('Empty or malformed CSV measurement table')
    return rows

def acquire(record,file,output,timeout=30,client=None):
    if not re.fullmatch(r'[0-9]{1,9}',record):raise ValueError('CERN record must be a numeric identifier')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+\.csv',file):raise ValueError('Select one CSV basename')
    out=pathlib.Path(output);out.mkdir(parents=True,exist_ok=True)
    receipt={'schema':'one-wave-cern-measurement-v1','provider':'CERN Open Data','record':record,'file':file,'retrieved_at_utc':utc_now(),'classification':'externally_sourced_measurement_product','units_policy':'Preserve source labels; units require the linked record/analysis documentation before conversion','not_equivalent_to':'HEPData publication tables or One-Wave physical proof'}
    try:
        client=client or build_opener(CheckedRedirect(HOSTS))
        url='https://opendata.cern.ch/api/records/'+record
        manifest=read(client,url,timeout);(out/'record.raw.json').write_bytes(manifest)
        doc=json.loads(manifest)
        if str(doc.get('id'))!=record:raise ValueError('Returned record does not match requested identifier')
        entries=doc.get('files',doc.get('metadata',{}).get('_files',[]))
        entry=next((x for x in entries if x.get('key')==file),None)
        if entry is None:raise ValueError('Requested CSV absent from CERN manifest')
        if not 0<entry['size']<=MAX_BYTES:raise ValueError('Manifest file exceeds permitted size')
        url='https://opendata.cern.ch/record/'+record+'/files/'+quote(file)
        raw=read(client,url,timeout);(out/file).write_bytes(raw)
        receipt.update(url=url,manifest_sha256=hashlib.sha256(manifest).hexdigest(),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),published_checksum=entry.get('checksum'))
        rows=verify(raw,entry)
        (out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')
        receipt.update(status='acquired',checksum_verified=True,row_count=len(rows),columns=list(rows[0]),source_title=doc['metadata'].get('title'),source_license=doc['metadata'].get('license'))
    except Exception as exc:receipt.update(status='failed',error=type(exc).__name__+': '+str(exc))
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt

def main():
    p=argparse.ArgumentParser();p.add_argument('--record',required=True);p.add_argument('--file',required=True);p.add_argument('--output',required=True);p.add_argument('--timeout',type=int,default=30);a=p.parse_args()
    if not 1<=a.timeout<=60:p.error('timeout must be 1..60 seconds')
    result=acquire(a.record,a.file,a.output,a.timeout);print(json.dumps(result));return 0 if result['status']=='acquired' else 1
if __name__=='__main__':raise SystemExit(main())
