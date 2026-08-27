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
    lock_frequency_epsilon: float = 0.12
    lock_phase_epsilon: float = 0.55
    break_frequency_epsilon: float = 0.24
    break_phase_epsilon: float = 1.10
    lock_rate: float = 0.10
    break_rate: float = 0.06
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


def wrap_phase(value: np.ndarray | float) -> np.ndarray | float:
    return (value + np.pi) % (2.0 * np.pi) - np.pi


def harmonic_branches(harmonic: int) -> tuple[int, int]:
    """Return the shared-node odd-harmonic graph branches."""
    return 2 * harmonic + 1, 2 * harmonic + 3


def cartesian_gradients(field: np.ndarray, dx: float) -> tuple[np.ndarray, np.ndarray]:
    """Cartesian gradient reconstructed from two triangular axial directions."""
    dq = (np.roll(field, -1, axis=0) - np.roll(field, 1, axis=0)) / (2.0 * dx)
    dr = (np.roll(field, -1, axis=1) - np.roll(field, 1, axis=1)) / (2.0 * dx)
    grad_x = dq
    grad_y = (2.0 / np.sqrt(3.0)) * (dr - 0.5 * dq)
    return grad_x, grad_y


def field_descriptors(
    previous: np.ndarray,
    current: np.ndarray,
    cfg: Config,
) -> dict[str, np.ndarray | float]:
    """Scalar, vector, tensor-proxy, harmonic, and rotation diagnostics."""
    grad_x, grad_y = cartesian_gradients(current, cfg.dx)
    density = np.abs(current) ** 2
    current_x = np.imag(np.conj(current) * grad_x)
    current_y = np.imag(np.conj(current) * grad_y)
    regularized = density + 1e-12
    velocity_x = current_x / regularized
    velocity_y = current_y / regularized
    _, dvx_dy = cartesian_gradients(velocity_x, cfg.dx)
    dvy_dx, _ = cartesian_gradients(velocity_y, cfg.dx)
    vorticity = dvy_dx - dvx_dy

    # Candidate gradient-stress diagnostic. It is not a complete physical
    # stress tensor until a canonical Field Lagrangian is fixed.
    t_xx = np.real(np.conj(grad_x) * grad_x)
    t_xy = np.real(np.conj(grad_x) * grad_y)
    t_yy = np.real(np.conj(grad_y) * grad_y)
    phase_unit = current / np.maximum(np.abs(current), 1e-12)
    phase_coherence = float(np.abs(np.sum(density * phase_unit) / np.sum(density)))
    return {
        "density": density,
        "velocity_x": velocity_x,
        "velocity_y": velocity_y,
        "vorticity": vorticity,
        "stress_xx": t_xx,
        "stress_xy": t_xy,
        "stress_yy": t_yy,
        "phase_coherence": phase_coherence,
        "field_velocity_rms": float(np.sqrt(np.mean(velocity_x**2 + velocity_y**2))),
        "field_vorticity_rms": float(np.sqrt(np.mean(vorticity**2))),
        "stress_trace_mean": float(np.mean(t_xx + t_yy)),
    }


