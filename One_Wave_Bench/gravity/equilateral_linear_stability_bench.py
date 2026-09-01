#!/usr/bin/env python3
"""Linear-stability benchmark for the regularized equilateral three-body orbit.

Candidate pair acceleration:
    a_i = K sum_{j!=i} m_j F(r_ij/lambda) (r_j-r_i)/r_ij^3
where F(x)=1-(1+x)e^{-x}.

For the exact equilateral relative equilibrium, define
    beta = (m1*m2 + m2*m3 + m3*m1) / M^2
    eta(x) = d ln[h(r)] / d ln[r] at r=s
with h(r)=K F(r/lambda)/r^3 and x=s/lambda.

Then
    eta(x) = x^2/(e^x-1-x) - 3.

After normalizing the orbital frequency to omega=1, the planar rotating-frame
characteristic determinant factors as

    sigma^2 (sigma^2+1)^2 (sigma^2+eta+4)
    * [sigma^4 + (eta+4)sigma^2 + (3/4)eta^2 beta].

For this kernel -3 < eta < -1, so the only nontrivial spectral-stability
condition is

    beta <= beta_crit(x) = (eta+4)^2/(3 eta^2).

The Newtonian limit x->infinity gives eta->-3 and beta_crit->1/27,
recovering the classical Gascheau/Routh threshold.
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
from typing import Sequence


def kernel_factor(x: float) -> float:
    if x <= 0.0:
        raise ValueError("x must be positive")
    return 1.0 - (1.0 + x) * math.exp(-x)


def log_pair_coefficient_slope(x: float) -> float:
    """eta = d ln(F/r^3)/d ln r with x=r/lambda."""
    if x <= 0.0:
        raise ValueError("x must be positive")
    if x > 50.0:
        return -3.0
    den = math.expm1(x) - x
    return (x * x) / den - 3.0


def mass_beta(masses: Sequence[float]) -> float:
    if len(masses) != 3 or any(m <= 0.0 for m in masses):
        raise ValueError("exactly three positive masses are required")
    m1, m2, m3 = (float(m) for m in masses)
    total = m1 + m2 + m3
    return (m1 * m2 + m2 * m3 + m3 * m1) / (total * total)


def beta_critical(x: float) -> float:
    eta = log_pair_coefficient_slope(x)
    return ((eta + 4.0) ** 2) / (3.0 * eta * eta)


def stability_discriminant(masses: Sequence[float], x: float) -> float:
    eta = log_pair_coefficient_slope(x)
    beta = mass_beta(masses)
    return (eta + 4.0) ** 2 - 3.0 * eta * eta * beta


def stability_class(masses: Sequence[float], x: float, tol: float = 1e-12) -> str:
    """Classify nontrivial planar modes after removing symmetry factors."""
    eta = log_pair_coefficient_slope(x)
    if eta + 4.0 <= 0.0:
        return "UNSTABLE_BREATHING_MODE"
    disc = stability_discriminant(masses, x)
    if disc > tol:
        return "STABLE_INTERIOR"
    if disc < -tol:
        return "UNSTABLE_SHAPE_MODE"
    return "MARGINAL_BOUNDARY"


def spectrally_stable(masses: Sequence[float], x: float, tol: float = 1e-12) -> bool:
    """True only for the strict interior, not the repeated-root boundary."""
    return stability_class(masses, x, tol) == "STABLE_INTERIOR"


def critical_eta(beta: float) -> float:
    if beta <= 0.0 or beta > 1.0 / 3.0 + 1e-15:
        raise ValueError("physical positive-mass beta must lie in (0,1/3]")
    return -4.0 / (1.0 + math.sqrt(3.0 * beta))


def critical_x_for_beta(beta: float) -> float:
    """Return finite x threshold; +inf if stable through Newtonian limit."""
    if beta <= 0.0 or beta > 1.0 / 3.0 + 1e-15:
        raise ValueError("physical positive-mass beta must lie in (0,1/3]")
    if beta <= 1.0 / 27.0:
        return math.inf
    target = critical_eta(beta)
    lo, hi = 1e-8, 64.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if log_pair_coefficient_slope(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def shape_mode_sigma_squared(masses: Sequence[float], x: float) -> tuple[complex, complex]:
    """Roots u=sigma^2 of the nontrivial shape quartic."""
    eta = log_pair_coefficient_slope(x)
    beta = mass_beta(masses)
    disc = complex((eta + 4.0) ** 2 - 3.0 * eta * eta * beta, 0.0)
    root_disc = cmath.sqrt(disc)
    return (
        (-(eta + 4.0) + root_disc) / 2.0,
        (-(eta + 4.0) - root_disc) / 2.0,
    )


def _zeros(n: int) -> list[list[complex]]:
    return [[0j for _ in range(n)] for _ in range(n)]


def _determinant(matrix: Sequence[Sequence[complex]]) -> complex:
    a = [list(map(complex, row)) for row in matrix]
    n = len(a)
    det = 1.0 + 0.0j
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-15:
            return 0.0 + 0.0j
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        pv = a[col][col]
        det *= pv
        for r in range(col + 1, n):
            factor = a[r][col] / pv
            if factor == 0:
                continue
            for c in range(col + 1, n):
                a[r][c] -= factor * a[col][c]
    return det


def raw_characteristic_determinant(masses: Sequence[float], eta: float, sigma: complex) -> complex:
    """Direct 6x6 rotating-frame determinant, normalized to M=omega=s=1."""
    if len(masses) != 3 or any(m <= 0.0 for m in masses):
        raise ValueError("exactly three positive masses are required")
    total = float(sum(masses))
    ms = [float(m) / total for m in masses]
    rt3 = math.sqrt(3.0)
    points = ((0.0, 0.0), (1.0, 0.0), (0.5, 0.5 * rt3))
    A = _zeros(6)

    for i in range(3):
        for j in range(i + 1, 3):
            nx = points[j][0] - points[i][0]
            ny = points[j][1] - points[i][1]
            D = (
                (1.0 + eta * nx * nx, eta * nx * ny),
                (eta * ny * nx, 1.0 + eta * ny * ny),
            )
            mi, mj = ms[i], ms[j]
            for a in range(2):
                for b in range(2):
                    d = D[a][b]
                    A[2 * i + a][2 * i + b] -= mj * d
                    A[2 * i + a][2 * j + b] += mj * d
                    A[2 * j + a][2 * j + b] -= mi * d
                    A[2 * j + a][2 * i + b] += mi * d

    Q = _zeros(6)
    for r in range(6):
        for c in range(6):
            Q[r][c] = -A[r][c]
            if r == c:
                Q[r][c] += sigma * sigma - 1.0
    for k in range(3):
        Q[2 * k][2 * k + 1] += -2.0 * sigma
        Q[2 * k + 1][2 * k] += 2.0 * sigma
    return _determinant(Q)


def factored_characteristic_determinant(masses: Sequence[float], eta: float, sigma: complex) -> complex:
    beta = mass_beta(masses)
    s2 = sigma * sigma
    return (
        s2
        * (s2 + 1.0) ** 2
        * (s2 + eta + 4.0)
        * (s2 * s2 + (eta + 4.0) * s2 + 0.75 * eta * eta * beta)
    )


def determinant_factorization_relative_error(masses: Sequence[float], x: float) -> float:
    eta = log_pair_coefficient_slope(x)
    probes = (0.37 + 0.21j, -0.82 + 0.17j, 1.13 - 0.31j)
    worst = 0.0
    for sigma in probes:
        raw = raw_characteristic_determinant(masses, eta, sigma)
        fac = factored_characteristic_determinant(masses, eta, sigma)
        worst = max(worst, abs(raw - fac) / max(1.0, abs(raw), abs(fac)))
    return worst


def report(masses: Sequence[float], x: float) -> dict:
    beta = mass_beta(masses)
    eta = log_pair_coefficient_slope(x)
    bc = beta_critical(x)
    xcrit = critical_x_for_beta(beta)
    return {
        "claim_status": "EXACT_LINEAR_SPECTRAL_STABILITY_THEOREM_FOR_DECLARED_PAIR_LAW",
        "masses": [float(m) for m in masses],
        "beta": beta,
        "side_over_lambda": x,
        "eta": eta,
        "eta_range_for_kernel": "-3 < eta < -1",
        "beta_critical": bc,
        "stability_discriminant": stability_discriminant(masses, x),
        "stability_class": stability_class(masses, x),
        "strictly_spectrally_stable_modulo_symmetry_modes": spectrally_stable(masses, x),
        "critical_side_over_lambda": None if math.isinf(xcrit) else xcrit,
        "stable_for_all_finite_side_over_lambda": math.isinf(xcrit),
        "newtonian_limit_beta_critical": 1.0 / 27.0,
        "all_positive_mass_triplets_stable_below_x": critical_x_for_beta(1.0 / 3.0),
        "determinant_factorization_relative_error": determinant_factorization_relative_error(masses, x),
        "characteristic_factorization": "sigma^2 (sigma^2+1)^2 (sigma^2+eta+4) [sigma^4+(eta+4)sigma^2+(3/4)eta^2 beta]",
        "criterion": "beta < (eta+4)^2/(3 eta^2) for strict interior; equality is marginal",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Equilateral three-body linear-stability theorem bench")
    parser.add_argument("--masses", nargs=3, type=float, default=(1.0, 1.7, 2.4))
    parser.add_argument("--x", type=float, default=5.0, help="side/lambda")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = report(args.masses, args.x)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print("Equilateral linear-stability theorem bench")
    print("=" * 45)
    print(f"masses: {payload['masses']}")
    print(f"beta: {payload['beta']:.12g}")
    print(f"side/lambda: {payload['side_over_lambda']:.12g}")
    print(f"eta: {payload['eta']:.12g}")
    print(f"beta_critical: {payload['beta_critical']:.12g}")
    print(f"stability class: {payload['stability_class']}")
    print(f"critical side/lambda: {payload['critical_side_over_lambda']}")
    print(f"factorization relative error: {payload['determinant_factorization_relative_error']:.3e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
