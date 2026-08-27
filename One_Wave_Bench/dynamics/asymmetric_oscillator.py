"""Dimensionless asymmetric center-origin oscillator reference mechanics.

Equation:
    x_ddot + c*x_dot + a*x^3 - b*x - h = u(t)

with c=2*zeta*omega_ref and potential
    V(x)=a*x^4/4-b*x^2/2-h*x.

This is a controlled candidate for gate mechanics, not the foundational
One-Wave field equation.  Its value is that equilibria, folds, stability, and
the energy ledger are exact and testable before coupling it to a field solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Callable, Iterable, Tuple

import numpy as np


Drive = Callable[[float], float]


@dataclass(frozen=True)
class OscillatorParameters:
    a: float = 1.0
    b: float = 1.0
    zeta: float = 0.15
    omega_ref: float = 1.0
    bias: float = 0.0

    def __post_init__(self) -> None:
        if self.a <= 0.0 or self.b <= 0.0:
            raise ValueError("a and b must be positive for the bounded double well")
        if self.zeta < 0.0 or self.omega_ref <= 0.0:
            raise ValueError("zeta must be nonnegative and omega_ref positive")

    @property
    def damping(self) -> float:
        return 2.0 * self.zeta * self.omega_ref

    @property
    def fold_bias(self) -> float:
        """Magnitude of the saddle-node bias for a*x^3-b*x-h=0."""
        return 2.0 * self.b ** 1.5 / (3.0 * sqrt(3.0 * self.a))


@dataclass(frozen=True)
class Equilibrium:
    x: float
    curvature: float
    stable: bool
    potential: float


@dataclass(frozen=True)
class Barrier:
    well_position: float
    saddle_position: float
    barrier_energy: float


@dataclass(frozen=True)
class LinearResponse:
    equilibrium_position: float
    drive_frequency: float
    amplitude_per_unit_drive: float
    phase_lag: float


def potential(x: np.ndarray | float, p: OscillatorParameters) -> np.ndarray | float:
    return 0.25 * p.a * np.asarray(x) ** 4 - 0.5 * p.b * np.asarray(x) ** 2 - p.bias * np.asarray(x)


def potential_gradient(x: np.ndarray | float, p: OscillatorParameters) -> np.ndarray | float:
    return p.a * np.asarray(x) ** 3 - p.b * np.asarray(x) - p.bias


def equilibria(p: OscillatorParameters, tolerance: float = 1e-10) -> Tuple[Equilibrium, ...]:
    roots = np.roots((p.a, 0.0, -p.b, -p.bias))
    real_roots = sorted(float(root.real) for root in roots if abs(root.imag) <= tolerance)
    result = []
    for x in real_roots:
        curvature = 3.0 * p.a * x*x - p.b
        result.append(Equilibrium(x, curvature, curvature > tolerance, float(potential(x, p))))
    return tuple(result)


def barrier_heights(p: OscillatorParameters) -> Tuple[Barrier, ...]:
    """Conservative well-to-saddle barriers below the fold."""
    states = equilibria(p)
    saddles = [state for state in states if not state.stable]
    if len(saddles) != 1:
        return ()
    saddle = saddles[0]
    return tuple(
        Barrier(state.x, saddle.x, saddle.potential-state.potential)
        for state in states if state.stable
    )


def linear_response(
    p: OscillatorParameters,
    equilibrium_position: float,
    drive_frequency: float,
) -> LinearResponse:
    """Exact small-signal response after linearization around a stable well."""
    if drive_frequency < 0.0:
        raise ValueError("drive_frequency must be nonnegative")
    stiffness = 3.0*p.a*equilibrium_position**2-p.b
    if stiffness <= 0.0:
        raise ValueError("linear response requires a stable equilibrium")
    real = stiffness-drive_frequency**2
    imaginary = p.damping*drive_frequency
    amplitude = 1.0/sqrt(real*real+imaginary*imaginary)
    phase = float(np.arctan2(imaginary, real))
    return LinearResponse(equilibrium_position, drive_frequency, amplitude, phase)


def acceleration(t: float, x: float, v: float, p: OscillatorParameters, drive: Drive) -> float:
    return drive(t) - p.damping * v - float(potential_gradient(x, p))


def _rk4_step(t: float, x: float, v: float, dt: float, p: OscillatorParameters, drive: Drive) -> Tuple[float, float]:
    def rhs(time: float, position: float, velocity: float) -> Tuple[float, float]:
        return velocity, acceleration(time, position, velocity, p, drive)

    k1x, k1v = rhs(t, x, v)
    k2x, k2v = rhs(t + 0.5*dt, x + 0.5*dt*k1x, v + 0.5*dt*k1v)
    k3x, k3v = rhs(t + 0.5*dt, x + 0.5*dt*k2x, v + 0.5*dt*k2v)
    k4x, k4v = rhs(t + dt, x + dt*k3x, v + dt*k3v)
    return (
        x + dt*(k1x + 2*k2x + 2*k3x + k4x)/6.0,
        v + dt*(k1v + 2*k2v + 2*k3v + k4v)/6.0,
    )


@dataclass(frozen=True)
class Trajectory:
    time: np.ndarray
    x: np.ndarray
    v: np.ndarray
    drive: np.ndarray
    energy: np.ndarray
    balance_residual: np.ndarray

    def center_crossings(self, center_band: float = 0.0) -> int:
        if center_band < 0.0:
            raise ValueError("center_band must be nonnegative")
        side = np.where(self.x > center_band, 1, np.where(self.x < -center_band, -1, 0))
        nonzero = side[side != 0]
        return int(np.count_nonzero(nonzero[1:] != nonzero[:-1])) if nonzero.size > 1 else 0

    def center_dwell_fraction(self, center_band: float) -> float:
        if center_band < 0.0:
            raise ValueError("center_band must be nonnegative")
        return float(np.mean(np.abs(self.x) <= center_band))


def simulate(
    p: OscillatorParameters,
    x0: float,
    v0: float,
    duration: float,
    dt: float,
    drive: Drive = lambda _t: 0.0,
) -> Trajectory:
    if duration <= 0.0 or dt <= 0.0:
        raise ValueError("duration and dt must be positive")
    steps = int(round(duration / dt))
    time = np.linspace(0.0, steps*dt, steps + 1)
    x = np.empty(steps + 1)
    v = np.empty(steps + 1)
    applied = np.empty(steps + 1)
    x[0], v[0], applied[0] = x0, v0, drive(0.0)
    for index in range(steps):
        x[index + 1], v[index + 1] = _rk4_step(time[index], x[index], v[index], dt, p, drive)
        applied[index + 1] = drive(time[index + 1])

    energy = 0.5*v*v + potential(x, p)
    power = applied*v - p.damping*v*v
    cumulative = np.zeros_like(time)
    cumulative[1:] = np.cumsum(0.5*(power[1:] + power[:-1])*dt)
    residual = energy - energy[0] - cumulative
    return Trajectory(time, x, v, applied, energy, residual)


@dataclass(frozen=True)
class BiasSweepRow:
    bias: float
    fold_ratio: float
    equilibrium_count: int
    stable_count: int
    stable_positions: Tuple[float, ...]
    unstable_positions: Tuple[float, ...]


def sweep_bias(values: Iterable[float], base: OscillatorParameters = OscillatorParameters()) -> Tuple[BiasSweepRow, ...]:
    rows = []
    for bias in values:
        p = OscillatorParameters(base.a, base.b, base.zeta, base.omega_ref, float(bias))
        states = equilibria(p)
        rows.append(BiasSweepRow(
            bias=float(bias),
            fold_ratio=float(bias) / p.fold_bias,
            equilibrium_count=len(states),
            stable_count=sum(state.stable for state in states),
            stable_positions=tuple(state.x for state in states if state.stable),
            unstable_positions=tuple(state.x for state in states if not state.stable),
        ))
    return tuple(rows)


if __name__ == "__main__":
    base = OscillatorParameters()
    print(f"fold_bias={base.fold_bias:.9f}")
    for row in sweep_bias(np.linspace(-0.6, 0.6, 13), base):
        print(row)
