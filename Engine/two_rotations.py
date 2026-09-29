#!/usr/bin/env python3
"""Two mirrored rotations: +5 and -5. They meet at 6 and close at 0."""
from __future__ import annotations

import json


def walk(step: int, start: int = 0, n: int = 12):
    p, out = start, [start]
    for _ in range(n):
        p = p + step
        # keep spoken labels in -5..6, wrap 12-count under the hood
        r = p % 12
        if r > 6:
            r = r - 12  # 7..11 become -5..-1
        out.append(r)
    return out


def run():
    fwd = walk(+5)
    back = walk(-5)
    # first time each hits 6
    meet_f = next(i for i, x in enumerate(fwd) if x == 6)
    meet_b = next(i for i, x in enumerate(back) if x == 6)
    close_f = next(i for i, x in enumerate(fwd[1:], 1) if x == 0)
    close_b = next(i for i, x in enumerate(back[1:], 1) if x == 0)
    return {
        "job": "two_opposing_rotations",
        "brick": "YELLOW",
        "forward_+5": fwd,
        "back_-5": back,
        "meet_at_6_forward_steps": meet_f,
        "meet_at_6_back_steps": meet_b,
        "close_at_0_forward_steps": close_f,
        "close_at_0_back_steps": close_b,
        "pass": meet_f == 6 and meet_b == 6 and close_f == 12 and close_b == 12,
        "honest": "Two mirrored walks. Labels stay -5..+5 and 6. Residue 7-11 folded back to -5..-1.",
        "not_this_job": ["chromatic hours 7-11", "T6", "Mass Effect"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
