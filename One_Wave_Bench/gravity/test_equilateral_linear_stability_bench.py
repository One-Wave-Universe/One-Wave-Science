#!/usr/bin/env python3
import math
import unittest

from equilateral_linear_stability_bench import (
    beta_critical,
    critical_x_for_beta,
    determinant_factorization_relative_error,
    log_pair_coefficient_slope,
    mass_beta,
    spectrally_stable,
    stability_class,
)


class EquilateralLinearStabilityTests(unittest.TestCase):
    def test_positive_mass_beta_is_bounded_by_one_third(self):
        self.assertAlmostEqual(mass_beta((1.0, 1.0, 1.0)), 1.0 / 3.0, places=15)
        self.assertLess(mass_beta((100.0, 1.0, 0.5)), 1.0 / 27.0)

    def test_eta_has_short_and_long_range_limits(self):
        self.assertGreater(log_pair_coefficient_slope(1e-4), -1.001)
        self.assertAlmostEqual(log_pair_coefficient_slope(100.0), -3.0, places=14)

    def test_newtonian_gascheau_routh_limit(self):
        self.assertAlmostEqual(beta_critical(100.0), 1.0 / 27.0, places=14)

    def test_equal_mass_all_mass_boundary(self):
        xstar = critical_x_for_beta(1.0 / 3.0)
        self.assertAlmostEqual(xstar, 1.79328213290076, places=11)
        self.assertTrue(spectrally_stable((1.0, 1.0, 1.0), 1.0))
        self.assertFalse(spectrally_stable((1.0, 1.0, 1.0), 3.0))
        self.assertEqual(stability_class((1.0, 1.0, 1.0), xstar), "MARGINAL_BOUNDARY")

    def test_previous_stress_examples_are_classified(self):
        self.assertFalse(spectrally_stable((1.0, 1.7, 2.4), 5.0))
        self.assertTrue(spectrally_stable((1.0, 1.7, 2.4), 1.0))
        self.assertTrue(spectrally_stable((100.0, 1.0, 0.5), 100.0))

    def test_newtonian_stable_mass_triplet_stays_stable_for_all_finite_x(self):
        beta = mass_beta((100.0, 1.0, 0.5))
        self.assertLess(beta, 1.0 / 27.0)
        self.assertTrue(math.isinf(critical_x_for_beta(beta)))
        for x in (0.1, 1.0, 5.0, 20.0, 100.0):
            self.assertTrue(spectrally_stable((100.0, 1.0, 0.5), x))

    def test_raw_jacobian_determinant_matches_closed_factorization(self):
        for masses, x in (
            ((1.0, 2.0, 3.0), 1.0),
            ((1.0, 1.7, 2.4), 5.0),
            ((100.0, 1.0, 0.5), 10.0),
        ):
            self.assertLess(determinant_factorization_relative_error(masses, x), 2e-12)


if __name__ == "__main__":
    unittest.main()
