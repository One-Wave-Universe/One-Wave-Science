"""Validated diagnostics for line-vortex and toroidal-ring trial profiles."""

from __future__ import annotations

from math import pi, sqrt
from typing import Callable, Tuple

import numpy as np


def line_vortex_continuum_energies(sigma: float) -> Tuple[float, float, float]:
    """Exact I1, I3, and dilation minimum for (x+i y)/sigma Gaussian."""
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    i1 = 2.5 * pi ** 1.5 * sigma
    i3 = 8.75 * pi ** 1.5 / sigma
    return i1, i3, sqrt(i3 / i1)


def wrapped_winding(phase: np.ndarray) -> float:
    """Winding of ordered samples on a loop that does not cross a field zero."""
    phase = np.asarray(phase, dtype=float)
    if phase.ndim != 1 or phase.size < 3:
        raise ValueError("phase must contain at least three ordered loop samples")
    closed = np.concatenate((phase, phase[:1]))
    return float(np.angle(np.exp(1j * np.diff(closed))).sum() / (2.0 * pi))


def periodic_laplacian(field: np.ndarray, dx: float) -> np.ndarray:
    if field.ndim != 3 or dx <= 0.0:
        raise ValueError("field must be 3D and dx positive")
    return (
        np.roll(field, 1, 0) + np.roll(field, -1, 0)
        + np.roll(field, 1, 1) + np.roll(field, -1, 1)
        + np.roll(field, 1, 2) + np.roll(field, -1, 2)
        - 6.0 * field
    ) / dx**2


def positive_spatial_operator(field: np.ndarray, dx: float, beta: float = 1.0) -> np.ndarray:
    """A psi for psi_tt + A psi = 0 using the exact evolution stencil."""
    if beta < 0.0:
        raise ValueError("beta must be nonnegative")
    lap = periodic_laplacian(field, dx)
    return -lap + beta * periodic_laplacian(lap, dx)


def leapfrog_invariant(
    psi_n: np.ndarray,
    psi_np1: np.ndarray,
    dx: float,
    dt: float,
    beta: float = 1.0,
) -> float:
    """Exact quadratic invariant of the undamped leapfrog recurrence.

    E_(n+1/2)=1/2||v_(n+1/2)||^2 + 1/2 Re<psi_(n+1),A psi_n>.
    It is distinct from evaluating the continuum Hamiltonian at one time.
    """
    if psi_n.shape != psi_np1.shape or dt <= 0.0:
        raise ValueError("states must share shape and dt must be positive")
    velocity = (psi_np1 - psi_n) / dt
    kinetic = 0.5 * np.vdot(velocity, velocity).real
    potential = 0.5 * np.vdot(psi_np1, positive_spatial_operator(psi_n, dx, beta)).real
    return float((kinetic + potential) * dx**3)


def leapfrog_step(
    psi_nm1: np.ndarray,
    psi_n: np.ndarray,
    dx: float,
    dt: float,
    beta: float = 1.0,
) -> np.ndarray:
    return 2.0 * psi_n - psi_nm1 - dt**2 * positive_spatial_operator(psi_n, dx, beta)


def toroidal_core_radius(
    psi: np.ndarray,
    coordinates: np.ndarray,
    search_annulus: Tuple[float, float],
    radial_bins: int = 256,
) -> float:
    """Find the radial amplitude minimum inside a declared core annulus.

    The search annulus is mandatory because localized envelopes also approach
    zero at the outer boundary. A global argmin therefore does not identify a
    toroidal core.
    """
    if psi.ndim != 3 or psi.shape[0] != psi.shape[1] or psi.shape[2] != coordinates.size:
        raise ValueError("psi must be a cubic grid matching coordinates")
    r_min, r_max = search_annulus
    if not 0.0 <= r_min < r_max or radial_bins < 4:
        raise ValueError("invalid search annulus or radial bin count")
    z_index = int(np.argmin(np.abs(coordinates)))
    x, y = np.meshgrid(coordinates, coordinates, indexing="ij")
    radius = np.sqrt(x*x + y*y).ravel()
    amplitude = np.abs(psi[:, :, z_index]).ravel()
    edges = np.linspace(r_min, r_max, radial_bins + 1)
    which = np.digitize(radius, edges) - 1
    means = np.full(radial_bins, np.inf)
    for index in range(radial_bins):
        selected = which == index
        if np.any(selected):
            means[index] = float(amplitude[selected].mean())
    best = int(np.argmin(means))
    return float(0.5 * (edges[best] + edges[best + 1]))

