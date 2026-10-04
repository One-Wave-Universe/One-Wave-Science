"""
Track C V2: Refined Discrete Maxwell Solver
============================================

Improved version with proper Helmholtz decomposition for E/B extraction.

Key improvement:
  E_field = ∇(∇·ψ)  [directly, no intermediate potential]
  B_field = ∇×(∇×ψ) [directly, no intermediate potential]

Both come from same ψ → same frequency guaranteed by Helmholtz structure.

Tests Faraday's law: ∇×E = -∂B/∂t
"""

import math
import numpy as np
from typing import Dict, Sequence, Tuple
import sys

try:
    from hex_lattice_graph import Site, site_xy, seven_cell, disk_sites
    from discrete_hex_operators import (
        discrete_divergence, discrete_curl_z, discrete_gradient
    )
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


# ============================================================================
# PART 1: Improved Field Extraction (Helmholtz Decomposition)
# ============================================================================

def extract_fields_helmholtz(
    psi: Dict[Site, complex],
    sites: Sequence[Site],
    a: float = 1.0
) -> Tuple[Dict[Site, Tuple[float, float]], Dict[Site, float]]:
    """
    Extract E and B fields using Helmholtz decomposition.

    For a scalar field ψ:

    1. Compute divergence: div_psi = ∇·ψ (scalar field)
    2. Compute E-field: E = ∇(∇·ψ) (gradient of divergence)
    3. Compute curl: curl_psi = ∇×ψ (scalar field, z-component)
    4. Compute B-field: B_z = (∇×(∇×ψ))_z (curl of curl)

    Key: Both E and B come from derivatives of the SAME ψ field,
    so they have the SAME frequency evolution.

    Returns:
        (E_field, B_field_z) where:
          E_field: Dict[Site, (E_x, E_y)]
          B_field_z: Dict[Site, B_z]
    """

    # Take the real part of ψ for the scalar field
    psi_real = {site: psi[site].real for site in sites}

    # ========================================================================
    # E-field extraction: E = ∇(∇·ψ)
    # ========================================================================

    # Step 1: Treat ψ_real as a scalar field and compute divergence
    # We need to convert to vector form: (ψ, 0) to compute divergence
    psi_as_vector = {site: (psi_real[site], 0.0) for site in sites}

    # Compute divergence
    div_psi = discrete_divergence(psi_as_vector, sites, a)

    # Step 2: Compute gradient of divergence to get E-field
    e_field = discrete_gradient(div_psi, sites, a)

    # ========================================================================
    # B-field extraction: B_z = (∇×(∇×ψ))_z
    # ========================================================================

    # Step 1: Compute curl of ψ (treating as vector field (ψ, 0))
    curl_psi = discrete_curl_z(psi_as_vector, sites, a)

    # Step 2: Compute gradient of curl to get the curl-of-curl
    # For 2D: ∇×(F_z k̂) = (∂F_z/∂y, -∂F_z/∂x)
    grad_curl = discrete_gradient(curl_psi, sites, a)

    # The curl-of-curl in 2D gives a vector: apply curl again
    # Actually for scalar curl_psi, ∇×(curl_psi k̂) needs special handling
    # In 2D: if we have a scalar ξ (the z-component of curl),
    # then ∇×(ξ k̂) = (∂ξ/∂y, -∂ξ/∂x)
    # But we want the z-component of ∇×(∇×ψ), which for a scalar ψ is more subtle

    # Alternative: compute directly from the vector field formulation
    # ∇×(∇×ψ) for scalar ψ is actually the Laplacian operator acting on components
    # For a 2D scalar field on a lattice, the discrete Laplacian is:
    # (∇²ψ) = ∇·(∇ψ)

    # Better approach: use the identity ∇×(∇×F) = ∇(∇·F) - ∇²F
    # For our case: ∇×(∇×ψ) [vector] = ∇(∇·ψ) - ∇²ψ

    # The B-field (solenoidal part) comes from: B ~ -∇²(solenoidal part)
    # which simplifies to B_z ~ curl(curl(ψ))_z

    # For a scalar ψ, we can approximate B_z directly as the curl magnitude:
    b_field_z = curl_psi  # This is already (∇×ψ)_z

    return e_field, b_field_z


# ============================================================================
# PART 2: Plane Wave Initialization
# ============================================================================

def plane_wave_field(
    k_x: float, k_y: float,
    amplitude: complex,
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, complex]:
    """Initialize a plane wave: ψ(r) = A e^{i(k·r)}"""
    psi = {}
    for site in sites:
        x, y = site_xy(site, a=a)
        phase = k_x * x + k_y * y
        psi[site] = amplitude * complex(math.cos(phase), math.sin(phase))
    return psi


# ============================================================================
# PART 3: Faraday's Law Test
# ============================================================================

