"""Toy four-interaction hold. Not a 125 GeV derivation."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Tuple

# q = (r_knot, r_shell, theta_mirror, weave)
# theta = 0 and pi are candidate basins.


@dataclass(frozen=True)
class Q:
    rk: float
    rs: float
    th: float
    w: float

    def as_tuple(self) -> Tuple[float, float, float, float]:
        return (self.rk, self.rs, self.th, self.w)


def e4(q: Q) -> dict:
    ek = (q.rk - 1.0) ** 2 + 0.05 * q.w ** 2
    ee = (q.rs - 1.6) ** 2
    em = 0.35 * math.sin(q.th) ** 2
    et = 0.8 * (q.rs - q.rk - 0.6) ** 2 + 0.2 * (q.w - 0.2 * math.cos(q.th)) ** 2
    ex = 0.15 * (q.rk - 1.0) * math.sin(q.th)
    total = ek + ee + em + et + ex
    return {"K": ek, "E": ee, "M": em, "T": et, "x": ex, "total": total}


def descend(q: Q, steps: int = 400, lr: float = 0.08, h: float = 1e-4) -> Q:
    rk, rs, th, w = q.as_tuple()
    for _ in range(steps):
        def tot(rk_, rs_, th_, w_):
            return e4(Q(rk_, rs_, th_, w_))["total"]
        g_rk = (tot(rk + h, rs, th, w) - tot(rk - h, rs, th, w)) / (2 * h)
        g_rs = (tot(rk, rs + h, th, w) - tot(rk, rs - h, th, w)) / (2 * h)
        g_th = (tot(rk, rs, th + h, w) - tot(rk, rs, th - h, w)) / (2 * h)
        g_w = (tot(rk, rs, th, w + h) - tot(rk, rs, th, w - h)) / (2 * h)
        rk -= lr * g_rk
        rs -= lr * g_rs
        th -= lr * g_th
        w -= lr * g_w
    return Q(rk, rs, th, w)


def two_basins() -> dict:
    a = descend(Q(1.1, 1.7, 0.2, 0.1))
    b = descend(Q(1.1, 1.7, math.pi - 0.2, 0.1))
    ea, eb = e4(a)["total"], e4(b)["total"]
    return {
        "basin_0": {"q": a.as_tuple(), "E": ea},
        "basin_pi": {"q": b.as_tuple(), "E": eb},
        "delta_E": abs(ea - eb),
        "same_energy_family": abs(ea - eb) < 0.05,
        "derived_a0": False,
        "is_C322": False,
    }
