"""Dockable panel listing character layers top-to-bottom, kept in sync
with the canvas's z-order and selection."""
from __future__ import annotations

import os
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .canvas_view import SceneCanvas
from .graphics_items import CharacterItem

ITEM_ROLE = Qt.ItemDataRole.UserRole


class LayersPanel(QWidget):
    """Lists character layers top-to-bottom, in sync with canvas z-order."""

    def __init__(self, canvas: SceneCanvas, parent=None):
        super().__init__(parent)
        self._canvas = canvas
        self._syncing = False

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.up_button = QPushButton("Move Up", self)
        self.down_button = QPushButton("Move Down", self)
        self.delete_button = QPushButton("Delete", self)

        button_row = QHBoxLayout()
        button_row.addWidget(self.up_button)
        button_row.addWidget(self.down_button)
        button_row.addWidget(self.delete_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_row)

        self.list_widget.itemSelectionChanged.connect(self._on_list_selection_changed)
        self.up_button.clicked.connect(self._on_move_up)
        self.down_button.clicked.connect(self._on_move_down)
        self.delete_button.clicked.connect(self._on_delete)

        self._canvas.selection_changed.connect(self._sync_selection_from_canvas)
        self._canvas.modified.connect(self.refresh)

        self.refresh()

    def refresh(self) -> None:
        self._syncing = True
        self.list_widget.clear()
        for index, item in enumerate(self._canvas.layers_top_to_bottom()):
            label = f"{index + 1}. {os.path.basename(item.source_path)}"
            list_item = QListWidgetItem(label)
            list_item.setData(ITEM_ROLE, item)
            self.list_widget.addItem(list_item)
        background = self._canvas.background_item()
        if background is not None:
            bg_item = QListWidgetItem(f"Background: {os.path.basename(background.source_path)}")
            bg_item.setFlags(bg_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            font = bg_item.font()
            font.setItalic(True)
            bg_item.setFont(font)
            self.list_widget.addItem(bg_item)
        self._syncing = False
        self._sync_selection_from_canvas()

    def _sync_selection_from_canvas(self) -> None:
        if self._syncing:
            return
        self._syncing = True
        selected = self._canvas.selected_character()
        self.list_widget.clearSelection()
        if selected is not None:
            for row in range(self.list_widget.count()):
                list_item = self.list_widget.item(row)
                if list_item.data(ITEM_ROLE) is selected:
                    list_item.setSelected(True)
                    self.list_widget.setCurrentItem(list_item)
                    break
        self._syncing = False

    def _on_list_selection_changed(self) -> None:
        if self._syncing:
            return
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        character = selected_items[0].data(ITEM_ROLE)
        if isinstance(character, CharacterItem):
            self._syncing = True
            self._canvas.select_character(character)
            self._syncing = False

    def _current_character(self) -> Optional[CharacterItem]:
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return None
        data = selected_items[0].data(ITEM_ROLE)
        return data if isinstance(data, CharacterItem) else None

    def _on_move_up(self) -> None:
        item = self._current_character()
        if item is not None:
            self._canvas.move_layer_up(item)

    def _on_move_down(self) -> None:
        item = self._current_character()
        if item is not None:
            self._canvas.move_layer_down(item)

    def _on_delete(self) -> None:
        item = self._current_character()
        if item is not None:
            self._canvas.delete_character(item)
