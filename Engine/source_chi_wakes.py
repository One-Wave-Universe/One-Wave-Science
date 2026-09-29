#!/usr/bin/env python3
"""D-413 source χ from nested wakes, not a painted well.

Curvature is top-down: parent wake (octave-up / hop TOP) plus local event leftovers.
g = -α ∇χ. Painted Gaussian is demo-only and must fail the promotion test.

Yellow. No T6. No Builds.
"""
from __future__ import annotations

import json
import math
from typing import Iterable


def hop_packet(N: int) -> dict:
    if not (1 <= N <= 12):
        raise ValueError("N on 1..12 rail")
    return {"N": N, "TOP": 2 * N, "plus": 2 * N + 1, "minus": 2 * N - 1}


def wake_kernel(r: float, sigma: float) -> float:
    """Leftover field of one event. Soft Yukawa. No 1/r pole, no painted Gaussian well."""
    s = max(sigma, 1e-9)
    return math.exp(-r / s) / math.sqrt(r * r + 0.04 * s * s)


def chi_from_wakes(points, wakes: Iterable[dict]) -> list[float]:
    out = []
    for x, y in points:
        s = 0.0
        for w in wakes:
            r = math.hypot(x - w["x"], y - w["y"])
            s += w["amp"] * wake_kernel(r, w["sigma"])
        out.append(s)
    return out


def grad_chi(x, y, wakes, h=1e-3) -> tuple[float, float]:
    def c(xx, yy):
        return chi_from_wakes([(xx, yy)], wakes)[0]

    gx = (c(x + h, y) - c(x - h, y)) / (2 * h)
    gy = (c(x, y + h) - c(x, y - h)) / (2 * h)
    return gx, gy


def lap_chi(x, y, wakes, h=1e-3) -> float:
    def c(xx, yy):
        return chi_from_wakes([(xx, yy)], wakes)[0]

    return (c(x + h, y) + c(x - h, y) + c(x, y + h) + c(x, y - h) - 4 * c(x, y)) / (h * h)


def painted_gaussian(points, depth=1.0, sigma=2.0):
    return [depth * math.exp(-(x * x + y * y) / (2 * sigma * sigma)) for x, y in points]


def nest_wakes(parent_N: int):
    pkt = hop_packet(parent_N)
    parent = {
        "x": 0.0,
        "y": 0.0,
        "amp": 1.0,
        "sigma": float(pkt["TOP"]),
        "name": "PARENT_WAKE",
        "packet": pkt,
    }
    locals_ = []
    for k, name in enumerate(("A", "B", "C")):
        ang = 2 * math.pi * k / 3
        locals_.append(
            {
                "x": 1.6 * math.cos(ang),
                "y": 1.6 * math.sin(ang),
                "amp": 0.28,
                "sigma": float(parent_N),
                "name": f"LOCAL_{name}",
            }
        )
    return parent, locals_


def run():
    parent, locals_ = nest_wakes(6)
    wakes = [parent] + locals_
    pts = [(i * 0.4, 0.0) for i in range(-15, 16)]
    chi = chi_from_wakes(pts, wakes)
    chi_no_parent = chi_from_wakes(pts, locals_)
    paint = painted_gaussian(pts)
    mid = 15
    parent_delta = max(abs(a - b) for a, b in zip(chi, chi_no_parent))
    gx, gy = grad_chi(0.0, 0.0, wakes)
    lap0 = lap_chi(0.0, 0.0, wakes)
    ok = (
        chi[mid] > chi[0]
        and parent_delta > 0.05
        and parent["packet"]["TOP"] == 12
        and parent["packet"]["plus"] == 13
    )
    return {
        "job": "D-413 source_chi from nested wakes",
        "brick": "YELLOW",
        "chi_center": chi[mid],
        "chi_edge": chi[0],
        "parent_removed_delta": parent_delta,
        "grad_at_origin": [gx, gy],
        "lap_chi_origin": lap0,
        "paint_ignores_parent": True,
        "packet": parent["packet"],
        "rule": "χ = parent_wake(TOP) + Σ local leftovers. g=-α∇χ. Paint may demo, must not promote.",
        "pass": ok,
        "note": "Well in official D-413 HTML remains imposed (audit 31). This file is the un-painted source law.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
