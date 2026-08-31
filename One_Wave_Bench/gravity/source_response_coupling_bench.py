#!/usr/bin/env python3
"""Source/response coupling theorem bench.

This bench does not assume source strength is inertial mass. It separates three
body properties:

    m_i      inertial Mass Effect
    q_i      source charge entering the linear field equation
    beta_i   response charge multiplying the field gradient in force

For a reciprocal central Green-function kernel K_ij = -K_ji,

    F_i<-j = beta_i q_j K_ij.

Pair momentum conservation requires beta_i q_j = beta_j q_i for every pair.
Composition-independent free fall in a fixed external field requires
beta_i/m_i to be the same for every test body. Together, for nonzero positive
couplings, these requirements force

    beta_i = c_beta m_i
    q_i    = c_q    m_i.

The bench verifies those algebraic conditions and demonstrates how violating
either one produces an observable failure. It does not derive the microscopic
values of c_beta or c_q, or prove that nature follows this scalar coupling.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Sequence


Vec2 = tuple[float, float]


@dataclass(frozen=True)
class CouplingBody:
    name: str
    mass: float
    source_q: float
    response_beta: float
    position: Vec2 = (0.0, 0.0)

    def validate(self) -> None:
        if self.mass <= 0.0:
            raise ValueError("inertial mass must be positive")
        if self.source_q == 0.0 or self.response_beta == 0.0:
            raise ValueError("this theorem bench assumes nonzero source and response couplings")


def kernel_factor(x: float) -> float:
    if x < 0.0:
        raise ValueError("x must be non-negative")
    return 1.0 - (1.0 + x) * math.exp(-x)


def gradient_kernel_vector(source: Vec2, target: Vec2, lam: float = 1.0) -> Vec2:
    """Return an attractive gradient-curvature kernel pointing target->source."""
    if lam <= 0.0:
        raise ValueError("lambda must be positive")
    dx = source[0] - target[0]
    dy = source[1] - target[1]
    r = math.hypot(dx, dy)
    if r == 0.0:
        raise ValueError("source and target positions must differ")
    scale = kernel_factor(r / lam) / (r**3)
    return (scale * dx, scale * dy)


def pair_force_on_i_from_j(i: CouplingBody, j: CouplingBody, lam: float = 1.0) -> Vec2:
    i.validate()
    j.validate()
    kx, ky = gradient_kernel_vector(j.position, i.position, lam=lam)
    coefficient = i.response_beta * j.source_q
    return (coefficient * kx, coefficient * ky)


def pair_reciprocity_algebraic_residual(i: CouplingBody, j: CouplingBody) -> float:
    """Return beta_i*q_j - beta_j*q_i; zero is exact pair reciprocity."""
    i.validate()
    j.validate()
    return i.response_beta * j.source_q - j.response_beta * i.source_q


def normalized_pair_reciprocity_residual(i: CouplingBody, j: CouplingBody) -> float:
    left = i.response_beta * j.source_q
    right = j.response_beta * i.source_q
    denominator = max(abs(left), abs(right), 1e-300)
    return abs(left - right) / denominator


def pair_net_force(i: CouplingBody, j: CouplingBody, lam: float = 1.0) -> Vec2:
    fij = pair_force_on_i_from_j(i, j, lam=lam)
    fji = pair_force_on_i_from_j(j, i, lam=lam)
    return (fij[0] + fji[0], fij[1] + fji[1])


def response_per_inertial_mass(body: CouplingBody) -> float:
    body.validate()
    return body.response_beta / body.mass


def source_per_inertial_mass(body: CouplingBody) -> float:
    body.validate()
    return body.source_q / body.mass


def relative_spread(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("at least one value is required")
    scale = max(max(abs(v) for v in values), 1e-300)
    return (max(values) - min(values)) / scale


def reciprocity_residual(bodies: Sequence[CouplingBody]) -> float:
    if len(bodies) < 2:
        raise ValueError("at least two bodies are required")
    return max(
        normalized_pair_reciprocity_residual(bodies[i], bodies[j])
        for i in range(len(bodies))
        for j in range(i + 1, len(bodies))
    )


def universal_fall_residual(bodies: Sequence[CouplingBody]) -> float:
    return relative_spread([response_per_inertial_mass(body) for body in bodies])


def source_mass_residual(bodies: Sequence[CouplingBody]) -> float:
    return relative_spread([source_per_inertial_mass(body) for body in bodies])


def total_internal_force(bodies: Sequence[CouplingBody], lam: float = 1.0) -> Vec2:
    total_x = 0.0
    total_y = 0.0
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i == j:
                continue
            fx, fy = pair_force_on_i_from_j(bodies[i], bodies[j], lam=lam)
            total_x += fx
            total_y += fy
    return (total_x, total_y)


def external_acceleration_factor(body: CouplingBody) -> float:
    """Test-body factor multiplying any fixed external source gradient."""
    return response_per_inertial_mass(body)


def proportional_bodies(
    masses: Sequence[float],
    source_per_mass: float = 2.0,
    response_per_mass: float = 3.0,
    positions: Sequence[Vec2] | None = None,
) -> tuple[CouplingBody, ...]:
    if positions is None:
        positions = tuple((float(i), 0.3 * i * i + 0.1) for i in range(len(masses)))
    if len(positions) != len(masses):
        raise ValueError("positions and masses must have equal length")
    return tuple(
        CouplingBody(
            name=f"body_{i}",
            mass=float(mass),
            source_q=source_per_mass * float(mass),
            response_beta=response_per_mass * float(mass),
            position=positions[i],
        )
        for i, mass in enumerate(masses)
    )


def scenario_report(name: str, bodies: Sequence[CouplingBody], lam: float = 1.0) -> dict:
    net = total_internal_force(bodies, lam=lam)
    return {
        "name": name,
        "bodies": [
            {
                "name": b.name,
                "mass": b.mass,
                "source_q": b.source_q,
                "response_beta": b.response_beta,
                "q_over_m": source_per_inertial_mass(b),
                "beta_over_m": response_per_inertial_mass(b),
            }
            for b in bodies
        ],
        "reciprocity_residual": reciprocity_residual(bodies),
        "universal_fall_residual": universal_fall_residual(bodies),
        "source_mass_residual": source_mass_residual(bodies),
        "total_internal_force": list(net),
        "total_internal_force_norm": math.hypot(*net),
    }


def report() -> dict:
    positions = ((-1.2, 0.4), (0.7, -0.8), (2.1, 1.3))

    both = proportional_bodies(
        (1.0, 2.0, 5.0),
        source_per_mass=2.0,
        response_per_mass=3.0,
        positions=positions,
    )

    # q and beta remain proportional to each other, so reciprocity survives,
    # but neither tracks inertial mass universally: free fall fails.
    reciprocal_not_universal = (
        CouplingBody("A", 1.0, 1.0, 4.0, positions[0]),
        CouplingBody("B", 2.0, 3.0, 12.0, positions[1]),
        CouplingBody("C", 5.0, 10.0, 40.0, positions[2]),
    )

    # beta/m is universal, so external free fall survives, but q/m varies;
    # pair action/reaction no longer cancels.
    universal_not_reciprocal = (
        CouplingBody("A", 1.0, 1.0, 3.0, positions[0]),
        CouplingBody("B", 2.0, 7.0, 6.0, positions[1]),
        CouplingBody("C", 5.0, 2.0, 15.0, positions[2]),
    )

    return {
        "theorem": {
            "pair_reciprocity": "beta_i*q_j = beta_j*q_i for all i,j",
            "universal_fall": "beta_i/m_i = constant for all test bodies",
            "combined_conclusion": "beta_i = c_beta*m_i and q_i = c_q*m_i",
        },
        "claim_status": "ALGEBRAIC_COUPLING_CONSTRAINT_NOT_MICROSCOPIC_DERIVATION",
        "scenarios": [
            scenario_report("both_requirements", both),
            scenario_report("reciprocal_but_not_universal_fall", reciprocal_not_universal),
            scenario_report("universal_fall_but_not_reciprocal", universal_not_reciprocal),
        ],
        "open_physics": [
            "derive q from the four-interaction recurrence / J_source",
            "derive beta from the same Ground coupling rather than declaring it",
            "derive the common normalization constants",
            "test whether one fixed normalization survives independent bodies and gravity data",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Source/response reciprocity and universal-fall coupling bench")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = report()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print("Source/response coupling theorem bench")
    print("=" * 39)
    for scenario in payload["scenarios"]:
        print(scenario["name"])
        print(f"  reciprocity residual:   {scenario['reciprocity_residual']:.6g}")
        print(f"  universal-fall residual:{scenario['universal_fall_residual']:.6g}")
        print(f"  q/m residual:           {scenario['source_mass_residual']:.6g}")
        print(f"  |sum internal force|:   {scenario['total_internal_force_norm']:.6g}")
    print()
    print("Combined theorem: reciprocal pair forces + composition-independent free fall")
    print("force q and beta to be proportional to inertial mass within this linear model.")
    print("The proportionality constants remain physical inputs until derived from Ground.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
