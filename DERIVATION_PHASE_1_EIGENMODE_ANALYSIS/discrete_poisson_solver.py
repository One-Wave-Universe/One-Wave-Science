"""
Track C: Discrete Poisson Solver on Hexagonal Lattice
========================================================

Implement solution to ∇²φ = ρ on 2D hexagonal lattice using Fourier method.

This is the key refinement for Phase 6C: enabling proper Helmholtz decomposition
by solving for potentials (φ and A_z) rather than just applying derivative operators.

The problem:
  Phase 6B field extraction E = ∇(∇·ψ) creates artifacts because it bypasses the
  potential-solving step. Correct approach:
    1. Compute ∇·ψ to get ρ_E (charge-like source)
    2. Solve ∇²φ = ρ_E for scalar potential φ
    3. Extract E = ∇φ (now physical, no artifacts)

Similarly for curl field (magnetic potential A_z):
    1. Compute (∇×ψ)_z to get ρ_B
    2. Solve ∇²A_z = ρ_B for vector potential
    3. Extract B = ∇×(A_z k̂)

Method: Fourier space inversion (exact for periodic boundaries)
  - Transform source ρ to Fourier space via FFT
  - Divide by Laplacian eigenvalues λ(k) for each k-mode
  - Inverse FFT to get physical-space solution φ
"""

import numpy as np
import math
from typing import Dict, List, Tuple, Sequence
from discrete_hex_operators import (
    Site, NEIGHBOR_OFFSETS, neighbor, site_xy,
    discrete_divergence, discrete_curl_z, discrete_gradient
)


# ============================================================================
# PART 1: Fourier Space Laplacian Eigenvalues
# ============================================================================

def laplacian_eigenvalues_2d(shape: Tuple[int, int], a: float = 1.0) -> np.ndarray:
    """
    Compute Laplacian eigenvalues λ(k) for hexagonal lattice in Fourier space.

    For a hexagonal lattice with discrete Laplacian:
      ∇²f(i) = (1/A_cell) ∑_j (f_j - f_i) · (normal weight)

    The eigenvalues in Fourier space are:
      λ(k_x, k_y) = ∑_neighbors cos(k · offset) - z_coord

    where z_coord = 6 for hexagonal lattice.

    Args:
      shape: (nx, ny) size of lattice for FFT
      a: lattice constant

    Returns:
      lambda_k: (nx, ny) array of eigenvalues
    """
    nx, ny = shape

    # Compute frequencies
    kx = 2 * np.pi * np.fft.fftfreq(nx) / a
    ky = 2 * np.pi * np.fft.fftfreq(ny) / a

    # Meshgrid of frequencies
    KX, KY = np.meshgrid(kx, ky, indexing='ij')

    # Sum cos(k · offset) for all neighbor offsets
    lambda_k = np.zeros_like(KX, dtype=float)

    for (mx, my) in NEIGHBOR_OFFSETS:
        x, y = site_xy((mx, my), a=a)
        # e^(i k·r) has real part cos(k·r)
        phase = KX * x + KY * y
        lambda_k += np.cos(phase)

    # Subtract coordination number (6 for hex)
    lambda_k -= 6.0

    return lambda_k


def safe_invert_laplacian(lambda_k: np.ndarray, zero_mode_value: float = 1.0) -> np.ndarray:
    """
    Safely invert Laplacian eigenvalues with singularity handling.

    The k=0 mode has λ(0) = 0 (Laplacian of constant is zero).
    For solving ∇²φ = ρ, the zero mode is determined by boundary conditions.

    For periodic boundary conditions with ∑ρ = 0, set λ⁻¹(0) = 0.
    For other cases, the zero mode is underdetermined (Poisson equation constraint).

    Args:
      lambda_k: Laplacian eigenvalues
      zero_mode_value: value to use for k=0 mode (default: 0 for periodic)

    Returns:
      lambda_k_inv: 1/λ(k) with singularity handled
    """
    lambda_k_inv = np.zeros_like(lambda_k)

    # Safe division: avoid singularities at k=0
    nonzero = np.abs(lambda_k) > 1e-14
    lambda_k_inv[nonzero] = 1.0 / lambda_k[nonzero]

    # For k=0 (DC component), set to zero_mode_value
    lambda_k_inv[0, 0] = zero_mode_value

    return lambda_k_inv


# ============================================================================
# PART 2: Fourier-Space Poisson Solver
# ============================================================================

