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

    def test_fermi_target_requires_ceff_past_the_gray_anchor(self):
        # a0 scales directly with c_eff in this formula (a0 = pi*hbar*c_eff/E),
        # so closing the ~1000x gap between the Gray-control a0 (~0.005 fm)
        # and a Fermi-scale target (1 fm) requires c_eff/c to be LARGE, not
        # small -- roughly 200x past the Gray c_eff~=c anchor. An earlier
        # version of this test (and of the G-745 node it mirrors) inverted
        # the fraction and required a small ratio instead.
        #
        # This is not a relativity/superluminal-speed argument -- that is
        # not this framework's own criterion. C-309 Friction Limit /
        # Propagation Ceiling already names the actual bound a lattice
        # candidate answers to (c_lat = sqrt(beta_max)*dx/dt, from the
        # lattice's own coupling/discretization parameters), and leaves
        # "does long-wave signal speed match measured c" as an open Yellow
        # item, not a fixed identity. So this test only pins the required
        # ratio down as a number; whether that ratio is allowed is a
        # question for C-309's own (currently undetermined) formula.
        a0_fm = zone_edge_a0_m(E125_MEV, 1.0) / 1e-15
        required_c_eff_over_c = 1.0 / a0_fm
        self.assertGreater(required_c_eff_over_c, 100.0)


if __name__ == "__main__":
    unittest.main()
