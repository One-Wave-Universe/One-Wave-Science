import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState
from onewave_mapper.ui.panels.resonance_panel import ResonancePanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_resonance_trail_created_for_decaying_tone(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.exponential_decay(500, 2.0, sr, decay_tau_seconds=0.5, amplitude=1.0))
    panel = ResonancePanel(state, fft_size=4096, hop_size=1024)

    assert len(panel._events) > 0
    assert len(panel._trail_items) == len(panel._events)
    assert panel.count_label.text() == str(len(panel._events))


def test_trail_segment_spans_start_to_end_time(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.exponential_decay(500, 2.0, sr, decay_tau_seconds=0.5, amplitude=1.0))
    panel = ResonancePanel(state, fft_size=4096, hop_size=1024)

    top_event = panel._events[0]
    item = panel._trail_items[0]
    x, y = item.getData()
    assert x[0] == pytest.approx(top_event.start_sample / sr)
    assert x[1] == pytest.approx(top_event.end_sample / sr)
    assert y[0] == y[1] == top_event.center_frequency_hz


def test_redraw_on_view_range_change_updates_events(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.exponential_decay(500, 3.0, sr, decay_tau_seconds=0.5, amplitude=1.0))
    panel = ResonancePanel(state, fft_size=4096, hop_size=1024)
    assert len(panel._events) > 0

    state.set_view_range(0, 4000)  # too short for fft_size
    assert panel._events == []
    assert panel.count_label.text() == "--"


def test_empty_recording_does_not_crash(qapp):
    state = AnalysisState(sample_rate=48000)
    panel = ResonancePanel(state)
    assert panel._events == []
    assert panel.count_label.text() == "--"
