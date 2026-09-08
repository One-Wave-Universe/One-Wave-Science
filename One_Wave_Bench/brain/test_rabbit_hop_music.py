import unittest

from One_Wave_Bench.brain.rabbit_hop_core import RouteFamily
from One_Wave_Bench.brain.rabbit_hop_music import (
    FifthDirection,
    NoteSpelling,
    ONE_WAVE_MAJOR_SPAN,
    ONE_WAVE_MINOR_SPAN,
    chromatic_source_rank,
    circle_index,
    circle_of_fifths,
    fifths_rabbit_route,
    flip_span,
    music_offset_ladder,
    music_wrapper_pair,
    note_name,
    pitch_class,
    recover_music_source,
    source_rank_note,
    span_notes,
    transpose,
)


class RabbitHopMusicTests(unittest.TestCase):
    def test_enharmonic_spellings_share_pitch_class(self):
        for left, right in (
            ("C#", "Db"),
            ("D#", "Eb"),
            ("F#", "Gb"),
            ("G#", "Ab"),
            ("A#", "Bb"),
            ("B#", "C"),
            ("Cb", "B"),
            ("E#", "F"),
            ("Fb", "E"),
        ):
            self.assertEqual(pitch_class(left), pitch_class(right))

    def test_chromatic_adapter_is_reversible_one_through_twelve(self):
        expected = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
        self.assertEqual(
            tuple(source_rank_note(rank) for rank in range(1, 13)),
            expected,
        )
        for rank, note in enumerate(expected, start=1):
            self.assertEqual(chromatic_source_rank(note), rank)

    def test_sharp_and_flat_display_maps_are_explicit(self):
        self.assertEqual(note_name(1, spelling=NoteSpelling.SHARPS), "C#")
        self.assertEqual(note_name(1, spelling=NoteSpelling.FLATS), "Db")
        self.assertEqual(note_name(10, spelling=NoteSpelling.SHARPS), "A#")
        self.assertEqual(note_name(10, spelling=NoteSpelling.FLATS), "Bb")

    def test_transpose_wraps_modulo_twelve(self):
        self.assertEqual(transpose("B", 1), "C")
        self.assertEqual(transpose("C", -1), "B")
        self.assertEqual(transpose("F#", 12), "F#")

    def test_forward_circle_of_fifths_has_all_twelve_pitch_classes(self):
        circle = circle_of_fifths("C")
        self.assertEqual(
            circle,
            ("C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"),
        )
        self.assertEqual(len({pitch_class(note) for note in circle}), 12)
        self.assertEqual(circle_of_fifths("C", include_return=True)[-1], "C")

    def test_reverse_circle_of_fifths_is_reversible(self):
        reverse = circle_of_fifths(
            "C",
            direction=FifthDirection.REVERSE,
            spelling=NoteSpelling.FLATS,
        )
        self.assertEqual(
            reverse,
            ("C", "F", "Bb", "Eb", "Ab", "Db", "Gb", "B", "E", "A", "D", "G"),
        )
        for note in reverse:
            forward_index = circle_index(note, start="C", direction=FifthDirection.FORWARD)
            reverse_index = circle_index(note, start="C", direction=FifthDirection.REVERSE)
            self.assertEqual((forward_index + reverse_index) % 12, 0)

    def test_music_uses_complete_signed_k_rabbit_hop_family(self):
        ladder = music_offset_ladder(
            "C",
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            min_k=-3,
            max_k=3,
        )
        self.assertEqual([pair[0].top_address for pair in ladder], [-1, 0, 1, 2, 3, 4, 5])
        self.assertEqual(
            [[record.wrapper_address for record in pair] for pair in ladder],
            [[-2, 0], [-1, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],
        )

    def test_music_shift_then_double_family_is_also_complete(self):
        ladder = music_offset_ladder(
            "C",
            route_family=RouteFamily.SHIFT_THEN_DOUBLE,
            min_k=-3,
            max_k=3,
        )
        self.assertEqual([pair[0].top_address for pair in ladder], [-4, -2, 0, 2, 4, 6, 8])

    def test_music_receipt_rebuilds_original_note(self):
        for note in ("C", "Db", "E", "F#", "Bb", "B"):
            for family, ks in (
                (RouteFamily.ORIGINAL, (0,)),
                (RouteFamily.DOUBLE_THEN_SHIFT, (-3, -1, 0, 2, 3)),
                (RouteFamily.SHIFT_THEN_DOUBLE, (-3, -1, 0, 2, 3)),
            ):
                for k in ks:
                    for record in music_wrapper_pair(note, route_family=family, k=k):
                        recovered = recover_music_source(record)
                        self.assertEqual(pitch_class(recovered), pitch_class(note))

    def test_circle_can_compile_directly_to_rabbit_hop_receipts(self):
        route = fifths_rabbit_route(
            "C",
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            k=3,
        )
        self.assertEqual(len(route), 12)
        self.assertEqual([pair[0].note for pair in route[:4]], ["C", "G", "D", "A"])
        for pair in route:
            self.assertEqual(pair[0].k, 3)
            self.assertEqual(pair[0].route_family, RouteFamily.DOUBLE_THEN_SHIFT)
            self.assertEqual(pair[0].wrapper_address, pair[0].top_address - 1)
            self.assertEqual(pair[1].wrapper_address, pair[1].top_address + 1)

    def test_one_wave_major_minor_spans_are_explicit_project_conventions(self):
        self.assertEqual(ONE_WAVE_MAJOR_SPAN.tuple, (-5, 0, 4))
        self.assertEqual(ONE_WAVE_MINOR_SPAN.tuple, (-5, 0, 3))
        self.assertEqual(flip_span(ONE_WAVE_MAJOR_SPAN).tuple, (-4, 0, 5))
        self.assertEqual(flip_span(flip_span(ONE_WAVE_MAJOR_SPAN)), ONE_WAVE_MAJOR_SPAN)
        self.assertEqual(flip_span(ONE_WAVE_MINOR_SPAN).tuple, (-3, 0, 5))

    def test_span_notes_are_pitch_class_coordinates_not_theory_claims(self):
        self.assertEqual(span_notes("A", ONE_WAVE_MAJOR_SPAN), ("E", "A", "C#"))
        self.assertEqual(span_notes("A", ONE_WAVE_MINOR_SPAN), ("E", "A", "C"))


if __name__ == "__main__":
    unittest.main()
