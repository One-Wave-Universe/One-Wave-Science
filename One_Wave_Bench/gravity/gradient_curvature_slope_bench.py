#!/usr/bin/env python3
"""A-106 gradient+curvature Green-function slope bench.

This bench starts from the candidate far-field energy density already declared in
A-106, with an explicit localized source coupling added for the proof test:

    E = ∫ [a/2 |grad psi|^2 + b/2 (laplacian psi)^2 - J psi] d^3x

with a>0, b>0 and V'(psi)=0 in the far-field region under test.

Variation gives

    b ∇^4 psi - a ∇^2 psi = J.

For J=q delta^3(r), the 3D Green function is

    psi(r) = q/(4 pi a r) * (1 - exp(-r/lambda)),
    lambda = sqrt(b/a).

The corresponding radial slope approaches inverse-square at long range while
its short-range correction dies exponentially. This is a mathematical result
of the declared candidate functional. It is not evidence that the functional
is the physical law of gravity, and q is not identified with gravitational
mass by this bench.
"""

from __future__ import annotations

import argparse
import json
import math


FOUR_PI = 4.0 * math.pi


def screening_length(a: float, b: float) -> float:
    if a <= 0.0 or b <= 0.0:
        raise ValueError("a and b must be positive")
    return math.sqrt(b / a)


def potential(r: float, a: float = 1.0, b: float = 1.0, q: float = 1.0) -> float:
    """Point-source Green-function potential.

    The r=0 value is returned by its analytic finite limit.
    """
    if r < 0.0:
        raise ValueError("r must be non-negative")
    lam = screening_length(a, b)
    prefactor = q / (FOUR_PI * a)
    if r == 0.0:
        return prefactor / lam
    return prefactor * (-math.expm1(-r / lam)) / r


def inverse_square_slope(r: float, a: float = 1.0, q: float = 1.0) -> float:
    if r <= 0.0:
        raise ValueError("r must be positive")
    return abs(q) / (FOUR_PI * a * r * r)


def slope_ratio_to_inverse_square(r: float, a: float = 1.0, b: float = 1.0) -> float:
    """Return |grad psi| divided by its asymptotic inverse-square slope."""
    if r < 0.0:
        raise ValueError("r must be non-negative")
    lam = screening_length(a, b)
    if r == 0.0:
        return 0.0
    x = r / lam
    return 1.0 - (1.0 + x) * math.exp(-x)


def slope_magnitude(r: float, a: float = 1.0, b: float = 1.0, q: float = 1.0) -> float:
    """Magnitude of the point-source radial slope.

    The r=0 value is the analytic finite limit q/(8 pi a lambda^2).
    """
    if r < 0.0:
        raise ValueError("r must be non-negative")
    lam = screening_length(a, b)
    prefactor = abs(q) / (FOUR_PI * a)
    if r == 0.0:
        return prefactor / (2.0 * lam * lam)
    return inverse_square_slope(r, a=a, q=q) * slope_ratio_to_inverse_square(
        r, a=a, b=b
    )


def relative_curvature_correction(r: float, a: float = 1.0, b: float = 1.0) -> float:
    """Fractional difference from the asymptotic inverse-square slope."""
    if r < 0.0:
        raise ValueError("r must be non-negative")
    lam = screening_length(a, b)
    x = r / lam
    return (1.0 + x) * math.exp(-x)


