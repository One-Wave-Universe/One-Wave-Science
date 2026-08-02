import numpy as np

from onewave_mapper import signal_generator, chord


def test_interval_ratio_and_cents_for_perfect_fifth():
    f1, f2 = 220.0, 330.0
    assert abs(chord.interval_ratio(f1, f2) - 1.5) < 1e-9
    assert abs(chord.cents_interval(f1, f2) - 701.955) < 1.0


def test_beat_frequency_matches_difference():
    assert chord.beat_frequency(440.0, 442.0) == 2.0


def test_shared_harmonics_finds_octave_coincidence():
    matches = chord.shared_harmonics(220.0, 440.0, max_harmonic=4)
    assert any(m["n"] == 2 and m["m"] == 1 for m in matches)


def test_intermodulation_candidates_include_sum_and_difference():
    candidates = chord.intermodulation_candidates(440.0, 660.0, max_order=2)
    freqs = {round(c["frequency_hz"], 2) for c in candidates}
    assert round(440.0 + 660.0, 2) in freqs
    assert round(660.0 - 440.0, 2) in freqs


def test_roughness_higher_for_dissonant_than_consonant_interval():
    consonant = chord.harmonic_series_roughness(220.0, 330.0)  # perfect fifth
    dissonant = chord.harmonic_series_roughness(220.0, 233.08)  # minor second
    assert dissonant > consonant


def test_analyze_interval_reports_both_names_and_raw_frequencies():
    result = chord.analyze_interval(220.0, 440.0)
    assert result["note_names"] == ["A3", "A4"]
    assert result["frequencies_hz"] == [220.0, 440.0]
    assert abs(result["cents"] - 1200) < 1.0


def test_detect_two_pitches_recovers_known_dyad():
    sr = 48000
    f1, f2 = 220.0, 330.0
    signal = (
        signal_generator.harmonic_series(f1, 1.5, sr, harmonic_amplitudes=[1.0, 0.5, 0.25]) +
        signal_generator.harmonic_series(f2, 1.5, sr, harmonic_amplitudes=[1.0, 0.5, 0.25])
    )
    result = chord.detect_two_pitches(signal, sr, fmin=100, fmax=500, resolution_hz=1.0)
    detected = sorted(result["fundamentals_hz"])
    assert abs(detected[0] - f1) < 3.0
    assert abs(detected[1] - f2) < 3.0


def test_build_chord_event_matches_schema_fields():
    event = chord.build_chord_event([220.0, 330.0], [0.9, 0.85])
    assert event.detected_fundamentals == [220.0, 330.0]
    assert event.candidate_notes == ["A3", "E4"]
    assert len(event.pairwise_intervals) == 1
    assert len(event.frequency_ratios) == 1
    assert len(event.beat_components) == 1


def test_detect_pitches_single_note_matches_pitch_detector():
    sr = 48000
    signal = signal_generator.harmonic_series(220.0, 1.0, sr, harmonic_amplitudes=[1.0, 0.5, 0.25])
    result = chord.detect_pitches(signal, sr, n_notes=1, fmin=100, fmax=500, resolution_hz=1.0)
    assert len(result["fundamentals_hz"]) == 1
    assert abs(result["fundamentals_hz"][0] - 220.0) < 3.0


def test_detect_pitches_recovers_known_triad():
    sr = 48000
    f1, f2, f3 = 261.63, 329.63, 392.00  # C4 major triad
    signal = (
        signal_generator.harmonic_series(f1, 1.5, sr, harmonic_amplitudes=[1.0, 0.5, 0.25]) +
        signal_generator.harmonic_series(f2, 1.5, sr, harmonic_amplitudes=[1.0, 0.5, 0.25]) +
        signal_generator.harmonic_series(f3, 1.5, sr, harmonic_amplitudes=[1.0, 0.5, 0.25])
    )
    result = chord.detect_pitches(signal, sr, n_notes=3, fmin=200, fmax=450, resolution_hz=1.0)
    detected = sorted(result["fundamentals_hz"])
    for expected, found in zip([f1, f2, f3], detected):
        assert abs(expected - found) < 3.0
    assert len(result["confidences"]) == 3


def test_detect_two_pitches_still_works_as_named_wrapper():
    sr = 48000
    f1, f2 = 220.0, 330.0
    signal = (
        signal_generator.harmonic_series(f1, 1.5, sr, harmonic_amplitudes=[1.0, 0.5]) +
        signal_generator.harmonic_series(f2, 1.5, sr, harmonic_amplitudes=[1.0, 0.5])
    )
    result = chord.detect_two_pitches(signal, sr, fmin=100, fmax=500, resolution_hz=1.0)
    assert len(result["fundamentals_hz"]) == 2
