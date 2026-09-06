"""G-757 discrete E4 on the D-408 seven-cell."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "logic_core"))
from hex_lattice_graph import NEIGHBOR_OFFSETS, seven_cell


def wrap(d: float) -> float:
    return (d + math.pi) % (2.0 * math.pi) - math.pi


@dataclass
class Coeff:
    aK: float = 1.0
    bK: float = 0.4
    gK: float = 0.2
    aE: float = 1.0
    dE: float = 0.5
    aM: float = 0.35
    aT: float = 0.8
    bT: float = 0.2
    kappa: float = 0.1
    chi: float = 0.0
    Gstar: float = 0.0
    Rstar: float = 1.0
    eps: float = 1e-9


@dataclass
class State:
    a: List[float]  # 7: center then ring in NEIGHBOR_OFFSETS order
    phi: List[float]

    def ring_amp(self) -> List[float]:
        return self.a[1:]


def circulation(phi_ring: Sequence[float]) -> float:
    g = 0.0
    n = len(phi_ring)
    for i in range(n):
        g += wrap(phi_ring[(i + 1) % n] - phi_ring[i])
    return g


def dipole(a_ring: Sequence[float]) -> Tuple[float, float, float]:
    C = S = 0.0
    for k, ak in enumerate(a_ring):
        ang = 2.0 * math.pi * k / 6.0
        C += ak * math.cos(ang)
        S += ak * math.sin(ang)
    return C, S, math.atan2(S, C)


def e4(state: State, c: Coeff = Coeff()) -> dict:
    ac, ar = state.a[0], state.a[1:]
    pc, pr = state.phi[0], state.phi[1:]
    G = circulation(pr)
    C, S, th = dipole(ar)
    R = (sum(ar) / 6.0) / (ac + c.eps)
    eK = c.aK * (G - c.Gstar) ** 2
    eK += c.bK * sum((ar[i] - ar[(i + 1) % 6]) ** 2 for i in range(6))
    eK += c.gK * ac * sum(1.0 - math.cos(pr[i] - pc) for i in range(6))
    eE = c.aE * (R - c.Rstar) ** 2 + c.dE * (ac - 1.0) ** 2
    eM = c.aM * math.sin(th) ** 2
    eT = c.aT * (R - c.Rstar - c.kappa * (G - c.Gstar)) ** 2
    eT += c.bT * sum((ar[i] - ac * c.Rstar) ** 2 for i in range(6))
    eX = c.chi * (ac - 1.0) * S
    tot = eK + eE + eM + eT + eX
    return {"K": eK, "E": eE, "M": eM, "T": eT, "x": eX, "total": tot, "Gamma": G, "theta": th, "R": R}


def symmetric_hold() -> State:
    return State(a=[1.0] + [1.0] * 6, phi=[0.0] * 7)


def dipole_seed(eps: float = 0.05, well: float = 0.0) -> State:
    a = [1.0]
    for k in range(6):
        ang = 2.0 * math.pi * k / 6.0 + well
        a.append(1.0 + eps * math.cos(ang))
    return State(a=a, phi=[0.0] * 7)
