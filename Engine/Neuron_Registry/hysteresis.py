#!/usr/bin/env python3
"""Process is the memory. q keeps a hysteresis path. Not a chip image."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CELLS = ROOT / "cells"

R, G, QMAX = 0.92, 0.24, 1.0
PARTIAL_ENTER, PARTIAL_EXIT = 0.4, 0.28
FULL_ENTER, FULL_EXIT = 0.82, 0.68


def clip(x: float) -> float:
    return max(-QMAX, min(QMAX, x))


def band(q: float, prev: str) -> str:
    a = abs(q)
    if prev == "full":
        if a < FULL_EXIT:
            prev = "partial" if a >= PARTIAL_EXIT else "unity"
        return prev if q != 0 else "unity"
    if prev == "partial":
        if a >= FULL_ENTER:
            return "full"
        if a < PARTIAL_EXIT:
            return "unity"
        return "partial"
    if a >= FULL_ENTER:
        return "full"
    if a >= PARTIAL_ENTER:
        return "partial"
    return "unity"


def step_q(q: float, choice: int, L: float = 1.0) -> float:
    # q(n+1) = clip(r q + g b m d L); m=d=1 here
    return clip(R * q + G * choice * L)


def run(n: int = 12) -> dict:
    qf = qb = 0.0
    bf = bb = "unity"
    path = []
    for t in range(n + 1):
        seat_f = [0, 5, -2, 3, -4, 1, 6, -1, 4, -3, 2, -5, 0][min(t, 12)]
        seat_b = [0, -5, 2, -3, 4, -1, 6, 1, -4, 3, -2, 5, 0][min(t, 12)]
        cf = 0 if seat_f in (0, 6) else 1
        cb = 0 if seat_b in (0, 6) else -1
        if t:
            qf = step_q(qf, cf)
            qb = step_q(qb, cb)
            bf = band(qf, bf)
            bb = band(qb, bb)
        path.append({"t": t, "qf": round(qf, 4), "qb": round(qb, 4), "bf": bf, "bb": bb, "sf": seat_f, "sb": seat_b})
        for name, q, ch, seat in (("Nf", qf, cf, seat_f), ("Nb", qb, cb, seat_b)):
            p = CELLS / name / "STATE.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({"id": name, "q": q, "choice": ch, "seat": seat, "band": bf if name == "Nf" else bb}, indent=2))
    return {
        "job": "hysteresis_process_memory",
        "brick": "YELLOW",
        "rule": "memory is the q path, not a snapshot file",
        "r": R,
        "g": G,
        "path": path,
        "pass": path[6]["sf"] == 6 and path[-1]["sf"] == 0,
        "honest": "r,g are working calibration. Process trace is the memory. Not T6.",
        "not_this_job": ["chip RAM", "T6", "Mass Effect"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
