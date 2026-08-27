"""Executable state and receipts from Updated 38-41.

No new planetary law is inserted here. Unresolved maps remain inputs so the
repository's Yellow motion architecture can be tested without silently choosing
body-specific coefficients.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Bound2DState:
    displacement: float
    compression: float
    tension: float
    shear_damping: float
    integrity: float
    phase: float
    circulation: float


@dataclass(frozen=True)
class RotationState:
    core: np.ndarray
    fluid: np.ndarray
    mantle: np.ndarray
    body: np.ndarray
    em: np.ndarray
    field: np.ndarray


@dataclass(frozen=True)
class PointState:
    density: float
    phase: float
    rotations: RotationState
    internal_current: np.ndarray
    internal_field: np.ndarray


@dataclass(frozen=True)
class PathState:
    position: np.ndarray
    velocity: np.ndarray
    phase: float
    slope_differential: float
    overlap: float

    @property
    def rotation(self) -> np.ndarray:
        radius2 = float(self.position @ self.position)
        return np.zeros(3) if radius2 == 0 else np.cross(self.position, self.velocity) / radius2


@dataclass(frozen=True)
class FieldState:
    slope: float
    curvature: float
    active_range: float
    rotation: np.ndarray
    phase: float
    em_shell: float
    reference_slope: float


@dataclass(frozen=True)
class RecursivePPF:
    PP: float
    PPa: float
    PF: float
    PaP: float
    PaPa: float
    PaF: float
    FP: float
    FPa: float
    FF: float

    def as_array(self) -> np.ndarray:
        return np.array((self.PP, self.PPa, self.PF, self.PaP, self.PaPa,
                         self.PaF, self.FP, self.FPa, self.FF))


@dataclass(frozen=True)
class PlanetaryDisplacementState:
    name: str
    bound: Bound2DState
    point: PointState
    path: PathState
    field: FieldState
    recursive: RecursivePPF


@dataclass(frozen=True)
class DisplacementReceipt:
    name: str
    local_slope: float
    reference_slope: float
    slope_differential: float
    active_range: float
    path_rotation: tuple[float, float, float]
    core_mantle_differential: float
    matter_em_differential: float
    point_field_differential: float
    spin_path_differential: float
    shear_measure: float
    overlap_count: int
    ppf_norm: float


def local_reference_slope(slopes: np.ndarray, weights: np.ndarray,
                          reference: float) -> tuple[float, float]:
    """Updated 38-41: DeltaS = S_local - S_reference."""
    slopes = np.asarray(slopes, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if slopes.shape != weights.shape or np.any(weights < 0):
        raise ValueError("slope and nonnegative overlap-weight arrays must match")
    local = float(np.sum(weights * slopes))
    return local, local - float(reference)


def distinguishable_active_range(radius: np.ndarray, slope: np.ndarray,
                                 reference: np.ndarray, threshold: float) -> float:
    """Updated 39/41: range is where slope remains distinguishable."""
    radius, slope, reference = map(lambda x: np.asarray(x, dtype=float),
                                   (radius, slope, reference))
    if not (radius.shape == slope.shape == reference.shape):
        raise ValueError("radius, slope, and reference samples must match")
    visible = np.abs(slope - reference) >= threshold
    return 0.0 if not np.any(visible) else float(np.max(radius[visible]))


def rotation_differentials(state: PlanetaryDisplacementState) -> dict[str, float]:
    rotations = state.point.rotations
    path_rotation = state.path.rotation
    return {
        "core_mantle": float(np.linalg.norm(rotations.core - rotations.mantle)),
        "matter_em": float(np.linalg.norm(rotations.body - rotations.em)),
        "point_field": float(np.linalg.norm(rotations.body - rotations.field)),
        "spin_path": float(np.linalg.norm(rotations.body - path_rotation)),
    }


def shear_measure(rotations: list[np.ndarray], damping: np.ndarray) -> float:
    """Updated 40: H_shear = sum gamma_ab |DeltaOmega_ab|^2."""
    damping = np.asarray(damping, dtype=float)
    expected = len(rotations) * (len(rotations) - 1) // 2
    if damping.shape != (expected,) or np.any(damping < 0):
        raise ValueError("one nonnegative damping value is required per rotation pair")
    value, index = 0.0, 0
    for i in range(len(rotations)):
        for j in range(i + 1, len(rotations)):
            delta = np.asarray(rotations[i]) - np.asarray(rotations[j])
            value += float(damping[index] * (delta @ delta))
            index += 1
    return value


def em_shell_modifier(base_stiffness: float, coupling: float, eta: float) -> float:
    """Updated 39/41 K_eff = K0 [1 + eta C], with C supplied by its model."""
    return float(base_stiffness * (1.0 + eta * coupling))


def make_receipt(state: PlanetaryDisplacementState, neighbor_slopes: np.ndarray,
                 overlap_weights: np.ndarray, shear_damping: np.ndarray) -> DisplacementReceipt:
    local, differential = local_reference_slope(
        neighbor_slopes, overlap_weights, state.field.reference_slope
    )
    diffs = rotation_differentials(state)
    r = state.point.rotations
    shear = shear_measure([r.core, r.fluid, r.mantle, r.body, r.em], shear_damping)
    return DisplacementReceipt(
        name=state.name,
        local_slope=local,
        reference_slope=state.field.reference_slope,
        slope_differential=differential,
        active_range=state.field.active_range,
        path_rotation=tuple(float(x) for x in state.path.rotation),
        core_mantle_differential=diffs["core_mantle"],
        matter_em_differential=diffs["matter_em"],
        point_field_differential=diffs["point_field"],
        spin_path_differential=diffs["spin_path"],
        shear_measure=shear,
        overlap_count=int(np.count_nonzero(overlap_weights)),
        ppf_norm=float(np.linalg.norm(state.recursive.as_array())),
    )
