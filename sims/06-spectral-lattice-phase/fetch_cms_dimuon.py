#!/usr/bin/env python3
"""Fetch the official CMS 2010 dimuon CSV from CERN Open Data record 700.

Writes immutable source bytes plus a compact G-767 scale CSV.
Conventional muon/dimuon terminology is provenance metadata, not simulator ontology.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,pathlib,urllib.request

RECORD="https://opendata.cern.ch/record/700"
API="https://opendata.cern.ch/api/records/700"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="data"); a=ap.parse_args()
    out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=True)
    meta=json.load(urllib.request.urlopen(API,timeout=30))
    files=meta.get("files",[])
    csvs=[f for f in files if str(f.get("key","")).lower().endswith(".csv")]
    if not csvs: raise SystemExit("record 700 API returned no CSV files")
    # Prefer the full 100k file: largest CSV in the official record.
    f=max(csvs,key=lambda x:int(x.get("size",0)))
    url=f.get("uri") or f.get("links",{}).get("self")
    if url and url.startswith("/"): url="https://opendata.cern.ch"+url
    if not url: raise SystemExit("CSV has no download URI")
    raw=urllib.request.urlopen(url,timeout=120).read()
    raw_path=out/pathlib.Path(f["key"]).name; raw_path.write_bytes(raw)
    sha=hashlib.sha256(raw).hexdigest()
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    scale_path=out/"cms_record700_g767_scales.csv"
    kept=0
    with scale_path.open("w",newline="",encoding="utf-8") as h:
        w=csv.writer(h); w.writerow(["scale","width","uncertainty","label"])
        for r in rows:
            # Official schema calls invariant mass M (GeV).
            v=r.get("M") or r.get("m")
            if not v: continue
            try: x=float(v)
            except ValueError: continue
            if x>0: w.writerow([format(x,".12g"),"","","CMS-record-700"]); kept+=1
    provenance={"source_record":RECORD,"api":API,"download_url":url,"source_file":f["key"],
      "sha256":sha,"rows_in":len(rows),"positive_scales_out":kept,"unit":"GeV",
      "observable":"experiment-provided invariant mass M","ontology_rule":"source labels retained as metadata only"}
    (out/"cms_record700_provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
    print(json.dumps(provenance,sort_keys=True))
if __name__=="__main__": main()
