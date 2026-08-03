import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState
from onewave_mapper.ui.panels.modulation_panel import ModulationPanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_tremolo_detected_as_amplitude_modulation(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.amplitude_modulated(440, 6.0, 3.0, sr, mod_depth=0.8))
    panel = ModulationPanel(state)

    am_rate = panel.readout_labels["AM rate (Hz)"].text()
    assert am_rate != "--"
    assert abs(float(am_rate) - 6.0) < 0.5


def test_vibrato_detected_as_frequency_modulation(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.frequency_modulated(440, 5.0, 3.0, sr, mod_index=3.0))
    panel = ModulationPanel(state)

    fm_rate = panel.readout_labels["FM rate (Hz)"].text()
    assert fm_rate != "--"
    assert abs(float(fm_rate) - 5.0) < 1.0


def test_envelope_ac_curve_populates(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.amplitude_modulated(440, 6.0, 2.0, sr, mod_depth=0.8))
    panel = ModulationPanel(state)
    t, ac = panel.envelope_ac_curve.getData()
    assert len(t) > 0
    assert len(ac) == len(t)


def test_am_and_fm_spectra_restricted_to_display_range(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.amplitude_modulated(440, 6.0, 2.0, sr, mod_depth=0.8))
    panel = ModulationPanel(state)
    am_freqs, _ = panel.am_curve.getData()
    fm_freqs, _ = panel.fm_curve.getData()
    assert np.all(am_freqs <= 30.0)
    assert np.all(fm_freqs <= 30.0)


def test_empty_recording_does_not_crash(qapp):
    state = AnalysisState(sample_rate=48000)
    panel = ModulationPanel(state)
    assert panel.readout_labels["AM rate (Hz)"].text() == "--"
