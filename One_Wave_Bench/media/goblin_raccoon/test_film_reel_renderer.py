from PIL import Image

from One_Wave_Bench.media.goblin_raccoon.film_reel import (
    AudioTrack,
    Exposure,
    FilmProject,
    PerspectiveGrid,
)
from One_Wave_Bench.media.goblin_raccoon.film_reel_renderer import (
    _audio_filter,
    _render_frame,
)


def _opaque_sprite(width=10, height=20):
    return Image.new("RGBA", (width, height), (255, 0, 0, 255))


def test_renderer_uses_ground_contact_as_bottom_anchor():
    project = FilmProject(
        fps=24,
        background_width=100,
        background_height=100,
        fallback_duration_ms=100,
        grid=PerspectiveGrid(horizon_y=0.0, horizon_scale=1.0, front_scale=1.0),
        exposures=[Exposure("gr", 0, 1, x=0.5, ground_y=0.8)],
    )
    background = Image.new("RGB", (100, 100), (0, 0, 0))
    rendered = _render_frame(project, background, {"gr": _opaque_sprite()}, 0, 0.20)

    # 20px-tall rendered actor has feet at y=80, therefore occupies y=60..79.
    assert rendered.getpixel((50, 79)) == (255, 0, 0)
    assert rendered.getpixel((50, 80)) == (0, 0, 0)
    assert rendered.getpixel((50, 59)) == (0, 0, 0)


def test_renderer_depth_scaling_changes_height_not_ground_point():
    project = FilmProject(
        fps=24,
        background_width=100,
        background_height=100,
        fallback_duration_ms=100,
        grid=PerspectiveGrid(horizon_y=0.40, horizon_scale=0.25, front_scale=1.0),
        exposures=[
            Exposure("gr", 0, 1, x=0.25, ground_y=1.0),
            Exposure("gr", 1, 1, x=0.75, ground_y=0.40),
        ],
    )
    background = Image.new("RGB", (100, 100), (0, 0, 0))
    assets = {"gr": _opaque_sprite()}
    near = _render_frame(project, background, assets, 0, 0.40)
    far = _render_frame(project, background, assets, 1, 0.40)

    # Near actor: 40px tall, feet at scene bottom.
    assert near.getpixel((25, 99)) == (255, 0, 0)
    assert near.getpixel((25, 59)) == (0, 0, 0)
    # Far actor: 10px tall, feet at y=40.
    assert far.getpixel((75, 39)) == (255, 0, 0)
    assert far.getpixel((75, 40)) == (0, 0, 0)
    assert far.getpixel((75, 29)) == (0, 0, 0)


def test_audio_filter_keeps_tracks_independent_before_mix():
    project = FilmProject(
        audio=[
            AudioTrack("music", "m.wav", 1000, gain=0.25),
            AudioTrack("ambience", "a.wav", 1000, gain=0.50, start_ms=125),
            AudioTrack("dialogue", "d.wav", 1000, gain=1.00, start_ms=500),
        ]
    )
    expression, output = _audio_filter(
        project,
        [(1, 0.25, 0), (2, 0.50, 125), (3, 1.00, 500)],
    )
    assert output == "[aout]"
    assert "[1:a]adelay=0|0,volume=0.250000[a0]" in expression
    assert "[2:a]adelay=125|125,volume=0.500000[a1]" in expression
    assert "[3:a]adelay=500|500,volume=1.000000[a2]" in expression
    assert "amix=inputs=3:duration=longest:normalize=0[aout]" in expression
