import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scene_model import BackgroundLayer, CharacterLayer, Scene  # noqa: E402


def test_round_trip_with_background_and_characters(tmp_path):
    bg_path = tmp_path / "bg.png"
    bg_path.write_bytes(b"fake-png-bytes")
    char_path = tmp_path / "char.png"
    char_path.write_bytes(b"fake-png-bytes")

    scene = Scene(
        canvas_width=800,
        canvas_height=450,
        background=BackgroundLayer(path=str(bg_path), width=800, height=450),
        characters=[
            CharacterLayer(path=str(char_path), x=10.5, y=20.25, width=100, height=160, z=1),
            CharacterLayer(path=str(char_path), x=50, y=60, width=80, height=128, z=2),
        ],
    )

    scene_file = tmp_path / "scene.owascene"
    scene.save(str(scene_file))
    loaded = Scene.load(str(scene_file))

    assert loaded.canvas_width == 800
    assert loaded.canvas_height == 450
    assert loaded.background is not None
    assert os.path.abspath(loaded.background.path) == os.path.abspath(str(bg_path))
    assert loaded.background.width == 800
    assert loaded.background.height == 450

    assert len(loaded.characters) == 2
    first, second = sorted(loaded.characters, key=lambda c: c.z)
    assert first.x == 10.5
    assert first.y == 20.25
    assert first.width == 100
    assert first.height == 160
    assert first.z == 1
    assert second.z == 2
    assert os.path.abspath(first.path) == os.path.abspath(str(char_path))


def test_paths_are_stored_relative_to_scene_file(tmp_path):
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    bg_path = assets_dir / "bg.png"
    bg_path.write_bytes(b"fake-png-bytes")

    scene = Scene(background=BackgroundLayer(path=str(bg_path), width=100, height=100))
    scene_file = tmp_path / "scene.owascene"
    scene.save(str(scene_file))

    raw = scene_file.read_text()
    assert "assets/bg.png" in raw
    assert str(tmp_path) not in raw  # no leftover absolute path baked in

    loaded = Scene.load(str(scene_file))
    assert os.path.abspath(loaded.background.path) == os.path.abspath(str(bg_path))


def test_empty_scene_round_trip(tmp_path):
    scene = Scene()
    scene_file = tmp_path / "empty.owascene"
    scene.save(str(scene_file))
    loaded = Scene.load(str(scene_file))

    assert loaded.background is None
    assert loaded.characters == []
    assert loaded.canvas_width == scene.canvas_width
    assert loaded.canvas_height == scene.canvas_height
