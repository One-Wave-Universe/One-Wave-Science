import numpy as np

from onewave_mapper import signal_generator, fft_analyzer


def test_bin_spacing_formula():
    assert fft_analyzer.bin_spacing(48000, 4800) == 10.0


def test_strongest_peak_finds_known_frequency():
    sr = 48000
    freq = 1000.0
    sine = signal_generator.sine(freq, 1.0, sr, amplitude=1.0)
    spectrum = fft_analyzer.compute_spectrum(sine, sr, window="hann", fft_size=8192)
    peak_freq, peak_mag = fft_analyzer.strongest_peak(spectrum)
    assert abs(peak_freq - freq) < 1.0
    assert peak_mag > 0.1


def test_magnitude_reflects_amplitude():
    sr = 48000
    sine = signal_generator.sine(500, 1.0, sr, amplitude=0.5)
    spectrum = fft_analyzer.compute_spectrum(sine, sr, window="hann", fft_size=8192)
    _, peak_mag = fft_analyzer.strongest_peak(spectrum)
    assert abs(peak_mag - 0.5) < 0.05


def test_all_window_functions_run():
    sr = 48000
    sine = signal_generator.sine(500, 0.5, sr)
    for window in fft_analyzer.WINDOW_FUNCTIONS:
        spectrum = fft_analyzer.compute_spectrum(sine, sr, window=window)
        assert spectrum.magnitude.shape == spectrum.freqs_hz.shape


def test_spectral_centroid_of_single_tone_near_tone_frequency():
    sr = 48000
    freq = 2000.0
    sine = signal_generator.sine(freq, 1.0, sr, amplitude=1.0)
    spectrum = fft_analyzer.compute_spectrum(sine, sr, window="hann", fft_size=8192)
    centroid = fft_analyzer.spectral_centroid(spectrum)
    assert abs(centroid - freq) < 50.0


def test_spectral_flatness_higher_for_noise_than_tone():
    sr = 48000
    tone = signal_generator.sine(1000, 1.0, sr)
    noise = signal_generator.white_noise(1.0, sr, seed=0)
    tone_spectrum = fft_analyzer.compute_spectrum(tone, sr, fft_size=8192)
    noise_spectrum = fft_analyzer.compute_spectrum(noise, sr, fft_size=8192)
    assert fft_analyzer.spectral_flatness(noise_spectrum) > fft_analyzer.spectral_flatness(tone_spectrum)
