import math
import unittest

from group_velocity_zeros import a114_vg_undamped, receipt, vg_vp_continuum


class TwoZerosTests(unittest.TestCase):
    def test_continuum_product_is_ceff2(self):
        vg, vp = vg_vp_continuum(2.0, 1.5, 0.7, 0.0)
        self.assertAlmostEqual(vg * vp, 1.5 * 1.5, places=12)

    def test_continuum_rest_vg_zero(self):
        vg, _ = vg_vp_continuum(0.0, 1.0, 1.0, 0.0)
        self.assertEqual(vg, 0.0)

    def test_a114_zone_edge_vg_zero(self):
        self.assertAlmostEqual(a114_vg_undamped(math.pi), 0.0, places=6)

    def test_a114_long_wave_matches_leading_order(self):
        self.assertAlmostEqual(a114_vg_undamped(1e-3), 0.5, places=3)

    def test_receipt_refuses_scale(self):
        rec = receipt()
        self.assertFalse(rec["continuum_has_zone_edge"])
        self.assertFalse(rec["derived_a0"])
        self.assertFalse(rec["closes_E5"])


if __name__ == "__main__":
    unittest.main()
