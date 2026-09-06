import math
import unittest

from e4_seven_cell import Coeff, dipole_seed, e4, symmetric_hold


class SevenCellE4Tests(unittest.TestCase):
    def test_symmetric_zero_dipole_and_circulation(self):
        rec = e4(symmetric_hold())
        self.assertAlmostEqual(rec["Gamma"], 0.0, places=12)
        self.assertAlmostEqual(rec["theta"], 0.0, places=12)
        self.assertAlmostEqual(rec["R"], 1.0, places=12)

    def test_pi_seed_lands_near_pi_angle(self):
        rec = e4(dipole_seed(0.08, well=math.pi))
        self.assertGreater(abs(rec["theta"]), 1.0)

    def test_energy_finite(self):
        self.assertGreater(e4(symmetric_hold(), Coeff(chi=0.2))["total"], -1.0)


if __name__ == "__main__":
    unittest.main()
