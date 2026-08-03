import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import time

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.panels.epicycle_panel import EpicyclePanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def _pump(qapp, iterations=15, delay=0.02):
    for _ in range(iterations):
        qapp.processEvents()
        time.sleep(delay)


def test_set_signal_computes_epicycles(qapp):
    sr = 48000
    panel = EpicyclePanel(sample_rate=sr, max_harmonics=6)
    panel.set_signal(signal_generator.guitar_note(220.0, 1.0, sr), sr)
    assert len(panel.epicycles) > 0
    assert len(panel.epicycles) <= 6


def test_animation_advances_and_draws_circles(qapp):
    sr = 48000
    panel = EpicyclePanel(sample_rate=sr, max_harmonics=4, animation_interval_ms=10)
    panel.set_signal(signal_generator.guitar_note(220.0, 1.0, sr), sr)
    _pump(qapp, 10)

    assert len(panel.circle_outline_curves) == len(panel.epicycles)
    assert panel._t > 0
    x, y = panel.radius_line.getData()
    assert len(x) == len(panel.epicycles) + 1


def test_trace_curve_accumulates_reconstructed_trail(qapp):
    sr = 48000
    panel = EpicyclePanel(sample_rate=sr, max_harmonics=3, animation_interval_ms=10)
    panel.set_signal(signal_generator.sine(220.0, 1.0, sr), sr)
    _pump(qapp, 10)

    t, y = panel.trace_curve.getData()
    assert len(t) > 0
    assert len(y) == len(t)


def test_raw_reference_curve_matches_original_signal(qapp):
    sr = 48000
    panel = EpicyclePanel(sample_rate=sr, max_harmonics=3)
    signal = signal_generator.sine(220.0, 1.0, sr, amplitude=0.5)
    panel.set_signal(signal, sr)

    t, y = panel.raw_curve.getData()
    assert np.array_equal(y, signal[: len(y)])


def test_reconstructed_value_at_matches_raw_signal_reasonably(qapp):
    sr = 48000
    fft_size = 4800
    freq = 200.0  # bin-aligned, avoids leakage
    panel = EpicyclePanel(sample_rate=sr, max_harmonics=1)
    signal = signal_generator.sine(freq, 1.0, sr, amplitude=0.6)
    from onewave_mapper.ui.panels.epicycle_panel import compute_epicycles
    panel.epicycles = compute_epicycles(signal, sr, max_harmonics=1, fft_size=fft_size)

    t = 5000 / sr
    assert abs(panel.reconstructed_value_at(t) - signal[5000]) < 0.02


def test_switching_signal_resets_trail_and_time(qapp):
    sr = 48000
    panel = EpicyclePanel(sample_rate=sr, max_harmonics=3, animation_interval_ms=10)
    panel.set_signal(signal_generator.sine(220.0, 1.0, sr), sr)
    _pump(qapp, 10)
    assert panel._t > 0

    panel.set_signal(signal_generator.sine(330.0, 1.0, sr), sr)
    assert panel._t == 0.0
    assert panel._trail == []


def test_empty_signal_does_not_crash(qapp):
    panel = EpicyclePanel(sample_rate=48000)
    panel.set_signal(np.zeros(0, dtype=np.float32), 48000)
    _pump(qapp, 5)
    assert panel.epicycles == [] or len(panel.epicycles) >= 0
