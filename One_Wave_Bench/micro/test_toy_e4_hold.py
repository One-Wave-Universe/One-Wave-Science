import math
import unittest

from toy_e4_hold import Q, descend, e4, two_basins


class ToyE4Tests(unittest.TestCase):
    def test_hold_near_unit_knot(self):
        q = descend(Q(1.2, 1.9, 0.1, 0.0))
        self.assertAlmostEqual(q.rk, 1.0, delta=0.15)
        self.assertLess(e4(q)["total"], e4(Q(1.2, 1.9, 0.1, 0.0))["total"])

    def test_two_basins_exist(self):
        rec = two_basins()
        self.assertFalse(rec["is_C322"])
        self.assertFalse(rec["derived_a0"])
        th0 = rec["basin_0"]["q"][2]
        thp = rec["basin_pi"]["q"][2]
        self.assertLess(abs(th0), 0.4)
        self.assertLess(abs(thp - math.pi), 0.4)


if __name__ == "__main__":
    unittest.main()
