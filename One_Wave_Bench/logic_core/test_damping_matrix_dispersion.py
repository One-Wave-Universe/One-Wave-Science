import math
import unittest

from damping_matrix_dispersion import (
    a114_z_roots,
    attenuation_length,
    decoupled_matches_scalar,
    k_spatial_scalar,
    matrix_lambda_roots,
    omega_temporal_scalar,
    receipt_scalar,
    temporal_regime,
)


class ScalarE1Tests(unittest.TestCase):
    def test_undamped_recovers_kg(self):
        wp, wm = omega_temporal_scalar(k=2.0, c_eff=1.0, omega0=0.0, gamma=0.0)
        self.assertAlmostEqual(wp.real, 2.0, places=12)
        self.assertAlmostEqual(wp.imag, 0.0, places=12)
        self.assertAlmostEqual(wm.real, -2.0, places=12)

    def test_overdamped_is_temporal_not_spatial_label(self):
        self.assertEqual(temporal_regime(k=0.0, c_eff=1.0, omega0=0.1, gamma=2.0), "overdamped")
        kplus, _ = k_spatial_scalar(omega=0.2, c_eff=1.0, omega0=0.1, gamma=0.01)
        self.assertTrue(abs(kplus.imag) >= 0.0)

    def test_attenuation_positive_when_damped(self):
        ell = attenuation_length(omega=0.3, c_eff=1.0, omega0=0.0, gamma=0.4)
        self.assertGreater(ell, 0.0)
        self.assertLess(ell, float("inf"))

    def test_receipt_refuses_e5_and_a0(self):
        rec = receipt_scalar(1.0, 1.0, 0.0, 0.1)
        self.assertFalse(rec["closes_E5"])
        self.assertFalse(rec["derived_a0"])


class A114Tests(unittest.TestCase):
    def test_gamma_zero_unit_circle(self):
        z1, z2 = a114_z_roots(k=0.01, dx=1.0, beta=0.5, gamma=0.0)
        self.assertAlmostEqual(abs(z1), 1.0, places=9)
        self.assertAlmostEqual(abs(z2), 1.0, places=9)

    def test_product_is_one_minus_gamma(self):
        z1, z2 = a114_z_roots(k=0.3, dx=1.0, beta=0.5, gamma=0.2)
        self.assertAlmostEqual((z1 * z2).real, 0.8, places=12)
        self.assertAlmostEqual((z1 * z2).imag, 0.0, places=12)


class MatrixTests(unittest.TestCase):
    def test_decoupled_contains_scalar_pair(self):
        self.assertTrue(decoupled_matches_scalar(k=1.5, c_eff=1.0, omega0=0.2, gamma=0.1))

    def test_coupling_splits_product_offset(self):
        roots0 = matrix_lambda_roots(1.0, 1.0, 1.0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.0)
        roots1 = matrix_lambda_roots(1.0, 1.0, 1.0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.4)
        self.assertFalse(sorted(roots0.real) == sorted(roots1.real))


if __name__ == "__main__":
    unittest.main()
