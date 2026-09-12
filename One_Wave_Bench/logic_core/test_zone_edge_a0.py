import unittest

from zone_edge_a0 import E125_MEV, receipt, zone_edge_a0_m


class ZoneEdgeA0Tests(unittest.TestCase):
    def test_gray_control_is_attometer_not_fermi(self):
        a0 = zone_edge_a0_m(E125_MEV, 1.0)
        self.assertGreater(a0, 4.9e-18)
        self.assertLess(a0, 5.0e-18)

    def test_receipt_refuses_derived_and_hoyle(self):
        rec = receipt()
        self.assertFalse(rec["derived"])
        self.assertFalse(rec["allowed_in_blind_hoyle_test"])
        self.assertEqual(rec["brick"], "Yellow")
        self.assertEqual(len(rec["assumptions"]), 4)

    def test_fermi_target_requires_superluminal_ceff(self):
        # a0 scales directly with c_eff in this formula (a0 = pi*hbar*c_eff/E),
        # so closing the ~1000x gap between the Gray-control a0 (~0.005 fm)
        # and a Fermi-scale target (1 fm) requires c_eff/c to be LARGE
        # (faster than light), not small. An earlier version of this test
        # (and of the G-745 node it mirrors) inverted the fraction and
        # required a small ratio instead -- see G-745's corrected math.
        a0_fm = zone_edge_a0_m(E125_MEV, 1.0) / 1e-15
        required_c_eff_over_c = 1.0 / a0_fm
        self.assertGreater(required_c_eff_over_c, 100.0)


if __name__ == "__main__":
    unittest.main()
