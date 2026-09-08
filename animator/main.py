#!/usr/bin/env python3
"""Animator v1: runnable fixed-layer desktop animation editor.

This is deliberately a product slice, not a framework demo. It can load image
layers, move them on a scene, control frame exposure, play the timeline, and
save/reopen projects as portable JSON next to their referenced assets.
"""

from __future__ import annotations

import json
import sys
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QAction, QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

APP_NAME = "Animator"
PROJECT_VERSION = 1
DEFAULT_FPS = 12
DEFAULT_FRAMES = 120
CANVAS_W = 1280
CANVAS_H = 720


@dataclass
class LayerState:
    id: str
    name: str
    source: str
    x: float = 0.0
    y: float = 0.0
    scale: float = 1.0
    rotation: float = 0.0
    start_frame: int = 0
    end_frame: int = DEFAULT_FRAMES - 1
    visible: bool = True
    locked: bool = False


class CanvasScene(QGraphicsScene):
    """Scene with an editor-only placement grid."""

    def __init__(self) -> None:
        super().__init__(0, 0, CANVAS_W, CANVAS_H)
        self.grid_enabled = True
        self.setBackgroundBrush(QColor(32, 34, 38))

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:  # noqa: N802
        super().drawBackground(painter, rect)
        if not self.grid_enabled:
            return
        grid = 40
        left = int(rect.left()) - (int(rect.left()) % grid)
        top = int(rect.top()) - (int(rect.top()) % grid)
        painter.save()
        painter.setPen(QPen(QColor(64, 67, 73), 1))
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += grid
        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += grid
        painter.restore()


class LayerItem(QGraphicsPixmapItem):
    def __init__(self, state: LayerState, pixmap: QPixmap) -> None:
        super().__init__(pixmap)
        self.layer_id = state.id
        self.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, not state.locked)
        self.apply_state(state)

    def apply_state(self, state: LayerState) -> None:
        self.setPos(QPointF(state.x, state.y))
        self.setScale(state.scale)
        self.setRotation(state.rotation)
        self.setVisible(state.visible)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, not state.locked)


class AnimatorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1500, 900)

        self.project_path: Path | None = None
        self.layers: list[LayerState] = []
        self.items: dict[str, LayerItem] = {}
        self.current_frame = 0
        self.frame_count = DEFAULT_FRAMES
        self.fps = DEFAULT_FPS
        self.playing = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._advance_frame)

        self.scene = CanvasScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )
        self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.layer_list = QListWidget()
        self.layer_list.currentItemChanged.connect(self._layer_selection_changed)

        self.start_spin = QSpinBox()
        self.end_spin = QSpinBox()
        self.start_spin.setRange(0, self.frame_count - 1)
        self.end_spin.setRange(0, self.frame_count - 1)
        self.start_spin.valueChanged.connect(self._exposure_changed)
        self.end_spin.valueChanged.connect(self._exposure_changed)

        self.timeline = QSlider(Qt.Orientation.Horizontal)
        self.timeline.setRange(0, self.frame_count - 1)
        self.timeline.valueChanged.connect(self.set_frame)
        self.frame_label = QLabel()

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_playback)
        self.grid_button = QPushButton("Grid: On")
        self.grid_button.clicked.connect(self.toggle_grid)

        self._build_ui()
        self._build_actions()
        self._refresh_frame_label()
        self.statusBar().showMessage("Ready — add a background or character layer")

    def _build_ui(self) -> None:
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("LAYERS"))
        left_layout.addWidget(self.layer_list, 1)

        add_layer = QPushButton("+ Add Image Layer")
        add_layer.clicked.connect(self.add_image_layer)
        remove_layer = QPushButton("Remove Layer")
        remove_layer.clicked.connect(self.remove_selected_layer)
        lock_layer = QPushButton("Lock / Unlock")
        lock_layer.clicked.connect(self.toggle_selected_lock)
        visible_layer = QPushButton("Show / Hide")
        visible_layer.clicked.connect(self.toggle_selected_visibility)
        left_layout.addWidget(add_layer)
        left_layout.addWidget(remove_layer)
        left_layout.addWidget(lock_layer)
        left_layout.addWidget(visible_layer)

        exposure = QFormLayout()
        exposure.addRow("First frame", self.start_spin)
        exposure.addRow("Last frame", self.end_spin)
        left_layout.addLayout(exposure)

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(self.view)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([260, 1200])

        timeline_bar = QWidget()
        timeline_layout = QHBoxLayout(timeline_bar)
        timeline_layout.setContentsMargins(8, 4, 8, 4)
        timeline_layout.addWidget(self.play_button)
        timeline_layout.addWidget(self.grid_button)
        timeline_layout.addWidget(self.timeline, 1)
        timeline_layout.addWidget(self.frame_label)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter, 1)
        layout.addWidget(timeline_bar)
        self.setCentralWidget(central)

    def _build_actions(self) -> None:
        toolbar = QToolBar("Project")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_project)
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_project)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_project)
        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(lambda: self.save_project(save_as=True))
        fit_action = QAction("Fit Canvas", self)
        fit_action.triggered.connect(
            lambda: self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        )
        fullscreen_action = QAction("Playback Fullscreen", self)
        fullscreen_action.triggered.connect(self.fullscreen_playback)

        for action in (new_action, open_action, save_action, save_as_action, fit_action, fullscreen_action):
            toolbar.addAction(action)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addActions([new_action, open_action, save_action, save_as_action])

    def add_image_layer(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Add image layer",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)",
        )
        if not filename:
            return
        pixmap = QPixmap(filename)
        if pixmap.isNull():
            QMessageBox.warning(self, APP_NAME, "That image could not be opened.")
            return

        state = LayerState(
            id=str(uuid.uuid4()),
            name=Path(filename).stem,
            source=str(Path(filename).resolve()),
            end_frame=self.frame_count - 1,
        )
        # Put newly added assets near center while keeping their native pixels.
        state.x = max(0.0, (CANVAS_W - pixmap.width()) / 2)
        state.y = max(0.0, (CANVAS_H - pixmap.height()) / 2)
        self.layers.append(state)
        self._create_scene_item(state, pixmap)
        self._rebuild_layer_list(select_id=state.id)
        self.update_frame_visibility()

    def _create_scene_item(self, state: LayerState, pixmap: QPixmap | None = None) -> None:
        pixmap = pixmap or QPixmap(state.source)
        if pixmap.isNull():
            return
        item = LayerItem(state, pixmap)
        self.items[state.id] = item
        self.scene.addItem(item)

    def remove_selected_layer(self) -> None:
        state = self._selected_state()
        if not state:
            return
        item = self.items.pop(state.id, None)
        if item:
            self.scene.removeItem(item)
        self.layers = [layer for layer in self.layers if layer.id != state.id]
        self._rebuild_layer_list()

    def toggle_selected_lock(self) -> None:
        state = self._selected_state()
        if not state:
            return
        state.locked = not state.locked
        item = self.items.get(state.id)
        if item:
            item.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, not state.locked)
        self._rebuild_layer_list(select_id=state.id)

    def toggle_selected_visibility(self) -> None:
        state = self._selected_state()
        if not state:
            return
        state.visible = not state.visible
        self.update_frame_visibility()
        self._rebuild_layer_list(select_id=state.id)

    def _selected_state(self) -> LayerState | None:
        current = self.layer_list.currentItem()
        if current is None:
            return None
        layer_id = current.data(Qt.ItemDataRole.UserRole)
        return next((layer for layer in self.layers if layer.id == layer_id), None)

    def _layer_selection_changed(self, current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        if current is None:
            return
        state = self._selected_state()
        if not state:
            return
        self.start_spin.blockSignals(True)
        self.end_spin.blockSignals(True)
        self.start_spin.setValue(state.start_frame)
        self.end_spin.setValue(state.end_frame)
        self.start_spin.blockSignals(False)
        self.end_spin.blockSignals(False)
        self.scene.clearSelection()
        item = self.items.get(state.id)
        if item:
            item.setSelected(True)

    def _exposure_changed(self) -> None:
        state = self._selected_state()
        if not state:
            return
        start = min(self.start_spin.value(), self.end_spin.value())
        end = max(self.start_spin.value(), self.end_spin.value())
        state.start_frame = start
        state.end_frame = end
        self.update_frame_visibility()

    def _sync_item_transforms(self) -> None:
        for state in self.layers:
            item = self.items.get(state.id)
            if not item:
                continue
            state.x = item.pos().x()
            state.y = item.pos().y()
            state.scale = item.scale()
            state.rotation = item.rotation()

    def _rebuild_layer_list(self, select_id: str | None = None) -> None:
        self.layer_list.blockSignals(True)
        self.layer_list.clear()
        for state in reversed(self.layers):
            flags = []
            if state.locked:
                flags.append("LOCK")
            if not state.visible:
                flags.append("HIDDEN")
            suffix = f"  [{' | '.join(flags)}]" if flags else ""
            row = QListWidgetItem(f"{state.name}{suffix}")
            row.setData(Qt.ItemDataRole.UserRole, state.id)
            self.layer_list.addItem(row)
            if state.id == select_id:
                self.layer_list.setCurrentItem(row)
        self.layer_list.blockSignals(False)

    def set_frame(self, frame: int) -> None:
        self.current_frame = frame
        if self.timeline.value() != frame:
            self.timeline.blockSignals(True)
            self.timeline.setValue(frame)
            self.timeline.blockSignals(False)
        self.update_frame_visibility()
        self._refresh_frame_label()

    def update_frame_visibility(self) -> None:
        for state in self.layers:
            item = self.items.get(state.id)
            if item:
                exposed = state.start_frame <= self.current_frame <= state.end_frame
                item.setVisible(state.visible and exposed)

    def _refresh_frame_label(self) -> None:
        self.frame_label.setText(f"Frame {self.current_frame + 1} / {self.frame_count}")

    def toggle_playback(self) -> None:
        self.playing = not self.playing
        self.play_button.setText("Stop" if self.playing else "Play")
        if self.playing:
            self.scene.grid_enabled = False
            self.scene.update()
            self.timer.start(max(1, round(1000 / self.fps)))
        else:
            self.timer.stop()
            self.scene.grid_enabled = True
            self.scene.update()
            self.grid_button.setText("Grid: On")

    def _advance_frame(self) -> None:
        next_frame = self.current_frame + 1
        if next_frame >= self.frame_count:
            next_frame = 0
        self.set_frame(next_frame)

    def toggle_grid(self) -> None:
        if self.playing:
            return
        self.scene.grid_enabled = not self.scene.grid_enabled
        self.grid_button.setText("Grid: On" if self.scene.grid_enabled else "Grid: Off")
        self.scene.update()

    def fullscreen_playback(self) -> None:
        self.view.setWindowFlag(Qt.WindowType.Window, True)
        self.view.showFullScreen()
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        if not self.playing:
            self.toggle_playback()

    def new_project(self) -> None:
        if self.playing:
            self.toggle_playback()
        self.project_path = None
        self.layers.clear()
        self.items.clear()
        self.scene.clear()
        self._rebuild_layer_list()
        self.set_frame(0)
        self.setWindowTitle(APP_NAME)

    def project_dict(self) -> dict:
        self._sync_item_transforms()
        return {
            "format": "one-wave-animator",
            "version": PROJECT_VERSION,
            "canvas": {"width": CANVAS_W, "height": CANVAS_H},
            "fps": self.fps,
            "frame_count": self.frame_count,
            "layers": [asdict(layer) for layer in self.layers],
        }

    def save_project(self, save_as: bool = False) -> None:
        path = self.project_path
        if save_as or path is None:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Animator project", "scene.animator.json", "Animator Project (*.animator.json)")
            if not filename:
                return
            path = Path(filename)
            if not str(path).endswith(".animator.json"):
                path = Path(str(path) + ".animator.json")
        path.write_text(json.dumps(self.project_dict(), indent=2), encoding="utf-8")
        self.project_path = path
        self.setWindowTitle(f"{APP_NAME} — {path.name}")
        self.statusBar().showMessage(f"Saved {path}", 4000)

    def open_project(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(self, "Open Animator project", "", "Animator Project (*.animator.json);;JSON (*.json)")
        if not filename:
            return
        path = Path(filename)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("format") != "one-wave-animator":
                raise ValueError("Not an Animator project")
            loaded = [LayerState(**entry) for entry in data.get("layers", [])]
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            QMessageBox.critical(self, APP_NAME, f"Could not open project:\n{exc}")
            return

        self.new_project()
        self.fps = int(data.get("fps", DEFAULT_FPS))
        self.frame_count = max(1, int(data.get("frame_count", DEFAULT_FRAMES)))
        self.timeline.setRange(0, self.frame_count - 1)
        self.start_spin.setRange(0, self.frame_count - 1)
        self.end_spin.setRange(0, self.frame_count - 1)
        self.layers = loaded
        missing = []
        for state in self.layers:
            pixmap = QPixmap(state.source)
            if pixmap.isNull():
                missing.append(state.source)
                continue
            self._create_scene_item(state, pixmap)
        self.project_path = path
        self._rebuild_layer_list()
        self.set_frame(0)
        self.setWindowTitle(f"{APP_NAME} — {path.name}")
        if missing:
            QMessageBox.warning(self, APP_NAME, "Project opened, but these source images are missing:\n\n" + "\n".join(missing))

    def closeEvent(self, event) -> None:  # noqa: N802
        self.timer.stop()
        event.accept()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    window = AnimatorWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
