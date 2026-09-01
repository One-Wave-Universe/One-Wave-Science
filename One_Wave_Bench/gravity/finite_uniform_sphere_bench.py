#!/usr/bin/env python3
"""Finite uniform-sphere bench for the Proof-09 gradient-curvature kernel.

Operator:
    b nabla^4 psi - a nabla^2 psi = rho, lambda=sqrt(b/a)

Green kernel:
    G(r)=(1/(4*pi*a))*(1/r-exp(-r/lambda)/r)

This is a mathematical consistency bench for the declared static model, not
experimental evidence for a physical gravity law.
"""

from __future__ import annotations

import argparse
import json
import math

PI = math.pi


def sinhc(x: float) -> float:
    if abs(x) < 1e-5:
        x2 = x * x
        return 1.0 + x2 / 6.0 + x2 * x2 / 120.0
    return math.sinh(x) / x


def dsinhc_dx(x: float) -> float:
    if abs(x) < 1e-5:
        return x / 3.0 + x**3 / 30.0 + x**5 / 840.0
    return (x * math.cosh(x) - math.sinh(x)) / (x * x)


def yukawa_form_factor(z: float) -> float:
    if z <= 0.0:
        raise ValueError("R/lambda must be positive")
    if z < 1e-4:
        z2 = z * z
        return 1.0 + z2 / 10.0 + z2 * z2 / 280.0
    return 3.0 * (z * math.cosh(z) - math.sinh(z)) / (z**3)


def rho_uniform(q: float, radius: float) -> float:
    return 3.0 * q / (4.0 * PI * radius**3)


def coulomb(r: float, q: float, radius: float) -> float:
    rho0 = rho_uniform(q, radius)
    if r <= radius:
        return 2.0 * PI * rho0 * (radius * radius - r * r / 3.0)
    return q / r


def dcoulomb_dr(r: float, q: float, radius: float) -> float:
    rho0 = rho_uniform(q, radius)
    if r <= radius:
        return -4.0 * PI * rho0 * r / 3.0
    return -q / (r * r)


def yukawa(r: float, q: float, radius: float, lam: float) -> float:
    mu = 1.0 / lam
    z = radius * mu
    rho0 = rho_uniform(q, radius)
    if r <= radius:
        y = mu * r
        c = (z + 1.0) * math.exp(-z)
        return 4.0 * PI * rho0 / (mu * mu) * (1.0 - c * sinhc(y))
    return q * yukawa_form_factor(z) * math.exp(-mu * r) / r


def dyukawa_dr(r: float, q: float, radius: float, lam: float) -> float:
    mu = 1.0 / lam
    z = radius * mu
    rho0 = rho_uniform(q, radius)
    if r <= radius:
        if r == 0.0:
            return 0.0
        y = mu * r
        c = (z + 1.0) * math.exp(-z)
        return -4.0 * PI * rho0 / mu * c * dsinhc_dx(y)
    A = yukawa_form_factor(z)
    return -q * A * math.exp(-mu * r) * (mu / r + 1.0 / (r * r))


def psi(r: float, q=1.0, radius=1.0, a=1.0, lam=1.0) -> float:
    return (coulomb(r, q, radius) - yukawa(r, q, radius, lam)) / (4.0 * PI * a)


def dpsi_dr(r: float, q=1.0, radius=1.0, a=1.0, lam=1.0) -> float:
    return (dcoulomb_dr(r, q, radius) - dyukawa_dr(r, q, radius, lam)) / (4.0 * PI * a)


def point_dpsi_dr(r: float, q=1.0, a=1.0, lam=1.0) -> float:
    x = r / lam
    f = 1.0 - (1.0 + x) * math.exp(-x)
    return -q * f / (4.0 * PI * a * r * r)


def exterior_dpsi_dr(r: float, q=1.0, radius=1.0, a=1.0, lam=1.0) -> float:
    z = radius / lam
    x = r / lam
    A = yukawa_form_factor(z)
    return -q / (4.0 * PI * a * r * r) * (1.0 - A * (1.0 + x) * math.exp(-x))


def relerr(x: float, y: float) -> float:
    return abs(x - y) / max(abs(x), abs(y), 1e-30)


def run(q=1.0, radius=1.5, a=1.0, lam=1.0):
    if min(radius, a, lam) <= 0.0:
        raise ValueError("radius, a, and lambda must be positive")

    eps = 1e-8 * max(radius, lam)
    pin = psi(radius - eps, q, radius, a, lam)
    pout = psi(radius + eps, q, radius, a, lam)
    din = dpsi_dr(radius - eps, q, radius, a, lam)
    dout = dpsi_dr(radius + eps, q, radius, a, lam)

    z = radius / lam
    rho0 = rho_uniform(q, radius)
    center_exact = -rho0 * (1.0 - (z + 1.0) * math.exp(-z)) / (3.0 * a)
    rsmall = 1e-6 * min(radius, lam)
    center_numeric = dpsi_dr(rsmall, q, radius, a, lam) / rsmall

    rtest = 5.0 * lam
    tiny_radius = 1e-3 * lam
    tiny = exterior_dpsi_dr(rtest, q, tiny_radius, a, lam)
    point = point_dpsi_dr(rtest, q, a, lam)

    rfar = max(20.0 * lam, 10.0 * radius)
    far = exterior_dpsi_dr(rfar, q, radius, a, lam)
    invsq = -q / (4.0 * PI * a * rfar * rfar)

    rex = 2.3 * radius
    ext_generic = dpsi_dr(rex, q, radius, a, lam)
    ext_closed = exterior_dpsi_dr(rex, q, radius, a, lam)

    result = {
        "status": "analytic_finite_source_model_theorem_bench",
        "q": q,
        "radius": radius,
        "a": a,
        "lambda": lam,
        "R_over_lambda": z,
        "yukawa_form_factor_A": yukawa_form_factor(z),
        "center_potential": psi(0.0, q, radius, a, lam),
        "center_slope": dpsi_dr(0.0, q, radius, a, lam),
        "center_linear_coefficient_exact": center_exact,
        "center_linear_coefficient_numeric": center_numeric,
        "center_linear_coefficient_relative_error": relerr(center_exact, center_numeric),
        "boundary_potential_relative_mismatch": relerr(pin, pout),
        "boundary_slope_relative_mismatch": relerr(din, dout),
        "exterior_formula_relative_mismatch": relerr(ext_generic, ext_closed),
        "tiny_source_to_point_source_relative_mismatch": relerr(tiny, point),
        "far_field_to_inverse_square_relative_mismatch": relerr(far, invsq),
    }
    result["pass"] = {
        "finite_center_potential": math.isfinite(result["center_potential"]),
        "zero_center_slope": abs(result["center_slope"]) < 1e-15,
        "center_linear_term": result["center_linear_coefficient_relative_error"] < 1e-9,
        "C1_boundary": result["boundary_potential_relative_mismatch"] < 1e-6
        and result["boundary_slope_relative_mismatch"] < 1e-6,
        "point_source_limit": result["tiny_source_to_point_source_relative_mismatch"] < 1e-6,
        "inverse_square_far_field": result["far_field_to_inverse_square_relative_mismatch"] < 1e-6,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=float, default=1.0)
    parser.add_argument("--radius", type=float, default=1.5)
    parser.add_argument("--a", type=float, default=1.0)
    parser.add_argument("--lambda", dest="lam", type=float, default=1.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run(args.q, args.radius, args.a, args.lam)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Finite uniform-sphere gradient-curvature bench")
        for key, value in result.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
