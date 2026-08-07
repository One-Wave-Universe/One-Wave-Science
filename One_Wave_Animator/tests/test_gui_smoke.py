"""GUI smoke test: exercises the whole Step 1 workflow (import, drag,
resize, reorder, delete, save, reopen) against real Qt objects, run
headlessly via the 'offscreen' platform plugin."""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PySide6 = pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication  # noqa: E402

from app.main_window import MainWindow  # noqa: E402
from app.scene_model import Scene  # noqa: E402

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sample")
BACKGROUND_PNG = os.path.join(ASSETS_DIR, "sample_background.png")
CHARACTER_PNG = os.path.join(ASSETS_DIR, "sample_character.png")


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication(sys.argv)


def test_full_workflow(app, tmp_path):
    window = MainWindow()
    canvas = window.canvas

    # Import background: canvas resizes to the image's native size.
    canvas.set_background(BACKGROUND_PNG)
    assert canvas.has_background()
    assert canvas.canvas_size() == (800.0, 450.0)

    # Import two characters.
    char_a = canvas.add_character(CHARACTER_PNG)
    char_b = canvas.add_character(CHARACTER_PNG)
    assert set(canvas.character_items()) == {char_a, char_b}
    assert char_b.zValue() > char_a.zValue()

    # Drag: moving is just setting position, exercised directly (mouse
    # delivery isn't meaningful under the offscreen platform).
    char_a.setPos(120, 80)
    assert char_a.pos().x() == 120
    assert char_a.pos().y() == 80

    # Resize preserves aspect ratio.
    orig_w, orig_h = char_a.size()
    aspect = orig_w / orig_h
    char_a.set_size(orig_w * 2, orig_h * 2)
    new_w, new_h = char_a.size()
    assert new_w == pytest.approx(orig_w * 2)
    assert abs((new_w / new_h) - aspect) < 1e-6

    # Layer order: char_b starts above char_a; move char_a to the top.
    assert canvas.layers_top_to_bottom() == [char_b, char_a]
    canvas.move_layer_up(char_a)
    assert canvas.layers_top_to_bottom() == [char_a, char_b]

    # Delete one character.
    canvas.delete_character(char_b)
    assert canvas.character_items() == [char_a]

    # Save the scene, reload it into a fresh window, and confirm it
    # comes back exactly as saved.
    # Bypass the (blocking, dialog-driven) save_scene()/save_scene_as() UI
    # entry points and write directly, the way they do once a path is known.
    scene_file = str(tmp_path / "scene.owascene")
    assert window._write_scene(scene_file) is True

    reloaded_scene = Scene.load(scene_file)
    assert reloaded_scene.canvas_width == 800
    assert reloaded_scene.canvas_height == 450
    assert reloaded_scene.background is not None
    assert len(reloaded_scene.characters) == 1
    restored = reloaded_scene.characters[0]
    assert restored.x == 120
    assert restored.y == 80
    assert restored.width == pytest.approx(new_w)
    assert restored.height == pytest.approx(new_h)

    window2 = MainWindow()
    warnings = window2.canvas.load_scene_model(reloaded_scene)
    assert warnings == []
    assert window2.canvas.has_background()
    reloaded_items = window2.canvas.character_items()
    assert len(reloaded_items) == 1
    assert reloaded_items[0].pos().x() == 120
    assert reloaded_items[0].pos().y() == 80
    assert reloaded_items[0].size() == pytest.approx((new_w, new_h))
