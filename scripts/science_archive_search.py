#!/usr/bin/env python3
"""Bounded public archive search/relay with exact response receipts."""
import argparse,csv,hashlib,io,json,pathlib,re,subprocess,sys
from urllib.parse import urlencode,urlparse
from urllib.request import Request,build_opener,HTTPRedirectHandler
from open_data_fetch import load_registry,source_by_id,allowed_hosts,utc_now
MAX_BYTES=2*1024*1024

class CheckedRedirect(HTTPRedirectHandler):
    def __init__(self,hosts):self.hosts=hosts
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        p=urlparse(newurl)
        if p.scheme!="https" or p.hostname not in self.hosts:raise ValueError("Undeclared redirect host")
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def route(source,query,record,limit):
    if source=="cern-open-data":return "https://opendata.cern.ch/api/records/?"+urlencode({"q":query or "CMS","size":limit}),None,"json"
    if source=="hepdata":return "https://www.hepdata.net/search/?"+urlencode({"q":query or "Higgs","format":"json"}),None,"json"
    if source=="gwosc":return "https://gwosc.org/api/v2/runs",None,"json"
    if source=="dandi":return "https://api.dandiarchive.org/api/dandisets/?"+urlencode({"page_size":limit,"search":query}),None,"json"
    if source=="openneuro":
        if record:
            if not re.fullmatch(r"ds[0-9]{6}",record):raise ValueError("OpenNeuro record must be ds plus six digits")
            q='query { dataset(id: '+json.dumps(record)+') { id name } }'
        else:
            if query:raise ValueError("OpenNeuro use --record for a targeted query; listing is not global text search")
            q='query { datasets(first: '+str(limit)+') { edges { node { id name } } } }'
        return "https://openneuro.org/crn/graphql",json.dumps({"query":q}).encode(),"json"
    if source=="physionet-eeg":return "https://physionet.org/files/eegmmidb/1.0.0/RECORDS",None,"text"
    if source=="gaia-archive":
        return "https://gea.esac.esa.int/tap-server/tap/sync?"+urlencode({"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","MAXREC":limit,"QUERY":"SELECT TOP "+str(limit)+" source_id,ra,dec FROM gaiadr3.gaia_source"}),None,"csv"
    if source in ("eso","alma"):
        root="https://archive.eso.org/tap_obs/sync" if source=="eso" else "https://almascience.eso.org/tap/sync"
        return root+"?"+urlencode({"REQUEST":"doQuery","LANG":"ADQL","FORMAT":"csv","MAXREC":limit,"QUERY":"SELECT TOP "+str(limit)+" obs_id, s_ra, s_dec FROM ivoa.obscore"}),None,"csv"
    if source=="desi":return "https://data.desi.lbl.gov/public/dr1/",None,"html"
    raise ValueError("Use archive_metadata_query.py for MAST, HEASARC, Gaia native queries")

def acquire(source,query,record,limit,output,timeout=30,opener=None):
    if not 1<=limit<=10:raise ValueError("limit must be 1..10")
    entry=source_by_id(load_registry(),source);hosts=allowed_hosts(entry)
    url,data,kind=route(source,query,record,limit)
    if urlparse(url).hostname not in hosts:raise ValueError("Source host not registered")
    output=pathlib.Path(output);output.mkdir(parents=True,exist_ok=True)
    receipt={"schema":"one-wave-archive-search-v1","source":source,"query":query,"record":record,"limit":limit,"requested_url":url,"retrieved_at_utc":utc_now(),"classification":"provider_metadata_not_measurements","method":"POST" if data else "GET"}
    if data:receipt["request_body_sha256"]=hashlib.sha256(data).hexdigest();receipt["request_body"]=json.loads(data)
    try:
        client=opener or build_opener(CheckedRedirect(hosts))
        req=Request(url,data=data,headers={"User-Agent":"One-Wave-Science/metadata-relay","Accept":"application/json" if kind=="json" else "*/*",**({"Content-Type":"application/json"} if data else {})})
        with client.open(req,timeout=timeout) as response:
            raw=response.read(MAX_BYTES+1)
            if len(raw)>MAX_BYTES:raise ValueError("Response exceeded 2 MiB cap")
            final=response.geturl()
            if urlparse(final).scheme!="https" or urlparse(final).hostname not in hosts:raise ValueError("Final host not registered")
            receipt.update(http_status=response.status,final_url=final,content_type=response.headers.get("Content-Type"))
        (output/"provider.raw").write_bytes(raw)
        receipt.update(raw_file="provider.raw",sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
        if kind=="json":
            doc=json.loads(raw)
            if isinstance(doc,dict) and (doc.get("errors") or doc.get("status")=="ERROR"):raise ValueError("Provider returned application error: "+str(doc)[:1000])
            if source=="openneuro":rows=([doc["data"]["dataset"]] if record and doc["data"].get("dataset") else [x["node"] for x in doc["data"].get("datasets",{}).get("edges",[])])
            elif source=="cern-open-data":rows=doc.get("hits",{}).get("hits",[])
            elif source=="dandi":rows=doc.get("results",[])
            else:rows=doc.get("results",doc.get("runs",[])) if isinstance(doc,dict) else doc
            receipt["page_next"]=doc.get("next") if isinstance(doc,dict) else None
            (output/"provider.json").write_text(json.dumps(doc,indent=2))
        elif kind=="csv":
            text=raw.decode();rows=list(csv.DictReader(io.StringIO(text)))
            if text.lstrip().startswith("<"):raise ValueError("TAP returned XML/HTML rather than CSV")
        elif kind=="text":rows=[x for x in raw.decode().splitlines() if not query or query.lower() in x.lower()]
        else:
            if b"<html" not in raw.lower() and b"<!doctype" not in raw.lower():raise ValueError("Expected archive directory HTML")
            rows=re.findall(r'href="([^"]+)"',raw.decode(errors="replace"))
        receipt.update(status="acquired",returned_count=len(rows),sample=rows[:limit],scope="bounded provider page; no complete-catalog claim")
    except Exception as exc:receipt.update(status="failed",error=type(exc).__name__+": "+str(exc))
    (output/"receipt.json").write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt

def main():
    p=argparse.ArgumentParser();p.add_argument("source");p.add_argument("--query",default="");p.add_argument("--record",default="");p.add_argument("--limit",type=int,default=3);p.add_argument("--output",required=True);p.add_argument("--timeout",type=int,default=30);a=p.parse_args()
    if not 1<=a.timeout<=60:p.error("timeout must be 1..60 seconds")
    result=acquire(a.source,a.query,a.record,a.limit,a.output,a.timeout);print(json.dumps(result));return 0 if result["status"]=="acquired" else 1
if __name__=="__main__":raise SystemExit(main())
