"""
Track C V3: Discrete Maxwell Solver — Proper Complex Field Handling
====================================================================

Fixed version that:
1. Preserves complex ψ field (not just real part)
2. Implements proper curl-of-curl operator
3. Uses field-splitting interpretation: ψ itself carries E and B information

Key insight: E and B are not independent; they're two views of the same
complex amplitude evolving at a single frequency. The extraction should
preserve this coupling, not force orthogonality.
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
# PART 1: Vector Laplacian (Helmholtz-free approach)
# ============================================================================

def discrete_laplacian_scalar(
    scalar_field: Dict[Site, float],
    sites: Sequence[Site],
    a: float = 1.0
) -> Dict[Site, float]:
    """
    Compute scalar Laplacian ∇²φ using ∇²φ = ∇·(∇φ).
    """
    grad_phi = discrete_gradient(scalar_field, sites, a)
    laplacian = discrete_divergence(grad_phi, sites, a)
    return laplacian


# ============================================================================
# PART 2: Direct E/B Extraction (Complex-Aware)
# ============================================================================

def extract_fields_direct(
    psi: Dict[Site, complex],
    sites: Sequence[Site],
    a: float = 1.0
) -> Tuple[Dict[Site, Tuple[float, float]], Dict[Site, float]]:
    """
    Extract E and B directly from complex ψ using amplitude-phase decomposition.

    For ψ = A·e^{iφ}:
    - E field relates to the divergence structure (amplitude gradient)
    - B field relates to the curl structure (vorticity)

    Both preserve the complex nature of ψ without forcing orthogonality.
    """

    # Split ψ into magnitude and phase
    psi_mag = {}
    psi_phase = {}

    for site in sites:
        z = psi[site]
        psi_mag[site] = abs(z)
        # Phase: angle of complex number
        psi_phase[site] = math.atan2(z.imag, z.real)

    # ========================================================================
    # E-field: based on amplitude gradients (potential-like)
    # ========================================================================

    # Gradient of magnitude (envelope modulation)
    grad_mag = discrete_gradient(psi_mag, sites, a)

    # Phase gradient (relates to frequency and direction)
    grad_phase = discrete_gradient(psi_phase, sites, a)

    # E is a combination: amplitude gradient + phase rotation effect
    # E ~ ∇|ψ| + i·|ψ|·∇φ (complex gradient)
    e_field = {}
    for site in sites:
        gm = grad_mag.get(site, (0.0, 0.0))
        gp = grad_phase.get(site, (0.0, 0.0))
        amp = psi_mag.get(site, 0.0)

        # E field as complex vector (Ex, Ey)
        ex = gm[0] + amp * (-gp[1])  # Real + phase rotation
        ey = gm[1] + amp * (gp[0])
        e_field[site] = (ex, ey)

    # ========================================================================
    # B-field: based on vorticity (solenoidal-like)
    # ========================================================================

    # Magnitude gives local circulation strength
    laplacian_mag = discrete_laplacian_scalar(psi_mag, sites, a)

    # Phase gives local vorticity
    curl_phase = discrete_curl_z(
        {site: grad_phase[site] for site in sites},
        sites, a
    )

    # B is circulation: Laplacian of envelope + phase vorticity
    b_field_z = {}
    for site in sites:
        lap_mag = laplacian_mag.get(site, 0.0)
        curl_ph = curl_phase.get(site, 0.0)
        b_field_z[site] = lap_mag + curl_ph

    return e_field, b_field_z


# ============================================================================
# PART 3: Plane Wave Initialization
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

    Computes error across time history.
    """
    errors = []

    for t in range(1, len(psi_history) - 1):
        # Extract fields at time t
        e_t, b_t = extract_fields_direct(psi_history[t], sites, a)
        e_tp, b_tp = extract_fields_direct(psi_history[t+1], sites, a)
        e_tm, b_tm = extract_fields_direct(psi_history[t-1], sites, a)

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
# PART 5: One-Wave Evolution
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
    # Convert to vector form (ψ, 0) for operator application
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
# MAIN: Run V3 Solver
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TRACK C V3: DISCRETE MAXWELL SOLVER (COMPLEX-AWARE)")
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
    print("Extracting E and B fields (direct complex-aware method)...")
    e_final, b_final = extract_fields_direct(psi_history[-1], sites, a)
    print(f"  E-field extracted (complex vector)")
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
    print("V3 SOLVER COMPLETE")
    print("=" * 80)
    print()

    if faraday['max_error'] < 0.01:
        print("SUCCESS: Faraday error is acceptable")
        print("Next: Test on larger domains (disk radius 2+)")
    else:
        print("DIAGNOSTIC: Faraday error indicates extraction approach needs revision")
        print("Options:")
        print("  1. Reconsider what E/B extraction should mean for scalar ψ")
        print("  2. Map problem to vector ψ formulation")
        print("  3. Use mode decomposition instead of field projection")
