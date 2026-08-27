"""Independent Ground, center, movement, and coherent-Hold measurements.

Logical Ground means no committed binary relation plus sub-threshold resolved
activity.  It is not a claim that the physical Field or vacuum contains zero
energy.  Center residence, zero net movement, phase lock, and retained
structure are deliberately separate observables.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from mirror_operator import PhaseState, at_shared_center, classify_move
from six_route_logic import BinaryChoice, LogicRoute, TernaryMove


@dataclass(frozen=True)
class HoldThresholds:
    center_band: float = 1e-3
    speed_band: float = 1e-3
    ground_amplitude_max: float = 1e-3
    ground_energy_max: float = 1e-6
    phase_lock_min: float = 0.90
    retained_energy_min: float = 0.05
    topology_min: float = 0.90

    def __post_init__(self) -> None:
        nonnegative = (
            self.center_band,
            self.speed_band,
            self.ground_amplitude_max,
            self.ground_energy_max,
            self.retained_energy_min,
        )
        if any(value < 0.0 for value in nonnegative):
            raise ValueError("bands and energy thresholds must be nonnegative")
        if not 0.0 <= self.phase_lock_min <= 1.0:
            raise ValueError("phase_lock_min must be in [0,1]")
        if not 0.0 <= self.topology_min <= 1.0:
            raise ValueError("topology_min must be in [0,1]")


@dataclass(frozen=True)
class PresenceSample:
    oscillator: PhaseState
    choice: Optional[BinaryChoice]
    stored_energy: float
    phase_lock: float
    topology_retention: float

    def __post_init__(self) -> None:
        if self.stored_energy < 0.0:
            raise ValueError("stored_energy must be nonnegative")
        if not 0.0 <= self.phase_lock <= 1.0:
            raise ValueError("phase_lock must be in [0,1]")
        if not 0.0 <= self.topology_retention <= 1.0:
            raise ValueError("topology_retention must be in [0,1]")


@dataclass(frozen=True)
class PresenceReceipt:
    logical_ground: bool
    at_center: bool
    movement: TernaryMove
    binary_relation: Optional[str]
    route: Optional[LogicRoute]
    phase_locked: bool
    energy_retained: bool
    topology_retained: bool
    coherent_hold: bool
    turning_point_hold: bool
    center_crossing: bool


def classify_presence(
    sample: PresenceSample,
    thresholds: HoldThresholds = HoldThresholds(),
) -> PresenceReceipt:
    movement = classify_move(sample.oscillator, thresholds.speed_band)
    center = at_shared_center(sample.oscillator, thresholds.center_band)
    phase_locked = sample.phase_lock >= thresholds.phase_lock_min
    energy_retained = sample.stored_energy >= thresholds.retained_energy_min
    topology_retained = sample.topology_retention >= thresholds.topology_min

    logical_ground = (
        sample.choice is None
        and sample.oscillator.amplitude <= thresholds.ground_amplitude_max
        and sample.stored_energy <= thresholds.ground_energy_max
    )
    route = LogicRoute(sample.choice, movement) if sample.choice is not None else None
    coherent_hold = (
        sample.choice is not None
        and movement is TernaryMove.HOLD
        and phase_locked
        and energy_retained
        and topology_retained
    )
    turning_point_hold = movement is TernaryMove.HOLD and not center
    center_crossing = center and movement is not TernaryMove.HOLD

    return PresenceReceipt(
        logical_ground=logical_ground,
        at_center=center,
        movement=movement,
        binary_relation=sample.choice.name if sample.choice is not None else None,
        route=route,
        phase_locked=phase_locked,
        energy_retained=energy_retained,
        topology_retained=topology_retained,
        coherent_hold=coherent_hold,
        turning_point_hold=turning_point_hold,
        center_crossing=center_crossing,
    )

