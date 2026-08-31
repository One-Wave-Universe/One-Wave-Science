#!/usr/bin/env python3
import math
import unittest

from source_response_coupling_bench import (
    CouplingBody,
    external_acceleration_factor,
    normalized_pair_reciprocity_residual,
    pair_net_force,
    proportional_bodies,
    reciprocity_residual,
    source_mass_residual,
    total_internal_force,
    universal_fall_residual,
)


class SourceResponseCouplingTests(unittest.TestCase):
    def setUp(self):
        self.positions = ((-1.2, 0.4), (0.7, -0.8), (2.1, 1.3))

    def test_proportional_mass_coupling_satisfies_both_requirements(self):
        bodies = proportional_bodies(
            (1.0, 2.0, 5.0),
            source_per_mass=2.0,
            response_per_mass=3.0,
            positions=self.positions,
        )
        self.assertLess(reciprocity_residual(bodies), 1e-15)
        self.assertLess(universal_fall_residual(bodies), 1e-15)
        self.assertLess(source_mass_residual(bodies), 1e-15)

    def test_proportional_mass_coupling_cancels_total_internal_force(self):
        bodies = proportional_bodies(
            (1.0, 2.0, 5.0),
            source_per_mass=2.0,
            response_per_mass=3.0,
            positions=self.positions,
        )
        fx, fy = total_internal_force(bodies, lam=0.9)
        self.assertLess(math.hypot(fx, fy), 1e-13)

    def test_reciprocity_alone_does_not_imply_universal_fall(self):
        # beta = 4 q exactly, but q is not proportional to inertial mass.
        bodies = (
            CouplingBody("A", 1.0, 1.0, 4.0, self.positions[0]),
            CouplingBody("B", 2.0, 3.0, 12.0, self.positions[1]),
            CouplingBody("C", 5.0, 10.0, 40.0, self.positions[2]),
        )
        self.assertLess(reciprocity_residual(bodies), 1e-15)
        self.assertGreater(universal_fall_residual(bodies), 0.1)
        self.assertGreater(source_mass_residual(bodies), 0.1)

    def test_universal_fall_alone_does_not_imply_reciprocity(self):
        # beta/m = 3 exactly, but q/m varies.
        bodies = (
            CouplingBody("A", 1.0, 1.0, 3.0, self.positions[0]),
            CouplingBody("B", 2.0, 7.0, 6.0, self.positions[1]),
            CouplingBody("C", 5.0, 2.0, 15.0, self.positions[2]),
        )
        self.assertLess(universal_fall_residual(bodies), 1e-15)
        self.assertGreater(reciprocity_residual(bodies), 0.1)
        fx, fy = total_internal_force(bodies, lam=1.1)
        self.assertGreater(math.hypot(fx, fy), 1e-6)

    def test_external_acceleration_factor_is_composition_independent_when_beta_tracks_mass(self):
        bodies = proportional_bodies(
            (0.2, 3.0, 100.0),
            source_per_mass=7.0,
            response_per_mass=0.125,
            positions=self.positions,
        )
        factors = [external_acceleration_factor(body) for body in bodies]
        for factor in factors:
            self.assertAlmostEqual(factor, 0.125, places=15)

    def test_pair_net_force_is_zero_exactly_when_cross_couplings_match(self):
        a = CouplingBody("A", 2.0, 6.0, 10.0, (-1.0, 0.25))
        b = CouplingBody("B", 7.0, 21.0, 35.0, (2.0, -0.5))
        self.assertAlmostEqual(normalized_pair_reciprocity_residual(a, b), 0.0)
        fx, fy = pair_net_force(a, b, lam=0.7)
        self.assertAlmostEqual(fx, 0.0, places=14)
        self.assertAlmostEqual(fy, 0.0, places=14)

    def test_nonreciprocal_pair_has_nonzero_net_internal_force(self):
        a = CouplingBody("A", 2.0, 6.0, 10.0, (-1.0, 0.25))
        b = CouplingBody("B", 7.0, 4.0, 35.0, (2.0, -0.5))
        self.assertGreater(normalized_pair_reciprocity_residual(a, b), 0.1)
        fx, fy = pair_net_force(a, b, lam=0.7)
        self.assertGreater(math.hypot(fx, fy), 1e-6)


if __name__ == "__main__":
    unittest.main()
