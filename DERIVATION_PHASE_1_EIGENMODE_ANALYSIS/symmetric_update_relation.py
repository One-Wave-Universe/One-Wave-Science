"""
What the symmetric update actually preserves.

The step is
    psi^{n+1} = 2 psi^n - psi^{n-1} - gamma (psi^n - psi^{n-1}) + beta * lap(psi^n)

If lap(v) = mu v, the time factor lambda = psi^n / psi^{n-1} obeys
    lambda^2 - (2 - gamma + beta * mu) lambda + (1 - gamma) = 0

Faraday is not this relation. This script checks the relation on one real
eigenmode of the disk Laplacian, and on the plane wave used by V5, which is
not an eigenmode of that disk.
"""

import math
import sys
from typing import Dict, Sequence, Tuple

import numpy as np

try:
    from hex_lattice_graph import Site, disk_sites
    from discrete_maxwell_solver_v5_symmetric import (
        discrete_laplacian_vector,
        one_wave_update_symmetric,
        plane_wave_field_vector,
    )
    from discrete_maxwell_solver_v6_poisson import laplacian_matrix
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


GAMMA = 0.5
BETA = 0.5
A = 1.0
DT = 0.01
N_STEPS = 40


def characteristic_roots(mu: complex) -> Tuple[complex, complex]:
    b = (2.0 - GAMMA) + BETA * mu
    c = 1.0 - GAMMA
    disc = np.sqrt(complex(b * b - 4.0 * c))
    return (b + disc) / 2.0, (b - disc) / 2.0


def physical_root(mu: complex) -> complex:
    roots = characteristic_roots(mu)
    return min(roots, key=lambda z: abs(abs(z) - 1.0))


def as_vector(mode: np.ndarray, sites: Sequence[Site]) -> Dict[Site, Tuple[complex, complex]]:
    return {sites[i]: (complex(mode[i]), 0.0j) for i in range(len(sites))}


def ratio_error(history, sites, lam: complex) -> float:
    worst = 0.0
    for n in range(1, len(history)):
        for site in sites:
            prev = history[n - 1][site][0]
            curr = history[n][site][0]
            if abs(prev) < 1e-8:
                continue
            worst = max(worst, abs(curr / prev - lam))
    return worst


def update_residual(history, sites) -> float:
    worst = 0.0
    for n in range(1, len(history) - 1):
        stepped = one_wave_update_symmetric(history[n - 1], history[n], GAMMA, BETA, sites, A)
        for site in sites:
            for comp in (0, 1):
                worst = max(worst, abs(stepped[site][comp] - history[n + 1][site][comp]))
    return worst


def evolve_from(psi0, lam, sites):
    psi1 = {site: (psi0[site][0] * lam, psi0[site][1] * lam) for site in sites}
    history = [psi0, psi1]
    for _ in range(N_STEPS - 1):
        history.append(one_wave_update_symmetric(history[-2], history[-1], GAMMA, BETA, sites, A))
    return history


def eigenmode_case(radius: int):
    sites = disk_sites(radius)
    matrix = laplacian_matrix(sites, A)
    eigvals, eigvecs = np.linalg.eig(matrix)
    # Drop the constant kernel. Take the eigenvalue closest to -k^2 = -0.25
    # so the comparison with the V5 wave number is the same scale.
    order = np.argsort(np.abs(eigvals.real + 0.25))
    pick = None
    for idx in order:
        if abs(eigvals[idx].real) < 1e-8:
            continue
        pick = idx
        break
    mu = complex(eigvals[pick])
    mode = eigvecs[:, pick]
    mode = mode / np.max(np.abs(mode))
    # The matrix is real. A complex phase from the eigensolver is noise.
    mode = np.real_if_close(mode, tol=1e6)
    mode = np.real(mode)
    lam = physical_root(mu)
    history = evolve_from(as_vector(mode, sites), lam, sites)
    print(f"eigenmode  radius {radius}  sites {len(sites)}")
    print(f"  mu {mu.real:.6e}  {mu.imag:.3e}i")
    print(f"  lambda {lam.real:.6f} {lam.imag:.6f}i   |lambda| {abs(lam):.6f}")
    print(f"  update residual {update_residual(history, sites):.3e}")
    print(f"  lambda error    {ratio_error(history, sites, lam):.3e}")
    return mu, lam


def plane_wave_case(radius: int):
    sites = disk_sites(radius)
    k_x, k_y = 0.5, 0.0
    psi0 = plane_wave_field_vector(k_x, k_y, 1.0 + 0.0j, 0.0, sites, A)
    lap = discrete_laplacian_vector(psi0, sites, A)
    mus = []
    for site in sites:
        vx = psi0[site][0]
        if abs(vx) < 1e-8:
            continue
        mus.append(lap[site][0] / vx)
    mus = np.array(mus)
    center = (0, 0)
    mu_center = lap[center][0] / psi0[center][0]
    lam_assumed = complex(math.cos(-0.236039 * DT), math.sin(-0.236039 * DT))
    history = evolve_from(psi0, lam_assumed, sites)
    measured = []
    for n in range(1, len(history)):
        prev = history[n - 1][center][0]
        curr = history[n][center][0]
        measured.append(curr / prev)
    measured = np.array(measured)
    print(f"plane wave radius {radius}  sites {len(sites)}  assumed k^2 {-k_x * k_x:.3f}")
    print(f"  mu center {mu_center.real:.6e} {mu_center.imag:.3e}i")
    print(f"  mu real spread {mus.real.min():.4f} .. {mus.real.max():.4f}")
    print(f"  lambda from center mu {physical_root(mu_center)}")
    print(f"  lambda assumed        {lam_assumed}")
    print(f"  center lambda drift   {np.max(np.abs(measured - measured[0])):.3e}")
    print(f"  update residual {update_residual(history, sites):.3e}")


def main():
    print("Relation: lambda^2 - (2 - gamma + beta*mu) lambda + (1 - gamma) = 0")
    print(f"gamma {GAMMA}  beta {BETA}")
    print()
    eigenmode_case(2)
    print()
    eigenmode_case(3)
    print()
    plane_wave_case(2)
    print()
    plane_wave_case(3)


if __name__ == "__main__":
    main()
