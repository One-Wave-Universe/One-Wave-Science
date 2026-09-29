#!/usr/bin/env python3
"""omega_s from the moving triad, not an overlay spring.

omega = d theta / dt of blob-0 around the triad centroid.
Compare omega^2 to 3*tau/2 with tau = 1/parent_sigma (octave-up scale).
Prior hex receipt: rel err ~ 1. This may fail again.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_chi_wakes import grad_chi, nest_wakes  # noqa: E402


def angle_about_centroid(blobs):
    cx = sum(b["x"] for b in blobs) / 3.0
    cy = sum(b["y"] for b in blobs) / 3.0
    return math.atan2(blobs[0]["y"] - cy, blobs[0]["x"] - cx), cx, cy


def run(steps=200, alpha=1.8, dt=0.04, damp=0.08):
    parent, locals_ = nest_wakes(6)
    wakes = [parent] + locals_
    tau = 1.0 / max(parent["sigma"], 1e-9)
    theory = 1.5 * tau
    blobs = [{"x": w["x"], "y": w["y"], "vx": 0.0, "vy": 0.12 * (1 if i else -1)} for i, w in enumerate(locals_)]
    th0, _, _ = angle_about_centroid(blobs)
    omegas = []
    last = th0
    for _ in range(steps):
        for b in blobs:
            gx, gy = grad_chi(b["x"], b["y"], wakes)
            b["vx"] = (b["vx"] - alpha * gx * dt) * (1.0 - damp)
            b["vy"] = (b["vy"] - alpha * gy * dt) * (1.0 - damp)
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
        th, _, _ = angle_about_centroid(blobs)
        dth = (th - last + math.pi) % (2 * math.pi) - math.pi
        omegas.append(dth / dt)
        last = th
    tail = omegas[len(omegas) // 2 :]
    w = sum(tail) / len(tail)
    w2 = w * w
    rel = abs(w2 - theory) / max(theory, 1e-12)
    return {
        "job": "omega_s_from_field",
        "brick": "YELLOW",
        "packet": parent["packet"],
        "tau": tau,
        "theory_omega_s2": theory,
        "mean_omega_tail": w,
        "mean_omega2_tail": w2,
        "rel_err": rel,
        "pass": rel < 0.35,
        "honest": "pass bar 35% is a smoke gate, not the D-413 shear law",
        "prior": "omega_s2 rel err mean 0.999977 on hex lock receipt",
        "not_this_job": ["Mass Effect", "T6", "official D-413 well"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
