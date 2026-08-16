"""End-to-end test of the Animation menu's export path: background +
multiple character layers -> MainWindow.export_animation_gif's testable
half (_export_gif_to_path) -> a real GIF, verified frame-by-frame against
what was actually on the canvas for each layer."""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PIL")
PySide6 = pytest.importorskip("PySide6")

from PySide6.QtGui import QColor, QImage  # noqa: E402
from PySide6.QtWidgets import QApplication, QMessageBox  # noqa: E402
from PIL import Image  # noqa: E402

from app.main_window import MainWindow  # noqa: E402


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication(sys.argv)


def _solid_png(path, w, h, color):
    img = QImage(w, h, QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(color)
    assert img.save(path, "PNG")
    return path


def test_export_requires_background(app, tmp_path, monkeypatch):
    # export_animation_gif() shows a real blocking QMessageBox.warning() on
    # failure - correct desktop behavior, but it hangs forever under headless
    # testing with nothing to click it away. Stub it out to a no-op, the
    # standard way to test Qt code paths that pop a modal dialog.
    monkeypatch.setattr(QMessageBox, "warning", lambda *a, **k: None)
    window = MainWindow()
    assert window.export_animation_gif() is False


def test_export_requires_at_least_two_characters(app, tmp_path, monkeypatch):
    monkeypatch.setattr(QMessageBox, "warning", lambda *a, **k: None)
    window = MainWindow()
    bg = _solid_png(str(tmp_path / "bg.png"), 200, 150, QColor("gray"))
    window.canvas.set_background(bg)
    char = _solid_png(str(tmp_path / "c1.png"), 40, 40, QColor("red"))
    window.canvas.add_character(char)
    assert window.export_animation_gif() is False


def test_full_export_pipeline_frame_order_and_content(app, tmp_path):
    window = MainWindow()
    bg = _solid_png(str(tmp_path / "bg.png"), 200, 150, QColor(30, 30, 30))
    window.canvas.set_background(bg)

    # Three distinctly-colored, distinctly-positioned character layers -
    # z-order (import order here) should become frame order 1, 2, 3.
    colors = [QColor(220, 30, 30), QColor(30, 200, 40), QColor(30, 60, 220)]
    items = []
    for i, color in enumerate(colors):
        p = _solid_png(str(tmp_path / f"c{i}.png"), 40, 40, color)
        item = window.canvas.add_character(p)
        item.setPos(20, 20)  # same spot for all three, like alternate poses
        items.append(item)

    assert [it.zValue() for it in window.canvas.characters_by_z_ascending()] == sorted(
        it.zValue() for it in items
    )

    out = str(tmp_path / "clip.gif")
    ok = window._export_gif_to_path(out, duration_ms=80)
    assert ok is True
    assert os.path.exists(out)

    gif = Image.open(out)
    assert gif.is_animated
    assert gif.n_frames == 3

    for i, expected in enumerate(colors):
        gif.seek(i)
        rgb = gif.convert("RGB")
        sampled = rgb.getpixel((40, 40))  # inside the 20,20 -> 60,60 character square
        assert abs(sampled[0] - expected.red()) < 12, f"frame {i} red channel off"
        assert abs(sampled[1] - expected.green()) < 12, f"frame {i} green channel off"
        assert abs(sampled[2] - expected.blue()) < 12, f"frame {i} blue channel off"
        # background color should show outside every character's square
        bg_sample = rgb.getpixel((150, 100))
        assert abs(bg_sample[0] - 30) < 12


def test_reordering_layers_changes_exported_frame_order(app, tmp_path):
    window = MainWindow()
    bg = _solid_png(str(tmp_path / "bg.png"), 120, 90, QColor(200, 200, 200))
    window.canvas.set_background(bg)

    red_path = _solid_png(str(tmp_path / "red.png"), 30, 30, QColor(220, 20, 20))
    blue_path = _solid_png(str(tmp_path / "blue.png"), 30, 30, QColor(20, 20, 220))
    red = window.canvas.add_character(red_path)
    red.setPos(10, 10)
    blue = window.canvas.add_character(blue_path)
    blue.setPos(10, 10)

    # blue was imported second, so it's on top; move red above it instead.
    window.canvas.move_layer_up(red)
    assert window.canvas.characters_by_z_ascending()[0] is blue
    assert window.canvas.characters_by_z_ascending()[1] is red

    out = str(tmp_path / "reordered.gif")
    assert window._export_gif_to_path(out, duration_ms=80) is True

    gif = Image.open(out)
    assert gif.n_frames == 2
    gif.seek(0)
    frame0 = gif.convert("RGB").getpixel((25, 25))
    gif.seek(1)
    frame1 = gif.convert("RGB").getpixel((25, 25))
    assert frame0[2] > frame0[0]  # frame 0 = blue (bluer than red)
    assert frame1[0] > frame1[2]  # frame 1 = red (redder than blue)
