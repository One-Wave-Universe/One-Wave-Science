#!/usr/bin/env python3
"""3-body on shared parent wake. No 1/r point singularity.

Newton pairwise 1/r^2 is Gray comparison only.
Relay: chi = W_parent + sum local. Common envelope, not FTL.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_chi_wakes import wake_kernel, hop_packet  # noqa: E402


def chi_and_grad(x, y, parent, bodies, skip=None, h=1e-3):
    def c(xx, yy):
        s = parent["amp"] * wake_kernel(
            math.hypot(xx - parent["x"], yy - parent["y"]), parent["sigma"]
        )
        for i, b in enumerate(bodies):
            if skip is not None and i == skip:
                continue
            s += b["amp"] * wake_kernel(math.hypot(xx - b["x"], yy - b["y"]), b["sigma"])
        return s

    gx = (c(x + h, y) - c(x - h, y)) / (2 * h)
    gy = (c(x, y + h) - c(x, y - h)) / (2 * h)
    return c(x, y), gx, gy


def newton_pair(bodies, i, G=0.35, soft=0.25):
    ax = ay = 0.0
    bi = bodies[i]
    for j, bj in enumerate(bodies):
        if j == i:
            continue
        dx, dy = bj["x"] - bi["x"], bj["y"] - bi["y"]
        r2 = dx * dx + dy * dy + soft * soft
        r = math.sqrt(r2)
        f = G * bj["amp"] / r2
        ax += f * dx / r
        ay += f * dy / r
    return ax, ay


def step_relay(bodies, parent, alpha=2.2, dt=0.03, damp=0.03):
    acc = []
    for i, b in enumerate(bodies):
        _, gx, gy = chi_and_grad(b["x"], b["y"], parent, bodies, skip=i)
        acc.append((-alpha * gx, -alpha * gy))
    for b, (ax, ay) in zip(bodies, acc):
        b["vx"] = (b["vx"] + ax * dt) * (1.0 - damp)
        b["vy"] = (b["vy"] + ay * dt) * (1.0 - damp)
        b["x"] += b["vx"] * dt
        b["y"] += b["vy"] * dt


def step_newton(bodies, dt=0.03, damp=0.03):
    acc = [newton_pair(bodies, i) for i in range(len(bodies))]
    for b, (ax, ay) in zip(bodies, acc):
        b["vx"] = (b["vx"] + ax * dt) * (1.0 - damp)
        b["vy"] = (b["vy"] + ay * dt) * (1.0 - damp)
        b["x"] += b["vx"] * dt
        b["y"] += b["vy"] * dt


def spread(bodies):
    cx = sum(b["x"] for b in bodies) / 3.0
    cy = sum(b["y"] for b in bodies) / 3.0
    return math.sqrt(sum((b["x"] - cx) ** 2 + (b["y"] - cy) ** 2 for b in bodies) / 3.0)


def trio(scale=1.6):
    out = []
    for k in range(3):
        ang = 2 * math.pi * k / 3
        out.append(
            {
                "x": scale * math.cos(ang),
                "y": scale * math.sin(ang),
                "vx": -0.12 * math.sin(ang),
                "vy": 0.12 * math.cos(ang),
                "amp": 0.28,
                "sigma": 6.0,
            }
        )
    return out


def run(steps=280):
    pkt = hop_packet(6)
    parent = {"x": 0.0, "y": 0.0, "amp": 1.0, "sigma": float(pkt["TOP"])}
    dead = {"x": 0.0, "y": 0.0, "amp": 0.0, "sigma": float(pkt["TOP"])}
    relay, newton, nop = trio(), trio(), trio()
    s_r, s_n, s_d = [], [], []
    for _ in range(steps):
        step_relay(relay, parent)
        step_newton(newton)
        step_relay(nop, dead)
        s_r.append(spread(relay))
        s_n.append(spread(newton))
        s_d.append(spread(nop))
    tail = steps // 4

    def mean(a):
        t = a[-tail:]
        return sum(t) / len(t)

    mr, mn, md = mean(s_r), mean(s_n), mean(s_d)
    k0 = wake_kernel(0.0, 6.0)
    return {
        "job": "three_body_relay",
        "brick": "YELLOW",
        "packet": pkt,
        "kernel_at_zero": k0,
        "kernel_finite_at_point": k0 < 1e9,
        "spread_tail_relay_with_parent": mr,
        "spread_tail_newton_pairwise": mn,
        "spread_tail_relay_no_parent": md,
        "parent_tightens": mr < md,
        "pass": (k0 < 1e9) and (mr < md),
        "rule": "Shared parent wake relays curvature. Drop parent -> wider triad. Kernel finite at r=0.",
        "not_solved": "Poincare closed form, solar system, Mass Effect, T6",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
