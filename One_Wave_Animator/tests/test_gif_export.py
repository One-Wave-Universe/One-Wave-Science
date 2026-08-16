"""Unit tests for app.gif_export - pure QImage-list -> GIF encoding, no
QMainWindow or scene needed."""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PIL")
PySide6 = pytest.importorskip("PySide6")

from PySide6.QtGui import QColor, QImage  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from app.gif_export import GifExportError, qimages_to_gif  # noqa: E402
from PIL import Image  # noqa: E402


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication(sys.argv)


def _solid_frame(color: QColor, w: int = 40, h: int = 30) -> QImage:
    img = QImage(w, h, QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(color)
    return img


def test_requires_at_least_two_frames(app):
    with pytest.raises(GifExportError, match="at least 2 frames"):
        qimages_to_gif([_solid_frame(QColor("red"))], "/tmp/should_not_be_written.gif")


def test_writes_a_real_multi_frame_gif(app, tmp_path):
    colors = [QColor(220, 40, 40), QColor(40, 200, 60), QColor(40, 80, 220)]
    frames = [_solid_frame(c) for c in colors]
    out = str(tmp_path / "clip.gif")

    qimages_to_gif(frames, out, duration_ms=90, loop=0)

    assert os.path.exists(out)
    assert os.path.getsize(out) > 0

    reopened = Image.open(out)
    assert reopened.is_animated
    assert reopened.n_frames == 3

    for i, expected in enumerate(colors):
        reopened.seek(i)
        frame_rgb = reopened.convert("RGB")
        sampled = frame_rgb.getpixel((20, 15))
        # Palette quantization to 256 colors on a single flat solid color
        # should be exact or within a couple of levels, not a different hue.
        assert abs(sampled[0] - expected.red()) < 10
        assert abs(sampled[1] - expected.green()) < 10
        assert abs(sampled[2] - expected.blue()) < 10


def test_transparent_regions_flatten_onto_white(app, tmp_path):
    """GIF has no real alpha compositing across frames - transparent source
    pixels should end up white (the flattening background this module
    chose), not black or garbage, and definitely not crash."""
    transparent = QImage(20, 20, QImage.Format.Format_ARGB32_Premultiplied)
    transparent.fill(QColor(0, 0, 0, 0))
    opaque = _solid_frame(QColor(10, 10, 10), 20, 20)
    out = str(tmp_path / "flatten.gif")

    qimages_to_gif([transparent, opaque], out, duration_ms=100)

    reopened = Image.open(out).convert("RGB")
    reopened.seek(0)
    px = Image.open(out).convert("RGB").getpixel((10, 10))
    assert px == (255, 255, 255)


def test_missing_pillow_raises_gif_export_error(app, tmp_path, monkeypatch):
    import app.gif_export as gif_export_module

    monkeypatch.setattr(gif_export_module, "Image", None)
    with pytest.raises(GifExportError, match="Pillow is not installed"):
        qimages_to_gif(
            [_solid_frame(QColor("red")), _solid_frame(QColor("blue"))],
            str(tmp_path / "x.gif"),
        )
