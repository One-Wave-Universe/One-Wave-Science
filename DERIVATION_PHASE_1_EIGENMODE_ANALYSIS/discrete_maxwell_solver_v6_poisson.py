"""
Track C V6: Helmholtz extraction by a discrete Poisson solve.

V5 extracts E = grad(div psi) and B = -curl(curl psi).
Those are second derivatives of the fields, and on this lattice they are not
the Helmholtz parts. V6 solves

    lap(phi) = div(psi)     E = grad(phi)
    lap(A)   = curl(psi)    S = (-dA/dy, dA/dx)    B = curl(S)

using the same div and grad already in discrete_hex_operators.
The Laplacian matrix is singular (constants). The solve is least squares.
"""

import math
import sys
from typing import Dict, Sequence, Tuple

import numpy as np

try:
    from hex_lattice_graph import Site, disk_sites
    from discrete_hex_operators import discrete_divergence, discrete_curl_z, discrete_gradient
    from discrete_maxwell_solver_v5_symmetric import (
        extract_fields_vector,
        one_wave_update_symmetric,
        plane_wave_field_vector,
    )
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


def apply_scalar_laplacian(phi: Dict[Site, complex], sites: Sequence[Site], a: float) -> Dict[Site, complex]:
    grad = discrete_gradient(phi, sites, a)
    return discrete_divergence(grad, sites, a)


def laplacian_matrix(sites: Sequence[Site], a: float) -> np.ndarray:
    n = len(sites)
    index = {site: i for i, site in enumerate(sites)}
    matrix = np.zeros((n, n), dtype=float)
    for col, site in enumerate(sites):
        basis = {s: 0.0 for s in sites}
        basis[site] = 1.0
        lap = apply_scalar_laplacian(basis, sites, a)
        for s, value in lap.items():
            matrix[index[s], col] = float(np.real(value))
    return matrix


def poisson(rhs: Dict[Site, complex], sites: Sequence[Site], matrix: np.ndarray) -> Dict[Site, complex]:
    n = len(sites)
    real = np.array([float(np.real(rhs[s])) for s in sites])
    imag = np.array([float(np.imag(rhs[s])) for s in sites])
    x_real, *_ = np.linalg.lstsq(matrix, real, rcond=1e-8)
    x_imag, *_ = np.linalg.lstsq(matrix, imag, rcond=1e-8)
    return {sites[i]: complex(x_real[i], x_imag[i]) for i in range(n)}


def residual(lhs: Dict[Site, complex], rhs: Dict[Site, complex], sites: Sequence[Site]) -> float:
    return max(abs(lhs[s] - rhs[s]) for s in sites)


def extract_fields_poisson(
    psi: Dict[Site, Tuple[complex, complex]],
    sites: Sequence[Site],
    matrix: np.ndarray,
    a: float = 1.0,
) -> Tuple[Dict[Site, Tuple[complex, complex]], Dict[Site, complex], float]:
    div_psi = discrete_divergence(psi, sites, a)
    phi = poisson(div_psi, sites, matrix)
    e_field = discrete_gradient(phi, sites, a)
    lap_phi = apply_scalar_laplacian(phi, sites, a)

    curl_psi = discrete_curl_z(psi, sites, a)
    avec = poisson(curl_psi, sites, matrix)
    grad_a = discrete_gradient(avec, sites, a)
    # S = curl(A k) = (dA/dy, -dA/dx) with the sign used by the hex curl.
    solenoidal = {site: (grad_a[site][1], -grad_a[site][0]) for site in sites}
    b_field = discrete_curl_z(solenoidal, sites, a)
    return e_field, b_field, residual(lap_phi, div_psi, sites)


def faraday_with(extract, psi_history, sites, dt, a, matrix=None) -> Dict:
    errors = []
    residuals = []
    for t in range(1, len(psi_history) - 1):
        if matrix is None:
            e_t, b_t = extract(psi_history[t], sites, a)
            e_tp, b_tp = extract(psi_history[t + 1], sites, a)
            e_tm, b_tm = extract(psi_history[t - 1], sites, a)
        else:
            e_t, b_t, r = extract(psi_history[t], sites, matrix, a)
            e_tp, b_tp, _ = extract(psi_history[t + 1], sites, matrix, a)
            e_tm, b_tm, _ = extract(psi_history[t - 1], sites, matrix, a)
            residuals.append(r)
        db_dt = {site: (b_tp[site] - b_tm[site]) / (2.0 * dt) for site in sites}
        curl_e = discrete_curl_z(e_t, sites, a)
        for site in sites:
            errors.append(abs(curl_e[site] + db_dt[site]))
    return {
        "max_error": max(errors) if errors else 0.0,
        "mean_error": (sum(errors) / len(errors)) if errors else 0.0,
        "poisson_residual": max(residuals) if residuals else None,
    }


def evolve(radius: int, n_steps: int = 30):
    gamma, beta = 0.5, 0.5
    a = 1.0
    dt = 0.01
    k_x, k_y = 0.5, 0.0
    omega = 0.236039
    sites = disk_sites(radius)
    psi_0 = plane_wave_field_vector(k_x, k_y, 1.0 + 0.0j, 0.0, sites, a)
    factor = complex(math.cos(-omega * dt), math.sin(-omega * dt))
    psi_1 = {site: (psi_0[site][0] * factor, psi_0[site][1] * factor) for site in sites}
    history = [psi_0, psi_1]
    for _ in range(1, n_steps):
        history.append(one_wave_update_symmetric(history[-2], history[-1], gamma, beta, sites, a))
    return sites, history, dt, a


def main():
    print("V6 Poisson extraction vs V5 second-derivative extraction")
    for radius in (2, 3):
        sites, history, dt, a = evolve(radius)
        matrix = laplacian_matrix(sites, a)
        rank = np.linalg.matrix_rank(matrix, tol=1e-8)
        v5 = faraday_with(extract_fields_vector, history, sites, dt, a)
        v6 = faraday_with(extract_fields_poisson, history, sites, dt, a, matrix)
        print()
        print(f"disk radius {radius}: {len(sites)} sites, laplacian rank {rank}/{len(sites)}")
        print(f"  V5 max {v5['max_error']:.6e}  mean {v5['mean_error']:.6e}")
        print(f"  V6 max {v6['max_error']:.6e}  mean {v6['mean_error']:.6e}")
        print(f"  Poisson residual max {v6['poisson_residual']:.6e}")


if __name__ == "__main__":
    main()
