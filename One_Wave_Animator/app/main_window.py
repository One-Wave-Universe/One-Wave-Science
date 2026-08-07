"""Top-level application window: menus, dockable layers panel, canvas."""
from __future__ import annotations

import os
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from .canvas_view import SceneCanvas
from .layers_panel import LayersPanel
from .scene_model import Scene

APP_NAME = "One-Wave Animator"
SCENE_FILE_FILTER = "One-Wave Animator Scene (*.owascene)"
BACKGROUND_FILE_FILTER = "Images (*.png *.jpg *.jpeg)"
CHARACTER_FILE_FILTER = "Transparent PNG (*.png)"
SCENE_EXTENSION = ".owascene"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_file: Optional[str] = None

        self.canvas = SceneCanvas(self)
        self.setCentralWidget(self.canvas)

        self.layers_panel = LayersPanel(self.canvas, self)
        dock = QDockWidget("Layers", self)
        dock.setWidget(self.layers_panel)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        self.canvas.modified.connect(self._on_modified)

        self._build_menus()
        self._update_title()
        self.resize(1200, 800)

    # ---- menu construction ------------------------------------------
    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")

        new_action = QAction("&New Scene", self, shortcut=QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_scene)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        import_bg_action = QAction("Import &Background...", self, shortcut="Ctrl+I")
        import_bg_action.triggered.connect(self.import_background)
        file_menu.addAction(import_bg_action)

        import_char_action = QAction("Import &Character...", self, shortcut="Ctrl+Shift+I")
        import_char_action.triggered.connect(self.import_character)
        file_menu.addAction(import_char_action)

        file_menu.addSeparator()

        open_action = QAction("&Open Scene...", self, shortcut=QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_scene)
        file_menu.addAction(open_action)

        save_action = QAction("&Save Scene", self, shortcut=QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_scene)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save Scene &As...", self, shortcut=QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_scene_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self, shortcut=QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        layers_menu = self.menuBar().addMenu("&Layers")
        delete_action = QAction("&Delete Selected Layer", self, shortcut=QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self._delete_selected)
        layers_menu.addAction(delete_action)

        move_up_action = QAction("Move Layer &Up", self, shortcut="Ctrl+]")
        move_up_action.triggered.connect(self._move_selected_up)
        layers_menu.addAction(move_up_action)

        move_down_action = QAction("Move Layer &Down", self, shortcut="Ctrl+[")
        move_down_action.triggered.connect(self._move_selected_down)
        layers_menu.addAction(move_down_action)

    # ---- File actions --------------------------------------------------
    def new_scene(self) -> None:
        if not self._confirm_discard_unsaved():
            return
        self.canvas.clear()
        self._current_file = None
        self.setWindowModified(False)
        self._update_title()

    def import_background(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Import Background", "", BACKGROUND_FILE_FILTER)
        if not path:
            return
        try:
            self.canvas.set_background(path)
        except ValueError as exc:
            QMessageBox.warning(self, APP_NAME, str(exc))

    def import_character(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Import Character", "", CHARACTER_FILE_FILTER)
        if not path:
            return
        try:
            self.canvas.add_character(path)
        except ValueError as exc:
            QMessageBox.warning(self, APP_NAME, str(exc))

    def open_scene(self) -> None:
        if not self._confirm_discard_unsaved():
            return
        path, _ = QFileDialog.getOpenFileName(self, "Open Scene", "", SCENE_FILE_FILTER)
        if not path:
            return
        try:
            scene = Scene.load(path)
        except (OSError, ValueError, KeyError) as exc:
            QMessageBox.critical(self, APP_NAME, f"Could not open scene:\n{exc}")
            return
        warnings = self.canvas.load_scene_model(scene)
        self._current_file = path
        self.setWindowModified(False)
        self._update_title()
        if warnings:
            QMessageBox.warning(
                self,
                APP_NAME,
                "Some layers could not be restored:\n\n" + "\n".join(warnings),
            )

    def save_scene(self) -> bool:
        if self._current_file is None:
            return self.save_scene_as()
        return self._write_scene(self._current_file)

    def save_scene_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(self, "Save Scene As", "", SCENE_FILE_FILTER)
        if not path:
            return False
        if not path.lower().endswith(SCENE_EXTENSION):
            path += SCENE_EXTENSION
        return self._write_scene(path)

    def _write_scene(self, path: str) -> bool:
        try:
            self.canvas.to_scene_model().save(path)
        except OSError as exc:
            QMessageBox.critical(self, APP_NAME, f"Could not save scene:\n{exc}")
            return False
        self._current_file = path
        self.setWindowModified(False)
        self._update_title()
        return True

    # ---- Layers menu actions -------------------------------------------
    def _delete_selected(self) -> None:
        self.canvas.delete_selected()

    def _move_selected_up(self) -> None:
        item = self.canvas.selected_character()
        if item is not None:
            self.canvas.move_layer_up(item)

    def _move_selected_down(self) -> None:
        item = self.canvas.selected_character()
        if item is not None:
            self.canvas.move_layer_down(item)

    # ---- dirty / title tracking ------------------------------------------
    def _on_modified(self) -> None:
        self.setWindowModified(True)
        self._update_title()

    def _update_title(self) -> None:
        name = os.path.basename(self._current_file) if self._current_file else "Untitled Scene"
        self.setWindowTitle(f"{name}[*] - {APP_NAME}")

    def _confirm_discard_unsaved(self) -> bool:
        if not self.isWindowModified():
            return True
        response = QMessageBox.question(
            self,
            APP_NAME,
            "This scene has unsaved changes. Save before continuing?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )
        if response == QMessageBox.StandardButton.Save:
            return self.save_scene()
        if response == QMessageBox.StandardButton.Discard:
            return True
        return False

    def closeEvent(self, event) -> None:  # noqa: D102 - Qt override
        if self._confirm_discard_unsaved():
            event.accept()
        else:
            event.ignore()
