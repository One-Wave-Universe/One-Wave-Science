import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.panels.interference_panel import InterferencePanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_generates_demo_sources_on_construction(qapp):
    panel = InterferencePanel(sample_rate=48000)
    assert len(panel.source_a) > 0
    assert len(panel.source_b) > 0


def test_each_source_plotted_separately_not_merged(qapp):
    panel = InterferencePanel(sample_rate=48000)
    _, a_data = panel.curve_a.getData()
    _, b_data = panel.curve_b.getData()
    assert np.array_equal(a_data, panel.source_a)
    assert np.array_equal(b_data, panel.source_b)
    assert not np.array_equal(a_data, b_data)


def test_combined_curve_is_real_sum(qapp):
    panel = InterferencePanel(sample_rate=48000)
    _, combined = panel.curve_sum.getData()
    assert np.allclose(combined, panel.source_a + panel.source_b)


def test_difference_curve_is_real_difference(qapp):
    panel = InterferencePanel(sample_rate=48000)
    _, diff = panel.curve_diff.getData()
    assert np.allclose(diff, panel.source_a - panel.source_b)


def test_set_sources_updates_all_curves(qapp):
    sr = 48000
    panel = InterferencePanel(sample_rate=sr)
    a = signal_generator.sine(300, 0.5, sr, amplitude=0.4)
    b = signal_generator.sine(305, 0.5, sr, amplitude=0.4)
    panel.set_sources(a, b, sr)

    _, a_data = panel.curve_a.getData()
    assert np.array_equal(a_data, a)


def test_beat_frequency_readout_matches_known_beat(qapp):
    sr = 48000
    panel = InterferencePanel(sample_rate=sr)
    a = signal_generator.sine(440.0, 3.0, sr, amplitude=0.5)
    b = signal_generator.sine(442.0, 3.0, sr, amplitude=0.5)
    panel.set_sources(a, b, sr)

    beat_text = panel.readout_labels["Beat frequency (Hz)"].text()
    assert beat_text != "--"
    assert abs(float(beat_text) - 2.0) < 0.5


def test_identical_in_phase_sources_are_fully_constructive(qapp):
    sr = 48000
    panel = InterferencePanel(sample_rate=sr)
    tone = signal_generator.sine(500, 1.0, sr, amplitude=0.5)
    panel.set_sources(tone, tone, sr)

    assert float(panel.readout_labels["Constructive score"].text()) > 0.99
    assert float(panel.readout_labels["Destructive score"].text()) < 0.01


def test_inverted_sources_are_fully_destructive(qapp):
    sr = 48000
    panel = InterferencePanel(sample_rate=sr)
    tone = signal_generator.sine(500, 1.0, sr, amplitude=0.5)
    panel.set_sources(tone, -tone, sr)

    assert float(panel.readout_labels["Destructive score"].text()) > 0.99
    _, boundary = panel.curve_boundary.getData()
    assert np.all(boundary < -20)  # every window strongly cancelling


def test_time_varying_boundary_has_one_point_per_window(qapp):
    sr = 48000
    panel = InterferencePanel(sample_rate=sr)
    a = signal_generator.sine(440, 1.0, sr)
    b = signal_generator.sine(442, 1.0, sr)
    panel.set_sources(a, b, sr)
    t, boundary = panel.curve_boundary.getData()
    assert len(t) == len(boundary)
    assert len(t) == len(a) // int(sr * 0.02)


def test_generate_button_regenerates_from_spin_values(qapp):
    panel = InterferencePanel(sample_rate=48000)
    panel.freq_a_spin.setValue(200.0)
    panel.freq_b_spin.setValue(203.0)
    panel.generate_button.click()

    beat_text = panel.readout_labels["Beat frequency (Hz)"].text()
    assert abs(float(beat_text) - 3.0) < 0.5
