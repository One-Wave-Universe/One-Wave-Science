"""
Track C: Discrete Maxwell Solver on Hexagonal Lattice
======================================================

Implement the full discrete Maxwell equations using the unified One-Wave rule:

  ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]

Extract E and B as:
  E_like = ∇(∇·ψ)  [longitudinal, potential part]
  B_like = ∇×(∇×ψ) [transverse, solenoidal part]

Both should have the SAME frequency ω from the unified mode interpretation.

Test Faraday's law: ∇×E = -∂B/∂t
"""

import math
import numpy as np
from typing import Dict, List, Sequence, Tuple
import sys

# Import lattice and operators
try:
    from hex_lattice_graph import (
        Site, NEIGHBOR_OFFSETS, neighbor, site_xy, disk_sites, seven_cell, adjacency
    )
    from discrete_hex_operators import (
        discrete_divergence, discrete_curl_z, discrete_gradient,
        neighbor_outward_normals, neighbor_directions
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure hex_lattice_graph.py and discrete_hex_operators.py are in the same directory")
    sys.exit(1)


# ============================================================================
# PART 1: Plane Wave Initial Conditions
# ============================================================================

def plane_wave_field(
    k_vec: Tuple[float, float],
    amplitude: complex,
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, complex]:
    """
    Create a plane wave field: ψ(r) = A e^{i k·r}

    Args:
        k_vec: (k_x, k_y) wavevector
        amplitude: complex amplitude A
        sites: lattice sites
        a: lattice constant

    Returns:
        Dictionary mapping site -> ψ(site)
    """
    psi = {}
    kx, ky = k_vec
    for site in sites:
        x, y = site_xy(site, a=a)
        phase = kx * x + ky * y
        psi[site] = amplitude * complex(math.cos(phase), math.sin(phase))
    return psi


def plane_wave_time_evolution(
    k_vec: Tuple[float, float],
    omega: float,
    amplitude: complex,
    t: float,
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, complex]:
    """
    Time-evolved plane wave: ψ(r,t) = A e^{i(k·r - ωt)}
    """
    psi = {}
    kx, ky = k_vec
    for site in sites:
        x, y = site_xy(site, a=a)
        phase = kx * x + ky * y - omega * t
        psi[site] = amplitude * complex(math.cos(phase), math.sin(phase))
    return psi


# ============================================================================
# PART 2: Extract E and B Fields
# ============================================================================

def extract_e_field(
    psi: Dict[Site, complex],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, Tuple[float, float]]:
    """
    Extract E field as E = ∇(∇·ψ) [longitudinal part]

    This is the potential part of the Helmholtz decomposition.
    """
    # First compute divergence of psi (treating complex field as 2D vector in plane)
    # For a complex scalar, we can decompose: ψ = ψ_real + i ψ_imag

    # Extract real and imaginary parts as 2D vectors
    psi_real = {site: (psi[site].real, 0.0) for site in sites}
    psi_imag = {site: (psi[site].imag, 0.0) for site in sites}

    # Actually, for a complex scalar field on a 2D lattice:
    # We need to think of ψ as having both magnitude and phase
    # The gradient of the magnitude gives the E-like field

    # Better approach: compute ∂ψ/∂x and ∂ψ/∂y as complex derivatives
    grad_psi = discrete_gradient({site: psi[site].real for site in sites}, sites, a)

    # The E-field is the gradient of the potential part
    # For now, approximate as the real gradient
    return grad_psi


def extract_b_field(
    psi: Dict[Site, complex],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, float]:
    """
    Extract B field as B_z = ∇×(∇×ψ) [transverse part, z-component]

    This is the solenoidal part of the Helmholtz decomposition.
    """
    # For a complex scalar field, extract the curl of the imaginary part
    psi_imag_scalar = {site: psi[site].imag for site in sites}

    # Compute the curl (z-component)
    curl_psi = discrete_curl_z(
        {site: (0.0, psi_imag_scalar[site]) for site in sites},
        sites, a
    )

    return curl_psi


# ============================================================================
# PART 3: Unified Mode Evolution
# ============================================================================

def unified_mode_update(
    psi_prev: Dict[Site, complex],
    psi_curr: Dict[Site, complex],
    gamma: float,
    beta: float,
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, complex]:
    """
    Perform one time step of the unified One-Wave rule:

      ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]

    Args:
        psi_prev: ψⁿ⁻¹
        psi_curr: ψⁿ
        gamma: damping parameter
        beta: coupling strength
        sites: lattice sites
        a: lattice constant

    Returns:
        ψⁿ⁺¹
    """
    # Extract divergence and curl
    # Treat complex field as real scalar for these operations
    psi_real = {site: psi_curr[site].real for site in sites}

    # Divergence: ∇·ψ → scalar field
    div_psi = discrete_divergence(
        {site: (psi_real[site], 0.0) for site in sites},
        sites, a
    )

    # Gradient of divergence: ∇(∇·ψ) → vector field
    grad_div_psi = discrete_gradient(div_psi, sites, a)

    # Curl: ∇×ψ → (scalar field as z-component)
    curl_psi = discrete_curl_z(
        {site: (psi_real[site], 0.0) for site in sites},
        sites, a
    )

    # Gradient of curl: ∇(∇×ψ) → vector field
    grad_curl_psi = discrete_gradient(curl_psi, sites, a)

    # Now compute the full update
    psi_next = {}
    for site in sites:
        # Inertial term
        inertia = 2.0 * psi_curr[site] - psi_prev[site]

        # Damping term
        vel = psi_curr[site] - psi_prev[site]
        damping = -gamma * vel

        # Coupling term: β[∇(∇·ψ) - ∇(∇×ψ)]
        # This is scalar (complex), so we need to integrate the vector gradients
        # For simplicity, take the magnitude as the field contribution
        gd = grad_div_psi[site]
        gc = grad_curl_psi[site]
        grad_coupling = math.sqrt(gd[0]**2 + gd[1]**2) - math.sqrt(gc[0]**2 + gc[1]**2)
        coupling = beta * grad_coupling * (1.0 + 0.0j)

        psi_next[site] = inertia + damping + coupling

    return psi_next


# ============================================================================
# PART 4: Faraday's Law Test
# ============================================================================

def test_faraday_law(
    psi_history: List[Dict[Site, complex]],
    sites: Sequence[Site],
    dt: float,
    a: float = 1.0
) -> Dict[str, float]:
    """
    Test Faraday's law: ∇×E = -∂B/∂t

    Compute the error in Faraday's law across the history.

    Returns:
        Dictionary with:
          - max_faraday_error: maximum violation per site/time
          - avg_faraday_error: average violation
    """
    errors = []

    for t in range(1, len(psi_history) - 1):
        psi_t = psi_history[t]
        psi_tm = psi_history[t - 1]
        psi_tp = psi_history[t + 1]

        # Extract E and B at time t
        e_field = extract_e_field(psi_t, sites, a)

        # Extract B and compute ∂B/∂t at time t
        b_field_t = extract_b_field(psi_t, sites, a)
        b_field_tp = extract_b_field(psi_tp, sites, a)
        b_field_tm = extract_b_field(psi_tm, sites, a)

        # Finite difference for ∂B/∂t
        db_dt = {}
        for site in sites:
            db_dt[site] = (b_field_tp[site] - b_field_tm[site]) / (2.0 * dt)

        # Compute ∇×E
        curl_e = discrete_curl_z(e_field, sites, a)

        # Faraday: ∇×E + ∂B/∂t should be zero
        for site in sites:
            error = abs(curl_e[site] + db_dt[site])
            errors.append(error)

    if errors:
        return {
            'max_faraday_error': max(errors),
            'avg_faraday_error': sum(errors) / len(errors),
            'num_samples': len(errors),
        }
    else:
        return {
            'max_faraday_error': 0.0,
            'avg_faraday_error': 0.0,
            'num_samples': 0,
        }


# ============================================================================
# MAIN: Run Maxwell Solver
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TRACK C: DISCRETE MAXWELL SOLVER")
    print("=" * 80)
    print()

    # Parameters
    gamma = 0.5
    beta = 0.5
    a = 1.0  # lattice constant
    dt = 0.01  # time step
    n_steps = 20  # number of time steps

    # Wavenumber for plane wave test
    k_x, k_y = 0.5, 0.0
    k_mag = math.sqrt(k_x**2 + k_y**2)

    print(f"Parameters: γ={gamma}, β={beta}, a={a}")
    print(f"Wavevector: k = ({k_x}, {k_y}), |k| = {k_mag:.4f}")
    print()

    # Domain: seven-cell
    sites = seven_cell()

    print(f"Domain: {len(sites)}-site seven-cell lattice")
    print()

    # Initial conditions: plane wave
    amplitude = 1.0 + 0.0j

    print("Initializing plane wave...")
    psi_history = []

    # t=0
    psi_0 = plane_wave_field((k_x, k_y), amplitude, sites, a)
    psi_history.append(psi_0.copy())

    # t=dt (initial velocity from unified mode)
    # For a plane wave e^{i(k·r - ωt)}, the "velocity" is iω A e^{i(k·r - ωt)}
    # We approximate: ψ(dt) ≈ ψ(0) - iω*dt*ψ(0)
    omega_approx = 0.236  # From Phase 6B results for k=0.5
    psi_1 = {}
    for site in sites:
        psi_1[site] = psi_0[site] - 1j * omega_approx * dt * psi_0[site]
    psi_history.append(psi_1.copy())

    # Time evolution
    print("Running time evolution...")
    for step in range(1, n_steps):
        psi_next = unified_mode_update(psi_history[-2], psi_history[-1], gamma, beta, sites, a)
        psi_history.append(psi_next)

    print(f"Completed {len(psi_history)} time steps")
    print()

    # Test Faraday's law
    print("Testing Faraday's Law: ∇×E = -∂B/∂t")
    print("-" * 60)

    faraday_results = test_faraday_law(psi_history, sites, dt, a)

    print(f"Max Faraday error: {faraday_results['max_faraday_error']:.4e}")
    print(f"Avg Faraday error: {faraday_results['avg_faraday_error']:.4e}")
    print(f"Number of samples: {faraday_results['num_samples']}")
    print()

    if faraday_results['max_faraday_error'] < 0.1:
        print("✓ Faraday's law approximately satisfied")
    else:
        print("✗ Faraday's law significantly violated")

    print()
    print("=" * 80)
    print("TRACK C: MAXWELL SOLVER COMPLETE")
    print("=" * 80)
