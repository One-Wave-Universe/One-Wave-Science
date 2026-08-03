import pytest

from onewave_mapper import chord_geometry


def note_hz(semitones_from_a4: int) -> float:
    return 440.0 * 2 ** (semitones_from_a4 / 12.0)


def test_semitone_distance_matches_upward_interval():
    root = note_hz(0)
    fifth = note_hz(7)
    assert chord_geometry.semitone_distance(fifth, root) == 7


def test_mirrored_coordinate_interior_positions():
    assert chord_geometry.mirrored_coordinate(0) == 0
    assert chord_geometry.mirrored_coordinate(4) == 4
    assert chord_geometry.mirrored_coordinate(5) == 5


def test_mirrored_coordinate_negative_positions():
    assert chord_geometry.mirrored_coordinate(7) == -5
    assert chord_geometry.mirrored_coordinate(11) == -1


def test_mirrored_coordinate_shared_mirror():
    assert chord_geometry.mirrored_coordinate(6) == "±6"


def test_chord_coordinates_major_triad_matches_canon_example():
    # E-511: Major triad {0, +4, -5}
    root = note_hz(0)
    third = note_hz(4)
    fifth = note_hz(7)
    result = chord_geometry.chord_coordinates([root, third, fifth], root_hz=root)
    assert result.coordinates == [0, 4, -5]


def test_chord_coordinates_minor_triad_matches_canon_example():
    # E-511: Minor triad {0, +3, -5}
    root = note_hz(0)
    minor_third = note_hz(3)
    fifth = note_hz(7)
    result = chord_geometry.chord_coordinates([root, minor_third, fifth], root_hz=root)
    assert result.coordinates == [0, 3, -5]


def test_chord_coordinates_augmented_triad_matches_canon_example():
    # E-511: Augmented triad {0, +4, -4}
    root = note_hz(0)
    third = note_hz(4)
    sharp_fifth = note_hz(8)  # 8 semitones up == -4 mirrored
    result = chord_geometry.chord_coordinates([root, third, sharp_fifth], root_hz=root)
    assert result.coordinates == [0, 4, -4]


def test_chord_coordinates_diminished_triad_matches_canon_example():
    # E-511: Diminished triad {0, +3, ±6}
    root = note_hz(0)
    minor_third = note_hz(3)
    tritone = note_hz(6)
    result = chord_geometry.chord_coordinates([root, minor_third, tritone], root_hz=root)
    assert result.coordinates == [0, 3, "±6"]


def test_chord_coordinates_power_chord_matches_canon_example():
    # E-511: Power chord {0, -5}
    root = note_hz(0)
    fifth = note_hz(7)
    result = chord_geometry.chord_coordinates([root, fifth], root_hz=root)
    assert result.coordinates == [0, -5]


def test_chord_coordinates_defaults_root_to_lowest_tone():
    low = note_hz(0)
    high = note_hz(4)
    result = chord_geometry.chord_coordinates([high, low])
    assert result.root_hz == low


def test_envelope_boundary_augmented_matches_augmented_balance_geometry():
    root = note_hz(0)
    third = note_hz(4)
    sharp_fifth = note_hz(8)
    coords = chord_geometry.chord_coordinates([root, third, sharp_fifth], root_hz=root)
    boundary = chord_geometry.envelope_boundary(coords)
    assert (boundary.low, boundary.high) == (-4, 4)
    assert boundary.matched_geometry == "augmented_balance"
    assert boundary.is_retired_representation is True


def test_envelope_boundary_major_triad_does_not_force_a_named_match():
    # Canon Major triad boundary is (-5, 4), which is NOT one of the four
    # named geometries -- the mapper must not force it into one anyway.
    root = note_hz(0)
    third = note_hz(4)
    fifth = note_hz(7)
    coords = chord_geometry.chord_coordinates([root, third, fifth], root_hz=root)
    boundary = chord_geometry.envelope_boundary(coords)
    assert (boundary.low, boundary.high) == (-5, 4)
    assert boundary.matched_geometry is None


def test_envelope_boundary_excludes_shared_mirror_tone():
    root = note_hz(0)
    minor_third = note_hz(3)
    tritone = note_hz(6)
    coords = chord_geometry.chord_coordinates([root, minor_third, tritone], root_hz=root)
    boundary = chord_geometry.envelope_boundary(coords)
    # only numeric coordinates [0, 3] considered; "±6" excluded
    assert (boundary.low, boundary.high) == (0, 3)


def test_named_geometries_are_available_for_lookup():
    assert chord_geometry.NAMED_ENVELOPE_GEOMETRIES["triad"] == (-3, 5)
    assert chord_geometry.NAMED_ENVELOPE_GEOMETRIES["augmented_balance"] == (-4, 4)
    assert chord_geometry.NAMED_ENVELOPE_GEOMETRIES["wider_augmented"] == (-5, 5)
    assert chord_geometry.NAMED_ENVELOPE_GEOMETRIES["augmented_third"] == (-3, 3)


def test_chord_coordinates_rejects_empty_input():
    with pytest.raises(ValueError):
        chord_geometry.chord_coordinates([])
