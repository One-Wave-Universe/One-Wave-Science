import math
import unittest

from path_rotation import path_receipt, regular_hex, turning_angle


class PathRotationTests(unittest.TestCase):
    def test_hex_closes_one_turn(self):
        rec = path_receipt(regular_hex(), closed=True)
        self.assertAlmostEqual(rec["turning"], 2.0 * math.pi, places=10)
        self.assertEqual(rec["n_corners"], 6)
        self.assertIsNone(rec["L"])
        self.assertFalse(rec["magnetic_gradient_applied"])
        self.assertEqual(rec["gravity_coefficient_on_point"], 0.0)

    def test_straight_ride_does_not_turn(self):
        points = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (2.0, 0.0, 0.0))
        self.assertAlmostEqual(turning_angle(*points), 0.0, places=12)
        rec = path_receipt(points, closed=False)
        self.assertAlmostEqual(rec["turning"], 0.0, places=12)

    def test_right_angle_is_not_a_point_receipt(self):
        points = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0))
        self.assertAlmostEqual(turning_angle(*points), math.pi / 2.0, places=12)
        self.assertIsNone(path_receipt(points)["L"])


if __name__ == "__main__":
    unittest.main()
