"""Declared field encoding for normalized reconstructed collider events.

The initial implementation intentionally builds a sparse observable field. It does not
assign unmeasured phase, invent a trajectory, or identify a representation with a
physical mechanism.
"""

from __future__ import annotations

from typing import Any, Mapping


def cern_event_to_wave(
    observation: Mapping[str, Any],
    *,
    observation_id: str,
    parameters: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Encode source-defined reconstructed objects into a sparse event field.

    Object dictionaries are retained unchanged, so source-defined fields and their
    meanings remain inspectable. A gridded kernel projection belongs in a later,
    separately validated transform revision.
    """
    if observation.get("observation_kind") != "collider_reconstructed_event":
        raise ValueError("expected collider_reconstructed_event observation")

    return {
        "schema_version": "wave-state-v1",
        "status": "ENCODED",
        "source_observation_id": observation_id,
        "transform": {
            "name": "cern_event_to_wave",
            "version": "0.1.0",
            "mode": "representation",
            "parameters": {"encoding": "sparse_reconstructed_object_field", **dict(parameters or {})},
            "assumptions": ["Each input object retains its source-defined reconstruction semantics.", "No physical phase or continuous trajectory is inferred by this encoding."],
        },
        "field": {
            "domain": "reconstructed_event_object_space",
            "components": {"objects": observation["observables"]["objects"], "coordinates": observation["coordinates"]},
            "units": observation["units"],
            "lossiness": "lossless",
        },
        "validation": {"status": "NOT_YET_TESTED", "required_baselines": ["source_standard_representation", "task_specific_conventional_baseline"]},
    }
