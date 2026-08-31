#!/usr/bin/env python3
import math
import unittest

from gradient_curvature_three_body_bench import (
    accelerations,
    center_of_mass,
    closure_residual,
    equilateral_state,
    integrate_verlet,
    kernel_factor,
    pair_potential_shape,
    side_lengths,
    total_momentum,
)


class GradientCurvatureThreeBodyTests(unittest.TestCase):
    def test_kernel_recovers_newtonian_fraction_at_large_separation(self):
        self.assertGreater(kernel_factor(10.0), 0.999)
        self.assertLess(kernel_factor(0.1), 0.01)

    def test_pair_potential_is_finite_at_zero(self):
        self.assertAlmostEqual(pair_potential_shape(0.0, 2.5), 0.4)

    def test_unequal_mass_equilateral_configuration_closes_exactly(self):
        state = equilateral_state(masses=(1.0, 2.0, 3.0), side=4.0, lam=0.8, coupling=2.3)
        residual = closure_residual(state)
        self.assertLess(residual["max_vector_residual"], 1e-13)

    def test_center_of_mass_frame_is_zero(self):
        state = equilateral_state(masses=(1.0, 4.0, 9.0), side=7.0, lam=1.3)
        cx, cy = center_of_mass(state.masses, state.positions)
        self.assertAlmostEqual(cx, 0.0, places=14)
        self.assertAlmostEqual(cy, 0.0, places=14)

    def test_rigid_rotation_initial_momentum_is_zero(self):
        state = equilateral_state(masses=(1.0, 2.0, 5.0), side=5.0, lam=1.0)
        px, py = total_momentum(state.masses, state.velocities)
        self.assertAlmostEqual(px, 0.0, places=14)
        self.assertAlmostEqual(py, 0.0, places=14)

    def test_pair_distances_are_exactly_equal(self):
        state = equilateral_state(masses=(1.0, 3.0, 7.0), side=6.0, lam=1.0)
        lengths = side_lengths(state.positions)
        for length in lengths:
            self.assertAlmostEqual(length, state.side, places=14)

    def test_numerical_orbit_preserves_equilateral_shape_and_invariants(self):
        state = equilateral_state(masses=(1.0, 2.0, 3.0), side=4.0, lam=0.8)
        receipt = integrate_verlet(state, periods=1.0, steps_per_period=2000)
        self.assertLess(receipt["max_side_spread_fraction"], 1e-9)
        self.assertLess(receipt["relative_energy_drift"], 1e-9)
        self.assertLess(receipt["relative_angular_momentum_drift"], 1e-11)
        self.assertLess(math.hypot(*receipt["final_com"]), 1e-10)
        self.assertLess(math.hypot(*receipt["final_total_momentum"]), 1e-10)

    def test_analytic_acceleration_points_to_center_of_mass(self):
        state = equilateral_state(masses=(2.0, 5.0, 11.0), side=3.5, lam=0.7)
        acc = accelerations(state.masses, state.positions, state.lam, state.coupling)
        omega2 = state.omega**2
        for (x, y), (ax, ay) in zip(state.positions, acc):
            self.assertAlmostEqual(ax, -omega2 * x, places=13)
            self.assertAlmostEqual(ay, -omega2 * y, places=13)


if __name__ == "__main__":
    unittest.main()
