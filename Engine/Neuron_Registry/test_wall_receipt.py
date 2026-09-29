#!/usr/bin/env python3
"""Sandbox wall receipt: prove runtime writes stay under cells/*/STATE.json."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
NODES = REPO / "Nodes"


def digest_tree(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            h.update(path.relative_to(root).as_posix().encode())
            h.update(hashlib.sha256(path.read_bytes()).digest())
    return h.hexdigest()


before_nodes = digest_tree(NODES)
before_status = subprocess.run(
    ["git", "-C", str(REPO), "status", "--porcelain", "--", "Nodes"],
    text=True, capture_output=True, check=True
).stdout

subprocess.run([sys.executable, str(ROOT / "wave_manipulator.py")], check=True, capture_output=True, text=True)
subprocess.run([sys.executable, str(ROOT / "hysteresis.py")], check=True, capture_output=True, text=True)
subprocess.run([sys.executable, str(ROOT / "linkage.py"), "--apply"], check=True, capture_output=True, text=True)

after_nodes = digest_tree(NODES)
after_status = subprocess.run(
    ["git", "-C", str(REPO), "status", "--porcelain", "--", "Nodes"],
    text=True, capture_output=True, check=True
).stdout

cell_states = {}
for cid in ("N0","N6","Nf","Nb"):
    p = ROOT / "cells" / cid / "STATE.json"
    cell_states[cid] = json.loads(p.read_text())

ok = (
    before_nodes == after_nodes
    and before_status == after_status
    and all("linkage" in s for s in cell_states.values())
    and cell_states["N0"].get("choice") == 0
    and cell_states["N6"].get("choice") == 0
    and cell_states["Nf"].get("choice") in (0,1)
    and cell_states["Nb"].get("choice") in (0,-1)
)

receipt = {
    "job": "neuron_registry_wall_receipt",
    "brick": "YELLOW",
    "nodes_unchanged": before_nodes == after_nodes,
    "nodes_git_status_unchanged": before_status == after_status,
    "registered_cells": sorted(cell_states),
    "linkage_present": all("linkage" in s for s in cell_states.values()),
    "wall_held": ok,
    "honest": "Proves this test path did not write Nodes/. Does not prove biological/neural equivalence.",
}
print(json.dumps(receipt, indent=2, sort_keys=True))
raise SystemExit(0 if ok else 2)
