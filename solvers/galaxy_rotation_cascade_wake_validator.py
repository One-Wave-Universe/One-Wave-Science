#!/usr/bin/env python3
"""
PHASE 2.2: Galaxy Rotation Cascade Wake Validator (CORRECTED)
One-Wave Framework: Dark Matter as Extended Compression Effect (Wake Nesting)

Tests whether hierarchical gravity wakes explain galaxy rotation curves.
Physics: v_c²(r)/r = |g_local(r) + g_inherited(r)|

Author: Claude Haiku 4.5 + Mark Wright Adlard
Date: October 5, 2026
"""

import numpy as np
from scipy.interpolate import interp1d
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass
import json

from observational_data_loader import ValidatorDataInterface

# ============================================================================
# GALAXY LOCAL GRAVITY FIELD (CORRECTED UNITS)
# ============================================================================

class GalaxyLocalGravity:
    """
    Model LOCAL gravity from galaxy's mass distribution.
    
    Rotation velocity formula: v_c(r) = sqrt(r * g_total)
    
    For observed v ~ 200 km/s at r ~ 20 kpc:
    g_total ~ v²/r ~ 2.0 (km/s)² / kpc
    """
    
    def __init__(self, galaxy_name: str, radii_kpc: np.ndarray,
                 velocity_scaling: float = 1.0):
        """
        Args:
            galaxy_name: e.g., "Milky Way", "Andromeda"
            radii_kpc: Array of radii
            velocity_scaling: Factor to scale predicted velocity
        """
        self.name = galaxy_name
        self.radii = radii_kpc
        self.velocity_scaling = velocity_scaling
        
        # Compute local gravity in normalized units
        # Based on standard disk model
        self.g_local_profile = self._compute_local_gravity()
    
    def _compute_local_gravity(self) -> np.ndarray:
        """
        Compute g_local from disk + bulge model.
        
        For Milky Way / Andromeda scale systems, approximate as:
        - Inner region (r < 2 kpc): bulge dominates, rotation rises
        - Middle region (2-20 kpc): disk dominates, Keplerian-ish falloff
        - Outer region (r > 20 kpc): low mass, rotation should fall
        
        But observations show flat rotation, explained by g_wake.
        """
        g_local = np.zeros_like(self.radii)
        
        for i, r in enumerate(self.radii):
            if r < 0.1:
                g_local[i] = 0.0
            elif r < 2.0:
                # Bulge-dominated: fast rise
                g_local[i] = 1.0 * (r / 2.0)**1.5
            elif r < 10.0:
                # Disk transition: slower falloff than pure Keplerian
                # Pure Keplerian: g ~ 1/r²
                # With disk: g ~ 1/r * (1 + corrections)
                bulge_contrib = 0.5 / (r**2 + 1.0)  # Soft core
                disk_contrib = 1.0 / r  # Disk contribution
                g_local[i] = bulge_contrib + disk_contrib
            else:
                # Outer disk: low contribution, rotation should drop
                g_local[i] = 0.5 / (r**2) + 0.1 / r
        
        return g_local * self.velocity_scaling
    
    def evaluate_at_radius(self, r_kpc: float) -> float:
        """Get g_local value at specific radius."""
        if len(self.radii) > 1:
            f = interp1d(self.radii, self.g_local_profile, kind='cubic',
                        fill_value='extrapolate')
            return float(f(r_kpc))
        return self.g_local_profile[0]


# ============================================================================
# INHERITED CLUSTER WAKE GEOMETRY
# ============================================================================

