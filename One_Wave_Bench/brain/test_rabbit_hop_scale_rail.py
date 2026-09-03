import unittest

from One_Wave_Bench.brain.rabbit_hop_scale_rail import (
    DivisionRole,
    division_candidates,
    division_rail,
    forward_pair,
)


class RabbitHopScaleRailTests(unittest.TestCase):
    def test_forward_domain_is_one_through_twelve(self):
        self.assertEqual([p.tuple for p in forward_pair(1)], [(1, 2, 1), (1, 2, 3)])
        self.assertEqual([p.tuple for p in forward_pair(6)], [(6, 12, 11), (6, 12, 13)])
        self.assertEqual([p.tuple for p in forward_pair(12)], [(12, 24, 23), (12, 24, 25)])
        for invalid in (0, 13, 1.5):
            with self.assertRaises(ValueError):
                forward_pair(invalid)

    def test_division_domain_is_twelve_through_twenty_four(self):
        self.assertEqual(
            division_rail(),
            (
                (12, (6,)),
                (13, (6, 7)),
                (14, (7,)),
                (15, (7, 8)),
                (16, (8,)),
                (17, (8, 9)),
                (18, (9,)),
                (19, (9, 10)),
                (20, (10,)),
                (21, (10, 11)),
                (22, (11,)),
                (23, (11, 12)),
                (24, (12,)),
            ),
        )

    def test_even_addresses_divide_directly(self):
        for address in range(12, 25, 2):
            candidate, = division_candidates(address)
            self.assertEqual(candidate.source, address // 2)
            self.assertEqual(candidate.source_top, address)
            self.assertIs(candidate.outer_role, DivisionRole.TOP)

    def test_odd_addresses_are_shared_wrappers_not_half_addresses(self):
        for address in range(13, 24, 2):
            lower, upper = division_candidates(address)
            self.assertEqual(lower.source_top, address - 1)
            self.assertEqual(upper.source_top, address + 1)
            self.assertEqual((lower.source, upper.source), ((address - 1) // 2, (address + 1) // 2))
            self.assertIs(lower.outer_role, DivisionRole.UPPER_WRAPPER)
            self.assertIs(upper.outer_role, DivisionRole.LOWER_WRAPPER)

    def test_every_division_candidate_reconstructs_the_outer_address(self):
        for address in range(12, 25):
            for candidate in division_candidates(address):
                pair = forward_pair(candidate.source)
                values = {candidate.source_top, *(packet.wrapper for packet in pair)}
                self.assertIn(address, values)

    def test_division_rejects_addresses_outside_declared_rail(self):
        for invalid in (11, 25, 12.5):
            with self.assertRaises(ValueError):
                division_candidates(invalid)


if __name__ == "__main__":
    unittest.main()

