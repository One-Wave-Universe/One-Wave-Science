"""Input calibration profiles (Section 4.2).

The program must not label a signal in volts or SPL unless a valid
calibration profile is active for that device/channel -- everything here
defaults to dBFS/normalized amplitude, and the volts/SPL conversions
below refuse to run without an explicit CalibrationProfile.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

import numpy as np


class ReferenceSignalType(Enum):
    VOLTAGE = "voltage"
    SPL = "spl"


@dataclass
class CalibrationProfile:
    device_id: str
    driver_type: str
    input_channel: int
    sample_rate: int
    interface_gain_setting: str
    reference_signal: str
    reference_voltage_or_spl: float
    measured_digital_rms: float
    conversion_factor: float
    calibration_date: str
    notes: str = ""

    @classmethod
    def create(cls, device_id: str, driver_type: str, input_channel: int, sample_rate: int,
               interface_gain_setting: str, reference_signal: ReferenceSignalType,
               reference_voltage_or_spl: float, measured_digital_rms: float,
               notes: str = "") -> "CalibrationProfile":
        """Derive conversion_factor from a reference signal of known physical
        level and its measured digital RMS (Section 4.2)."""
        if measured_digital_rms <= 0:
            raise ValueError("measured_digital_rms must be positive to calibrate")

        conversion_factor = reference_voltage_or_spl / measured_digital_rms

        return cls(
            device_id=device_id,
            driver_type=driver_type,
            input_channel=input_channel,
            sample_rate=sample_rate,
            interface_gain_setting=interface_gain_setting,
            reference_signal=reference_signal.value,
            reference_voltage_or_spl=reference_voltage_or_spl,
            measured_digital_rms=measured_digital_rms,
            conversion_factor=conversion_factor,
            calibration_date=datetime.now(timezone.utc).isoformat(),
            notes=notes,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str | Path) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str | Path) -> "CalibrationProfile":
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

    def digital_amplitude_to_physical(self, digital_amplitude: float) -> float:
        """Convert a normalized digital amplitude (-1..1) to volts or SPL,
        per this profile's reference_signal type."""
        return digital_amplitude * self.conversion_factor

    def digital_rms_to_physical(self, digital_rms: float) -> float:
        return digital_rms * self.conversion_factor


def dbfs(digital_amplitude: float, full_scale: float = 1.0) -> float:
    """Digital full-scale amplitude in dBFS -- always available, no calibration needed."""
    return float(20 * np.log10(max(abs(digital_amplitude), 1e-12) / full_scale))


def dbfs_array(signal: np.ndarray, full_scale: float = 1.0) -> np.ndarray:
    return 20 * np.log10(np.maximum(np.abs(signal), 1e-12) / full_scale)


def to_volts(digital_amplitude: float, profile: CalibrationProfile | None) -> float:
    if profile is None:
        raise ValueError(
            "no active calibration profile: cannot label this channel in volts. "
            "Display dBFS instead until CalibrationProfile.create(...) has been run."
        )
    if profile.reference_signal != ReferenceSignalType.VOLTAGE.value:
        raise ValueError(
            f"calibration profile for device {profile.device_id!r} channel "
            f"{profile.input_channel} was calibrated against "
            f"{profile.reference_signal!r}, not voltage"
        )
    return profile.digital_amplitude_to_physical(digital_amplitude)


def to_spl(digital_amplitude: float, profile: CalibrationProfile | None) -> float:
    if profile is None:
        raise ValueError(
            "no active calibration profile: cannot label this channel in SPL. "
            "Display dBFS instead until CalibrationProfile.create(...) has been run."
        )
    if profile.reference_signal != ReferenceSignalType.SPL.value:
        raise ValueError(
            f"calibration profile for device {profile.device_id!r} channel "
            f"{profile.input_channel} was calibrated against "
            f"{profile.reference_signal!r}, not SPL"
        )
    return profile.digital_amplitude_to_physical(digital_amplitude)
