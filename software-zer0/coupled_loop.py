#!/usr/bin/env python3
"""SOFTWARE ONLY — two coupled state machines + reinjection loop.

Machine 1  BC–DC   binary brain     N / Y   commit after body leaves HOLD
Machine 2  TC–AC   ternary body     - / 0 / +   lives on walking virtual ground

One FLIP: new view up, old action down, same tick.
Reinjection: consequence of the pair becomes next input bias (V_BUS-like number).
Not iron. Not memory. Helper grammar for the analog build.
"""

from __future__ import annotations

from dataclasses import dataclass, field


DEAD = 0.05
ALPHA = 0.25


def clip(x: float) -> float:
    return max(-1.0, min(1.0, x))


def trit(delta: float) -> str:
    if delta > DEAD:
        return "+"
    if delta < -DEAD:
        return "-"
    return "0"


@dataclass
class BodyAC:
    """Ternary body. Virtual ground is `ground`."""

    ground: float = 0.0
    lean: str = "0"

    def sense(self, u: float) -> dict:
        delta = u - self.ground
        c = trit(delta)
        return {"u": u, "delta": delta, "trit": c, "hold": c == "0"}


@dataclass
class BrainDC:
    """Binary brain. May not commit while body is HOLD."""

    last: str = "N"

    def commit(self, body_trit: str) -> str:
        if body_trit == "0":
            return "N"
        return "Y"


@dataclass
class CoupledLoop:
    body: BodyAC = field(default_factory=BodyAC)
    brain: BrainDC = field(default_factory=BrainDC)
    bus: float = 0.0
    step: int = 0
    log: list = field(default_factory=list)

    def flip(self, u: float) -> dict:
        view = self.body.sense(u + self.bus)
        body_trit = view["trit"]
        commit = self.brain.commit(body_trit)
        old_ground = self.body.ground
        if commit == "N":
            new_ground = old_ground
            action = 0.0
        else:
            sign = 1.0 if body_trit == "+" else -1.0
            action = sign * abs(view["delta"])
            new_ground = clip((1.0 - ALPHA) * old_ground + ALPHA * action)
        self.bus = clip(0.7 * self.bus + 0.3 * action)
        self.body.ground = new_ground
        self.body.lean = body_trit
        self.brain.last = commit
        rec = {
            "kind": "software-coupled-loop",
            "step": self.step,
            "u": u,
            "view": view,
            "body_AC": body_trit,
            "brain_DC": commit,
            "action": action,
            "ground_in": old_ground,
            "ground_out": new_ground,
            "bus": self.bus,
        }
        self.step += 1
        self.log.append(rec)
        return rec

    def run(self, inputs: list) -> list:
        return [self.flip(u) for u in inputs]


def main() -> int:
    loop = CoupledLoop()
    seq = [0.4, 0.4, 0.01, -0.6, -0.6, 0.0, 0.8]
    rows = loop.run(seq)
    print("t  u     AC  DC  ground        bus")
    for r in rows:
        print(
            f"{r['step']}  {r['u']:+.2f}  {r['body_AC']:>2}  {r['brain_DC']}   "
            f"{r['ground_in']:+.3f}->{r['ground_out']:+.3f}  {r['bus']:+.3f}"
        )
    holds = [r for r in rows if r["body_AC"] == "0"]
    commits = [r for r in rows if r["brain_DC"] == "Y"]
    print("SOFTWARE_ONLY coupled-loop")
    print("HOLD ticks", len(holds), "COMMIT ticks", len(commits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
