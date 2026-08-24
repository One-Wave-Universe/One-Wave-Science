"""Reusable slider+spinbox control bound to a Recipe field, plus a small
row widget for per-source amount/solo/mute."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QSlider,
    QWidget,
)

SLIDER_STEPS = 1000


class TraitSlider(QWidget):
    """A labelled slider bound to a float field on the current recipe via
    getter/setter callables, with an optional "lock" checkbox that keeps
    the trait out of Randomize."""

    def __init__(self, controller, label, getter, setter, minv, maxv,
                 decimals=2, lock_key=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.getter = getter
        self.setter = setter
        self.minv = minv
        self.maxv = maxv
        self.lock_key = lock_key
        self._suppress = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)

        self.lock_box = None
        if lock_key is not None:
            self.lock_box = QCheckBox()
            self.lock_box.setToolTip("Lock this trait (skip it when randomizing)")
            self.lock_box.toggled.connect(self._on_lock_toggled)
            layout.addWidget(self.lock_box)

        name_label = QLabel(label)
        name_label.setMinimumWidth(190)
        layout.addWidget(name_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(SLIDER_STEPS)
        self.slider.sliderPressed.connect(self._on_pressed)
        self.slider.valueChanged.connect(self._on_slider_changed)
        self.slider.sliderReleased.connect(self._on_released)
        layout.addWidget(self.slider, stretch=1)

        self.spin = QDoubleSpinBox()
        self.spin.setDecimals(decimals)
        self.spin.setRange(minv, maxv)
        self.spin.setSingleStep((maxv - minv) / 200.0 or 0.01)
        self.spin.valueChanged.connect(self._on_spin_changed)
        layout.addWidget(self.spin)

        self.refresh()
        controller.changed.connect(self.refresh)

    def _to_slider(self, value):
        span = self.maxv - self.minv
        return int(round((value - self.minv) / span * SLIDER_STEPS)) if span else 0

    def _from_slider(self, pos):
        return self.minv + (pos / SLIDER_STEPS) * (self.maxv - self.minv)

    def _on_pressed(self):
        self.controller.snapshot()

    def _on_slider_changed(self, pos):
        if self._suppress:
            return
        value = self._from_slider(pos)
        self.setter(self.controller.recipe, value)
        self._suppress = True
        self.spin.setValue(value)
        self._suppress = False

    def _on_spin_changed(self, value):
        if self._suppress:
            return
        self.controller.snapshot()
        self.setter(self.controller.recipe, value)
        self._suppress = True
        self.slider.setValue(self._to_slider(value))
        self._suppress = False
        self.controller.commit()

    def _on_released(self):
        self.controller.commit()

    def _on_lock_toggled(self, checked):
        locked = self.controller.recipe.locked_traits
        if checked and self.lock_key not in locked:
            locked.append(self.lock_key)
        elif not checked and self.lock_key in locked:
            locked.remove(self.lock_key)

    def refresh(self):
        value = self.getter(self.controller.recipe)
        self._suppress = True
        self.slider.setValue(self._to_slider(value))
        self.spin.setValue(value)
        self._suppress = False
        if self.lock_box is not None:
            self.lock_box.setChecked(self.lock_key in self.controller.recipe.locked_traits)


class BoolControl(QWidget):
    """A labelled checkbox bound to a boolean field on the current recipe."""

    def __init__(self, controller, label, getter, setter, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.getter = getter
        self.setter = setter

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)
        self.checkbox = QCheckBox(label)
        self.checkbox.toggled.connect(self._on_toggled)
        layout.addWidget(self.checkbox)
        layout.addStretch(1)

        self.refresh()
        controller.changed.connect(self.refresh)

    def _on_toggled(self, checked):
        self.controller.snapshot()
        self.setter(self.controller.recipe, checked)
        self.controller.commit()

    def refresh(self):
        self.checkbox.blockSignals(True)
        self.checkbox.setChecked(bool(self.getter(self.controller.recipe)))
        self.checkbox.blockSignals(False)