def poisson_solve_fourier(
    rho: Dict[Site, float],
    sites: Sequence[Site],
    a: float = 1.0,
    zero_mode_value: float = 0.0
) -> Dict[Site, float]:
    """
    Solve ∇²φ = ρ on hexagonal lattice using Fourier method.

    Algorithm:
      1. Embed site values into regular grid (nx, ny)
      2. Compute λ(k) eigenvalues of Laplacian in Fourier space
      3. FFT: ρ̂(k) = FFT(ρ)
      4. Divide: φ̂(k) = ρ̂(k) / λ(k)  [with singularity handling at k=0]
      5. Inverse FFT: φ = IFFT(φ̂)
      6. Extract values at site locations

    Args:
      rho: source term ρ (as dict Site -> float)
      sites: list of Site coordinates
      a: lattice constant
      zero_mode_value: value to use for k=0 (default 0 for periodic boundary)

    Returns:
      phi: solution φ (as dict Site -> float)
    """
    if not sites:
        return {}

    # Determine grid bounds
    sites_list = list(sites)
    m_coords = [s[0] for s in sites_list]
    n_coords = [s[1] for s in sites_list]

    m_min, m_max = min(m_coords), max(m_coords)
    n_min, n_max = min(n_coords), max(n_coords)

    # Grid dimensions (power of 2 for efficiency)
    nx = 2 ** math.ceil(math.log2(m_max - m_min + 1))
    ny = 2 ** math.ceil(math.log2(n_max - n_min + 1))

    # Create regular grid (pad with zeros for FFT)
    rho_grid = np.zeros((nx, ny), dtype=complex)

    # Fill in site values (shifted to origin)
    for site in sites:
        if site in rho:
            m, n = site
            i = m - m_min
            j = n - n_min
            if 0 <= i < nx and 0 <= j < ny:
                rho_grid[i, j] = rho[site]

    # Compute Laplacian eigenvalues
    lambda_k = laplacian_eigenvalues_2d((nx, ny), a=a)

    # Safe inversion
    lambda_k_inv = safe_invert_laplacian(lambda_k, zero_mode_value=zero_mode_value)

    # Fourier transform
    rho_hat = np.fft.fft2(rho_grid)

    # Divide by eigenvalues (element-wise in Fourier space)
    phi_hat = rho_hat * lambda_k_inv

    # Inverse Fourier transform
    phi_grid = np.fft.ifft2(phi_hat)

    # Extract real part and map back to sites
    phi = {}
    for site in sites:
        m, n = site
        i = m - m_min
        j = n - n_min
        if 0 <= i < nx and 0 <= j < ny:
            # Take real part (imaginary should be negligible)
            phi[site] = float(np.real(phi_grid[i, j]))
        else:
            phi[site] = 0.0

    return phi


# ============================================================================
# PART 3: Iterative Solver (Jacobi method) - Backup/Verification
# ============================================================================

def poisson_solve_jacobi(
    rho: Dict[Site, float],
    sites: Sequence[Site],
    a: float = 1.0,
    max_iterations: int = 100,
    tolerance: float = 1e-6
) -> Dict[Site, float]:
    """
    Solve ∇²φ = ρ using Jacobi iteration (for verification/validation).

    The Jacobi iteration for discrete Laplacian:
      φⁿ⁺¹(i) = (1/6) ∑_neighbors φⁿ(j) - (a²/A_cell) ρ(i)

    This is slower than Fourier but useful for validation on non-periodic domains.

    Args:
      rho: source term
      sites: lattice sites
      a: lattice constant
      max_iterations: maximum number of iterations
      tolerance: convergence criterion (max change in φ)

    Returns:
      phi: solution after convergence
    """
    # Initialize
    phi = {site: 0.0 for site in sites}
    sites_adj = {site: [] for site in sites}

    # Build adjacency
    site_set = set(sites)
    for site in sites:
        for offset in NEIGHBOR_OFFSETS:
            nbr = neighbor(site, offset)
            if nbr in site_set:
                sites_adj[site].append(nbr)

    # Laplacian scaling factor
    a_hex = (3.0 * math.sqrt(3.0) / 2.0) * (a ** 2)

    # Jacobi iteration
    for iteration in range(max_iterations):
        phi_new = {}
        max_change = 0.0

        for site in sites:
            if site not in sites_adj or len(sites_adj[site]) == 0:
                phi_new[site] = 0.0
                continue

            # Average of neighbors
            neighbor_sum = sum(phi.get(nbr, 0.0) for nbr in sites_adj[site])
            neighbor_avg = neighbor_sum / len(sites_adj[site])

            # Jacobi update: φ ≈ (neighbor_avg - (a²/6) * ρ)
            # Approximate from stencil: -∇²φ = -ρ means 6*φ - sum_neighbors ≈ a²*ρ
            rho_val = rho.get(site, 0.0)
            phi_new[site] = neighbor_avg - (a_hex / 6.0) * rho_val

            max_change = max(max_change, abs(phi_new[site] - phi.get(site, 0.0)))

        phi = phi_new

        if max_change < tolerance:
            print(f"Jacobi converged in {iteration + 1} iterations")
            break
    else:
        print(f"Jacobi reached max iterations ({max_iterations}) without convergence")

    return phi


