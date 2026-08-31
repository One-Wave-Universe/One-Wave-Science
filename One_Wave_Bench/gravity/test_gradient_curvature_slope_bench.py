#!/usr/bin/env python3
import math
import unittest

from gradient_curvature_slope_bench import (
    assimilation_radius,
    has_massless_far_field_mode,
    potential,
    relative_curvature_correction,
    screening_length,
    slope_magnitude,
    slope_ratio_to_inverse_square,
)


class GradientCurvatureSlopeTests(unittest.TestCase):
    def test_screening_length_is_sqrt_b_over_a(self):
        self.assertAlmostEqual(screening_length(2.0, 18.0), 3.0)

    def test_point_source_potential_has_finite_core_limit(self):
        a = 2.0
        b = 8.0
        q = 3.0
        lam = screening_length(a, b)
        expected = q / (4.0 * math.pi * a * lam)
        self.assertAlmostEqual(potential(0.0, a=a, b=b, q=q), expected)

    def test_point_source_slope_has_finite_core_limit(self):
        a = 2.0
        b = 8.0
        q = 3.0
        lam = screening_length(a, b)
        expected = abs(q) / (8.0 * math.pi * a * lam * lam)
        self.assertAlmostEqual(slope_magnitude(0.0, a=a, b=b, q=q), expected)

    def test_far_field_slope_approaches_inverse_square(self):
        lam = screening_length(1.0, 1.0)
        ratio = slope_ratio_to_inverse_square(10.0 * lam)
        self.assertGreater(ratio, 0.999)
        self.assertAlmostEqual(
            1.0 - ratio,
            relative_curvature_correction(10.0 * lam),
            places=14,
        )

    def test_curvature_correction_decreases_with_radius(self):
        values = [relative_curvature_correction(x) for x in (0.5, 1, 2, 3, 5, 10)]
        self.assertTrue(all(b < a for a, b in zip(values, values[1:])))

    def test_one_percent_assimilation_boundary_is_derived(self):
        lam = screening_length(3.0, 12.0)
        radius = assimilation_radius(0.01, a=3.0, b=12.0)
        self.assertAlmostEqual(radius / lam, 6.638352067993813, places=10)
        self.assertLessEqual(relative_curvature_correction(radius, a=3.0, b=12.0), 0.01)

    def test_boundary_scales_with_lambda_not_absolute_radius(self):
        r1 = assimilation_radius(0.01, a=1.0, b=1.0)
        r2 = assimilation_radius(0.01, a=1.0, b=9.0)
        self.assertAlmostEqual(r2 / r1, 3.0, places=12)

    def test_far_field_pinning_removes_massless_mode(self):
        self.assertTrue(has_massless_far_field_mode(0.0))
        self.assertFalse(has_massless_far_field_mode(1e-12))
        self.assertFalse(has_massless_far_field_mode(1.0))


if __name__ == "__main__":
    unittest.main()
