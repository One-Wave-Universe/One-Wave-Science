import numpy as np

from onewave_mapper import signal_generator, spectrogram


def test_spectrogram_shape_and_frame_count():
    sr = 48000
    signal = signal_generator.sine(440, 1.0, sr)
    spec = spectrogram.compute_spectrogram(signal, sr, fft_size=2048, hop_size=512)
    expected_frames = 1 + (len(signal) - 2048) // 512
    assert spec.magnitude.shape == (2048 // 2 + 1, expected_frames)
    assert spec.times_seconds.shape[0] == expected_frames


def test_spectrogram_tracks_frequency_sweep():
    sr = 48000
    signal = signal_generator.frequency_sweep(200, 2000, 2.0, sr)
    spec = spectrogram.compute_spectrogram(signal, sr, fft_size=2048, hop_size=256)

    peak_freqs = spec.freqs_hz[np.argmax(spec.magnitude, axis=0)]
    assert peak_freqs[0] < peak_freqs[-1]
    assert 150 < peak_freqs[0] < 400
    assert 1700 < peak_freqs[-1] < 2100


def test_frame_spectrum_matches_direct_fft_peak():
    sr = 48000
    signal = signal_generator.sine(1000, 1.0, sr)
    spec = spectrogram.compute_spectrogram(signal, sr, fft_size=4096, hop_size=1024)
    mid_frame = spec.frame_spectrum(spec.magnitude.shape[1] // 2)
    peak_index = int(np.argmax(mid_frame.magnitude))
    assert abs(mid_frame.freqs_hz[peak_index] - 1000) < mid_frame.bin_spacing_hz * 2


def test_frequency_axis_scales():
    freqs = np.array([100.0, 200.0, 440.0])
    assert np.array_equal(spectrogram.frequency_axis(freqs, "linear"), freqs)
    log_axis = spectrogram.frequency_axis(freqs, "log")
    assert np.allclose(log_axis, np.log10(freqs))
    note_axis = spectrogram.frequency_axis(freqs, "note")
    assert note_axis[2] == 69.0  # 440 Hz is A4 = MIDI 69


def test_fundamental_track_follows_decaying_note():
    sr = 48000
    note = signal_generator.exponential_decay(220, 1.0, sr, decay_tau_seconds=0.5, amplitude=1.0)
    track = spectrogram.fundamental_track(note, sr, frame_size=2048, hop_size=512, fmin=100, fmax=500)
    valid = ~np.isnan(track["frequency_hz"])
    assert np.sum(valid) > 0
    assert np.all(np.abs(track["frequency_hz"][valid] - 220) < 5)


def test_harmonic_track_overlay_matches_frame_count():
    sr = 48000
    signal = signal_generator.harmonic_series(220, 1.0, sr)
    spec = spectrogram.compute_spectrogram(signal, sr, fft_size=4096, hop_size=1024)
    n_frames = spec.magnitude.shape[1]
    fundamentals = np.full(n_frames, 220.0)
    tracks = spectrogram.harmonic_track_overlay(spec, fundamentals, max_harmonics=4)
    assert len(tracks) == n_frames
    assert all(len(t) == 4 for t in tracks)
