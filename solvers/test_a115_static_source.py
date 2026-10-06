"""Analytic and conservation controls for the restricted A-115 source branch."""
import unittest
from a115_static_source import solve

class StaticSourceTests(unittest.TestCase):
    def test_analytic_profile_second_order(self):
        errors = [solve(n)["max_compression_error"] for n in (64,128,256)]
        for coarse, fine in zip(errors, errors[1:]):
            self.assertGreater(coarse/fine, 3.5)
            self.assertLess(coarse/fine, 4.5)

    def test_exterior_is_not_inverse_square(self):
        result = solve()
        self.assertLess(result["max_exterior_acceleration"], 1e-12)
        self.assertEqual(result["radial_source_flux_at_outer_boundary"], 0.)
        self.assertGreater(abs(result["center_compression"]), .05)

    def test_original_displacement_and_source_flux(self):
        result = solve()
        self.assertLess(result["max_flux_balance_residual"], 1e-12)
        self.assertLess(result["max_displacement_identity_error"], 1e-12)
        self.assertLess(result["max_acceleration_gradient_error"], 1e-12)

    def test_coefficients_have_declared_scaling(self):
        base, doubled = solve(), solve(stiffness=4., alpha=3.)
        self.assertAlmostEqual(doubled["center_compression"]/base["center_compression"], .5)
        self.assertLess(doubled["max_acceleration_gradient_error"], 1e-12)

    def test_invalid_input_rejected(self):
        for args in [dict(cells=7), dict(cells=8.5), dict(stiffness=0),
                     dict(outer_radius=1), dict(alpha=float("nan"))]:
            with self.assertRaises(ValueError):
                solve(**args)

if __name__ == "__main__":
    unittest.main()
