import unittest

from One_Wave_Bench.brain.rabbit_hop_core import RouteFamily
from One_Wave_Bench.brain.rabbit_hop_neck import (
    DEFAULT_MAX_FRET,
    STANDARD_GUITAR_TUNING,
    fret_note,
    neck_map,
    neck_position,
    neck_rabbit_pair,
)


class RabbitHopNeckTests(unittest.TestCase):
    def test_standard_tuning_is_six_to_one(self):
        self.assertEqual(
            STANDARD_GUITAR_TUNING,
            ((6, "E"), (5, "A"), (4, "D"), (3, "G"), (2, "B"), (1, "E")),
        )

    def test_twelve_and_twenty_four_frets_return_octaves(self):
        for open_note in ("E", "A", "D", "G", "B"):
            self.assertEqual(fret_note(open_note, 12), open_note)
            self.assertEqual(fret_note(open_note, 24), open_note)

    def test_known_neck_positions(self):
        self.assertEqual(neck_position(6, 0).note, "E")
        self.assertEqual(neck_position(6, 5).note, "A")
        self.assertEqual(neck_position(5, 0).note, "A")
        self.assertEqual(neck_position(2, 1).note, "C")
        self.assertEqual(neck_position(1, 12).note, "E")

    def test_default_map_is_six_strings_times_open_through_fret_24(self):
        positions = neck_map()
        self.assertEqual(DEFAULT_MAX_FRET, 24)
        self.assertEqual(len(positions), 6 * 25)
        self.assertEqual({p.string_number for p in positions}, {1, 2, 3, 4, 5, 6})
        self.assertEqual({p.fret for p in positions}, set(range(25)))
        self.assertEqual(len({p.pitch_class for p in positions}), 12)

    def test_every_neck_position_can_use_full_signed_route_family(self):
        for k in (-3, -2, -1, 0, 1, 2, 3):
            pair = neck_rabbit_pair(
                6,
                5,
                route_family=RouteFamily.DOUBLE_THEN_SHIFT,
                k=k,
            )
            self.assertEqual(pair[0].note, "A")
            self.assertEqual(pair[0].k, k)
            self.assertEqual(pair[0].wrapper_address, pair[0].top_address - 1)
            self.assertEqual(pair[1].wrapper_address, pair[1].top_address + 1)

    def test_shift_then_double_is_also_available_on_neck_positions(self):
        pair = neck_rabbit_pair(
            3,
            2,
            route_family=RouteFamily.SHIFT_THEN_DOUBLE,
            k=3,
        )
        self.assertEqual(pair[0].note, "A")
        self.assertEqual(pair[0].route_family, RouteFamily.SHIFT_THEN_DOUBLE)
        self.assertEqual(pair[0].k, 3)


if __name__ == "__main__":
    unittest.main()
