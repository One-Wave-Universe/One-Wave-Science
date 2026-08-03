"""Epicycle / phasor map: the raw waveform re-expressed as nested rotating
circles (a Fourier/harmonic decomposition) instead of flattened onto a
time axis.

This is a lossless geometric re-expression of the same captured samples,
not an interpretation layer -- chaining each harmonic's rotating vector
tip to tip and taking the real part of the final tip exactly reconstructs
the waveform (this is what a Fourier series *is*; using more harmonics
converges to the exact signal). The familiar linear "wavy line" waveform
is the real-axis projection of these rotating circles over time -- both
are drawn together, live, so that relationship is shown directly instead
of asserted.

Point Rotation = one circle (one harmonic) rotating at its own frequency
and radius. Path Rotation = the chained tip's trajectory as time advances
-- the accumulating trace on the right, and the spiral each circle's own
center traces if its amplitude changes (decay = inward spiral, attack =
outward spiral).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets

from onewave_mapper import fft_analyzer

CIRCLE_POINTS = 48
TRAIL_LENGTH = 600


@dataclass
class Epicycle:
    frequency_hz: float
    amplitude: float
    phase_rad: float


def compute_epicycles(signal: np.ndarray, sample_rate: float, max_harmonics: int = 10,
                       fft_size: int | None = None) -> list[Epicycle]:
    """Top max_harmonics frequency components by magnitude, ordered by
    ascending frequency (so the fundamental sits closest to the origin in
    the epicycle chain, the usual convention). This is a *finite* Fourier
    approximation -- exact reconstruction is the max_harmonics -> all-bins
    limit, same as any truncated Fourier series."""
    n = fft_size or min(8192, max(256, 1 << int(np.floor(np.log2(max(len(signal), 8))))))
    spectrum = fft_analyzer.compute_spectrum(signal, sample_rate, window="rectangular", fft_size=n)

    order = np.argsort(spectrum.magnitude)[::-1]
    order = order[spectrum.freqs_hz[order] > 0][:max_harmonics]  # skip DC, keep strongest positive-freq bins
    order = order[np.argsort(spectrum.freqs_hz[order])]  # re-sort ascending by frequency

    return [
        Epicycle(frequency_hz=float(spectrum.freqs_hz[i]), amplitude=float(spectrum.magnitude[i]),
                 phase_rad=float(spectrum.phase_rad[i]))
        for i in order
    ]


def epicycle_tip_positions(epicycles: list[Epicycle], t: float) -> np.ndarray:
    """Complex position of each circle's center (index 0 = origin) and the
    final reconstructed tip, at time t. Returns an array of length
    len(epicycles) + 1: centers[0]=0, centers[i+1] = tip after adding
    epicycle i."""
    positions = np.zeros(len(epicycles) + 1, dtype=complex)
    for i, cycle in enumerate(epicycles):
        vector = cycle.amplitude * np.exp(1j * (2 * np.pi * cycle.frequency_hz * t + cycle.phase_rad))
        positions[i + 1] = positions[i] + vector
    return positions


class EpicyclePanel(QtWidgets.QWidget):
    def __init__(self, sample_rate: int = 48000, max_harmonics: int = 8,
                 animation_interval_ms: int = 30, parent=None):
        super().__init__(parent)
        self.sample_rate = sample_rate
        self.max_harmonics = max_harmonics
        self.signal = np.zeros(0, dtype=np.float32)
        self.epicycles: list[Epicycle] = []
        self._t = 0.0
        self._trail: list[tuple] = []

        self._build_ui()

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(animation_interval_ms)

    def _build_ui(self) -> None:
        layout = QtWidgets.QHBoxLayout(self)

        self.circle_plot = pg.PlotWidget(title="Point Rotation -- nested epicycles")
        self.circle_plot.setAspectLocked(True)
        self.circle_plot.showGrid(x=True, y=True, alpha=0.2)
        self.circle_outline_curves: list = []
        self.radius_line = self.circle_plot.plot(pen=pg.mkPen((120, 160, 255), width=1.5))
        self.tip_marker = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(255, 80, 80))
        self.circle_plot.addItem(self.tip_marker)
        layout.addWidget(self.circle_plot, stretch=1)

        self.trace_plot = pg.PlotWidget(title="Path Rotation -- the same tip, unrolled over time")
        self.trace_plot.setLabel("bottom", "Time", units="s")
        self.trace_plot.setLabel("left", "Amplitude (real-axis projection)")
        self.trace_plot.showGrid(x=True, y=True, alpha=0.2)
        self.trace_curve = self.trace_plot.plot(pen=pg.mkPen((120, 220, 140), width=2))
        self.raw_curve = self.trace_plot.plot(pen=pg.mkPen((90, 90, 90), width=1))
        layout.addWidget(self.trace_plot, stretch=2)

    def set_signal(self, signal: np.ndarray, sample_rate: int) -> None:
        self.signal = signal
        self.sample_rate = sample_rate
        self.epicycles = compute_epicycles(signal, sample_rate, self.max_harmonics)
        self._t = 0.0
        self._trail = []
        self._redraw_raw_reference()

    def _redraw_raw_reference(self) -> None:
        if self.signal.size == 0:
            self.raw_curve.setData([], [])
            return
        window_seconds = min(2.0, self.signal.size / self.sample_rate)
        n = int(window_seconds * self.sample_rate)
        t = np.arange(n) / self.sample_rate
        self.raw_curve.setData(t, self.signal[:n])

    def _advance(self) -> None:
        if not self.epicycles:
            return
        dt = self._timer.interval() / 1000.0
        self._t += dt
        self._redraw_at(self._t)

    def _redraw_at(self, t: float) -> None:
        positions = epicycle_tip_positions(self.epicycles, t)

        for curve in self.circle_outline_curves:
            self.circle_plot.removeItem(curve)
        self.circle_outline_curves = []

        angles = np.linspace(0, 2 * np.pi, CIRCLE_POINTS)
        for i, cycle in enumerate(self.epicycles):
            center = positions[i]
            outline = center + cycle.amplitude * np.exp(1j * angles)
            curve = self.circle_plot.plot(outline.real, outline.imag, pen=pg.mkPen((90, 110, 140), width=1))
            self.circle_outline_curves.append(curve)

        self.radius_line.setData(positions.real, positions.imag)
        self.tip_marker.setData([positions[-1].real], [positions[-1].imag])

        reconstructed_value = float(positions[-1].real)
        self._trail.append((t, reconstructed_value))
        if len(self._trail) > TRAIL_LENGTH:
            self._trail = self._trail[-TRAIL_LENGTH:]
        trail_t = [p[0] for p in self._trail]
        trail_y = [p[1] for p in self._trail]
        self.trace_curve.setData(trail_t, trail_y)

    def reconstructed_value_at(self, t: float) -> float:
        """The epicycle chain's real-axis projection at time t -- should
        track the original raw signal closely as max_harmonics grows."""
        return float(epicycle_tip_positions(self.epicycles, t)[-1].real)
