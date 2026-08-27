import unittest

from six_route_logic import (
    BinaryChoice,
    LogicRoute,
    TernaryMove,
    all_routes,
    decode_one_hot,
    validate_route_space,
)


class SixRouteLogicTests(unittest.TestCase):
    def test_two_choices_times_three_moves_is_six(self):
        routes = all_routes()
        self.assertEqual(len(routes), 6)
        self.assertEqual({route.address for route in routes}, set(range(6)))

    def test_one_hot_choices(self):
        self.assertIs(decode_one_hot((1, 0)), BinaryChoice.YES)
        self.assertIs(decode_one_hot((0, 1)), BinaryChoice.NO)

    def test_ground_is_not_a_choice(self):
        with self.assertRaisesRegex(ValueError, "Ground"):
            decode_one_hot((0, 0))

    def test_conflict_is_not_a_choice(self):
        with self.assertRaisesRegex(ValueError, "Conflict"):
            decode_one_hot((1, 1))

    def test_hold_routes_retain_binary_relation(self):
        yes_hold = LogicRoute(BinaryChoice.YES, TernaryMove.HOLD)
        no_hold = LogicRoute(BinaryChoice.NO, TernaryMove.HOLD)
        self.assertNotEqual(yes_hold, no_hold)
        self.assertNotEqual(yes_hold.address, no_hold.address)

    def test_invalid_route_set_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "six routes"):
            validate_route_space(all_routes()[:-1])


if __name__ == "__main__":
    unittest.main()

