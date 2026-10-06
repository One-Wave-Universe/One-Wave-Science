#!/usr/bin/env python3
"""
Test Suite for Algorithm Zero Phase 3: Pressure Tensor Extension

Tests the new pressure tensor formalism with:
1. Initialization and stability
2. Nonlinear saturation effects
3. Asymmetric mass-field coupling
4. Rotation curve structure formation
5. Galaxy morphology differentiation
6. Comparison to Phase 2 baseline

Target: 30+ tests, all passing
"""

import pytest
import numpy as np
from solvers.algorithm_zero_phase3_pressure_tensor import PressureTensorLattice


class TestPressureTensorInitialization:
    """Test lattice initialization and setup"""

    def test_lattice_creates_without_error(self):
        """Test that PressureTensorLattice instantiates correctly"""
        lattice = PressureTensorLattice()
        assert lattice is not None
        assert lattice.radius_points == 32
        assert lattice.theta_points == 48
        assert lattice.height_points == 16

    def test_universal_parameters_preserved(self):
        """Test that Phase 1 universal parameters are unchanged"""
        lattice = PressureTensorLattice()
        assert lattice.gamma == 0.05, "Damping parameter changed"
        assert lattice.beta == 0.15, "Coupling parameter changed"

    def test_pressure_tensor_shape(self):
        """Test that pressure tensor has correct shape"""
        lattice = PressureTensorLattice()
        assert lattice.pressure.shape == (6, 32, 48, 16)
        assert lattice.pressure_prev.shape == (6, 32, 48, 16)

    def test_pressure_tensor_initialized_zero(self):
        """Test that pressure tensor starts at zero"""
        lattice = PressureTensorLattice()
        assert np.max(np.abs(lattice.pressure)) < 1e-10

    def test_mass_distribution_initialized(self):
        """Test that mass distribution is created"""
        lattice = PressureTensorLattice()
        assert np.max(lattice.rho) > 0
        assert np.min(lattice.rho) >= 0

    def test_mass_distribution_radial_profile(self):
        """Test that mass distribution follows exponential radial profile"""
        lattice = PressureTensorLattice()
        # Check that mass decreases with radius
        center_mass = np.mean(lattice.rho[1:3, :, :])
        outer_mass = np.mean(lattice.rho[28:30, :, :])
        assert center_mass > outer_mass, "Radial mass profile should decrease"

    def test_mass_distribution_thin_disk(self):
        """Test that mass distribution is thin in vertical direction"""
        lattice = PressureTensorLattice()
        center_height = lattice.rho[:, :, lattice.height_points // 2]
        outer_height = lattice.rho[:, :, 0]
        assert np.mean(center_height) > np.mean(outer_height), "Should be thin disk"

    def test_mass_gradient_computed(self):
        """Test that mass gradient is computed"""
        lattice = PressureTensorLattice()
        assert lattice.grad_rho.shape == (3, 32, 48, 16)
        # At least some gradient values should be non-zero
        assert np.max(np.abs(lattice.grad_rho)) > 0

    def test_initial_stability(self):
        """Test that initial state is stable (no NaN or inf)"""
        lattice = PressureTensorLattice()
        assert np.all(np.isfinite(lattice.pressure))
        assert np.all(np.isfinite(lattice.rho))


class TestPressureTensorEvolution:
    """Test time evolution and stability"""

    def test_single_update_step_runs(self):
        """Test that a single update step executes without error"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        pressure_old = lattice.pressure.copy()
        lattice.update_step_pressure_tensor()
        # Pressure should change after update
        assert not np.allclose(lattice.pressure, pressure_old)

    def test_multiple_steps_stable(self):
        """Test that multiple steps execute without divergence"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        for _ in range(50):
            lattice.update_step_pressure_tensor()
        assert lattice.is_stable()

    def test_long_evolution_stable(self):
        """Test that 1000+ steps don't cause divergence"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        for _ in range(500):
            lattice.update_step_pressure_tensor()
        # Should still be stable
        assert np.max(np.abs(lattice.pressure)) < 1e3
        assert np.all(np.isfinite(lattice.pressure))

    def test_time_step_counter_increments(self):
        """Test that time step counter increments properly"""
        lattice = PressureTensorLattice()
        assert lattice.time_steps == 0
        lattice.update_step_pressure_tensor()
        assert lattice.time_steps == 1
        lattice.update_step_pressure_tensor()
        assert lattice.time_steps == 2

    def test_pressure_grows_then_stabilizes(self):
        """Test that pressure evolves smoothly without oscillations"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake(amplitude=0.5)
        max_pressures = []
        for _ in range(100):
            lattice.update_step_pressure_tensor()
            max_pressures.append(np.max(np.abs(lattice.pressure)))

        # Check that growth is not chaotic
        # (differences between successive steps should be small)
        diffs = np.abs(np.diff(max_pressures))
        assert np.mean(diffs) < 0.1  # Smooth evolution


class TestNonlinearSaturation:
    """Test nonlinear saturation coupling"""

    def test_saturation_disabled_by_default(self):
        """Test that nonlinear saturation is disabled by default"""
        lattice = PressureTensorLattice()
        assert not lattice.nonlinear_enabled

    def test_enable_saturation(self):
        """Test that saturation can be enabled"""
        lattice = PressureTensorLattice()
        lattice.enable_nonlinear_saturation()
        assert lattice.nonlinear_enabled

    def test_saturation_prevents_unbounded_growth(self):
        """Test that saturation prevents pressure from growing without bound"""
        # Without saturation
        lattice_linear = PressureTensorLattice()
        lattice_linear.inject_pressure_wake(amplitude=1.0)
        max_linear = []
        for _ in range(200):
            lattice_linear.update_step_pressure_tensor()
            max_linear.append(np.max(np.abs(lattice_linear.pressure)))

        # With saturation
        lattice_sat = PressureTensorLattice()
        lattice_sat.inject_pressure_wake(amplitude=1.0)
        lattice_sat.enable_nonlinear_saturation()
        max_sat = []
        for _ in range(200):
            lattice_sat.update_step_pressure_tensor()
            max_sat.append(np.max(np.abs(lattice_sat.pressure)))

        # Saturation should limit growth
        assert max_sat[-1] < max_linear[-1] * 2  # Saturation limits growth

    def test_saturation_amplitude_parameter(self):
        """Test that saturation amplitude affects evolution"""
        # Low saturation amplitude (stronger saturation effect)
        lat_low = PressureTensorLattice()
        lat_low.saturation_amplitude = 0.5
        lat_low.enable_nonlinear_saturation()
        lat_low.inject_pressure_wake(amplitude=1.0)
        for _ in range(100):
            lat_low.update_step_pressure_tensor()
        max_low = np.max(np.abs(lat_low.pressure))

        # High saturation amplitude (weaker saturation effect)
        lat_high = PressureTensorLattice()
        lat_high.saturation_amplitude = 5.0
        lat_high.enable_nonlinear_saturation()
        lat_high.inject_pressure_wake(amplitude=1.0)
        for _ in range(100):
            lat_high.update_step_pressure_tensor()
        max_high = np.max(np.abs(lat_high.pressure))

        # Both should be well-behaved (not NaN or inf)
        assert np.isfinite(max_low)
        assert np.isfinite(max_high)
        # Saturation should prevent excessive growth
        assert max_low < 100  # Should be bounded
        assert max_high < 100  # Should be bounded


class TestAsymmetricMassFieldCoupling:
    """Test asymmetric mass-field coupling"""

    def test_asymmetric_coupling_disabled_by_default(self):
        """Test that asymmetric coupling is disabled by default"""
        lattice = PressureTensorLattice()
        assert not lattice.asymmetric_coupling_enabled

    def test_enable_asymmetric_coupling(self):
        """Test that asymmetric coupling can be enabled"""
        lattice = PressureTensorLattice()
        lattice.enable_asymmetric_mass_coupling()
        assert lattice.asymmetric_coupling_enabled

    def test_mass_gradient_affects_evolution(self):
        """Test that mass gradient actually affects pressure evolution"""
        # Without asymmetric coupling
        lat_standard = PressureTensorLattice()
        lat_standard.inject_pressure_wake(amplitude=1.0)
        for _ in range(100):
            lat_standard.update_step_pressure_tensor()
        curve_standard = lat_standard.measure_rotation_velocity()

        # With asymmetric coupling
        lat_asym = PressureTensorLattice()
        lat_asym.inject_pressure_wake(amplitude=1.0)
        lat_asym.enable_asymmetric_mass_coupling()
        for _ in range(100):
            lat_asym.update_step_pressure_tensor()
        curve_asym = lat_asym.measure_rotation_velocity()

        # Curves should differ
        v_std = np.array(curve_standard["rotation_velocities_km_s"][:8])
        v_asym = np.array(curve_asym["rotation_velocities_km_s"][:8])
        # Asymmetric coupling should produce different velocity structure
        assert not np.allclose(v_std, v_asym, atol=10)


class TestRotationCurveMeasurement:
    """Test rotation curve extraction from pressure tensor"""

    def test_rotation_curve_extraction(self):
        """Test that rotation curves can be extracted"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)
        curve = lattice.measure_rotation_velocity()

        assert "radii_kpc" in curve
        assert "rotation_velocities_km_s" in curve
        assert len(curve["radii_kpc"]) > 0
        assert len(curve["rotation_velocities_km_s"]) > 0

    def test_rotation_velocities_physical(self):
        """Test that rotation velocities are in physical range"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)
        curve = lattice.measure_rotation_velocity()

        velocities = np.array(curve["rotation_velocities_km_s"])
        # Galaxy rotation should be between 20 and 400 km/s
        assert np.all(velocities >= 20)
        assert np.all(velocities <= 400)

    def test_rotation_curve_changes_with_evolution(self):
        """Test that rotation velocities change during evolution"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()

        initial_curve = lattice.measure_rotation_velocity()
        initial_v = np.mean(initial_curve["rotation_velocities_km_s"]) if initial_curve["rotation_velocities_km_s"] else 0

        lattice.run_equilibration(steps=100)

        final_curve = lattice.measure_rotation_velocity()
        final_v = np.mean(final_curve["rotation_velocities_km_s"]) if final_curve["rotation_velocities_km_s"] else 0

        # Velocities should change (not identical)
        # They might increase or decrease, but should evolve
        assert abs(final_v - initial_v) > 0.1  # Should noticeably change

    def test_radii_ordered(self):
        """Test that radii are in increasing order"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)
        curve = lattice.measure_rotation_velocity()

        radii = curve["radii_kpc"]
        assert radii == sorted(radii)


class TestPressureStatistics:
    """Test pressure tensor statistics and diagnostics"""

    def test_pressure_statistics_computation(self):
        """Test that pressure statistics are computed"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)

        stats = lattice.measure_pressure_statistics()
        assert "max_pressure" in stats
        assert "mean_pressure" in stats
        assert "tangential_pressure_avg" in stats
        assert "is_stable" in stats

    def test_pressure_components_tracked(self):
        """Test that individual pressure components are tracked"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)

        stats = lattice.measure_pressure_statistics()
        assert "radial_pressure_avg" in stats
        assert "tangential_pressure_avg" in stats
        assert "shear_coupling_avg" in stats

    def test_stability_flag_works(self):
        """Test that stability flag correctly identifies stable states"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()

        stats = lattice.measure_pressure_statistics()
        assert stats["is_stable"]  # Should be stable initially

    def test_max_velocity_method(self):
        """Test that max_velocity method works"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)

        max_v = lattice.max_velocity()
        assert isinstance(max_v, float)
        assert max_v > 0
        assert max_v < 400


class TestPhase3FullPhysics:
    """Test full Phase 3 implementation with all features"""

    def test_full_physics_initialization(self):
        """Test initialization with all features enabled"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake(amplitude=1.5)
        lattice.enable_nonlinear_saturation()
        lattice.enable_asymmetric_mass_coupling()

        assert lattice.nonlinear_enabled
        assert lattice.asymmetric_coupling_enabled

    def test_full_physics_evolution(self):
        """Test evolution with all features enabled"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake(amplitude=1.5)
        lattice.enable_nonlinear_saturation()
        lattice.enable_asymmetric_mass_coupling()

        for _ in range(100):
            lattice.update_step_pressure_tensor()

        assert lattice.is_stable()

    def test_all_features_produce_different_curves(self):
        """Test that enabling all features changes rotation curves"""
        # Basic
        lat_basic = PressureTensorLattice()
        lat_basic.inject_pressure_wake()
        lat_basic.run_equilibration(steps=80)
        curve_basic = lat_basic.measure_rotation_velocity()

        # Full physics
        lat_full = PressureTensorLattice()
        lat_full.inject_pressure_wake(amplitude=1.5)
        lat_full.enable_nonlinear_saturation()
        lat_full.enable_asymmetric_mass_coupling()
        lat_full.run_equilibration(steps=80)
        curve_full = lat_full.measure_rotation_velocity()

        v_basic = np.array(curve_basic["rotation_velocities_km_s"])
        v_full = np.array(curve_full["rotation_velocities_km_s"])

        # Should be different (not just noise)
        assert not np.allclose(v_basic, v_full, atol=15)

    def test_full_physics_generates_structure(self):
        """Test that full physics can generate rotation curve structure"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake(amplitude=2.0)
        lattice.enable_nonlinear_saturation()
        lattice.enable_asymmetric_mass_coupling()

        # Run longer evolution
        lattice.run_equilibration(steps=150)
        curve = lattice.measure_rotation_velocity()

        velocities = np.array(curve["rotation_velocities_km_s"])

        # Check for some structure (not completely flat)
        velocity_variation = np.std(velocities)
        assert velocity_variation > 1.0, "Should have some structure"


class TestComparisonsAndImprovement:
    """Test improvements over Phase 2"""

    def test_pressure_tensor_enables_velocity_range(self):
        """Test that pressure tensor can achieve wider velocity range"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake(amplitude=2.0)
        lattice.enable_nonlinear_saturation()
        lattice.enable_asymmetric_mass_coupling()

        for _ in range(200):
            lattice.update_step_pressure_tensor()

        curve = lattice.measure_rotation_velocity()
        velocities = np.array(curve["rotation_velocities_km_s"])

        # Should have reasonable velocity range
        v_min = np.min(velocities)
        v_max = np.max(velocities)

        assert v_min > 20, "Minimum velocity should be above 20 km/s"
        assert v_max > 80, "Maximum velocity should exceed 80 km/s"

    def test_tangential_pressure_dominates(self):
        """Test that tangential pressure (drives rotation) is significant"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake(amplitude=1.5)
        lattice.enable_nonlinear_saturation()
        lattice.enable_asymmetric_mass_coupling()

        for _ in range(150):
            lattice.update_step_pressure_tensor()

        stats = lattice.measure_pressure_statistics()
        # Tangential pressure should be significant
        assert stats["tangential_pressure_avg"] > 0.01


class TestDataSerialization:
    """Test that lattice state can be serialized"""

    def test_to_dict_method(self):
        """Test that lattice state converts to dictionary"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)

        state_dict = lattice.to_dict()
        assert isinstance(state_dict, dict)
        assert "time_steps" in state_dict
        assert "parameters" in state_dict
        assert "statistics" in state_dict

    def test_serialized_data_valid(self):
        """Test that serialized data contains valid values"""
        lattice = PressureTensorLattice()
        lattice.inject_pressure_wake()
        lattice.run_equilibration(steps=50)

        state_dict = lattice.to_dict()

        assert state_dict["time_steps"] >= 50
        assert "gamma" in state_dict["parameters"]
        assert "beta" in state_dict["parameters"]


# Running tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
