"""Spectrogram panel: frequency vertically, time horizontally, measured
strength through intensity -- zoomable (pyqtgraph's native wheel/drag
zoom on the ViewBox) so harmonic birth, movement, persistence, and
disappearance across time are actually followable.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets

from onewave_mapper import spectrogram as spectrogram_module
from onewave_mapper.ui.analysis_state import AnalysisState

MAX_ANALYSIS_SAMPLES = 48000 * 5  # cap at 5 seconds for responsiveness


class SpectrogramPanel(QtWidgets.QWidget):
    def __init__(self, state: AnalysisState, fft_size: int = 2048, hop_size: int = 256, parent=None):
        super().__init__(parent)
        self.state = state
        self.fft_size = fft_size
        self.hop_size = hop_size

        self._build_ui()
        self._connect_state()
        self._redraw()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Frequency", units="Hz")

        self.image_item = pg.ImageItem()
        colormap = pg.colormap.get("viridis")
        self.image_item.setColorMap(colormap)
        self.plot_widget.addItem(self.image_item)

        layout.addWidget(self.plot_widget, stretch=1)

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
        if window.size < self.fft_size:
            self.image_item.clear()
            return

        sr = self.state.sample_rate
        spec = spectrogram_module.compute_spectrogram(window, sr, fft_size=self.fft_size, hop_size=self.hop_size)
        if spec.magnitude.shape[1] == 0:
            self.image_item.clear()
            return

        image_data = spec.magnitude_db.T  # (n_frames, n_freq_bins) for pg.ImageItem's (x, y) convention
        self.image_item.setImage(image_data, autoLevels=True)

        t0 = start_sample / sr
        t_span = spec.times_seconds[-1] - spec.times_seconds[0] if len(spec.times_seconds) > 1 else 1.0 / sr
        f_span = spec.freqs_hz[-1] if len(spec.freqs_hz) else sr / 2
        self.image_item.setRect(QtCore.QRectF(t0, 0.0, max(t_span, 1e-6), f_span))