def assimilation_radius(
    tolerance: float,
    a: float = 1.0,
    b: float = 1.0,
) -> float:
    """Radius where the curvature correction falls below a requested tolerance.

    This is a resolution/compression boundary, not an influence cutoff.
    """
    if not 0.0 < tolerance < 1.0:
        raise ValueError("tolerance must lie strictly between 0 and 1")
    lam = screening_length(a, b)

    lo = 0.0
    hi = lam
    while relative_curvature_correction(hi, a=a, b=b) > tolerance:
        hi *= 2.0

    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if relative_curvature_correction(mid, a=a, b=b) > tolerance:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def has_massless_far_field_mode(local_pinning_mu2: float) -> bool:
    """A structural pole test for adding V ~= mu^2 psi^2/2 in the far field.

    Fourier denominator:
        b k^4 + a k^2 + mu^2

    A 1/k^2 pole, and therefore the unscreened 1/r Green-function component,
    exists only when mu^2 is zero. This does not assert that D-413's mechanical
    anchor is literally this continuum term; it flags the same pinning risk.
    """
    if local_pinning_mu2 < 0.0:
        raise ValueError("mu^2 must be non-negative")
    return local_pinning_mu2 == 0.0


def report(a: float = 1.0, b: float = 1.0, q: float = 1.0) -> dict:
    lam = screening_length(a, b)
    samples = []
    for x in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0):
        r = x * lam
        samples.append(
            {
                "r_over_lambda": x,
                "potential": potential(r, a=a, b=b, q=q),
                "slope_magnitude": slope_magnitude(r, a=a, b=b, q=q),
                "inverse_square_ratio": slope_ratio_to_inverse_square(r, a=a, b=b),
                "curvature_correction_fraction": relative_curvature_correction(
                    r, a=a, b=b
                ),
            }
        )

    tolerances = {}
    for eps in (0.10, 0.05, 0.01, 0.001):
        radius = assimilation_radius(eps, a=a, b=b)
        tolerances[str(eps)] = {
            "radius": radius,
            "radius_over_lambda": radius / lam,
        }

    return {
        "model": "A-106 gradient+curvature far-field point-source control",
        "claim_status": "MATHEMATICALLY_DERIVED_UNDER_DECLARED_FUNCTIONAL_NOT_PHYSICALLY_VALIDATED",
        "equation": "b nabla^4 psi - a nabla^2 psi = J",
        "green_function": "q/(4*pi*a*r) * (1-exp(-r/lambda))",
        "lambda": lam,
        "a": a,
        "b": b,
        "q": q,
        "far_field": "slope -> q/(4*pi*a*r^2)",
        "core": "potential and slope remain finite for the idealized point source",
        "assimilation_interpretation": (
            "curvature correction becomes unresolved below declared tolerance; "
            "long-range gradient mode remains active"
        ),
        "assumptions": [
            "3 spatial dimensions",
            "a > 0 and b > 0",
            "localized source coupling -J*psi is declared",
            "V'(psi)=0 in the far-field region under test",
            "source normalization q is not yet identified with gravitational mass",
        ],
        "pinning_warning": (
            "A nonzero quadratic far-field pinning term removes the massless k=0 pole "
            "and therefore removes the unscreened 1/r component."
        ),
        "samples": samples,
        "tolerance_boundaries": tolerances,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Derive and inspect the A-106 gradient+curvature slope law."
    )
    parser.add_argument("--a", type=float, default=1.0)
    parser.add_argument("--b", type=float, default=1.0)
    parser.add_argument("--q", type=float, default=1.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = report(a=args.a, b=args.b, q=args.q)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print("A-106 gradient+curvature slope bench")
    print("=" * 39)
    print(f"lambda = sqrt(b/a) = {payload['lambda']:.9g}")
    print("r/lambda    slope / inverse-square    curvature correction")
    for row in payload["samples"]:
        print(
            f"{row['r_over_lambda']:>7.2f}    "
            f"{row['inverse_square_ratio']:>14.9f}    "
            f"{row['curvature_correction_fraction']:>14.9f}"
        )
    print()
    for eps, row in payload["tolerance_boundaries"].items():
        print(
            f"correction <= {float(eps):.3%}: "
            f"r >= {row['radius_over_lambda']:.6f} lambda"
        )
    print()
    print("Result: curvature regularizes the local mode; the gradient mode carries")
    print("an unscreened inverse-square far-field slope under the declared assumptions.")
    print("This is a mathematical bridge, not physical confirmation of One-Wave gravity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
