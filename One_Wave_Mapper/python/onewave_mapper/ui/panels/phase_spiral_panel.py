"""Phase-space spiral: the raw signal as a single rotating, scaling
trajectory Psi(t) = A(t) * e^(j*theta(t)) -- A-110 Oscillation's own
defining form (Nodes/Appendix_A/A-110_Oscillation.md) -- computed
directly from the analytic signal (Hilbert transform), not a chained
per-harmonic decomposition (that was the wrong model -- see
epicycle_panel.py's docstring for the earlier, incorrect attempt).

A(t) = |Psi(t)| is exactly envelope.hilbert_envelope(signal); theta(t) =
angle(Psi(t)) is the same instantaneous phase already used in
phase_analysis.py and cursor_readout.py. Plotting Re(Psi) vs Im(Psi)
directly traces:

- Point Rotation: each fast small loop, one per waveform cycle.
- Path Rotation: the overall path those loops trace as A(t) changes --
  spiraling outward while a driven attack builds tension (A-105/A-106
  moving the state away from Ground), settling into a roughly
  constant-radius orbit during a sustained tone (A-107 Bounded Motion),
  spiraling inward as the restoring response pulls the state back toward
  Ground/Zero (A-101) during decay.

This is the same shape a decaying orbit, a settling spring, or a
dissipating vortex traces in its own phase space -- not a metaphor
specific to audio.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets
from scipy.signal import hilbert

TRAIL_LENGTH = 4000


def analytic_trajectory(signal: np.ndarray) -> np.ndarray:
    """Psi(t) = A(t) * e^(j*theta(t)), one complex sample per input sample."""
    return hilbert(signal)


class PhaseSpiralPanel(QtWidgets.QWidget):
    def __init__(self, sample_rate: int = 48000, playback_speed: float = 1.0,
                 refresh_interval_ms: int = 20, parent=None):
        super().__init__(parent)
        self.sample_rate = sample_rate
        self.playback_speed = playback_speed
        self.signal = np.zeros(0, dtype=np.float32)
        self.trajectory = np.zeros(0, dtype=complex)
        self._sample_cursor = 0.0

        self._build_ui()

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(refresh_interval_ms)

    def _build_ui(self) -> None:
        layout = QtWidgets.QHBoxLayout(self)

        self.spiral_plot = pg.PlotWidget(title="Phase-space trajectory -- Point + Path Rotation")
        self.spiral_plot.setAspectLocked(True)
        self.spiral_plot.setLabel("bottom", "Re(Psi)")
        self.spiral_plot.setLabel("left", "Im(Psi)")
        self.spiral_plot.showGrid(x=True, y=True, alpha=0.2)
        self.trail_curve = self.spiral_plot.plot(pen=pg.mkPen((120, 200, 255), width=1.5))
        self.tip_marker = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(255, 80, 80))
        self.spiral_plot.addItem(self.tip_marker)
        layout.addWidget(self.spiral_plot, stretch=1)

        self.envelope_plot = pg.PlotWidget(title="|Psi(t)| -- radius over time (building tension / restoring)")
        self.envelope_plot.setLabel("bottom", "Time", units="s")
        self.envelope_plot.setLabel("left", "Radius A(t)")
        self.envelope_plot.showGrid(x=True, y=True, alpha=0.2)
        self.envelope_curve = self.envelope_plot.plot(pen=pg.mkPen((255, 165, 0), width=2))
        self.envelope_cursor = pg.InfiniteLine(angle=90, pen=pg.mkPen((255, 80, 80), width=1))
        self.envelope_plot.addItem(self.envelope_cursor)
        layout.addWidget(self.envelope_plot, stretch=1)

    def set_signal(self, signal: np.ndarray, sample_rate: int) -> None:
        self.signal = signal
        self.sample_rate = sample_rate
        self.trajectory = analytic_trajectory(signal) if signal.size > 0 else np.zeros(0, dtype=complex)
        self._sample_cursor = 0.0

        if self.trajectory.size > 0:
            t = np.arange(len(self.trajectory)) / sample_rate
            self.envelope_curve.setData(t, np.abs(self.trajectory))
        else:
            self.envelope_curve.setData([], [])

        self._redraw()

    def _advance(self) -> None:
        if self.trajectory.size == 0:
            return
        dt_samples = self._timer.interval() / 1000.0 * self.sample_rate * self.playback_speed
        self._sample_cursor = (self._sample_cursor + dt_samples) % len(self.trajectory)
        self._redraw()

    def _redraw(self) -> None:
        if self.trajectory.size == 0:
            self.trail_curve.setData([], [])
            self.tip_marker.setData([])
            return

        cursor = int(self._sample_cursor)
        start = max(0, cursor - TRAIL_LENGTH)
        segment = self.trajectory[start:cursor + 1]
        if segment.size == 0:
            segment = self.trajectory[:1]

        self.trail_curve.setData(segment.real, segment.imag)
        tip = self.trajectory[cursor]
        self.tip_marker.setData([tip.real], [tip.imag])
        self.envelope_cursor.setPos(cursor / self.sample_rate)

    def radius_at(self, sample_index: int) -> float:
        return float(np.abs(self.trajectory[sample_index]))

    def angle_at(self, sample_index: int) -> float:
        return float(np.angle(self.trajectory[sample_index]))
