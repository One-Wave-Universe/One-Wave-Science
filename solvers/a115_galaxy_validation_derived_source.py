#!/usr/bin/env python3
"""Test derived A-115 source parameters (σ_core=0.5, σ_tail=2.0, weight_tail=0.4)
against real MW rotation curve data (45 published measurements) with only scale calibration.

Key: The source amplitude law derivation predicts these parameters should produce
exterior/interior acceleration ratio = 0.0391 at 3D layer-12 (r=12).
This test checks whether that predicted structure matches observed galaxy kinematics.

Circular velocity from A-115: v_c(r) = sqrt(a_radial(r) * r), where a_radial = -alpha * dχ/dr
Single free parameter: overall amplitude scale (K_chi).
No parameter fitting - only scale calibration.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded
from scipy.interpolate import interp1d
import sys

# Import solver
sys.path.insert(0, str(Path(__file__).parent))
from a115_dimensional_source_analysis import source_hybrid_nd, solve_a115_dimensional

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / 'data/mw_dr3plus_2023.csv'


def load_galaxy_data(csv_path=DATA_FILE):
    """Load 45-point MW rotation curve from real published measurements."""
    data = np.loadtxt(csv_path, delimiter=',', skiprows=1)
    if data.shape[0] != 45:
        raise ValueError(f"Expected 45 rows, got {data.shape[0]}")
    radius_kpc = data[:, 0]
    velocity_kms = data[:, 1]
    error_kms = data[:, 2]
    return radius_kpc, velocity_kms, error_kms


def acceleration_to_velocity(radius_kpc, radial_acceleration_from_solver):
    """Convert A-115 radial acceleration to circular velocity.

    v_c(r) = sqrt(a_radial(r) * r)

    Input: radial_acceleration from solver (outward positive)
    Note: a_radial = -alpha * grad(compression) from solver output
    """
    # Ensure acceleration is positive (outward)
    a_rad = np.abs(radial_acceleration_from_solver)

    # v_c^2 = a_centripetal * r = a_radial * r (when in balance)
    v_c_squared = a_rad * radius_kpc
    v_c = np.sqrt(np.maximum(v_c_squared, 0))

    return v_c


def solve_a115_galaxy_scale(dimension=3, outer_radius=30.0, cells=512,
                           sigma_core=0.5, sigma_tail=2.0, weight_tail=0.4,
                           stiffness=2.0, alpha=1.0):
    """Solve A-115 at galaxy scale with derived source parameters.

    Args:
        outer_radius: Match MW data range (5.25-27.25 kpc) + buffer
        sigma_core, sigma_tail, weight_tail: Derived from amplitude law
        stiffness, alpha: A-115 constitutive parameters

    Returns:
        result dict with grid, acceleration profile, etc.
    """
    def galaxy_source(r):
        return source_hybrid_nd(r, dimension,
                               sigma_core=sigma_core,
                               sigma_tail=sigma_tail,
                               weight_tail=weight_tail)

    result = solve_a115_dimensional(
        dimension=dimension,
        cells=cells,
        outer_radius=outer_radius,
        stiffness=stiffness,
        alpha=alpha,
        source_func=galaxy_source
    )

    return result


def fit_amplitude_scale(observed_velocity, predicted_velocity, error_observed):
    """Fit single amplitude scale parameter to match observations.

    Since predictions scale linearly with alpha, scale = mean(v_obs / v_pred)
    Use error-weighted least squares.
    """
    # Avoid division by zero
    mask = predicted_velocity > 1e-6

    if not np.any(mask):
        return 1.0, np.inf

    v_obs = observed_velocity[mask]
    v_pred = predicted_velocity[mask]
    w = 1.0 / (error_observed[mask]**2 + 1e-6)  # weight by inverse error

    # Solve: alpha = sum(w * v_obs * v_pred) / sum(w * v_pred^2)
    alpha_fit = np.sum(w * v_obs * v_pred) / np.sum(w * v_pred**2)

    # Compute weighted RMS
    residual = v_obs - alpha_fit * v_pred
    rms = np.sqrt(np.sum(w * residual**2) / np.sum(w))

    return alpha_fit, rms


def evaluate_derived_source():
    """Main evaluation: derived source vs 45-point MW data."""
    print("="*80)
    print("A-115 DERIVED SOURCE VALIDATION")
    print("Testing: σ_core=0.5, σ_tail=2.0, weight_tail=0.4 (from amplitude law)")
    print("Against: 45 published MW rotation measurements (DR3+ 2023)")
    print("="*80)

    # Load real data
    print("\n[1] Loading MW rotation curve (45 measurements)...")
    r_data, v_data, err_data = load_galaxy_data()
    print(f"    Range: {r_data[0]:.2f}-{r_data[-1]:.2f} kpc")
    print(f"    Velocity: {v_data.mean():.1f} ± {v_data.std():.1f} km/s")

    # Solve A-115 with derived parameters
    print("\n[2] Solving A-115 with derived source parameters...")
    result = solve_a115_galaxy_scale(
        dimension=3,
        outer_radius=30.0,  # Cover data range + buffer
        cells=512,
        sigma_core=0.5,
        sigma_tail=2.0,
        weight_tail=0.4,
        stiffness=2.0,
        alpha=1.0
    )

    print(f"    Solved on {result['cells']} cells, r=0-{result['outer_radius']:.1f}")
    print(f"    Max compression: {result['max_compression']:.6e}")
    print(f"    Max ext accel: {result['max_exterior_acceleration']:.6e}")
    print(f"    Max int accel: {result['max_interior_acceleration']:.6e}")
    print(f"    Ext/Int ratio: {result['max_exterior_acceleration']/max(result['max_interior_acceleration'], 1e-10):.6f}")

    # Interpolate solver solution to measurement radii
    print("\n[3] Interpolating predictions to measurement radii...")
    r_solver = np.array(result['radius_grid'])
    a_solver = np.array(result['acceleration_profile'])

    # Create interpolation function
    accel_interp = interp1d(r_solver, a_solver, kind='cubic', fill_value='extrapolate')
    a_at_data = accel_interp(r_data)

    # Convert to velocity
    v_predicted = acceleration_to_velocity(r_data, a_at_data)
    print(f"    Predicted velocity range: {v_predicted.min():.1f}-{v_predicted.max():.1f} km/s")

    # Fit amplitude scale
    print("\n[4] Fitting amplitude scale (single parameter)...")
    scale_fit, rms_residual = fit_amplitude_scale(v_data, v_predicted, err_data)
    print(f"    Fitted scale: {scale_fit:.6f}")
    print(f"    RMS residual: {rms_residual:.3f} km/s")

    # Compute error metrics
    v_predicted_scaled = scale_fit * v_predicted
    residuals = v_data - v_predicted_scaled

    mae = np.mean(np.abs(residuals))
    mape = np.mean(np.abs(residuals) / v_data) * 100
    chi2 = np.sum((residuals / err_data)**2)

    print("\n[5] Error metrics (after scale calibration):")
    print(f"    Mean Absolute Error: {mae:.3f} km/s")
    print(f"    Mean Absolute Percentage Error: {mape:.2f}%")
    print(f"    χ² (diagnostic): {chi2:.1f}")
    print(f"    χ²/N: {chi2/len(r_data):.2f}")

    # Detailed results at measurement points
    print("\n[6] Sample predictions (first 10 points):")
    print("    r(kpc)  v_obs(km/s)  v_pred_raw  v_pred_scaled  residual(km/s)  rel_error(%)")
    for i in range(min(10, len(r_data))):
        rel_err = abs(residuals[i]) / v_data[i] * 100
        print(f"    {r_data[i]:6.2f}  {v_data[i]:9.1f}  {v_predicted[i]:10.1f}  {v_predicted_scaled[i]:13.1f}  {residuals[i]:14.1f}  {rel_err:9.1f}")

    # Pass/fail criterion
    print("\n[7] Assessment:")
    if mape < 5.0:
        status = "✓ EXCELLENT"
        interpretation = "Derived source parameters match observations within ~5%"
    elif mape < 10.0:
        status = "✓ GOOD"
        interpretation = "Derived source parameters are consistent with observations"
    elif mape < 15.0:
        status = "≈ MODERATE"
        interpretation = "Derived source captures gross structure; systematic differences present"
    else:
        status = "✗ POOR"
        interpretation = "Derived source does not match observations; model requires revision"

    print(f"    {status}: {interpretation}")

    # Prepare report
    report = {
        "schema_version": 1,
        "test": "A-115 derived source validation against MW rotation curve",
        "data": {
            "source": "DR3+ 2023 published MW kinematics",
            "points": len(r_data),
            "radius_range_kpc": [float(r_data[0]), float(r_data[-1])],
            "velocity_mean_kms": float(v_data.mean()),
            "velocity_std_kms": float(v_data.std()),
        },
        "derived_parameters": {
            "sigma_core": 0.5,
            "sigma_tail": 2.0,
            "weight_tail": 0.4,
            "dimension": 3,
            "layer": 12,
            "predicted_ext_int_ratio": 0.0391,
            "source": "Derived from dimensional amplitude law (not fitted to galaxy data)",
        },
        "solver": {
            "method": "A-115 static compression field (radial symmetry, 3D)",
            "cells": result['cells'],
            "outer_radius_kpc": result['outer_radius'],
            "stiffness": result['stiffness'],
            "alpha": result['alpha'],
        },
        "fitting": {
            "free_parameters": 1,
            "parameter": "overall_amplitude_scale",
            "fitted_scale": float(scale_fit),
            "method": "error-weighted least squares on interpolated predictions",
        },
        "results": {
            "mean_absolute_error_kms": float(mae),
            "mean_absolute_percentage_error_percent": float(mape),
            "rms_residual_kms": float(rms_residual),
            "chi_squared_diagnostic": float(chi2),
            "chi_squared_per_point": float(chi2 / len(r_data)),
            "interpretation": interpretation,
            "status": status.split(":")[0].strip(),
        },
        "detailed_predictions": [
            {
                "radius_kpc": float(r),
                "observed_velocity_kms": float(v_obs),
                "quoted_error_kms": float(e),
                "predicted_velocity_raw_kms": float(v_pred),
                "predicted_velocity_scaled_kms": float(v_pred_scaled),
                "residual_kms": float(res),
                "relative_error_percent": float(abs(res) / v_obs * 100),
            }
            for r, v_obs, e, v_pred, v_pred_scaled, res
            in zip(r_data, v_data, err_data, v_predicted, v_predicted_scaled, residuals)
        ]
    }

    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                       default=ROOT / 'a115_galaxy_validation_report.json')
    args = parser.parse_args()

    try:
        report = evaluate_derived_source()
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Write report
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(f"\n[8] Full report written to: {args.output}")

    sys.exit(0)
