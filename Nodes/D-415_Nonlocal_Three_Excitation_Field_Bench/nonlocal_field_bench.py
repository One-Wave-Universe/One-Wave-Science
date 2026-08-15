"""One-Wave nonlocal three-excitation field bench.

This is a YELLOW numerical experiment, not a validated physical law.
It evolves one complex field on a periodic 2D triangular lattice, measures
three extended excitations through a partition of unity, and emits
origin-free relational observables.  It contains no point-mass force law.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Config:
    n: int = 48
    dx: float = 1.0
    dt: float = 0.04
    wave_speed: float = 0.35
    damping: float = 0.02
    linear_response: float = 0.05
    nonlinear_response: float = 0.02
    nonlocal_response: float = 0.12
    kernel_length: float = 10.0
    window_width: float = 6.0
    steps: int = 300


def triangular_laplacian(field: np.ndarray, dx: float) -> np.ndarray:
    """Six-neighbor Laplacian on an axial-coordinate triangular lattice."""
    neighbor_sum = (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        + np.roll(np.roll(field, 1, axis=0), -1, axis=1)
        + np.roll(np.roll(field, -1, axis=0), 1, axis=1)
    )
    return (2.0 / (3.0 * dx * dx)) * (neighbor_sum - 6.0 * field)


def periodic_axial_distance2(n: int) -> np.ndarray:
    """Squared minimum-image distance for a periodic axial-coordinate grid."""
    q, r = np.indices((n, n), dtype=np.float64)
    best = np.full((n, n), np.inf)
    for aq in (-n, 0, n):
        for ar in (-n, 0, n):
            dq = q + aq
            dr = r + ar
            best = np.minimum(best, dq * dq + dq * dr + dr * dr)
    return best


def make_global_kernel(cfg: Config) -> tuple[np.ndarray, np.ndarray]:
    """Strictly positive normalized kernel and its FFT.

    The nonzero floor prevents an artificial interaction cutoff.  The kernel
    reads one field globally; it does not represent independent body fields.
    """
    radius = np.sqrt(periodic_axial_distance2(cfg.n)) * cfg.dx
    kernel = np.exp(-radius / cfg.kernel_length) / (1.0 + radius)
    kernel += np.finfo(np.float64).eps
    kernel /= kernel.sum()
    return kernel, np.fft.fft2(kernel)


def global_reference(field: np.ndarray, kernel_fft: np.ndarray) -> np.ndarray:
    return np.fft.ifft2(np.fft.fft2(field) * kernel_fft)


def seed_three_excitations(cfg: Config) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create three extended pulses and a prior state encoding initial motion."""
    q, r = np.indices((cfg.n, cfg.n), dtype=np.float64)
    centers = np.array(
        [
            [0.30 * cfg.n, 0.35 * cfg.n],
            [0.70 * cfg.n, 0.35 * cfg.n],
            [0.50 * cfg.n, 0.70 * cfg.n],
        ],
        dtype=np.float64,
    )
    amplitudes = np.array([1.0, 0.85, 0.70])
    phases = np.array([0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0])
    field = np.zeros((cfg.n, cfg.n), dtype=np.complex128)
    velocity = np.zeros_like(field)

    for k, center in enumerate(centers):
        dq = ((q - center[0] + cfg.n / 2.0) % cfg.n) - cfg.n / 2.0
        dr = ((r - center[1] + cfg.n / 2.0) % cfg.n) - cfg.n / 2.0
        radius2 = dq * dq + dq * dr + dr * dr
        pulse = amplitudes[k] * np.exp(-radius2 / (2.0 * cfg.window_width**2))
        carrier = np.exp(1j * (phases[k] + 0.025 * (k - 1) * (dq - dr)))
        field += pulse * carrier
        velocity += 1j * (0.05 * (k - 1)) * pulse * carrier

    previous = field - cfg.dt * velocity
    return previous, field, centers


def advance(
    previous: np.ndarray,
    current: np.ndarray,
    cfg: Config,
    kernel_fft: np.ndarray,
) -> np.ndarray:
    """Advance the one-field nonlinear nonlocal wave equation by one step."""
    lap = triangular_laplacian(current, cfg.dx)
    reference = global_reference(current, kernel_fft)
    acceleration = (
        cfg.wave_speed**2 * lap
        - cfg.linear_response * current
        - cfg.nonlinear_response * np.abs(current) ** 2 * current
        - cfg.nonlocal_response * (current - reference)
    )
    velocity_increment = current - previous
    return (
        current
        + (1.0 - cfg.damping * cfg.dt) * velocity_increment
        + cfg.dt**2 * acceleration
    )


