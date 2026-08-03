"""Spectrum panel: FFT magnitude spectrum with each harmonic independently
identified and clickable, not merged into one generic brightness value.

Analyzes state.selection when one is active, otherwise the current view
range (capped for responsiveness) -- so selecting a region anywhere in the
mapper changes what this panel shows, per the "one selection" requirement.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets

from onewave_mapper import fft_analyzer, pitch as pitch_module, harmonics as harmonics_module
from onewave_mapper.ui.analysis_state import AnalysisState

MAX_ANALYSIS_SAMPLES = 32768
HIGHLIGHT_COLOR = (255, 60, 60)
NORMAL_COLOR = (100, 180, 255)


class SpectrumPanel(QtWidgets.QWidget):
    def __init__(self, state: AnalysisState, parent=None):
        super().__init__(parent)
        self.state = state
        self._harmonic_tracks: list = []

        self._build_ui()
        self._connect_state()
        self._redraw()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("bottom", "Frequency", units="Hz")
        self.plot_widget.setLabel("left", "Magnitude", units="dBFS")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.curve = self.plot_widget.plot(pen=pg.mkPen((120, 120, 120), width=1))

        self.harmonic_scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(*NORMAL_COLOR))
        self.harmonic_scatter.sigClicked.connect(self._on_harmonic_clicked)
        self.plot_widget.addItem(self.harmonic_scatter)

        self._harmonic_labels: list[pg.TextItem] = []

        layout.addWidget(self.plot_widget, stretch=1)

        readout_layout = QtWidgets.QHBoxLayout()
        readout_layout.addWidget(QtWidgets.QLabel("Fundamental (Hz):"))
        self.fundamental_label = QtWidgets.QLabel("--")
        self.fundamental_label.setStyleSheet("font-weight: bold;")
        readout_layout.addWidget(self.fundamental_label)
        readout_layout.addStretch(1)
        layout.addLayout(readout_layout)

    def _connect_state(self) -> None:
        self.state.recording_changed.connect(self._redraw)
        self.state.view_range_changed.connect(lambda *_: self._redraw())
        self.state.selection_changed.connect(lambda *_: self._redraw())
        self.state.highlighted_harmonic_changed.connect(lambda *_: self._refresh_harmonic_colors())

    def _analysis_window(self) -> tuple[np.ndarray, int]:
        signal = self.state.raw_signal
        n = len(signal)
        if n == 0:
            return np.zeros(0), 0

        if self.state.selection is not None:
            start, end = self.state.selection
        else:
            start, end = self.state.view_start_sample, self.state.view_end_sample

        start = int(np.clip(start, 0, n))
        end = int(np.clip(end, start + 1, n))
        if end - start > MAX_ANALYSIS_SAMPLES:
            end = start + MAX_ANALYSIS_SAMPLES
        return signal[start:end], start

    def _redraw(self) -> None:
        for label in self._harmonic_labels:
            self.plot_widget.removeItem(label)
        self._harmonic_labels = []
        self._harmonic_tracks = []

        window, _ = self._analysis_window()
        if window.size < 64:
            self.curve.setData([], [])
            self.harmonic_scatter.setData([])
            self.fundamental_label.setText("--")
            return

        sr = self.state.sample_rate
        fft_size = min(16384, max(256, 1 << int(np.floor(np.log2(window.size)))))
        spectrum = fft_analyzer.compute_spectrum(window, sr, window="hann", fft_size=fft_size)
        self.curve.setData(spectrum.freqs_hz, spectrum.magnitude_db)

        pitch_result = pitch_module.detect_pitch(window, sr, fmin=60, fmax=1500)
        if pitch_result.frequency_hz is None:
            self.harmonic_scatter.setData([])
            self.fundamental_label.setText("--")
            return

        self.fundamental_label.setText(f"{pitch_result.frequency_hz:.2f}")
        self._harmonic_tracks = harmonics_module.track_harmonics(spectrum, pitch_result.frequency_hz, max_harmonics=16)
        self._refresh_harmonic_colors()

    def _refresh_harmonic_colors(self) -> None:
        points = []
        for label in self._harmonic_labels:
            self.plot_widget.removeItem(label)
        self._harmonic_labels = []

        for track in self._harmonic_tracks:
            if track.measured_frequency_hz is None or track.amplitude is None:
                continue
            amplitude_db = 20 * np.log10(max(track.amplitude, 1e-12))
            is_highlighted = self.state.highlighted_harmonic == track.harmonic_number
            color = HIGHLIGHT_COLOR if is_highlighted else NORMAL_COLOR
            points.append({
                "pos": (track.measured_frequency_hz, amplitude_db),
                "data": track.harmonic_number,
                "brush": pg.mkBrush(*color),
                "size": 14 if is_highlighted else 10,
            })
            label = pg.TextItem(f"H{track.harmonic_number}", anchor=(0.5, 1.2), color=color)
            label.setPos(track.measured_frequency_hz, amplitude_db)
            self.plot_widget.addItem(label)
            self._harmonic_labels.append(label)

        self.harmonic_scatter.setData(points)

    def _on_harmonic_clicked(self, _scatter, spot_points) -> None:
        if not spot_points:
            return
        harmonic_number = spot_points[0].data()
        current = self.state.highlighted_harmonic
        self.state.set_highlighted_harmonic(None if current == harmonic_number else harmonic_number)
