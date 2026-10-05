#!/usr/bin/env python3
"""See → gate → drum → hear → speak.

Bar clock is the HEX-SPLIT fifths walk (clock.py).
Guitar stub lands on Express polarity. Mouth only speaks if the drum hit.
"""
from __future__ import annotations

import argparse

from clock import slot_at
from senses import Drum, Ear, Eye, Mouth

DEAD = 0.08


def gate(motion: float, guitar: bool) -> int:
    drive = motion + (0.2 if guitar else 0.0)
    if abs(drive) < DEAD:
        return 0
    return 1 if drive > 0 else -1


def bar(t: int, eye: Eye, ear: Ear, drum: Drum, mouth: Mouth) -> dict:
    slot = slot_at(t)
    frame = eye.grab(t)
    guitar = slot["polarity"] == "express"
    decision = gate(frame.motion, guitar)
    hit = drum.hit(frame.motion + 0.25 * decision) if decision >= 0 else False
    heard = ear.hear(hit, guitar)
    word = slot["gray"] if hit else ""
    spoken = mouth.say(word)
    return {
        "t": t,
        "gray_eye": round(frame.mean, 3),
        "motion": round(frame.motion, 3),
        "gate": decision,
        "hit": hit,
        "guitar": guitar,
        "slot": slot["tag"],
        "note": slot["gray"],
        "midi": slot["midi"],
        "heard": heard["room"],
        "said": spoken,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--beats", type=int, default=12)
    args = p.parse_args()
    eye, ear, drum, mouth = Eye(), Ear(), Drum(), Mouth()
    print("BUCKET-R2 loop  ·  clock = fifths weave")
    print(f"{'t':>3} {'eye':>6} {'mot':>6} {'g':>3} {'hit':>5} {'gtr':>5} {'slot':<6} {'note':<3} {'said'}")
    for t in range(args.beats):
        r = bar(t, eye, ear, drum, mouth)
        print(
            f"{r['t']:3d} {r['gray_eye']:6.3f} {r['motion']:6.3f} {r['gate']:3d} "
            f"{str(r['hit']):>5} {str(r['guitar']):>5} {r['slot']:<6} {r['note']:<3} {r['said']}"
        )


if __name__ == "__main__":
    main()
