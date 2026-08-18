from One_Wave_Bench.media.goblin_raccoon.film_reel import (
    AudioTrack,
    Exposure,
    FilmProject,
    PerspectiveGrid,
    lay_art_sequence,
    project_from_dict,
)


def test_audio_owns_project_duration():
    project = FilmProject(
        fallback_duration_ms=99_000,
        audio=[
            AudioTrack("music", "music.wav", duration_ms=8_000),
            AudioTrack("ambience", "wind.wav", duration_ms=12_000),
            AudioTrack("dialogue", "line.wav", duration_ms=2_000, start_ms=3_000),
        ],
    )
    assert project.duration_ms == 12_000
    assert project.frame_count == 288


def test_no_audio_uses_fallback_duration():
    project = FilmProject(fps=24, fallback_duration_ms=2_500)
    assert project.duration_ms == 2_500
    assert project.frame_count == 60


def test_perspective_scale_uses_ground_contact():
    grid = PerspectiveGrid(
        horizon_y=0.40, horizon_scale=0.20, front_scale=1.00
    )
    assert grid.scale_at(0.40) == 0.20
    assert grid.scale_at(0.0) == 0.20
    assert grid.scale_at(1.0) == 1.00
    mid = grid.scale_at(0.70)
    assert 0.20 < mid < 1.00


def test_horizontal_motion_at_same_depth_keeps_scale():
    project = FilmProject(
        fps=24,
        fallback_duration_ms=1_000,
        exposures=[
            Exposure("a", 0, 1, x=0.20, ground_y=0.75),
            Exposure("b", 1, 1, x=0.80, ground_y=0.75),
        ],
    )
    assert project.resolve_frame(0).scale == project.resolve_frame(1).scale


def test_moving_toward_horizon_shrinks_actor():
    project = FilmProject(
        fps=24,
        fallback_duration_ms=1_000,
        exposures=[
            Exposure("near", 0, 1, ground_y=0.90),
            Exposure("far", 1, 1, ground_y=0.50),
        ],
    )
    assert project.resolve_frame(1).scale < project.resolve_frame(0).scale


def test_exposure_is_discrete_not_tweened():
    project = FilmProject(
        fps=24,
        fallback_duration_ms=1_000,
        exposures=[Exposure("pose-a", 3, 4, x=0.2, ground_y=0.8)],
    )
    assert project.resolve_frame(2).asset_id is None
    for frame in range(3, 7):
        resolved = project.resolve_frame(frame)
        assert resolved.asset_id == "pose-a"
        assert resolved.x == 0.2
    assert project.resolve_frame(7).asset_id is None


def test_lay_sequence_distributes_drawings_across_time():
    project = FilmProject(fps=24, fallback_duration_ms=2_000)
    placed = lay_art_sequence(
        project,
        ["a", "b", "c", "d"],
        start_ms=500,
        end_ms=1_500,
        x=0.55,
        ground_y=0.70,
    )
    assert len(placed) == 4
    assert placed[0].start_frame == 12
    assert placed[-1].end_frame == 36
    assert sum(item.hold_frames for item in placed) == 24
    assert all(item.x == 0.55 for item in placed)
    assert all(item.ground_y == 0.70 for item in placed)


def test_lay_sequence_never_puts_more_drawings_than_slots():
    project = FilmProject(fps=10, fallback_duration_ms=1_000)
    placed = project.lay_sequence(
        [str(index) for index in range(20)], start_ms=0, end_ms=500
    )
    assert len(placed) == 5
    assert all(item.hold_frames == 1 for item in placed)


def test_project_round_trip_keeps_shared_human_ai_state():
    project = FilmProject(
        fps=24,
        background="forest.png",
        background_width=1920,
        background_height=1080,
        grid=PerspectiveGrid(horizon_y=0.33, vanishing_x=0.61),
        audio=[AudioTrack("ambience", "birds.wav", 3_000, gain=0.4)],
        exposures=[Exposure("gr-look", 4, 3, x=0.45, ground_y=0.72)],
    )
    restored = project_from_dict(project.to_dict())
    assert restored.fps == 24
    assert restored.background == "forest.png"
    assert restored.background_width == 1920
    assert restored.grid.horizon_y == 0.33
    assert restored.audio[0].gain == 0.4
    assert restored.exposures[0].asset_id == "gr-look"
