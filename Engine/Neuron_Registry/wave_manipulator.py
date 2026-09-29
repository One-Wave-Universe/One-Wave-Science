#!/usr/bin/env python3
"""Sandbox wave manipulator. Writes only under Engine/Neuron_Registry/cells."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CELLS = ROOT / "cells"
REG = ROOT / "REGISTRY.json"


def label(p: int) -> int:
    r = p % 12
    return r - 12 if r > 6 else r


def run(steps: int = 12) -> dict:
    reg = json.loads(REG.read_text())
    ids = {c["id"] for c in reg["cells"]}
    assert ids == {"N0", "N6", "Nf", "Nb"}
    f = b = 0
    trace = []
    for i in range(steps + 1):
        lf, lb = label(f), label(b)
        choice_f = 1 if lf != 6 else 0
        choice_b = -1 if lb != 6 else 0
        if i == 0:
            choice_f = choice_b = 0
        trace.append({"t": i, "fwd": lf, "back": lb})
        (CELLS / "Nf" / "STATE.json").write_text(
            json.dumps({"id": "Nf", "seat": lf, "choice": choice_f, "step": 5}, indent=2)
        )
        (CELLS / "Nb" / "STATE.json").write_text(
            json.dumps({"id": "Nb", "seat": lb, "choice": choice_b, "step": -5}, indent=2)
        )
        (CELLS / "N0" / "STATE.json").write_text(
            json.dumps({"id": "N0", "seat": 0, "choice": 0, "meet": lf == 0 and lb == 0}, indent=2)
        )
        (CELLS / "N6" / "STATE.json").write_text(
            json.dumps({"id": "N6", "seat": 6, "choice": 0, "meet": lf == 6 and lb == 6}, indent=2)
        )
        f += 5
        b -= 5
    meet6 = any(x["fwd"] == 6 and x["back"] == 6 for x in trace)
    home = trace[-1]["fwd"] == 0 and trace[-1]["back"] == 0
    return {
        "job": "wave_manipulator",
        "brick": "YELLOW",
        "sandbox": str(CELLS),
        "trace": trace,
        "meet_6": meet6,
        "home_0": home,
        "pass": meet6 and home,
        "honest": "Sandbox only. Does not write Nodes/. Not a wet neuron.",
        "not_this_job": ["T6", "Mass Effect", "biological neuron"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
