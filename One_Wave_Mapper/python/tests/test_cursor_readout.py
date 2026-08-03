import numpy as np

from onewave_mapper import signal_generator
from onewave_mapper.ui.cursor_readout import measure_at_cursor


def test_measure_at_cursor_reports_time_and_amplitude():
    sr = 48000
    signal = signal_generator.sine(440.0, 1.0, sr, amplitude=0.5)
    readout = measure_at_cursor(signal, sr, cursor_sample=4800)
    assert readout.time_seconds == 4800 / sr
    assert readout.amplitude == signal[4800]


def test_measure_at_cursor_detects_frequency_and_note():
    sr = 48000
    signal = signal_generator.sine(220.0, 1.0, sr, amplitude=0.8)
    readout = measure_at_cursor(signal, sr, cursor_sample=24000, fmin=100, fmax=500)
    assert readout.frequency_hz is not None
    assert abs(readout.frequency_hz - 220.0) < 3.0
    assert readout.note_name == "A3"
    assert readout.phase_rad is not None


def test_measure_at_cursor_clamps_out_of_range_index():
    sr = 48000
    signal = signal_generator.sine(440.0, 0.1, sr)
    readout = measure_at_cursor(signal, sr, cursor_sample=999999)
    assert readout.sample_index == len(signal) - 1


def test_measure_at_cursor_handles_empty_signal():
    readout = measure_at_cursor(np.zeros(0), 48000, 0)
    assert readout.sample_index == 0
    assert readout.frequency_hz is None


def test_measure_at_cursor_near_edges_does_not_crash():
    sr = 48000
    signal = signal_generator.sine(300.0, 0.05, sr)
    start_readout = measure_at_cursor(signal, sr, cursor_sample=0)
    end_readout = measure_at_cursor(signal, sr, cursor_sample=len(signal) - 1)
    assert start_readout.sample_index == 0
    assert end_readout.sample_index == len(signal) - 1
