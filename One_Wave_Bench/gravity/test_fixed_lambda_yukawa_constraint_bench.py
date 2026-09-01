#!/usr/bin/env python3
import math
import unittest

from fixed_lambda_yukawa_constraint_bench import (
    LAMBDA_MAX_95_M,
    distance_for_deficit,
    force_deficit_fraction,
    kernel_factor,
    proof13_all_mass_scale_ceiling,
    report,
    x_for_deficit,
)


class FixedLambdaConstraintTests(unittest.TestCase):
    def test_exact_kernel_identity(self):
        for x in (0.1, 1.0, 5.0, 20.0):
            self.assertAlmostEqual(
                kernel_factor(x),
                1.0 - (1.0 + x) * math.exp(-x),
                places=15,
            )

    def test_deficit_monotone(self):
        ds = [
            force_deficit_fraction(r, LAMBDA_MAX_95_M)
            for r in (50e-6, 100e-6, 500e-6, 1e-3)
        ]
        self.assertTrue(all(a > b for a, b in zip(ds, ds[1:])))

    def test_inverse_threshold_solver(self):
        for eps in (1e-2, 1e-6, 1e-12):
            x = x_for_deficit(eps)
            self.assertAlmostEqual(
                (1.0 + x) * math.exp(-x),
                eps,
                delta=eps * 1e-12,
            )

    def test_one_percent_scale_is_submillimetre(self):
        self.assertLess(distance_for_deficit(1e-2), 0.3e-3)

    def test_one_ppm_scale_is_submillimetre(self):
        self.assertLess(distance_for_deficit(1e-6), 1.0e-3)

    def test_proof13_cross_scale(self):
        self.assertAlmostEqual(
            proof13_all_mass_scale_ceiling() * 1e6,
            69.221,
            delta=0.002,
        )

    def test_report_mapping(self):
        payload = report()
        self.assertEqual(payload["exact_mapping"]["alpha"], -1.0)
        self.assertTrue(payload["exact_mapping"]["G_inf_equals_K"])
        self.assertEqual(
            payload["published_external_bound"]["lambda_max_95_um"],
            38.6,
        )


if __name__ == "__main__":
    unittest.main()
