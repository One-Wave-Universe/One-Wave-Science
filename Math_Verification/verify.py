#!/usr/bin/env python3
"""Reference-based, standard-library-only mathematical controls. No physics overclaims."""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "registry.json"

def frequency(n):
    return 440.0 * 2.0 ** (n / 12.0)

def close(a, b, rel=1e-11):
    return math.isclose(a, b, rel_tol=rel, abs_tol=1e-11)

def tests():
    return {
        "octave": close(frequency(12), 880) and close(frequency(-12), 220),
        "fifth": close(frequency(7) / frequency(0), 2**(7/12)) and abs(2**(7/12)-1.5)>0.001,
        "wrapping": all(close(frequency(n+12), 2*frequency(n)) for n in range(-24,25)),
        "crossing": close(1000/(2*frequency(0)), 1.1363636363636365),
        "transposition": all(close(frequency(n+7)/frequency(n), 2**(7/12)) for n in (-5,0,4)),
        "major_minor": close(frequency(4)/frequency(3), 2**(1/12)),
        "balanced": close(frequency(-4)*frequency(4), frequency(0)**2),
        "phase": close(math.sin(math.pi), 0, rel=1e-9) and not close(math.sin(math.pi/2), 0),
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--all",action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--list",action="store_true")
    args=parser.parse_args()
    reg=json.loads(REGISTRY.read_text())
    models=reg["models"]
    if args.list:
        print(json.dumps([m["id"] for m in models]))
        return 0
    if not args.all and not args.model:
        parser.error("choose --all, --model ID, or --list")
    chosen=[m for m in models if args.all or m["id"]==args.model]
    if not chosen:
        print(json.dumps({"error":"unknown model","model":args.model}))
        return 2
    required={"id","owner","source","canonical_math_reference","evidence_class","equations","assumptions","units","tests","physical_hypotheses"}
    results={}
    for m in chosen:
        missing=sorted(required-set(m))
        if missing:
            results[m.get("id","unnamed")]={"pass":False,"error":"missing registry fields","fields":missing}
            continue
        absent=[p for p in [m["source"],m["canonical_math_reference"]] if not (ROOT.parent/p).is_file()]
        if absent:
            results[m["id"]]={"pass":False,"error":"missing source references","paths":absent}
            continue
        known=tests()
        results[m["id"]]={"pass":all(known.get(k,False) for k in m["tests"]),"tests":{k:known.get(k,False) for k in m["tests"]},"evidence_class":m["evidence_class"],"unverified":m["physical_hypotheses"]}
    ok=bool(results) and all(x["pass"] for x in results.values())
    print(json.dumps({"pass":ok,"models":results},indent=2))
    return 0 if ok else 1

if __name__=="__main__":
    raise SystemExit(main())
