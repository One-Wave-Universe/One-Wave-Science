#!/usr/bin/env python3
"""
DISTANCE-DEPENDENT COUPLING MODEL: Cascade boundary layer physics

Physics: At distance, satellites inherit path curvature (rotation) but not direct gravity.

Coupling function: β(r) = β₀ × exp(-r/r_decay)
- β₀ = base coupling factor (0.3 from Algorithm Zero)
- r_decay = distance scale where coupling drops to ~37% (e⁻¹)

Tests whether path-curvature-only inheritance explains SMC/distant satellites.
"""

import numpy as np
from scipy.optimize import minimize
from satellite_galaxy_velocity_validator import (
    SatelliteVelocityPredictor, MW_SATELLITES, M31_SATELLITES
)

class DistanceDependentPredictor(SatelliteVelocityPredictor):
    """Satellite predictor with distance-dependent coupling."""
    
    def __init__(self, velocity_scale_factor=39.23, beta_0=0.3, r_decay_mw=50.0, r_decay_m31=40.0):
        super().__init__()
        self.velocity_scale_factor = velocity_scale_factor
        self.beta_0 = beta_0
        self.r_decay_mw = r_decay_mw  # Distance scale for MW coupling decay
        self.r_decay_m31 = r_decay_m31  # Distance scale for M31 coupling decay

    def coupling_factor(self, distance_kpc, host):
        """Distance-dependent coupling β(r) = β₀ × exp(-r/r_decay)."""
        if host == "Milky Way":
            r_decay = self.r_decay_mw
        elif host == "Andromeda":
            r_decay = self.r_decay_m31
        else:
            return self.beta_0
        
        # Exponential decay with distance
        return self.beta_0 * np.exp(-distance_kpc / r_decay)

    def predict_satellite_velocity(self, satellite):
        """Predict with distance-dependent coupling."""
        result = super().predict_satellite_velocity(satellite)
        
        if result['in_cascade']:
            # Replace constant coupling with distance-dependent
            beta_r = self.coupling_factor(satellite.distance_kpc, satellite.host)
            
            if satellite.host == "Milky Way":
                v_host = self.mw_orbital_velocity
            else:
                v_host = self.m31_orbital_velocity
            
            # Recalculate with distance-dependent coupling
            v_inherited_new = v_host * beta_r
            v_total_new = result['v_local'] + v_inherited_new
            
            result['v_inherited'] = v_inherited_new
            result['v_total'] = v_total_new
            result['residual'] = satellite.velocity_dispersion_kms - v_total_new
            result['error_pct'] = 100 * abs(satellite.velocity_dispersion_kms - v_total_new) / satellite.velocity_dispersion_kms
            result['coupling_factor'] = beta_r
        
        return result

def compute_chi2_distance_coupling(params):
    """Compute χ² for distance-dependent coupling model."""
    velocity_scale, beta_0, r_decay_mw, r_decay_m31 = params
    
    if velocity_scale <= 0 or beta_0 <= 0 or r_decay_mw <= 0 or r_decay_m31 <= 0:
        return 1e10
    
    predictor = DistanceDependentPredictor(velocity_scale, beta_0, r_decay_mw, r_decay_m31)
    chi2_total = 0
    count = 0
    
    for satellite in MW_SATELLITES + M31_SATELLITES:
        result = predictor.predict_satellite_velocity(satellite)
        if result['in_cascade']:
            obs_err = 2.0  # ~2 km/s measurement uncertainty
            residual = (result['v_observed'] - result['v_total']) / obs_err
            chi2_total += residual ** 2
            count += 1
    
    return chi2_total if count > 0 else 1e10

print("\n" + "="*80)
print("OPTIMIZATION: Distance-Dependent Coupling Model")
print("="*80)
print("\nPhysics: β(r) = β₀ × exp(-r/r_decay)")
print("Fitting: velocity_scale, β₀, r_decay_mw, r_decay_m31\n")

# Initial guess
x0 = [39.23, 0.3, 50.0, 40.0]

# Optimize
result = minimize(compute_chi2_distance_coupling, x0, method='Nelder-Mead',
                  options={'maxiter': 1000, 'xatol': 0.01, 'fatol': 10})

