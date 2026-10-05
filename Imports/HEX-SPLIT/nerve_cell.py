#!/usr/bin/env python3
"""Three-winding nerve cell — kickable model.

BC-DC engage. TC-AC lean on ONE live winding. QC-RC one flip both ways.
Windings ARE memory. Mid / I_G is vagus. Hold = no drive, not empty memory.
"""
from __future__ import annotations

from dataclasses import dataclass, field

BELT = 0.05
TAU = 0.12
DT = 0.12
DECAY = 0.20
SHUT = 0.35


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


@dataclass
class Receipt:
    seq: int
    engage: int
    live_gate: int
    lean: float
    i_g: float
    g: float
    windings: tuple
    ternary: int
    stamp: str
    views: tuple
    action: tuple


@dataclass
class NerveCell:
    g: float = 0.0
    w: list = field(default_factory=lambda: [0.0, 0.0, 0.0])
    engage: int = 0
    live: int = 0
    seq: int = 0
    lean: float = 0.0

    def i_g(self) -> float:
        return sum(self.w)

    def ternary(self) -> int:
        x = self.i_g()
        if abs(x) < BELT:
            return 0
        return 1 if x > 0 else -1

    def stamp_of(self) -> str:
        if self.engage == 0 or abs(self.lean) < BELT:
            return "hold"
        return "commit"

    def tick(self, engage: int, live: int, lean: float) -> Receipt:
        self.engage = 1 if engage else 0
        self.live = int(live) % 3
        self.lean = clamp(float(lean), -1.0, 1.0)
        prev = list(self.w)

        for i in range(3):
            if i != self.live:
                self.w[i] *= 1.0 - SHUT

        if self.engage == 0 or abs(self.lean) < BELT:
            self.w[self.live] *= 1.0 - DECAY
            self.g += DT * (-self.g / TAU)
        else:
            self.w[self.live] += DT * (self.lean - self.w[self.live]) / TAU
            self.g += DT * (self.i_g() - self.g) / TAU

        action = tuple(self.w[i] - prev[i] for i in range(3))
        views = tuple(self.w)
        self.seq += 1
        st = self.stamp_of()
        tern = 0 if st == "hold" else (1 if self.lean > 0 else -1)
        return Receipt(
            seq=self.seq,
            engage=self.engage,
            live_gate=self.live,
            lean=self.lean,
            i_g=self.i_g(),
            g=self.g,
            windings=views,
            ternary=tern,
            stamp=st,
            views=views,
            action=action,
        )


def demo() -> None:
    cell = NerveCell()
    print("NERVE CELL  3 windings  mid=vagus  process=memory")
    print(f"{'seq':>4} {'eng':>3} {'g':>2} {'lean':>6} {'I_G':>7} {'tern':>5} {'stamp':<7} {'w0':>7} {'w1':>7} {'w2':>7}")

    def show(r: Receipt) -> Receipt:
        print(
            f"{r.seq:4d} {r.engage:3d} {r.live_gate:2d} {r.lean:6.2f} {r.i_g:7.3f} "
            f"{r.ternary:5d} {r.stamp:<7} {r.views[0]:7.3f} {r.views[1]:7.3f} {r.views[2]:7.3f}"
        )
        return r

    rest = show(cell.tick(0, 0, 0.0))
    assert rest.stamp == "hold" and abs(rest.i_g) < BELT

    right = show(cell.tick(1, 0, 0.9))
    assert right.stamp == "commit" and right.ternary == 1
    assert right.seq == rest.seq + 1
    assert abs(sum(right.action) - (sum(right.views) - sum(rest.views))) < 1e-9

    hold = show(cell.tick(1, 0, 0.0))
    assert hold.stamp == "hold"
    assert abs(hold.views[0]) > 0.05

    left = show(cell.tick(1, 1, -0.9))
    assert left.live_gate == 1
    assert left.ternary == -1 and left.stamp == "commit"

    quiet = show(cell.tick(0, 1, 0.0))
    assert quiet.stamp == "hold"

    print()
    print("memory after lean-then-hold w0", round(hold.views[0], 3))
    print("vagus I_G", round(hold.i_g, 3), "g", round(hold.g, 3))
    print("law: process is memory. hold is no drive. others shut.")
    print("hold: 1(0)1")


if __name__ == "__main__":
    demo()
