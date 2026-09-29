#!/usr/bin/env python3
"""Fifths circle labels: 0, ±1..5, 6. No named 7-11."""
from __future__ import annotations

import json

LABELS = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]


def run():
    named_seven_to_eleven = [n for n in LABELS if n in (7, 8, 9, 10, 11)]
    plus7_is_minus5 = ((+7) % 12) == ((-5) % 12)
    minus7_is_plus5 = ((-7) % 12) == ((+5) % 12)
    return {
        "job": "fifths_circle_labels",
        "brick": "YELLOW",
        "labels": LABELS,
        "named_7_through_11": named_seven_to_eleven,
        "plus7_same_step_as_minus5": plus7_is_minus5,
        "minus7_same_step_as_plus5": minus7_is_plus5,
        "across_from_0": 6,
        "across_from_6": 0,
        "pass": named_seven_to_eleven == [] and plus7_is_minus5 and minus7_is_plus5,
        "honest": "7 is not a fifths-circle hour. It is the other-direction name of -5.",
        "not_this_job": ["chromatic hour names", "T6", "Mass Effect"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
