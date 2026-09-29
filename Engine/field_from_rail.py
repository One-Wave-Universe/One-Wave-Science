#!/usr/bin/env python3
"""12-rail: 12=0, diameter through 6 is the mirror, +7≡-5 and -7≡+5."""
from __future__ import annotations

import json
import math


def hop_packet(N: int) -> dict:
    return {"N": N, "TOP": 2 * N, "plus": 2 * N + 1, "minus": 2 * N - 1}


def fifth_step(n: int, sign: int = 1) -> int:
    return (n + sign * 7) % 12


def mirror6(n: int) -> int:
    return (n + 6) % 12


def run():
    pkt = hop_packet(6)
    omega = 2 * math.pi * 7 / 12 / pkt["TOP"]
    mirrors = {n: mirror6(n) for n in range(12)}
    diameter = all(mirror6(mirror6(n)) == n for n in range(12))
    six_is_zero = mirror6(0) == 6 and mirror6(6) == 0
    both_dirs = (7 % 12 == (-5) % 12) and ((-7) % 12 == 5 % 12)
    return {
        "job": "field_from_rail",
        "brick": "YELLOW",
        "packet": pkt,
        "rule": "12 is 0. Across 6 o'clock from any tonic is the mirror note.",
        "omega_field": omega,
        "mirror_table": mirrors,
        "mirror0_is_6": mirror6(0),
        "mirror6_is_0": mirror6(6),
        "twelve_is_0": 12 % 12,
        "plus7_is_minus5": 7 % 12 == (-5) % 12,
        "minus7_is_plus5": (-7) % 12 == 5 % 12,
        "diameter_involution": diameter,
        "pass": both_dirs and six_is_zero and diameter and 12 % 12 == 0,
        "honest": "Clock identities only. Not T6. Not semitones.",
        "not_this_job": ["T6 REBASE", "Mass Effect", "semitones"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
