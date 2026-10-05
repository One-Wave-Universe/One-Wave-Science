"""
Phase 6C: Maxwell Solver with Proper Helmholtz Decomposition
=============================================================

Refinement to Phase 6B V5: Replace simple operator extraction with proper
Poisson-based potential solving.

Key improvement:
  Phase 6B: E = ∇(∇·ψ), B = -∇×(∇×ψ)  ← creates artifacts
  Phase 6C: E = ∇φ where ∇²φ = ∇·ψ, B = ∇×A where ∇²A = ∇×ψ  ← exact

Expected result: Faraday error should reduce from ~2.36 to near-zero,
validating that the evolution rule is physically correct and remaining error
was purely from field extraction method.
"""

import math
import cmath
from typing import Dict, List, Tuple, Sequence
import sys

# Import operators
try:
    from hex_lattice_graph import (
        Site, NEIGHBOR_OFFSETS, AXIS_PAIRS, neighbor, adjacency, site_xy
    )
except ImportError:
    Site = Tuple[int, int]
    NEIGHBOR_OFFSETS = (
        (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1),
    )
    AXIS_PAIRS = (
        ((1, 0), (-1, 0)),
        ((0, 1), (0, -1)),
        ((-1, 1), (1, -1)),
    )

    def neighbor(site: Site, offset: Site) -> Site:
        return (site[0] + offset[0], site[1] + offset[1])

    def adjacency(sites: Sequence[Site]) -> Dict[Site, List[Site]]:
        present = set(sites)
        adj: Dict[Site, List[Site]] = {}
        for site in sites:
            nbrs = [neighbor(site, off) for off in NEIGHBOR_OFFSETS
                   if neighbor(site, off) in present]
            adj[site] = nbrs
        return adj

    def site_xy(site: Site, a: float = 1.0) -> Tuple[float, float]:
        A1 = (1.0, 0.0)
        A2 = (0.5, math.sqrt(3.0) / 2.0)
        m, n = site
        return (a * (m * A1[0] + n * A2[0]), a * (m * A1[1] + n * A2[1]))

# Import discrete operators
from discrete_hex_operators import (
    discrete_divergence, discrete_curl_z, discrete_gradient,
    neighbor_outward_normals
)

# Import Poisson solver
from discrete_poisson_solver import poisson_solve_fourier


# ============================================================================
# PART 1: Helmholtz Decomposition via Poisson Solving
# ============================================================================

def helmholtz_decomposition_proper(
    scalar_field: Dict[Site, float],
    sites: Sequence[Site],
    a: float = 1.0
) -> Tuple[Dict[Site, Tuple[float, float]], Dict[Site, Tuple[float, float]]]:
    """
    Extract E and B fields from scalar field ψ using proper Helmholtz decomposition.

    For scalar field ψ:
      E = ∇φ  where  ∇²φ = ∇·ψ (divergence of scalar → scalar source)
      B = ∇×A where  ∇²A = ∇×ψ (curl of scalar gives scalar)

    This is the correct extraction that eliminates discrete operator artifacts.
    """
    # Compute divergence of scalar field (treat as vector (ψ, 0))
    div_psi = discrete_divergence({site: (scalar_field[site], 0.0) for site in sites},
                                   sites, a)

    # Solve for scalar potential φ: ∇²φ = ∇·ψ
    phi = poisson_solve_fourier(div_psi, sites, a, zero_mode_value=0.0)

    # Extract E field: E = ∇φ
    E_field = discrete_gradient(phi, sites, a)

    # Compute curl of scalar field (treat scalar ψ as vector (ψ, 0))
    curl_psi = discrete_curl_z({site: (scalar_field[site], 0.0) for site in sites},
                                sites, a)

    # Solve for vector potential A_z: ∇²A = ∇×ψ
    A_z = poisson_solve_fourier(curl_psi, sites, a, zero_mode_value=0.0)

    # Extract B field: B = ∇×(A_z k̂) = (∂A/∂y, -∂A/∂x)
    grad_A = discrete_gradient(A_z, sites, a)
    B_field = {}
    for site in sites:
        dA_dy, dA_dx = grad_A.get(site, (0.0, 0.0))
        B_field[site] = (dA_dy, -dA_dx)  # Rotate gradient 90° clockwise

    return E_field, B_field


# ============================================================================
# PART 2: Phase 6C Maxwell Evolution with Proper Extraction
# ============================================================================

