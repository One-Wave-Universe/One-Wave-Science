"""Custom QGraphicsItem subclasses for the scene canvas.

Layer geometry (width/height) is tracked explicitly on the item rather
than through a QTransform scale, so it can be read back and written to
the scene JSON without doing any transform math.
"""
from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPen, QPixmap
from PySide6.QtWidgets import QGraphicsItem

HANDLE_SIZE = 12.0
MIN_SIZE = 16.0


class ImageLayerItem(QGraphicsItem):
    """Base class: draws a QPixmap stretched to fill (0, 0, width, height)."""

    def __init__(self, pixmap: QPixmap, width: float, height: float, source_path: str):
        super().__init__()
        self.pixmap = pixmap
        self.source_path = source_path
        self._width = width
        self._height = height

    def rect(self) -> QRectF:
        return QRectF(0, 0, self._width, self._height)

    def boundingRect(self) -> QRectF:  # noqa: D102 - Qt override
        return self.rect()

    def paint(self, painter, option, widget=None):  # noqa: D102 - Qt override
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.drawPixmap(self.rect(), self.pixmap, QRectF(self.pixmap.rect()))

    def set_size(self, width: float, height: float) -> None:
        self.prepareGeometryChange()
        self._width = max(MIN_SIZE, width)
        self._height = max(MIN_SIZE, height)
        self.update()

    def size(self) -> tuple[float, float]:
        return self._width, self._height


class BackgroundItem(ImageLayerItem):
    """Fixed, non-interactive backdrop that always sits behind every character."""

    def __init__(self, pixmap: QPixmap, width: float, height: float, source_path: str):
        super().__init__(pixmap, width, height, source_path)
        self.setZValue(-1000)
        # Deliberately no ItemIsMovable / ItemIsSelectable: the background is locked.


class CharacterItem(ImageLayerItem):
    """Draggable, aspect-locked-resizable, selectable character cutout."""

    def __init__(
        self,
        pixmap: QPixmap,
        width: float,
        height: float,
        source_path: str,
        on_changed: Optional[Callable[[], None]] = None,
    ):
        super().__init__(pixmap, width, height, source_path)
        self._aspect = (width / height) if height else 1.0
        self._on_changed = on_changed
        self._resizing = False
        self._resize_start_mouse = QPointF()
        self._resize_start_size = (width, height)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)

    def _handle_rect(self) -> QRectF:
        return QRectF(self._width - HANDLE_SIZE, self._height - HANDLE_SIZE, HANDLE_SIZE, HANDLE_SIZE)

    def boundingRect(self) -> QRectF:  # noqa: D102 - Qt override
        # Pad slightly so the dashed selection outline and handle never clip.
        return self.rect().adjusted(-2, -2, 2, 2)

    def paint(self, painter, option, widget=None):  # noqa: D102 - Qt override
        super().paint(painter, option, widget)
        if self.isSelected():
            pen = QPen(QColor(60, 160, 255), 1.5, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(self.rect())
            handle = self._handle_rect()
            painter.setPen(QPen(QColor(30, 100, 200), 1))
            painter.setBrush(QBrush(QColor(60, 160, 255)))
            painter.drawRect(handle)

    def hoverMoveEvent(self, event):  # noqa: D102 - Qt override
        if self.isSelected() and self._handle_rect().contains(event.pos()):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        else:
            self.unsetCursor()
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):  # noqa: D102 - Qt override
        if (
            self.isSelected()
            and event.button() == Qt.MouseButton.LeftButton
            and self._handle_rect().contains(event.pos())
        ):
            self._resizing = True
            self._resize_start_mouse = event.scenePos()
            self._resize_start_size = (self._width, self._height)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):  # noqa: D102 - Qt override
        if self._resizing:
            delta = event.scenePos() - self._resize_start_mouse
            start_w, start_h = self._resize_start_size
            new_w = max(MIN_SIZE, start_w + delta.x())
            new_h = new_w / self._aspect if self._aspect else new_w
            if new_h < MIN_SIZE:
                new_h = MIN_SIZE
                new_w = new_h * self._aspect
            self.set_size(new_w, new_h)
            if self._on_changed:
                self._on_changed()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):  # noqa: D102 - Qt override
        if self._resizing:
            self._resizing = False
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):  # noqa: D102 - Qt override
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged and self._on_changed:
            self._on_changed()
        return super().itemChange(change, value)
