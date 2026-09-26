"""G-766 discrete triangular-lattice dispersion and octave controls.

This is a numerical control fixture, not a physical lattice derivation.
The coordinate spacing ``a_num`` is dimensionless unless an independent
calibration establishes otherwise.
"""

from __future__ import annotations

import cmath
import itertools
import json
import math
from dataclasses import asdict, dataclass
from typing import Iterable, List, Sequence, Tuple


GATE = "YELLOW"
MODEL = "g766_triangular_lattice_linear_control"


def triangular_laplacian_symbol(kx: float, ky: float, a_num: float = 1.0) -> float:
    """Return the six-neighbor triangular-lattice Laplacian symbol."""
    if a_num <= 0.0:
        raise ValueError("a_num must be positive")
    a1_dot_k = a_num * kx
    a2_dot_k = a_num * (0.5 * kx + math.sqrt(3.0) * 0.5 * ky)
    a3_dot_k = a2_dot_k - a1_dot_k
    return (2.0 / (a_num * a_num)) * (
        math.cos(a1_dot_k) + math.cos(a2_dot_k) + math.cos(a3_dot_k) - 3.0
    )


def omega_squared(
    kx: float,
    ky: float,
    c_lattice: float,
    omega0: float,
    a_num: float = 1.0,
) -> float:
    if c_lattice < 0.0 or omega0 < 0.0:
        raise ValueError("c_lattice and omega0 must be non-negative")
    symbol = triangular_laplacian_symbol(kx, ky, a_num)
    return omega0 * omega0 - c_lattice * c_lattice * symbol


def temporal_roots(
    kx: float,
    ky: float,
    c_lattice: float,
    omega0: float,
    zeta: float,
    a_num: float = 1.0,
) -> Tuple[complex, complex]:
    if zeta < 0.0:
        raise ValueError("zeta must be non-negative")
    damping_rate = zeta * omega0
    root = cmath.sqrt(
        omega_squared(kx, ky, c_lattice, omega0, a_num)
        - damping_rate * damping_rate
    )
    shift = -1j * damping_rate
    return shift + root, shift - root


def leapfrog_step(
    q_now: float,
    q_previous: float,
    omega_sq: float,
    dt: float,
    drive: float = 0.0,
) -> float:
    if dt <= 0.0:
        raise ValueError("dt must be positive")
    return 2.0 * q_now - q_previous + dt * dt * (drive - omega_sq * q_now)


def leapfrog_frequency(omega_sq: float, dt: float) -> float:
    """Return the frequency represented by the undamped leapfrog update."""
    if omega_sq < 0.0 or dt <= 0.0:
        raise ValueError("omega_sq must be non-negative and dt positive")
    cosine = 1.0 - 0.5 * dt * dt * omega_sq
    if cosine < -1.0 or cosine > 1.0:
        raise ValueError("unstable timestep for this mode")
    return math.acos(cosine) / dt


def group_velocity_numeric(
    kx: float,
    ky: float,
    c_lattice: float,
    omega0: float,
    a_num: float = 1.0,
    delta_k: float = 1.0e-6,
) -> Tuple[float, float]:
    if delta_k <= 0.0:
        raise ValueError("delta_k must be positive")

    def omega(x: float, y: float) -> float:
        return math.sqrt(omega_squared(x, y, c_lattice, omega0, a_num))

    vx = (omega(kx + delta_k, ky) - omega(kx - delta_k, ky)) / (2.0 * delta_k)
    vy = (omega(kx, ky + delta_k) - omega(kx, ky - delta_k)) / (2.0 * delta_k)
    return vx, vy


def octave_residual(f_high: float, f_low: float) -> float:
    if f_high <= 0.0 or f_low <= 0.0:
        raise ValueError("frequencies must be positive")
    ratio_log = math.log2(f_high / f_low)
    return ratio_log - round(ratio_log)


def pairwise_octave_residuals(frequencies: Iterable[float]) -> List[float]:
    values = sorted(float(value) for value in frequencies)
    if len(values) < 2:
        raise ValueError("at least two frequencies are required")
    return [octave_residual(high, low) for low, high in itertools.combinations(values, 2)]


@dataclass(frozen=True)
class OctaveControlReceipt:
    frequencies_hz: Tuple[float, ...]
    epsilon_octave: float
    residuals: Tuple[float, ...]
    compatible_pairs: int
    total_pairs: int
    all_pairs_compatible: bool


def octave_control_receipt(
    frequencies_hz: Sequence[float], epsilon_octave: float = 0.01
) -> OctaveControlReceipt:
    if epsilon_octave < 0.0:
        raise ValueError("epsilon_octave must be non-negative")
    residuals = tuple(pairwise_octave_residuals(frequencies_hz))
    compatible = sum(abs(value) <= epsilon_octave for value in residuals)
    return OctaveControlReceipt(
        frequencies_hz=tuple(float(value) for value in frequencies_hz),
        epsilon_octave=epsilon_octave,
        residuals=residuals,
        compatible_pairs=compatible,
        total_pairs=len(residuals),
        all_pairs_compatible=compatible == len(residuals),
    )


def dispersion_receipt(
    kx: float,
    ky: float,
    c_lattice: float,
    omega0: float,
    timesteps: Sequence[float],
    a_num: float = 1.0,
) -> dict:
    omega_sq = omega_squared(kx, ky, c_lattice, omega0, a_num)
    analytic = math.sqrt(omega_sq)
    refinements = []
    for dt in timesteps:
        measured = leapfrog_frequency(omega_sq, dt)
        refinements.append(
            {
                "dt": dt,
                "measured_omega": measured,
                "absolute_error": abs(measured - analytic),
            }
        )
    return {
        "gate": GATE,
        "model": MODEL,
        "k": [kx, ky],
        "a_num": a_num,
        "a_num_is_physical_length": False,
        "derived_physical_lattice_spacing": False,
        "laplacian_symbol": triangular_laplacian_symbol(kx, ky, a_num),
        "analytic_omega": analytic,
        "group_velocity": list(group_velocity_numeric(kx, ky, c_lattice, omega0, a_num)),
        "refinements": refinements,
    }


def main() -> None:
    receipt = {
        "dispersion": dispersion_receipt(
            kx=0.35,
            ky=0.2,
            c_lattice=1.0,
            omega0=0.25,
            timesteps=(0.2, 0.1, 0.05, 0.025),
        ),
        "exact_octave_control": asdict(octave_control_receipt((10.0, 20.0, 40.0))),
        "non_octave_control": asdict(octave_control_receipt((10.0, 15.0, 23.0))),
        "sampling_rate_is_signal_frequency": False,
        "claim": "control fixture only; no octave emergence or physical scale established",
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
