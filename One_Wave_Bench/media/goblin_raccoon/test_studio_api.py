import pytest

from One_Wave_Bench.media.goblin_raccoon.film_reel import AudioTrack, FilmProject
from One_Wave_Bench.media.goblin_raccoon.studio_api import (
    StudioActionError,
    action_schema,
    apply_action,
    apply_actions,
)


def test_human_and_ai_grid_action_changes_same_project_state():
    project = FilmProject()
    receipt = apply_action(
        project,
        {"type": "set_grid", "horizon_y": 0.31, "vanishing_x": 0.62},
    )
    assert project.grid.horizon_y == 0.31
    assert project.grid.vanishing_x == 0.62
    assert receipt["grid"]["horizon_y"] == 0.31


def test_place_exposure_uses_milliseconds_and_film_frames():
    project = FilmProject(fps=24, fallback_duration_ms=10_000)
    receipt = apply_action(
        project,
        {
            "type": "place_exposure",
            "asset_id": "gr-look",
            "start_ms": 3250,
            "hold_frames": 4,
            "x": 0.42,
            "ground_y": 0.77,
        },
    )
    exposure = project.exposures[0]
    assert exposure.start_frame == 78
    assert exposure.hold_frames == 4
    assert receipt["exposure"]["asset_id"] == "gr-look"


def test_lay_sequence_is_same_deterministic_operation_for_agent_or_button():
    project = FilmProject(fps=24, fallback_duration_ms=4_000)
    receipt = apply_action(
        project,
        {
            "type": "lay_sequence",
            "asset_ids": ["a", "b", "c", "d"],
            "start_ms": 1000,
            "end_ms": 2000,
            "x": 0.6,
            "ground_y": 0.7,
        },
    )
    assert receipt["placed"] == 4
    assert [item.start_frame for item in project.exposures] == [24, 30, 36, 42]
    assert all(item.hold_frames == 6 for item in project.exposures)


def test_manual_audio_gain_action_keeps_other_tracks_unchanged():
    project = FilmProject(
        audio=[
            AudioTrack("music", "m.wav", 1000, gain=0.3),
            AudioTrack("ambience", "a.wav", 1000, gain=0.4),
        ]
    )
    apply_action(project, {"type": "set_audio_gain", "track": "ambience", "gain": 0.7})
    assert project.audio[0].gain == 0.3
    assert project.audio[1].gain == 0.7


def test_move_exposure_changes_ground_position_not_art_identity():
    project = FilmProject(fps=24, fallback_duration_ms=2000)
    apply_action(project, {"type": "place_exposure", "asset_id": "locked-gr-art", "start_ms": 0})
    apply_action(project, {"type": "move_exposure", "index": 0, "x": 0.7, "ground_y": 0.55})
    exposure = project.exposures[0]
    assert exposure.asset_id == "locked-gr-art"
    assert exposure.x == 0.7
    assert exposure.ground_y == 0.55


def test_apply_actions_returns_receipts_and_final_state():
    project = FilmProject(fps=24, fallback_duration_ms=1000)
    result = apply_actions(
        project,
        [
            {"type": "set_grid", "horizon_y": 0.4},
            {"type": "place_exposure", "asset_id": "gr", "start_ms": 0},
        ],
    )
    assert len(result["receipts"]) == 2
    assert result["project"]["grid"]["horizon_y"] == 0.4
    assert result["project"]["exposures"][0]["asset_id"] == "gr"


def test_bad_action_fails_loudly_instead_of_guessing():
    with pytest.raises(StudioActionError):
        apply_action(FilmProject(), {"type": "make_gr_cuter"})


def test_action_schema_exposes_supported_operations():
    types = {item["type"] for item in action_schema()["actions"]}
    assert {"set_grid", "place_exposure", "lay_sequence", "set_audio_gain"} <= types
