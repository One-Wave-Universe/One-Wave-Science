"""Direct implementations of the example acceptance tests in Section 24.3."""

import numpy as np

from onewave_mapper import signal_generator, pitch, envelope, phase_analysis
from onewave_mapper.trigger import TriggerEngine, TriggerConfig, TriggerType, TriggerEdge


def test_acceptance_frequency_accuracy_440hz_within_0p1hz():
    sr = 48000
    sine = signal_generator.sine(440.0, 2.0, sr, amplitude=1.0)
    detected_freq, confidence = pitch.autocorrelation_pitch(sine, sr, fmin=200, fmax=1000)
    assert detected_freq is not None
    assert abs(detected_freq - 440.0) <= 0.1


def test_acceptance_beat_detection_440_and_442hz_gives_2hz_beat():
    sr = 48000
    duration = 3.0
    two_tone = signal_generator.two_tone(440.0, 442.0, duration, sr, amplitude=0.5)

    env = envelope.hilbert_envelope(two_tone)
    env = env - np.mean(env)
    n = len(env)
    spectrum = np.abs(np.fft.rfft(env * np.hanning(n)))
    freqs = np.fft.rfftfreq(n, d=1.0 / sr)

    mask = (freqs > 0.2) & (freqs < 20.0)
    peak_index = np.argmax(spectrum[mask])
    beat_freq = freqs[mask][peak_index]

    assert abs(beat_freq - 2.0) < 0.3


def test_acceptance_phase_difference_90_degrees():
    sr = 48000
    freq = 1000.0
    duration = 0.1
    reference = signal_generator.sine(freq, duration, sr)
    shifted = signal_generator.with_phase_offset_copy(reference, freq, sr, phase_offset_deg=90.0)

    phase_diff_deg = phase_analysis.instantaneous_phase_difference_deg(shifted, reference)
    assert abs(abs(phase_diff_deg) - 90.0) < 5.0


def test_acceptance_delay_detection_48_samples_at_48khz():
    sr = 48000
    noise = signal_generator.white_noise(1.0, sr, seed=99)
    delayed = signal_generator.with_delay(noise, delay_samples=48)

    estimate = phase_analysis.cross_correlation_delay(noise, delayed, sr)
    assert abs(estimate.delay_seconds - 0.001) < 0.0001


def test_acceptance_trigger_stability_no_horizontal_jumping():
    sr = 48000
    freq = 440.0
    sine = signal_generator.sine(freq, 2.0, sr, amplitude=1.0)

    engine = TriggerEngine(TriggerConfig(
        trigger_type=TriggerType.LEVEL, edge=TriggerEdge.RISING, threshold=0.0, hysteresis=0.05,
    ))
    triggers = engine.find_triggers(sine, sr)
    period_samples = sr / freq

    intervals = np.diff(triggers)
    max_jump_samples = np.max(np.abs(intervals - period_samples))
    assert max_jump_samples < 0.01
