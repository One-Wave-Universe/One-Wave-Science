import math
import unittest

from mirror_operator import (
    PhaseState,
    apply_mirror_phase,
    at_shared_center,
    classify_move,
    mirror_route,
    rotate_phase,
)
from six_route_logic import LogicRoute, TernaryMove, all_routes


class MirrorOperatorTests(unittest.TestCase):
    def test_discrete_mirror_preserves_binary_choice(self):
        for route in all_routes():
            self.assertIs(mirror_route(route).choice, route.choice)

    def test_discrete_mirror_is_an_involution(self):
        for route in all_routes():
            self.assertEqual(mirror_route(mirror_route(route)), route)

    def test_hold_is_fixed_only_in_discrete_projection(self):
        fixed = [route for route in all_routes() if mirror_route(route) == route]
        self.assertEqual(len(fixed), 2)
        self.assertTrue(all(route.move is TernaryMove.HOLD for route in fixed))

    def test_half_cycle_reverses_continuous_state_and_move(self):
        state = PhaseState(0.25, 0.75)
        receipt = apply_mirror_phase(state, math.pi)
        self.assertAlmostEqual(receipt.after.x, -state.x)
        self.assertAlmostEqual(receipt.after.v_scaled, -state.v_scaled)
        self.assertIs(receipt.before_move, TernaryMove.UP)
        self.assertIs(receipt.after_move, TernaryMove.DOWN)

    def test_full_cycle_returns_to_reference(self):
        state = PhaseState(-0.2, 0.9)
        returned = rotate_phase(state, 2.0 * math.pi)
        self.assertAlmostEqual(returned.x, state.x)
        self.assertAlmostEqual(returned.v_scaled, state.v_scaled)

    def test_undamped_phase_rotation_preserves_amplitude(self):
        state = PhaseState(0.6, -0.8)
        for angle in (0.1, math.pi / 2, math.pi, 4.7):
            self.assertAlmostEqual(rotate_phase(state, angle).amplitude, 1.0)

    def test_center_crossing_and_hold_are_not_the_same_measurement(self):
        crossing = PhaseState(0.0, 1.0)
        turning_hold = PhaseState(1.0, 0.0)
        self.assertTrue(at_shared_center(crossing))
        self.assertIs(classify_move(crossing), TernaryMove.UP)
        self.assertFalse(at_shared_center(turning_hold))
        self.assertIs(classify_move(turning_hold), TernaryMove.HOLD)

    def test_negative_bands_are_rejected(self):
        with self.assertRaises(ValueError):
            classify_move(PhaseState(0.0, 0.0), -1.0)
        with self.assertRaises(ValueError):
            at_shared_center(PhaseState(0.0, 0.0), -1.0)


if __name__ == "__main__":
    unittest.main()

