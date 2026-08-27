import unittest

import numpy as np

from asymmetric_oscillator import (
    OscillatorParameters, barrier_heights, equilibria, linear_response,
    simulate, sweep_bias,
)


class AsymmetricOscillatorTests(unittest.TestCase):
    def test_exact_fold_threshold(self):
        p = OscillatorParameters()
        self.assertAlmostEqual(p.fold_bias, 2.0/(3.0*np.sqrt(3.0)))

    def test_three_equilibria_below_fold(self):
        states = equilibria(OscillatorParameters(bias=0.2))
        self.assertEqual(len(states), 3)
        self.assertEqual(sum(state.stable for state in states), 2)

    def test_one_stable_equilibrium_above_fold(self):
        states = equilibria(OscillatorParameters(bias=0.5))
        self.assertEqual(len(states), 1)
        self.assertTrue(states[0].stable)

    def test_bias_mirror_symmetry(self):
        positive = equilibria(OscillatorParameters(bias=0.2))
        negative = equilibria(OscillatorParameters(bias=-0.2))
        self.assertTrue(np.allclose([s.x for s in positive], [-s.x for s in negative[::-1]]))

    def test_undamped_energy_is_conserved(self):
        trajectory = simulate(OscillatorParameters(zeta=0.0), 0.2, 0.3, 20.0, 0.002)
        self.assertLess(np.max(np.abs(trajectory.energy-trajectory.energy[0])), 1e-10)

    def test_damped_energy_is_nonincreasing_without_drive(self):
        trajectory = simulate(OscillatorParameters(zeta=0.2), 0.2, 0.3, 20.0, 0.002)
        self.assertLessEqual(np.max(np.diff(trajectory.energy)), 1e-10)

    def test_energy_work_balance(self):
        drive = lambda t: 0.1*np.sin(0.7*t)
        trajectory = simulate(OscillatorParameters(zeta=0.1), 0.2, 0.0, 20.0, 0.002, drive)
        self.assertLess(np.max(np.abs(trajectory.balance_residual)), 1e-7)

    def test_stable_well_recovers_after_small_perturbation(self):
        p = OscillatorParameters(zeta=0.2, bias=0.1)
        target = max(state.x for state in equilibria(p) if state.stable)
        trajectory = simulate(p, target+0.1, 0.0, 40.0, 0.005)
        self.assertLess(abs(trajectory.x[-1]-target), 1e-3)
        self.assertLess(abs(trajectory.v[-1]), 1e-3)

    def test_sweep_changes_root_count_at_fold(self):
        rows = sweep_bias((0.0, 0.3, 0.5))
        self.assertEqual([row.equilibrium_count for row in rows], [3, 3, 1])

    def test_center_metrics_are_distinct(self):
        trajectory = simulate(OscillatorParameters(zeta=0.0), 0.0, 0.5, 10.0, 0.002)
        self.assertGreater(trajectory.center_crossings(), 0)
        self.assertGreater(trajectory.center_dwell_fraction(0.05), 0.0)
        self.assertLess(trajectory.center_dwell_fraction(0.05), 1.0)

    def test_symmetric_barrier_is_one_quarter(self):
        barriers = barrier_heights(OscillatorParameters())
        self.assertEqual(len(barriers), 2)
        self.assertTrue(all(abs(item.barrier_energy-0.25) < 1e-12 for item in barriers))

    def test_barrier_disappears_above_fold(self):
        self.assertEqual(barrier_heights(OscillatorParameters(bias=0.5)), ())

    def test_small_signal_phase_response(self):
        response = linear_response(OscillatorParameters(zeta=0.1), 1.0, 0.0)
        self.assertAlmostEqual(response.amplitude_per_unit_drive, 0.5)
        self.assertAlmostEqual(response.phase_lag, 0.0)

    def test_unstable_point_rejected_by_response(self):
        with self.assertRaises(ValueError):
            linear_response(OscillatorParameters(), 0.0, 1.0)


if __name__ == "__main__":
    unittest.main()
