"""Undo/redo-aware holder for the Recipe being edited."""
from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from engine.recipe import Recipe

MAX_HISTORY = 100


class RecipeController(QObject):
    changed = Signal()

    def __init__(self, recipe: Recipe | None = None):
        super().__init__()
        self._recipe = recipe if recipe is not None else Recipe()
        self._undo_stack: list[Recipe] = []
        self._redo_stack: list[Recipe] = []
        self.base_dir: str | None = None

    @property
    def recipe(self) -> Recipe:
        return self._recipe

    def replace(self, recipe: Recipe, base_dir: str | None = None) -> None:
        self._push_undo()
        self._recipe = recipe
        if base_dir is not None:
            self.base_dir = base_dir
        self.changed.emit()

    def snapshot(self) -> None:
        """Call before mutating .recipe in place, to make the change undoable."""
        self._push_undo()

    def commit(self) -> None:
        """Call after mutating .recipe in place, to notify listeners."""
        self.changed.emit()

    def _push_undo(self) -> None:
        self._undo_stack.append(self._recipe.clone())
        if len(self._undo_stack) > MAX_HISTORY:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self._redo_stack.append(self._recipe.clone())
        self._recipe = self._undo_stack.pop()
        self.changed.emit()
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        self._undo_stack.append(self._recipe.clone())
        self._recipe = self._redo_stack.pop()
        self.changed.emit()
        return True
