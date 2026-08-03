"""Acoustic wavelength (Section 1: "oscilloscope ... spectrum, resonance ...
analysis" implies the physical wave, not just its digitized frequency).

Wavelength depends on the propagation medium's speed of sound, which this
engine has no way to measure -- it defaults to the standard dry-air value
at 20C and lets the caller override it (e.g. for a different temperature,
altitude, or medium) rather than silently assuming one. This mirrors
Section 4.2's calibration discipline: don't imply a physical quantity is
known more precisely than it actually is.
"""

from __future__ import annotations

import numpy as np

SPEED_OF_SOUND_DRY_AIR_20C_MPS = 343.0


def speed_of_sound_in_air(temperature_celsius: float = 20.0) -> float:
    """v ~= 331.3 * sqrt(1 + T/273.15) m/s, the standard dry-air approximation."""
    return 331.3 * (1 + temperature_celsius / 273.15) ** 0.5


def wavelength_meters(frequency_hz: float, speed_of_sound_mps: float = SPEED_OF_SOUND_DRY_AIR_20C_MPS) -> float:
    """lambda = v / f."""
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    return speed_of_sound_mps / frequency_hz


def frequency_from_wavelength(wavelength_meters_value: float,
                               speed_of_sound_mps: float = SPEED_OF_SOUND_DRY_AIR_20C_MPS) -> float:
    """f = v / lambda."""
    if wavelength_meters_value <= 0:
        raise ValueError("wavelength_meters_value must be positive")
    return speed_of_sound_mps / wavelength_meters_value


def wave_number(frequency_hz: float, speed_of_sound_mps: float = SPEED_OF_SOUND_DRY_AIR_20C_MPS) -> float:
    """Angular wave number k = 2*pi / lambda = 2*pi*f / v (radians per meter)."""
    return 2 * np.pi * frequency_hz / speed_of_sound_mps
