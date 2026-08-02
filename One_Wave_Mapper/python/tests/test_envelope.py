import numpy as np

from onewave_mapper import signal_generator, envelope


def test_hilbert_envelope_of_decaying_sine_matches_exponential():
    sr = 48000
    tau = 0.4
    signal = signal_generator.exponential_decay(1000, 2.0, sr, decay_tau_seconds=tau, amplitude=1.0)
    env = envelope.hilbert_envelope(signal)
    t = np.arange(len(signal)) / sr
    expected = np.exp(-t / tau)

    steady_region = slice(int(0.05 * sr), int(1.5 * sr))
    relative_error = np.abs(env[steady_region] - expected[steady_region]) / expected[steady_region]
    assert np.median(relative_error) < 0.05


def test_measure_envelope_decay_times_are_ordered():
    sr = 48000
    signal = signal_generator.exponential_decay(500, 3.0, sr, decay_tau_seconds=0.5, amplitude=1.0)
    env = envelope.hilbert_envelope(signal)
    measurements = envelope.measure_envelope(env, sr)
    assert measurements.decay_20db_seconds is not None
    assert measurements.decay_40db_seconds is not None
    assert measurements.decay_40db_seconds > measurements.decay_20db_seconds


def test_fit_exponential_decay_recovers_known_tau():
    sr = 48000
    true_tau = 0.6
    signal = signal_generator.exponential_decay(500, 3.0, sr, decay_tau_seconds=true_tau, amplitude=1.0)
    env = envelope.hilbert_envelope(signal)
    peak_index = int(np.argmax(env))
    fit = envelope.fit_exponential_decay(env, sr, start_index=peak_index)
    assert fit["tau_seconds"] is not None
    assert abs(fit["tau_seconds"] - true_tau) / true_tau < 0.1
    assert fit["r_squared"] > 0.9


def test_attack_time_detected_for_fast_attack():
    sr = 48000
    note = signal_generator.guitar_note(220, 1.0, sr)
    env = envelope.hilbert_envelope(note)
    measurements = envelope.measure_envelope(env, sr)
    assert measurements.attack_time_seconds is not None
    assert measurements.attack_time_seconds < 0.05
