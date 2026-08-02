import numpy as np

from onewave_mapper import signal_generator, one_wave_views


def test_inward_rule_fires_on_decaying_note():
    sr = 48000
    signal = signal_generator.exponential_decay(440, 1.5, sr, decay_tau_seconds=0.3, amplitude=1.0)
    tag = one_wave_views.inward_rule(signal, sr, 0, len(signal))
    assert tag is not None
    assert tag.tag == "Inward"
    assert tag.evidence["envelope_slope_db_per_second"] < 0
    assert tag.confidence > 0


def test_outward_rule_fires_on_rising_attack():
    sr = 48000
    t = np.arange(int(0.05 * sr)) / sr
    rising = np.exp(t / 0.01) * np.sin(2 * np.pi * 440 * t)
    rising /= np.max(np.abs(rising))
    tag = one_wave_views.outward_rule(rising, sr, 0, len(rising))
    assert tag is not None
    assert tag.tag == "Outward"
    assert tag.evidence["envelope_slope_db_per_second"] > 0


def test_outward_and_inward_are_mutually_exclusive_on_same_segment():
    sr = 48000
    decaying = signal_generator.exponential_decay(440, 1.0, sr, decay_tau_seconds=0.3, amplitude=1.0)
    assert one_wave_views.outward_rule(decaying, sr, 0, len(decaying)) is None

    t = np.arange(int(0.05 * sr)) / sr
    rising = np.exp(t / 0.01) * np.sin(2 * np.pi * 440 * t)
    assert one_wave_views.inward_rule(rising, sr, 0, len(rising)) is None


def test_across_rule_reports_zero_crossings():
    sr = 48000
    signal = signal_generator.sine(440, 0.1, sr)
    tag = one_wave_views.across_rule(signal, sr, 1000, 1000 + len(signal))
    assert tag is not None
    assert tag.tag == "Across"
    assert tag.evidence["zero_crossing_count"] > 0
    assert tag.start_sample == 1000


def test_across_rule_none_for_dc_signal():
    signal = np.ones(1000) * 0.5
    tag = one_wave_views.across_rule(signal, 48000, 0, 1000)
    assert tag is None


def test_over_rule_matches_spec_example_shape():
    sr = 48000
    signal = signal_generator.amplitude_modulated(440, 5.8, 3.0, sr, mod_depth=0.8)
    tag = one_wave_views.over_rule(signal, sr, 144000, 144000 + len(signal))
    assert tag is not None
    assert tag.tag == "Over"
    assert abs(tag.evidence["modulation_frequency_hz"] - 5.8) < 0.3
    assert "repeating modulation" in tag.reasons[0]
    assert any("confidence" in r for r in tag.reasons)
    assert tag.start_sample == 144000


def test_over_rule_none_for_unmodulated_tone():
    sr = 48000
    signal = signal_generator.sine(440, 1.0, sr)
    tag = one_wave_views.over_rule(signal, sr, 0, len(signal))
    assert tag is None


def test_classify_window_can_return_multiple_simultaneous_tags():
    sr = 48000
    carrier = signal_generator.amplitude_modulated(440, 6.0, 2.0, sr, mod_depth=0.9)
    decay_envelope = np.exp(-np.arange(len(carrier)) / (sr * 0.5))
    signal = carrier * decay_envelope

    tags = one_wave_views.classify_window(signal, sr)
    tag_names = {t.tag for t in tags}
    assert "Inward" in tag_names
    assert "Over" in tag_names


def test_classify_window_respects_custom_rule_list():
    sr = 48000
    signal = signal_generator.sine(440, 0.1, sr)
    tags = one_wave_views.classify_window(signal, sr, rules=[one_wave_views.across_rule])
    assert all(t.tag == "Across" for t in tags)


def test_tag_str_matches_spec_reason_format():
    tag = one_wave_views.OneWaveTag(
        tag="Over", reasons=["5.8 Hz repeating modulation", "confidence 0.91"],
        confidence=0.91, start_sample=144000, end_sample=288000,
    )
    text = str(tag)
    assert text.startswith("Tag: Over\nReason:\n")
    assert "- 5.8 Hz repeating modulation" in text
