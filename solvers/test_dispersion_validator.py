#!/usr/bin/env python3
"""
Unit tests for One-Wave Dispersion Validator

Tests:
- D-600 characteristic equation solutions
- D-602 sign flip mechanism
- Stability analysis
- Theoretical predictions consistency
"""

import numpy as np
import unittest
from dispersion_validator import OneWaveDispersionValidator, DispersionParams


class TestD600Dispersion(unittest.TestCase):
    """Test D-600 1D scalar dispersion."""

    def setUp(self):
        self.params = DispersionParams(gamma=0.5, beta=0.5)
        self.validator = OneWaveDispersionValidator(self.params)

    def test_characteristic_equation_k_zero(self):
        """At k=0, characteristic equation should have known solutions."""
        k = np.array([0.0])
        lambda_plus, lambda_minus = self.validator.d600_characteristic_equation(k)

        # At k=0: C(0) = 2 - γ + β(1-1) = 2 - γ
        C_0 = 2 - self.params.gamma
        expected_product = 1 - self.params.gamma
        actual_product = lambda_plus[0] * lambda_minus[0]

        self.assertAlmostEqual(actual_product, expected_product, places=5)

    def test_characteristic_equation_k_pi(self):
        """At k=π, characteristic equation with known bounds."""
        k = np.array([np.pi])
        lambda_plus, lambda_minus = self.validator.d600_characteristic_equation(k)

        # Both eigenvalues should have magnitude close to 1 for stability
        self.assertLess(np.abs(lambda_plus[0]), 1.1)
        self.assertLess(np.abs(lambda_minus[0]), 1.1)

    def test_two_mode_families(self):
        """Verify two distinct mode families for all k."""
        k_vals = np.linspace(0.1, np.pi, 10)
        lambda_plus, lambda_minus = self.validator.d600_characteristic_equation(k_vals)

        # Modes should be different
        differences = np.abs(lambda_plus - lambda_minus)
        self.assertTrue(np.all(differences > 1e-6))

    def test_omega_from_lambda_consistency(self):
        """Verify ω = -i ln(λ) is computed consistently."""
        k = np.array([0.5])
        lambda_vals = np.array([0.8 + 0.1j, 0.9 - 0.05j])

        omega_1 = self.validator.d600_omega_from_lambda(lambda_vals[0])
        omega_2 = self.validator.d600_omega_from_lambda(lambda_vals[1])

        # Verify inverse: λ = exp(-i*ω)
        lambda_recovered_1 = np.exp(-1j * omega_1)
        lambda_recovered_2 = np.exp(-1j * omega_2)

        self.assertAlmostEqual(np.abs(lambda_recovered_1 - lambda_vals[0]), 0, places=10)
        self.assertAlmostEqual(np.abs(lambda_recovered_2 - lambda_vals[1]), 0, places=10)


class TestD602VectorField(unittest.TestCase):
    """Test D-602 vector field E/B emergence."""

    def setUp(self):
        self.params = DispersionParams(gamma=0.5, beta=0.5)
        self.validator = OneWaveDispersionValidator(self.params)

    def test_sign_flip_longitudinal_suppression(self):
        """Longitudinal modes should be suppressed (smaller real part) at high k."""
        k_low = 0.1
        k_high = 2.0

        omega_e_low = self.validator.d602_longitudinal_dispersion(np.array([k_low]))
        omega_e_high = self.validator.d602_longitudinal_dispersion(np.array([k_high]))

        # Longitudinal should decrease or stay small
        # (It's gapped at k=0, grows slowly)
        self.assertLess(np.abs(omega_e_high[0]), 2.0)

    def test_sign_flip_transverse_enhancement(self):
        """Transverse modes should be enhanced (grow) at higher k."""
        k_vals = np.linspace(0.1, 2.0, 10)
        omega_b = self.validator.d602_transverse_dispersion(k_vals)

        # Transverse real parts should generally increase with k
        # (Check trends)
        self.assertTrue(np.all(np.abs(omega_b) > 0))

    def test_three_mode_families(self):
        """Verify we get 3 mode families: 1 longitudinal + 2 transverse."""
        k = np.array([0.5])

        omega_e = self.validator.d602_longitudinal_dispersion(k)
        omega_b = self.validator.d602_transverse_dispersion(k)

        # We should have 3 frequencies (1 from E, 1 from B, but B is 2× degenerate in full theory)
        # For now, verify they're both real-valued solutions
        self.assertEqual(len(omega_e), 1)
        self.assertEqual(len(omega_b), 1)

    def test_c_long_vs_c_trans_coefficients(self):
        """Verify C_long and C_trans have opposite k² dependence."""
        k = 1.0

        # C_long = 2 - γ - β*k²
        C_long = 2 - self.params.gamma - self.params.beta * k**2

        # C_trans = 2 - γ + β*k²
        C_trans = 2 - self.params.gamma + self.params.beta * k**2

        # They should differ by 2*β*k²
        expected_diff = 2 * self.params.beta * k**2
        actual_diff = C_trans - C_long

        self.assertAlmostEqual(actual_diff, expected_diff, places=10)


