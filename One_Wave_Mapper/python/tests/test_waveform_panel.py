import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState, ViewMode
from onewave_mapper.ui.panels.waveform_panel import WaveformPanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def _state_with_note(sample_rate=48000):
    state = AnalysisState(sample_rate=sample_rate)
    signal = signal_generator.guitar_note(220.0, 1.0, sample_rate)
    state.set_recording(signal)
    return state


def test_panel_constructs_and_plots_full_recording(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    x, y = panel.curve.getData()
    assert len(x) == len(state.raw_signal)
    assert np.array_equal(y, state.raw_signal)


def test_curve_never_smoothed_matches_raw_samples_exactly(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    state.set_view_range(1000, 5000)
    _, y = panel.curve.getData()
    assert np.array_equal(y, state.raw_signal[1000:5000])


def test_zoom_to_full_capture_shows_everything(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    state.set_view_range(1000, 2000)
    panel.zoom_full_button.click()
    assert state.view_start_sample == 0
    assert state.view_end_sample == len(state.raw_signal)


def test_zoom_to_sample_level_is_narrow(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    state.set_cursor(24000)
    panel.zoom_to_sample_level()
    width = state.view_end_sample - state.view_start_sample
    assert width <= 300


def test_zoom_to_note_level_is_about_one_second(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    state.set_cursor(24000)
    panel.zoom_to_note_level()
    width = state.view_end_sample - state.view_start_sample
    assert abs(width - state.sample_rate) < 10


def test_cursor_line_follows_state(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    state.set_cursor(9600)
    assert panel.cursor_line.value() == pytest.approx(9600 / state.sample_rate)
    assert panel.readout_labels["Time (s)"].text() == f"{9600 / state.sample_rate:.4f}"


def test_moving_cursor_line_updates_state(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    panel.cursor_line.setValue(0.2)
    assert state.cursor_sample == int(round(0.2 * state.sample_rate))


def test_selection_region_follows_state(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    state.set_selection(1000, 5000)
    low, high = panel.selection_region.getRegion()
    assert low == pytest.approx(1000 / state.sample_rate)
    assert high == pytest.approx(5000 / state.sample_rate)


def test_dragging_selection_region_updates_state(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    panel.selection_region.setRegion((0.1, 0.3))
    assert state.selection is not None
    assert state.selection[0] == pytest.approx(int(0.1 * state.sample_rate), abs=1)
    assert state.selection[1] == pytest.approx(int(0.3 * state.sample_rate), abs=1)


def test_trigger_threshold_change_moves_trigger_line(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    panel.threshold_spin.setValue(0.3)
    assert panel.trigger_line.pos().y() == pytest.approx(0.3)


def test_find_and_set_trigger_sets_state_trigger_point(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    panel.threshold_spin.setValue(0.0)
    panel._on_trigger_settings_changed()
    panel.find_and_set_trigger()
    assert state.trigger_sample is not None


def test_one_wave_overlays_present_in_both_mode_absent_in_raw_mode(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    signal = signal_generator.exponential_decay(440, 1.0, sr, decay_tau_seconds=0.2, amplitude=1.0)
    state.set_recording(signal)
    panel = WaveformPanel(state)

    state.set_mode(ViewMode.BOTH)
    panel._redraw()
    assert len(panel._one_wave_regions) > 0

    state.set_mode(ViewMode.RAW)
    panel._redraw()
    assert len(panel._one_wave_regions) == 0


def test_point_ticks_visible_when_zoomed_in_close(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.sine(220.0, 1.0, sr, amplitude=0.8))
    panel = WaveformPanel(state)

    state.set_view_range(24000, 24000 + int(0.1 * sr))  # 100ms, well under the 250ms cutoff
    assert len(panel._point_tick_items) > 0


def test_point_ticks_hidden_when_zoomed_out_too_far(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.sine(220.0, 2.0, sr, amplitude=0.8))
    panel = WaveformPanel(state)

    state.zoom_to_full_capture()  # 2 seconds, far past the point-tick cutoff
    assert len(panel._point_tick_items) == 0


def test_point_ticks_hidden_when_visibility_toggled_off(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.sine(220.0, 1.0, sr, amplitude=0.8))
    panel = WaveformPanel(state)
    state.set_view_range(24000, 24000 + int(0.1 * sr))
    assert len(panel._point_tick_items) > 0

    state.set_point_rotation_visible(False)
    assert len(panel._point_tick_items) == 0


def test_path_regions_created_for_detected_note_onset(qapp):
    sr = 48000
    silence = np.zeros(int(0.2 * sr), dtype=np.float32)
    note = signal_generator.exponential_decay(220, 1.0, sr, decay_tau_seconds=0.3, amplitude=1.0).astype(np.float32)
    state = AnalysisState(sample_rate=sr)
    state.set_recording(np.concatenate([silence, note]))
    panel = WaveformPanel(state)

    assert len(panel._path_region_items) >= 1


def test_path_regions_hidden_when_visibility_toggled_off(qapp):
    sr = 48000
    silence = np.zeros(int(0.2 * sr), dtype=np.float32)
    note = signal_generator.exponential_decay(220, 1.0, sr, decay_tau_seconds=0.3, amplitude=1.0).astype(np.float32)
    state = AnalysisState(sample_rate=sr)
    state.set_recording(np.concatenate([silence, note]))
    panel = WaveformPanel(state)
    assert len(panel._path_region_items) >= 1

    state.set_path_rotation_visible(False)
    assert len(panel._path_region_items) == 0


def test_cycle_overlays_absent_in_raw_mode(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.exponential_decay(220, 1.0, sr, decay_tau_seconds=0.3, amplitude=1.0))
    panel = WaveformPanel(state)
    state.set_view_range(0, int(0.1 * sr))

    state.set_mode(ViewMode.RAW)
    assert len(panel._point_tick_items) == 0
    assert len(panel._path_region_items) == 0


def test_zero_line_and_cursor_line_present_in_plot(qapp):
    state = _state_with_note()
    panel = WaveformPanel(state)
    assert panel.zero_line in panel.plot_widget.items()
    assert panel.cursor_line in panel.plot_widget.items()
    assert panel.selection_region in panel.plot_widget.items()


def test_empty_recording_does_not_crash(qapp):
    state = AnalysisState(sample_rate=48000)
    panel = WaveformPanel(state)
    x, y = panel.curve.getData()
    assert x is None or len(x) == 0