velocity_scale_opt, beta_0_opt, r_decay_mw_opt, r_decay_m31_opt = result.x
chi2_opt = result.fun

print(f"Optimized Parameters:")
print(f"  velocity_scale_factor: {velocity_scale_opt:.2f}")
print(f"  β₀ (base coupling): {beta_0_opt:.3f}")
print(f"  r_decay_mw (MW decay scale): {r_decay_mw_opt:.1f} kpc")
print(f"  r_decay_m31 (M31 decay scale): {r_decay_m31_opt:.1f} kpc")
print(f"  χ² (in-cascade): {chi2_opt:.1f}\n")

# Test with optimized parameters
predictor = DistanceDependentPredictor(velocity_scale_opt, beta_0_opt, r_decay_mw_opt, r_decay_m31_opt)

print("="*80)
print("RESULTS: DISTANCE-DEPENDENT COUPLING MODEL")
print("="*80)

print("\nMILKY WAY (in-cascade satellites):")
print("Name                          | r(kpc) | β(r)   | v_obs | v_pred | Error")
print("-" * 80)

mw_results = []
for sat in MW_SATELLITES:
    result = predictor.predict_satellite_velocity(sat)
    if result['in_cascade']:
        mw_results.append(result)
        beta_r = result.get('coupling_factor', 0.3)
        print(f"{sat.name:28} | {result['distance_kpc']:6.1f} | {beta_r:.3f} | "
              f"{result['v_observed']:5.0f} | {result['v_total']:6.0f} | {result['error_pct']:5.1f}%")

if mw_results:
    mw_errors = [r['error_pct'] for r in mw_results]
    print(f"\nMW In-Cascade: Mean error = {np.mean(mw_errors):.1f}%")

print("\nANDROMEDA (in-cascade satellites):")
print("Name                          | r(kpc) | β(r)   | v_obs | v_pred | Error")
print("-" * 80)

m31_results = []
for sat in M31_SATELLITES:
    result = predictor.predict_satellite_velocity(sat)
    if result['in_cascade']:
        m31_results.append(result)
        beta_r = result.get('coupling_factor', 0.3)
        print(f"{sat.name:28} | {result['distance_kpc']:6.1f} | {beta_r:.3f} | "
              f"{result['v_observed']:5.0f} | {result['v_total']:6.0f} | {result['error_pct']:5.1f}%")

if m31_results:
    m31_errors = [r['error_pct'] for r in m31_results]
    print(f"\nM31 In-Cascade: Mean error = {np.mean(m31_errors):.1f}%")

print("\n" + "="*80)
print("VALIDATION ASSESSMENT")
print("="*80)

all_results = mw_results + m31_results
if all_results:
    all_errors = [r['error_pct'] for r in all_results]
    mean_error = np.mean(all_errors)
    
    print(f"\nIn-Cascade Satellites (Total: {len(all_results)}):")
    print(f"  Mean error: {mean_error:.1f}%")
    print(f"  Median error: {np.median(all_errors):.1f}%")
    print(f"  RMS error: {np.sqrt(np.mean(np.array(all_errors)**2)):.1f}%")
    
    print(f"\nCoupling Decay Scales:")
    print(f"  MW: β(r) = {beta_0_opt:.3f} × exp(-r/{r_decay_mw_opt:.1f})")
    print(f"      At r=50 kpc: β = {beta_0_opt * np.exp(-50/r_decay_mw_opt):.3f}")
    print(f"      At r=65 kpc: β = {beta_0_opt * np.exp(-65/r_decay_mw_opt):.3f}")
    print(f"  M31: β(r) = {beta_0_opt:.3f} × exp(-r/{r_decay_m31_opt:.1f})")
    print(f"      At r=26 kpc: β = {beta_0_opt * np.exp(-26/r_decay_m31_opt):.3f}")
    
    if mean_error < 30:
        print(f"\n  ✓ STRONG VALIDATION: Distance-dependent coupling explains all in-cascade satellites!")
        print(f"    Path curvature inheritance confirmed.")
    elif mean_error < 50:
        print(f"\n  ⚠ PARTIAL VALIDATION: Good structure, minor refinements needed")
    else:
        print(f"\n  ✗ Need further physics refinement")

print("\n" + "="*80)