class ClusterWakeGeometry:
    """
    Model gravity wake inherited from parent cluster.

    Standard terminology: "dark matter halo"
    One-Wave interpretation: Extended displaced energy in the superfluid.
    The halo is not a separate entity—it's the superfluid's response to mass
    concentrations. Pressure gradients ∇P in the superfluid generate the
    measured gravitational effects.
    """
    
    def __init__(self, cluster_name: str, radii_kpc: np.ndarray,
                 wake_amplitude: float = 1.0):
        """
        Args:
            cluster_name: e.g., "Local_Group"
            radii_kpc: Array of radii
            wake_amplitude: How strong the inherited wake is
        """
        self.cluster_name = cluster_name
        self.radii = radii_kpc
        self.wake_amplitude = wake_amplitude
        
        # Compute inherited wake
        self.g_wake_profile = self._compute_inherited_wake()
    
    def _compute_inherited_wake(self) -> np.ndarray:
        """
        Compute inherited gravity wake from parent cluster.
        
        Wake properties:
        - Core: weak (galaxy is inside cluster, not sampling strong gradient there)
        - Middle: rising (galaxy samples edge of cluster compression)
        - Outer: extended plateau (magnetic field keeps wake coherent)
        
        Model: Extended NFW-like profile
        """
        g_wake = np.zeros_like(self.radii)
        
        for i, r in enumerate(self.radii):
            if r < 1.0:
                # Inside cluster core: weak wake
                g_wake[i] = 0.1 * self.wake_amplitude
            elif r < 15.0:
                # Rising edge: galaxy samples cluster's compression gradient
                g_wake[i] = self.wake_amplitude * (r - 1.0) / (r + 5.0)
            else:
                # Extended halo: coherent displaced superfluid energy
                # Not separate dark matter particles, but the superfluid's
                # pressure response to the mass distribution
                g_wake[i] = self.wake_amplitude * 10.0 / (r + 20.0)
        
        return g_wake
    
    def evaluate_at_radius(self, r_kpc: float) -> float:
        """Get g_wake value at specific radius."""
        if len(self.radii) > 1:
            f = interp1d(self.radii, self.g_wake_profile, kind='cubic',
                        fill_value='extrapolate')
            return float(f(r_kpc))
        return self.g_wake_profile[0]


# ============================================================================
# MAIN VALIDATOR
# ============================================================================

class CascadeWakeRotationValidator:
    """Test: v_c²(r)/r = |g_local(r) + g_inherited(r)|"""
    
    def __init__(self, use_real_data: bool = True):
        self.interface = ValidatorDataInterface(use_real_data=use_real_data)
    
    def load_observational_data(self, galaxy_name: str) -> Dict:
        """Load real rotation curve from MAST."""
        query_name = "milky_way_rotation" if "milky" in galaxy_name.lower() else "andromeda_rotation"
        
        dataset, is_real = self.interface.fetch_observational_data(
            "mast", {"name": query_name}
        )
        
        radii = np.array(dataset.metadata.get("radius_kpc", []))
        velocities = np.array([r.value for r in dataset.records])
        errors = np.array([r.uncertainty for r in dataset.records])
        
        if len(radii) == 0:
            radii = np.linspace(1, len(dataset.records) * 2, len(dataset.records))
        
        return {
            "radii_kpc": radii,
            "velocities_kms": velocities,
            "errors_kms": errors,
            "is_real": is_real,
        }
    
    def predict_rotation_curve(self, galaxy_name: str, radii_kpc: np.ndarray,
                               wake_amplitude: float = 1.0) -> Dict:
        """
        Predict rotation curve from cascade geometry.
        
        Args:
            galaxy_name: "Milky Way" or "Andromeda"
            radii_kpc: Radii where to predict
            wake_amplitude: Strength of inherited wake
        
        Returns:
            Dict with predictions and component breakdown
        """
        # Local gravity from mass distribution
        local_scaling = 1.2 if "milky" in galaxy_name.lower() else 0.9
        galaxy_local = GalaxyLocalGravity(
            galaxy_name=galaxy_name,
            radii_kpc=radii_kpc,
            velocity_scaling=local_scaling
        )
        
        # Inherited wake from parent cluster
        cluster_wake = ClusterWakeGeometry(
            cluster_name="Local_Group",
            radii_kpc=radii_kpc,
            wake_amplitude=wake_amplitude
        )
        
        # Total gravity
        g_local = galaxy_local.g_local_profile
        g_inherited = cluster_wake.g_wake_profile
        g_total = g_local + g_inherited
        
        # Ensure positive
        g_total = np.maximum(g_total, 0.01)
        
        # Rotation curve: v = sqrt(r * g)
        velocities = np.sqrt(radii_kpc * g_total)
        
        return {
            "radii_kpc": radii_kpc,
            "velocities_kms": velocities,
            "g_local": g_local,
            "g_inherited": g_inherited,
            "g_total": g_total,
        }
    
    def compare_to_observations(self, galaxy_name: str,
                               wake_amplitude: float = 1.0) -> Dict:
        """Full validation: load obs, predict, compare."""
        print(f"\n{'='*70}")
        print(f"CASCADE WAKE: {galaxy_name.upper()}")
        print(f"{'='*70}")
        
        # Load observations
        obs = self.load_observational_data(galaxy_name)
        print(f"Loaded {len(obs['radii_kpc'])} points from MAST")
        print(f"  Radii: {obs['radii_kpc'][0]:.1f} to {obs['radii_kpc'][-1]:.1f} kpc")
        print(f"  Velocities: {obs['velocities_kms'][0]:.0f} to {obs['velocities_kms'][-1]:.0f} km/s")
        
        # Predict
        pred = self.predict_rotation_curve(
            galaxy_name=galaxy_name,
            radii_kpc=obs['radii_kpc'],
            wake_amplitude=wake_amplitude
        )
        
        # Compare
        obs_vel = obs['velocities_kms']
        pred_vel = pred['velocities_kms']
        errors = obs['errors_kms']
        
        residuals = obs_vel - pred_vel
        chi2 = np.sum((residuals / errors) ** 2)
        rms = np.sqrt(np.mean(residuals ** 2))
        norm_error = rms / np.mean(obs_vel)
        
        print(f"\nResults:")
        print(f"  χ² = {chi2:.2f}")
        print(f"  RMS = {rms:.1f} km/s")
        print(f"  Normalized error = {norm_error:.1%}")
        print(f"\n  g_local: {pred['g_local'].min():.2f} to {pred['g_local'].max():.2f}")
        print(f"  g_inherited: {pred['g_inherited'].min():.2f} to {pred['g_inherited'].max():.2f}")
        print(f"  Inherited contribution: {(np.mean(pred['g_inherited']) / np.mean(pred['g_total']) * 100):.0f}%")
        
        return {
            "galaxy": galaxy_name,
            "obs_data": obs,
            "prediction": pred,
            "chi2": chi2,
            "rms": rms,
            "norm_error": norm_error,
        }


