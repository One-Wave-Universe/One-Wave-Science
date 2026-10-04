"""
Track C V4: Discrete Maxwell Solver — Vector Field Formulation
===============================================================

CORRECTED INTERPRETATION:
ψ is a 2D vector field, not a scalar.
The One-Wave rule evolves ψ = (ψ_x, ψ_y) at each lattice site.

Then:
- E-field: Extract from potential part ∇(∇·ψ)
- B-field: Extract from solenoidal part (∇×(∇×ψ))_z

Both come from the same ψ evolving at the same ω, guaranteeing
frequency matching and Faraday compatibility by structure.
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
# PART 1: Vector Laplacian
# ============================================================================

def discrete_laplacian_vector(
    vector_field: Dict[Site, Tuple[float, float]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, Tuple[float, float]]:
    """
    Compute vector Laplacian: ∇²F = ∇(∇·F) - ∇×(∇×F)
    """
    # Divergence of vector field
    div_f = discrete_divergence(vector_field, sites, a)

    # Curl of vector field (returns scalar z-component)
    curl_z_f = discrete_curl_z(vector_field, sites, a)

    # Gradient of divergence (potential part)
    grad_div = discrete_gradient(div_f, sites, a)

    # Gradient of curl: ∇×(∇×F) in 2D requires constructing the curl vector
    # For scalar curl_z, the vector ∇×(curl_z k̂) = (∂curl_z/∂y, -∂curl_z/∂x)
    grad_curl = discrete_gradient(curl_z_f, sites, a)

    # Solenoidal part: -∇×(curl_z k̂) = (-∂curl_z/∂y, ∂curl_z/∂x)
    laplacian = {}
    for site in sites:
        gd = grad_div.get(site, (0.0, 0.0))
        gc = grad_curl.get(site, (0.0, 0.0))

        # ∇² = ∇(∇·) - ∇×(∇×)
        # Solenoidal part negated: (-gc[1], gc[0])
        laplacian[site] = (
            gd[0] - (-gc[1]),  # = gd[0] + gc[1]
            gd[1] - (gc[0])    # = gd[1] - gc[0]
        )

    return laplacian


# ============================================================================
# PART 2: Field Extraction from Vector ψ
# ============================================================================

def extract_fields_vector(
    psi: Dict[Site, Tuple[complex, complex]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Tuple[Dict[Site, Tuple[float, float]], Dict[Site, float]]:
    """
    Extract E and B from vector field ψ = (ψ_x, ψ_y).

    Both are extracted from the same ψ field, guaranteeing
    frequency matching by Helmholtz structure.

    Returns:
        (E_field, B_field_z) where:
          E_field: Dict[Site, (E_x, E_y)] — real 2D vector
          B_field_z: Dict[Site, B_z] — real scalar
    """

    # Convert complex ψ to real (take real parts of both components)
    psi_real = {}
    for site in sites:
        psi_x, psi_y = psi[site]
        psi_real[site] = (psi_x.real, psi_y.real)

    # ====================================================================
    # E-field: comes from ∇(∇·ψ) [potential part]
    # ====================================================================

    div_psi = discrete_divergence(psi_real, sites, a)
    e_field = discrete_gradient(div_psi, sites, a)

    # ====================================================================
    # B-field: comes from (∇×(∇×ψ))_z [solenoidal part]
    # ====================================================================

    curl_psi_z = discrete_curl_z(psi_real, sites, a)
    grad_curl = discrete_gradient(curl_psi_z, sites, a)

    # ∇×(∇×ψ) in 2D: the z-component is ∂(curl_z)/∂x ∂(curl_z)/∂y mixed term
    # Actually simpler: just take the scalar curl of the curl
    # (∇×(F_z k̂))_z = (∂F_z/∂x, ∂F_z/∂y) → curl of this vector
    curl_curl_vec = {site: (grad_curl[site][0], grad_curl[site][1]) for site in sites}
    b_field_z_raw = discrete_curl_z(curl_curl_vec, sites, a)

    # Negate for proper ∇×(∇×) identity
    b_field_z = {site: -b_field_z_raw[site] for site in sites}

    return e_field, b_field_z


# ============================================================================
# PART 3: Plane Wave Initialization (Vector)
# ============================================================================

def plane_wave_field_vector(
    k_x: float, k_y: float,
    amplitude: complex,
    polarization_angle: float = 0.0,
    sites: Sequence[Site] = None,
    a: float = 1.0
) -> Dict[Site, Tuple[complex, complex]]:
    """
    Initialize a vector plane wave.
    ψ(r) = A · [cos(θ), sin(θ)] · e^{i(k·r)}

    polarization_angle determines the direction of the vector at each point.
    """
    if sites is None:
        sites = []

    psi = {}
    for site in sites:
        x, y = site_xy(site, a=a)
        phase = k_x * x + k_y * y
        exp_phase = complex(math.cos(phase), math.sin(phase))

        # Vector components with polarization
        psi_x = amplitude * math.cos(polarization_angle) * exp_phase
        psi_y = amplitude * math.sin(polarization_angle) * exp_phase

        psi[site] = (psi_x, psi_y)

    return psi


# ============================================================================
# PART 4: Faraday's Law Test
# ============================================================================

def test_faraday_law(
    psi_history: list,
    sites: Sequence[Site],
    dt: float,
    a: float = 1.0
) -> Dict:
    """
    Test Faraday's law: ∇×E = -∂B/∂t
    """
    errors = []

    for t in range(1, len(psi_history) - 1):
        # Extract fields at time t
        e_t, b_t = extract_fields_vector(psi_history[t], sites, a)
        e_tp, b_tp = extract_fields_vector(psi_history[t+1], sites, a)
        e_tm, b_tm = extract_fields_vector(psi_history[t-1], sites, a)

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
# PART 5: One-Wave Evolution (Vector)
# ============================================================================

def one_wave_update_vector(
    psi_prev: Dict[Site, Tuple[complex, complex]],
    psi_curr: Dict[Site, Tuple[complex, complex]],
    gamma: float,
    beta: float,
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, Tuple[complex, complex]]:
    """
    Time-step the One-Wave rule for vector ψ = (ψ_x, ψ_y):
      ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]
    """
    # Convert to real for operator application
    psi_real = {}
    for site in sites:
        psi_x, psi_y = psi_curr[site]
        psi_real[site] = (psi_x.real, psi_y.real)

    psi_prev_real = {}
    for site in sites:
        psi_x, psi_y = psi_prev[site]
        psi_prev_real[site] = (psi_x.real, psi_y.real)

    # Divergence and curl terms
    div_psi = discrete_divergence(psi_real, sites, a)
    grad_div_psi = discrete_gradient(div_psi, sites, a)

    curl_psi = discrete_curl_z(psi_real, sites, a)
    grad_curl_psi = discrete_gradient(curl_psi, sites, a)

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

        # Coupling: β[∇(∇·ψ) - ∇(∇×ψ)]
        gd = grad_div_psi[site]
        gc = grad_curl_psi[site]

        coupling_x = beta * (gd[0] - gc[0])
        coupling_y = beta * (gd[1] - gc[1])

        psi_next[site] = (
            inertia_x + damping_x + coupling_x,
            inertia_y + damping_y + coupling_y
        )

    return psi_next


# ============================================================================
# MAIN: Run V4 Solver
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TRACK C V4: DISCRETE MAXWELL SOLVER (VECTOR FIELD)")
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
    print("Initializing vector plane wave and evolving...")
    amplitude = 1.0 + 0.0j

    psi_history = []

    # t=0: Initial vector plane wave
    # Polarization: along x-direction
    psi_0 = plane_wave_field_vector(k_x, k_y, amplitude, 0.0, sites, a)
    psi_history.append(psi_0.copy())

    # t=dt: Approximate velocity from unified mode dispersion
    psi_1 = {}
    for site in sites:
        psi_x_0, psi_y_0 = psi_0[site]
        psi_1[site] = (
            psi_x_0 - 1j * omega_unified * dt * psi_x_0,
            psi_y_0 - 1j * omega_unified * dt * psi_y_0
        )
    psi_history.append(psi_1.copy())

    # Time evolution
    for step in range(1, n_steps):
        psi_next = one_wave_update_vector(psi_history[-2], psi_history[-1], gamma, beta, sites, a)
        psi_history.append(psi_next)

    print(f"Evolved {len(psi_history)} time steps")
    print()

    # Extract fields at final time
    print("Extracting E and B fields from vector ψ...")
    e_final, b_final = extract_fields_vector(psi_history[-1], sites, a)
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
    print("V4 SOLVER COMPLETE")
    print("=" * 80)
    print()

    if faraday['max_error'] < 0.01:
        print("SUCCESS: Faraday error is acceptable")
        print("Vector formulation validated. Next: Test on larger domains")
    else:
        print("DIAGNOSTIC: Vector formulation did not resolve Faraday error")
        print("May need: boundary handling, larger domain, or alternative approach")
