#!/usr/bin/env python3
"""SOFTWARE bench helper for the analog CELL build.

Reads voltages you type or pipe. Scores differentials, HOLD, history test.
Does not store magnetic state. Does not replace the core.

Usage:
  python3 bench_assist.py demo
  python3 bench_assist.py score --vp 2.1 --vm 1.7 --center 1.9
  python3 bench_assist.py history --probe-a 0.82 --probe-b 0.61 --noise 0.05
  python3 bench_assist.py triad --da 0.3 --db 0.25 --dc -0.05
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


HOLD_LO, HOLD_HI = 0.45, 0.55
KIND = "software-bench-assist"


def clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def normalize_d(vp: float, vm: float, center: float, span: float):
    d = vp - vm
    mid = (vp + vm) / 2.0
    mid_err = mid - center
    n = 0.5 + (d / (2.0 * span))
    return clip01(n), d, mid_err


def band(n: float):
    x = n * 100.0
    table = (
        (90, 100.0001, 3, "EXTREME+"),
        (85, 90, None, "GAP"),
        (75, 85, 2, "STRONG+"),
        (70, 75, None, "GAP"),
        (60, 70, 1, "MOD+"),
        (55, 60, None, "GAP"),
        (45, 55, 0, "HOLD"),
        (40, 45, None, "GAP"),
        (30, 40, -1, "MOD-"),
        (25, 30, None, "GAP"),
        (15, 25, -2, "STRONG-"),
        (10, 15, None, "GAP"),
        (0, 10, -3, "EXTREME-"),
    )
    for lo, hi, lvl, name in table:
        if lo <= x < hi:
            return lvl if lvl is not None else 99, name
    return 99, "GAP"


def trit_from_n(n: float) -> str:
    if n > HOLD_HI:
        return "+"
    if n < HOLD_LO:
        return "-"
    return "0"


@dataclass
class AxisScore:
    vp: float
    vm: float
    center: float
    d: float
    mid_err: float
    n: float
    trit: str
    level: int
    band: str
    hold: bool
    rails_ok: bool
    notes: list


def score_axis(vp, vm, center, vbus=None, span=1.0) -> AxisScore:
    n, d, mid_err = normalize_d(vp, vm, center, span)
    lvl, name = band(n)
    notes = []
    rails_ok = True
    if vbus is not None and abs(center - vbus) < 1e-6:
        rails_ok = False
        notes.append("FAIL CENTER tied to V_BUS")
    if abs(mid_err) > 0.25 * max(span, 1e-9):
        notes.append("WARN pair mid drifted off CENTER")
    hold = trit_from_n(n) == "0"
    if hold:
        notes.append("HOLD is live mid, not off")
    return AxisScore(vp, vm, center, d, mid_err, n, trit_from_n(n), lvl, name, hold, rails_ok, notes)


def history(probe_a, probe_b, noise):
    delta = abs(probe_a - probe_b)
    ok = delta > noise
    return {
        "kind": KIND,
        "test": "retained-state",
        "probe_after_plus_write": probe_a,
        "probe_after_minus_write": probe_b,
        "abs_delta": delta,
        "noise_floor": noise,
        "pass": ok,
        "meaning": (
            "same probe distinguished two histories — iron may be remembering"
            if ok
            else "FAIL same probe after opposite writes — stop, revise nucleus"
        ),
    }


def triad(da, db, dc, span=1.0):
    def n_from_d(d):
        return clip01(0.5 + d / (2.0 * span))

    ns = {"A": n_from_d(da), "B": n_from_d(db), "C": n_from_d(dc)}
    votes = {k: trit_from_n(v) for k, v in ns.items()}
    bag = list(votes.values())
    resolved = "0"
    for t in ("+", "-", "0"):
        if bag.count(t) >= 2:
            resolved = t
            break
    return {
        "kind": KIND,
        "test": "two-of-three-software-score",
        "D": {"A": da, "B": db, "C": dc},
        "votes": votes,
        "resolved": resolved,
        "hold": resolved == "0",
        "note": "this is a score of measured D, not a digital majority chip in the cell",
    }


def demo():
    a = score_axis(2.10, 1.70, 1.90, vbus=3.3, span=1.0)
    return {"kind": KIND, "axis": asdict(a), "history": history(0.82, 0.61, 0.05), "triad": triad(0.40, 0.30, -0.05)}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="SOFTWARE helper for analog CELL bench")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    s = sub.add_parser("score")
    s.add_argument("--vp", type=float, required=True)
    s.add_argument("--vm", type=float, required=True)
    s.add_argument("--center", type=float, required=True)
    s.add_argument("--vbus", type=float, default=None)
    s.add_argument("--span", type=float, default=1.0)
    h = sub.add_parser("history")
    h.add_argument("--probe-a", type=float, required=True)
    h.add_argument("--probe-b", type=float, required=True)
    h.add_argument("--noise", type=float, default=0.05)
    t = sub.add_parser("triad")
    t.add_argument("--da", type=float, required=True)
    t.add_argument("--db", type=float, required=True)
    t.add_argument("--dc", type=float, required=True)
    t.add_argument("--span", type=float, default=1.0)
    args = p.parse_args(argv)
    if args.cmd == "demo":
        out = demo()
    elif args.cmd == "score":
        out = asdict(score_axis(args.vp, args.vm, args.center, args.vbus, args.span))
        out["kind"] = KIND
    elif args.cmd == "history":
        out = history(args.probe_a, args.probe_b, args.noise)
    else:
        out = triad(args.da, args.db, args.dc, args.span)
    print(json.dumps(out, indent=2))
    if args.cmd == "history":
        return 0 if out["pass"] else 2
    if args.cmd == "score" and not out.get("rails_ok", True):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
