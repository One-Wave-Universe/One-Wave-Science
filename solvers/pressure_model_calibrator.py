#!/usr/bin/env python3
"""
Priority 2: Pressure Model Calibrator
One-Wave Framework: Galaxy Rotation

Systematic parameter optimization for GalacticPressureProfile against real MAST data.

Current Status:
- Pressure model fits poorly on real galaxy data (synthetic was optimistic)
- Need to find best-fit (P₀, a_s, r_core) parameters on real observations
- Synthetic parameters: P₀=1.0, a_s=3.0, r_core=0.5 (clearly wrong for real data)

Strategy:
1. Coarse grid search over parameter space
2. Fine-grained optimization around best regions
3. Cross-validation: fit to Milky Way, test on Andromeda
4. Document parameter sensitivity

Author: Claude Haiku 4.5 + Mark Wright Adlard
Date: October 5, 2026
"""

import numpy as np
from scipy.optimize import minimize
import json
from typing import Dict, Tuple
from observational_data_loader import ValidatorDataInterface
from galaxy_rotation_validator import GalacticPressureProfile, compute_residuals

class PressureModelCalibrator:
    """Optimize pressure profile parameters against real observational data."""

    def __init__(self, use_real_data: bool = True):
        self.interface = ValidatorDataInterface(use_real_data=use_real_data)
        self.calibration_results = {}

    def load_galaxy_data(self, galaxy_name: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Load real galaxy rotation curve data."""
        query_name = "milky_way_rotation" if "milky" in galaxy_name.lower() else "andromeda_rotation"

        dataset, is_real = self.interface.fetch_observational_data(
            "mast",
            {"name": query_name}
        )

        # Extract metadata
        radii = np.array(dataset.metadata.get("radius_kpc", []))
        velocities = np.array([r.value for r in dataset.records])
        errors = np.array([r.uncertainty for r in dataset.records])

        if len(radii) == 0:
            # Fallback: generate radii assuming linear spacing
            radii = np.linspace(1, len(dataset.records) * 2, len(dataset.records))

        return radii, velocities, errors

    def objective_function(self, params: np.ndarray, radii: np.ndarray,
                          velocities: np.ndarray, errors: np.ndarray) -> float:
        """
        Objective for optimization: reduced chi-squared.

        Parameters: [P0, a_s, r_core]
        """
        P0, a_s, r_core = params

        # Physical constraints
        if P0 <= 0 or a_s <= 0 or r_core <= 0:
            return 1e10
        if P0 > 10 or a_s > 20 or r_core > 5:
            return 1e10

        profile = GalacticPressureProfile(P0, a_s, r_core)
        predicted = profile.rotation_velocity(radii)

        # Chi-squared
        chi2 = np.sum(((velocities - predicted) / errors) ** 2)
        reduced_chi2 = chi2 / (len(radii) - 1)

        return reduced_chi2

    def coarse_grid_search(self, radii: np.ndarray, velocities: np.ndarray,
                          errors: np.ndarray, n_points: int = 5) -> Dict:
        """
        Coarse grid search over parameter space.

        Returns: best parameters and residuals dict
        """
        P0_range = np.linspace(0.5, 3.0, n_points)
        a_s_range = np.linspace(2.0, 10.0, n_points)
        r_core_range = np.linspace(0.2, 2.0, n_points)

        best_chi2 = np.inf
        best_params = None
        results = []

        for P0 in P0_range:
            for a_s in a_s_range:
                for r_core in r_core_range:
                    params = np.array([P0, a_s, r_core])
                    chi2 = self.objective_function(params, radii, velocities, errors)

                    results.append({
                        "P0": P0, "a_s": a_s, "r_core": r_core,
                        "reduced_chi2": chi2
                    })

                    if chi2 < best_chi2:
                        best_chi2 = chi2
                        best_params = params

        return {
            "best_params": best_params,
            "best_chi2": best_chi2,
            "all_results": results
        }

    def fine_optimization(self, params_init: np.ndarray, radii: np.ndarray,
                         velocities: np.ndarray, errors: np.ndarray) -> Dict:
        """
        Fine-grained optimization using scipy.optimize.minimize.
        """
        result = minimize(
            self.objective_function,
            params_init,
            args=(radii, velocities, errors),
            method='Nelder-Mead',
            options={'maxiter': 1000}
        )

        return {
            "best_params": result.x,
            "best_chi2": result.fun,
            "success": result.success,
            "n_iterations": result.nit
        }

    def calibrate_galaxy(self, galaxy_name: str) -> Dict:
        """
        Full calibration pipeline for a single galaxy.
        """
        print(f"\nCALIBRATING: {galaxy_name.upper()}")
        print("-" * 70)

        # Load data
        radii, velocities, errors = self.load_galaxy_data(galaxy_name)
        print(f"Loaded {len(radii)} data points")
        print(f"Velocity range: {velocities.min():.1f} - {velocities.max():.1f} km/s")

        # Coarse grid search
        print("\nPhase 1: Coarse grid search...")
        coarse = self.coarse_grid_search(radii, velocities, errors, n_points=5)
        print(f"Best from grid: χ² = {coarse['best_chi2']:.2f}")
        print(f"  P₀ = {coarse['best_params'][0]:.3f}")
        print(f"  a_s = {coarse['best_params'][1]:.3f} kpc")
        print(f"  r_core = {coarse['best_params'][2]:.3f} kpc")

        # Fine optimization
        print("\nPhase 2: Fine optimization...")
        fine = self.fine_optimization(coarse['best_params'], radii, velocities, errors)
        print(f"Best from optimization: χ² = {fine['best_chi2']:.2f}")
        print(f"  P₀ = {fine['best_params'][0]:.3f}")
        print(f"  a_s = {fine['best_params'][1]:.3f} kpc")
        print(f"  r_core = {fine['best_params'][2]:.3f} kpc")

        # Generate predictions with optimized model
        profile = GalacticPressureProfile(*fine['best_params'])
        predicted = profile.rotation_velocity(radii)
        residuals = compute_residuals(predicted, velocities, errors)

        return {
            "galaxy": galaxy_name,
            "coarse_search": coarse,
            "fine_optimization": fine,
            "residuals": residuals,
            "best_params": {
                "P0": float(fine['best_params'][0]),
                "a_s": float(fine['best_params'][1]),
                "r_core": float(fine['best_params'][2]),
            }
        }

    def cross_validate(self, fit_galaxy: str, test_galaxy: str) -> Dict:
        """
        Cross-validation: fit model to one galaxy, test on another.
        """
        print(f"\nCROSS-VALIDATION: Fit on {fit_galaxy.upper()}, test on {test_galaxy.upper()}")
        print("-" * 70)

        # Calibrate on fit galaxy
        fit_result = self.calibrate_galaxy(fit_galaxy)

        # Test on other galaxy
        test_radii, test_velocities, test_errors = self.load_galaxy_data(test_galaxy)

        profile = GalacticPressureProfile(*fit_result['best_params'].values())
        test_predicted = profile.rotation_velocity(test_radii)
        test_residuals = compute_residuals(test_predicted, test_velocities, test_errors)

        print(f"\nTest results on {test_galaxy}:")
        print(f"  χ² = {test_residuals['chi2']:.2f}")
        print(f"  RMS error = {test_residuals['rms']:.2f} km/s")
        print(f"  Normalized error = {test_residuals['normalized_error']:.1%}")

        return {
            "fit_galaxy": fit_galaxy,
            "fit_result": fit_result,
            "test_galaxy": test_galaxy,
            "test_residuals": test_residuals
        }


def main():
    """Run full calibration pipeline."""
    print("=" * 70)
    print("PRIORITY 2: PRESSURE MODEL CALIBRATION")
    print("Real Data Optimization (MAST Galaxy Rotation Curves)")
    print("=" * 70)

    calibrator = PressureModelCalibrator(use_real_data=True)

    # Calibrate individual galaxies
    mw_result = calibrator.calibrate_galaxy("milky_way")
    m31_result = calibrator.calibrate_galaxy("andromeda")

    # Cross-validation
    cv_mw_to_m31 = calibrator.cross_validate("milky_way", "andromeda")
    cv_m31_to_mw = calibrator.cross_validate("andromeda", "milky_way")

    # Summary
    print("\n\n" + "=" * 70)
    print("CALIBRATION SUMMARY")
    print("=" * 70)

    print(f"\nMillky Way best fit:")
    print(f"  χ² = {mw_result['residuals']['chi2']:.2f}")
    print(f"  P₀ = {mw_result['best_params']['P0']:.3f}")
    print(f"  a_s = {mw_result['best_params']['a_s']:.3f} kpc")
    print(f"  r_core = {mw_result['best_params']['r_core']:.3f} kpc")

    print(f"\nAndromeda best fit:")
    print(f"  χ² = {m31_result['residuals']['chi2']:.2f}")
    print(f"  P₀ = {m31_result['best_params']['P0']:.3f}")
    print(f"  a_s = {m31_result['best_params']['a_s']:.3f} kpc")
    print(f"  r_core = {m31_result['best_params']['r_core']:.3f} kpc")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
