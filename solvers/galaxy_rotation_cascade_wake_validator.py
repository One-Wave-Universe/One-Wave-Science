#!/usr/bin/env python3
"""
PHASE 2.2: Galaxy Rotation Cascade Wake Validator
One-Wave Framework: Dark Matter as Extended Compression Effect (Wake Nesting)

This validator tests whether hierarchical gravity wakes (from Great Attractor
down through galaxy clusters to individual galaxies) explain observed galaxy
rotation curves WITHOUT invoking:
  1. Dark matter particles
  2. Local pressure profile fitting

Instead: Each galaxy sits in its parent cluster's gravity wake. The rotation
curve is determined by:
  - g_local(r) = local gradient from galaxy's mass distribution
  - g_inherited(r) = galaxy's sampling of parent cluster's organized wake
  
The sum g_total(r) = g_local + g_inherited produces the observed rotation curve.

Physics Reference:
  - GRAVITY_WAKE_NESTING_ROTATION_CASCADE.md (cascade mechanism)
  - algorithm_zero_physics_engine.py (CascadeSimulator implementation)
  - A-115 Unified Compression Field (source theory)
  - Book5_Ch1 Galaxies and Dark Matter (application at galactic scale)

Author: Claude Haiku 4.5 + Mark Wright Adlard
Date: October 5, 2026
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage import zoom
from scipy.fft import fftn, ifftn
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass
import json

from observational_data_loader import ValidatorDataInterface

# ============================================================================
# CASCADE WAKE LEVEL: Imported from algorithm_zero_physics_engine
# ============================================================================

@dataclass
class CascadeWakeLevel:
    """One level in gravitational cascade (parent → child galaxy)."""
    name: str                          # "Great Attractor", "Virgo Cluster", "Milky Way"
    scale_size_kpc: float              # Physical size scale
    wake_field: np.ndarray             # Gravity wake field: g_wake(r)
    wake_amplitude: float              # Maximum wake strength
    coherence_radius_kpc: float        # How far wake persists coherently
    frequency_ratio: float             # Frequency relative to parent

# ============================================================================
# PART 1: Inherited Cluster Wake Geometry
# ============================================================================

class ClusterWakeGeometry:
    """
    Model the gravity wake left by a parent galaxy cluster as it moves
    through cosmological structure (or maintains its structure in space).
    
    This is the INHERITED environment into which a galaxy is born.
    """
    
    def __init__(self, cluster_name: str, cluster_center_kpc: Tuple[float, float],
                 cluster_velocity_kms: Tuple[float, float], radii_kpc: np.ndarray):
        """
        Args:
            cluster_name: e.g., "Virgo Cluster", "Local Group"
            cluster_center_kpc: (x, y) center position in cluster coordinates
            cluster_velocity_kms: (vx, vy) velocity of cluster through cosmic space
            radii_kpc: Array of radii where we evaluate g_wake
        """
        self.cluster_name = cluster_name
        self.center = np.array(cluster_center_kpc)
        self.velocity = np.array(cluster_velocity_kms)
        self.radii = radii_kpc
        
        # Compute inherited wake profile
        self.g_wake_profile = self._compute_inherited_wake()
    
    def _compute_inherited_wake(self) -> np.ndarray:
        """
        Compute the gravity wake left by parent cluster.
        
        Wake is strongest where cluster concentration was highest, persists
        along direction of cluster motion, and decays with distance.
        
        Physics: Cluster moving through field leaves compression trail.
        Trail persists due to magnetic field organization.
        """
        g_wake = np.zeros_like(self.radii)
        
        for i, r in enumerate(self.radii):
            # Distance from cluster center
            distance = r
            
            # Wake amplitude decays with distance
            # At r = 0: maximum (where cluster is/was)
            # At large r: asymptotic to small value
            # Shape: exponential with scale ~correlation length
            
            correlation_length = 500.0  # ~500 kpc for Local Group scale
            decay_scale = 2.0 * correlation_length  # 2× correlation = falloff scale
            
            # Inherited wake follows the cluster's mass distribution
            # Model: Generalized NFW-like profile from cluster wake
            amplitude = 200.0  # km/s² at reference
            
            # Wake profile: high in core, extended halo
            if distance < 100:
                # Inner core: strong wake
                g_wake[i] = amplitude * np.exp(-(distance / 50.0)**2)
            else:
                # Extended halo: wake persists
                # This is the "dark matter"-like extended component
                g_wake[i] = amplitude * 50.0 / distance * np.exp(-(distance / decay_scale))
        
        return g_wake
    
    def evaluate_at_radius(self, r_kpc: float) -> float:
        """Get g_wake value at specific radius (interpolated)."""
        if len(self.radii) > 1:
            f = interp1d(self.radii, self.g_wake_profile, kind='cubic',
                        fill_value='extrapolate')
            return float(f(r_kpc))
        return self.g_wake_profile[0]

# ============================================================================
# PART 2: Galaxy Local Gravity Field
# ============================================================================

class GalaxyLocalGravity:
    """
    Model the LOCAL gravity field created by galaxy's own mass distribution.
    
    This is g_local in: g_total = g_local + g_inherited
    """
    
    def __init__(self, galaxy_name: str, radii_kpc: np.ndarray,
                 bulge_mass_solar: float = 2e10, disk_scale_kpc: float = 5.0):
        """
        Args:
            galaxy_name: e.g., "Milky Way", "Andromeda"
            radii_kpc: Array of radii where we evaluate g_local
            bulge_mass_solar: Central bulge mass in solar masses
            disk_scale_kpc: Scale radius of disk
        """
        self.name = galaxy_name
        self.radii = radii_kpc
        self.bulge_mass = bulge_mass_solar
        self.disk_scale = disk_scale_kpc
        
        # Compute local gravity profile
        self.g_local_profile = self._compute_local_gravity()
    
    def _compute_local_gravity(self) -> np.ndarray:
        """
        Compute g_local from galaxy's mass distribution.
        
        Using Keplerian approximation with scale height:
            g(r) ≈ G*M(r) / r²
        where M(r) includes both bulge and disk contributions.
        """
        g_local = np.zeros_like(self.radii)
        G_eff = 1.0  # Effective gravitational constant (normalized units)
        
        for i, r in enumerate(self.radii):
            # Bulge mass (concentrated at center)
            M_bulge = self.bulge_mass
            
            # Disk mass (distributed in disk)
            # Scale-height model: M_disk(r) ≈ M_disk_total * (1 - exp(-r/scale))
            M_disk_total = 5e10  # Solar masses
            M_disk = M_disk_total * (1.0 - np.exp(-r / self.disk_scale))
            
            # Total mass within radius
            M_total = M_bulge + M_disk
            
            # Local gravity (Keplerian falloff + disk flattening effects)
            if r > 0.1:
                # Includes correction for finite disk scale height
                g_local[i] = G_eff * M_total / (r**2) * (1.0 - 0.1 * np.exp(-r/5.0))
            else:
                g_local[i] = 0.0
        
        return g_local
    
    def evaluate_at_radius(self, r_kpc: float) -> float:
        """Get g_local value at specific radius (interpolated)."""
        if len(self.radii) > 1:
            f = interp1d(self.radii, self.g_local_profile, kind='cubic',
                        fill_value='extrapolate')
            return float(f(r_kpc))
        return self.g_local_profile[0]

# ============================================================================
# PART 3: Cascade Wake Validator (Main)
# ============================================================================

class CascadeWakeRotationValidator:
    """
    Validate whether cascade wake nesting explains galaxy rotation curves.
    
    Core test: v_c²(r)/r = |g_local(r) + g_inherited(r)|
    
    where:
      - g_local = galaxy's own mass distribution gravity
      - g_inherited = galaxy's sampling of parent cluster's organized wake
    
    Result: If this explains observed curves, dark matter = wake (not particle)
    """
    
    def __init__(self, use_real_data: bool = True):
        self.interface = ValidatorDataInterface(use_real_data=use_real_data)
        self.results = {}
    
    def load_observational_data(self, galaxy_name: str) -> Dict:
        """Load real galaxy rotation curve data from MAST archive."""
        query_name = "milky_way_rotation" if "milky" in galaxy_name.lower() else "andromeda_rotation"
        
        dataset, is_real = self.interface.fetch_observational_data(
            "mast",
            {"name": query_name}
        )
        
        # Extract data
        radii = np.array(dataset.metadata.get("radius_kpc", []))
        velocities = np.array([r.value for r in dataset.records])
        errors = np.array([r.uncertainty for r in dataset.records])
        
        if len(radii) == 0:
            # Fallback: generate radii assuming linear spacing
            radii = np.linspace(1, len(dataset.records) * 2, len(dataset.records))
        
        return {
            "radii_kpc": radii,
            "velocities_kms": velocities,
            "errors_kms": errors,
            "is_real": is_real,
            "source": dataset.source,
            "reference": dataset.reference,
        }
    
    def predict_rotation_curve(self, galaxy_name: str, radii_kpc: np.ndarray,
                               cluster_name: str = "Local_Group",
                               galaxy_position_in_cluster: float = 0.3) -> Dict:
        """
        Predict rotation curve from cascade wake inheritance.
        
        Args:
            galaxy_name: "Milky Way" or "Andromeda"
            radii_kpc: Radii where to predict
            cluster_name: Parent cluster (context)
            galaxy_position_in_cluster: Position in cluster (0=center, 1=edge) normalized
        
        Returns:
            Dict with predicted velocities, g_local, g_inherited breakdown
        """
        
        # 1. Get parent cluster's inherited wake
        cluster_wake = ClusterWakeGeometry(
            cluster_name=cluster_name,
            cluster_center_kpc=(0.0, 0.0),  # Cluster at origin
            cluster_velocity_kms=(50.0, 30.0),  # Cluster velocity
            radii_kpc=radii_kpc
        )
        
        # 2. Get galaxy's local gravity
        galaxy_local = GalaxyLocalGravity(
            galaxy_name=galaxy_name,
            radii_kpc=radii_kpc,
            bulge_mass_solar=2e10 if "milky" in galaxy_name.lower() else 3e10,
            disk_scale_kpc=5.0 if "milky" in galaxy_name.lower() else 6.0
        )
        
        # 3. Galaxy position in cluster wake affects how strongly it inherits
        # Galaxies at edge sample outer wake more; at center sample core more
        inherited_scaling = 0.5 + 0.5 * galaxy_position_in_cluster
        
        # 4. Compute total gravity and rotation curve
        g_local_arr = galaxy_local.g_local_profile
        g_inherited_arr = cluster_wake.g_wake_profile * inherited_scaling
        g_total = g_local_arr + g_inherited_arr
        
        # Rotation curve: v²/r = g_total  →  v = sqrt(r * g_total)
        # Ensure g_total > 0
        g_total = np.maximum(g_total, 0.1)
        velocities = np.sqrt(radii_kpc * g_total)
        
        return {
            "radii_kpc": radii_kpc,
            "velocities_kms": velocities,
            "g_local": g_local_arr,
            "g_inherited": g_inherited_arr,
            "g_total": g_total,
            "cluster_name": cluster_name,
            "galaxy_position_scaling": inherited_scaling,
        }
    
    def compare_to_observations(self, galaxy_name: str) -> Dict:
        """
        Full validation pipeline:
        1. Load observational data
        2. Predict rotation curve from cascade wake
        3. Compute residuals and fit quality
        4. Report results
        """
        print(f"\n{'='*70}")
        print(f"CASCADE WAKE VALIDATOR: {galaxy_name.upper()}")
        print(f"{'='*70}")
        
        # Load observations
        obs_data = self.load_observational_data(galaxy_name)
        print(f"\nLoaded observational data:")
        print(f"  Radii: {obs_data['radii_kpc'][:3]} ... {obs_data['radii_kpc'][-3:]} kpc")
        print(f"  Velocities: {obs_data['velocities_kms'][:3]} ... {obs_data['velocities_kms'][-3:]} km/s")
        print(f"  Data source: {'REAL (MAST)' if obs_data['is_real'] else 'SYNTHETIC'}")
        
        # Predict from cascade wake
        prediction = self.predict_rotation_curve(
            galaxy_name=galaxy_name,
            radii_kpc=obs_data['radii_kpc'],
            cluster_name="Local_Group" if "milky" in galaxy_name.lower() else "Andromeda_Local",
            galaxy_position_in_cluster=0.3 if "milky" in galaxy_name.lower() else 0.4
        )
        
        # Compare
        obs_vel = obs_data['velocities_kms']
        pred_vel = prediction['velocities_kms']
        errors = obs_data['errors_kms']
        
        # Residuals
        residuals = obs_vel - pred_vel
        chi2 = np.sum((residuals / errors) ** 2)
        rms_error = np.sqrt(np.mean(residuals ** 2))
        normalized_error = rms_error / np.mean(obs_vel)
        
        print(f"\nPrediction Results:")
        print(f"  χ² = {chi2:.2f}")
        print(f"  RMS error = {rms_error:.2f} km/s")
        print(f"  Normalized error = {normalized_error:.1%}")
        print(f"\n  g_local range: {prediction['g_local'].min():.1f} to {prediction['g_local'].max():.1f}")
        print(f"  g_inherited range: {prediction['g_inherited'].min():.1f} to {prediction['g_inherited'].max():.1f}")
        print(f"  g_total range: {prediction['g_total'].min():.1f} to {prediction['g_total'].max():.1f}")
        print(f"\n  Inherited wake contribution: {(prediction['g_inherited'].mean() / prediction['g_total'].mean() * 100):.1f}% of total gravity")
        
        return {
            "galaxy": galaxy_name,
            "obs_data": obs_data,
            "prediction": prediction,
            "residuals": residuals,
            "chi2": chi2,
            "rms_error": rms_error,
            "normalized_error": normalized_error,
        }


# ============================================================================
# MAIN: Run Full Cascade Wake Validation
# ============================================================================

def main():
    """Run complete cascade wake validator against real MAST data."""
    print("\n" + "="*70)
    print("PHASE 2.2: GALAXY ROTATION CASCADE WAKE VALIDATOR")
    print("Testing: Do hierarchical gravity wakes explain rotation curves?")
    print("="*70)
    
    validator = CascadeWakeRotationValidator(use_real_data=True)
    
    # Test both galaxies
    mw_result = validator.compare_to_observations("Milky Way")
    m31_result = validator.compare_to_observations("Andromeda")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY: INHERITED WAKE vs DARK MATTER PARTICLE")
    print("="*70)
    
    print("\nMillky Way:")
    print(f"  χ² = {mw_result['chi2']:.2f}")
    print(f"  RMS = {mw_result['rms_error']:.2f} km/s")
    
    print("\nAndromeda:")
    print(f"  χ² = {m31_result['chi2']:.2f}")
    print(f"  RMS = {m31_result['rms_error']:.2f} km/s")
    
    print("\n" + "-"*70)
    print("INTERPRETATION:")
    print("-"*70)
    print("\nIf χ² is reasonable (< 200) and RMS < 50 km/s:")
    print("  → Cascade wake nesting explains rotation without dark matter particle")
    print("  → 'Dark matter' halo = inherited gravity wake from parent cluster")
    print("  → No new substance needed; same A-115 compression field viewed top-down")
    
    print("\nIf χ² >> 200 or RMS >> 50 km/s:")
    print("  → Cascade model incomplete (likely needs C-319 magnetic effects)")
    print("  → Or galaxy position in cluster wake needs refinement")
    print("  → Or 3D effects missing from 2D model")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
