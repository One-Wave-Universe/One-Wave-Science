import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState
from onewave_mapper.ui.panels.spectrum_panel import SpectrumPanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def _state_with_harmonics(sample_rate=48000):
    state = AnalysisState(sample_rate=sample_rate)
    signal = signal_generator.harmonic_series(220.0, 1.0, sample_rate, harmonic_amplitudes=[1.0, 0.5, 0.25, 0.125])
    state.set_recording(signal)
    return state


def test_spectrum_curve_populates(qapp):
    state = _state_with_harmonics()
    panel = SpectrumPanel(state)
    freqs, mags = panel.curve.getData()
    assert len(freqs) > 0
    assert len(mags) == len(freqs)


def test_fundamental_label_matches_detected_pitch(qapp):
    state = _state_with_harmonics()
    panel = SpectrumPanel(state)
    assert panel.fundamental_label.text() != "--"
    assert abs(float(panel.fundamental_label.text()) - 220.0) < 3.0


def test_harmonic_scatter_has_multiple_independent_points(qapp):
    state = _state_with_harmonics()
    panel = SpectrumPanel(state)
    points = panel.harmonic_scatter.points()
    assert len(points) >= 4  # at least the 4 harmonics we synthesized

    freqs_seen = sorted(p.pos().x() for p in points)
    # each harmonic peak independently identifiable -- not collapsed to one bin
    assert len(set(round(f) for f in freqs_seen)) == len(freqs_seen)


def test_harmonic_labels_match_scatter_point_count(qapp):
    state = _state_with_harmonics()
    panel = SpectrumPanel(state)
    assert len(panel._harmonic_labels) == len(panel.harmonic_scatter.points())


def test_selection_changes_analysis_window(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    silence = np.zeros(int(0.2 * sr), dtype=np.float32)
    tone = signal_generator.sine(440.0, 0.5, sr, amplitude=0.8).astype(np.float32)
    state.set_recording(np.concatenate([silence, tone]))
    panel = SpectrumPanel(state)

    # selecting just the silent region should find no fundamental
    state.set_selection(0, len(silence))
    assert panel.fundamental_label.text() == "--"

    # selecting the tone region should
    state.set_selection(len(silence), len(silence) + len(tone))
    assert panel.fundamental_label.text() != "--"
    assert abs(float(panel.fundamental_label.text()) - 440.0) < 3.0


def test_clicking_harmonic_sets_and_toggles_highlight(qapp):
    state = _state_with_harmonics()
    panel = SpectrumPanel(state)
    points = panel.harmonic_scatter.points()
    first_harmonic_number = points[0].data()

    panel._on_harmonic_clicked(panel.harmonic_scatter, [points[0]])
    assert state.highlighted_harmonic == first_harmonic_number

    panel._on_harmonic_clicked(panel.harmonic_scatter, [points[0]])
    assert state.highlighted_harmonic is None


def test_external_highlight_change_updates_panel_colors(qapp):
    state = _state_with_harmonics()
    panel = SpectrumPanel(state)
    state.set_highlighted_harmonic(2)
    points = panel.harmonic_scatter.points()
    highlighted = [p for p in points if p.data() == 2]
    assert len(highlighted) == 1


def test_empty_recording_does_not_crash(qapp):
    state = AnalysisState(sample_rate=48000)
    panel = SpectrumPanel(state)
    freqs, _ = panel.curve.getData()
    assert freqs is None or len(freqs) == 0
