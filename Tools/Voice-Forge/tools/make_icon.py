"""Generates a simple app icon (two merging waveforms) using Qt drawing
primitives, the same approach the Animator uses for its sample art, so
the repo doesn't need to vendor any external artwork.

Re-run with: python tools/make_icon.py
"""
import math
import os
import sys

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QApplication

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")


def make_icon(path: str, size: int = 512) -> None:
    from PySide6.QtGui import QPixmap

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    bg = QLinearGradient(0, 0, 0, size)
    bg.setColorAt(0.0, QColor(30, 34, 48))
    bg.setColorAt(1.0, QColor(15, 17, 26))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(bg))
    painter.drawRoundedRect(0, 0, size, size, size * 0.18, size * 0.18)

    mid = size / 2
    for color, freq, amp, phase in (
        (QColor(90, 200, 255), 2.0, 0.16, 0.0),
        (QColor(255, 150, 90), 2.0, 0.16, math.pi),
    ):
        path_obj = QPainterPath()
        n = 200
        for i in range(n + 1):
            x = size * 0.12 + (size * 0.76) * (i / n)
            t = i / n
            envelope = math.sin(math.pi * t)
            y = mid + math.sin(freq * math.pi * t + phase) * size * amp * envelope
            if i == 0:
                path_obj.moveTo(QPointF(x, y))
            else:
                path_obj.lineTo(QPointF(x, y))
        pen = QPen(color, size * 0.035)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path_obj)

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
    painter.drawEllipse(QPointF(mid, mid), size * 0.05, size * 0.05)

    painter.end()
    pixmap.save(path, "PNG")


def main() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "icon.png")
    make_icon(out_path)
    print(f"Wrote icon to {os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()
