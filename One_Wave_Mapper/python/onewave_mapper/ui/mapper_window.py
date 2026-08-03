"""One-Wave Mapper main window: every panel driven by one shared
AnalysisState, so one timeline/selection/zoom/cursor/mode governs all of
them (Section "Interface behavior").

A tabbed workspace rather than a single crowded window, but every tab
reads the same state -- switching tabs never loses the current selection,
cursor position, zoom range, or Raw/One-Wave/Both mode.
"""

from __future__ import annotations

import numpy as np
from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState, ViewMode
from onewave_mapper.ui.panels.waveform_panel import WaveformPanel
from onewave_mapper.ui.panels.envelope_panel import EnvelopePanel
from onewave_mapper.ui.panels.spectrum_panel import SpectrumPanel
from onewave_mapper.ui.panels.spectrogram_panel import SpectrogramPanel
from onewave_mapper.ui.panels.phase_panel import PhasePanel
from onewave_mapper.ui.panels.interference_panel import InterferencePanel
from onewave_mapper.ui.panels.resonance_panel import ResonancePanel
from onewave_mapper.ui.panels.modulation_panel import ModulationPanel

MODE_LABELS = {ViewMode.RAW: "Raw", ViewMode.ONE_WAVE: "One-Wave", ViewMode.BOTH: "Both"}


class MapperWindow(QtWidgets.QMainWindow):
    def __init__(self, sample_rate: int = 48000, parent=None):
        super().__init__(parent)
        self.setWindowTitle("One-Wave Mapper")
        self.state = AnalysisState(sample_rate=sample_rate)

        self._build_ui()
        self.resize(1200, 800)

    # -- construction ---------------------------------------------------

    def _build_ui(self) -> None:
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        layout.addLayout(self._build_toolbar())

        self.tabs = QtWidgets.QTabWidget()
        self.waveform_panel = WaveformPanel(self.state)
        self.envelope_panel = EnvelopePanel(self.state)
        self.spectrum_panel = SpectrumPanel(self.state)
        self.spectrogram_panel = SpectrogramPanel(self.state)
        self.phase_panel = PhasePanel(self.state)
        self.interference_panel = InterferencePanel(sample_rate=self.state.sample_rate)
        self.resonance_panel = ResonancePanel(self.state)
        self.modulation_panel = ModulationPanel(self.state)

        self.tabs.addTab(self.waveform_panel, "Raw waveform")
        self.tabs.addTab(self.envelope_panel, "Envelope")
        self.tabs.addTab(self.spectrum_panel, "Spectrum")
        self.tabs.addTab(self.spectrogram_panel, "Spectrogram")
        self.tabs.addTab(self.phase_panel, "Phase")
        self.tabs.addTab(self.interference_panel, "Interference")
        self.tabs.addTab(self.resonance_panel, "Resonance")
        self.tabs.addTab(self.modulation_panel, "Modulation")

        layout.addWidget(self.tabs, stretch=1)
        self.setCentralWidget(central)

    def _build_toolbar(self) -> QtWidgets.QHBoxLayout:
        toolbar = QtWidgets.QHBoxLayout()

        toolbar.addWidget(QtWidgets.QLabel("Load:"))
        for label, handler in [
            ("Guitar note", self.load_synthetic_guitar_note),
            ("Sine tone", self.load_synthetic_sine),
            ("Open E chord", self.load_synthetic_chord),
        ]:
            button = QtWidgets.QPushButton(label)
            button.clicked.connect(handler)
            toolbar.addWidget(button)

        toolbar.addSpacing(20)
        toolbar.addWidget(QtWidgets.QLabel("Mode:"))
        self.mode_group = QtWidgets.QButtonGroup(self)
        for mode in (ViewMode.RAW, ViewMode.ONE_WAVE, ViewMode.BOTH):
            button = QtWidgets.QRadioButton(MODE_LABELS[mode])
            button.setChecked(mode == self.state.mode)
            button.toggled.connect(lambda checked, m=mode: self.state.set_mode(m) if checked else None)
            self.mode_group.addButton(button)
            toolbar.addWidget(button)

        toolbar.addSpacing(20)
        toolbar.addWidget(QtWidgets.QLabel("Nested motion:"))
        self.point_checkbox = QtWidgets.QCheckBox("Point")
        self.point_checkbox.setChecked(self.state.show_point_rotation)
        self.point_checkbox.toggled.connect(self.state.set_point_rotation_visible)
        toolbar.addWidget(self.point_checkbox)

        self.path_checkbox = QtWidgets.QCheckBox("Path")
        self.path_checkbox.setChecked(self.state.show_path_rotation)
        self.path_checkbox.toggled.connect(self.state.set_path_rotation_visible)
        toolbar.addWidget(self.path_checkbox)

        self.field_checkbox = QtWidgets.QCheckBox("Field")
        self.field_checkbox.setChecked(self.state.show_field_rotation)
        self.field_checkbox.toggled.connect(self.state.set_field_rotation_visible)
        toolbar.addWidget(self.field_checkbox)

        toolbar.addStretch(1)
        return toolbar

    # -- loading recordings ---------------------------------------------

    def load_recording(self, signal: np.ndarray, sample_rate: int | None = None) -> None:
        """Load a preserved, timestamped raw recording (Section 2.1) --
        from a synthetic generator here, or a real captured/loaded WAV in
        general use."""
        self.state.set_recording(signal.astype(np.float32), sample_rate)

    def load_synthetic_guitar_note(self) -> None:
        self.load_recording(signal_generator.guitar_note(220.0, 1.5, self.state.sample_rate))

    def load_synthetic_sine(self) -> None:
        self.load_recording(signal_generator.sine(440.0, 1.0, self.state.sample_rate, amplitude=0.7))

    def load_synthetic_chord(self) -> None:
        sr = self.state.sample_rate
        open_e_major_freqs = [82.41, 123.47, 164.81, 207.65, 246.94, 329.63]
        notes = [signal_generator.guitar_note(f, 1.5, sr, amplitude=0.3) for f in open_e_major_freqs]
        self.load_recording(np.sum(notes, axis=0))
