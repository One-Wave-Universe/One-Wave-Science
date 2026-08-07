"""Generates the placeholder sample assets under assets/sample/ using Qt
drawing primitives, so the repo doesn't need to vendor any external
artwork. Re-run with: python tools/make_sample_assets.py
"""
import os
import sys

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QApplication

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sample")


def make_background(path: str) -> None:
    width, height = 800, 450
    pixmap = QPixmap(width, height)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    sky = QLinearGradient(0, 0, 0, height * 0.7)
    sky.setColorAt(0.0, QColor(135, 206, 235))
    sky.setColorAt(1.0, QColor(210, 240, 250))
    painter.fillRect(QRectF(0, 0, width, height * 0.7), QBrush(sky))

    ground = QLinearGradient(0, height * 0.65, 0, height)
    ground.setColorAt(0.0, QColor(120, 190, 90))
    ground.setColorAt(1.0, QColor(80, 150, 60))
    painter.fillRect(QRectF(0, height * 0.65, width, height * 0.35), QBrush(ground))

    painter.setBrush(QBrush(QColor(255, 250, 210)))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(QPointF(width * 0.85, height * 0.15), 40, 40)

    painter.end()
    pixmap.save(path, "PNG")


def make_character(path: str) -> None:
    width, height = 200, 320
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    painter.setPen(QPen(QColor(40, 40, 40), 4))
    painter.setBrush(QBrush(QColor(250, 210, 170)))
    painter.drawEllipse(QPointF(width / 2, 60), 45, 45)

    painter.setBrush(QBrush(QColor(70, 120, 200)))
    painter.drawRoundedRect(QRectF(width / 2 - 55, 100, 110, 140), 20, 20)

    painter.setBrush(QBrush(QColor(250, 210, 170)))
    painter.drawEllipse(QRectF(width / 2 - 90, 110, 30, 100))
    painter.drawEllipse(QRectF(width / 2 + 60, 110, 30, 100))

    painter.setBrush(QBrush(QColor(60, 60, 90)))
    painter.drawRoundedRect(QRectF(width / 2 - 40, 235, 35, 80), 12, 12)
    painter.drawRoundedRect(QRectF(width / 2 + 5, 235, 35, 80), 12, 12)

    painter.end()
    pixmap.save(path, "PNG")


def main() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    os.makedirs(OUT_DIR, exist_ok=True)
    make_background(os.path.join(OUT_DIR, "sample_background.png"))
    make_character(os.path.join(OUT_DIR, "sample_character.png"))
    print(f"Wrote sample assets to {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    main()
