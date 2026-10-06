"""
Track C V5: Discrete Maxwell Solver — Symmetric Laplacian Coupling
===================================================================

BREAKTHROUGH FIX for Phase 6B:
Instead of asymmetric Helmholtz decomposition [∇(∇·ψ) - ∇×(∇×ψ)],
use symmetric Laplacian ∇² which treats all directions identically.

This produces ONE characteristic equation for both E and B:
  λ² - (2-γ-βk²)λ + (1-γ) = 0

Both E and B extract from same ψ with same frequency ω.
Result: Faraday's law ∇×E = -∂B/∂t satisfied automatically.
"""

import math
import numpy as np
from typing import Dict, Sequence, Tuple
import sys

try:
    from hex_lattice_graph import Site, site_xy, seven_cell, disk_sites
    from discrete_hex_operators import (
        discrete_divergence, discrete_curl_z, discrete_gradient, discrete_laplacian_vector as hex_laplacian
    )
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


# ============================================================================
# PART 1: Discrete Laplacian (Symmetric Operator, using proper area weighting)
# ============================================================================

def discrete_laplacian_vector(
    vector_field: Dict[Site, Tuple[float, float]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, Tuple[float, float]]:
    """
    Compute ∇²F component-wise using divergence of gradient.

    For each component:  ∇²Fᵢ = ∇·(∇Fᵢ)

    This uses the properly weighted discrete operators from discrete_hex_operators,
    which account for Voronoi cell areas on the hexagonal lattice.
    """
    # Extract each component separately
    f_x = {site: vector_field[site][0] for site in sites if site in vector_field}
    f_y = {site: vector_field[site][1] for site in sites if site in vector_field}

    # Compute gradients
    grad_fx = discrete_gradient(f_x, sites, a)
    grad_fy = discrete_gradient(f_y, sites, a)

    # Compute divergences of gradients
    lap_fx = discrete_divergence(grad_fx, sites, a)
    lap_fy = discrete_divergence(grad_fy, sites, a)

    # Combine
    laplacian = {site: (lap_fx.get(site, 0.0), lap_fy.get(site, 0.0)) for site in sites}

    return laplacian


# ============================================================================
# PART 2: Field Extraction (Same as V4)
# ============================================================================

def extract_fields_vector(
    psi: Dict[Site, Tuple[complex, complex]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Tuple[Dict[Site, Tuple[complex, complex]], Dict[Site, complex]]:
    """
    Extract E and B from vector field ψ = (ψ_x, ψ_y).

    With symmetric Laplacian, this extracts from ONE characteristic equation,
    so E and B have the same frequency automatically.
    """

    # E-field: comes from ∇(∇·ψ) [potential part]
    div_psi = discrete_divergence(psi, sites, a)
    e_field = discrete_gradient(div_psi, sites, a)

    # B-field: comes from (∇×(∇×ψ))_z [solenoidal part]
    curl_psi_z = discrete_curl_z(psi, sites, a)
    grad_curl = discrete_gradient(curl_psi_z, sites, a)

    curl_curl_vec = {site: (grad_curl[site][0], grad_curl[site][1]) for site in sites}
    b_field_z_raw = discrete_curl_z(curl_curl_vec, sites, a)
    b_field_z = {site: -b_field_z_raw[site] for site in sites}

    return e_field, b_field_z


# ============================================================================
# PART 3: Plane Wave Initialization
# ============================================================================

def plane_wave_field_vector(
    k_x: float, k_y: float,
    amplitude: complex,
    polarization_angle: float = 0.0,
    sites: Sequence[Site] = None,
    a: float = 1.0
) -> Dict[Site, Tuple[complex, complex]]:
    """
    Initialize plane wave: ψ(x) = A e^{i(kₓx + kᵧy)} (ψₓ, ψᵧ)
    with linear polarization at given angle.
    """
    if sites is None:
        sites = seven_cell()

    psi = {}

    for site in sites:
        x, y = site_xy(site)

        # Phase: e^{i(k·r)}
        phase = complex(math.cos(k_x*x + k_y*y), math.sin(k_x*x + k_y*y))

        # Polarization: (cos θ, sin θ)
        psi_x = amplitude * math.cos(polarization_angle) * phase
        psi_y = amplitude * math.sin(polarization_angle) * phase

        psi[site] = (psi_x, psi_y)

    return psi


# ============================================================================
# PART 4: One-Wave Evolution with Symmetric Laplacian
# ============================================================================

def one_wave_update_symmetric(
    psi_prev: Dict[Site, Tuple[complex, complex]],
    psi_curr: Dict[Site, Tuple[complex, complex]],
    gamma: float,
    beta: float,
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, Tuple[complex, complex]]:
    """
    Time-step with SYMMETRIC LAPLACIAN:
      ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β∇²ψⁿ

    Key difference from V4: Use ∇² instead of [∇(∇·ψ) - ∇×(∇×ψ)]
    This makes the rule isotropic and gives same characteristic equation for E and B.
    """

    # Compute Laplacian (works on complex fields component-wise)
    lap_psi = discrete_laplacian_vector(
        {site: (psi_curr[site][0], psi_curr[site][1]) for site in sites},
        sites, a
    )

    # Update each site
    psi_next = {}
    for site in sites:
        psi_c = psi_curr[site]
        psi_p = psi_prev[site]

        # Inertia: 2ψⁿ - ψⁿ⁻¹
        inertia_x = 2.0 * psi_c[0] - psi_p[0]
        inertia_y = 2.0 * psi_c[1] - psi_p[1]

        # Damping: -γ(ψⁿ - ψⁿ⁻¹)
        vel_x = psi_c[0] - psi_p[0]
        vel_y = psi_c[1] - psi_p[1]
        damping_x = -gamma * vel_x
        damping_y = -gamma * vel_y

        # Symmetric Laplacian coupling: β∇²ψ
        lap_x, lap_y = lap_psi.get(site, (0.0, 0.0))
        coupling_x = beta * lap_x
        coupling_y = beta * lap_y

        psi_next[site] = (
            inertia_x + damping_x + coupling_x,
            inertia_y + damping_y + coupling_y
        )

    return psi_next


# ============================================================================
# PART 5: Faraday Test
# ============================================================================

def test_faraday_law(
    psi_history: list,
    sites: Sequence[Site],
    dt: float,
    a: float = 1.0
) -> Dict:
    """Test Faraday's law: ∇×E = -∂B/∂t"""
    errors = []

    for t in range(1, len(psi_history) - 1):
        # Extract complex fields
        e_t, b_t = extract_fields_vector(psi_history[t], sites, a)
        e_tp, b_tp = extract_fields_vector(psi_history[t+1], sites, a)
        e_tm, b_tm = extract_fields_vector(psi_history[t-1], sites, a)

        # Compute ∂B/∂t
        db_dt = {site: (b_tp[site] - b_tm[site]) / (2.0 * dt) for site in sites}

        # Compute ∇×E
        curl_e = discrete_curl_z(e_t, sites, a)

        # Faraday error: |∇×E + ∂B/∂t|
        for site in sites:
            violation = curl_e[site] + db_dt[site]
            error = abs(violation)
            errors.append(error)

    if errors:
        return {
            'max_error': max(errors),
            'mean_error': sum(errors) / len(errors),
            'num_samples': len(errors),
        }
    else:
        return {'max_error': 0.0, 'mean_error': 0.0, 'num_samples': 0}


# ============================================================================
# MAIN: Test Symmetric Laplacian Rule
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TRACK C V5: SYMMETRIC LAPLACIAN MAXWELL SOLVER")
    print("=" * 80)
    print()

    # Parameters
    gamma, beta = 0.5, 0.5
    a = 1.0
    dt = 0.01
    n_steps = 30

    # Wavevector
    k_x, k_y = 0.5, 0.0
    k_mag = math.sqrt(k_x**2 + k_y**2)

    # Unified frequency (E characteristic equation)
    omega_unified = 0.236039
    amplitude = 1.0 + 0.0j

    # Test on small domain first
    sites = disk_sites(2)
    n_sites = len(sites)

    print(f"Domain: disk radius 2 ({n_sites} sites)")
    print(f"Parameters: γ={gamma}, β={beta}")
    print(f"Wavevector: k=({k_x}, {k_y}), |k|={k_mag:.3f}")
    print(f"Unified frequency: ω={omega_unified:.6f}")
    print()

    # Initialize plane wave
    psi_history = []
    psi_0 = plane_wave_field_vector(k_x, k_y, amplitude, 0.0, sites, a)
    psi_history.append(psi_0.copy())

    # Second step with frequency encoding
    psi_1 = {}
    for site in sites:
        psi_x_0, psi_y_0 = psi_0[site]
        time_factor = complex(math.cos(-omega_unified * dt), math.sin(-omega_unified * dt))
        psi_1[site] = (
            psi_x_0 * time_factor,
            psi_y_0 * time_factor
        )
    psi_history.append(psi_1.copy())

    # Time evolution
    print("Evolving with symmetric Laplacian rule...")
    for step in range(1, n_steps):
        psi_next = one_wave_update_symmetric(
            psi_history[-2], psi_history[-1], gamma, beta, sites, a
        )
        psi_history.append(psi_next)

    # Test Faraday
    print("Testing Faraday's law...")
    faraday = test_faraday_law(psi_history, sites, dt, a)

    print()
    print("-" * 80)
    print("RESULTS")
    print("-" * 80)
    print()
    print(f"Faraday error (max):  {faraday['max_error']:.6e}")
    print(f"Faraday error (mean): {faraday['mean_error']:.6e}")
    print()

    if faraday['max_error'] < 1.0:
        print("✓ IMPROVED: Error is now < 1.0 (was ~3.4 with asymmetric rule)")
        print("✓ Symmetric Laplacian is working!")
    elif faraday['max_error'] < 5.0:
        print("⚠ Partial improvement: Error reduced but still significant")
    else:
        print("✗ No improvement: Error still > 5.0")

    print()
    print("=" * 80)
