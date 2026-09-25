import unittest

import numpy as np

from center_geometry import classify_center_geometry


class CenterGeometryTests(unittest.TestCase):
    def classify(self, t, x, v, **kwargs):
        return classify_center_geometry(
            t, x, v,
            point_x_tol=1e-3,
            point_v_tol=1e-3,
            band_half_width=0.2,
            **kwargs,
        )

    def test_fast_crossing_is_not_point_residence(self):
        t = np.linspace(-0.5, 0.5, 102)
        x = t
        v = np.ones_like(t)
        r = self.classify(t, x, v)
        self.assertTrue(r.has_crossing_section)
        self.assertFalse(r.has_point_residence)

    def test_equilibrium_is_point_residence_without_crossing(self):
        t = np.linspace(0.0, 1.0, 20)
        r = self.classify(t, np.zeros_like(t), np.zeros_like(t))
        self.assertTrue(r.has_point_residence)
        self.assertFalse(r.has_crossing_section)

    def test_periodic_orbit_has_recurrent_section(self):
        t = np.linspace(0.01, 8.01 * np.pi, 8001)
        x, v = np.sin(t), np.cos(t)
        r = self.classify(t, x, v)
        self.assertTrue(r.has_crossing_section)
        self.assertTrue(r.has_limit_cycle_section)
        self.assertIn(r.recurrent_direction, (-1, 1))
        self.assertLess(r.return_time_cv, 1e-3)
        self.assertLess(r.crossing_speed_cv, 1e-3)

    def test_finite_band_and_slow_motion_are_separate_receipts(self):
        t = np.arange(8.0)
        x = np.array([-1.0, -0.5, -0.15, -0.05, 0.05, 0.15, 0.5, 1.0])
        v = np.array([2.0, 2.0, 0.2, 0.2, 0.2, 0.2, 2.0, 2.0])
        r = self.classify(t, x, v, slow_ratio_min=3.0)
        self.assertTrue(r.has_finite_band)
        self.assertTrue(r.has_slow_manifold_candidate)
        self.assertGreaterEqual(r.slow_speed_ratio, 3.0)

    def test_irregular_crossing_is_not_promoted_to_limit_cycle(self):
        t = np.arange(9.0)
        x = np.array([-1, 1, -1, 1, 1, -1, -1, -1, 1], dtype=float)
        v = np.gradient(x, t)
        r = self.classify(t, x, v, recurrence_cv_tol=0.01, speed_cv_tol=0.01)
        self.assertTrue(r.has_crossing_section)
        self.assertFalse(r.has_limit_cycle_section)

    def test_invalid_threshold_order_is_rejected(self):
        t = np.arange(3.0)
        with self.assertRaises(ValueError):
            classify_center_geometry(
                t, t, np.ones_like(t),
                point_x_tol=1.0,
                point_v_tol=0.0,
                band_half_width=0.5,
            )


if __name__ == "__main__":
    unittest.main()
