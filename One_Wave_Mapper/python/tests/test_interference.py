import numpy as np
import pytest

from onewave_mapper import signal_generator, interference


def test_sum_and_difference_signals():
    x1 = np.array([1.0, 2.0, 3.0])
    x2 = np.array([0.5, 0.5, 0.5])
    assert np.allclose(interference.sum_signal(x1, x2), [1.5, 2.5, 3.5])
    assert np.allclose(interference.difference_signal(x1, x2), [0.5, 1.5, 2.5])


def test_frequency_dependent_response_zero_db_for_in_phase_identical_tones():
    sr = 48000
    tone = signal_generator.sine(1000, 1.0, sr, amplitude=0.5)
    combined = tone + tone
    response = interference.frequency_dependent_response(tone, tone, combined, sr, fft_size=8192)

    peak_bin = np.argmax(response["predicted_magnitude"])
    assert abs(response["db_difference"][peak_bin]) < 0.1


def test_frequency_dependent_response_large_cancellation_for_out_of_phase_tones():
    sr = 48000
    tone = signal_generator.sine(1000, 1.0, sr, amplitude=0.5)
    combined = tone + (-tone)
    response = interference.frequency_dependent_response(tone, -tone, combined, sr, fft_size=8192)

    peak_bin = np.argmax(response["predicted_magnitude"])
    assert response["db_difference"][peak_bin] < -60


def test_detect_beats_matches_known_beat_frequency():
    sr = 48000
    combined = signal_generator.two_tone(440.0, 442.0, 3.0, sr, amplitude=0.5)
    result = interference.detect_beats(combined, sr)
    assert result.beat_frequency_hz is not None
    assert abs(result.beat_frequency_hz - 2.0) < 0.3
    assert result.confidence > 0.1


def test_interference_scores_fully_constructive_for_identical_in_phase_signals():
    sr = 48000
    tone = signal_generator.sine(500, 1.0, sr, amplitude=0.5)
    scores = interference.interference_scores(tone, tone, sr)
    assert scores.constructive_score > 0.99
    assert scores.destructive_score < 0.01
    assert scores.phase_alignment_score > 0.99


def test_interference_scores_fully_destructive_for_inverted_signals():
    sr = 48000
    tone = signal_generator.sine(500, 1.0, sr, amplitude=0.5)
    scores = interference.interference_scores(tone, -tone, sr)
    assert scores.destructive_score > 0.99
    assert scores.constructive_score < 0.01
    assert scores.phase_alignment_score < 0.01
    assert scores.cancellation_depth_db > 40


def test_interference_scores_recurrence_period_matches_beat_period():
    sr = 48000
    a = signal_generator.sine(440.0, 3.0, sr, amplitude=0.5)
    b = signal_generator.sine(442.0, 3.0, sr, amplitude=0.5)
    scores = interference.interference_scores(a, b, sr)
    assert scores.recurrence_period_seconds is not None
    assert abs(scores.recurrence_period_seconds - 0.5) < 0.1


def test_compare_isolated_vs_combined_near_zero_residual_for_linear_sum():
    sr = 48000
    a = signal_generator.sine(300, 1.0, sr, amplitude=0.4)
    b = signal_generator.sine(500, 1.0, sr, amplitude=0.3)
    combined = a + b

    result, residual = interference.compare_isolated_vs_combined(a, b, combined, sr)
    assert result.residual_to_combined_db < -60
    assert abs(result.gain_a - 1.0) < 0.05
    assert abs(result.gain_b - 1.0) < 0.05


def test_compare_isolated_vs_combined_detects_nonlinear_residual_from_clipping():
    sr = 48000
    a = signal_generator.sine(300, 1.0, sr, amplitude=0.7)
    b = signal_generator.sine(500, 1.0, sr, amplitude=0.7)
    combined = signal_generator.clipped(a + b, ceiling=0.8)

    result, residual = interference.compare_isolated_vs_combined(a, b, combined, sr)
    assert result.residual_to_combined_db > -20  # clipping leaves a much larger residual


