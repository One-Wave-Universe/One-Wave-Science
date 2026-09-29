#!/usr/bin/env python3
"""Symmetries of the 12-rail / chromatic circle."""
from __future__ import annotations

import json

UNITS = (1, 5, 7, 11)


def R(n: int) -> int:
    return (n + 1) % 12


def I(n: int) -> int:
    return (n + 6) % 12


def S(n: int) -> int:
    return (-n) % 12


def mul(a: int, n: int) -> int:
    return (a * n) % 12


def order(a: int) -> int:
    x = 1
    for k in range(1, 13):
        x = (x * a) % 12
        if x == 1:
            return k
    return -1


def run():
    orders = {a: order(a) for a in UNITS}
    involution = all(I(I(n)) == n for n in range(12))
    t6_is_I = all(I(n) == (n + 7 * 6) % 12 for n in range(12))
    commute_IS = all(S(I(S(n))) == I(n) for n in range(12))
    dihedral = all(S(S(n)) == n and S(R(S(n))) == (n - 1) % 12 for n in range(12))
    aut_closed = all((a * b) % 12 in UNITS for a in UNITS for b in UNITS)
    return {
        "job": "chromatic_circle_symmetries",
        "brick": "YELLOW",
        "units_Aut_Z12": list(UNITS),
        "unit_orders": orders,
        "plus7_is_minus5": 7 % 12 == (-5) % 12,
        "minus7_is_plus5": (-7) % 12 == 5 % 12,
        "T6_is_diameter_I": t6_is_I,
        "I2_id": involution,
        "S_fixes_0_and_6": [n for n in range(12) if S(n) == n],
        "S_major_047": sorted({S(x) for x in (0, 4, 7)}),
        "S_minor_037": sorted({S(x) for x in (0, 3, 7)}),
        "times7_major": sorted({mul(7, x) for x in (0, 4, 7)}),
        "dihedral_SR": dihedral,
        "S_conjugates_I_to_I": commute_IS,
        "Aut_closed": aut_closed,
        "pass": involution and t6_is_I and dihedral and aut_closed and orders[7] == 2,
        "honest": "Clock group only. times-7 is the fifth map, not a new particle.",
        "not_this_job": ["T6 REBASE", "Mass Effect", "semitones"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
