import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

from onewave_mapper import signal_generator
from onewave_mapper.ui.panels.epicycle_panel import Epicycle, compute_epicycles, epicycle_tip_positions


def test_single_tone_reconstructs_as_one_circle():
    sr = 48000
    freq = 440.0
    signal = signal_generator.sine(freq, 1.0, sr, amplitude=0.7)
    epicycles = compute_epicycles(signal, sr, max_harmonics=1)

    assert len(epicycles) == 1
    assert abs(epicycles[0].frequency_hz - freq) < sr / 8192 * 2
    assert abs(epicycles[0].amplitude - 0.7) < 0.05


def test_epicycle_chain_math_exactly_reconstructs_known_sinusoids():
    # Isolates the chain math itself (given exact, hand-built epicycle
    # parameters) from any FFT bin-extraction error -- a sine is cosine
    # phase-shifted by -pi/2, so Re(A*exp(j*(wt - pi/2))) must equal
    # A*sin(wt) at every t, exactly, with no leakage involved.
    amplitude, freq = 0.6, 220.0
    epicycles = [Epicycle(frequency_hz=freq, amplitude=amplitude, phase_rad=-np.pi / 2)]
    sr = 48000
    for sample_index in [0, 1000, 5000, 20000]:
        t = sample_index / sr
        tip = epicycle_tip_positions(epicycles, t)[-1]
        expected = amplitude * np.sin(2 * np.pi * freq * t)
        assert abs(tip.real - expected) < 1e-9


def test_fft_extraction_matches_raw_signal_at_bin_aligned_frequency():
    # A bin-aligned frequency (exact number of cycles fit the rectangular
    # analysis window) avoids spectral leakage, so compute_epicycles'
    # extracted amplitude/phase should closely match the true signal.
    sr = 48000
    fft_size = 4800  # bin spacing 10 Hz
    freq = 200.0  # exactly bin 20 -- no leakage
    signal = signal_generator.sine(freq, 1.0, sr, amplitude=0.6)
    epicycles = compute_epicycles(signal, sr, max_harmonics=1, fft_size=fft_size)

    for sample_index in [0, 1000, 5000, 20000]:
        t = sample_index / sr
        tip = epicycle_tip_positions(epicycles, t)[-1]
        assert abs(tip.real - signal[sample_index]) < 0.02


def test_more_harmonics_reconstructs_harmonic_series_better():
    sr = 48000
    signal = signal_generator.harmonic_series(220.0, 1.0, sr, harmonic_amplitudes=[1.0, 0.5, 0.25, 0.125])

    def reconstruction_error(max_harmonics):
        epicycles = compute_epicycles(signal, sr, max_harmonics=max_harmonics)
        t = np.arange(0, 0.02, 1.0 / sr)  # first 20ms
        reconstructed = np.array([epicycle_tip_positions(epicycles, tt)[-1].real for tt in t])
        original = signal[: len(t)]
        return float(np.sqrt(np.mean((reconstructed - original) ** 2)))

    error_1 = reconstruction_error(1)
    error_4 = reconstruction_error(4)
    assert error_4 < error_1


def test_epicycle_tip_positions_chain_length_matches_harmonic_count():
    sr = 48000
    signal = signal_generator.harmonic_series(220.0, 0.5, sr, harmonic_amplitudes=[1.0, 0.5, 0.25])
    epicycles = compute_epicycles(signal, sr, max_harmonics=3)
    positions = epicycle_tip_positions(epicycles, 0.01)
    assert len(positions) == len(epicycles) + 1
    assert positions[0] == 0j  # chain starts at the origin


def test_epicycles_ordered_by_ascending_frequency():
    sr = 48000
    signal = signal_generator.harmonic_series(220.0, 1.0, sr, harmonic_amplitudes=[1.0, 0.7, 0.5, 0.3])
    epicycles = compute_epicycles(signal, sr, max_harmonics=4)
    freqs = [c.frequency_hz for c in epicycles]
    assert freqs == sorted(freqs)


def test_decaying_tone_amplitude_shrinks_in_later_window():
    sr = 48000
    signal = signal_generator.exponential_decay(440, 1.0, sr, decay_tau_seconds=0.2, amplitude=1.0)

    early_epicycles = compute_epicycles(signal[: int(0.05 * sr)], sr, max_harmonics=1)
    late_epicycles = compute_epicycles(signal[int(0.5 * sr):], sr, max_harmonics=1)

    assert late_epicycles[0].amplitude < early_epicycles[0].amplitude
