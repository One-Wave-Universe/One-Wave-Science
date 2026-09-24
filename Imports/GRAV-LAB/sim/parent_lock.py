#!/usr/bin/env python3
"""Point rotation + parent proximity lock.

No weak-field. No GEM. A child site has a facing angle.
A parent writes a torque from proximity and alignment mismatch.
Lock = facing stops walking relative to the parent line.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Child:
    facing: float = 0.0       # radians, 0 = looking at parent
    spin: float = 0.35        # d(facing)/dt in the inertial sense, rad/tick
    gamma: float = 0.08       # inertial memory damping
    beta: float = 0.12        # restore toward neighbors / parent line
    align: float = 1.0        # how much of an alignment channel it has (0=insulator)


@dataclass
class Parent:
    proximity: float = 1.0    # 1 = sitting in the near field, decays as used below
    phase: float = 0.0        # parent lattice phase at the child's orbit


def torque(child: Child, parent: Parent) -> float:
    # mismatch between child's face and parent line/phase
    mismatch = math.sin(child.facing - parent.phase)
    # near field weights alignment harder; far field still has geometric restore
    near = parent.proximity
    geo = child.beta * math.sin(-child.facing)  # geometry wants face-on
    aln = child.align * near * 0.7 * mismatch
    return -geo - aln


def step(child: Child, parent: Parent) -> None:
    tau = torque(child, parent)
    # point rotation update: spin remembers, torque writes, dead-ish belt near lock
    child.spin = (1.0 - child.gamma) * child.spin + tau
    if abs(child.facing) < 0.03 and abs(child.spin) < 0.02:
        child.spin *= 0.3  # hold belt — legal rest, not a clamp
    child.facing += child.spin
    # wrap
    child.facing = (child.facing + math.pi) % (2 * math.pi) - math.pi


def run(steps: int = 80, proximity: float = 1.0, align: float = 1.0, spin0: float = 0.35) -> dict:
    child = Child(facing=1.2, spin=spin0, align=align)
    parent = Parent(proximity=proximity)
    hist = []
    locked_at = None
    for t in range(steps):
        step(child, parent)
        hist.append((t, child.facing, child.spin))
        if locked_at is None and abs(child.facing) < 0.05 and abs(child.spin) < 0.02:
            locked_at = t
    return {
        "proximity": proximity,
        "align": align,
        "spin0": spin0,
        "final_face": child.facing,
        "final_spin": child.spin,
        "locked_at": locked_at,
        "hist": hist,
    }


def demo() -> None:
    print("GRAV-LAB parent lock — no weak field")
    print(f"{'prox':>6} {'align':>6} {'spin0':>6} {'lock@':>6} {'face':>8} {'spin':>8}")
    cases = [
        (1.0, 1.0, 0.35),
        (1.0, 0.0, 0.35),   # insulator — geometry only
        (0.15, 1.0, 0.35),  # far parent field
        (1.0, 1.0, 1.10),   # wild initial spin
        (0.05, 0.0, 0.80),  # far + insulator + hot spin
    ]
    for prox, aln, s0 in cases:
        r = run(proximity=prox, align=aln, spin0=s0)
        lock = "-" if r["locked_at"] is None else str(r["locked_at"])
        print(
            f"{prox:6.2f} {aln:6.2f} {s0:6.2f} {lock:>6} "
            f"{r['final_face']:8.3f} {r['final_spin']:8.3f}"
        )
    print()
    print("lock@ = first tick face and spin both sit in the hold belt")
    print("align=0 is a child with no magnetic / alignment channel")
    print("If align=0 still locks, the face lock was geometry+rotation, not parent B")


if __name__ == "__main__":
    demo()
