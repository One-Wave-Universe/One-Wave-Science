#!/usr/bin/env python3
"""Diameter involution on the 12-rail."""
from __future__ import annotations

import json


def I(n: int) -> int:
    return (n + 6) % 12


def T(n: int) -> int:
    return (n + 7) % 12


def run():
    fixed = [n for n in range(12) if I(n) == n]
    involution = all(I(I(n)) == n for n in range(12))
    commute = all(I(T(n)) == T(I(n)) for n in range(12))
    pairs = [[n, I(n)] for n in range(6)]
    return {
        "job": "diameter_involution",
        "brick": "YELLOW",
        "I": "n + 6 mod 12",
        "T": "n + 7 mod 12  (+7 ≡ -5)",
        "fixed_points": fixed,
        "pairs": pairs,
        "I2_is_id": involution,
        "IT_equals_TI": commute,
        "I_major_047": sorted({I(x) for x in (0, 4, 7)}),
        "I_minor_037": sorted({I(x) for x in (0, 3, 7)}),
        "I_aug_048": sorted({I(x) for x in (0, 4, 8)}),
        "pass": involution and commute and fixed == [],
        "honest": "Z/12 identities. Not a physical field. Not T6.",
        "not_this_job": ["T6 REBASE", "Mass Effect", "semitones"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
