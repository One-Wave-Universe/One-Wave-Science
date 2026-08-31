#!/usr/bin/env python3
import unittest

from finite_slope_sieve_bench import (
    AU_M,
    EARTH_SUN_M,
    JUPITER_SUN_M,
    MASS_EARTH_KG,
    MASS_JUPITER_KG,
    MASS_SUN_KG,
    MOON_EARTH_M,
    Body,
    absolute_background_crossing_radius,
    differential_balance_residual,
    differential_dominance_radius,
    monopole_compression_error,
    opening_ratio,
)


class FiniteSlopeBoundaryTests(unittest.TestCase):
    def test_differential_radius_solves_balance_equation(self):
        radius = differential_dominance_radius(
            EARTH_SUN_M,
            MASS_EARTH_KG,
            MASS_SUN_KG,
            kappa=3.0,
        )
        residual = differential_balance_residual(
            radius,
            EARTH_SUN_M,
            MASS_EARTH_KG,
            MASS_SUN_KG,
            kappa=3.0,
        )
        local_scale = 6.67430e-11 * MASS_EARTH_KG / radius**2
        self.assertLess(abs(residual) / local_scale, 1e-12)

    def test_absolute_parent_slope_crossing_fails_moon_control(self):
        radius = absolute_background_crossing_radius(
            EARTH_SUN_M,
            MASS_EARTH_KG,
            MASS_SUN_KG,
        )
        self.assertLess(radius, MOON_EARTH_M)

    def test_differential_boundary_contains_moon_control(self):
        radius = differential_dominance_radius(
            EARTH_SUN_M,
            MASS_EARTH_KG,
            MASS_SUN_KG,
            kappa=3.0,
        )
        self.assertGreater(radius, MOON_EARTH_M)

    def test_hill_like_boundary_is_not_a_hard_influence_cutoff(self):
        jupiter_boundary = differential_dominance_radius(
            JUPITER_SUN_M,
            MASS_JUPITER_KG,
            MASS_SUN_KG,
            kappa=3.0,
        )
        nominal_earth_jupiter_separation = JUPITER_SUN_M - AU_M
        self.assertLess(jupiter_boundary, nominal_earth_jupiter_separation)


class SieveCompressionTests(unittest.TestCase):
    def setUp(self):
        self.sources = [
            Body("left", 1.0, (-1.0, 0.0, 0.0)),
            Body("right", 1.0, (1.0, 0.0, 0.0)),
        ]

    def test_monopole_error_decreases_with_distance(self):
        near = monopole_compression_error(
            (0.0, 10.0, 0.0),
            self.sources,
            gravitational_constant=1.0,
        )
        far = monopole_compression_error(
            (0.0, 20.0, 0.0),
            self.sources,
            gravitational_constant=1.0,
        )
        self.assertLess(far, near)

    def test_center_of_mass_monopole_has_quadratic_far_field_error(self):
        theta_10 = opening_ratio((0.0, 10.0, 0.0), self.sources)
        theta_20 = opening_ratio((0.0, 20.0, 0.0), self.sources)
        err_10 = monopole_compression_error(
            (0.0, 10.0, 0.0),
            self.sources,
            gravitational_constant=1.0,
        )
        err_20 = monopole_compression_error(
            (0.0, 20.0, 0.0),
            self.sources,
            gravitational_constant=1.0,
        )

        normalized_10 = err_10 / theta_10**2
        normalized_20 = err_20 / theta_20**2

        self.assertAlmostEqual(normalized_10, normalized_20, delta=0.02)
        self.assertAlmostEqual(err_10 / err_20, 4.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
