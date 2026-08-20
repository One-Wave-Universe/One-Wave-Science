"""Canonical five-state / scale kernel for Field branch 05."""

from __future__ import annotations

from enum import IntEnum


class ScaleState(IntEnum):
    MICRO_FLOOR = 0
    SMALL_LOW = 25
    MEDIUM_MID = 50
    LARGE_HIGH = 75
    MACRO_EXTREME = 100


_MIN_INTENSITY = 0.0
_MAX_INTENSITY = 100.0


def validate_intensity(value: float) -> float:
    """Return a normalized numeric intensity inside the canonical 0..100 range."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("intensity must be numeric")
    numeric = float(value)
    if numeric < _MIN_INTENSITY or numeric > _MAX_INTENSITY:
        raise ValueError("intensity must be between 0 and 100 inclusive")
    return numeric


def state_from_intensity(value: float) -> ScaleState:
    """Map intensity deterministically to the nearest canonical 25-point state anchor."""
    numeric = validate_intensity(value)
    anchors = tuple(ScaleState)
    return min(anchors, key=lambda state: (abs(numeric - int(state)), int(state)))


def anchor_for_state(state: ScaleState) -> int:
    """Return the exact canonical numeric anchor for a scale state."""
    return int(ScaleState(state))
