import numpy as np

from onewave_mapper import signal_generator, phase_analysis


def test_cross_correlation_delay_recovers_known_delay():
    sr = 48000
    noise = signal_generator.white_noise(1.0, sr, seed=42)
    delayed = signal_generator.with_delay(noise, delay_samples=48)

    estimate = phase_analysis.cross_correlation_delay(noise, delayed, sr)
    assert abs(estimate.delay_samples - 48) < 1.0
    assert estimate.correlation_coefficient > 0.9


def test_correlation_coefficient_identical_signals_is_one():
    sr = 48000
    sine = signal_generator.sine(300, 0.5, sr)
    assert phase_analysis.correlation_coefficient(sine, sine) > 0.999


def test_correlation_coefficient_inverted_signal_is_negative_one():
    sr = 48000
    sine = signal_generator.sine(300, 0.5, sr)
    assert phase_analysis.correlation_coefficient(sine, -sine) < -0.999


def test_mid_side_reconstructs_original_channels():
    sr = 48000
    left = signal_generator.sine(300, 0.5, sr, amplitude=0.6)
    right = signal_generator.sine(300, 0.5, sr, amplitude=0.4, phase_rad=0.3)
    mid, side = phase_analysis.mid_side(left, right)
    assert np.allclose(mid + side, left)
    assert np.allclose(mid - side, right)


def test_coherence_is_high_for_identical_signals():
    sr = 48000
    noise = signal_generator.white_noise(2.0, sr, seed=7)
    freqs, coh = phase_analysis.magnitude_squared_coherence(noise, noise, sr)
    assert np.mean(coh) > 0.95