def partition_windows(centers: np.ndarray, cfg: Config) -> np.ndarray:
    """Three moving windows normalized to sum to one at every lattice site."""
    q, r = np.indices((cfg.n, cfg.n), dtype=np.float64)
    raw = np.empty((3, cfg.n, cfg.n), dtype=np.float64)
    for k, center in enumerate(centers):
        dq = ((q - center[0] + cfg.n / 2.0) % cfg.n) - cfg.n / 2.0
        dr = ((r - center[1] + cfg.n / 2.0) % cfg.n) - cfg.n / 2.0
        radius2 = dq * dq + dq * dr + dr * dr
        raw[k] = np.exp(-radius2 / (2.0 * cfg.window_width**2))
    return raw / np.maximum(raw.sum(axis=0), np.finfo(np.float64).tiny)


def circular_coordinate(weights: np.ndarray, axis: int, n: int) -> float:
    marginal = weights.sum(axis=1 - axis)
    angles = 2.0 * np.pi * np.arange(n) / n
    z = np.sum(marginal * np.exp(1j * angles))
    return float((np.angle(z) % (2.0 * np.pi)) * n / (2.0 * np.pi))


def measure_excitations(
    previous: np.ndarray,
    current: np.ndarray,
    centers: np.ndarray,
    cfg: Config,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Measure centers and energy-like weights; no particle state is inserted."""
    windows = partition_windows(centers, cfg)
    velocity = (current - previous) / cfg.dt
    density = (
        np.abs(current) ** 2
        + np.abs(velocity) ** 2
        + 0.25 * np.abs(triangular_laplacian(current, cfg.dx)) ** 2
    )
    new_centers = np.empty_like(centers)
    weights = np.empty(3, dtype=np.float64)
    amplitudes = np.empty(3, dtype=np.complex128)
    for k in range(3):
        measured = windows[k] * density
        weights[k] = measured.sum()
        new_centers[k, 0] = circular_coordinate(measured, 0, cfg.n)
        new_centers[k, 1] = circular_coordinate(measured, 1, cfg.n)
        amplitudes[k] = np.sum(windows[k] * current) / np.sum(windows[k])
    return new_centers, weights, amplitudes


def minimum_image(delta: np.ndarray, n: int) -> np.ndarray:
    return (delta + n / 2.0) % n - n / 2.0


def relational_observables(
    centers: np.ndarray, weights: np.ndarray, n: int
) -> dict[str, float]:
    """Field-weighted Jacobi-like coordinates plus required shape variables."""
    e12 = minimum_image(centers[1] - centers[0], n)
    pair_center = (weights[0] * centers[0] + weights[1] * centers[1]) / (
        weights[0] + weights[1]
    )
    e3 = minimum_image(centers[2] - pair_center, n)
    rho1 = np.sqrt(weights[0] * weights[1] / (weights[0] + weights[1])) * e12
    rho2 = np.sqrt(
        weights[2]
        * (weights[0] + weights[1])
        / np.maximum(weights.sum(), np.finfo(np.float64).tiny)
    ) * e3
    norm1 = float(np.linalg.norm(rho1))
    norm2 = float(np.linalg.norm(rho2))
    hyperradius = float(np.sqrt(norm1 * norm1 + norm2 * norm2))
    alpha = float(np.arctan2(norm1, norm2))
    cosine = float(np.dot(rho1, rho2) / max(norm1 * norm2, 1e-15))
    return {
        "edge_12": float(np.linalg.norm(e12)),
        "edge_23": float(np.linalg.norm(minimum_image(centers[2] - centers[1], n))),
        "edge_31": float(np.linalg.norm(minimum_image(centers[0] - centers[2], n))),
        "hyperradius": hyperradius,
        "hyperangle_alpha": alpha,
        "shape_cosine": float(np.clip(cosine, -1.0, 1.0)),
    }


def run(cfg: Config, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    kernel, kernel_fft = make_global_kernel(cfg)
    previous, current, centers = seed_three_excitations(cfg)
    rows: list[dict[str, float]] = []

    for step in range(cfg.steps + 1):
        centers, weights, amplitudes = measure_excitations(previous, current, centers, cfg)
        relational = relational_observables(centers, weights, cfg.n)
        row: dict[str, float] = {"step": float(step), "time": step * cfg.dt, **relational}
        for k in range(3):
            row[f"q{k + 1}"] = centers[k, 0]
            row[f"r{k + 1}"] = centers[k, 1]
            row[f"weight{k + 1}"] = weights[k]
            row[f"phase{k + 1}"] = float(np.angle(amplitudes[k]))
        rows.append(row)
        if step < cfg.steps:
            following = advance(previous, current, cfg, kernel_fft)
            previous, current = current, following

    csv_path = output_dir / "three_excitation_trace.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "status": "YELLOW numerical experiment",
        "config": asdict(cfg),
        "kernel_min": float(kernel.min()),
        "kernel_sum": float(kernel.sum()),
        "initial": rows[0],
        "final": rows[-1],
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=Config.steps)
    parser.add_argument("--size", type=int, default=Config.n)
    parser.add_argument("--output", type=Path, default=Path("run_output"))
    args = parser.parse_args()
    cfg = Config(n=args.size, steps=args.steps)
    print(json.dumps(run(cfg, args.output), indent=2))


if __name__ == "__main__":
    main()