def update_phase_locks(
    lock_strength: np.ndarray,
    frequencies: np.ndarray,
    phases: np.ndarray,
    cfg: Config,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Update three pair locks with separate lock and break thresholds."""
    pairs = ((0, 1), (1, 2), (2, 0))
    delta_frequency = np.empty(3)
    delta_phase = np.empty(3)
    updated = lock_strength.copy()
    for pair_index, (a, b) in enumerate(pairs):
        delta_frequency[pair_index] = abs(frequencies[a] - frequencies[b])
        delta_phase[pair_index] = abs(float(wrap_phase(phases[a] - phases[b])))
        inside = (
            delta_frequency[pair_index] < cfg.lock_frequency_epsilon
            and delta_phase[pair_index] < cfg.lock_phase_epsilon
        )
        outside = (
            delta_frequency[pair_index] > cfg.break_frequency_epsilon
            or delta_phase[pair_index] > cfg.break_phase_epsilon
        )
        if inside:
            updated[pair_index] += cfg.lock_rate * (1.0 - updated[pair_index])
        elif outside:
            updated[pair_index] -= cfg.break_rate * updated[pair_index]
        updated[pair_index] = np.clip(updated[pair_index], 0.0, 1.0)
    return updated, delta_frequency, delta_phase


def rotation_receipts(
    centers: np.ndarray,
    previous_centers: np.ndarray,
    weights: np.ndarray,
    windows: np.ndarray,
    descriptors: dict[str, np.ndarray | float],
    cfg: Config,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Measure internal Point, relational Path, and surrounding Field rotation."""
    density = np.asarray(descriptors["density"])
    vorticity = np.asarray(descriptors["vorticity"])
    point_rotation = np.empty(3)
    field_rotation = np.empty(3)
    for k in range(3):
        core = windows[k] ** 2 * density
        surrounding = windows[k] * (1.0 - windows[k]) * density
        point_rotation[k] = np.sum(core * vorticity) / max(np.sum(core), 1e-15)
        field_rotation[k] = np.sum(surrounding * vorticity) / max(
            np.sum(surrounding), 1e-15
        )

    def relative_angles(points: np.ndarray) -> np.ndarray:
        local = np.zeros_like(points)
        local[1] = minimum_image(points[1] - points[0], cfg.n)
        local[2] = minimum_image(points[2] - points[0], cfg.n)
        centroid = np.sum(weights[:, None] * local, axis=0) / weights.sum()
        relative = local - centroid
        return np.arctan2(relative[:, 1], relative[:, 0])

    current_angles = relative_angles(centers)
    previous_angles = relative_angles(previous_centers)
    path_rotation = np.asarray(wrap_phase(current_angles - previous_angles)) / cfg.dt
    return point_rotation, path_rotation, field_rotation


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
    previous_centers = centers.copy()
    previous_phases = np.zeros(3)
    lock_strength = np.zeros(3)
    lock_breaks = np.zeros(3, dtype=np.int64)
    lock_returns = np.zeros(3, dtype=np.int64)
    was_locked = np.zeros(3, dtype=bool)
    rows: list[dict[str, float]] = []

    for step in range(cfg.steps + 1):
        centers, weights, amplitudes = measure_excitations(previous, current, centers, cfg)
        phases = np.angle(amplitudes)
        frequencies = np.asarray(wrap_phase(phases - previous_phases)) / cfg.dt
        lock_strength, delta_frequency, delta_phase = update_phase_locks(
            lock_strength, frequencies, phases, cfg
        )
        now_locked = lock_strength >= 0.5
        lock_breaks += was_locked & ~now_locked
        lock_returns += ~was_locked & now_locked
        was_locked = now_locked
        descriptors = field_descriptors(previous, current, cfg)
        windows = partition_windows(centers, cfg)
        point_rotation, path_rotation, field_rotation = rotation_receipts(
            centers, previous_centers, weights, windows, descriptors, cfg
        )
        relational = relational_observables(centers, weights, cfg.n)
        row: dict[str, float] = {"step": float(step), "time": step * cfg.dt, **relational}
        row["phase_coherence"] = float(descriptors["phase_coherence"])
        row["field_velocity_rms"] = float(descriptors["field_velocity_rms"])
        row["field_vorticity_rms"] = float(descriptors["field_vorticity_rms"])
        row["stress_trace_mean"] = float(descriptors["stress_trace_mean"])
        for k in range(3):
            row[f"q{k + 1}"] = centers[k, 0]
            row[f"r{k + 1}"] = centers[k, 1]
            row[f"weight{k + 1}"] = weights[k]
            row[f"phase{k + 1}"] = float(phases[k])
            row[f"frequency{k + 1}"] = float(frequencies[k])
            row[f"point_rotation{k + 1}"] = float(point_rotation[k])
            row[f"path_rotation{k + 1}"] = float(path_rotation[k])
            row[f"field_rotation{k + 1}"] = float(field_rotation[k])
            row[f"lock{k + 1}"] = float(lock_strength[k])
            row[f"lock_delta_frequency{k + 1}"] = float(delta_frequency[k])
            row[f"lock_delta_phase{k + 1}"] = float(delta_phase[k])
        rows.append(row)
        previous_centers = centers.copy()
        previous_phases = phases.copy()
        if step < cfg.steps:
            following = advance(previous, current, cfg, kernel_fft)
            previous, current = current, following

    csv_path = output_dir / "three_excitation_trace.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    min_edge = min(min(row["edge_12"], row["edge_23"], row["edge_31"]) for row in rows)
    max_edge = max(max(row["edge_12"], row["edge_23"], row["edge_31"]) for row in rows)
    accumulated_rotation = max(
        abs(sum(row[f"path_rotation{k}"] * cfg.dt for row in rows)) for k in (1, 2, 3)
    )
    if min_edge < 0.5 * cfg.window_width:
        outcome = "collision_or_merge_candidate"
    elif max_edge > 0.70 * cfg.n:
        outcome = "ejection_candidate"
    elif accumulated_rotation > 2.0 * np.pi:
        outcome = "bounded_rotation_candidate"
    else:
        outcome = "bounded_or_unresolved"

    summary = {
        "status": "YELLOW numerical experiment",
        "config": asdict(cfg),
        "kernel_min": float(kernel.min()),
        "kernel_sum": float(kernel.sum()),
        "harmonic_graph_seed": {
            str(h): list(harmonic_branches(h)) for h in (0, 1, 2)
        },
        "classification": outcome,
        "lock_breaks": lock_breaks.tolist(),
        "lock_returns": lock_returns.tolist(),
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
