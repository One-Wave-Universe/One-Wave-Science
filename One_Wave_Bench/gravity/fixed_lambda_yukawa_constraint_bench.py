#!/usr/bin/env python3
"""Proof 14 bench: experimental constraint on the universal fixed-lambda kernel."""

from __future__ import annotations
import argparse, json, math

LAMBDA_MAX_95_M = 38.6e-6
G_CODATA_2022 = 6.67430e-11
G_REL_STD_UNCERTAINTY = 2.2e-5


def kernel_factor(x: float) -> float:
    if x < 0:
        raise ValueError("x must be non-negative")
    return 1.0 - (1.0 + x) * math.exp(-x)


def force_deficit_fraction(r: float, lam: float) -> float:
    if r < 0 or lam <= 0:
        raise ValueError("r must be non-negative and lambda positive")
    x = r / lam
    if x > 750:
        return 0.0
    return (1.0 + x) * math.exp(-x)


def x_for_deficit(eps: float) -> float:
    if not (0.0 < eps < 1.0):
        raise ValueError("eps must lie strictly between 0 and 1")
    lo, hi = 0.0, 1.0
    while (1.0 + hi) * math.exp(-hi) > eps:
        hi *= 2.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if (1.0 + mid) * math.exp(-mid) > eps:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def distance_for_deficit(eps: float, lam: float = LAMBDA_MAX_95_M) -> float:
    return x_for_deficit(eps) * lam


def proof13_all_mass_scale_ceiling(lam: float = LAMBDA_MAX_95_M) -> float:
    return 1.79328213290076 * lam


def report() -> dict:
    sample_distances = {
        "52_um": 52e-6,
        "0.1_mm": 0.1e-3,
        "0.25_mm": 0.25e-3,
        "0.5_mm": 0.5e-3,
        "1_mm": 1e-3,
        "1_cm": 1e-2,
        "1_m": 1.0,
        "earth_moon_mean": 384_400_000.0,
        "1_AU": 149_597_870_700.0,
    }
    deficits = {
        key: force_deficit_fraction(value, LAMBDA_MAX_95_M)
        for key, value in sample_distances.items()
    }
    thresholds = {}
    for eps in (1e-2, 1e-3, 1e-6, 1e-9, 1e-12):
        x = x_for_deficit(eps)
        thresholds[f"{eps:.0e}"] = {
            "x": x,
            "distance_m_at_lambda_max": x * LAMBDA_MAX_95_M,
        }
    return {
        "claim_status": "EMPIRICAL_CONSTRAINT_ON_UNIVERSAL_FIXED_LAMBDA_CANDIDATE",
        "exact_mapping": {
            "candidate": "-K*m1*m2*(1-exp(-r/lambda))/r",
            "standard_yukawa": "-G_inf*m1*m2*(1+alpha*exp(-r/lambda))/r",
            "G_inf_equals_K": True,
            "alpha": -1.0,
        },
        "published_external_bound": {
            "lambda_max_95_m": LAMBDA_MAX_95_M,
            "lambda_max_95_um": LAMBDA_MAX_95_M * 1e6,
            "source": "Lee et al., Phys. Rev. Lett. 124, 101101 (2020)",
            "scope": "gravitational-strength Yukawa interaction, 95% confidence",
        },
        "far_field_coupling": {
            "K_identified_with_G_in_far_field": True,
            "G_CODATA_2022_m3_kg-1_s-2": G_CODATA_2022,
            "relative_standard_uncertainty": G_REL_STD_UNCERTAINTY,
        },
        "force_deficit_at_lambda_max": deficits,
        "distance_where_deficit_falls_below": thresholds,
        "proof13_cross_check": {
            "all_positive_mass_modified_stability_region_x_less_than": 1.79328213290076,
            "scale_ceiling_m_at_lambda_max": proof13_all_mass_scale_ceiling(),
            "scale_ceiling_um_at_lambda_max": proof13_all_mass_scale_ceiling() * 1e6,
        },
        "verdict": (
            "For universal constant lambda and fixed alpha=-1, lambda >= 38.6 um is excluded "
            "at 95% confidence by Lee et al. The non-Newtonian correction is therefore confined "
            "to sub-millimetre scales. A macroscopic lambda requires a different model and a new derivation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = report()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("Proof 14 - fixed-lambda experimental constraint")
        print("=" * 51)
        print("Exact Yukawa mapping: alpha = -1, G_inf = K")
        print(f"Published 95% upper bound: lambda < {LAMBDA_MAX_95_M*1e6:.1f} um")
        print(
            "Proof-13 all-positive-mass modified-stability scale < "
            f"{proof13_all_mass_scale_ceiling()*1e6:.3f} um"
        )
        for eps in (1e-2, 1e-3, 1e-6):
            print(
                f"|Delta F|/F < {eps:g} by r > "
                f"{distance_for_deficit(eps)*1e6:.3f} um"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
