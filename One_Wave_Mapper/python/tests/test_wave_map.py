import numpy as np

from onewave_mapper import signal_generator, wave_map


def test_map_wave_reports_frequency_wavelength_octave_and_note():
    sr = 48000
    signal = signal_generator.guitar_note(220.0, 1.0, sr)  # A3
    result = wave_map.map_wave(signal, sr, fmin=100, fmax=500)

    assert result.frequency_hz is not None
    assert abs(result.frequency_hz - 220.0) < 3.0
    assert result.note_name == "A3"
    assert result.octave == 3
    assert result.wavelength_m is not None
    assert abs(result.wavelength_m - 343.0 / result.frequency_hz) < 1e-6
    assert abs(result.cents_offset) < 20


def test_map_wave_wavelength_matches_speed_of_sound_parameter():
    sr = 48000
    signal = signal_generator.sine(440.0, 1.0, sr)
    v = 340.0
    result = wave_map.map_wave(signal, sr, fmin=200, fmax=800, speed_of_sound_mps=v)
    assert abs(result.wavelength_m - v / result.frequency_hz) < 1e-6


def test_map_wave_includes_harmonics_for_harmonic_series():
    sr = 48000
    signal = signal_generator.harmonic_series(220.0, 1.0, sr, harmonic_amplitudes=[1.0, 0.5, 0.25])
    result = wave_map.map_wave(signal, sr, fmin=100, fmax=500, max_harmonics=4)
    assert len(result.harmonics) == 4
    assert result.harmonics[0]["harmonic_number"] == 1


def test_map_wave_includes_rotational_envelope_point_path_cycles():
    sr = 48000
    signal = signal_generator.guitar_note(220.0, 1.0, sr, vibrato_hz=5.5, vibrato_depth_cents=40.0)
    result = wave_map.map_wave(signal, sr, fmin=100, fmax=500, max_point_cycles=8)

    assert result.point_cycle_count == 8
    assert result.path_cycle is not None
    assert result.path_cycle["cycle_level"] == "path_rotation"
    # a note with strong vibrato should surface a modulation (Path-level) cycle
    if result.modulation_cycle is not None:
        assert result.modulation_cycle["cycle_level"] == "path_rotation"


def test_map_wave_includes_one_wave_tags():
    sr = 48000
    signal = signal_generator.exponential_decay(440, 1.0, sr, decay_tau_seconds=0.2, amplitude=1.0)
    result = wave_map.map_wave(signal, sr, fmin=200, fmax=800)
    tags = {t["tag"] for t in result.one_wave_tags}
    assert "Inward" in tags  # decaying note


def test_map_wave_includes_resonances_when_signal_long_enough():
    sr = 48000
    signal = signal_generator.exponential_decay(500, 1.0, sr, decay_tau_seconds=0.3, amplitude=1.0)
    result = wave_map.map_wave(signal, sr, fmin=200, fmax=800)
    assert len(result.resonances) > 0


def test_map_wave_handles_unpitched_signal_gracefully():
    sr = 48000
    noise = signal_generator.white_noise(1.0, sr, seed=3)
    result = wave_map.map_wave(noise, sr, fmin=200, fmax=800)
    assert result.frequency_hz is None
    assert result.wavelength_m is None
    assert result.note_name is None
    assert result.harmonics == []
    # cycle tree and tags are still computed -- they don't require a pitch
    assert result.path_cycle is not None


def test_map_wave_interference_populated_when_comparing_two_signals():
    sr = 48000
    a = signal_generator.sine(440.0, 1.0, sr, amplitude=0.5)
    b = signal_generator.sine(442.0, 1.0, sr, amplitude=0.5)
    result = wave_map.map_wave(a, sr, fmin=200, fmax=800, compare_signal=b)

    assert result.interference is not None
    assert "scores" in result.interference
    assert "beats" in result.interference
    assert abs(result.interference["beats"]["beat_frequency_hz"] - 2.0) < 0.5


def test_map_wave_interference_none_without_compare_signal():
    sr = 48000
    a = signal_generator.sine(440.0, 1.0, sr)
    result = wave_map.map_wave(a, sr, fmin=200, fmax=800)
    assert result.interference is None


def test_map_wave_to_dict_is_json_serializable():
    import json
    sr = 48000
    signal = signal_generator.guitar_note(220.0, 0.5, sr)
    result = wave_map.map_wave(signal, sr, fmin=100, fmax=500)
    json.dumps(result.to_dict())  # must not raise
