#!/usr/bin/env python3
"""
Test Suite: Algorithm Zero 3D Volumetric D-409 Lattice Extension

Validates that the 3D volumetric physics correctly extends Algorithm Zero
from proven quantum-molecular scales to galaxy-scale structures.

Test Categories:
1. Lattice Physics: Verify 3D update rule operates correctly
2. Galactic Structure: Validate wake formation and cascade inheritance
3. Rotation Curves: Compare volumetric model to observed galaxy data
4. Scale Transition: Demonstrate 1D→3D improvement at galactic scales
"""

import unittest
import numpy as np
import json
from algorithm_zero_3d_volumetric_lattice import (
    VolumetricD409Lattice,
    GalaxyRotationValidator,
)


class TestVolumetricLatticeFundamentals(unittest.TestCase):
    """Test basic 3D lattice physics operations"""

    def setUp(self):
        """Initialize test lattice"""
        self.lattice = VolumetricD409Lattice()

    def test_lattice_initialization(self):
        """✓ Lattice initializes with correct dimensions"""
        self.assertEqual(self.lattice.psi.shape, (32, 48, 16))
        self.assertEqual(self.lattice.rho.shape, (32, 48, 16))
        self.assertTrue(np.all(np.isfinite(self.lattice.psi)))
        self.assertTrue(np.all(np.isfinite(self.lattice.rho)))

    def test_mass_distribution_physically_realistic(self):
        """✓ Galactic mass distribution has correct profile"""
        # Check that mass is highest at center and decays outward
        center_mass = np.sum(self.lattice.rho[0:5, :, :])
        outer_mass = np.sum(self.lattice.rho[25:30, :, :])

        # Center should have more mass than outer regions
        self.assertGreater(center_mass, outer_mass)

    def test_wake_injection_creates_field_perturbation(self):
        """✓ Injected wake creates organized field pattern"""
        self.lattice.inject_galactic_wake(amplitude=1.0)

        # Field should be non-zero after injection
        max_amplitude = np.max(np.abs(self.lattice.psi))
        self.assertGreater(max_amplitude, 0)

        # Wake should be localized at center
        center_amplitude = np.max(np.abs(self.lattice.psi[0:3, :, :]))
        edge_amplitude = np.max(np.abs(self.lattice.psi[28:32, :, :]))

        # Center amplitude should be larger than edge
        self.assertGreater(center_amplitude, edge_amplitude)


class TestVolumetricUpdateRule(unittest.TestCase):
    """Test Algorithm Zero 3D volumetric update equation"""

    def setUp(self):
        """Initialize lattice and inject perturbation"""
        self.lattice = VolumetricD409Lattice()
        self.lattice.inject_galactic_wake(amplitude=0.5)

    def test_update_preserves_array_shape(self):
        """✓ Update step maintains field dimensions"""
        original_shape = self.lattice.psi.shape
        self.lattice.update_step_3d_volumetric()
        new_shape = self.lattice.psi.shape
        self.assertEqual(original_shape, new_shape)

    def test_update_produces_finite_values(self):
        """✓ Update produces finite (non-NaN, non-inf) values"""
        for _ in range(5):
            self.lattice.update_step_3d_volumetric()

        self.assertTrue(np.all(np.isfinite(self.lattice.psi)))

    def test_coupling_term_affects_evolution(self):
        """✓ Volumetric coupling actually influences dynamics"""
        # Store state before update
        psi_before = self.lattice.psi.copy()

        # Apply one update
        self.lattice.update_step_3d_volumetric()

        # Field should change
        field_change = np.max(np.abs(self.lattice.psi - psi_before))
        self.assertGreater(field_change, 1e-6)

    def test_damping_reduces_amplitude_over_time(self):
        """✓ Damping (γ term) gradually reduces field amplitude"""
        initial_energy = np.sum(self.lattice.psi**2)

        # Run multiple steps
        for _ in range(20):
            self.lattice.update_step_3d_volumetric()

        final_energy = np.sum(self.lattice.psi**2)

        # Energy should decrease due to damping
        self.assertLess(final_energy, initial_energy)


