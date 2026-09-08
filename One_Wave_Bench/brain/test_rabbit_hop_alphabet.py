from dataclasses import replace
import unittest

from One_Wave_Bench.brain.rabbit_hop_alphabet import (
    AlphabetMirrorLayout,
    AlphabetOrientation,
    MirrorPolarity,
    RouteFamily,
    TraversalDirection,
    WrapperSide,
    all_declared_routes,
    alphabet_map,
    alphabet_rank,
    ascending_ladder,
    connection_addresses,
    coordinate,
    mirrored_alphabet_runs,
    offset_ladder,
    recover_source_rank,
    shared_original_bridge,
    validate_coordinate,
    validate_wrapper_pair,
    wrapper_pair,
)


class RabbitHopAlphabetTests(unittest.TestCase):
    def test_three_canonical_route_families_are_declared(self):
        self.assertEqual(
            set(RouteFamily),
            {
                RouteFamily.ORIGINAL,
                RouteFamily.DOUBLE_THEN_SHIFT,
                RouteFamily.SHIFT_THEN_DOUBLE,
            },
        )

    def test_legacy_route_names_are_compatible_aliases(self):
        self.assertIs(RouteFamily.ASCENDING_AFTER, RouteFamily.DOUBLE_THEN_SHIFT)
        self.assertIs(RouteFamily.ASCENDING_BEFORE, RouteFamily.SHIFT_THEN_DOUBLE)

    def test_original_route_is_separate_and_has_both_wrappers(self):
        pair = wrapper_pair("A")
        self.assertEqual([packet.tuple for packet in pair], [(1, 2, 1), (1, 2, 3)])
        self.assertTrue(all(packet.route_family is RouteFamily.ORIGINAL for packet in pair))
        self.assertTrue(all(packet.k == 0 for packet in pair))

    def test_double_then_shift_has_complete_negative_zero_positive_ladder(self):
        ladder = offset_ladder(
            "A", route_family=RouteFamily.DOUBLE_THEN_SHIFT, min_k=-3, max_k=3
        )
        self.assertEqual(
            [[packet.tuple for packet in pair] for pair in ladder],
            [
                [(1, -1, -2), (1, -1, 0)],
                [(1, 0, -1), (1, 0, 1)],
                [(1, 1, 0), (1, 1, 2)],
                [(1, 2, 1), (1, 2, 3)],
                [(1, 3, 2), (1, 3, 4)],
                [(1, 4, 3), (1, 4, 5)],
                [(1, 5, 4), (1, 5, 6)],
            ],
        )

    def test_shift_then_double_has_complete_negative_zero_positive_ladder(self):
        ladder = offset_ladder(
            "A", route_family=RouteFamily.SHIFT_THEN_DOUBLE, min_k=-3, max_k=3
        )
        self.assertEqual(
            [[packet.tuple for packet in pair] for pair in ladder],
            [
                [(1, -4, -5), (1, -4, -3)],
                [(1, -2, -3), (1, -2, -1)],
                [(1, 0, -1), (1, 0, 1)],
                [(1, 2, 1), (1, 2, 3)],
                [(1, 4, 3), (1, 4, 5)],
                [(1, 6, 5), (1, 6, 7)],
                [(1, 8, 7), (1, 8, 9)],
            ],
        )

    def test_top_offset_and_wrapper_are_separate_operations(self):
        pair = wrapper_pair(
            "A", route_family=RouteFamily.DOUBLE_THEN_SHIFT, k=3
        )
        self.assertEqual(pair[0].top_address, 5)
        self.assertEqual([packet.wrapper_address for packet in pair], [4, 6])
        self.assertEqual(pair[0].k, 3)
        self.assertIs(pair[0].wrapper, WrapperSide.LOWER)
        self.assertIs(pair[1].wrapper, WrapperSide.UPPER)

    def test_signed_k_is_allowed_on_both_offset_routes_but_not_original(self):
        with self.assertRaises(ValueError):
            wrapper_pair("A", route_family=RouteFamily.ORIGINAL, k=1)
        with self.assertRaises(ValueError):
            wrapper_pair("A", route_family=RouteFamily.ORIGINAL, k=-1)
        for family in (
            RouteFamily.DOUBLE_THEN_SHIFT,
            RouteFamily.SHIFT_THEN_DOUBLE,
        ):
            for k in (-20, -3, -2, -1, 0, 1, 2, 3, 20):
                validate_wrapper_pair(wrapper_pair("K", route_family=family, k=k))

    def test_historical_positive_ladder_helper_still_works(self):
        ladder = ascending_ladder(
            "A", route_family=RouteFamily.ASCENDING_AFTER, max_k=3
        )
        self.assertEqual(
            [[packet.tuple for packet in pair] for pair in ladder],
            [
                [(1, 3, 2), (1, 3, 4)],
                [(1, 4, 3), (1, 4, 5)],
                [(1, 5, 4), (1, 5, 6)],
            ],
        )

    def test_equal_destination_keeps_operation_order_receipt(self):
        # 2N+2 == 2(N+1) for N=1, but the route that got there is not erased.
        after = wrapper_pair("A", route_family=RouteFamily.DOUBLE_THEN_SHIFT, k=2)
        before = wrapper_pair("A", route_family=RouteFamily.SHIFT_THEN_DOUBLE, k=1)
        self.assertEqual([p.tuple for p in after], [p.tuple for p in before])
        self.assertNotEqual(after[0].route_family, before[0].route_family)
        self.assertNotEqual(after[0].k, before[0].k)

    def test_every_top_has_mandatory_opposite_parity_wrappers(self):
        for pair in all_declared_routes("B", max_k=8):
            validate_wrapper_pair(pair)
            self.assertEqual(len(pair), 2)
            for packet in pair:
                self.assertEqual(abs(packet.wrapper_address - packet.top_address), 1)
                self.assertNotEqual(packet.top_parity, packet.wrapper_parity)

    def test_wrappers_connect_tops_across_routes_and_directions(self):
        top_four = wrapper_pair("A", route_family=RouteFamily.SHIFT_THEN_DOUBLE, k=1)
        top_five = wrapper_pair(
            "A",
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            k=3,
            traversal=TraversalDirection.REVERSE,
        )
        self.assertEqual(connection_addresses(top_four, top_five), (4, 5))
        self.assertEqual(connection_addresses(top_five, top_four), (4, 5))

    def test_alphabet_can_run_forward_or_inverted(self):
        normal = alphabet_map(AlphabetOrientation.NORMAL)
        inverted = alphabet_map(AlphabetOrientation.INVERTED)
        self.assertEqual((normal[0], normal[-1]), (("A", 1), ("Z", 26)))
        self.assertEqual((inverted[0], inverted[-1]), (("Z", 1), ("A", 26)))
        self.assertEqual(alphabet_rank("A", AlphabetOrientation.INVERTED), 26)
        self.assertEqual(alphabet_rank("Z", AlphabetOrientation.INVERTED), 1)
        self.assertEqual(wrapper_pair("A", alphabet_orientation=AlphabetOrientation.INVERTED)[0].top_address, 52)
        self.assertEqual(wrapper_pair("Z", alphabet_orientation=AlphabetOrientation.INVERTED)[0].top_address, 2)

    def test_side_inversion_also_inverts_logical_up_and_down(self):
        normal = wrapper_pair("A", alphabet_orientation=AlphabetOrientation.NORMAL)
        inverted = wrapper_pair("Z", alphabet_orientation=AlphabetOrientation.INVERTED)
        self.assertEqual([p.wrapper_address for p in normal], [1, 3])
        self.assertEqual([p.wrapper_address for p in inverted], [3, 1])
        self.assertEqual(inverted[0].wrapper, WrapperSide.LOWER)
        self.assertEqual(inverted[1].wrapper, WrapperSide.UPPER)

    def test_whole_alphabet_mirror_gate_layouts(self):
        self.assertEqual(
            mirrored_alphabet_runs(AlphabetMirrorLayout.A_TO_Z_MIRROR_Z_TO_A),
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0, "ZYXWVUTSRQPONMLKJIHGFEDCBA"),
        )
        self.assertEqual(
            mirrored_alphabet_runs(AlphabetMirrorLayout.Z_TO_A_MIRROR_A_TO_Z),
            ("ZYXWVUTSRQPONMLKJIHGFEDCBA", 0, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        )

    def test_polarity_mirrors_every_numeric_field(self):
        positive = wrapper_pair("B", route_family=RouteFamily.DOUBLE_THEN_SHIFT, k=-3)
        negative = wrapper_pair(
            "B",
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            k=-3,
            polarity=MirrorPolarity.NEGATIVE,
        )
        self.assertEqual(
            [packet.tuple for packet in negative],
            [tuple(-value for value in packet.tuple) for packet in positive],
        )

    def test_route_reversal_does_not_erase_other_receipt_fields(self):
        packet = coordinate(
            "K",
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            k=-4,
            wrapper=WrapperSide.LOWER,
        )
        opposed = packet.opposed()
        self.assertEqual(opposed.tuple, packet.tuple)
        self.assertEqual(opposed.route_family, packet.route_family)
        self.assertEqual(opposed.k, packet.k)
        self.assertNotEqual(opposed.traversal, packet.traversal)

    def test_mechanical_receipt_recovery_handles_signed_offsets(self):
        for orientation in AlphabetOrientation:
            for polarity in MirrorPolarity:
                for family, values in (
                    (RouteFamily.ORIGINAL, (0,)),
                    (RouteFamily.DOUBLE_THEN_SHIFT, (-20, -3, -1, 0, 1, 4, 20)),
                    (RouteFamily.SHIFT_THEN_DOUBLE, (-20, -3, -1, 0, 1, 4, 20)),
                ):
                    for k in values:
                        for packet in wrapper_pair(
                            "K",
                            alphabet_orientation=orientation,
                            polarity=polarity,
                            route_family=family,
                            k=k,
                        ):
                            self.assertEqual(recover_source_rank(packet), abs(packet.source_rank))
                            validate_coordinate(packet)

    def test_corrupt_receipt_fails_visibly(self):
        packet = coordinate("A")
        with self.assertRaises(ValueError):
            validate_coordinate(replace(packet, wrapper_address=99))

    def test_neighboring_original_routes_share_wrapper(self):
        self.assertEqual(shared_original_bridge("A"), 3)
        self.assertEqual(
            shared_original_bridge("Z", alphabet_orientation=AlphabetOrientation.INVERTED),
            3,
        )


if __name__ == "__main__":
    unittest.main()
