"""Live oscilloscope window (Section 6, Section 20).

Wired directly to the tested DSP core -- RingBuffer for live history,
TriggerEngine for the rising/falling/either-edge trigger with threshold
and hysteresis, metering.measure() for the scope readouts -- rather than
reimplementing any of that inside the UI. The vertical axis is labeled
"normalized, dBFS reference" and never volts, per Section 4.2, since no
CalibrationProfile is wired in here.

Verified in tests/test_gui_smoke.py against Qt's offscreen platform: the
window constructs, the plotted curve and readouts actually change across
timer ticks while a source is running, Freeze stops that, and a grabbed
screenshot is a real, non-blank image. That is not the same as having
been looked at on a real screen with real audio hardware -- there is
neither in the container this was built in.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets

from onewave_mapper.ring_buffer import RingBuffer
from onewave_mapper.trigger import TriggerEngine, TriggerConfig, TriggerType, TriggerEdge
from onewave_mapper import metering, pitch as pitch_module, wavelength as wavelength_module
from onewave_mapper import one_wave_views
from onewave_mapper.envelope import hilbert_envelope
from onewave_mapper.ui.live_sources import SyntheticSource

READOUT_FIELDS = ["Peak", "Peak-to-peak", "RMS", "DC offset", "Zero-crossing rate (Hz)",
                   "Pitch (Hz)", "Note", "Wavelength (m)", "Clipped samples", "Trigger status",
                   "Life-cycle state"]

EDGE_BY_LABEL = {"Rising": TriggerEdge.RISING, "Falling": TriggerEdge.FALLING,
                  "Either": TriggerEdge.EITHER}


class OscilloscopeWindow(QtWidgets.QMainWindow):
    def __init__(self, sample_rate: int = 48000, ring_buffer_seconds: float = 5.0,
                 refresh_interval_ms: int = 50, envelope_window_seconds: float = 2.0,
                 envelope_refresh_interval_ms: int = 150, parent=None):
        super().__init__(parent)
        self.setWindowTitle("One-Wave Mapper — Oscilloscope")

        self.sample_rate = sample_rate
        self.ring_buffer = RingBuffer(1, int(ring_buffer_seconds * sample_rate), sample_rate)
        self.source: SyntheticSource | None = None
        self.trigger_engine = TriggerEngine(TriggerConfig(
            trigger_type=TriggerType.LEVEL, edge=TriggerEdge.RISING, threshold=0.0, hysteresis=0.02,
        ))
        self.frozen = False
        self.envelope_window_seconds = envelope_window_seconds

        self._build_ui()

        self._refresh_timer = QtCore.QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start(refresh_interval_ms)

        # a slower, separate timer for the life-cycle envelope panel --
        # it looks at seconds of history (growth/sustain/decay), not the
        # millisecond-scale trigger window, so it doesn't need to redraw
        # at the scope's frame rate (Section 22.3 treats these as
        # different-latency-tier displays).
        self._envelope_timer = QtCore.QTimer(self)
        self._envelope_timer.timeout.connect(self._refresh_envelope)
        self._envelope_timer.start(envelope_refresh_interval_ms)

    def _build_ui(self) -> None:
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)

        controls = QtWidgets.QHBoxLayout()

        self.source_combo = QtWidgets.QComboBox()
        self.source_combo.addItems(["Synthetic: 220 Hz sine", "Synthetic: guitar note"])
        controls.addWidget(QtWidgets.QLabel("Source:"))
        controls.addWidget(self.source_combo)

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self._on_start_clicked)
        controls.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        controls.addWidget(self.stop_button)

        self.freeze_button = QtWidgets.QPushButton("Freeze")
        self.freeze_button.setCheckable(True)
        self.freeze_button.toggled.connect(self._on_freeze_toggled)
        controls.addWidget(self.freeze_button)

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
        self.threshold_spin.setValue(0.0)
        self.threshold_spin.valueChanged.connect(self._on_trigger_settings_changed)
        controls.addWidget(self.threshold_spin)

        controls.addWidget(QtWidgets.QLabel("Window (ms):"))
        self.window_spin = QtWidgets.QDoubleSpinBox()
        self.window_spin.setRange(1.0, 500.0)
        self.window_spin.setValue(20.0)
        controls.addWidget(self.window_spin)

        controls.addStretch(1)
        layout.addLayout(controls)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Amplitude (normalized, dBFS reference)")
        self.plot_widget.setYRange(-1.05, 1.05)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.curve = self.plot_widget.plot(pen=pg.mkPen(width=2))
        layout.addWidget(self.plot_widget, stretch=2)

        # the life-cycle panel: the envelope over seconds of history, not
        # one triggered waveform slice -- growth (attack), living
        # (sustain), decay (release) as the note actually plays out, per
        # Section 11 and the Point/Path nested-cycle structure of Section 16.
        self.envelope_plot_widget = pg.PlotWidget()
        self.envelope_plot_widget.setLabel("bottom", "Time", units="s")
        self.envelope_plot_widget.setLabel("left", "Envelope (Hilbert amplitude)")
        self.envelope_plot_widget.setYRange(0.0, 1.05)
        self.envelope_plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.envelope_curve = self.envelope_plot_widget.plot(pen=pg.mkPen(width=2, color="orange"))
        layout.addWidget(self.envelope_plot_widget, stretch=1)

        readout_layout = QtWidgets.QGridLayout()
        self.readout_labels: dict[str, QtWidgets.QLabel] = {}
        for i, name in enumerate(READOUT_FIELDS):
            row, col = divmod(i, 4)
            readout_layout.addWidget(QtWidgets.QLabel(f"{name}:"), row, col * 2)
            value_label = QtWidgets.QLabel("--")
            value_label.setStyleSheet("font-weight: bold;")
            readout_layout.addWidget(value_label, row, col * 2 + 1)
            self.readout_labels[name] = value_label
        layout.addLayout(readout_layout)

        self.setCentralWidget(central)
        self.resize(900, 600)

    # -- source control --------------------------------------------------

    def _on_start_clicked(self) -> None:
        if self.source is not None:
            return
        waveform = "sine" if "sine" in self.source_combo.currentText() else "guitar_note"
        self.source = SyntheticSource(self.ring_buffer, self.sample_rate, waveform=waveform)
        self.source.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.source_combo.setEnabled(False)

    def _on_stop_clicked(self) -> None:
        if self.source is None:
            return
        self.source.stop()
        self.source = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.source_combo.setEnabled(True)

    def _on_freeze_toggled(self, checked: bool) -> None:
        self.frozen = checked

    def _on_trigger_settings_changed(self, *_args) -> None:
        self.trigger_engine.config.edge = EDGE_BY_LABEL[self.edge_combo.currentText()]
        self.trigger_engine.config.threshold = self.threshold_spin.value()

    # -- live refresh ------------------------------------------------------

    def _refresh(self) -> None:
        if self.frozen:
            return

        window_samples = max(64, int(self.window_spin.value() / 1000.0 * self.sample_rate))
        history_samples = window_samples * 4
        block = self.ring_buffer.read_latest(history_samples)
        if block.shape[1] < 64:
            return
        signal = block[0]

        triggers = self.trigger_engine.find_triggers(signal, self.sample_rate)
        if triggers.size > 0:
            frame, _ = self.trigger_engine.capture_frame(
                signal, triggers[-1], pre_samples=window_samples // 4,
                post_samples=window_samples - window_samples // 4,
            )
            trigger_status = "Triggered"
        else:
            frame = signal[-window_samples:]
            trigger_status = "Free-run (no trigger found)"

        if frame.size < 8:
            return

        t = np.arange(len(frame)) / self.sample_rate
        self.curve.setData(t, frame)

        m = metering.measure(frame, self.sample_rate)
        self.readout_labels["Peak"].setText(f"{m.peak:.4f}")
        self.readout_labels["Peak-to-peak"].setText(f"{m.peak_to_peak:.4f}")
        self.readout_labels["RMS"].setText(f"{m.rms:.4f}")
        self.readout_labels["DC offset"].setText(f"{m.dc_offset:.4f}")
        self.readout_labels["Zero-crossing rate (Hz)"].setText(
            f"{m.zero_crossing_rate_hz:.1f}" if m.zero_crossing_rate_hz else "--")
        self.readout_labels["Clipped samples"].setText(str(m.clipping_count))
        self.readout_labels["Trigger status"].setText(trigger_status)

        # pitch/wavelength/note use the wider history window, not the
        # (possibly single-cycle) trigger frame -- autocorrelation needs
        # enough samples to see multiple periods at low frequencies.
        pitch_result = pitch_module.detect_pitch(signal, self.sample_rate, fmin=60, fmax=1500)
        if pitch_result.frequency_hz is not None:
            freq = pitch_result.frequency_hz
            note_info = pitch_module.frequency_to_note(freq)
            lam = wavelength_module.wavelength_meters(freq)
            self.readout_labels["Pitch (Hz)"].setText(f"{freq:.2f}")
            self.readout_labels["Note"].setText(
                f"{note_info['note_name']} ({note_info['cents_offset']:+.0f}c)")
            self.readout_labels["Wavelength (m)"].setText(f"{lam:.4f}")
        else:
            self.readout_labels["Pitch (Hz)"].setText("--")
            self.readout_labels["Note"].setText("--")
            self.readout_labels["Wavelength (m)"].setText("--")

    def _refresh_envelope(self) -> None:
        if self.frozen:
            return

        window_samples = int(self.envelope_window_seconds * self.sample_rate)
        block = self.ring_buffer.read_latest(window_samples)
        if block.shape[1] < 256:
            return
        signal = block[0]

        envelope = hilbert_envelope(signal)
        downsample_factor = max(1, len(envelope) // 2000)
        envelope_ds = envelope[::downsample_factor]
        t = np.arange(len(envelope_ds)) * downsample_factor / self.sample_rate
        self.envelope_curve.setData(t, envelope_ds)

        tags = one_wave_views.classify_window(signal, self.sample_rate)
        if tags:
            self.readout_labels["Life-cycle state"].setText(", ".join(t.tag for t in tags))
        else:
            self.readout_labels["Life-cycle state"].setText("steady")

    def closeEvent(self, event) -> None:
        if self.source is not None:
            self.source.stop()
        super().closeEvent(event)
