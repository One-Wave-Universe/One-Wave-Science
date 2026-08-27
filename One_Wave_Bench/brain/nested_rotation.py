"""Declared Point-Path-Field nesting and threshold/season cycles.

This is an executable state schema. It does not claim that the named quantum,
electric, quark-vortex, or proton-knot carriers have already been physically
derived or validated by this program.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite, tau


class RotationLevel(str, Enum):
    POINT = "Point"
    PATH = "Path"
    FIELD = "Field"


class Season(str, Enum):
    SPRING = "Spring/Birth"
    SUMMER = "Summer/Life"
    FALL = "Fall/Decline"
    WINTER = "Winter/Death"

    @property
    def next(self) -> "Season":
        cycle = tuple(Season)
        return cycle[(cycle.index(self) + 1) % len(cycle)]


class Carrier(str, Enum):
    QUANTUM_MAGNETIC = "Quantum magnetic"
    ELECTRIC = "Electric"
    QUARK_VORTEX = "Quark vortex"
    PROTON_KNOT = "Proton knot"


@dataclass(frozen=True, slots=True)
class ThresholdBand:
    high: float
    low: float

    def contains(self, value: float) -> bool:
        return self.low <= value <= self.high


THRESHOLD_BANDS = (
    ThresholdBand(100, 90),
    ThresholdBand(85, 75),
    ThresholdBand(70, 60),
    ThresholdBand(55, 45),
    ThresholdBand(40, 30),
    ThresholdBand(25, 15),
    ThresholdBand(15, 0),
)


def threshold_bands_for(value: float) -> tuple[int, ...]:
    """Return one-based matching bands; 15 intentionally returns (6, 7)."""

    if not isfinite(value) or not 0 <= value <= 100:
        raise ValueError("threshold value must be finite and in [0,100]")
    return tuple(
        index
        for index, band in enumerate(THRESHOLD_BANDS, start=1)
        if band.contains(value)
    )


@dataclass(frozen=True, slots=True)
class NestedRotationReceipt:
    """One carrier with simultaneous Point, Path, and Field phase receipts."""

    carrier: Carrier
    point_phase: float
    path_phase: float
    field_phase: float
    threshold: float
    season: Season
    contained: tuple["NestedRotationReceipt", ...] = ()

    def __post_init__(self) -> None:
        phases = (self.point_phase, self.path_phase, self.field_phase)
        if not all(isfinite(phase) and 0 <= phase < tau for phase in phases):
            raise ValueError("rotation phases must be finite and in [0,tau)")
        if not threshold_bands_for(self.threshold):
            raise ValueError("threshold falls in an undeclared gap")
        order = tuple(Carrier)
        parent_index = order.index(self.carrier)
        if any(order.index(child.carrier) >= parent_index for child in self.contained):
            raise ValueError("contained rotation must be from a smaller carrier layer")

    @property
    def phases(self) -> dict[RotationLevel, float]:
        return {
            RotationLevel.POINT: self.point_phase,
            RotationLevel.PATH: self.path_phase,
            RotationLevel.FIELD: self.field_phase,
        }
