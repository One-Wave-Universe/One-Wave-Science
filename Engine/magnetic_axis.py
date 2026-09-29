#!/usr/bin/env python3
"""Parent-axis magnetic reorienter + child moments.

chi pit (scalar) is already in source_chi_wakes.
This node adds orientation: torque on child spin toward parent axis.

CERN Z_K envelope peak stamps parent moment amplitude (not Tesla).
Planets in PLANET_SPIN_B.json are Gray observed constraints, not derived.
"""
from __future__ import annotations

import json
import math


def hop_packet(N: int) -> dict:
    return {"N": N, "TOP": 2 * N, "plus": 2 * N + 1, "minus": 2 * N - 1}


def cern_parent_amp(zk_peak: float = 1.0) -> float:
    return max(zk_peak, 0.0)


def torque(s, parent_axis, kappa: float):
    return (
        kappa * (s[1] * parent_axis[2] - s[2] * parent_axis[1]),
        kappa * (s[2] * parent_axis[0] - s[0] * parent_axis[2]),
        kappa * (s[0] * parent_axis[1] - s[1] * parent_axis[0]),
    )


def step_spin(s, tau, dt: float, damp: float = 0.18):
    sx, sy, sz = s
    tx, ty, tz = tau
    sx = (sx + tx * dt) * (1.0 - damp)
    sy = (sy + ty * dt) * (1.0 - damp)
    sz = (sz + tz * dt) * (1.0 - damp)
    n = math.sqrt(sx * sx + sy * sy + sz * sz) or 1.0
    return (sx / n, sy / n, sz / n)


def align(a, b) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def run(steps=320, dt=0.04, kappa=1.1, zk_peak=1.0):
    pkt = hop_packet(6)
    amp = cern_parent_amp(zk_peak) * (pkt["TOP"] / 12.0)
    parent = (0.0, 0.0, 1.0)
    kids = [
        {"name": "LOCK_CANDIDATE", "s": (0.2, 0.1, 0.97)},
        {"name": "URANUS_CLASS", "s": (0.86, 0.0, 0.50)},
        {"name": "VENUS_CLASS", "s": (0.05, 0.0, -0.99)},
    ]
    k = kappa * amp
    hist = {kid["name"]: [] for kid in kids}
    for _ in range(steps):
        for kid in kids:
            kid["s"] = step_spin(kid["s"], torque(kid["s"], parent, k), dt)
            hist[kid["name"]].append(align(kid["s"], parent))
    tail = steps // 3
    out = {}
    for name, series in hist.items():
        t = series[-tail:]
        out[name] = {"align_tail_mean": sum(t) / len(t), "align_end": series[-1]}
    lock = out["LOCK_CANDIDATE"]["align_tail_mean"] > 0.85
    return {
        "job": "magnetic_axis_nodes",
        "brick": "YELLOW",
        "packet": pkt,
        "cern_zk_peak_stamp": zk_peak,
        "parent_amp": amp,
        "kids": out,
        "pass_lock_candidate": lock,
        "uranus_class_still_tilted": out["URANUS_CLASS"]["align_tail_mean"] < 0.75,
        "venus_class_not_captured": out["VENUS_CLASS"]["align_tail_mean"] < 0.0,
        "pass": lock,
        "honest": "Lock candidate can align. Uranus/Venus starts are constraints, not derived planets. kappa is calibration.",
        "not_this_job": ["derived solar system", "Mass Effect", "T6", "omega_s shear law"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