def test_compare_isolated_vs_combined_recovers_known_delay():
    # Pure/decaying sine tones are ambiguous for delay estimation beyond
    # their own period (a 500 Hz tone repeats every 96 samples at 48 kHz),
    # so this uses decaying broadband noise bursts instead -- closer to a
    # real pick attack's transient content anyway, and unambiguous for
    # cross-correlation to lock onto.
    sr = 48000
    t = np.arange(int(1.0 * sr)) / sr
    envelope = np.exp(-t / 0.3)
    a = signal_generator.white_noise(1.0, sr, amplitude=0.4, seed=11) * envelope
    b = signal_generator.white_noise(1.0, sr, amplitude=0.3, seed=22) * envelope
    b_delayed = signal_generator.with_delay(b, delay_samples=100)
    combined = a + b_delayed

    result, _ = interference.compare_isolated_vs_combined(a, b, combined, sr)
    # cross_correlation_delay(combined, x_b) follows "positive delay means
    # the second argument lags the first" -- since combined already
    # contains b delayed by +100, undelayed b leads combined, so the
    # reported delay is -100 (and _shift applies -round(delay) internally,
    # i.e. +100, to correctly align b forward -- see the near-zero-residual
    # and clipping-residual tests above, which confirm alignment works).
    assert abs(result.delay_b_samples - (-100)) < 2


def test_compare_isolated_vs_combined_n_recovers_a_triad():
    # Simulates the real workflow: three isolated fretted notes, one real
    # combined recording (here just their exact linear sum, since this only
    # tests the N-way alignment/gain-fit machinery itself). Each note gets a
    # short broadband noise burst added at its true onset, standing in for a
    # real pick attack's transient content -- that's what a 20ms
    # alignment_window_samples locks cross-correlation onto instead of the
    # much longer, highly self-similar harmonic tail.
    sr = 48000
    freqs = [220.0, 261.63, 329.63]  # A minor triad
    rng = np.random.default_rng(0)
    burst_samples = int(0.005 * sr)
    burst_envelope = np.exp(-np.arange(burst_samples) / (burst_samples / 4))

    notes = []
    for f in freqs:
        note = signal_generator.guitar_note(f, 1.0, sr, amplitude=0.3)
        burst = 0.3 * rng.uniform(-1, 1, burst_samples) * burst_envelope
        note[:burst_samples] += burst
        notes.append(note)
    combined = np.sum(notes, axis=0)

    result, residual = interference.compare_isolated_vs_combined_n(
        notes, combined, sr, alignment_window_samples=int(0.02 * sr))

    assert result.n_sources == 3
    assert len(result.gains) == 3
    assert all(abs(d) < 2 for d in result.delays_samples)
    assert result.residual_to_combined_db < -60


def test_compare_isolated_vs_combined_n_dense_chord_is_a_documented_hard_case():
    # A full open-E six-string chord is close to a worst case for blind
    # broadband delay estimation: its strings are almost entirely octave/
    # fifth-related (246.94 Hz sits right on the 3rd harmonic of the
    # 82.41 Hz low E, etc.), so multiple lags can explain the correlation
    # nearly as well as the true one -- exactly the ambiguity Section 14.4
    # has in mind by calling this comparison an experiment, not a
    # measurement. This only asserts the machinery runs and produces
    # correctly-shaped output; see test_compare_isolated_vs_combined_n_
    # recovers_a_triad for a case where alignment is verified precise.
    sr = 48000
    open_e_chord_freqs = [82.41, 123.47, 164.81, 207.65, 246.94, 329.63]
    notes = [signal_generator.guitar_note(f, 1.0, sr, amplitude=0.3) for f in open_e_chord_freqs]
    combined = np.sum(notes, axis=0)

    result, residual = interference.compare_isolated_vs_combined_n(notes, combined, sr)

    assert result.n_sources == 6
    assert len(result.gains) == 6
    assert len(result.delays_samples) == 6
    assert residual.shape[0] > 0


def test_compare_isolated_vs_combined_n_single_source():
    sr = 48000
    a = signal_generator.sine(300, 0.5, sr, amplitude=0.5)
    result, residual = interference.compare_isolated_vs_combined_n([a], a, sr)
    assert result.n_sources == 1
    assert abs(result.gains[0] - 1.0) < 1e-6
    assert result.residual_to_combined_db < -100


def test_compare_isolated_vs_combined_two_note_matches_n_way_result():
    sr = 48000
    a = signal_generator.sine(300, 1.0, sr, amplitude=0.4)
    b = signal_generator.sine(500, 1.0, sr, amplitude=0.3)
    combined = a + b

    result_2, _ = interference.compare_isolated_vs_combined(a, b, combined, sr)
    result_n, _ = interference.compare_isolated_vs_combined_n([a, b], combined, sr)

    assert result_2.gain_a == pytest.approx(result_n.gains[0])
    assert result_2.gain_b == pytest.approx(result_n.gains[1])
    assert result_2.residual_to_combined_db == pytest.approx(result_n.residual_to_combined_db)