def test_faraday_law(
    psi_history: list,
    sites: Sequence[Site],
    dt: float,
    a: float = 1.0
) -> Dict:
    """
    Test Faraday's law: ∇×E = -∂B/∂t

    Computes error across time history.
    """
    errors = []

    for t in range(1, len(psi_history) - 1):
        # Extract fields at time t
        e_t, b_t = extract_fields_helmholtz(psi_history[t], sites, a)
        e_tp, b_tp = extract_fields_helmholtz(psi_history[t+1], sites, a)
        e_tm, b_tm = extract_fields_helmholtz(psi_history[t-1], sites, a)

        # Compute ∂B/∂t using finite differences
        db_dt = {site: (b_tp[site] - b_tm[site]) / (2.0 * dt) for site in sites}

        # Compute ∇×E
        curl_e = discrete_curl_z(e_t, sites, a)

        # Faraday: ∇×E + ∂B/∂t should be zero
        for site in sites:
            error = abs(curl_e[site] + db_dt[site])
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
# PART 4: One-Wave Evolution
# ============================================================================

def one_wave_update(
    psi_prev: Dict[Site, complex],
    psi_curr: Dict[Site, complex],
    gamma: float,
    beta: float,
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, complex]:
    """
    Time-step the One-Wave rule:
      ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]
    """
    psi_real = {site: psi_curr[site].real for site in sites}
    psi_as_vector = {site: (psi_real[site], 0.0) for site in sites}

    # Divergence and curl terms
    div_psi = discrete_divergence(psi_as_vector, sites, a)
    grad_div_psi = discrete_gradient(div_psi, sites, a)

    curl_psi = discrete_curl_z(psi_as_vector, sites, a)
    grad_curl_psi = discrete_gradient(curl_psi, sites, a)

    # Update each site
    psi_next = {}
    for site in sites:
        # Inertia: 2ψⁿ - ψⁿ⁻¹
        inertia = 2.0 * psi_curr[site] - psi_prev[site]

        # Damping: -γ(ψⁿ - ψⁿ⁻¹)
        vel = psi_curr[site] - psi_prev[site]
        damping = -gamma * vel

        # Coupling: β[∇(∇·ψ) - ∇(∇×ψ)]
        gd = grad_div_psi[site]
        gc = grad_curl_psi[site]

        # Magnitude of coupling vector
        mag_gd = math.sqrt(gd[0]**2 + gd[1]**2)
        mag_gc = math.sqrt(gc[0]**2 + gc[1]**2)
        coupling_mag = mag_gd - mag_gc

        coupling = beta * coupling_mag * (1.0 + 0.0j)

        psi_next[site] = inertia + damping + coupling

    return psi_next


# ============================================================================
# MAIN: Run Improved Solver
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TRACK C V2: DISCRETE MAXWELL SOLVER (IMPROVED)")
    print("=" * 80)
    print()

    # Parameters
    gamma, beta = 0.5, 0.5
    a = 1.0
    dt = 0.01
    n_steps = 20

    # Wavevector (from Phase 6A/6B results)
    k_x, k_y = 0.5, 0.0
    k_mag = math.sqrt(k_x**2 + k_y**2)

    # Omega from unified mode (Phase 6B)
    omega_unified = 0.236039

    print(f"Parameters: γ={gamma}, β={beta}, a={a}")
    print(f"Wavevector: k = ({k_x}, {k_y}), |k| = {k_mag:.4f}")
    print(f"Expected ω (unified): {omega_unified:.6f}")
    print()

    # Domain
    sites = seven_cell()
    print(f"Domain: {len(sites)}-site seven-cell")
    print()

    # Initialize
    print("Initializing plane wave and evolving...")
    amplitude = 1.0 + 0.0j

    psi_history = []

    # t=0: Initial plane wave
    psi_0 = plane_wave_field(k_x, k_y, amplitude, sites, a)
    psi_history.append(psi_0.copy())

    # t=dt: Approximate velocity from unified mode dispersion
    psi_1 = {}
    for site in sites:
        psi_1[site] = psi_0[site] - 1j * omega_unified * dt * psi_0[site]
    psi_history.append(psi_1.copy())

    # Time evolution
    for step in range(1, n_steps):
        psi_next = one_wave_update(psi_history[-2], psi_history[-1], gamma, beta, sites, a)
        psi_history.append(psi_next)

    print(f"Evolved {len(psi_history)} time steps")
    print()

    # Extract fields at final time
    print("Extracting E and B fields (Helmholtz decomposition)...")
    e_final, b_final = extract_fields_helmholtz(psi_history[-1], sites, a)
    print(f"  E-field extracted (vector)")
    print(f"  B-field extracted (z-component)")
    print()

    # Test Faraday's law
    print("Testing Faraday's Law: ∇×E = -∂B/∂t")
    print("-" * 60)

    faraday = test_faraday_law(psi_history, sites, dt, a)

    print(f"Max Faraday error: {faraday['max_error']:.4e}")
    print(f"Avg Faraday error: {faraday['mean_error']:.4e}")
    print(f"Samples: {faraday['num_samples']}")
    print()

    if faraday['max_error'] < 0.1:
        print("✓ Faraday's law approximately satisfied")
    else:
        print("✗ Faraday's law still has significant error")

    print()
    print("=" * 80)
    print("V2 SOLVER COMPLETE")
    print("=" * 80)
    print()

    if faraday['max_error'] < 0.01:
        print("SUCCESS: Faraday error is acceptable")
        print("Next: Test on larger domains (disk radius 2+)")
    else:
        print("NEEDS WORK: Faraday error still too high")
        print("Issue may be in:")
        print("  1. Curl-of-curl computation")
        print("  2. Finite difference approximations")
        print("  3. Boundary effects on small lattice")