def main():
    """Run cascade validator with optimized wake amplitude."""
    print("\n" + "="*70)
    print("PHASE 2.2 PRIORITY 1: REAL DATA TEST")
    print("Do hierarchical wakes explain rotation curves?")
    print("="*70)
    
    validator = CascadeWakeRotationValidator(use_real_data=True)
    
    # Test with different wake amplitudes to find best fit
    print("\nTesting wake amplitude sweep...")
    
    amplitudes = [0.5, 1.0, 1.5, 2.0, 2.5]
    results_by_amp = {}
    
    for amp in amplitudes:
        print(f"\n--- Wake Amplitude = {amp} ---")
        mw = validator.compare_to_observations("Milky Way", wake_amplitude=amp)
        m31 = validator.compare_to_observations("Andromeda", wake_amplitude=amp)
        
        results_by_amp[amp] = {
            "mw_chi2": mw['chi2'],
            "m31_chi2": m31['chi2'],
        }
    
    # Summary
    print("\n" + "="*70)
    print("AMPLITUDE SWEEP RESULTS")
    print("="*70)
    print("\nAmplitude | MW χ²     | M31 χ²    | Combined")
    print("-" * 50)
    for amp in amplitudes:
        mw_chi2 = results_by_amp[amp]['mw_chi2']
        m31_chi2 = results_by_amp[amp]['m31_chi2']
        combined = mw_chi2 + m31_chi2
        print(f"{amp:9.1f} | {mw_chi2:9.2f} | {m31_chi2:9.2f} | {combined:9.2f}")
    
    # Best fit
    best_amp = min(amplitudes, key=lambda a: results_by_amp[a]['mw_chi2'] + results_by_amp[a]['m31_chi2'])
    print(f"\nBest amplitude: {best_amp} (minimum combined χ²)")
    
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70)
    print("\nIf χ² ~ 10-50 (reasonable fit):")
    print("  → Cascade wake model works")
    print("  → Dark matter = inherited gravity wake, not particle")
    print("\nIf χ² still large (> 100):")
    print("  → Model needs refinement:")
    print("    - C-319 magnetic effects")
    print("    - 3D D-409 lattice effects")
    print("    - Better galaxy position modeling")


if __name__ == "__main__":
    main()
