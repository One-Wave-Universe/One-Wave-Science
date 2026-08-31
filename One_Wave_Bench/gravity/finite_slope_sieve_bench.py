#!/usr/bin/env python3
"""Finite-slope / sieve proof bench.

This bench deliberately separates three claims:

1. A body-specific *absolute background* crossing radius.
2. A local differential/tidal dominance radius.
3. Hierarchical far-field compression ("assimilation") versus a hard cutoff.

The Newtonian inverse-square equations here are a control model. Passing these
tests does not establish a new gravitational law.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence, Tuple

Vec3 = Tuple[float, float, float]
G_SI = 6.67430e-11
AU_M = 149_597_870_700.0

MASS_SUN_KG = 1.98847e30
MASS_EARTH_KG = 5.9722e24
MASS_MOON_KG = 7.342e22
MASS_JUPITER_KG = 1.89813e27

EARTH_SUN_M = AU_M
MOON_EARTH_M = 384_400_000.0
JUPITER_SUN_M = 5.2044 * AU_M


@dataclass(frozen=True)
class Body:
    name: str
    mass: float
    position: Vec3


def v_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_scale(a: Vec3, scalar: float) -> Vec3:
    return (a[0] * scalar, a[1] * scalar, a[2] * scalar)


def v_norm(a: Vec3) -> float:
    return sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def acceleration_from_body(
    target: Vec3,
    source: Body,
    gravitational_constant: float = G_SI,
) -> Vec3:
    delta = v_sub(source.position, target)
    r2 = delta[0] ** 2 + delta[1] ** 2 + delta[2] ** 2
    if r2 == 0.0:
        raise ValueError("target and source cannot occupy the same point")
    coefficient = gravitational_constant * source.mass / (r2 * sqrt(r2))
    return v_scale(delta, coefficient)


def direct_acceleration(
    target: Vec3,
    sources: Iterable[Body],
    gravitational_constant: float = G_SI,
) -> Vec3:
    total = (0.0, 0.0, 0.0)
    for source in sources:
        total = v_add(
            total,
            acceleration_from_body(target, source, gravitational_constant),
        )
    return total


def center_of_mass(sources: Sequence[Body]) -> Vec3:
    total_mass = sum(body.mass for body in sources)
    if total_mass <= 0.0:
        raise ValueError("aggregate mass must be positive")
    return tuple(
        sum(body.mass * body.position[axis] for body in sources) / total_mass
        for axis in range(3)
    )  # type: ignore[return-value]


def aggregate_monopole(sources: Sequence[Body], name: str = "parent") -> Body:
    return Body(
        name=name,
        mass=sum(body.mass for body in sources),
        position=center_of_mass(sources),
    )


def group_radius(sources: Sequence[Body]) -> float:
    center = center_of_mass(sources)
    return max(v_norm(v_sub(body.position, center)) for body in sources)


def opening_ratio(target: Vec3, sources: Sequence[Body]) -> float:
    """Return a/R for a source cluster about its center of mass."""
    center = center_of_mass(sources)
    distance = v_norm(v_sub(target, center))
    if distance == 0.0:
        return float("inf")
    return group_radius(sources) / distance


def relative_vector_error(reference: Vec3, approximation: Vec3) -> float:
    denominator = v_norm(reference)
    if denominator == 0.0:
        return v_norm(v_sub(reference, approximation))
    return v_norm(v_sub(reference, approximation)) / denominator


def absolute_background_crossing_radius(
    parent_distance: float,
    local_mass: float,
    parent_mass: float,
) -> float:
    """Solve G*m/r^2 = G*M/R^2.

    This candidate compares local slope to the *magnitude* of the parent slope,
    not to the local change in that reference slope. It is included so the
    bench can attack it explicitly.
    """
    if min(parent_distance, local_mass, parent_mass) <= 0.0:
        raise ValueError("distance and masses must be positive")
    return parent_distance * sqrt(local_mass / parent_mass)


def differential_dominance_radius(
    parent_distance: float,
    local_mass: float,
    parent_mass: float,
    kappa: float = 3.0,
) -> float:
    """Solve G*m/r^2 = kappa*G*M*r/R^3.

    kappa=2 is the first radial derivative of an inverse-square parent field.
    kappa=3 is the standard circular rotating-frame/Hill control coefficient.
    """
    if min(parent_distance, local_mass, parent_mass, kappa) <= 0.0:
        raise ValueError("distance, masses, and kappa must be positive")
    return parent_distance * (local_mass / (kappa * parent_mass)) ** (1.0 / 3.0)


def differential_balance_residual(
    radius: float,
    parent_distance: float,
    local_mass: float,
    parent_mass: float,
    kappa: float = 3.0,
    gravitational_constant: float = G_SI,
) -> float:
    local = gravitational_constant * local_mass / radius**2
    reference_change = (
        kappa
        * gravitational_constant
        * parent_mass
        * radius
        / parent_distance**3
    )
    return local - reference_change


def monopole_compression_error(
    target: Vec3,
    sources: Sequence[Body],
    gravitational_constant: float = 1.0,
) -> float:
    direct = direct_acceleration(target, sources, gravitational_constant)
    compressed = direct_acceleration(
        target,
        [aggregate_monopole(sources)],
        gravitational_constant,
    )
    return relative_vector_error(direct, compressed)


def boundary_report() -> dict:
    earth_absolute = absolute_background_crossing_radius(
        EARTH_SUN_M, MASS_EARTH_KG, MASS_SUN_KG
    )
    earth_differential = differential_dominance_radius(
        EARTH_SUN_M, MASS_EARTH_KG, MASS_SUN_KG, kappa=3.0
    )
    moon_differential = differential_dominance_radius(
        MOON_EARTH_M, MASS_MOON_KG, MASS_EARTH_KG, kappa=3.0
    )
    jupiter_differential = differential_dominance_radius(
        JUPITER_SUN_M, MASS_JUPITER_KG, MASS_SUN_KG, kappa=3.0
    )

    # Simple geometry control using the difference of mean orbital radii.
    # This is not advertised as a current ephemeris separation.
    nominal_earth_jupiter_separation = JUPITER_SUN_M - EARTH_SUN_M

    return {
        "earth_sun_absolute_crossing_m": earth_absolute,
        "earth_sun_differential_boundary_m": earth_differential,
        "moon_orbit_m": MOON_EARTH_M,
        "absolute_crossing_contains_moon": earth_absolute > MOON_EARTH_M,
        "differential_boundary_contains_moon": earth_differential > MOON_EARTH_M,
        "moon_earth_differential_boundary_m": moon_differential,
        "jupiter_sun_differential_boundary_m": jupiter_differential,
        "nominal_earth_jupiter_separation_m": nominal_earth_jupiter_separation,
        "jupiter_hard_cutoff_would_reach_earth": (
            jupiter_differential >= nominal_earth_jupiter_separation
        ),
        "interpretation": (
            "Differential/Hill-like radius is a dominance or independent-resolution "
            "boundary. It is not a valid hard influence cutoff."
        ),
    }


def compression_report() -> list[dict]:
    # Dimensionless symmetric binary source. Center of mass is exactly at zero,
    # so the dipole moment vanishes. The leading far-field correction is then
    # quadrupolar and the monopole acceleration error falls ~ (a/R)^2.
    sources = [
        Body("left", 1.0, (-1.0, 0.0, 0.0)),
        Body("right", 1.0, (1.0, 0.0, 0.0)),
    ]
    rows = []
    for distance in (3.0, 5.0, 10.0, 20.0, 50.0, 100.0):
        target = (0.0, distance, 0.0)
        theta = opening_ratio(target, sources)
        error = monopole_compression_error(target, sources, gravitational_constant=1.0)
        rows.append(
            {
                "distance": distance,
                "opening_ratio_a_over_R": theta,
                "monopole_relative_acceleration_error": error,
                "error_over_theta_squared": error / (theta * theta),
            }
        )
    return rows


def run_report() -> dict:
    return {
        "claim_status": {
            "absolute_background_cutoff": "FAIL_AS_GENERAL_BOUNDARY",
            "differential_dominance_boundary": "PASS_STANDARD_CONTROL_DERIVATION",
            "hard_finite_influence_cutoff": "FAIL_AGAINST_NONZERO_FAR_FIELD_CONTROL",
            "hierarchical_parent_assimilation": "PASS_STANDARD_MULTIPOLE_CONTROL",
            "one_wave_physical_law": "INCONCLUSIVE_UNTIL_FIELD_LAW_IS_DERIVED",
        },
        "boundary": boundary_report(),
        "compression": compression_report(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Attack finite-slope boundary and sieve assimilation logic."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )
    args = parser.parse_args()

    report = run_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        boundary = report["boundary"]
        print("Finite-slope / sieve proof bench")
        print("=" * 34)
        print(
            "Earth absolute-background crossing: "
            f"{boundary['earth_sun_absolute_crossing_m'] / 1e6:.3f} million km"
        )
        print(
            "Earth differential/Hill boundary:   "
            f"{boundary['earth_sun_differential_boundary_m'] / 1e6:.3f} million km"
        )
        print(f"Moon orbital radius:                 {MOON_EARTH_M / 1e6:.3f} million km")
        print(
            "Absolute candidate contains Moon?   "
            f"{boundary['absolute_crossing_contains_moon']}"
        )
        print(
            "Differential candidate contains Moon? "
            f"{boundary['differential_boundary_contains_moon']}"
        )
        print()
        print("Far-field parent compression")
        for row in report["compression"]:
            print(
                f"a/R={row['opening_ratio_a_over_R']:.3f} "
                f"relative acceleration error="
                f"{row['monopole_relative_acceleration_error']:.6g}"
            )
        print()
        print("Conclusion:")
        print("- hard cutoff is not assimilation")
        print("- local differential boundary is a dominance boundary")
        print("- distant structure can be compressed into parent moments with controlled error")
        print("- a One-Wave physical proof still requires its own derived field law")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
