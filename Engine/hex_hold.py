#!/usr/bin/env python3
"""Three blobs on an axial hex under g=-alpha nabla chi wakes.
Hold = stay inside R-1 for the last third of steps.
Yellow. Last official receipt was 0/5. This may fail again.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_chi_wakes import chi_from_wakes, grad_chi, nest_wakes  # noqa: E402


def hex_sites(R=4):
    pts = []
    for q in range(-R, R + 1):
        for r in range(-R, R + 1):
            if abs(q + r) <= R:
                x = math.sqrt(3) * (q + r / 2.0)
                y = 1.5 * r
                pts.append((q, r, x, y))
    return pts


def run(R=4, steps=180, alpha=1.8, dt=0.04, damp=0.08):
    parent, locals_ = nest_wakes(6)
    wakes = [parent] + locals_
    blobs = [{"x": w["x"], "y": w["y"], "vx": 0.0, "vy": 0.15 * (1 if i else -1)} for i, w in enumerate(locals_)]
    rim = 1.5 * R
    inside = [0, 0, 0]
    tail = max(steps // 3, 1)
    for t in range(steps):
        for i, b in enumerate(blobs):
            gx, gy = grad_chi(b["x"], b["y"], wakes)
            b["vx"] = (b["vx"] - alpha * gx * dt) * (1.0 - damp)
            b["vy"] = (b["vy"] - alpha * gy * dt) * (1.0 - damp)
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
            if t >= steps - tail and math.hypot(b["x"], b["y"]) < rim:
                inside[i] += 1
    held = sum(1 for n in inside if n > tail * 0.7)
    ends = [[round(b["x"], 3), round(b["y"], 3)] for b in blobs]
    return {
        "job": "hex_hold",
        "brick": "YELLOW",
        "held": held,
        "n": 3,
        "ends": ends,
        "inside_tail": inside,
        "tail": tail,
        "pass": held == 3,
        "honest": "pass only if all three stay inside rim for 70% of the last third",
        "prior_receipt": "0 locked / 5 failed",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
