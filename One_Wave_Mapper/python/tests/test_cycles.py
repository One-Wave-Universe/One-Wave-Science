import numpy as np

from onewave_mapper import signal_generator, cycles
from onewave_mapper.cycles import CycleLevel


def test_detect_point_cycles_matches_known_period():
    sr = 48000
    freq = 220.0
    sine = signal_generator.sine(freq, 0.1, sr, amplitude=1.0)
    point_cycles = cycles.detect_point_cycles(sine, sr)

    assert len(point_cycles) > 0
    periods = [c.period_samples for c in point_cycles]
    expected_period = sr / freq
    assert all(abs(p - expected_period) < 1.0 for p in periods)
    assert all(c.cycle_level == CycleLevel.POINT.value for c in point_cycles)


def test_detect_modulation_cycle_finds_tremolo_rate():
    sr = 48000
    signal = signal_generator.amplitude_modulated(440, 6.0, 3.0, sr, mod_depth=0.8)
    mod_cycle = cycles.detect_modulation_cycle(signal, sr, min_mod_hz=0.5, max_mod_hz=20.0)

    assert mod_cycle is not None
    assert abs(mod_cycle.frequency_hz - 6.0) < 0.3
    assert mod_cycle.cycle_level == CycleLevel.PATH.value


def test_detect_modulation_cycle_none_for_flat_envelope():
    sr = 48000
    signal = signal_generator.sine(440, 1.0, sr, amplitude=1.0)
    mod_cycle = cycles.detect_modulation_cycle(signal, sr, min_confidence=0.3)
    assert mod_cycle is None


def test_build_note_cycle_tree_links_parent_and_children():
    sr = 48000
    signal = signal_generator.guitar_note(220, 1.0, sr, vibrato_hz=5.5, vibrato_depth_cents=40.0)
    tree = cycles.build_note_cycle_tree(signal, sr, max_point_cycles=10)

    path_cycle = tree["path_cycle"]
    assert path_cycle.cycle_level == CycleLevel.PATH.value
    assert len(tree["point_cycles"]) == 10
    for point_cycle in tree["point_cycles"]:
        assert point_cycle.parent_cycle_id == path_cycle.cycle_id
        assert point_cycle.cycle_id in path_cycle.child_cycle_ids

    if tree["modulation_cycle"] is not None:
        assert tree["modulation_cycle"].parent_cycle_id == path_cycle.cycle_id
        assert tree["modulation_cycle"].cycle_id in path_cycle.child_cycle_ids


def test_build_field_cycle_groups_children():
    sr = 48000
    note_a = signal_generator.guitar_note(220, 1.0, sr)
    note_b = signal_generator.guitar_note(330, 1.0, sr)

    tree_a = cycles.build_note_cycle_tree(note_a, sr, max_point_cycles=4)
    tree_b = cycles.build_note_cycle_tree(note_b, sr, max_point_cycles=4)

    field_cycle = cycles.build_field_cycle([tree_a["path_cycle"], tree_b["path_cycle"]])

    assert field_cycle.cycle_level == CycleLevel.FIELD.value
    assert set(field_cycle.child_cycle_ids) == {tree_a["path_cycle"].cycle_id, tree_b["path_cycle"].cycle_id}
    assert tree_a["path_cycle"].parent_cycle_id == field_cycle.cycle_id
    assert tree_b["path_cycle"].parent_cycle_id == field_cycle.cycle_id


def test_modulation_spectrum_separates_from_carrier_frequency():
    sr = 48000
    signal = signal_generator.amplitude_modulated(2000, 4.0, 2.0, sr, mod_depth=0.9)
    result = cycles.modulation_spectrum(signal, sr, feature="envelope")
    peak_freq = result["freqs_hz"][np.argmax(result["magnitude"])]
    assert peak_freq < 50  # modulation-rate peak, nowhere near the 2000 Hz carrier
