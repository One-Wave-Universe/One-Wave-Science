import numpy as np
import pytest

from onewave_mapper import signal_generator, fretboard
from onewave_mapper.wav_io import write_wav


def test_expected_frequency_open_strings_match_standard_tuning():
    assert fretboard.expected_frequency_hz(1, 0) == pytest.approx(329.63)
    assert fretboard.expected_frequency_hz(6, 0) == pytest.approx(82.41)


def test_expected_frequency_twelfth_fret_is_one_octave_up():
    open_freq = fretboard.expected_frequency_hz(6, 0)
    twelfth_fret_freq = fretboard.expected_frequency_hz(6, 12)
    assert twelfth_fret_freq == pytest.approx(2 * open_freq, rel=1e-6)


def test_register_with_signal_measures_pitch_and_cents_error():
    sr = 48000
    fmap = fretboard.FretboardMap()
    expected_hz = fretboard.expected_frequency_hz(6, 0)  # low E open, 82.41 Hz
    signal = signal_generator.guitar_note(expected_hz, 1.0, sr)

    entry = fmap.register(6, 0, signal=signal, sample_rate=sr, fmin=60, fmax=200)

    assert entry.expected_note == "E2"
    assert entry.measured_frequency_hz is not None
    assert abs(entry.measured_frequency_hz - expected_hz) < 2.0
    assert abs(entry.cents_error) < 50


def test_register_and_get_round_trip():
    sr = 48000
    fmap = fretboard.FretboardMap()
    signal = signal_generator.guitar_note(110.0, 0.5, sr)
    fmap.register(5, 0, signal=signal, sample_rate=sr, fmin=80, fmax=300)

    entry = fmap.get(5, 0)
    assert entry is not None
    assert entry.string_number == 5
    assert entry.fret_number == 0
    assert fmap.get(5, 1) is None


def test_get_signal_returns_registered_array():
    sr = 48000
    fmap = fretboard.FretboardMap()
    signal = signal_generator.guitar_note(110.0, 0.5, sr)
    fmap.register(5, 0, signal=signal, sample_rate=sr, fmin=80, fmax=300)

    retrieved = fmap.get_signal(5, 0)
    assert np.array_equal(retrieved, signal)


def test_get_signal_missing_raises_key_error():
    fmap = fretboard.FretboardMap()
    with pytest.raises(KeyError):
        fmap.get_signal(1, 5)


def test_register_from_audio_path(tmp_path):
    sr = 48000
    signal = signal_generator.guitar_note(fretboard.expected_frequency_hz(1, 0), 0.5, sr)
    path = tmp_path / "e4_open.wav"
    write_wav(str(path), signal, sr, bit_depth="float32")

    fmap = fretboard.FretboardMap()
    entry = fmap.register(1, 0, audio_path=path, fmin=200, fmax=500)

    assert entry.audio_path == str(path)
    assert entry.measured_frequency_hz is not None
    assert abs(entry.measured_frequency_hz - fretboard.expected_frequency_hz(1, 0)) < 3.0


def test_signals_for_chord_assembles_open_e_major():
    sr = 48000
    fmap = fretboard.FretboardMap()
    open_e_major_shape = [(6, 0), (5, 2), (4, 2), (3, 1), (2, 0), (1, 0)]
    for string_number, fret_number in open_e_major_shape:
        freq = fretboard.expected_frequency_hz(string_number, fret_number)
        signal = signal_generator.guitar_note(freq, 0.5, sr)
        fmap.register(string_number, fret_number, signal=signal, sample_rate=sr)

    signals = fmap.signals_for_chord(open_e_major_shape)
    assert len(signals) == 6


def test_signals_for_chord_raises_on_missing_position():
    sr = 48000
    fmap = fretboard.FretboardMap()
    signal = signal_generator.guitar_note(fretboard.expected_frequency_hz(6, 0), 0.3, sr)
    fmap.register(6, 0, signal=signal, sample_rate=sr)

    with pytest.raises(KeyError, match="string 3 fret 1"):
        fmap.signals_for_chord([(6, 0), (3, 1)])


def test_coverage_report_tracks_registered_and_missing():
    sr = 48000
    fmap = fretboard.FretboardMap()
    signal = signal_generator.guitar_note(fretboard.expected_frequency_hz(1, 0), 0.3, sr)
    fmap.register(1, 0, signal=signal, sample_rate=sr)

    report = fmap.coverage_report(string_numbers=[1], fret_range=(0, 2))
    assert report["registered_count"] == 1
    assert report["missing_count"] == 2
    assert (1, 0) in report["registered"]
    assert (1, 1) in report["missing"]
    assert (1, 2) in report["missing"]
