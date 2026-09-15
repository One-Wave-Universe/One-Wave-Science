"""LIGO normalization boundary.

This module deliberately accepts already acquired data. Retrieval and calibration choices
are recorded in the source manifest rather than hidden inside a transform.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def normalize_ligo_observation(
    *,
    source: Mapping[str, Any],
    detector: str,
    gps_start: float,
    sample_rate_hz: float,
    strain: Sequence[float],
    units: str = "dimensionless strain",
    data_quality: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a source-preserving NormalizedObservation for calibrated strain.

    No filtering, whitening, gating, interpolation, or physical inference occurs here.
    Those operations belong to versioned transforms and must be declared separately.
    """
    if not detector:
        raise ValueError("detector is required")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    if not strain:
        raise ValueError("strain cannot be empty")

    return {
        "schema_version": "normalized-observation-v1",
        "status": "NORMALIZED",
        "source": dict(source),
        "observation_kind": "gravitational_wave_strain",
        "coordinates": {
            "time_basis": "GPS",
            "gps_start": float(gps_start),
            "sample_rate_hz": float(sample_rate_hz),
            "frame": "detector",
            "detector": detector,
        },
        "units": {"amplitude": units},
        "observables": {"strain": list(strain)},
        "quality": dict(data_quality or {}),
        "normalization": {
            "software": "normalize_ligo_observation",
            "operations": [],
            "normalized_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    }
