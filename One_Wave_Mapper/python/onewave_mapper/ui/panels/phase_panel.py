"""Phase panel: phase of the fundamental and major harmonics over time,
plus a circular phase display tied to the shared cursor.

Wrapped phase (-pi..pi) is plotted per harmonic so alignment, opposition,
drift, and locking between harmonics are all visible directly: two curves
sitting on top of each other are in phase; two curves offset by pi are in
opposition; a curve whose wrap rate doesn't match its harmonic's expected
frequency is drifting.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets

from onewave_mapper import pitch as pitch_module, harmonics as harmonics_module
from onewave_mapper import spectrogram as spectrogram_module
from onewave_mapper.ui.analysis_state import AnalysisState

MAX_ANALYSIS_SAMPLES = 48000 * 3
HARMONIC_COLORS = [(255, 255, 255), (255, 140, 0), (100, 200, 255), (200, 100, 255), (140, 255, 140)]


class PhasePanel(QtWidgets.QWidget):
    def __init__(self, state: AnalysisState, n_harmonics: int = 4, fft_size: int = 4096,
                 hop_size: int = 512, parent=None):
        super().__init__(parent)
        self.state = state
        self.n_harmonics = n_harmonics
        self.fft_size = fft_size
        self.hop_size = hop_size

        self._phase_tracks: list[dict] = []  # [{harmonic_number, times, phases}, ...]

        self._build_ui()
        self._connect_state()
        self._redraw()

    def _build_ui(self) -> None:
        layout = QtWidgets.QHBoxLayout(self)

        self.time_plot = pg.PlotWidget()
        self.time_plot.setLabel("bottom", "Time", units="s")
        self.time_plot.setLabel("left", "Phase (rad)")
        self.time_plot.setYRange(-np.pi * 1.1, np.pi * 1.1)
        self.time_plot.showGrid(x=True, y=True, alpha=0.3)
        self.harmonic_curves: list = []
        layout.addWidget(self.time_plot, stretch=3)

        self.circular_plot = pg.PlotWidget()
        self.circular_plot.setAspectLocked(True)
        self.circular_plot.setLabel("bottom", "cos(phase)")
        self.circular_plot.setLabel("left", "sin(phase)")
        angles = np.linspace(0, 2 * np.pi, 200)
        self.circular_plot.plot(np.cos(angles), np.sin(angles), pen=pg.mkPen((120, 120, 120)))
        self.circular_scatter = pg.ScatterPlotItem(size=12)
        self.circular_plot.addItem(self.circular_scatter)
        layout.addWidget(self.circular_plot, stretch=1)

    def _connect_state(self) -> None:
        self.state.recording_changed.connect(self._redraw)
        self.state.view_range_changed.connect(lambda *_: self._redraw())
        self.state.cursor_changed.connect(lambda *_: self._update_circular_display())
        self.state.highlighted_harmonic_changed.connect(lambda *_: self._refresh_highlight())

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
        for curve in self.harmonic_curves:
            self.time_plot.removeItem(curve)
        self.harmonic_curves = []
        self._phase_tracks = []

        window, start_sample = self._analysis_window()
        if window.size < self.fft_size:
            self._update_circular_display()
            return

        sr = self.state.sample_rate
        pitch_result = pitch_module.detect_pitch(window, sr, fmin=60, fmax=1500)
        if pitch_result.frequency_hz is None:
            self._update_circular_display()
            return

        spec = spectrogram_module.compute_spectrogram(window, sr, fft_size=self.fft_size, hop_size=self.hop_size)
        if spec.magnitude.shape[1] == 0:
            self._update_circular_display()
            return

        for harmonic_number in range(1, self.n_harmonics + 1):
            expected_freq = harmonic_number * pitch_result.frequency_hz
            if expected_freq >= sr / 2:
                break
            bin_index = int(np.argmin(np.abs(spec.freqs_hz - expected_freq)))
            phases = spec.phase_rad[bin_index, :]
            times = start_sample / sr + spec.times_seconds

            color = HARMONIC_COLORS[(harmonic_number - 1) % len(HARMONIC_COLORS)]
            curve = self.time_plot.plot(times, phases, pen=None, symbol="o", symbolSize=4,
                                         symbolBrush=color, symbolPen=None,
                                         name=f"H{harmonic_number}")
            self.harmonic_curves.append(curve)
            self._phase_tracks.append({"harmonic_number": harmonic_number, "times": times, "phases": phases,
                                        "curve": curve, "color": color})

        self._refresh_highlight()
        self._update_circular_display()

    def _refresh_highlight(self) -> None:
        """React to state.highlighted_harmonic -- e.g. clicking a peak in
        the spectrum panel emphasizes that same harmonic's phase curve here."""
        for track in self._phase_tracks:
            is_highlighted = self.state.highlighted_harmonic == track["harmonic_number"]
            size = 9 if is_highlighted else 4
            track["curve"].setSymbolSize(size)

    def _update_circular_display(self) -> None:
        if not self._phase_tracks:
            self.circular_scatter.setData([])
            return

        cursor_time = self.state.cursor_sample / self.state.sample_rate
        points = []
        for track_index, track in enumerate(self._phase_tracks):
            times = track["times"]
            phases = track["phases"]
            if len(times) == 0:
                continue
            nearest_index = int(np.argmin(np.abs(times - cursor_time)))
            phase = phases[nearest_index]
            color = HARMONIC_COLORS[track_index % len(HARMONIC_COLORS)]
            points.append({
                "pos": (np.cos(phase), np.sin(phase)),
                "brush": pg.mkBrush(*color),
                "data": track["harmonic_number"],
            })
        self.circular_scatter.setData(points)