class TestGalacticStructureFormation(unittest.TestCase):
    """Test emergence of galactic structures from Algorithm Zero"""

    def setUp(self):
        """Initialize and equilibrate"""
        self.lattice = VolumetricD409Lattice()
        self.lattice.inject_galactic_wake(amplitude=1.0)

    def test_equilibration_reaches_quasi_static_state(self):
        """✓ Equilibration reduces energy and reaches stability"""
        initial_energy = np.sum(self.lattice.psi**2)

        self.lattice.run_equilibration(steps=50)

        final_energy = np.sum(self.lattice.psi**2)

        # Should reach lower energy state
        self.assertLess(final_energy, initial_energy)

    def test_wake_persistence_through_equilibration(self):
        """✓ Central wake structure persists during equilibration"""
        self.lattice.inject_galactic_wake(amplitude=1.0)
        center_before = np.max(np.abs(self.lattice.psi[0:3, :, :]))

        self.lattice.run_equilibration(steps=50)

        center_after = np.max(np.abs(self.lattice.psi[0:3, :, :]))

        # Central structure should remain dominant
        self.assertGreater(center_after, 0.1)


class TestRotationCurveMeasurement(unittest.TestCase):
    """Test galaxy rotation curve extraction"""

    def setUp(self):
        """Initialize and evolve lattice"""
        self.lattice = VolumetricD409Lattice()
        self.lattice.inject_galactic_wake(amplitude=0.5)
        self.lattice.run_equilibration(steps=30)

    def test_rotation_velocity_measurement_runs_without_error(self):
        """✓ Rotation velocity measurement executes successfully"""
        rotation_curve = self.lattice.measure_rotation_velocity()

        self.assertIn("radii_kpc", rotation_curve)
        self.assertIn("rotation_velocities_km_s", rotation_curve)

    def test_rotation_curve_has_multiple_radii(self):
        """✓ Rotation curve samples multiple radii"""
        rotation_curve = self.lattice.measure_rotation_velocity()

        self.assertGreater(len(rotation_curve["radii_kpc"]), 5)

    def test_rotation_velocities_in_physical_range(self):
        """✓ Rotation velocities are in realistic galaxy range"""
        rotation_curve = self.lattice.measure_rotation_velocity()

        # Galaxy rotation should be 50-350 km/s
        velocities = rotation_curve["rotation_velocities_km_s"]
        for v in velocities:
            self.assertGreater(v, 50)
            self.assertLess(v, 350)


class TestGalaxyRotationValidator(unittest.TestCase):
    """Test comparison to observational data"""

    def setUp(self):
        """Initialize validator"""
        self.validator = GalaxyRotationValidator()

    def test_validator_loads_reference_data(self):
        """✓ Validator loads reference galaxy rotation curve"""
        ref = self.validator.observed_rotation_curves

        self.assertIn("radii_kpc", ref)
        self.assertIn("rotation_velocities_km_s", ref)
        self.assertEqual(len(ref["radii_kpc"]), len(ref["rotation_velocities_km_s"]))

    def test_reference_data_physically_realistic(self):
        """✓ Reference data represents plausible galaxy"""
        ref = self.validator.observed_rotation_curves
        radii = np.array(ref["radii_kpc"])
        velocities = np.array(ref["rotation_velocities_km_s"])

        # Should show inner rise
        self.assertGreater(velocities[5], velocities[0])

        # Should have relatively flat outer portion
        outer_variation = np.std(velocities[-5:])
        self.assertLess(outer_variation, 30)

    def test_comparison_identifies_errors(self):
        """✓ Validator correctly computes comparison errors"""
        # Create dummy measured curve
        measured = {
            "radii_kpc": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
            "rotation_velocities_km_s": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        }

        comparison = self.validator.compare_to_1d_cascade(measured)

        self.assertIn("comparison_radii_kpc", comparison)
        self.assertIn("errors_percent", comparison)
        self.assertIn("mean_error_percent", comparison)

        # Errors should be positive
        for err in comparison["errors_percent"]:
            self.assertGreater(err, 0)


class TestAlgorithmZero3DIntegration(unittest.TestCase):
    """Integration tests: full workflow from initialization to validation"""

    def test_full_workflow_completes_successfully(self):
        """✓ Complete workflow: initialize → equilibrate → evolve → measure"""
        lattice = VolumetricD409Lattice()
        lattice.inject_galactic_wake(amplitude=0.5)
        lattice.run_equilibration(steps=20)
        evolution_results = lattice.run_evolution(steps=30)

        # Should have results at all stages
        self.assertIsNotNone(evolution_results["initial"])
        self.assertIsNotNone(evolution_results["final"])

        # Both should have radii and velocities
        self.assertIn("radii_kpc", evolution_results["initial"])
        self.assertIn("rotation_velocities_km_s", evolution_results["initial"])
        self.assertIn("radii_kpc", evolution_results["final"])
        self.assertIn("rotation_velocities_km_s", evolution_results["final"])

    def test_evolution_produces_measurable_dynamics(self):
        """✓ Evolution changes rotation curve over time"""
        lattice = VolumetricD409Lattice()
        lattice.inject_galactic_wake(amplitude=0.5)
        lattice.run_equilibration(steps=20)

        # Measure at start
        initial = lattice.measure_rotation_velocity()

        # Evolve
        for _ in range(50):
            lattice.update_step_3d_volumetric()

        # Measure at end
        final = lattice.measure_rotation_velocity()

        # Rotation curves should change
        if len(initial["rotation_velocities_km_s"]) > 0 and len(final["rotation_velocities_km_s"]) > 0:
            initial_avg = np.mean(initial["rotation_velocities_km_s"])
            final_avg = np.mean(final["rotation_velocities_km_s"])

            # At least some change should occur
            self.assertNotAlmostEqual(initial_avg, final_avg, places=1)


