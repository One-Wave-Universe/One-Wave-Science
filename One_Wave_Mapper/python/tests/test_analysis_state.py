import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")

from PySide6 import QtWidgets

from onewave_mapper.ui.analysis_state import AnalysisState, ViewMode, TransportMode


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_set_recording_updates_view_range(qapp):
    state = AnalysisState(sample_rate=48000)
    signal = np.arange(1000, dtype=np.float32)
    state.set_recording(signal)
    assert np.array_equal(state.raw_signal, signal)
    assert state.view_start_sample == 0
    assert state.view_end_sample == 1000


def test_recording_changed_signal_fires(qapp):
    state = AnalysisState(sample_rate=48000)
    calls = []
    state.recording_changed.connect(lambda: calls.append(True))
    state.set_recording(np.zeros(10, dtype=np.float32))
    assert len(calls) == 1


def test_append_to_recording_concatenates(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.array([1.0, 2.0], dtype=np.float32))
    state.append_to_recording(np.array([3.0, 4.0], dtype=np.float32))
    assert np.array_equal(state.raw_signal, [1.0, 2.0, 3.0, 4.0])


def test_cursor_clamped_to_recording_bounds(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.zeros(100, dtype=np.float32))
    state.set_cursor(500)
    assert state.cursor_sample == 99
    state.set_cursor(-10)
    assert state.cursor_sample == 0


def test_cursor_changed_signal_carries_value(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.zeros(100, dtype=np.float32))
    received = []
    state.cursor_changed.connect(received.append)
    state.set_cursor(42)
    assert received == [42]


def test_selection_normalizes_order(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_selection(500, 100)
    assert state.selection == (100, 500)


def test_selection_none_clears(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_selection(10, 20)
    state.set_selection(None, None)
    assert state.selection is None


def test_selection_changed_signal_fires_with_tuple(qapp):
    state = AnalysisState(sample_rate=48000)
    received = []
    state.selection_changed.connect(received.append)
    state.set_selection(10, 20)
    assert received == [(10, 20)]


def test_zoom_to_full_capture(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.zeros(48000, dtype=np.float32))
    state.set_view_range(1000, 2000)
    state.zoom_to_full_capture()
    assert state.view_start_sample == 0
    assert state.view_end_sample == 48000


def test_zoom_to_samples_centers_on_sample(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.zeros(48000, dtype=np.float32))
    state.zoom_to_samples(24000, 2000)
    assert state.view_start_sample == 23000
    assert state.view_end_sample == 25000


def test_zoom_to_note_uses_duration_seconds(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.zeros(96000, dtype=np.float32))
    state.zoom_to_note(48000, note_duration_seconds=0.5)
    width = state.view_end_sample - state.view_start_sample
    assert abs(width - 24000) <= 1


def test_pan_shifts_view_range_by_delta(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.zeros(48000, dtype=np.float32))
    state.set_view_range(1000, 2000)
    state.pan(500)
    assert state.view_start_sample == 1500
    assert state.view_end_sample == 2500


def test_view_range_clamped_to_recording_length(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_recording(np.zeros(1000, dtype=np.float32))
    state.set_view_range(-500, 5000)
    assert state.view_start_sample == 0
    assert state.view_end_sample == 1000


def test_mode_defaults_to_both_and_can_change(qapp):
    state = AnalysisState(sample_rate=48000)
    assert state.mode == ViewMode.BOTH
    received = []
    state.mode_changed.connect(received.append)
    state.set_mode(ViewMode.RAW)
    assert state.mode == ViewMode.RAW
    assert received == ["raw"]


def test_transport_mode_change(qapp):
    state = AnalysisState(sample_rate=48000)
    received = []
    state.transport_mode_changed.connect(received.append)
    state.set_transport_mode(TransportMode.TRIGGERED)
    assert state.transport_mode == TransportMode.TRIGGERED
    assert received == ["triggered"]


def test_trigger_point_can_be_set_and_cleared(qapp):
    state = AnalysisState(sample_rate=48000)
    state.set_trigger_point(1234)
    assert state.trigger_sample == 1234
    state.set_trigger_point(None)
    assert state.trigger_sample is None


def test_highlighted_harmonic_signal(qapp):
    state = AnalysisState(sample_rate=48000)
    received = []
    state.highlighted_harmonic_changed.connect(received.append)
    state.set_highlighted_harmonic(3)
    assert received == [3]
    state.set_highlighted_harmonic(None)
    assert received == [3, None]


def test_markers_accumulate_and_signal(qapp):
    state = AnalysisState(sample_rate=48000)
    fired = []
    state.markers_changed.connect(lambda: fired.append(True))
    marker = state.add_marker(4800, "attack")
    assert marker["time_seconds"] == pytest.approx(0.1)
    assert len(state.markers) == 1
    assert len(fired) == 1

    state.clear_markers()
    assert state.markers == []
    assert len(fired) == 2
