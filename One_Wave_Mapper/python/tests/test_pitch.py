import numpy as np

from onewave_mapper import signal_generator, pitch


def test_autocorrelation_pitch_accuracy_within_tolerance():
    sr = 48000
    freq = 440.0
    sine = signal_generator.sine(freq, 2.0, sr, amplitude=1.0)
    detected_freq, confidence = pitch.autocorrelation_pitch(sine, sr, fmin=80, fmax=1000)
    assert detected_freq is not None
    assert abs(detected_freq - freq) < 0.1
    assert confidence > 0.9


def test_detect_pitch_returns_note_name():
    sr = 48000
    sine = signal_generator.sine(440.0, 1.0, sr)
    result = pitch.detect_pitch(sine, sr, fmin=80, fmax=1000)
    assert result.frequency_hz is not None
    note_info = pitch.frequency_to_note(result.frequency_hz)
    assert note_info["note_name"] == "A4"
    assert abs(note_info["cents_offset"]) < 5


def test_low_confidence_on_pure_noise():
    sr = 48000
    noise = signal_generator.white_noise(1.0, sr, seed=1)
    result = pitch.detect_pitch(noise, sr, fmin=80, fmax=1000, min_confidence=0.5)
    assert result.frequency_hz is None


def test_zero_crossing_pitch_reasonable_for_clean_tone():
    sr = 48000
    freq = 200.0
    sine = signal_generator.sine(freq, 1.0, sr)
    detected = pitch.zero_crossing_pitch(sine, sr)
    assert detected is not None
    assert abs(detected - freq) < 1.0


def test_frequency_to_note_reference_a4():
    info = pitch.frequency_to_note(440.0)
    assert info["note_name"] == "A4"
    assert abs(info["cents_offset"]) < 1e-6
