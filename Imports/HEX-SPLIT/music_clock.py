#!/usr/bin/env python3
"""E-510 overlay on the hex split. One Wave names only.

6 notes. Those 6 are the mirror notes.
6 pyramids × {Express, Compress} = 12 clock slots (views, not 12 animals).
Express ↔ Compress is Mirror (B-205) through the plane.
Opposite pyramids share a midline. That is the 3.
Tritone is a Gray sticker. It is not an ID.
"""
from __future__ import annotations

GRAY_STICKERS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def pyramids() -> list[dict]:
    out = []
    for i in range(6):
        pid = i + 1
        out.append(
            {
                "id": pid,
                "express": f"E{pid}",
                "compress": f"C{pid}",
                "opposite": ((i + 3) % 6) + 1,
                "gray_face_sticker": GRAY_STICKERS[i],
                "gray_flip_sticker": GRAY_STICKERS[i + 6],
            }
        )
    return out


def midlines(ps: list[dict]) -> list[tuple[int, int]]:
    seen = set()
    pairs = []
    for p in ps:
        pair = tuple(sorted((p["id"], p["opposite"])))
        if pair not in seen:
            seen.add(pair)
            pairs.append(pair)
    return pairs


def main() -> None:
    ps = pyramids()
    print("HEX-SPLIT music clock — One Wave")
    print("pyramid  express  compress  midline  [gray stickers, optional]")
    for p in ps:
        print(
            f"  P{p['id']}     {p['express']:<3}     {p['compress']:<3}      P{p['opposite']}"
            f"     {p['gray_face_sticker']}/{p['gray_flip_sticker']}"
        )
    print()
    print("midlines (M4 candidates — pick one, freeze):")
    for a, b in midlines(ps):
        print(f"  P{a} — P{b}")
    print()
    print("law: 6 notes. Those 6 are the mirror notes.")
    print("      Express ↔ Compress = Mirror on the same note.")
    print("hold: 1(0)1")


if __name__ == "__main__":
    main()
