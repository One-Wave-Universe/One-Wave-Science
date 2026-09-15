"""CERN event normalization boundary."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def normalize_cern_event(
    *,
    source: Mapping[str, Any],
    run: int | str,
    luminosity_block: int | str | None,
    event: int | str,
    objects: Sequence[Mapping[str, Any]],
    frame: str,
    momentum_unit: str,
    selection: Mapping[str, Any] | None = None,
    uncertainties: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an un-interpreted normalized collider-event record.

    Objects remain source-defined reconstructed records. Coordinate completion, wave
    encoding, and hypothesis assumptions are deferred to explicit transforms.
    """
    if run is None or event is None:
        raise ValueError("run and event identifiers are required")
    if not frame:
        raise ValueError("frame is required")
    if not momentum_unit:
        raise ValueError("momentum_unit is required")

    return {
        "schema_version": "normalized-observation-v1",
        "status": "NORMALIZED",
        "source": dict(source),
        "observation_kind": "collider_reconstructed_event",
        "coordinates": {
            "frame": frame,
            "run": str(run),
            "luminosity_block": None if luminosity_block is None else str(luminosity_block),
            "event": str(event),
        },
        "units": {"momentum": momentum_unit},
        "observables": {"objects": [dict(item) for item in objects]},
        "selection": dict(selection or {}),
        "uncertainties": dict(uncertainties or {}),
        "normalization": {
            "software": "normalize_cern_event",
            "operations": [],
            "normalized_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    }
