import unittest

from One_Wave_Bench.brain.rabbit_hop_core import (
    MirrorPolarity,
    RouteFamily,
    TraversalDirection,
    WrapperSide,
    connection_addresses,
    numeric_coordinate,
    numeric_offset_ladder,
    numeric_wrapper_pair,
    recover_source_rank,
    validate_numeric_receipt,
)


class RabbitHopCoreTests(unittest.TestCase):
    def test_double_then_shift_signed_k_minus_three_through_plus_three(self):
        ladder = numeric_offset_ladder(
            1,
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            min_k=-3,
            max_k=3,
        )
        self.assertEqual(
            [[record.tuple for record in pair] for pair in ladder],
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

    def test_shift_then_double_signed_k_minus_three_through_plus_three(self):
        ladder = numeric_offset_ladder(
            1,
            route_family=RouteFamily.SHIFT_THEN_DOUBLE,
            min_k=-3,
            max_k=3,
        )
        self.assertEqual(
            [pair[0].top_address for pair in ladder],
            [-4, -2, 0, 2, 4, 6, 8],
        )

    def test_offset_and_wrapper_are_separate_receipt_fields(self):
        record = numeric_coordinate(
            1,
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            k=3,
            wrapper=WrapperSide.UPPER,
        )
        self.assertEqual(record.top_address, 5)
        self.assertEqual(record.wrapper_address, 6)
        self.assertEqual(record.k, 3)
        self.assertIs(record.wrapper, WrapperSide.UPPER)

    def test_equal_destination_retains_operation_order(self):
        double_then_shift = numeric_coordinate(
            1,
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            k=2,
        )
        shift_then_double = numeric_coordinate(
            1,
            route_family=RouteFamily.SHIFT_THEN_DOUBLE,
            k=1,
        )
        self.assertEqual(double_then_shift.tuple, shift_then_double.tuple)
        self.assertNotEqual(
            double_then_shift.route_family, shift_then_double.route_family
        )
        self.assertNotEqual(double_then_shift.k, shift_then_double.k)

    def test_complete_receipt_rebuilds_source_for_large_signed_offsets(self):
        for source in (1, 6, 12, 26):
            for family, ks in (
                (RouteFamily.ORIGINAL, (0,)),
                (RouteFamily.DOUBLE_THEN_SHIFT, (-50, -3, -1, 0, 1, 3, 50)),
                (RouteFamily.SHIFT_THEN_DOUBLE, (-50, -3, -1, 0, 1, 3, 50)),
            ):
                for k in ks:
                    for polarity in MirrorPolarity:
                        for record in numeric_wrapper_pair(
                            source,
                            route_family=family,
                            k=k,
                            polarity=polarity,
                        ):
                            validate_numeric_receipt(record)
                            self.assertEqual(recover_source_rank(record), source)

    def test_vertical_inversion_swaps_logical_wrapper_numbers(self):
        normal = numeric_wrapper_pair(1, vertical_sign=1)
        inverted = numeric_wrapper_pair(1, vertical_sign=-1)
        self.assertEqual([r.wrapper_address for r in normal], [1, 3])
        self.assertEqual([r.wrapper_address for r in inverted], [3, 1])

    def test_reverse_traversal_keeps_route_math(self):
        record = numeric_coordinate(
            7,
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            k=-3,
            traversal=TraversalDirection.FORWARD,
        )
        opposed = record.opposed()
        self.assertEqual(record.tuple, opposed.tuple)
        self.assertEqual(record.k, opposed.k)
        self.assertEqual(record.route_family, opposed.route_family)
        self.assertIs(opposed.traversal, TraversalDirection.REVERSE)

    def test_shared_connectors_cross_route_families(self):
        top_four = numeric_wrapper_pair(
            1, route_family=RouteFamily.SHIFT_THEN_DOUBLE, k=1
        )
        top_five = numeric_wrapper_pair(
            1, route_family=RouteFamily.DOUBLE_THEN_SHIFT, k=3
        )
        self.assertEqual(connection_addresses(top_four, top_five), (4, 5))


if __name__ == "__main__":
    unittest.main()
