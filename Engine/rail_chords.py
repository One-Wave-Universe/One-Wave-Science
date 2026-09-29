#!/usr/bin/env python3
"""Chords on the 12-rail around local 0.

-5 (0) 4+  Major (leans +4)
-5 (0) 3+  Minor (leans +3)
-5 (0) 5+  or  -4 (0) 4+  Augmented, no directional lean
"""
from __future__ import annotations

import json


def pc(*steps):
    return sorted({s % 12 for s in steps})


def run():
    major = pc(-5, 0, 4)   # {7,0,4} = {0,4,7}
    minor = pc(-5, 0, 3)   # {7,0,3} = {0,3,7}
    aug_55 = pc(-5, 0, 5)  # {7,0,5}
    aug_44 = pc(-4, 0, 4)  # {8,0,4} = {0,4,8}
    return {
        "job": "rail_chords",
        "brick": "YELLOW",
        "rule": "-5(0)4+ Major; -5(0)3+ Minor; -5(0)5+ or -4(0)4+ Augmented no lean",
        "major": {"shape": "-5(0)4+", "pcs": major, "is_047": major == [0, 4, 7]},
        "minor": {"shape": "-5(0)3+", "pcs": minor, "is_037": minor == [0, 3, 7]},
        "aug_pm5": {"shape": "-5(0)5+", "pcs": aug_55, "span_equal": True},
        "aug_pm4": {"shape": "-4(0)4+", "pcs": aug_44, "is_048": aug_44 == [0, 4, 8]},
        "mirror6_of_major_third": (4 + 6) % 12,
        "pass": major == [0, 4, 7] and minor == [0, 3, 7] and aug_44 == [0, 4, 8],
        "honest": "Pitch-class shapes on the rail. Not a key theory. No semitone naming.",
        "not_this_job": ["T6", "Mass Effect", "semitones"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
