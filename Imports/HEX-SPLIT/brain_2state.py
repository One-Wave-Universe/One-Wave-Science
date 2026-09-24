#!/usr/bin/env python3
"""2-state brain. Field explores. Void checks. That is the whole organ.

Not GPU. Not a committee. Two lives of 1(0)1.
Brainstem (outside this file) picks live gate. Body is nerve_cell.py.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Thought:
    seq: int
    lean: float
    live: int
    engage: int
    why: str


class Brain:
    """Field lists. Void may set engage=0. Hold is no new lean."""

    def __init__(self) -> None:
        self.seq = 0
        self.last_lean = 0.0
        self.hold = True

    def field(self, want_lean: float, want_live: int) -> tuple[float, int]:
        lean = max(-1.0, min(1.0, float(want_lean)))
        live = int(want_live) % 3
        return lean, live

    def void(self, lean: float, seen_i_g: float, seen_hall: float, override: bool) -> tuple[int, str]:
        if override:
            return 0, "override"
        if abs(lean) < 0.05:
            return 0, "hold"
        if abs(seen_i_g) > 2.0:
            return 0, "vagus too loud"
        if abs(seen_hall) > 2.0:
            return 0, "location lie"
        return 1, "pass"

    def tick(
        self,
        want_lean: float,
        want_live: int,
        seen_i_g: float = 0.0,
        seen_hall: float = 0.0,
        override: bool = False,
    ) -> Thought:
        lean, live = self.field(want_lean, want_live)
        engage, why = self.void(lean, seen_i_g, seen_hall, override)
        self.hold = engage == 0
        if engage:
            self.last_lean = lean
        self.seq += 1
        return Thought(self.seq, lean if engage else 0.0, live, engage, why)


def demo() -> None:
    b = Brain()
    print("2-STATE BRAIN  Field lists  Void checks")
    rows = [
        b.tick(0.0, 0),
        b.tick(0.8, 0),
        b.tick(0.8, 0, override=True),
        b.tick(-0.8, 1),
        b.tick(0.5, 2, seen_i_g=3.0),
    ]
    print(f"{'seq':>4} {'eng':>3} {'live':>4} {'lean':>6}  why")
    for t in rows:
        print(f"{t.seq:4d} {t.engage:3d} {t.live:4d} {t.lean:6.2f}  {t.why}")
    assert rows[0].engage == 0 and rows[0].why == "hold"
    assert rows[1].engage == 1
    assert rows[2].engage == 0 and rows[2].why == "override"
    assert rows[3].engage == 1 and rows[3].live == 1
    assert rows[4].engage == 0 and rows[4].why == "vagus too loud"
    print("hold: 1(0)1")


if __name__ == "__main__":
    demo()
