import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState
from onewave_mapper.ui.panels.phase_panel import PhasePanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def _state_with_harmonics(sample_rate=48000, duration=1.0):
    state = AnalysisState(sample_rate=sample_rate)
    signal = signal_generator.harmonic_series(220.0, duration, sample_rate,
                                               harmonic_amplitudes=[1.0, 0.6, 0.4, 0.2])
    state.set_recording(signal)
    return state


def test_phase_tracks_created_for_harmonics(qapp):
    state = _state_with_harmonics()
    panel = PhasePanel(state, n_harmonics=4)
    assert len(panel._phase_tracks) > 0
    harmonic_numbers = [t["harmonic_number"] for t in panel._phase_tracks]
    assert harmonic_numbers == sorted(harmonic_numbers)
    assert harmonic_numbers[0] == 1


def test_phase_values_are_wrapped_within_pi(qapp):
    state = _state_with_harmonics()
    panel = PhasePanel(state, n_harmonics=4)
    for track in panel._phase_tracks:
        assert np.all(track["phases"] >= -np.pi - 1e-6)
        assert np.all(track["phases"] <= np.pi + 1e-6)


def test_harmonic_curves_created_one_per_track(qapp):
    state = _state_with_harmonics()
    panel = PhasePanel(state, n_harmonics=4)
    assert len(panel.harmonic_curves) == len(panel._phase_tracks)


def test_circular_display_populates_from_cursor(qapp):
    state = _state_with_harmonics()
    panel = PhasePanel(state, n_harmonics=3)
    state.set_cursor(20000)
    points = panel.circular_scatter.points()
    assert len(points) == len(panel._phase_tracks)
    for p in points:
        x, y = p.pos().x(), p.pos().y()
        assert abs(x ** 2 + y ** 2 - 1.0) < 1e-6  # on the unit circle


def test_circular_display_updates_when_cursor_moves(qapp):
    state = _state_with_harmonics()
    panel = PhasePanel(state, n_harmonics=2)
    state.set_cursor(1000)
    points_a = [(p.pos().x(), p.pos().y()) for p in panel.circular_scatter.points()]
    state.set_cursor(30000)
    points_b = [(p.pos().x(), p.pos().y()) for p in panel.circular_scatter.points()]
    assert points_a != points_b


def test_redraw_on_view_range_change(qapp):
    state = _state_with_harmonics(duration=2.0)
    panel = PhasePanel(state, n_harmonics=2)
    first_tracks = len(panel._phase_tracks)
    state.set_view_range(0, 96000)
    assert len(panel._phase_tracks) >= 1
    assert first_tracks >= 1


def test_no_harmonics_for_unpitched_noise(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.white_noise(1.0, sr, seed=1))
    panel = PhasePanel(state, n_harmonics=4)
    assert panel._phase_tracks == []


def test_empty_recording_does_not_crash(qapp):
    state = AnalysisState(sample_rate=48000)
    panel = PhasePanel(state)
    assert panel._phase_tracks == []


def test_highlighting_harmonic_via_shared_state_emphasizes_its_curve(qapp):
    state = _state_with_harmonics()
    panel = PhasePanel(state, n_harmonics=3)

    state.set_highlighted_harmonic(2)
    for track in panel._phase_tracks:
        expected_size = 9 if track["harmonic_number"] == 2 else 4
        assert track["curve"].opts["symbolSize"] == expected_size

    state.set_highlighted_harmonic(None)
    for track in panel._phase_tracks:
        assert track["curve"].opts["symbolSize"] == 4
