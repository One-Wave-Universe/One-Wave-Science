"""Resonance panel: a persistence trail showing which frequency structures
remain active after the initial attack weakens.

Each detected resonance (resonance.detect_resonances, Section 15) is drawn
as a horizontal segment from its start to end time at its center
frequency -- color encodes decay rate (blue = slow/persistent, red = fast
decay), line width encodes persistence_score. This is a trail over time,
not a single freeze-frame of the finished spectrum.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets

from onewave_mapper import resonance as resonance_module
from onewave_mapper.ui.analysis_state import AnalysisState

MAX_ANALYSIS_SAMPLES = 48000 * 5


def _decay_rate_color(decay_rate_db_per_second: float | None) -> tuple:
    if decay_rate_db_per_second is None:
        return (150, 150, 150)
    # clamp to a reasonable range and map slow decay (near 0) -> blue,
    # fast decay (very negative) -> red
    clamped = float(np.clip(decay_rate_db_per_second, -80.0, 0.0))
    fraction = -clamped / 80.0  # 0 (slow) .. 1 (fast)
    red = int(80 + fraction * 175)
    blue = int(255 - fraction * 175)
    return (red, 100, blue)


class ResonancePanel(QtWidgets.QWidget):
    def __init__(self, state: AnalysisState, fft_size: int = 4096, hop_size: int = 1024, parent=None):
        super().__init__(parent)
        self.state = state
        self.fft_size = fft_size
        self.hop_size = hop_size
        self._trail_items: list[pg.PlotDataItem] = []
        self._events: list = []

        self._build_ui()
        self._connect_state()
        self._redraw()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Frequency", units="Hz")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        layout.addWidget(self.plot_widget, stretch=1)

        readout_layout = QtWidgets.QHBoxLayout()
        readout_layout.addWidget(QtWidgets.QLabel("Resonance candidates found:"))
        self.count_label = QtWidgets.QLabel("--")
        self.count_label.setStyleSheet("font-weight: bold;")
        readout_layout.addWidget(self.count_label)
        readout_layout.addStretch(1)
        layout.addLayout(readout_layout)

    def _connect_state(self) -> None:
        self.state.recording_changed.connect(self._redraw)
        self.state.view_range_changed.connect(lambda *_: self._redraw())

    def _analysis_window(self) -> tuple[np.ndarray, int]:
        signal = self.state.raw_signal
        n = len(signal)
        if n == 0:
            return np.zeros(0), 0
        start = int(np.clip(self.state.view_start_sample, 0, n))
        end = int(np.clip(self.state.view_end_sample, start + 1, n))
        if end - start > MAX_ANALYSIS_SAMPLES:
            end = start + MAX_ANALYSIS_SAMPLES
        return signal[start:end], start

    def _redraw(self) -> None:
        for item in self._trail_items:
            self.plot_widget.removeItem(item)
        self._trail_items = []
        self._events = []

        window, start_sample = self._analysis_window()
        if window.size < self.fft_size:
            self.count_label.setText("--")
            return

        sr = self.state.sample_rate
        events = resonance_module.detect_resonances(window, sr, fft_size=self.fft_size, hop_size=self.hop_size)
        self._events = events
        self.count_label.setText(str(len(events)))

        for event in events:
            t0 = (start_sample + event.start_sample) / sr
            t1 = (start_sample + event.end_sample) / sr
            color = _decay_rate_color(event.decay_rate_db_per_second)
            width = 1 + 6 * event.persistence_score
            item = self.plot_widget.plot(
                [t0, t1], [event.center_frequency_hz, event.center_frequency_hz],
                pen=pg.mkPen(color, width=width),
            )
            self._trail_items.append(item)
