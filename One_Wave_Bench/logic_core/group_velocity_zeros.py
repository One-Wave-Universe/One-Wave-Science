"""G-747 two group-velocity zeros."""

from __future__ import annotations

import math
from typing import Dict


def vg_vp_continuum(k: float, c_eff: float, omega0: float, gamma: float):
    disc = c_eff * c_eff * k * k + omega0 * omega0 - 0.25 * gamma * gamma
    if k == 0 or disc <= 0:
        return 0.0, 0.0
    root = math.sqrt(disc)
    vg = (c_eff * c_eff * k) / root
    vp = root / k
    return vg, vp


def a114_omega_undamped(k: float, dx: float = 1.0, dt: float = 1.0, beta: float = 0.5) -> float:
    arg = 1.0 + 0.5 * beta * (math.cos(k * dx) - 1.0)
    arg = max(-1.0, min(1.0, arg))
    return math.acos(arg) / dt


def a114_vg_undamped(k: float, dx: float = 1.0, dt: float = 1.0, beta: float = 0.5, dk: float = 1e-6) -> float:
    return (a114_omega_undamped(k + dk, dx, dt, beta) - a114_omega_undamped(k - dk, dx, dt, beta)) / (2.0 * dk)


def receipt() -> Dict[str, object]:
    vg, vp = vg_vp_continuum(1.0, 1.0, 1.0, 0.0)
    edge = math.pi
    return {
        "continuum_vg_vp_product": vg * vp,
        "continuum_has_zone_edge": False,
        "a114_vg_at_pi": a114_vg_undamped(edge),
        "a114_small_k_vg": a114_vg_undamped(1e-3),
        "a114_small_k_target": math.sqrt(0.25),
        "derived_a0": False,
        "closes_E5": False,
    }
