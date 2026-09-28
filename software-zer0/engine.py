#!/usr/bin/env python3
"""SOFTWARE ONLY — Algorythm-Zer0 grammar engine.

Not CELL_V1 memory. Not magnetics. Not the android.
Physical memory stays in Builds/cell-v1.
This file may describe, route, compare, rebase. It must not claim it remembers for the body.
"""

from __future__ import annotations

from dataclasses import dataclass, field


DEAD = 0.05
ALPHA = 0.25
BRANCHES = ("X", "Y", "Z", "T")
XYZ = ("X", "Y", "Z")


def clip(x: float) -> float:
    return max(-1.0, min(1.0, x))


def trit(delta: float, dead: float = DEAD) -> str:
    if delta > dead:
        return "+"
    if delta < -dead:
        return "-"
    return "0"


def two_of_three(votes: dict[str, str]) -> str:
    bag = [votes[b] for b in XYZ]
    for t in ("+", "-", "0"):
        if bag.count(t) >= 2:
            return t
    return "0"


@dataclass
class SoftState:
    """Walking software reference. Explicitly not hysteresis in iron."""

    ref: float = 0.0
    step: int = 0
    last_resolved: str = "0"
    log: list = field(default_factory=list)

    def perceive(self, inputs: dict[str, float]) -> dict:
        views = {}
        for b in BRANCHES:
            u = float(inputs[b])
            delta = u - self.ref
            c = trit(delta)
            move = 0.0 if c == "0" else (1.0 if c == "+" else -1.0)
            views[b] = {
                "u": u,
                "delta": delta,
                "choice": c,
                "move": move,
                "kappa": move * abs(delta),
            }
        return views

    def flip(self, inputs: dict[str, float]) -> dict:
        """One simultaneous software flip: views up, actions down, new zero."""
        views = self.perceive(inputs)
        choices = {b: views[b]["choice"] for b in BRANCHES}
        resolved = two_of_three(choices)
        mean_k = sum(abs(views[b]["kappa"]) for b in XYZ) / 3.0
        old = self.ref
        if resolved == "0":
            new = old
        else:
            sign = 1.0 if resolved == "+" else -1.0
            new = clip((1.0 - ALPHA) * old + ALPHA * sign * mean_k)
        rec = {
            "step": self.step,
            "ref_in": old,
            "inputs": dict(inputs),
            "choices": choices,
            "resolved": resolved,
            "hold": resolved == "0",
            "ref_out": new,
            "views": views,
            "kind": "software",
        }
        self.ref = new
        self.last_resolved = resolved
        self.step += 1
        self.log.append(rec)
        return rec


def demo() -> list:
    s = SoftState()
    seq = [
        {"X": 0.4, "Y": 0.5, "Z": 0.35, "T": 0.1},
        {"X": 0.4, "Y": 0.5, "Z": 0.35, "T": 0.1},
        {"X": 0.01, "Y": 0.0, "Z": -0.01, "T": 0.0},
        {"X": -0.7, "Y": -0.6, "Z": -0.65, "T": 0.2},
        {"X": 0.9, "Y": -0.9, "Z": 0.0, "T": 0.0},
    ]
    return [s.flip(u) for u in seq]


def main() -> int:
    rows = demo()
    for r in rows:
        print(
            f"t={r['step']} r {r['ref_in']:+.3f}->{r['ref_out']:+.3f} "
            f"xyz={r['choices']['X']}{r['choices']['Y']}{r['choices']['Z']} "
            f"res={r['resolved']} hold={r['hold']}"
        )
    print("SOFTWARE_ONLY PASS", rows[-1]["kind"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
