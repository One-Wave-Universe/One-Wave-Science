"""The editable scene canvas: one locked background plus draggable,
resizable, reorderable character layers."""
from __future__ import annotations

from typing import List, Optional

from PySide6.QtCore import Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView

from .graphics_items import BackgroundItem, CharacterItem
from .scene_model import (
    DEFAULT_CANVAS_HEIGHT,
    DEFAULT_CANVAS_WIDTH,
    BackgroundLayer,
    CharacterLayer,
    Scene,
)

CANVAS_BORDER_COLOR = QColor(120, 120, 120)
VIEW_BACKDROP_COLOR = QColor(64, 64, 64)


class SceneCanvas(QGraphicsView):
    """Editable scene canvas backed by a QGraphicsScene."""

    modified = Signal()
    selection_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setBackgroundBrush(QBrush(VIEW_BACKDROP_COLOR))
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        self._background_item: Optional[BackgroundItem] = None
        self._canvas_paper: Optional[QGraphicsRectItem] = None
        self._next_z = 1

        self._scene.selectionChanged.connect(self.selection_changed.emit)

        self.set_canvas_size(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)

    # ---- canvas geometry ---------------------------------------------
    def set_canvas_size(self, width: float, height: float) -> None:
        if self._canvas_paper is None:
            self._canvas_paper = QGraphicsRectItem(0, 0, width, height)
            self._canvas_paper.setZValue(-2000)
            self._canvas_paper.setPen(QPen(CANVAS_BORDER_COLOR, 1))
            self._canvas_paper.setBrush(QBrush(QColor(255, 255, 255)))
            self._scene.addItem(self._canvas_paper)
        else:
            self._canvas_paper.setRect(0, 0, width, height)
        self._scene.setSceneRect(0, 0, width, height)
        self.setSceneRect(0, 0, width, height)

    def canvas_size(self) -> tuple[float, float]:
        rect = self._scene.sceneRect()
        return rect.width(), rect.height()

    def clear(self) -> None:
        self._scene.clear()
        self._background_item = None
        self._canvas_paper = None
        self._next_z = 1
        self.set_canvas_size(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)

    # ---- background ----------------------------------------------------
    def set_background(self, path: str) -> None:
        pixmap = QPixmap(path)
        if pixmap.isNull():
            raise ValueError(f"Could not load image: {path}")
        if self._background_item is not None:
            self._scene.removeItem(self._background_item)
        width, height = pixmap.width(), pixmap.height()
        self._background_item = BackgroundItem(pixmap, width, height, path)
        self._scene.addItem(self._background_item)
        self.set_canvas_size(width, height)
        self._emit_modified()

    def _restore_background(self, layer: BackgroundLayer) -> None:
        pixmap = QPixmap(layer.path)
        if pixmap.isNull():
            raise ValueError(f"Could not load background image: {layer.path}")
        if self._background_item is not None:
            self._scene.removeItem(self._background_item)
        self._background_item = BackgroundItem(pixmap, layer.width, layer.height, layer.path)
        self._scene.addItem(self._background_item)

    def has_background(self) -> bool:
        return self._background_item is not None

    def background_item(self) -> Optional[BackgroundItem]:
        return self._background_item

    # ---- characters ------------------------------------------------------
    def add_character(self, path: str) -> CharacterItem:
        pixmap = QPixmap(path)
        if pixmap.isNull():
            raise ValueError(f"Could not load image: {path}")
        canvas_w, canvas_h = self.canvas_size()
        width, height = self._default_character_size(pixmap.width(), pixmap.height(), canvas_w, canvas_h)
        item = CharacterItem(pixmap, width, height, path, on_changed=self._emit_modified)
        item.setZValue(self._next_z)
        self._next_z += 1
        # Stagger repeated imports a little so they don't land exactly on top of each other.
        count = len(self.character_items())
        offset = (count % 6) * 24
        item.setPos((canvas_w - width) / 2 + offset, (canvas_h - height) / 2 + offset)
        self._scene.addItem(item)
        self.select_character(item)
        self._emit_modified()
        return item

    def _restore_character(self, layer: CharacterLayer) -> None:
        pixmap = QPixmap(layer.path)
        if pixmap.isNull():
            raise ValueError(f"Could not load character image: {layer.path}")
        item = CharacterItem(pixmap, layer.width, layer.height, layer.path, on_changed=self._emit_modified)
        item.setPos(layer.x, layer.y)
        item.setZValue(layer.z)
        self._scene.addItem(item)
        self._next_z = max(self._next_z, layer.z + 1)

    @staticmethod
    def _default_character_size(
        native_w: int, native_h: int, canvas_w: float, canvas_h: float
    ) -> tuple[float, float]:
        if native_w <= 0 or native_h <= 0:
            return 100.0, 100.0
        scale = min(1.0, (canvas_w * 0.5) / native_w, (canvas_h * 0.5) / native_h)
        return native_w * scale, native_h * scale

    def character_items(self) -> List[CharacterItem]:
        return [it for it in self._scene.items() if isinstance(it, CharacterItem)]

    def selected_character(self) -> Optional[CharacterItem]:
        for it in self._scene.selectedItems():
            if isinstance(it, CharacterItem):
                return it
        return None

    def select_character(self, item: CharacterItem) -> None:
        self._scene.clearSelection()
        item.setSelected(True)

    def delete_character(self, item: CharacterItem) -> None:
        self._scene.removeItem(item)
        self._emit_modified()

    def delete_selected(self) -> bool:
        item = self.selected_character()
        if item is None:
            return False
        self.delete_character(item)
        return True

    # ---- layer ordering ----------------------------------------------
    def layers_top_to_bottom(self) -> List[CharacterItem]:
        return sorted(self.character_items(), key=lambda it: it.zValue(), reverse=True)

    def move_layer_up(self, item: CharacterItem) -> None:
        self._swap_with_neighbor(item, -1)

    def move_layer_down(self, item: CharacterItem) -> None:
        self._swap_with_neighbor(item, 1)

    def _swap_with_neighbor(self, item: CharacterItem, direction: int) -> None:
        layers = self.layers_top_to_bottom()
        idx = layers.index(item)
        neighbor_idx = idx + direction
        if neighbor_idx < 0 or neighbor_idx >= len(layers):
            return
        neighbor = layers[neighbor_idx]
        item_z, neighbor_z = item.zValue(), neighbor.zValue()
        item.setZValue(neighbor_z)
        neighbor.setZValue(item_z)
        self._emit_modified()

    # ---- scene <-> model -------------------------------------------------
    def to_scene_model(self) -> Scene:
        canvas_w, canvas_h = self.canvas_size()
        background = None
        if self._background_item is not None:
            w, h = self._background_item.size()
            background = BackgroundLayer(path=self._background_item.source_path, width=w, height=h)
        characters = []
        for item in self.character_items():
            w, h = item.size()
            pos = item.pos()
            characters.append(
                CharacterLayer(
                    path=item.source_path,
                    x=pos.x(),
                    y=pos.y(),
                    width=w,
                    height=h,
                    z=int(item.zValue()),
                )
            )
        return Scene(canvas_width=canvas_w, canvas_height=canvas_h, background=background, characters=characters)

    def load_scene_model(self, scene: Scene) -> List[str]:
        """Rebuild the canvas from a Scene. Returns a list of human-readable
        warnings for any layer whose source image could not be loaded
        (e.g. it was moved or deleted since the scene was saved) - those
        layers are skipped rather than aborting the whole load."""
        self.clear()
        self.set_canvas_size(scene.canvas_width, scene.canvas_height)
        warnings: List[str] = []
        if scene.background is not None:
            try:
                self._restore_background(scene.background)
            except ValueError as exc:
                warnings.append(str(exc))
        for layer in sorted(scene.characters, key=lambda c: c.z):
            try:
                self._restore_character(layer)
            except ValueError as exc:
                warnings.append(str(exc))
        return warnings

    # ---- misc --------------------------------------------------------
    def _emit_modified(self) -> None:
        self.modified.emit()
