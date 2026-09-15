"""Declared representation transform for normalized LIGO strain.

This module is an encoding interface, not a claim that its output establishes a new
physical ontology. It preserves the transform configuration alongside output data.
"""

from __future__ import annotations

from typing import Any, Mapping


def ligo_strain_to_wave(
    observation: Mapping[str, Any],
    *,
    observation_id: str,
    representation: str = "time_series",
    parameters: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Encode normalized strain as a WaveState without hidden conditioning.

    Supported initial representation: direct time-series preservation. More advanced
    filtering or time-frequency transforms must be added as separately versioned modes.
    """
    if observation.get("observation_kind") != "gravitational_wave_strain":
        raise ValueError("expected gravitational_wave_strain observation")
    if representation != "time_series":
        raise NotImplementedError("only direct time_series encoding is implemented")

    coords = observation["coordinates"]
    strain = observation["observables"]["strain"]
    return {
        "schema_version": "wave-state-v1",
        "status": "ENCODED",
        "source_observation_id": observation_id,
        "transform": {
            "name": "ligo_strain_to_wave",
            "version": "0.1.0",
            "mode": "representation",
            "parameters": {"representation": representation, **dict(parameters or {})},
            "assumptions": ["Input strain is an externally calibrated detector observable."],
        },
        "field": {
            "domain": "detector_time",
            "components": {"amplitude": list(strain), "gps_start": coords["gps_start"], "sample_rate_hz": coords["sample_rate_hz"], "detector": coords["detector"]},
            "units": {"amplitude": observation["units"]["amplitude"], "time": "s (GPS basis)"},
            "lossiness": "lossless",
        },
        "validation": {"status": "NOT_YET_TESTED", "required_controls": ["off_source", "time_shifted_background"]},
    }