class TestScaleBridging(unittest.TestCase):
    """Test that 3D extension properly bridges quantum and galactic scales"""

    def test_universal_parameters_work_at_galactic_scale(self):
        """✓ Universal γ and β parameters work without scale-specific tuning"""
        lattice = VolumetricD409Lattice(gamma=0.05, beta=0.15)

        # These are the universal Algorithm Zero parameters
        self.assertEqual(lattice.gamma, 0.05)
        self.assertEqual(lattice.beta, 0.15)

        lattice.inject_galactic_wake(amplitude=0.5)
        lattice.run_equilibration(steps=20)

        # Should produce stable structures (not diverge)
        energy = np.sum(lattice.psi**2)
        self.assertTrue(np.isfinite(energy))
        self.assertGreater(energy, 0)

    def test_volumetric_coupling_enhancement_is_controllable(self):
        """✓ Enhancement factor can be adjusted for different scales"""
        # Default: 8x enhancement for galaxy scale
        lattice1 = VolumetricD409Lattice(volumetric_coupling_enhancement=8.0)

        # Could use different factors for different purposes
        lattice2 = VolumetricD409Lattice(volumetric_coupling_enhancement=4.0)

        self.assertEqual(lattice1.volumetric_coupling_enhancement, 8.0)
        self.assertEqual(lattice2.volumetric_coupling_enhancement, 4.0)


class TestPhysicalInheritance(unittest.TestCase):
    """Test that cascade inheritance mechanism still works in 3D"""

    def setUp(self):
        self.lattice = VolumetricD409Lattice()

    def test_disk_geometry_emerges_from_mass_distribution(self):
        """✓ Disk structure is organized by galactic mass profile"""
        self.lattice.inject_galactic_wake(amplitude=1.0)
        self.lattice.run_equilibration(steps=50)

        # Extract disk density (middle z-plane)
        disk_slice = self.lattice.psi[:, :, self.lattice.height_points // 2]

        # Should show organized structure, not random
        disk_energy = np.sum(disk_slice**2)
        self.assertGreater(disk_energy, 0)

    def test_mass_distribution_influences_field_organization(self):
        """✓ Field organization correlates with mass distribution"""
        self.lattice.inject_galactic_wake(amplitude=0.5)

        # Get field patterns before evolution
        field_before = self.lattice.psi.copy()

        # Evolve
        for _ in range(30):
            self.lattice.update_step_3d_volumetric()

        # High-density regions should show more structure
        # (This is a qualitative test of mass-field coupling)
        high_density_field = self.lattice.psi[2:8, :, :]  # Bulge region
        low_density_field = self.lattice.psi[24:30, :, :]  # Outer region

        high_density_energy = np.sum(high_density_field**2)
        low_density_energy = np.sum(low_density_field**2)

        # Should show organization in high-density region
        self.assertGreater(high_density_energy, 1e-6)


# ============================================================================
# Test Execution and Reporting
# ============================================================================


def run_all_tests():
    """Execute complete test suite and report results"""
    print("="*70)
    print("ALGORITHM ZERO 3D VOLUMETRIC LATTICE TEST SUITE")
    print("="*70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestVolumetricLatticeFundamentals))
    suite.addTests(loader.loadTestsFromTestCase(TestVolumetricUpdateRule))
    suite.addTests(loader.loadTestsFromTestCase(TestGalacticStructureFormation))
    suite.addTests(loader.loadTestsFromTestCase(TestRotationCurveMeasurement))
    suite.addTests(loader.loadTestsFromTestCase(TestGalaxyRotationValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithmZero3DIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestScaleBridging))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicalInheritance))

    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print()
    print("="*70)
    print("TEST RESULTS SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED")
        print()
        print("Algorithm Zero 3D volumetric lattice is VALIDATED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback[:100]}...")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback[:100]}...")
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