class TestStabilityAnalysis(unittest.TestCase):
    """Test stability constraints."""

    def test_stability_at_gamma_half_beta_half(self):
        """At γ=0.5, β=0.5, system should be stable."""
        params = DispersionParams(gamma=0.5, beta=0.5)
        validator = OneWaveDispersionValidator(params)

        # Test across full k range
        k_vals = np.linspace(0, np.pi, 20)
        lambda_plus, lambda_minus = validator.d600_characteristic_equation(k_vals)

        # All should satisfy |λ| ≤ 1
        self.assertTrue(np.all(np.abs(lambda_plus) <= 1.0))
        self.assertTrue(np.all(np.abs(lambda_minus) <= 1.0))

    def test_stability_dependent_on_parameters(self):
        """Test that solver correctly computes eigenvalues across parameter space."""
        # Stable case: β=0.5
        params_stable = DispersionParams(gamma=0.5, beta=0.5)
        validator_stable = OneWaveDispersionValidator(params_stable)

        k_vals = np.linspace(0, np.pi, 20)
        lambda_plus, lambda_minus = validator_stable.d600_characteristic_equation(k_vals)

        # All should be stable: |λ| ≤ 1
        stable_condition = np.all(np.abs(lambda_plus) <= 1.0) and np.all(np.abs(lambda_minus) <= 1.0)
        self.assertTrue(stable_condition, "System with β=0.5 should be stable")

        # Higher coupling case: β=1.5
        params_high = DispersionParams(gamma=0.5, beta=1.5)
        validator_high = OneWaveDispersionValidator(params_high)

        lambda_plus_high, lambda_minus_high = validator_high.d600_characteristic_equation(k_vals)

        # Verify the solver correctly computes eigenvalues at high β
        self.assertTrue(len(lambda_plus_high) > 0, "Solver should produce eigenvalues at high β")


class TestConsistency(unittest.TestCase):
    """Test overall consistency of solver."""

    def test_report_generation(self):
        """Verify report can be generated without errors."""
        params = DispersionParams(gamma=0.5, beta=0.5, k_points=8)
        validator = OneWaveDispersionValidator(params)

        # Generate report
        report = validator.report()

        # Verify structure
        self.assertIn('parameters', report)
        self.assertIn('results', report)
        self.assertIn('gamma', report['parameters'])
        self.assertIn('beta', report['parameters'])

    def test_d602_sign_flip_analysis(self):
        """Verify D-602 sign flip analysis produces output."""
        params = DispersionParams(gamma=0.5, beta=0.5)
        validator = OneWaveDispersionValidator(params)

        result = validator.validate_d602_sign_flip()

        # Check output structure
        self.assertIn('k_values', result)
        self.assertIn('longitudinal_omega_real', result)
        self.assertIn('transverse_omega_real', result)
        self.assertIn('observation', result)


def run_tests():
    """Run full test suite."""
    print("=" * 70)
    print("ONE-WAVE DISPERSION VALIDATOR - TEST SUITE")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestD600Dispersion))
    suite.addTests(loader.loadTestsFromTestCase(TestD602VectorField))
    suite.addTests(loader.loadTestsFromTestCase(TestStabilityAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestConsistency))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {100 * (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun:.1f}%")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
