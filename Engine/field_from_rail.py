#!/usr/bin/env python3
"""Fifths field rate using 0, ±5, 6. No hour named 7-11."""
from __future__ import annotations

import json
import math


def hop_packet(N: int) -> dict:
    return {"N": N, "TOP": 2 * N, "plus": 2 * N + 1, "minus": 2 * N - 1}


def run():
    pkt = hop_packet(6)
    # fifth step is +5 forward or -5 back; same length
    omega = 2 * math.pi * 5 / 12 / pkt["TOP"]
    labels = list(range(-5, 6)) + [6]
    return {
        "job": "field_from_rail",
        "brick": "YELLOW",
        "packet": pkt,
        "labels": labels,
        "named_7_11": [n for n in labels if n >= 7],
        "step_back": -5,
        "step_forward": 5,
        "across": 6,
        "omega_field": omega,
        "plus7_is_not_a_seat": True,
        "pass": 7 not in labels and 11 not in labels and labels[0] == -5,
        "honest": "omega uses step 5 on a 12-count under the hood. Spoken circle has no 7-11.",
        "not_this_job": ["chromatic hours", "T6", "Mass Effect"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
