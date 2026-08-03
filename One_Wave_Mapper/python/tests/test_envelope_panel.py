import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState
from onewave_mapper.ui.panels.envelope_panel import EnvelopePanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_upper_and_lower_curves_are_mirror_images(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.exponential_decay(440, 1.0, sr, decay_tau_seconds=0.3))
    panel = EnvelopePanel(state)

    _, upper = panel.upper_curve.getData()
    _, lower = panel.lower_curve.getData()
    assert np.allclose(upper, -lower)
    assert np.all(upper >= 0)
    assert np.all(lower <= 0)


def test_envelope_matches_hilbert_envelope_of_view_range(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    signal = signal_generator.guitar_note(220.0, 1.0, sr)
    state.set_recording(signal)
    panel = EnvelopePanel(state)

    from onewave_mapper.envelope import hilbert_envelope
    expected = hilbert_envelope(signal)
    _, upper = panel.upper_curve.getData()
    assert np.allclose(upper, expected, atol=1e-5)


def test_stage_markers_populate_readouts_for_decaying_note(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.exponential_decay(440, 2.0, sr, decay_tau_seconds=0.3, amplitude=1.0))
    panel = EnvelopePanel(state)

    assert panel.readout_labels["Peak (s)"].text() != "--"
    assert panel.readout_labels["Decay -20dB (s)"].text() != "--"
    assert len(panel._stage_lines) >= 2


def test_redraw_on_view_range_change(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.guitar_note(220.0, 1.0, sr))
    panel = EnvelopePanel(state)

    state.set_view_range(1000, 20000)
    _, upper = panel.upper_curve.getData()
    assert len(upper) == 19000


def test_empty_recording_does_not_crash(qapp):
    state = AnalysisState(sample_rate=48000)
    panel = EnvelopePanel(state)
    _, upper = panel.upper_curve.getData()
    assert upper is None or len(upper) == 0
