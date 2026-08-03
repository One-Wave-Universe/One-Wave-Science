"""Modulation panel: slower changes acting on faster oscillations --
amplitude modulation, vibrato/frequency movement, tremolo, beating,
envelope movement -- kept on their own modulation-rate axis, separate
from the audio-rate carrier (Section 16.1).
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from scipy.signal import detrend
from PySide6 import QtWidgets

from onewave_mapper.envelope import hilbert_envelope
from onewave_mapper import cycles as cycles_module
from onewave_mapper.ui.analysis_state import AnalysisState

MAX_ANALYSIS_SAMPLES = 48000 * 5
MAX_MOD_HZ_DISPLAY = 30.0


class ModulationPanel(QtWidgets.QWidget):
    def __init__(self, state: AnalysisState, parent=None):
        super().__init__(parent)
        self.state = state
        self._build_ui()
        self._connect_state()
        self._redraw()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        self.envelope_ac_plot = pg.PlotWidget(title="Envelope movement (trend removed)")
        self.envelope_ac_plot.setLabel("bottom", "Time", units="s")
        self.envelope_ac_plot.showGrid(x=True, y=True, alpha=0.3)
        self.envelope_ac_curve = self.envelope_ac_plot.plot(pen=pg.mkPen((255, 165, 0)))
        layout.addWidget(self.envelope_ac_plot, stretch=1)

        self.spectrum_plot = pg.PlotWidget(title="Modulation-rate spectrum (amplitude and frequency)")
        self.spectrum_plot.setLabel("bottom", "Modulation frequency", units="Hz")
        self.spectrum_plot.setLabel("left", "Magnitude")
        self.spectrum_plot.setXRange(0, MAX_MOD_HZ_DISPLAY)
        self.spectrum_plot.showGrid(x=True, y=True, alpha=0.3)
        self.am_curve = self.spectrum_plot.plot(pen=pg.mkPen((255, 165, 0)), name="Amplitude modulation")
        self.fm_curve = self.spectrum_plot.plot(pen=pg.mkPen((100, 200, 255)), name="Frequency modulation")
        layout.addWidget(self.spectrum_plot, stretch=1)

        readout_layout = QtWidgets.QGridLayout()
        self.readout_labels: dict[str, QtWidgets.QLabel] = {}
        for i, name in enumerate(["AM rate (Hz)", "AM confidence", "FM rate (Hz)", "FM confidence"]):
            readout_layout.addWidget(QtWidgets.QLabel(f"{name}:"), 0, i * 2)
            value_label = QtWidgets.QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            readout_layout.addWidget(value_label, 0, i * 2 + 1)
            self.readout_labels[name] = value_label
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
        window, start_sample = self._analysis_window()
        if window.size < 64:
            for curve in (self.envelope_ac_curve, self.am_curve, self.fm_curve):
                curve.setData([], [])
            for label in self.readout_labels.values():
                label.setText("--")
            return

        sr = self.state.sample_rate
        envelope = hilbert_envelope(window)
        envelope_ac = detrend(envelope, type="linear")
        t = (start_sample + np.arange(len(window))) / sr
        self.envelope_ac_curve.setData(t, envelope_ac)

        am_result = cycles_module.modulation_spectrum(window, sr, feature="envelope")
        fm_result = cycles_module.modulation_spectrum(window, sr, feature="instantaneous_frequency")

        am_mask = am_result["freqs_hz"] <= MAX_MOD_HZ_DISPLAY
        fm_mask = fm_result["freqs_hz"] <= MAX_MOD_HZ_DISPLAY
        self.am_curve.setData(am_result["freqs_hz"][am_mask], am_result["magnitude"][am_mask])
        self.fm_curve.setData(fm_result["freqs_hz"][fm_mask], fm_result["magnitude"][fm_mask])

        am_cycle = cycles_module.detect_modulation_cycle(window, sr, min_confidence=0.0)
        fm_peak_index = int(np.argmax(fm_result["magnitude"][fm_mask])) if np.any(fm_mask) else None

        self.readout_labels["AM rate (Hz)"].setText(f"{am_cycle.frequency_hz:.2f}" if am_cycle else "--")
        self.readout_labels["AM confidence"].setText(f"{am_cycle.confidence:.2f}" if am_cycle else "--")
        if fm_peak_index is not None and fm_result["freqs_hz"][fm_mask][fm_peak_index] > 0:
            fm_freq = fm_result["freqs_hz"][fm_mask][fm_peak_index]
            fm_total = np.sum(fm_result["magnitude"][fm_mask])
            fm_confidence = fm_result["magnitude"][fm_mask][fm_peak_index] / fm_total if fm_total > 1e-12 else 0.0
            self.readout_labels["FM rate (Hz)"].setText(f"{fm_freq:.2f}")
            self.readout_labels["FM confidence"].setText(f"{fm_confidence:.2f}")
        else:
            self.readout_labels["FM rate (Hz)"].setText("--")
            self.readout_labels["FM confidence"].setText("--")
