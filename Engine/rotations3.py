#!/usr/bin/env python3
"""Potential, slope, and three rotations: point, path, field.

V = chi
slope = nabla chi
point: spin rate of s-hat
path: theta-dot of position about parent
field: parent-axis rate (imposed in this smoke)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_chi_wakes import grad_chi, nest_wakes, chi_from_wakes  # noqa: E402


def wrap(dth: float) -> float:
    return (dth + math.pi) % (2 * math.pi) - math.pi


def run(steps=200, dt=0.04, alpha=2.0, kappa=1.1, damp=0.06):
    parent, locals_ = nest_wakes(6)
    wakes = [parent] + locals_
    x, y = locals_[0]["x"], locals_[0]["y"]
    vx, vy = 0.0, 0.18
    s = [0.2, 0.1, 0.97]
    field_rate = 0.07
    phi_f = 0.0
    pot, sl, point_w, path_w, field_w = [], [], [], [], []
    th_last = math.atan2(y, x)
    for _ in range(steps):
        phi_f += field_rate * dt
        axis = [0.0, 0.0, 1.0]
        gx, gy = grad_chi(x, y, wakes)
        V = chi_from_wakes([(x, y)], wakes)[0]
        slope = math.hypot(gx, gy)
        vx = (vx - alpha * gx * dt) * (1.0 - damp)
        vy = (vy - alpha * gy * dt) * (1.0 - damp)
        x += vx * dt
        y += vy * dt
        th = math.atan2(y, x)
        w_path = wrap(th - th_last) / dt
        th_last = th
        tx = kappa * (s[1] * axis[2] - s[2] * axis[1])
        ty = kappa * (s[2] * axis[0] - s[0] * axis[2])
        tz = kappa * (s[0] * axis[1] - s[1] * axis[0])
        s[0] = (s[0] + tx * dt) * (1.0 - 0.15)
        s[1] = (s[1] + ty * dt) * (1.0 - 0.15)
        s[2] = (s[2] + tz * dt) * (1.0 - 0.15)
        n = math.sqrt(s[0] ** 2 + s[1] ** 2 + s[2] ** 2) or 1.0
        s[0], s[1], s[2] = s[0] / n, s[1] / n, s[2] / n
        pot.append(V)
        sl.append(slope)
        point_w.append(math.hypot(tx, ty, tz))
        path_w.append(w_path)
        field_w.append(field_rate)
    def tail(a):
        t = a[len(a) // 2 :]
        return sum(t) / len(t)
    return {
        "job": "slope_potential_rotations3",
        "brick": "YELLOW",
        "packet": parent["packet"],
        "potential_tail": tail(pot),
        "slope_tail": tail(sl),
        "point_rotation_tail": tail(point_w),
        "path_rotation_tail": tail(path_w),
        "field_rotation_tail": tail(field_w),
        "levels": {
            "point": "spin s-hat of a node",
            "path": "theta-dot of node about parent",
            "field": "parent-axis rate (imposed here, not derived)",
        },
        "pass": tail(sl) > 0 and math.isfinite(tail(pot)),
        "honest": "Field rotation is an imposed rate in this smoke. Path/point are measured. Not 3-body solved.",
        "not_this_job": ["Mass Effect", "T6", "omega_s = 3 tau/2"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
