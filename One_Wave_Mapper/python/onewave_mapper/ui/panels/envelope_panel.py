"""Envelope panel: the waveform's changing outer shape, separated from its
rapid oscillation.

Upper and lower boundaries are drawn around the center zero line -- the
active oscillation range, not one positive-only amplitude curve. Stage
markers (attack, peak, rollover, sustain, decay, resolution) come from
envelope.py's real decay-fit measurements, not eyeballed positions.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets

from onewave_mapper.envelope import hilbert_envelope, measure_envelope
from onewave_mapper.ui.analysis_state import AnalysisState

STAGE_PEN = pg.mkPen((180, 180, 180), style=QtCore.Qt.DotLine)


class EnvelopePanel(QtWidgets.QWidget):
    def __init__(self, state: AnalysisState, parent=None):
        super().__init__(parent)
        self.state = state
        self._stage_lines: list[pg.InfiniteLine] = []
        self._stage_labels: list[pg.TextItem] = []

        self._build_ui()
        self._connect_state()
        self._redraw()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Envelope (upper/lower boundary)")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)

        self.zero_line = pg.InfiniteLine(angle=0, pos=0.0, pen=pg.mkPen((150, 150, 150), style=pg.QtCore.Qt.DashLine))
        self.plot_widget.addItem(self.zero_line)

        self.upper_curve = self.plot_widget.plot(pen=pg.mkPen((255, 165, 0), width=2))
        self.lower_curve = self.plot_widget.plot(pen=pg.mkPen((255, 165, 0), width=2))
        self.fill = pg.FillBetweenItem(self.upper_curve, self.lower_curve, brush=pg.mkBrush(255, 165, 0, 40))
        self.plot_widget.addItem(self.fill)

        layout.addWidget(self.plot_widget, stretch=1)

        readout_layout = QtWidgets.QGridLayout()
        self.readout_labels: dict[str, QtWidgets.QLabel] = {}
        for i, name in enumerate(["Attack (ms)", "Peak (s)", "Rollover (s)", "Decay -20dB (s)", "Decay -40dB (s)"]):
            readout_layout.addWidget(QtWidgets.QLabel(f"{name}:"), 0, i * 2)
            value_label = QtWidgets.QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            readout_layout.addWidget(value_label, 0, i * 2 + 1)
            self.readout_labels[name] = value_label
        layout.addLayout(readout_layout)

    def _connect_state(self) -> None:
        self.state.recording_changed.connect(self._redraw)
        self.state.view_range_changed.connect(lambda *_: self._redraw())

    def _redraw(self) -> None:
        signal = self.state.raw_signal
        sr = self.state.sample_rate
        n = len(signal)

        for line in self._stage_lines:
            self.plot_widget.removeItem(line)
        self._stage_lines = []
        for label in self._stage_labels:
            self.plot_widget.removeItem(label)
        self._stage_labels = []

        if n == 0:
            self.upper_curve.setData([], [])
            self.lower_curve.setData([], [])
            return

        start = int(np.clip(self.state.view_start_sample, 0, n))
        end = int(np.clip(self.state.view_end_sample, start + 1, n))
        segment = signal[start:end]

        if segment.size < 8:
            self.upper_curve.setData([], [])
            self.lower_curve.setData([], [])
            return

        envelope = hilbert_envelope(segment)
        t = (np.arange(start, end)) / sr
        self.upper_curve.setData(t, envelope)
        self.lower_curve.setData(t, -envelope)

        self._update_stage_markers(envelope, start, sr)

    def _update_stage_markers(self, envelope: np.ndarray, start_sample: int, sr: float) -> None:
        measurements = measure_envelope(envelope, sr)

        peak_value = float(np.max(envelope))
        peak_index = int(np.argmax(envelope))
        rollover_target = peak_value * 10 ** (-3 / 20.0)
        tail = envelope[peak_index:]
        below = np.where(tail <= rollover_target)[0]
        rollover_seconds = (peak_index + below[0]) / sr if below.size else None

        stages = []
        if measurements.attack_time_seconds is not None:
            stages.append(("Attack", measurements.attack_time_seconds))
        stages.append(("Peak", measurements.peak_time_seconds))
        if rollover_seconds is not None:
            stages.append(("Rollover", rollover_seconds))
        if measurements.decay_20db_seconds is not None:
            stages.append(("Decay -20dB", measurements.decay_20db_seconds))
        if measurements.decay_40db_seconds is not None:
            stages.append(("Resolution (-40dB)", measurements.decay_40db_seconds))

        for label_text, relative_seconds in stages:
            absolute_seconds = start_sample / sr + relative_seconds
            line = pg.InfiniteLine(angle=90, pos=absolute_seconds, pen=STAGE_PEN)
            self.plot_widget.addItem(line)
            self._stage_lines.append(line)

            text = pg.TextItem(label_text, anchor=(0, 1), color=(200, 200, 200))
            text.setPos(absolute_seconds, self.plot_widget.getViewBox().viewRange()[1][1])
            self.plot_widget.addItem(text)
            self._stage_labels.append(text)

        self.readout_labels["Attack (ms)"].setText(
            f"{measurements.attack_time_seconds * 1000:.1f}" if measurements.attack_time_seconds is not None else "--")
        self.readout_labels["Peak (s)"].setText(f"{measurements.peak_time_seconds:.4f}")
        self.readout_labels["Rollover (s)"].setText(f"{rollover_seconds:.4f}" if rollover_seconds is not None else "--")
        self.readout_labels["Decay -20dB (s)"].setText(
            f"{measurements.decay_20db_seconds:.4f}" if measurements.decay_20db_seconds is not None else "--")
        self.readout_labels["Decay -40dB (s)"].setText(
            f"{measurements.decay_40db_seconds:.4f}" if measurements.decay_40db_seconds is not None else "--")
