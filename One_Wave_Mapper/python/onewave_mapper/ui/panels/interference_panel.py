"""Interference panel: two source waveforms shown separately, their real
sum and difference, a time-varying reinforcing/cancelling boundary, and
beat measurements -- never just the finished combined chord (per spec:
"Claude must not display only the finished combined chord. We need to
see how the individual waves produce that combined result.").

Live capture in this engine is single-channel, so this panel drives its
own pair of sources (two adjustable synthetic tones by default, or any
two signals set via set_sources) rather than depending on the shared
recording -- it reuses interference.py end to end either way.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets

from onewave_mapper import signal_generator, interference as interference_module


class InterferencePanel(QtWidgets.QWidget):
    def __init__(self, sample_rate: int = 48000, parent=None):
        super().__init__(parent)
        self.sample_rate = sample_rate
        self.source_a = np.zeros(0, dtype=np.float32)
        self.source_b = np.zeros(0, dtype=np.float32)

        self._build_ui()
        self.generate_demo_sources()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        controls = QtWidgets.QHBoxLayout()
        controls.addWidget(QtWidgets.QLabel("Source A (Hz):"))
        self.freq_a_spin = QtWidgets.QDoubleSpinBox()
        self.freq_a_spin.setRange(20.0, 5000.0)
        self.freq_a_spin.setValue(440.0)
        controls.addWidget(self.freq_a_spin)

        controls.addWidget(QtWidgets.QLabel("Source B (Hz):"))
        self.freq_b_spin = QtWidgets.QDoubleSpinBox()
        self.freq_b_spin.setRange(20.0, 5000.0)
        self.freq_b_spin.setValue(442.0)
        controls.addWidget(self.freq_b_spin)

        self.generate_button = QtWidgets.QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_demo_sources)
        controls.addWidget(self.generate_button)
        controls.addStretch(1)
        layout.addLayout(controls)

        self.plot_a = self._make_mini_plot("Source A")
        self.plot_b = self._make_mini_plot("Source B")
        self.plot_sum = self._make_mini_plot("Combined (sum)")
        self.plot_diff = self._make_mini_plot("Difference")
        self.plot_boundary = self._make_mini_plot("Interference boundary (dB, 0 = fully constructive)")

        for plot in (self.plot_a.getPlotItem(), self.plot_b.getPlotItem(), self.plot_sum.getPlotItem(),
                     self.plot_diff.getPlotItem(), self.plot_boundary.getPlotItem()):
            plot.setXLink(self.plot_a.getPlotItem())

        for plot_widget in (self.plot_a, self.plot_b, self.plot_sum, self.plot_diff, self.plot_boundary):
            layout.addWidget(plot_widget, stretch=1)

        self.curve_a = self.plot_a.plot(pen=pg.mkPen((100, 200, 255)))
        self.curve_b = self.plot_b.plot(pen=pg.mkPen((255, 160, 100)))
        self.curve_sum = self.plot_sum.plot(pen=pg.mkPen((255, 255, 255)))
        self.curve_diff = self.plot_diff.plot(pen=pg.mkPen((200, 100, 255)))
        self.curve_boundary = self.plot_boundary.plot(pen=pg.mkPen((100, 255, 100)))
        self.boundary_zero_line = pg.InfiniteLine(angle=0, pos=0.0, pen=pg.mkPen((150, 150, 150)))
        self.plot_boundary.addItem(self.boundary_zero_line)

        readout_layout = QtWidgets.QGridLayout()
        self.readout_labels: dict[str, QtWidgets.QLabel] = {}
        fields = ["Beat frequency (Hz)", "Beat stability", "Constructive score",
                  "Destructive score", "Cancellation depth (dB)", "Reinforcement gain (dB)"]
        for i, name in enumerate(fields):
            row, col = divmod(i, 3)
            readout_layout.addWidget(QtWidgets.QLabel(f"{name}:"), row, col * 2)
            value_label = QtWidgets.QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            readout_layout.addWidget(value_label, row, col * 2 + 1)
            self.readout_labels[name] = value_label
        layout.addLayout(readout_layout)

    def _make_mini_plot(self, title: str) -> pg.PlotWidget:
        plot_widget = pg.PlotWidget(title=title)
        plot_widget.showGrid(x=True, y=True, alpha=0.25)
        plot_widget.setMaximumHeight(140)
        return plot_widget

    def generate_demo_sources(self) -> None:
        duration = 1.0
        a = signal_generator.sine(self.freq_a_spin.value(), duration, self.sample_rate, amplitude=0.5)
        b = signal_generator.sine(self.freq_b_spin.value(), duration, self.sample_rate, amplitude=0.5)
        self.set_sources(a, b, self.sample_rate)

    def set_sources(self, source_a: np.ndarray, source_b: np.ndarray, sample_rate: int) -> None:
        n = min(len(source_a), len(source_b))
        self.sample_rate = sample_rate
        self.source_a = source_a[:n]
        self.source_b = source_b[:n]
        self._redraw()

    def _redraw(self) -> None:
        a, b, sr = self.source_a, self.source_b, self.sample_rate
        n = len(a)
        if n < 8:
            for curve in (self.curve_a, self.curve_b, self.curve_sum, self.curve_diff, self.curve_boundary):
                curve.setData([], [])
            return

        t = np.arange(n) / sr
        combined = interference_module.sum_signal(a, b)
        difference = interference_module.difference_signal(a, b)

        self.curve_a.setData(t, a)
        self.curve_b.setData(t, b)
        self.curve_sum.setData(t, combined)
        self.curve_diff.setData(t, difference)

        boundary_t, boundary_db = self._time_varying_boundary(a, b, sr)
        self.curve_boundary.setData(boundary_t, boundary_db)

        scores = interference_module.interference_scores(a, b, sr)
        beats = interference_module.detect_beats(combined, sr)

        self.readout_labels["Beat frequency (Hz)"].setText(
            f"{beats.beat_frequency_hz:.2f}" if beats.beat_frequency_hz is not None else "--")
        self.readout_labels["Beat stability"].setText(
            f"{beats.stability:.2f}" if beats.stability is not None else "--")
        self.readout_labels["Constructive score"].setText(f"{scores.constructive_score:.3f}")
        self.readout_labels["Destructive score"].setText(f"{scores.destructive_score:.3f}")
        self.readout_labels["Cancellation depth (dB)"].setText(f"{scores.cancellation_depth_db:.2f}")
        self.readout_labels["Reinforcement gain (dB)"].setText(f"{scores.reinforcement_gain_db:.2f}")

    def _time_varying_boundary(self, a: np.ndarray, b: np.ndarray, sr: float,
                                window_ms: float = 20.0) -> tuple[np.ndarray, np.ndarray]:
        """Windowed constructive/destructive boundary over time: 0 dB means
        that window combined as constructively as |a|+|b| allows; more
        negative means more destructive cancellation in that window."""
        window_samples = max(8, int(sr * window_ms / 1000.0))
        n = len(a)
        n_windows = n // window_samples
        if n_windows < 1:
            return np.array([]), np.array([])

        times = np.zeros(n_windows)
        boundary_db = np.zeros(n_windows)
        for i in range(n_windows):
            start = i * window_samples
            end = start + window_samples
            combined_rms = np.sqrt(np.mean((a[start:end] + b[start:end]) ** 2))
            predicted_rms = np.sqrt(np.mean((np.abs(a[start:end]) + np.abs(b[start:end])) ** 2))
            times[i] = (start + window_samples / 2) / sr
            boundary_db[i] = 20 * np.log10(max(combined_rms, 1e-12) / max(predicted_rms, 1e-12))

        return times, boundary_db
