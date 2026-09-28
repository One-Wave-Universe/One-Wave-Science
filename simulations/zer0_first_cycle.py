#!/usr/bin/env python3
"""Zer0 first-cycle demonstrator.

Proves only the grammar in Builds/algorithms/IMPLEMENTATION_STATUS.md:

    reference -> opposed choice with HOLD -> move -> consequence
    -> classify -> resolve -> bounded new reference

Not a universe proof. Not CELL hardware. Software harness for the grammar.
"""

from __future__ import annotations

from dataclasses import dataclass


DEAD = 0.05  # HOLD band around current reference
ALPHA = 0.25  # rebase mix; keeps history, bounds walk
BRANCHES = ("X", "Y", "Z", "T")


@dataclass
class Cycle:
    ref: float
    inp: float
    delta: float
    choice: str  # "-", "0", "+"
    move: float
    consequence: float
    new_ref: float
    hold: bool


def classify(delta: float) -> str:
    if delta > DEAD:
        return "+"
    if delta < -DEAD:
        return "-"
    return "0"


def resolve(choices: dict[str, str]) -> str:
    """Two-of-three on X,Y,Z. T is timing/closure, not a fourth vote."""
    votes = [choices[b] for b in ("X", "Y", "Z")]
    for trit in ("+", "-", "0"):
        if votes.count(trit) >= 2:
            return trit
    return "0"  # genuine disagreement -> HOLD, not a hidden arbiter


def rebase(ref: float, resolved: str, consequence: float) -> float:
    if resolved == "0":
        return max(-1.0, min(1.0, ref))
    signed = 1.0 if resolved == "+" else -1.0
    nxt = (1.0 - ALPHA) * ref + ALPHA * signed * abs(consequence)
    return max(-1.0, min(1.0, nxt))


def one_branch(ref: float, inp: float) -> Cycle:
    delta = inp - ref
    choice = classify(delta)
    hold = choice == "0"
    move = 0.0 if hold else (1.0 if choice == "+" else -1.0)
    consequence = move * (abs(delta) if not hold else 0.0)
    new_ref = rebase(ref, choice, consequence if not hold else 0.0)
    return Cycle(ref, inp, delta, choice, move, consequence, new_ref, hold)


def shared_event(ref: float, inputs: dict[str, float]) -> dict:
    cycles = {b: one_branch(ref, inputs[b]) for b in BRANCHES}
    choices = {b: cycles[b].choice for b in BRANCHES}
    resolved = resolve(choices)
    mean_conseq = sum(abs(cycles[b].consequence) for b in ("X", "Y", "Z")) / 3.0
    new_ref = rebase(ref, resolved, mean_conseq)
    return {
        "ref": ref,
        "choices": choices,
        "resolved": resolved,
        "new_ref": new_ref,
        "hold": resolved == "0",
        "depends_on_prior": new_ref != ref or resolved == "0",
        "trace": {b: cycles[b] for b in BRANCHES},
    }


def runaway_test(n: int = 40) -> bool:
    ref = 0.0
    for _ in range(n):
        ev = shared_event(ref, {b: 1.0 for b in BRANCHES})
        ref = ev["new_ref"]
        if abs(ref) > 1.0 + 1e-9:
            return False
    return abs(ref) <= 1.0


def hold_is_real() -> bool:
    ev = shared_event(0.0, {b: 0.01 for b in BRANCHES})
    return ev["hold"] and ev["resolved"] == "0"


def history_depends() -> bool:
    a = shared_event(0.0, {b: 0.8 for b in BRANCHES})
    b = shared_event(a["new_ref"], {b: 0.8 for b in BRANCHES})
    return a["new_ref"] != 0.0 and (
        b["new_ref"] != a["new_ref"] or abs(b["new_ref"]) >= abs(a["new_ref"])
    )


def disagreement_hold() -> bool:
    ev = shared_event(
        0.0,
        {"X": 0.8, "Y": -0.8, "Z": 0.0, "T": 0.2},
    )
    return ev["resolved"] == "0"


def main() -> int:
    ev = shared_event(0.0, {"X": 0.4, "Y": 0.5, "Z": 0.35, "T": 0.1})
    print("first event", {k: ev[k] for k in ("ref", "choices", "resolved", "new_ref", "hold")})
    checks = {
        "bounded_rebase": runaway_test(),
        "hold_is_real": hold_is_real(),
        "history_depends": history_depends(),
        "disagreement_is_hold": disagreement_hold(),
    }
    print("checks", checks)
    ok = all(checks.values())
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
