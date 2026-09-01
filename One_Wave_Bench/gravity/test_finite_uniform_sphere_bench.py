import unittest

import finite_uniform_sphere_bench as bench


class FiniteUniformSphereBenchTests(unittest.TestCase):
    def test_center_is_smooth(self):
        result = bench.run(radius=1.5, lam=1.0)
        self.assertTrue(result["pass"]["finite_center_potential"])
        self.assertTrue(result["pass"]["zero_center_slope"])
        self.assertTrue(result["pass"]["center_linear_term"])

    def test_boundary_is_C1(self):
        result = bench.run(radius=1.5, lam=1.0)
        self.assertLess(result["boundary_potential_relative_mismatch"], 1e-6)
        self.assertLess(result["boundary_slope_relative_mismatch"], 1e-6)

    def test_point_source_limit(self):
        result = bench.run(radius=1.5, lam=1.0)
        self.assertTrue(result["pass"]["point_source_limit"])

    def test_far_field_limit(self):
        result = bench.run(radius=1.5, lam=1.0)
        self.assertTrue(result["pass"]["inverse_square_far_field"])

    def test_form_factor_small_source_limit(self):
        self.assertAlmostEqual(bench.yukawa_form_factor(1e-5), 1.0, places=9)

    def test_exterior_formula_matches_convolution_expression(self):
        result = bench.run(radius=0.7, lam=1.3)
        self.assertLess(result["exterior_formula_relative_mismatch"], 1e-12)


if __name__ == "__main__":
    unittest.main()
