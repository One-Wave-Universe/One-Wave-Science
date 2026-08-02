import numpy as np

from onewave_mapper import signal_generator, metering


def test_rms_of_unit_sine_is_sqrt2_over_2():
    sr = 48000
    sine = signal_generator.sine(1000, 1.0, sr, amplitude=1.0)
    m = metering.measure(sine, sr)
    assert abs(m.rms - (1.0 / np.sqrt(2))) < 1e-3


def test_peak_and_peak_to_peak():
    sr = 48000
    sine = signal_generator.sine(440, 0.5, sr, amplitude=0.7)
    m = metering.measure(sine, sr)
    assert abs(m.peak - 0.7) < 1e-3
    assert abs(m.peak_to_peak - 1.4) < 1e-3


def test_dc_offset_detected():
    sr = 48000
    sine = signal_generator.sine(440, 0.5, sr, amplitude=0.3)
    offset_signal = signal_generator.with_dc_offset(sine, 0.2)
    m = metering.measure(offset_signal, sr)
    assert abs(m.dc_offset - 0.2) < 1e-3


def test_clipping_detected():
    sr = 48000
    sine = signal_generator.sine(440, 0.5, sr, amplitude=1.5)
    clipped = signal_generator.clipped(sine, ceiling=1.0)
    m = metering.measure(clipped, sr, clip_ceiling=0.999)
    assert m.clipping_count > 0
    assert m.clipped_percentage > 0


def test_zero_crossing_rate_matches_known_frequency():
    sr = 48000
    freq = 500.0
    sine = signal_generator.sine(freq, 1.0, sr, amplitude=1.0)
    m = metering.measure(sine, sr)
    assert abs(m.zero_crossing_rate_hz - freq) < 2.0
