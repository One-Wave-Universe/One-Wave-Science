#!/usr/bin/env python3
"""Exact equilateral three-body benchmark for the gradient-curvature kernel.

The pair acceleration used here is the point-source slope derived in
Internal_Proofs/09, with one extra physical-identification assumption made
explicit: source strength and response strength share one common proportionality
to inertial mass. With that assumption the interaction is reciprocal and may be
written with one constant K:

    a_i = K sum_{j!=i} m_j F(r_ij/lambda) (r_j-r_i)/r_ij^3

where

    F(x) = 1 - (1+x) exp(-x).

For any three masses at equal pair separation s, the configuration has an exact
rigidly rotating equilateral solution with

    omega^2 = K M_total F(s/lambda) / s^3.

This is an exact solution of this candidate pair law, not a solution of the
general three-body problem and not experimental validation of One-Wave gravity.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Iterable, Sequence


Vec2 = tuple[float, float]


@dataclass(frozen=True)
class ThreeBodyState:
    masses: tuple[float, float, float]
    positions: tuple[Vec2, Vec2, Vec2]
    velocities: tuple[Vec2, Vec2, Vec2]
    side: float
    lam: float
    coupling: float
    omega: float


def kernel_factor(x: float) -> float:
    if x < 0.0:
        raise ValueError("x must be non-negative")
    return 1.0 - (1.0 + x) * math.exp(-x)


def pair_potential_shape(r: float, lam: float) -> float:
    """Return (1-exp(-r/lambda))/r with its finite r=0 limit."""
    if r < 0.0 or lam <= 0.0:
        raise ValueError("r must be non-negative and lambda positive")
    if r == 0.0:
        return 1.0 / lam
    return -math.expm1(-r / lam) / r


def center_of_mass(masses: Sequence[float], positions: Sequence[Vec2]) -> Vec2:
    total = sum(masses)
    if total <= 0.0 or any(m <= 0.0 for m in masses):
        raise ValueError("masses must be positive")
    return (
        sum(m * p[0] for m, p in zip(masses, positions)) / total,
        sum(m * p[1] for m, p in zip(masses, positions)) / total,
    )


def shift_to_com(masses: Sequence[float], positions: Sequence[Vec2]) -> tuple[Vec2, ...]:
    cx, cy = center_of_mass(masses, positions)
    return tuple((x - cx, y - cy) for x, y in positions)


def accelerations(
    masses: Sequence[float],
    positions: Sequence[Vec2],
    lam: float,
    coupling: float = 1.0,
) -> tuple[Vec2, ...]:
    if lam <= 0.0 or coupling <= 0.0:
        raise ValueError("lambda and coupling must be positive")
    if len(masses) != len(positions):
        raise ValueError("masses and positions must have equal length")

    out: list[Vec2] = []
    for i, (xi, yi) in enumerate(positions):
        ax = 0.0
        ay = 0.0
        for j, (xj, yj) in enumerate(positions):
            if i == j:
                continue
            dx = xj - xi
            dy = yj - yi
            r = math.hypot(dx, dy)
            if r == 0.0:
                raise ValueError("distinct bodies cannot occupy the same point")
            factor = coupling * masses[j] * kernel_factor(r / lam) / (r**3)
            ax += factor * dx
            ay += factor * dy
        out.append((ax, ay))
    return tuple(out)


def equilateral_state(
    masses: Sequence[float] = (1.0, 2.0, 3.0),
    side: float = 4.0,
    lam: float = 0.8,
    coupling: float = 1.0,
) -> ThreeBodyState:
    if len(masses) != 3 or any(m <= 0.0 for m in masses):
        raise ValueError("exactly three positive masses are required")
    if side <= 0.0 or lam <= 0.0 or coupling <= 0.0:
        raise ValueError("side, lambda, and coupling must be positive")

    raw = (
        (0.0, 0.0),
        (side, 0.0),
        (0.5 * side, 0.5 * math.sqrt(3.0) * side),
    )
    positions = shift_to_com(masses, raw)
    total_mass = sum(masses)
    f = kernel_factor(side / lam)
    omega2 = coupling * total_mass * f / (side**3)
    omega = math.sqrt(omega2)
    velocities = tuple((-omega * y, omega * x) for x, y in positions)

    return ThreeBodyState(
        masses=tuple(float(m) for m in masses),
        positions=positions,  # type: ignore[arg-type]
        velocities=velocities,  # type: ignore[arg-type]
        side=side,
        lam=lam,
        coupling=coupling,
        omega=omega,
    )


def closure_residual(state: ThreeBodyState) -> dict:
    acc = accelerations(
        state.masses,
        state.positions,
        state.lam,
        state.coupling,
    )
    omega2 = state.omega * state.omega
    residuals = []
    for position, measured in zip(state.positions, acc):
        expected = (-omega2 * position[0], -omega2 * position[1])
        residuals.append(math.hypot(measured[0] - expected[0], measured[1] - expected[1]))
    return {
        "per_body_vector_residual": residuals,
        "max_vector_residual": max(residuals),
    }


def total_momentum(masses: Sequence[float], velocities: Sequence[Vec2]) -> Vec2:
    return (
        sum(m * v[0] for m, v in zip(masses, velocities)),
        sum(m * v[1] for m, v in zip(masses, velocities)),
    )


def total_angular_momentum(
    masses: Sequence[float],
    positions: Sequence[Vec2],
    velocities: Sequence[Vec2],
) -> float:
    return sum(m * (p[0] * v[1] - p[1] * v[0]) for m, p, v in zip(masses, positions, velocities))


def total_energy(
    masses: Sequence[float],
    positions: Sequence[Vec2],
    velocities: Sequence[Vec2],
    lam: float,
    coupling: float,
) -> float:
    kinetic = 0.5 * sum(
        m * (v[0] * v[0] + v[1] * v[1])
        for m, v in zip(masses, velocities)
    )
    potential = 0.0
    for i in range(len(masses)):
        for j in range(i + 1, len(masses)):
            dx = positions[j][0] - positions[i][0]
            dy = positions[j][1] - positions[i][1]
            r = math.hypot(dx, dy)
            potential -= (
                coupling
                * masses[i]
                * masses[j]
                * pair_potential_shape(r, lam)
            )
    return kinetic + potential


def side_lengths(positions: Sequence[Vec2]) -> tuple[float, float, float]:
    pairs = ((0, 1), (1, 2), (2, 0))
    return tuple(
        math.hypot(
            positions[j][0] - positions[i][0],
            positions[j][1] - positions[i][1],
        )
        for i, j in pairs
    )  # type: ignore[return-value]


def integrate_verlet(state: ThreeBodyState, periods: float = 1.0, steps_per_period: int = 4000) -> dict:
    if periods <= 0.0 or steps_per_period < 100:
        raise ValueError("periods must be positive and steps_per_period >= 100")

    masses = state.masses
    positions = [list(p) for p in state.positions]
    velocities = [list(v) for v in state.velocities]
    period = 2.0 * math.pi / state.omega
    steps = max(1, round(periods * steps_per_period))
    dt = period / steps_per_period

    initial_energy = total_energy(masses, state.positions, state.velocities, state.lam, state.coupling)
    initial_L = total_angular_momentum(masses, state.positions, state.velocities)
    max_side_spread = 0.0

    current_acc = accelerations(masses, tuple(tuple(p) for p in positions), state.lam, state.coupling)
    for _ in range(steps):
        for i in range(3):
            positions[i][0] += velocities[i][0] * dt + 0.5 * current_acc[i][0] * dt * dt
            positions[i][1] += velocities[i][1] * dt + 0.5 * current_acc[i][1] * dt * dt

        new_acc = accelerations(
            masses,
            tuple(tuple(p) for p in positions),
            state.lam,
            state.coupling,
        )
        for i in range(3):
            velocities[i][0] += 0.5 * (current_acc[i][0] + new_acc[i][0]) * dt
            velocities[i][1] += 0.5 * (current_acc[i][1] + new_acc[i][1]) * dt
        current_acc = new_acc

        lengths = side_lengths(tuple(tuple(p) for p in positions))
        max_side_spread = max(max_side_spread, max(lengths) - min(lengths))

    final_positions = tuple(tuple(p) for p in positions)
    final_velocities = tuple(tuple(v) for v in velocities)
    final_energy = total_energy(masses, final_positions, final_velocities, state.lam, state.coupling)
    final_L = total_angular_momentum(masses, final_positions, final_velocities)

    return {
        "periods": periods,
        "steps": steps,
        "dt": dt,
        "max_side_spread": max_side_spread,
        "max_side_spread_fraction": max_side_spread / state.side,
        "relative_energy_drift": abs(final_energy - initial_energy) / max(abs(initial_energy), 1e-30),
        "relative_angular_momentum_drift": abs(final_L - initial_L) / max(abs(initial_L), 1e-30),
        "final_com": center_of_mass(masses, final_positions),
        "final_total_momentum": total_momentum(masses, final_velocities),
    }


def report(
    masses: Sequence[float] = (1.0, 2.0, 3.0),
    side: float = 4.0,
    lam: float = 0.8,
    coupling: float = 1.0,
    integrate: bool = True,
) -> dict:
    state = equilateral_state(masses=masses, side=side, lam=lam, coupling=coupling)
    f = kernel_factor(side / lam)
    payload = {
        "claim_status": "EXACT_THREE_BODY_SOLUTION_OF_CANDIDATE_PAIR_LAW_UNDER_COMMON_MASS_COUPLING_ASSUMPTION",
        "masses": list(state.masses),
        "side": side,
        "lambda": lam,
        "side_over_lambda": side / lam,
        "coupling": coupling,
        "kernel_factor": f,
        "newtonian_fraction_at_pair_distance": f,
        "omega": state.omega,
        "omega_squared_formula": coupling * sum(masses) * f / side**3,
        "positions_com_frame": [list(p) for p in state.positions],
        "velocities": [list(v) for v in state.velocities],
        "initial_total_momentum": list(total_momentum(state.masses, state.velocities)),
        "initial_angular_momentum": total_angular_momentum(state.masses, state.positions, state.velocities),
        "closure": closure_residual(state),
        "assumptions": [
            "gradient-curvature point-source kernel from Proof 09",
            "one common interaction constant K",
            "source/response coupling proportional to inertial mass",
            "instantaneous pairwise central interaction for this benchmark",
            "no claim of a general closed-form three-body solution",
        ],
    }
    if integrate:
        payload["numerical_orbit_receipt"] = integrate_verlet(state)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Exact equilateral three-body gradient-curvature benchmark")
    parser.add_argument("--masses", nargs=3, type=float, default=(1.0, 2.0, 3.0))
    parser.add_argument("--side", type=float, default=4.0)
    parser.add_argument("--lambda", dest="lam", type=float, default=0.8)
    parser.add_argument("--coupling", type=float, default=1.0)
    parser.add_argument("--no-integrate", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = report(
        masses=args.masses,
        side=args.side,
        lam=args.lam,
        coupling=args.coupling,
        integrate=not args.no_integrate,
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print("Gradient-curvature exact equilateral three-body bench")
    print("=" * 55)
    print(f"masses: {payload['masses']}")
    print(f"side/lambda: {payload['side_over_lambda']:.6g}")
    print(f"kernel/Newtonian fraction: {payload['kernel_factor']:.9f}")
    print(f"omega: {payload['omega']:.9g}")
    print(f"analytic closure residual: {payload['closure']['max_vector_residual']:.3e}")
    if "numerical_orbit_receipt" in payload:
        receipt = payload["numerical_orbit_receipt"]
        print(f"one-orbit side spread fraction: {receipt['max_side_spread_fraction']:.3e}")
        print(f"relative energy drift: {receipt['relative_energy_drift']:.3e}")
        print(f"relative angular momentum drift: {receipt['relative_angular_momentum_drift']:.3e}")
    print()
    print("Exact result: equal pair separation makes the kernel factor common, so")
    print("the three accelerations close on the center-of-mass rotation law.")
    print("This is not the general three-body solution and does not validate the physical coupling assumption.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
