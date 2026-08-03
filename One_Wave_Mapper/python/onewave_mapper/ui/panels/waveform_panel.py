"""Raw waveform panel: an Audacity/oscilloscope-style time-domain view.

The plotted curve is always state.raw_signal sliced to the current view
range -- unmodified, never smoothed or replaced by a derived shape. Zero
line through the center, positive and negative displacement both visible
(Section: "Main waveform view"). One-Wave tag regions are drawn as an
overlay on top, never in place of, the raw curve, and only when
state.mode is ONE_WAVE or BOTH.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets

from onewave_mapper.trigger import TriggerEngine, TriggerConfig, TriggerType, TriggerEdge
from onewave_mapper import one_wave_views
from onewave_mapper import cycles as cycles_module
from onewave_mapper.ui.analysis_state import AnalysisState, ViewMode, TransportMode
from onewave_mapper.ui.cursor_readout import measure_at_cursor

EDGE_BY_LABEL = {"Rising": TriggerEdge.RISING, "Falling": TriggerEdge.FALLING,
                  "Either": TriggerEdge.EITHER}

# Point-cycle tick marks are only legible when zoomed in close enough to
# see individual waveform periods -- past this view width they'd just be
# visual noise, so they're skipped rather than drawn illegibly.
POINT_TICK_MAX_VIEW_SECONDS = 0.25
MAX_POINT_TICKS = 400

ONE_WAVE_TAG_COLORS = {
    "Inward": (255, 80, 80, 60),
    "Outward": (80, 160, 255, 60),
    "Across": (255, 220, 80, 60),
    "Over": (140, 255, 140, 60),
}

_FEEDBACK_EPSILON = 1e-6


class WaveformPanel(QtWidgets.QWidget):
    def __init__(self, state: AnalysisState, parent=None):
        super().__init__(parent)
        self.state = state
        self.trigger_engine = TriggerEngine(TriggerConfig(
            trigger_type=TriggerType.LEVEL, edge=TriggerEdge.RISING, threshold=0.0, hysteresis=0.02,
        ))
        self._one_wave_regions: list[pg.LinearRegionItem] = []
        self._point_tick_items: list[pg.InfiniteLine] = []
        self._path_region_items: list[pg.LinearRegionItem] = []
        self._suppress_selection_feedback = False
        self._suppress_cursor_feedback = False

        self._build_ui()
        self._connect_state()
        self._redraw()

    # -- construction ---------------------------------------------------

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        controls = QtWidgets.QHBoxLayout()

        controls.addWidget(QtWidgets.QLabel("Transport:"))
        self.transport_combo = QtWidgets.QComboBox()
        self.transport_combo.addItems([m.value for m in TransportMode])
        self.transport_combo.currentTextChanged.connect(
            lambda text: self.state.set_transport_mode(TransportMode(text)))
        controls.addWidget(self.transport_combo)

        controls.addSpacing(20)
        controls.addWidget(QtWidgets.QLabel("Trigger edge:"))
        self.edge_combo = QtWidgets.QComboBox()
        self.edge_combo.addItems(list(EDGE_BY_LABEL.keys()))
        self.edge_combo.currentTextChanged.connect(self._on_trigger_settings_changed)
        controls.addWidget(self.edge_combo)

        controls.addWidget(QtWidgets.QLabel("Threshold:"))
        self.threshold_spin = QtWidgets.QDoubleSpinBox()
        self.threshold_spin.setRange(-1.0, 1.0)
        self.threshold_spin.setSingleStep(0.01)
        self.threshold_spin.valueChanged.connect(self._on_trigger_settings_changed)
        controls.addWidget(self.threshold_spin)

        controls.addSpacing(20)
        self.zoom_sample_button = QtWidgets.QPushButton("Zoom: Sample")
        self.zoom_sample_button.clicked.connect(self.zoom_to_sample_level)
        controls.addWidget(self.zoom_sample_button)

        self.zoom_note_button = QtWidgets.QPushButton("Zoom: Note")
        self.zoom_note_button.clicked.connect(self.zoom_to_note_level)
        controls.addWidget(self.zoom_note_button)

        self.zoom_full_button = QtWidgets.QPushButton("Zoom: Full capture")
        self.zoom_full_button.clicked.connect(self.state.zoom_to_full_capture)
        controls.addWidget(self.zoom_full_button)

        controls.addStretch(1)
        layout.addLayout(controls)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Amplitude (normalized, dBFS reference)")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setYRange(-1.05, 1.05)
        self.curve = self.plot_widget.plot(pen=pg.mkPen(width=1.2))

        self.zero_line = pg.InfiniteLine(angle=0, pos=0.0, pen=pg.mkPen((150, 150, 150), style=QtCore.Qt.DashLine))
        self.plot_widget.addItem(self.zero_line)

        self.trigger_line = pg.InfiniteLine(angle=0, pos=0.0, pen=pg.mkPen((255, 140, 0), width=1))
        self.plot_widget.addItem(self.trigger_line)

        self.cursor_line = pg.InfiniteLine(angle=90, movable=True, pen=pg.mkPen((0, 200, 255), width=1.5))
        self.cursor_line.sigPositionChanged.connect(self._on_cursor_line_moved)
        self.plot_widget.addItem(self.cursor_line)

        self.selection_region = pg.LinearRegionItem(values=(0, 0), movable=True)
        self.selection_region.sigRegionChanged.connect(self._on_selection_region_changed)
        self.plot_widget.addItem(self.selection_region)

        self.plot_widget.getViewBox().wheelEvent = self._on_wheel

        layout.addWidget(self.plot_widget, stretch=1)

        readout_layout = QtWidgets.QGridLayout()
        self.readout_labels: dict[str, QtWidgets.QLabel] = {}
        for i, name in enumerate(["Time (s)", "Amplitude", "Frequency (Hz)", "Note", "Phase (rad)"]):
            readout_layout.addWidget(QtWidgets.QLabel(f"{name}:"), 0, i * 2)
            value_label = QtWidgets.QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            readout_layout.addWidget(value_label, 0, i * 2 + 1)
            self.readout_labels[name] = value_label
        layout.addLayout(readout_layout)

    def _connect_state(self) -> None:
        self.state.recording_changed.connect(self._redraw)
        self.state.view_range_changed.connect(lambda *_: self._redraw())
        self.state.cursor_changed.connect(self._on_state_cursor_changed)
        self.state.selection_changed.connect(self._on_state_selection_changed)
        self.state.trigger_point_changed.connect(self._on_state_trigger_changed)
        self.state.mode_changed.connect(lambda *_: self._redraw())
        self.state.cycle_visibility_changed.connect(lambda *_: self._redraw())

    # -- zoom presets -----------------------------------------------------

    def zoom_to_sample_level(self) -> None:
        self.state.zoom_to_samples(self.state.cursor_sample, 256)

    def zoom_to_note_level(self) -> None:
        self.state.zoom_to_note(self.state.cursor_sample, note_duration_seconds=1.0)

    # -- mouse interaction --------------------------------------------------

    def _on_wheel(self, event) -> None:
        n = len(self.state.raw_signal)
        if n == 0:
            return
        width = max(1, self.state.view_end_sample - self.state.view_start_sample)
        zoom_in = event.angleDelta().y() > 0
        factor = 0.8 if zoom_in else 1.25
        new_width = max(16, int(width * factor))

        mouse_point = self.plot_widget.getViewBox().mapSceneToView(event.scenePos())
        center_sample = int(mouse_point.x() * self.state.sample_rate)
        left_fraction = (center_sample - self.state.view_start_sample) / width if width else 0.5

        new_start = center_sample - int(new_width * left_fraction)
        self.state.set_view_range(new_start, new_start + new_width)
        event.accept()

    def _on_cursor_line_moved(self) -> None:
        if self._suppress_cursor_feedback:
            return
        sample_index = int(round(self.cursor_line.value() * self.state.sample_rate))
        self.state.set_cursor(sample_index)

    def _on_selection_region_changed(self) -> None:
        if self._suppress_selection_feedback:
            return
        low, high = self.selection_region.getRegion()
        sr = self.state.sample_rate
        self.state.set_selection(int(low * sr), int(high * sr))

    # -- state -> view -------------------------------------------------------

    def _on_state_cursor_changed(self, sample_index: int) -> None:
        target = sample_index / self.state.sample_rate
        if abs(self.cursor_line.value() - target) > _FEEDBACK_EPSILON:
            self._suppress_cursor_feedback = True
            self.cursor_line.setValue(target)
            self._suppress_cursor_feedback = False
        self._update_readouts(sample_index)

    def _on_state_selection_changed(self, selection) -> None:
        sr = self.state.sample_rate
        target = (0, 0) if selection is None else (selection[0] / sr, selection[1] / sr)
        current = self.selection_region.getRegion()
        if abs(current[0] - target[0]) > _FEEDBACK_EPSILON or abs(current[1] - target[1]) > _FEEDBACK_EPSILON:
            self._suppress_selection_feedback = True
            self.selection_region.setRegion(target)
            self._suppress_selection_feedback = False

    def _on_state_trigger_changed(self, sample_index) -> None:
        if sample_index is None:
            self.trigger_line.setVisible(False)
        else:
            self.trigger_line.setVisible(True)
            self.trigger_line.setPos(self.threshold_spin.value())

    def _on_trigger_settings_changed(self, *_args) -> None:
        self.trigger_engine.config.edge = EDGE_BY_LABEL[self.edge_combo.currentText()]
        self.trigger_engine.config.threshold = self.threshold_spin.value()
        self.trigger_line.setPos(self.threshold_spin.value())

    def _update_readouts(self, sample_index: int) -> None:
        readout = measure_at_cursor(self.state.raw_signal, self.state.sample_rate, sample_index)
        self.readout_labels["Time (s)"].setText(f"{readout.time_seconds:.4f}")
        self.readout_labels["Amplitude"].setText(f"{readout.amplitude:.4f}")
        self.readout_labels["Frequency (Hz)"].setText(
            f"{readout.frequency_hz:.2f}" if readout.frequency_hz else "--")
        self.readout_labels["Note"].setText(
            f"{readout.note_name} ({readout.cents_offset:+.0f}c)" if readout.note_name else "--")
        self.readout_labels["Phase (rad)"].setText(
            f"{readout.phase_rad:.3f}" if readout.phase_rad is not None else "--")

    # -- redraw --------------------------------------------------------------

    def _redraw(self) -> None:
        signal = self.state.raw_signal
        sr = self.state.sample_rate
        n = len(signal)
        if n == 0:
            self.curve.setData([], [])
            return

        start = int(np.clip(self.state.view_start_sample, 0, n))
        end = int(np.clip(self.state.view_end_sample, start + 1, n))
        segment = signal[start:end]
        t = (np.arange(start, end)) / sr
        self.curve.setData(t, segment)

        self._redraw_one_wave_overlays(segment, start, sr)
        self._redraw_cycle_overlays(segment, start, sr)

    def _redraw_one_wave_overlays(self, segment: np.ndarray, start_sample: int, sr: float) -> None:
        for region in self._one_wave_regions:
            self.plot_widget.removeItem(region)
        self._one_wave_regions = []

        if self.state.mode == ViewMode.RAW or segment.size < 64:
            return

        # classify_window's start_sample/end_sample describe a sub-window of
        # the *signal it's given*, not an absolute offset into a larger
        # array -- so it's called on `segment` itself (tags come back with
        # segment-local sample coordinates), and start_sample is added back
        # in below to place the overlay at the correct absolute time.
        tags = one_wave_views.classify_window(segment, sr)
        for tag in tags:
            color = ONE_WAVE_TAG_COLORS.get(tag.tag, (200, 200, 200, 50))
            region = pg.LinearRegionItem(
                values=((start_sample + tag.start_sample) / sr, (start_sample + tag.end_sample) / sr),
                brush=pg.mkBrush(*color), movable=False,
            )
            region.setZValue(-10)
            self.plot_widget.addItem(region)
            self._one_wave_regions.append(region)

    def _redraw_cycle_overlays(self, segment: np.ndarray, start_sample: int, sr: float) -> None:
        """Nested Point/Path motion (Section 16.3), each independently
        toggleable. Point ticks are skipped above POINT_TICK_MAX_VIEW_SECONDS
        -- past that zoom level they'd just be illegible clutter, not a
        missing feature."""
        for item in self._point_tick_items:
            self.plot_widget.removeItem(item)
        self._point_tick_items = []
        for region in self._path_region_items:
            self.plot_widget.removeItem(region)
        self._path_region_items = []

        if self.state.mode == ViewMode.RAW or segment.size < 64:
            return

        view_seconds = segment.size / sr

        if self.state.show_point_rotation and view_seconds <= POINT_TICK_MAX_VIEW_SECONDS:
            point_cycles = cycles_module.detect_point_cycles(segment, sr, max_cycles=MAX_POINT_TICKS)
            y_range = self.plot_widget.getViewBox().viewRange()[1]
            tick_y = y_range[0] + 0.05 * (y_range[1] - y_range[0])
            for cycle in point_cycles:
                tick_time = (start_sample + cycle.start_sample) / sr
                tick = pg.InfiniteLine(angle=90, pos=tick_time, pen=pg.mkPen((120, 220, 120), width=1))
                tick.setBounds([None, None])
                self.plot_widget.addItem(tick)
                self._point_tick_items.append(tick)

        if self.state.show_path_rotation:
            onset_engine = TriggerEngine(TriggerConfig(trigger_type=TriggerType.NOTE_ONSET))
            onsets = onset_engine.find_triggers(segment, sr)
            boundaries = [0] + [int(o) for o in onsets] + [segment.size]
            boundaries = sorted(set(boundaries))
            for path_start, path_end in zip(boundaries[:-1], boundaries[1:]):
                if path_end - path_start < 64:
                    continue
                region = pg.LinearRegionItem(
                    values=((start_sample + path_start) / sr, (start_sample + path_end) / sr),
                    brush=pg.mkBrush(160, 100, 255, 25), movable=False,
                )
                region.setZValue(-20)
                region.lines[0].setPen(pg.mkPen((160, 100, 255), width=1))
                region.lines[1].setPen(pg.mkPen((160, 100, 255), width=1))
                self.plot_widget.addItem(region)
                self._path_region_items.append(region)

    def find_and_set_trigger(self) -> None:
        """Run the trigger engine over the current raw recording and update
        state.trigger_sample to the most recent trigger event, if any."""
        signal = self.state.raw_signal
        if len(signal) < 8:
            return
        triggers = self.trigger_engine.find_triggers(signal, self.state.sample_rate)
        self.state.set_trigger_point(int(triggers[-1]) if triggers.size > 0 else None)
