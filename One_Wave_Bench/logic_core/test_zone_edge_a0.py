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

    def test_fermi_target_requires_slow_ceff(self):
        a0_fm = zone_edge_a0_m(E125_MEV, 1.0) / 1e-15
        ratio = 1.0 / a0_fm
        self.assertAlmostEqual(ratio, 1.0 / a0_fm)
        self.assertLess(ratio, 0.01)


if __name__ == "__main__":
    unittest.main()