# ============================================================================
# PART 4: Proper Helmholtz Extraction
# ============================================================================

def helmholtz_decomposition_proper(
    vector_field: Dict[Site, Tuple[float, float]],
    sites: Sequence[Site],
    a: float = 1.0
) -> Tuple[Dict[Site, Tuple[float, float]], Dict[Site, Tuple[float, float]]]:
    """
    Decompose vector field F into potential and solenoidal parts using Poisson solving.

    Helmholtz decomposition: F = ∇φ + ∇×(A k̂)

    Procedure:
      1. Compute ρ_pot = ∇·F (divergence, gives potential source)
      2. Solve ∇²φ = ρ_pot to get scalar potential
      3. Compute E_pot = ∇φ (potential part, now exact)

      4. Compute ρ_sol = ∇×F (curl, gives solenoidal source)
      5. Solve ∇²A = ρ_sol to get vector potential
      6. Compute E_sol = ∇×(A k̂) (solenoidal part)

    Args:
      vector_field: input vector field F
      sites: lattice sites
      a: lattice constant

    Returns:
      (E_potential, E_solenoidal): decomposition into two parts
    """
    # Compute divergence (source for potential equation)
    div_f = discrete_divergence(vector_field, sites, a)

    # Solve for scalar potential φ
    phi = poisson_solve_fourier(div_f, sites, a, zero_mode_value=0.0)

    # Extract potential part: E = ∇φ
    E_pot = discrete_gradient(phi, sites, a)

    # Compute curl (source for solenoidal equation)
    curl_f = discrete_curl_z(vector_field, sites, a)

    # Solve for vector potential A_z
    A_z = poisson_solve_fourier(curl_f, sites, a, zero_mode_value=0.0)

    # Extract solenoidal part: B = ∇×(A_z k̂) = (∂A/∂y, -∂A/∂x)
    grad_A = discrete_gradient(A_z, sites, a)
    E_sol = {}
    for site in sites:
        dA_dy, dA_dx = grad_A.get(site, (0.0, 0.0))
        E_sol[site] = (dA_dy, -dA_dx)  # Rotate gradient 90° clockwise

    return E_pot, E_sol


# ============================================================================
# MAIN: Test the solver
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TRACK C: DISCRETE POISSON SOLVER FOR HEXAGONAL LATTICE")
    print("=" * 80)
    print()

    from hex_lattice_graph import seven_cell

    sites = seven_cell()
    print(f"Testing on {len(sites)}-site seven-cell domain")
    print()

    # Test 1: Simple source
    print("Test 1: Poisson solve with constant source")
    print("-" * 60)
    rho_test = {site: 1.0 for site in sites}
    phi_solution = poisson_solve_fourier(rho_test, sites)

    print("Solution φ at each site:")
    for site in sorted(sites):
        print(f"  {site}: φ = {phi_solution.get(site, 0.0):8.4f}")
    print()

    # Test 2: Verification with Jacobi
    print("Test 2: Comparison with Jacobi solver")
    print("-" * 60)
    phi_jacobi = poisson_solve_jacobi(rho_test, sites, max_iterations=50)

    print("Jacobi solution:")
    for site in sorted(sites):
        phi_f = phi_solution.get(site, 0.0)
        phi_j = phi_jacobi.get(site, 0.0)
        diff = abs(phi_f - phi_j)
        print(f"  {site}: Fourier={phi_f:8.4f}, Jacobi={phi_j:8.4f}, diff={diff:.2e}")
    print()

    print("=" * 80)
    print("TRACK C: POISSON SOLVER INITIALIZATION COMPLETE")
    print("=" * 80)
