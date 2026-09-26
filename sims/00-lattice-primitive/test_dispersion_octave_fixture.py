import math
import unittest

from dispersion_octave_fixture import (
    dispersion_receipt,
    leapfrog_frequency,
    leapfrog_step,
    octave_control_receipt,
    omega_squared,
    temporal_roots,
    triangular_laplacian_symbol,
)


class TriangularDispersionTests(unittest.TestCase):
    def test_zero_wavevector_symbol_is_zero(self):
        self.assertAlmostEqual(triangular_laplacian_symbol(0.0, 0.0), 0.0, places=15)

    def test_symbol_is_non_positive(self):
        for kx, ky in ((0.2, 0.0), (0.3, 0.4), (math.pi, 0.0)):
            self.assertLessEqual(triangular_laplacian_symbol(kx, ky), 0.0)

    def test_long_wave_speed_matches_stencil(self):
        k = 1.0e-4
        omega = math.sqrt(omega_squared(k, 0.0, c_lattice=2.0, omega0=0.0))
        expected_speed = math.sqrt(1.5) * 2.0
        self.assertAlmostEqual(omega / k, expected_speed, places=7)

    def test_temporal_roots_keep_declared_damping(self):
        plus, minus = temporal_roots(0.4, 0.1, 1.0, 0.5, zeta=0.2)
        self.assertAlmostEqual(plus.imag, -0.1, places=12)
        self.assertAlmostEqual(minus.imag, -0.1, places=12)

    def test_zero_state_stays_zero(self):
        self.assertEqual(leapfrog_step(0.0, 0.0, omega_sq=3.0, dt=0.1), 0.0)

    def test_leapfrog_frequency_converges_quadratically(self):
        omega_sq = 1.7
        exact = math.sqrt(omega_sq)
        coarse = abs(leapfrog_frequency(omega_sq, 0.2) - exact)
        fine = abs(leapfrog_frequency(omega_sq, 0.1) - exact)
        self.assertLess(fine, coarse / 3.5)

    def test_receipt_refuses_physical_spacing_claim(self):
        receipt = dispersion_receipt(0.3, 0.2, 1.0, 0.25, (0.1, 0.05))
        self.assertFalse(receipt["a_num_is_physical_length"])
        self.assertFalse(receipt["derived_physical_lattice_spacing"])
        self.assertLess(
            receipt["refinements"][1]["absolute_error"],
            receipt["refinements"][0]["absolute_error"],
        )


class OctaveControlTests(unittest.TestCase):
    def test_exact_octave_fixture_passes(self):
        receipt = octave_control_receipt((10.0, 20.0, 40.0), epsilon_octave=1.0e-12)
        self.assertTrue(receipt.all_pairs_compatible)
        self.assertEqual(receipt.compatible_pairs, 3)

    def test_non_octave_fixture_fails(self):
        receipt = octave_control_receipt((10.0, 15.0, 23.0), epsilon_octave=0.05)
        self.assertFalse(receipt.all_pairs_compatible)
        self.assertEqual(receipt.compatible_pairs, 0)

    def test_invalid_frequency_is_rejected(self):
        with self.assertRaises(ValueError):
            octave_control_receipt((0.0, 10.0))


if __name__ == "__main__":
    unittest.main()
