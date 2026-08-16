"""Extended smoke test: a realistic multi-pose transparent-PNG character
sheet workflow — several cutout poses of one character imported onto a
background, resized, reordered, deleted, and round-tripped through save/
reload. Complements test_gui_smoke.py's single-repeated-image workflow with
real alpha-channel verification and more than two character layers."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PySide6 = pytest.importorskip("PySide6")

from PySide6.QtCore import Qt, QRectF  # noqa: E402
from PySide6.QtGui import QColor, QImage, QPainter, QRadialGradient  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from app.main_window import MainWindow  # noqa: E402
from app.scene_model import Scene  # noqa: E402


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication(sys.argv)


def _make_transparent_character(path, w, h, color):
    img = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
    img.fill(Qt.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing, True)
    grad = QRadialGradient(w / 2, h * 0.4, max(w, h) * 0.6)
    c1 = QColor(color)
    c1.setAlpha(255)
    c2 = QColor(color)
    c2.setAlpha(0)
    grad.setColorAt(0.0, c1)
    grad.setColorAt(1.0, c2)
    p.setBrush(grad)
    p.setPen(Qt.NoPen)
    p.drawEllipse(QRectF(0, 0, w, h))
    p.end()
    assert img.save(path, "PNG")
    return path


def _make_background(path, w, h):
    img = QImage(w, h, QImage.Format_ARGB32)
    img.fill(QColor(60, 90, 60))
    assert img.save(path, "PNG")
    return path


def test_multi_pose_character_sheet_workflow(app, tmp_path):
    bg_path = _make_background(str(tmp_path / "forest_bg.png"), 1536, 1024)

    pose_names = ["idle", "cast", "leap", "tumble", "staff"]
    pose_paths = []
    for i, name in enumerate(pose_names):
        p = _make_transparent_character(
            str(tmp_path / f"raccoon_{name}.png"), 420, 620,
            QColor(90 + i * 20, 110, 60),
        )
        pose_paths.append(p)
        qimg = QImage(p)
        assert qimg.hasAlphaChannel()
        assert qimg.pixelColor(2, 2).alpha() < 40, f"{name}: corner should be transparent"
        assert qimg.pixelColor(210, 248).alpha() > 200, f"{name}: gradient center should be opaque"

    window = MainWindow()
    canvas = window.canvas
    canvas.set_background(bg_path)
    assert canvas.has_background()
    assert canvas.canvas_size() == (1536.0, 1024.0)

    items = []
    for i, p in enumerate(pose_paths):
        item = canvas.add_character(p)
        item.setPos(80 + i * 220, 150 + (i % 2) * 60)
        items.append(item)

    assert len(canvas.character_items()) == 5
    zs = [it.zValue() for it in items]
    assert zs == sorted(zs)

    # Auto-fit-to-half-canvas on import (real app behavior, canvas_view.py L134):
    # scale = min(1, (canvas_w*0.5)/native_w, (canvas_h*0.5)/native_h).
    # 1536x1024 canvas, 420x620 native -> limited by height: 512/620.
    expected_scale = min(1.0, (1536 * 0.5) / 420, (1024 * 0.5) / 620)
    for item in items:
        w, h = item.size()
        assert w == pytest.approx(420 * expected_scale)
        assert h == pytest.approx(620 * expected_scale)

    leap = items[2]
    orig_w, orig_h = leap.size()
    aspect = orig_w / orig_h
    leap.set_size(orig_w * 1.5, orig_h * 1.5)
    new_w, new_h = leap.size()
    assert abs((new_w / new_h) - aspect) < 1e-6
    assert new_w == pytest.approx(orig_w * 1.5)

    idle = items[0]
    assert canvas.layers_top_to_bottom()[-1] == idle
    for _ in range(4):
        canvas.move_layer_up(idle)
    assert canvas.layers_top_to_bottom()[0] == idle

    tumble = items[3]
    canvas.delete_character(tumble)
    assert len(canvas.character_items()) == 4
    assert tumble not in canvas.character_items()

    scene_file = str(tmp_path / "raccoon_scene.owascene")
    assert window._write_scene(scene_file) is True

    reloaded = Scene.load(scene_file)
    assert reloaded.canvas_width == 1536 and reloaded.canvas_height == 1024
    assert len(reloaded.characters) == 4

    window2 = MainWindow()
    warnings = window2.canvas.load_scene_model(reloaded)
    assert warnings == []
    assert window2.canvas.has_background()
    assert len(window2.canvas.character_items()) == 4

    with open(scene_file) as f:
        raw = json.load(f)
    assert raw["background"]["path"] == "forest_bg.png"
    char_paths = sorted(c["path"] for c in raw["characters"])
    assert all(not p.startswith("/") for p in char_paths)
