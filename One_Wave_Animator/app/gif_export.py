"""Turn a sequence of rendered QImage frames into an animated GIF.

Kept as its own small module (rather than folded into canvas_view.py) so
the Pillow dependency and the actual encoding logic can be unit tested
without touching Qt widgets, and so canvas_view.py stays free of an
image-library import it doesn't otherwise need.
"""
from __future__ import annotations

import io
from typing import List

from PySide6.QtCore import QBuffer, QIODevice
from PySide6.QtGui import QImage

try:
    from PIL import Image
except ImportError:  # pragma: no cover - exercised via GifExportError below
    Image = None


class GifExportError(RuntimeError):
    """Raised for any problem turning frames into a saved GIF file."""


def qimage_to_pil(image: QImage) -> "Image.Image":
    """Convert a QImage to a Pillow Image via PNG bytes.

    Going through an actual PNG round-trip (rather than reading QImage's
    raw buffer directly) sidesteps stride/byte-order pitfalls between Qt's
    and Pillow's native pixel layouts entirely - a few hundred extra bytes
    of encode/decode is a fine trade for correctness here.
    """
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    if not image.save(buffer, "PNG"):
        raise GifExportError("Could not encode a frame to PNG for GIF export.")
    data = bytes(buffer.data())
    buffer.close()
    return Image.open(io.BytesIO(data)).convert("RGBA")


def qimages_to_gif(
    images: List[QImage],
    output_path: str,
    duration_ms: int = 150,
    loop: int = 0,
) -> None:
    """Save a list of same-size QImage frames as an animated GIF.

    duration_ms: milliseconds each frame is shown.
    loop: 0 = loop forever (Pillow/GIF convention), N = loop N times.
    """
    if Image is None:
        raise GifExportError(
            "Pillow is not installed. Run: pip install Pillow"
        )
    if len(images) < 2:
        raise GifExportError("Need at least 2 frames to export an animation.")

    frames = [qimage_to_pil(img) for img in images]
    # Composite onto a flat white background before palette quantization -
    # GIF has no true alpha compositing across frames, only a single
    # transparent-color index, so blending against white here (rather than
    # leaving partially-transparent pixels for the GIF encoder to guess
    # at) keeps every frame looking like what was actually on the canvas.
    flattened = []
    for frame in frames:
        canvas = Image.new("RGBA", frame.size, (255, 255, 255, 255))
        canvas.alpha_composite(frame)
        flattened.append(canvas.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=256))

    try:
        flattened[0].save(
            output_path,
            save_all=True,
            append_images=flattened[1:],
            duration=duration_ms,
            loop=loop,
            optimize=False,
        )
    except OSError as exc:
        raise GifExportError(f"Could not write GIF file: {exc}") from exc
