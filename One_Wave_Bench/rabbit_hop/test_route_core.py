import unittest

from One_Wave_Bench.rabbit_hop.route_core import (
    HopReceipt,
    Polarity,
    RouteFamily,
    Traversal,
    WrapperSide,
    invert_address,
    make_receipt,
    mirror_receipt,
    oppose_receipt,
    route_address,
    route_center,
    shared_shift_boundary,
    validate_receipt,
    wrappers,
)


class RabbitHopRouteCoreTests(unittest.TestCase):
    def test_both_route_families_reconstruct_exact_n(self):
        for n in range(1, 27):
            for offset in (0, 1, 2, 7):
                for family in RouteFamily:
                    for wrapper in WrapperSide:
                        receipt = make_receipt(
                            n,
                            family,
                            offset=offset,
                            wrapper=wrapper,
                        )
                        self.assertEqual(
                            invert_address(
                                receipt.address,
                                family,
                                offset=offset,
                                wrapper=wrapper,
                            ),
                            n,
                        )

    def test_equal_destination_does_not_collapse_route_identity(self):
        n = 7
        m = 4
        double_first = make_receipt(
            n, RouteFamily.DOUBLE_FIRST, offset=2 * m
        )
        shift_first = make_receipt(
            n, RouteFamily.SHIFT_FIRST, offset=m
        )
        self.assertEqual(double_first.address, shift_first.address)
        self.assertNotEqual(double_first, shift_first)
        self.assertNotEqual(double_first.family, shift_first.family)

    def test_wrapper_is_opposite_parity_to_center(self):
        for n in (1, 2, 11):
            for family in RouteFamily:
                center = route_center(n, family, 3)
                lower, same, upper = wrappers(center)
                self.assertEqual(same, center)
                self.assertNotEqual(lower % 2, center % 2)
                self.assertNotEqual(upper % 2, center % 2)

    def test_adjacent_shift_first_nests_share_boundary(self):
        self.assertEqual(shared_shift_boundary(1), 3)
        self.assertEqual(shared_shift_boundary(2), 5)
        self.assertEqual(shared_shift_boundary(1, offset=2), 7)

    def test_negative_route_is_exact_sign_mirror(self):
        for family in RouteFamily:
            positive = make_receipt(
                5,
                family,
                offset=3,
                wrapper=WrapperSide.UPPER,
                polarity=Polarity.POSITIVE,
            )
            negative = mirror_receipt(positive)
            self.assertEqual(negative.address, -positive.address)
            self.assertEqual(negative.wrapper, positive.wrapper)
            self.assertEqual(negative.family, positive.family)

    def test_mirroring_twice_returns_original_receipt(self):
        receipt = make_receipt(
            9,
            RouteFamily.SHIFT_FIRST,
            offset=4,
            wrapper=WrapperSide.LOWER,
        )
        self.assertEqual(mirror_receipt(mirror_receipt(receipt)), receipt)

    def test_opposing_is_not_mirroring(self):
        receipt = make_receipt(
            4,
            RouteFamily.DOUBLE_FIRST,
            offset=5,
            wrapper=WrapperSide.UPPER,
        )
        opposed = oppose_receipt(receipt)
        mirrored = mirror_receipt(receipt)
        self.assertEqual(opposed.address, receipt.address)
        self.assertEqual(opposed.polarity, receipt.polarity)
        self.assertEqual(opposed.traversal, Traversal.OPPOSING)
        self.assertEqual(mirrored.address, -receipt.address)

    def test_opposing_twice_returns_original_receipt(self):
        receipt = make_receipt(3, RouteFamily.SHIFT_FIRST, offset=2)
        self.assertEqual(oppose_receipt(oppose_receipt(receipt)), receipt)

    def test_receipt_json_round_trip(self):
        receipt = make_receipt(
            13,
            RouteFamily.DOUBLE_FIRST,
            offset=8,
            wrapper=WrapperSide.LOWER,
            polarity=Polarity.NEGATIVE,
            traversal=Traversal.OPPOSING,
        )
        self.assertEqual(HopReceipt.from_json(receipt.to_json()), receipt)

    def test_corrupt_receipt_fails_visibly(self):
        receipt = make_receipt(6, RouteFamily.SHIFT_FIRST, offset=2)
        corrupt = HopReceipt(
            source_n=receipt.source_n,
            family=receipt.family,
            offset=receipt.offset,
            wrapper=receipt.wrapper,
            polarity=receipt.polarity,
            traversal=receipt.traversal,
            address=receipt.address + 2,
        )
        with self.assertRaises(ValueError):
            validate_receipt(corrupt)

    def test_wrong_inverse_receipt_fails_when_parity_is_impossible(self):
        address = route_address(3, RouteFamily.DOUBLE_FIRST, offset=1)
        with self.assertRaises(ValueError):
            invert_address(
                address,
                RouteFamily.DOUBLE_FIRST,
                offset=0,
                wrapper=WrapperSide.CENTER,
            )

    def test_large_offset_has_no_artificial_cap(self):
        receipt = make_receipt(
            2,
            RouteFamily.SHIFT_FIRST,
            offset=100_000,
            wrapper=WrapperSide.UPPER,
        )
        validate_receipt(receipt)
        self.assertEqual(
            invert_address(
                receipt.address,
                receipt.family,
                offset=receipt.offset,
                wrapper=receipt.wrapper,
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
