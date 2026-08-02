import numpy as np

from onewave_mapper import signal_generator, fft_analyzer, harmonics


def test_track_harmonics_finds_expected_series():
    sr = 48000
    f0 = 220.0
    amps = [1.0, 0.5, 0.25, 0.125]
    signal = signal_generator.harmonic_series(f0, 2.0, sr, harmonic_amplitudes=amps)
    spectrum = fft_analyzer.compute_spectrum(signal, sr, window="hann", fft_size=16384)

    tracks = harmonics.track_harmonics(spectrum, f0, max_harmonics=4)
    assert len(tracks) == 4
    for n, track in enumerate(tracks, start=1):
        assert track.measured_frequency_hz is not None
        assert abs(track.measured_frequency_hz - n * f0) < 5.0
        assert abs(track.deviation_cents) < 20.0

    amplitudes = [t.amplitude for t in tracks]
    assert amplitudes[0] > amplitudes[1] > amplitudes[2] > amplitudes[3]


def test_classify_peak_identifies_fundamental_and_harmonic():
    assert harmonics.classify_peak(220.0, 220.0) == "fundamental"
    assert harmonics.classify_peak(440.0, 220.0) == "harmonic"
    assert harmonics.classify_peak(110.0, 220.0) == "subharmonic"
    assert harmonics.classify_peak(301.0, 220.0) == "unknown"


def test_total_harmonic_distortion_zero_for_pure_tone():
    sr = 48000
    f0 = 300.0
    signal = signal_generator.sine(f0, 1.0, sr)
    spectrum = fft_analyzer.compute_spectrum(signal, sr, window="hann", fft_size=16384)
    tracks = harmonics.track_harmonics(spectrum, f0, max_harmonics=8)
    thd = harmonics.total_harmonic_distortion(tracks)
    assert thd is not None
    assert thd < 0.05
