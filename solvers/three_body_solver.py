#!/usr/bin/env python3
"""Legacy Gaussian pressure candidate, retained for falsification.

NOT a gravity solver or a derived One-Wave lattice evolution. Positive Gaussian
peaks with -grad(P) repel; division by test mass also breaks unequal-mass pair
momentum balance. field_damping is unused. Do not use this class for orbits.
Run this file for the separately labeled A-115 Newtonian-limit validation.
See THREE_BODY_VALIDATION.md for the original failure and open derivation.
"""

import numpy as np
from scipy.integrate import odeint
from typing import Tuple, Dict, List, Optional
import json

# ============================================================================
# Part 1: Three-Body Dynamics in Pressure Field
# ============================================================================

class ThreeBodyPressureField:
    """Rejected legacy candidate; equations retained to reproduce the failure."""

    def __init__(self, m1: float = 1.0, m2: float = 1.0, m3: float = 1.0,
                 coupling_strength: float = 1.0,
                 field_damping: float = 0.1):
        """
        Initialize three-body system.

        Parameters:
        - m1, m2, m3: Masses (in arbitrary units)
        - coupling_strength: How strongly mass couples to pressure
        - field_damping: Pressure field dissipation rate
        """
        self.masses = [m1, m2, m3]
        self.coupling = coupling_strength
        self.damping = field_damping

    def pressure_from_masses(self, r1: np.ndarray, r2: np.ndarray,
                            r3: np.ndarray, evaluation_point: np.ndarray) -> float:
        """
        Calculate pressure at a point due to three mass distributions.

        Model: Each mass creates a Gaussian pressure profile
        P(r) = Σᵢ mᵢ * exp(-|r - rᵢ|² / σᵢ²)

        where σ is the characteristic size of pressure spike.
        """
        sigma = 1.0  # Characteristic pressure width

        # Pressure contribution from each mass
        P1 = self.masses[0] * np.exp(-np.sum((evaluation_point - r1)**2) / sigma)
        P2 = self.masses[1] * np.exp(-np.sum((evaluation_point - r2)**2) / sigma)
        P3 = self.masses[2] * np.exp(-np.sum((evaluation_point - r3)**2) / sigma)

        return (P1 + P2 + P3) * self.coupling

    def pressure_gradient(self, r1: np.ndarray, r2: np.ndarray,
                         r3: np.ndarray, evaluation_point: np.ndarray,
                         dr: float = 0.001) -> np.ndarray:
        """
        Numerical gradient of pressure field.
        ∇P = (∂P/∂x, ∂P/∂y, ∂P/∂z)
        """
        grad = np.zeros(3)

        for i in range(3):
            r_plus = evaluation_point.copy()
            r_plus[i] += dr
            r_minus = evaluation_point.copy()
            r_minus[i] -= dr

            P_plus = self.pressure_from_masses(r1, r2, r3, r_plus)
            P_minus = self.pressure_from_masses(r1, r2, r3, r_minus)

            grad[i] = (P_plus - P_minus) / (2 * dr)

        return grad

    def equations_of_motion(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        Equations of motion for three bodies in shared pressure field.

        State vector: [x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, ...]

        Acceleration: a = -∇P (pressure gradient drives motion)
        """
        # Extract positions and velocities
        r1 = state[0:3]
        v1 = state[3:6]
        r2 = state[6:9]
        v2 = state[9:12]
        r3 = state[12:15]
        v3 = state[15:18]

        # Calculate pressure gradients at each body's location
        grad_P1 = self.pressure_gradient(r1, r2, r3, r1)
        grad_P2 = self.pressure_gradient(r1, r2, r3, r2)
        grad_P3 = self.pressure_gradient(r1, r2, r3, r3)

        # Accelerations (pressure gradient drives motion)
        a1 = -grad_P1 / self.masses[0]
        a2 = -grad_P2 / self.masses[1]
        a3 = -grad_P3 / self.masses[2]

        # State derivatives
        dstate_dt = np.zeros(18)
        dstate_dt[0:3] = v1
        dstate_dt[3:6] = a1
        dstate_dt[6:9] = v2
        dstate_dt[9:12] = a2
        dstate_dt[12:15] = v3
        dstate_dt[15:18] = a3

        return dstate_dt

# ============================================================================
# Part 2: Initial Conditions & Solutions
# ============================================================================

def euler_restricted_three_body(mass_ratio: float = 1.0):
    """Compatibility helper: equal-mass collinear Newtonian control only."""
    if mass_ratio != 1.0:
        raise ValueError("unequal-mass Euler initial conditions are not implemented")
    try:
        from .three_body_control import euler_collinear, unpack
    except ImportError:
        from three_body_control import euler_collinear, unpack
    state, _ = euler_collinear()
    return state, list(unpack(state)[0])


def figure_eight_three_body():
    """Compatibility helper: published Newtonian figure-eight initial state."""
    try:
        from .three_body_control import figure_eight, unpack
    except ImportError:
        from three_body_control import figure_eight, unpack
    state = figure_eight()
    return state, list(unpack(state)[0])

# ============================================================================
# Part 3: Chaos Analysis
# ============================================================================

class LyapunovExponent:
    """
    Legacy finite-time separation fit in position/velocity coordinates.

    This is not an asymptotic maximum Lyapunov estimate or proof of integrability.
    """

    def __init__(self, solver: ThreeBodyPressureField, initial_state: np.ndarray):
        self.solver = solver
        self.initial_state = initial_state.copy()
        self.perturbation_scale = 1e-8

    def compute(self, t_max: float, dt: float = 0.01) -> float:
        """
        Compute maximum Lyapunov exponent.

        Algorithm:
        1. Evolve system from two slightly different initial conditions
        2. Track divergence of trajectories
        3. λ = lim(t→∞) (1/t) log(|Δx(t)| / |Δx(0)|)
        """
        t = np.arange(0, t_max, dt)

        # Nominal trajectory
        traj1 = odeint(self.solver.equations_of_motion, self.initial_state, t)

        # Perturbed trajectory
        perturbed_state = self.initial_state.copy()
        perturbed_state[0] += self.perturbation_scale  # Small perturbation in x1
        traj2 = odeint(self.solver.equations_of_motion, perturbed_state, t)

        # Compute divergence
        divergence = np.linalg.norm(traj2 - traj1, axis=1)

        # Fit exponential growth (only regions where divergence is clear)
        valid_indices = (divergence > self.perturbation_scale * 1e2) & (divergence < 1.0)

        if np.sum(valid_indices) > 10:
            t_valid = t[valid_indices]
            div_valid = divergence[valid_indices]

            # Fit: log(divergence) = λ * t + const
            log_div = np.log(div_valid)
            coeffs = np.polyfit(t_valid, log_div, 1)
            lyapunov = coeffs[0]
        else:
            lyapunov = float("nan")  # Insufficient fit data: inconclusive, not integrable

        return float(lyapunov), t, divergence

# ============================================================================
# Part 4: Main Analysis
# ============================================================================

if __name__ == "__main__":
    try:
        from .three_body_control import main
    except ImportError:
        from three_body_control import main
    raise SystemExit(main())
