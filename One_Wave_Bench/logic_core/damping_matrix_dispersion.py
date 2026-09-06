"""G-746 damping-matrix dispersion.

Exact linear algebra for declared models. Not an a0 or vacuum derivation.
"""

from __future__ import annotations

import cmath
import math
from typing import Dict, List, Tuple

import numpy as np


def omega_temporal_scalar(k: float, c_eff: float, omega0: float, gamma: float) -> Tuple[complex, complex]:
    omega_k2 = c_eff * c_eff * k * k + omega0 * omega0
    disc = omega_k2 - 0.25 * gamma * gamma
    root = cmath.sqrt(disc)
    shift = -1j * gamma / 2.0
    return (shift + root, shift - root)


def temporal_regime(k: float, c_eff: float, omega0: float, gamma: float) -> str:
    omega_k2 = c_eff * c_eff * k * k + omega0 * omega0
    crit = 0.25 * gamma * gamma
    if abs(omega_k2 - crit) < 1e-15:
        return "critical"
    return "underdamped" if omega_k2 > crit else "overdamped"


def k_spatial_scalar(omega: float, c_eff: float, omega0: float, gamma: float) -> Tuple[complex, complex]:
    if c_eff == 0:
        raise ValueError("c_eff must be nonzero")
    inside = omega * omega + 1j * gamma * omega - omega0 * omega0
    root = cmath.sqrt(inside) / c_eff
    return (root, -root)


def attenuation_length(omega: float, c_eff: float, omega0: float, gamma: float) -> float:
    kplus, _ = k_spatial_scalar(omega, c_eff, omega0, gamma)
    im = abs(kplus.imag)
    if im == 0:
        return float("inf")
    return 1.0 / im


def group_velocity_real(k: float, c_eff: float, omega0: float, gamma: float, dk: float = 1e-6) -> float:
    w1, _ = omega_temporal_scalar(k + dk, c_eff, omega0, gamma)
    w0, _ = omega_temporal_scalar(k - dk, c_eff, omega0, gamma)
    return ((w1.real - w0.real) / (2.0 * dk))


def a114_z_roots(k: float, dx: float, beta: float, gamma: float) -> Tuple[complex, complex]:
    C = beta * (math.cos(k * dx) - 1.0)
    b = -(2.0 - gamma + C)
    c = 1.0 - gamma
    disc = b * b - 4.0 * c
    root = cmath.sqrt(disc)
    return ((-b + root) / 2.0, (-b - root) / 2.0)


def a114_omega(k: float, dx: float, dt: float, beta: float, gamma: float) -> Tuple[complex, complex]:
    z1, z2 = a114_z_roots(k, dx, beta, gamma)
    def w(z: complex) -> complex:
        if z == 0:
            return complex("nan")
        return 1j * cmath.log(z) / dt
    return (w(z1), w(z2))


def matrix_poly_lambda(k: float, cF: float, cV: float, wF: float, wV: float, gF: float, gV: float, gx: float, kappa: float) -> List[complex]:
    dF = cF * cF * k * k + wF * wF
    dV = cV * cV * k * k + wV * wV
    return [
        1.0 + 0j,
        (gF + gV) + 0j,
        (dF + dV + gF * gV - gx * gx) + 0j,
        (gF * dV + gV * dF - 2.0 * gx * kappa) + 0j,
        (dF * dV - kappa * kappa) + 0j,
    ]


def matrix_lambda_roots(k: float, cF: float, cV: float, wF: float, wV: float, gF: float, gV: float, gx: float, kappa: float) -> np.ndarray:
    coeffs = [z.real if abs(z.imag) < 1e-15 else z for z in matrix_poly_lambda(k, cF, cV, wF, wV, gF, gV, gx, kappa)]
    return np.roots(coeffs)


def matrix_omega_roots(k: float, **kwargs) -> np.ndarray:
    return 1j * matrix_lambda_roots(k, **kwargs)


def decoupled_matches_scalar(k: float, c_eff: float, omega0: float, gamma: float, atol: float = 1e-9) -> bool:
    scalar = set(_snap(omega_temporal_scalar(k, c_eff, omega0, gamma)))
    mat = matrix_omega_roots(
        k, cF=c_eff, cV=c_eff, wF=omega0, wV=omega0, gF=gamma, gV=gamma, gx=0.0, kappa=0.0
    )
    # two copies of the same scalar pair
    snapped = set(_snap(mat))
    return scalar <= snapped


def _snap(vals) -> Tuple[complex, ...]:
    out = []
    for v in vals:
        out.append(complex(round(v.real, 9), round(v.imag, 9)))
    return tuple(out)


def receipt_scalar(k: float, c_eff: float, omega0: float, gamma: float) -> Dict[str, object]:
    wp, wm = omega_temporal_scalar(k, c_eff, omega0, gamma)
    return {
        "brick": "Yellow",
        "model": "scalar_damped_kg",
        "k": k,
        "omega_plus": wp,
        "omega_minus": wm,
        "temporal_regime": temporal_regime(k, c_eff, omega0, gamma),
        "vg_plus": group_velocity_real(k, c_eff, omega0, gamma),
        "derived_a0": False,
        "closes_E5": False,
    }
