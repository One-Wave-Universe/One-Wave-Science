#!/usr/bin/env python3
"""Field rotation from hop rail + fifth, not a typed 0.07.

Y2 CLOCKWISE = +7 on the 12-cycle. +7 ≡ -5 (mod 12).
12 = next cycle 0. 13 = next +1.
No semitones. No T6 REBASE.
"""
from __future__ import annotations

import json
import math


def hop_packet(N: int) -> dict:
    if not (1 <= N <= 12):
        raise ValueError("N on 1..12")
    return {"N": N, "TOP": 2 * N, "plus": 2 * N + 1, "minus": 2 * N - 1}


def fifth_step(n: int, sign: int = 1) -> int:
    # CLOCKWISE +7, COUNTERCLOCKWISE -7 ≡ +5 the other way; user: +7 ≡ -5
    return (n + sign * 7) % 12


def field_rate(packet: dict) -> dict:
    top = packet["TOP"]
    # one fifth of the 12-rail, per parent octave (TOP)
    omega = 2 * math.pi * 7 / 12 / top
    L = (1.0 + math.cos(2 * math.pi * 7 / 12)) / 2.0
    return {
        "omega_field": omega,
        "L_fifth": L,
        "plus7_mod12": 7 % 12,
        "minus5_mod12": (-5) % 12,
        "twelve_is_next_0": 12 % 12,
        "thirteen_is_next_plus1": 13 - 12,
    }


def run():
    pkt = hop_packet(6)
    fr = field_rate(pkt)
    walk = [0]
    n = 0
    for _ in range(12):
        n = fifth_step(n, +1)
        walk.append(n)
    return {
        "job": "field_from_rail",
        "brick": "YELLOW",
        "packet": pkt,
        "Y": {"Y1": "AXIS=parent", "Y2": "CLOCKWISE=+7", "Y3": "ROTATE"},
        "Z6": {"RATIO": "7/12", "PHASE": "fifth vs unison", "LOCK": "not T6"},
        **fr,
        "fifths_walk_mod12": walk,
        "imposed_0_07_is_this": abs(fr["omega_field"] - 0.07) < 1e-6,
        "pass": fr["plus7_mod12"] == fr["minus5_mod12"] and walk[-1] == 0,
        "honest": "omega_field is rail algebra. It is not the typed 0.07. q recursion not committed. T6 denied.",
        "not_this_job": ["T6 REBASE", "Mass Effect", "semitones"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
