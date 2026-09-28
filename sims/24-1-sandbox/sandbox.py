#!/usr/bin/env python3
"""Headless 24→1 sandbox registry/validator. No third-party dependencies."""
from __future__ import annotations
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent
SCHEMA="one-wave-sandbox-module/v1"

def load_manifests():
    out=[]
    for p in sorted((ROOT/"modules").glob("*/manifest.json")):
        try: m=json.loads(p.read_text())
        except Exception as e: out.append({"_path":str(p),"_error":str(e)}); continue
        m["_path"]=str(p); out.append(m)
    return out

def validate(m):
    errors=[]
    for k in ("id","name","version","slot","claim_gate","dimensions","solver","render","controls","fixtures","validation"):
        if k not in m: errors.append("missing:"+k)
    if m.get("schema")!=SCHEMA: errors.append("schema")
    s=m.get("slot"); 
    if not isinstance(s,int) or not 1<=s<=24: errors.append("slot:must-be-1..24")
    if m.get("render",{}).get("solver_independent") is not True: errors.append("render:must-be-solver-independent")
    return errors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
    ms=load_manifests(); seen={}; report=[]
    for m in ms:
        e=[m["_error"]] if "_error" in m else validate(m)
        if not e:
            if m["slot"] in seen: e.append("duplicate-slot")
            seen[m["slot"]]=m.get("id")
        report.append({"id":m.get("id"),"slot":m.get("slot"),"path":m.get("_path"),"errors":e})
    ok=all(not x["errors"] for x in report)
    payload={"schema":SCHEMA,"modules":report,"occupied_slots":sorted(seen),"ok":ok}
    print(json.dumps(payload,indent=2) if a.json else "\n".join(f'{x["slot"]}: {x["id"]} '+("PASS" if not x["errors"] else "FAIL "+",".join(x["errors"])) for x in report))
    raise SystemExit(0 if ok else 2)
if __name__=="__main__": main()