def maxwell_evolution_v6(
    psi_0: Dict[Site, complex],
    psi_1: Dict[Site, complex],
    sites: Sequence[Site],
    a: float = 1.0,
    dt: float = 0.1,
    gamma: float = 0.5,
    beta: float = 0.5,
    num_steps: int = 10
) -> Tuple[List[Dict[Site, complex]], List[Dict[Site, Tuple[float, float]]],
           List[Dict[Site, Tuple[float, float]]]]:
    """
    Evolve Maxwell field using symmetric Laplacian rule + proper Helmholtz extraction.

    Update rule (Phase 6B):
      ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β∇²ψⁿ

    Field extraction (Phase 6C - improved):
      1. Decompose ψ-field into potential and solenoidal using Poisson solving
      2. E = ∇φ where ∇²φ = ∇·ψ
      3. B = ∇×A where ∇²A = ∇×ψ

    Args:
      psi_0, psi_1: initial fields at t=0 and t=dt
      sites: lattice sites
      a: lattice constant
      dt: time step
      gamma, beta: evolution parameters
      num_steps: number of evolution steps

    Returns:
      (psi_history, E_history, B_history): field evolution
    """
    from discrete_hex_operators import discrete_laplacian_vector

    psi_history = [psi_0, psi_1]
    E_history = []
    B_history = []

    # Extract initial fields
    psi_1_real = {site: psi_1[site].real for site in sites}

    # Compute initial E, B fields using proper Helmholtz decomposition
    E_0, B_0 = helmholtz_decomposition_proper(psi_1_real, sites, a)

    E_history.append(E_0)
    B_history.append(B_0)

    # Evolution loop
    psi_prev = psi_0
    psi_curr = psi_1

    for step in range(num_steps):
        # Convert complex field to real and imaginary parts
        psi_curr_real = {site: psi_curr[site].real for site in sites}
        psi_curr_imag = {site: psi_curr[site].imag for site in sites}

        # Compute Laplacian for real and imaginary parts
        # Treat scalar field as vector (ψ, 0) for Laplacian computation
        psi_curr_vec = {site: (psi_curr_real[site], 0.0) for site in sites}
        laplacian_vec = discrete_laplacian_vector(psi_curr_vec, sites, a)

        # Extract the scalar Laplacian from the x-component
        laplacian_real = {site: laplacian_vec[site][0] for site in sites}

        # Do the same for imaginary part
        psi_curr_imag_vec = {site: (psi_curr_imag[site], 0.0) for site in sites}
        laplacian_imag_vec = discrete_laplacian_vector(psi_curr_imag_vec, sites, a)
        laplacian_imag = {site: laplacian_imag_vec[site][0] for site in sites}

        # Update rule: ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β∇²ψⁿ
        psi_next = {}
        for site in sites:
            psi_p = psi_prev.get(site, 0.0)
            psi_c = psi_curr.get(site, 0.0)
            lap_real = laplacian_real.get(site, 0.0)
            lap_imag = laplacian_imag.get(site, 0.0)

            psi_next[site] = (2.0 * psi_c - psi_p - gamma * (psi_c - psi_p) +
                            beta * complex(lap_real, lap_imag))

        psi_history.append(psi_next)

        # Extract fields from current state (using proper Helmholtz)
        psi_c_real = {site: psi_curr[site].real for site in sites}
        E, B = helmholtz_decomposition_proper(psi_c_real, sites, a)
        E_history.append(E)
        B_history.append(B)

        # Update for next iteration
        psi_prev = psi_curr
        psi_curr = psi_next

    return psi_history, E_history, B_history


# ============================================================================
# PART 3: Faraday Law Validation
# ============================================================================

def validate_faraday_law(
    E_history: List[Dict[Site, Tuple[float, float]]],
    B_history: List[Dict[Site, Tuple[float, float]]],
    sites: Sequence[Site],
    dt: float = 0.1
) -> float:
    """
    Validate Faraday's law: ∇×E + ∂B/∂t ≈ 0

    Returns:
      max_error: maximum violation of Faraday law across all sites and times
    """
    max_error = 0.0

    for t in range(1, len(E_history)):
        E_curr = E_history[t]
        B_prev = B_history[t-1]
        B_curr = B_history[t]

        # Compute ∇×E (discrete curl of E field)
        curl_E = discrete_curl_z(E_curr, sites)

        # Compute ∂B/∂t (finite difference)
        dB_dt = {}
        for site in sites:
            B_p = B_prev.get(site, (0.0, 0.0))
            B_c = B_curr.get(site, (0.0, 0.0))
            dB_dt[site] = ((B_c[0] - B_p[0])/dt, (B_c[1] - B_p[1])/dt)

        # Compute |∇×E + ∂B/∂t|
        for site in sites:
            curl_e = curl_E.get(site, 0.0)
            db_dt = dB_dt.get(site, (0.0, 0.0))
            # Faraday relates scalar curl of E to time derivative of B magnitude
            violation = abs(curl_e + (db_dt[0]**2 + db_dt[1]**2)**0.5)
            max_error = max(max_error, violation)

    return max_error


# ============================================================================
# MAIN: Test Phase 6C
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 6C: MAXWELL SOLVER WITH PROPER HELMHOLTZ DECOMPOSITION")
    print("=" * 80)
    print()

    from hex_lattice_graph import seven_cell

    sites = seven_cell()
    print(f"Testing on {len(sites)}-site seven-cell domain")
    print()

    # Test parameters (same as Phase 6B for comparison)
    a = 1.0
    dt = 0.1
    gamma = 0.5
    beta = 0.5
    k_vec = (0.5, 0.0)
    omega = 0.236039

    # Initialize: plane wave
    psi_0 = {}
    psi_1 = {}
    for site in sites:
        x, y = site_xy(site, a)
        phase_0 = k_vec[0] * x + k_vec[1] * y
        phase_1 = k_vec[0] * x + k_vec[1] * y - omega * dt

        psi_0[site] = complex(math.cos(phase_0), math.sin(phase_0))
        psi_1[site] = complex(math.cos(phase_1), math.sin(phase_1))

    print("Phase 6C Evolution (proper Helmholtz extraction)")
    print("-" * 60)

    try:
        psi_hist, E_hist, B_hist = maxwell_evolution_v6(
            psi_0, psi_1, sites, a=a, dt=dt, gamma=gamma, beta=beta, num_steps=5
        )

        print(f"Evolution complete: {len(psi_hist)} timesteps")
        print(f"E field samples at final time: {len(E_hist[-1]) if E_hist else 0} sites")
        print(f"B field samples at final time: {len(B_hist[-1]) if B_hist else 0} sites")
        print()

        # Validate Faraday
        faraday_error = validate_faraday_law(E_hist, B_hist, sites, dt)
        print(f"Faraday law violation: {faraday_error:.6e}")
        print()

    except Exception as e:
        print(f"Evolution failed: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 80)
    print("PHASE 6C: INITIALIZATION COMPLETE")
    print("=" * 80)
