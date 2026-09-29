#!/usr/bin/env python3
"""Job: motion under g = -α ∇χ from nested wakes.

Kill test: drop parent wake → path must change.
Paint path is not this path.

Yellow. Science only. No T6. No Mass Effect.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_chi_wakes import grad_chi, nest_wakes  # noqa: E402


def step(x, y, vx, vy, wakes, alpha=2.4, dt=0.03, damp=0.02):
    gx, gy = grad_chi(x, y, wakes)
    ax, ay = -alpha * gx, -alpha * gy
    vx = (vx + ax * dt) * (1.0 - damp)
    vy = (vy + ay * dt) * (1.0 - damp)
    return x + vx * dt, y + vy * dt, vx, vy


def trajectory(wakes, steps=400, x0=8.0, y0=1.2, vx0=0.0, vy0=0.35):
    x, y, vx, vy = x0, y0, vx0, vy0
    path = []
    for _ in range(steps):
        x, y, vx, vy = step(x, y, vx, vy, wakes)
        path.append((x, y))
    return path


def path_l2(a, b) -> float:
    n = min(len(a), len(b))
    return math.sqrt(sum((a[i][0] - b[i][0]) ** 2 + (a[i][1] - b[i][1]) ** 2 for i in range(n)) / n)


def paint_force_traj(steps=400, x0=8.0, y0=1.2, vx0=0.0, vy0=0.35, depth=1.0, sigma=2.0, alpha=2.4, dt=0.03, damp=0.02):
    x, y, vx, vy = x0, y0, vx0, vy0
    path = []
    for _ in range(steps):
        r2 = x * x + y * y
        G = depth * math.exp(-r2 / (2 * sigma * sigma))
        gx = G * (-x / (sigma * sigma))
        gy = G * (-y / (sigma * sigma))
        ax, ay = -alpha * gx, -alpha * gy
        vx = (vx + ax * dt) * (1.0 - damp)
        vy = (vy + ay * dt) * (1.0 - damp)
        x += vx * dt
        y += vy * dt
        path.append((x, y))
    return path


def run():
    parent, locals_ = nest_wakes(6)
    full = [parent] + locals_
    p_full = trajectory(full)
    p_no = trajectory(locals_)
    p_paint = paint_force_traj()
    d_parent = path_l2(p_full, p_no)
    d_paint = path_l2(p_full, p_paint)
    parent_alt = dict(parent)
    parent_alt["sigma"] = float(parent["packet"]["N"])
    p_wrong_sigma = trajectory([parent_alt] + locals_)
    d_sigma = path_l2(p_full, p_wrong_sigma)
    ok = d_parent > 0.05 and d_paint > 0.05 and d_sigma > 0.02
    return {
        "job": "wake_chi_stepper",
        "brick": "YELLOW",
        "packet": parent["packet"],
        "end_full": [round(p_full[-1][0], 4), round(p_full[-1][1], 4)],
        "end_no_parent": [round(p_no[-1][0], 4), round(p_no[-1][1], 4)],
        "end_paint": [round(p_paint[-1][0], 4), round(p_paint[-1][1], 4)],
        "L2_drop_parent": d_parent,
        "L2_vs_paint": d_paint,
        "L2_wrong_parent_sigma": d_sigma,
        "pass": ok,
        "rule": "g=-α∇χ_wakes. Drop parent or change TOP → path changes. Paint path ≠ wake path.",
        "not_this_job": ["hex hold", "omega_s from field", "Mass Effect", "T6"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
