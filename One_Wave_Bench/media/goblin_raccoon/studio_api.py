"""Deterministic action API shared by human controls and AI directors.

An LLM should translate natural-language requests into these small actions.  The
renderer never needs to know which provider produced them, and a human UI can
call the exact same functions directly.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable, Mapping

from .film_reel import AudioTrack, Exposure, FilmProject, PerspectiveGrid


class StudioActionError(ValueError):
    pass


def _require(action: Mapping[str, Any], key: str) -> Any:
    if key not in action:
        raise StudioActionError(f"{action.get('type', 'action')} requires {key!r}")
    return action[key]


def apply_action(project: FilmProject, action: Mapping[str, Any]) -> dict[str, Any]:
    """Apply one validated state change and return a compact receipt."""
    kind = str(_require(action, "type"))

    if kind == "set_grid":
        allowed = {"horizon_y", "vanishing_x", "horizon_scale", "front_scale"}
        patch = {key: float(value) for key, value in action.items() if key in allowed}
        if not patch:
            raise StudioActionError("set_grid needs at least one grid value")
        project.grid = replace(project.grid, **patch)
        return {"type": kind, "grid": project.to_dict()["grid"]}

    if kind == "place_exposure":
        asset_id = str(_require(action, "asset_id"))
        start_ms = int(_require(action, "start_ms"))
        fps = max(1, int(project.fps))
        start_frame = max(0, round(start_ms * fps / 1000))
        exposure = Exposure(
            asset_id=asset_id,
            start_frame=start_frame,
            hold_frames=max(1, int(action.get("hold_frames", 1))),
            x=float(action.get("x", 0.50)),
            ground_y=float(action.get("ground_y", 0.82)),
            rotation_deg=float(action.get("rotation_deg", 0.0)),
            layer=int(action.get("layer", 0)),
        )
        project.exposures.append(exposure)
        return {"type": kind, "exposure": exposure.__dict__.copy()}

    if kind == "lay_sequence":
        asset_ids = [str(value) for value in _require(action, "asset_ids")]
        placed = project.lay_sequence(
            asset_ids,
            start_ms=int(_require(action, "start_ms")),
            end_ms=int(_require(action, "end_ms")),
            x=float(action.get("x", 0.50)),
            ground_y=float(action.get("ground_y", 0.82)),
            layer=int(action.get("layer", 0)),
        )
        return {
            "type": kind,
            "placed": len(placed),
            "exposures": [item.__dict__.copy() for item in placed],
        }

    if kind == "set_audio_gain":
        track_kind = str(_require(action, "track"))
        gain = max(0.0, float(_require(action, "gain")))
        changed = 0
        replaced_tracks: list[AudioTrack] = []
        for track in project.audio:
            if track.kind == track_kind:
                replaced_tracks.append(replace(track, gain=gain))
                changed += 1
            else:
                replaced_tracks.append(track)
        if not changed:
            raise StudioActionError(f"no loaded audio track named {track_kind!r}")
        project.audio = replaced_tracks
        return {"type": kind, "track": track_kind, "gain": gain, "changed": changed}

    if kind == "move_exposure":
        index = int(_require(action, "index"))
        try:
            current = project.sorted_exposures()[index]
        except IndexError as exc:
            raise StudioActionError(f"exposure index {index} does not exist") from exc
        updated = replace(
            current,
            x=float(action.get("x", current.x)),
            ground_y=float(action.get("ground_y", current.ground_y)),
            rotation_deg=float(action.get("rotation_deg", current.rotation_deg)),
        )
        original_index = project.exposures.index(current)
        project.exposures[original_index] = updated
        return {"type": kind, "index": index, "exposure": updated.__dict__.copy()}

    if kind == "delete_exposure":
        index = int(_require(action, "index"))
        ordered = project.sorted_exposures()
        try:
            victim = ordered[index]
        except IndexError as exc:
            raise StudioActionError(f"exposure index {index} does not exist") from exc
        project.exposures.remove(victim)
        return {"type": kind, "index": index, "deleted": victim.__dict__.copy()}

    raise StudioActionError(f"unknown studio action {kind!r}")


def apply_actions(
    project: FilmProject, actions: Iterable[Mapping[str, Any]]
) -> dict[str, Any]:
    """Apply an ordered action list and return receipts plus final project state."""
    receipts = [apply_action(project, action) for action in actions]
    return {"receipts": receipts, "project": project.to_dict()}


def action_schema() -> dict[str, Any]:
    """Small provider-neutral contract suitable for an LLM tool/function call."""
    return {
        "actions": [
            {"type": "set_grid", "horizon_y": 0.38, "vanishing_x": 0.50},
            {
                "type": "place_exposure",
                "asset_id": "gr_pose_001",
                "start_ms": 3200,
                "hold_frames": 3,
                "x": 0.45,
                "ground_y": 0.80,
            },
            {
                "type": "lay_sequence",
                "asset_ids": ["gr_walk_001", "gr_walk_002", "gr_walk_003"],
                "start_ms": 3200,
                "end_ms": 5000,
            },
            {"type": "set_audio_gain", "track": "ambience", "gain": 0.55},
            {"type": "move_exposure", "index": 0, "x": 0.52, "ground_y": 0.76},
            {"type": "delete_exposure", "index": 0},
        ]
    }
