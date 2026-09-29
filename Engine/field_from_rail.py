#!/usr/bin/env python3
"""Field rotation from hop rail + fifth.

+7 is the same step as -5 the other way.
-7 is the same step as +5 the other way.
12 = next 0. 13 = next +1. No semitones. No T6.
"""
from __future__ import annotations

import json
import math


def hop_packet(N: int) -> dict:
    if not (1 <= N <= 12):
        raise ValueError("N on 1..12")
    return {"N": N, "TOP": 2 * N, "plus": 2 * N + 1, "minus": 2 * N - 1}


def fifth_step(n: int, sign: int = 1) -> int:
    return (n + sign * 7) % 12


def field_rate(packet: dict) -> dict:
    top = packet["TOP"]
    omega = 2 * math.pi * 7 / 12 / top
    L = (1.0 + math.cos(2 * math.pi * 7 / 12)) / 2.0
    return {
        "omega_field": omega,
        "L_fifth": L,
        "plus7_mod12": 7 % 12,
        "minus5_mod12": (-5) % 12,
        "minus7_mod12": (-7) % 12,
        "plus5_mod12": 5 % 12,
        "twelve_is_next_0": 12 % 12,
        "thirteen_is_next_plus1": 13 - 12,
    }


def run():
    pkt = hop_packet(6)
    fr = field_rate(pkt)
    cw, ccw = [0], [0]
    n = m = 0
    for _ in range(12):
        n = fifth_step(n, +1)
        m = fifth_step(m, -1)
        cw.append(n)
        ccw.append(m)
    both = (
        fr["plus7_mod12"] == fr["minus5_mod12"]
        and fr["minus7_mod12"] == fr["plus5_mod12"]
        and cw[-1] == 0
        and ccw[-1] == 0
    )
    return {
        "job": "field_from_rail",
        "brick": "YELLOW",
        "packet": pkt,
        "rule": "+7 same as -5 other direction; -7 same as +5 other direction",
        **fr,
        "clockwise_walk_+7": cw,
        "counterclockwise_walk_-7": ccw,
        "imposed_0_07_is_this": abs(fr["omega_field"] - 0.07) < 1e-6,
        "pass": both,
        "honest": "Both directions are one rail. Not semitones. Not T6.",
        "not_this_job": ["T6 REBASE", "Mass Effect", "semitones"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
