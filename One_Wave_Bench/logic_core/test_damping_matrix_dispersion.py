import math
import unittest

from damping_matrix_dispersion import (
    E5_GATE,
    MATRIX_GATE,
    SCALAR_GATE,
    a114_z_roots,
    attenuation_length,
    decoupled_matches_scalar,
    group_velocity_analytic,
    k_spatial_scalar,
    matrix_lambda_roots,
    omega_temporal_scalar,
    receipt_scalar,
    temporal_regime,
)


class ScalarE1Tests(unittest.TestCase):
    def test_gates_split(self):
        self.assertEqual(SCALAR_GATE, "GREEN")
        self.assertEqual(MATRIX_GATE, "YELLOW")
        self.assertEqual(E5_GATE, "YELLOW")

    def test_undamped_recovers_kg(self):
        wp, wm = omega_temporal_scalar(k=2.0, c_eff=1.0, omega0=0.0, gamma=0.0)
        self.assertAlmostEqual(wp.real, 2.0, places=12)
        self.assertAlmostEqual(wm.real, -2.0, places=12)

    def test_analytic_vg_massless_undamped(self):
        vg = group_velocity_analytic(k=3.0, c_eff=2.0, omega0=0.0, gamma=0.0)
        self.assertAlmostEqual(vg, 2.0, places=12)

    def test_analytic_vg_massive(self):
        vg = group_velocity_analytic(k=1.0, c_eff=1.0, omega0=1.0, gamma=0.0)
        self.assertAlmostEqual(vg, 1.0 / math.sqrt(2.0), places=12)

    def test_overdamped_is_temporal(self):
        self.assertEqual(temporal_regime(k=0.0, c_eff=1.0, omega0=0.1, gamma=2.0), "overdamped")

    def test_attenuation_finite_when_damped(self):
        ell = attenuation_length(omega=0.3, c_eff=1.0, omega0=0.0, gamma=0.4)
        self.assertGreater(ell, 0.0)

    def test_receipt_refuses_e5_and_a0(self):
        rec = receipt_scalar(1.0, 1.0, 0.0, 0.1)
        self.assertEqual(rec["scalar_gate"], "GREEN")
        self.assertFalse(rec["closes_E5"])
        self.assertFalse(rec["derived_a0"])


class A114Tests(unittest.TestCase):
    def test_gamma_zero_unit_circle(self):
        z1, z2 = a114_z_roots(k=0.01, dx=1.0, beta=0.5, gamma=0.0)
        self.assertAlmostEqual(abs(z1), 1.0, places=9)
        self.assertAlmostEqual(abs(z2), 1.0, places=9)


class MatrixTests(unittest.TestCase):
    def test_decoupled_contains_scalar_pair(self):
        self.assertTrue(decoupled_matches_scalar(k=1.5, c_eff=1.0, omega0=0.2, gamma=0.1))

    def test_coupling_splits(self):
        roots0 = matrix_lambda_roots(1.0, 1.0, 1.0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.0)
        roots1 = matrix_lambda_roots(1.0, 1.0, 1.0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.4)
        self.assertFalse(sorted(roots0.real) == sorted(roots1.real))


if __name__ == "__main__":
    unittest.main()
