#!/usr/bin/env python3
"""Scan One_Wave_Bench/runs for receipts and write runs/manifest.json.
The bench UI reads this so human + AI see the identical set of real runs.
Also fold each receipt's raw arrays into a compact form for browser charts."""
from __future__ import annotations
import json, csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs"

def load_series(csvp: Path, keys):
    if not csvp.exists(): return {}
    rows = list(csv.DictReader(csvp.open()))
    return {k: [float(r[k]) for r in rows] for k in keys if rows and k in rows[0]}

entries = []
for rcp in sorted(RUNS.rglob("receipt_*.json")):
    d = json.loads(rcp.read_text())
    run_dir = rcp.parent
    cases = []
    for c in d.get("cases", []):
        csvp = run_dir / c.get("csv", "")
        series = load_series(csvp, ["t", "x", "y", "well_distance", "spin", "max_strain"])
        cases.append({
            "name": c["name"],
            "parameters": c.get("parameters", {}),
            "measurements": c.get("measurements", {}),
            "series": series,
        })
    entries.append({
        "receipt_id": d["receipt_id"],
        "request_id": d["request_id"],
        "author": d.get("author", d.get("provenance", {}).get("author", "ai")),
        "hypothesis": d.get("hypothesis", ""),
        "falsifiers": d.get("falsifiers", []),
        "status": d.get("status", "YELLOW"),
        "native_dimension": d.get("native_dimension", "2D"),
        "checks": d.get("checks", {}),
        "all_checks_pass": d.get("all_checks_pass", False),
        "interpretation": d.get("interpretation", ""),
        "generated_utc": d.get("provenance", {}).get("generated_utc", ""),
        "cases": cases,
        "receipt_rel": str(rcp.relative_to(RUNS.parent)),
    })

manifest = {"engine": "D-413", "stage": "01", "run_count": len(entries), "runs": entries}
(RUNS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"manifest.json written: {len(entries)} runs")
for e in entries:
    print(f"  {e['request_id']}  ({e['author']})  cases={len(e['cases'])}  pass={e['all_checks_pass']}")
