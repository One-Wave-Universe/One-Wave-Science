import json

import numpy as np

from onewave_mapper import signal_generator, prediction


def test_predict_interaction_two_notes_predicts_correct_beat_frequency():
    sr = 48000
    a = signal_generator.sine(440.0, 1.0, sr, amplitude=0.5)
    b = signal_generator.sine(442.0, 1.0, sr, amplitude=0.5)

    result, predicted_sum = prediction.predict_interaction([a, b], sr, fmin=200, fmax=800)

    assert result.n_sources == 2
    assert len(result.pairwise) == 1
    pair = result.pairwise[0]
    assert abs(pair["fundamental_i_hz"] - 440.0) < 2.0
    assert abs(pair["fundamental_j_hz"] - 442.0) < 2.0
    assert abs(pair["beat_frequency_hz"] - 2.0) < 2.0
    assert np.allclose(predicted_sum, a + b)


def test_predict_interaction_predicted_sum_matches_linear_superposition():
    sr = 48000
    a = signal_generator.sine(220.0, 0.5, sr, amplitude=0.3)
    b = signal_generator.sine(440.0, 0.5, sr, amplitude=0.3)
    c = signal_generator.sine(660.0, 0.5, sr, amplitude=0.3)

    result, predicted_sum = prediction.predict_interaction([a, b, c], sr, fmin=100, fmax=800)

    assert result.n_sources == 3
    assert len(result.pairwise) == 3  # C(3,2)
    assert np.allclose(predicted_sum, a + b + c)


def test_predict_interaction_finds_octave_shared_harmonics():
    sr = 48000
    a = signal_generator.harmonic_series(220.0, 1.0, sr, harmonic_amplitudes=[1.0, 0.5, 0.25])
    b = signal_generator.harmonic_series(440.0, 1.0, sr, harmonic_amplitudes=[1.0, 0.5, 0.25])

    result, _ = prediction.predict_interaction([a, b], sr, fmin=100, fmax=800)
    pair = result.pairwise[0]
    assert any(m["n"] == 2 and m["m"] == 1 for m in pair["shared_harmonics"])


def test_predict_interaction_interference_scores_match_direct_call():
    from onewave_mapper import interference

    sr = 48000
    a = signal_generator.sine(500, 1.0, sr, amplitude=0.5)
    b = signal_generator.sine(500, 1.0, sr, amplitude=0.5)  # identical, in phase

    result, _ = prediction.predict_interaction([a, b], sr, fmin=200, fmax=800)
    direct_scores = interference.interference_scores(a, b, sr)

    assert result.pairwise[0]["interference_scores"]["constructive_score"] == direct_scores.constructive_score


def test_predict_interaction_handles_unpitched_source_gracefully():
    sr = 48000
    tone = signal_generator.sine(440.0, 1.0, sr, amplitude=0.5)
    noise = signal_generator.white_noise(1.0, sr, seed=5)

    result, predicted_sum = prediction.predict_interaction([tone, noise], sr, fmin=200, fmax=800)
    pair = result.pairwise[0]
    assert pair["fundamental_j_hz"] is None
    assert pair["beat_frequency_hz"] is None
    assert pair["shared_harmonics"] == []
    assert predicted_sum.shape == tone.shape


def test_predict_interaction_predicted_levels_are_reasonable():
    sr = 48000
    a = signal_generator.sine(220.0, 0.5, sr, amplitude=0.5)
    b = signal_generator.sine(220.0, 0.5, sr, amplitude=0.5)  # in-phase doubling

    result, predicted_sum = prediction.predict_interaction([a, b], sr, fmin=100, fmax=500)
    assert result.predicted_peak_dbfs > -6  # roughly doubled amplitude vs a single 0.5-amplitude tone
    assert result.predicted_clipping_count >= 0


def test_predict_interaction_single_source():
    sr = 48000
    a = signal_generator.sine(300.0, 0.5, sr, amplitude=0.4)
    result, predicted_sum = prediction.predict_interaction([a], sr, fmin=100, fmax=500)
    assert result.n_sources == 1
    assert result.pairwise == []
    assert np.array_equal(predicted_sum, a)


def test_predict_interaction_to_dict_is_json_serializable():
    sr = 48000
    a = signal_generator.sine(220.0, 0.3, sr)
    b = signal_generator.sine(330.0, 0.3, sr)
    result, _ = prediction.predict_interaction([a, b], sr, fmin=100, fmax=500)
    json.dumps(result.to_dict())  # must not raise
