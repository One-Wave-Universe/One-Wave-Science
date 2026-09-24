#!/usr/bin/env python3
"""Circle of fifths as a walk on the HEX-SPLIT 12-slot clock.

Gray stickers (C, C#, … B) are labels only. Identity lives on the pyramids:

    6 pyramids × {Express, Compress} = 12 clock slots
    Tritone = same pyramid, flip face  (already in music_clock.py)
    Perfect fifth = +7 chromatic steps = weave to another pyramid
    Perfect fourth = +5 = the other weave

The circle of fifths is the generator that visits every slot once
before closing. Opposite on the *fifths* circle is the tritone —
same pyramid, Express ↔ Compress. So the music-theory circle and
the hex split are one object read two ways.

No physics claim. This is a coordination grammar you can kick.
"""
from __future__ import annotations

from dataclasses import dataclass

from music_clock import GRAY_STICKERS, pyramids

FIFTH = 7
FOURTH = 5
TRITONE = 6


def gray_index(name: str) -> int:
    return GRAY_STICKERS.index(name)


def slot_for_gray(idx: int) -> dict:
    """Map a chromatic index onto pyramid + polarity."""
    idx = idx % 12
    if idx < 6:
        pyramid_id = idx + 1
        polarity = "express"
    else:
        pyramid_id = (idx - 6) + 1
        polarity = "compress"
    return {
        "gray": GRAY_STICKERS[idx],
        "idx": idx,
        "pyramid": pyramid_id,
        "polarity": polarity,
        "tag": f"P{pyramid_id}-{'E' if polarity == 'express' else 'C'}",
    }


def walk(start: str = "C", step: int = FIFTH) -> list[dict]:
    """Closed walk of length 12. step=7 fifths, step=5 fourths."""
    i0 = gray_index(start)
    out = []
    for k in range(12):
        idx = (i0 + k * step) % 12
        rec = slot_for_gray(idx)
        rec["step"] = k
        rec["interval"] = "P1" if k == 0 else ("TT" if (k * step) % 12 == TRITONE else f"+{(k * step) % 12}")
        out.append(rec)
    return out


def neighbors(name: str) -> dict:
    i = gray_index(name)
    return {
        "tonic": slot_for_gray(i),
        "fifth": slot_for_gray(i + FIFTH),
        "fourth": slot_for_gray(i + FOURTH),
        "tritone": slot_for_gray(i + TRITONE),
        "relative_minor_guess": slot_for_gray(i + 9),
    }


def diatonic_triads(tonic: str) -> list[dict]:
    """Major-scale triads as gray-sticker stacks. Expand later with modes."""
    i = gray_index(tonic)
    major = [0, 2, 4, 5, 7, 9, 11]
    qualities = ["M", "m", "m", "M", "M", "m", "dim"]
    degrees = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
    out = []
    for deg, q, off in zip(degrees, qualities, major):
        root = (i + off) % 12
        third = (root + (4 if q == "M" else 3)) % 12
        fifth = (root + (6 if q == "dim" else 7)) % 12
        out.append(
            {
                "degree": deg,
                "quality": q,
                "root": slot_for_gray(root),
                "third": slot_for_gray(third),
                "fifth": slot_for_gray(fifth),
            }
        )
    return out


@dataclass
class FifthsReceipt:
    start: str
    generator: int
    walk: list[dict]
    midlines_hit: list[str]


def receipt(start: str = "C", generator: int = FIFTH) -> FifthsReceipt:
    w = walk(start, generator)
    mid = []
    for rec in w:
        if rec["polarity"] == "compress":
            mid.append(f"P{rec['pyramid']} flip via {rec['gray']}")
    return FifthsReceipt(start=start, generator=generator, walk=w, midlines_hit=mid)


def main() -> None:
    print("CIRCLE OF FIFTHS ↔ HEX-SPLIT clock")
    print("generator = +7 (perfect fifth). Opposite on the circle = tritone = same pyramid flip.")
    print()
    ps = {p["id"]: p for p in pyramids()}
    r = receipt("C", FIFTH)
    print("step  gray  slot       pyramid-pair (face/flip)")
    for rec in r.walk:
        p = ps[rec["pyramid"]]
        print(
            f"  {rec['step']:02d}   {rec['gray']:<3}  {rec['tag']:<8}  "
            f"P{p['id']} {p['gray_face_sticker']}/{p['gray_flip_sticker']}"
        )
    print()
    n = neighbors("C")
    print("C neighborhood:")
    for k in ("tonic", "fifth", "fourth", "tritone"):
        s = n[k]
        print(f"  {k:<8} {s['gray']:<3} {s['tag']}")
    print()
    print("C major triads (gray stacks — kickable, not sacred):")
    for t in diatonic_triads("C"):
        print(
            f"  {t['degree']:<4} {t['root']['gray']}{t['quality']:<3}  "
            f"{t['root']['tag']} + {t['third']['tag']} + {t['fifth']['tag']}"
        )
    print()
    print("law: fifths weave pyramids. tritones flip one pyramid.")
    print("hold: 1(0)1")


if __name__ == "__main__":
    main()
