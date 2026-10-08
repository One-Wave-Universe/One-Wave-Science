"""
Phase 5C: Three-View Verification - Unified Coefficient Set Validation

This module verifies that one coefficient set produces Higgs + mass-effect + dark-matter
from the same χ(r), and performs coefficient ablation tests to confirm load-bearing terms.

Verification strategy:
1. Extract three channels from baseline solution
2. Ablate each coefficient (set to zero) and observe degradation in all three channels
3. Verify no per-channel tuning is required
4. Calibrate global energy scale (Path A or B)
5. Predict particle spectrum from mass-effect tensor

Physics: All three observables come from the same Z state → J_source → χ(r) pipeline.
Removing any term in J_source degrades all three channels, confirming unification.

Author: Claude Haiku 4.5
Date: 2026-10-08
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from copy import deepcopy

try:
    from phase5a_source_term_bridge import FourInteractionSourceBridge
    from phase5a_unified_solver import UnifiedCompressionSolver
    from phase5b_bounded_knot_forward import BoundedKnotForwardSolver
except ImportError:
    print("Error: Phase 5A/5B modules not found.")
    import sys
    sys.exit(1)


class ThreeViewVerifier:
    """
    Verifies unified physics by testing coefficient ablations and energy calibration.
    """

    def __init__(self, Z_profile: Optional[Dict[str, np.ndarray]] = None):
        """
        Initialize verifier with four-interaction profile.

        Args:
            Z_profile: Native Z state (or extracts from D-409 if None)
        """
        self.solver = UnifiedCompressionSolver()
        self.bridge = FourInteractionSourceBridge(lattice_sites=13)

        # Extract native profile if not provided
        if Z_profile is None:
            print("Extracting native profile from D-409 ground state...")
            d409_solver = BoundedKnotForwardSolver()
            Z_profile = d409_solver.extract_equilibrium_profile()

        self.Z_profile = Z_profile
        self.baseline = None
        self.ablations = {}

    def compute_baseline(self, domain_radius: float = 4.0, grid_points: int = 256,
                        synthetic_profile: bool = False) -> Dict:
        """
        Compute baseline three channels with full coefficient set.

        Args:
            domain_radius: Outer radius for field solver
            grid_points: Radial grid resolution
            synthetic_profile: If True, use synthetic full-component profile; if False, use native Z_0

        Returns:
            Dict with three channels: mass_effect, gravity_dark_matter, mirror_gate
        """
        # If synthetic profile requested, create one with all four components
        if synthetic_profile:
            print("Creating synthetic full-component profile for ablation testing...")
            n_sites = 13
            r = np.linspace(0, 1, n_sites)
            # Create profile with all four components present
            Z_synthetic = {
                'K': 0.3 * np.exp(-(r**2)) * np.sin(2 * np.pi * r),
                'E': 0.2 * np.exp(-(r**2)) * (1 - r**2),
                'M': 0.25 * np.exp(-(r**2)) * np.cos(np.pi * r),
                'T': 0.15 * (1 - np.exp(-(r**2))) * r,
            }
            self.Z_profile_test = Z_synthetic
            test_profile = Z_synthetic
        else:
            test_profile = self.Z_profile

        print("Computing baseline solution with full coefficient set...")
        self.baseline = self.solver.solve_unified_field(
            test_profile, domain_radius=domain_radius, grid_points=grid_points
        )

        baseline_summary = {
            'mass_effect': self.baseline['mass_effect']['mass_effect'],
            'gravity_local': max(abs(float(x)) for x in self.baseline['gravity_dark_matter']['acceleration_local']),
            'gravity_wake': max(abs(float(x)) for x in self.baseline['gravity_dark_matter']['acceleration_wake']),
            'mirror_gate': self.baseline['mirror_gate']['E_MG_normalized'],
        }

        print(f"  m_eff = {baseline_summary['mass_effect']:.6f}")
        print(f"  g_local = {baseline_summary['gravity_local']:.6f}")
        print(f"  g_wake = {baseline_summary['gravity_wake']:.6f}")
        print(f"  E_MG = {baseline_summary['mirror_gate']:.6f}")

        return baseline_summary

    def ablate_coefficient(self, coefficient_name: str,
                          domain_radius: float = 4.0, grid_points: int = 256) -> Dict:
        """
        Remove one coefficient and observe impact on all three channels.

        Coefficients to ablate:
        - 's_K': Knot vortex coefficient
        - 's_E': Electrical shell coefficient
        - 's_M': Mirror-Gate coefficient
        - 's_T': Boundary-Tension coefficient
        - 'c_cross': Cross-interaction coupling

        Args:
            coefficient_name: Name of coefficient to ablate
            domain_radius: Field solver domain radius
            grid_points: Field solver grid resolution

        Returns:
            Dict with degraded three channels
        """
        # Create modified bridge with ablated coefficient
        modified_bridge = FourInteractionSourceBridge(lattice_sites=self.bridge.lattice_sites)

        # Store original value
        original_value = getattr(modified_bridge, coefficient_name)

        # Ablate (set to zero)
        setattr(modified_bridge, coefficient_name, 0.0)

        print(f"\nAblating {coefficient_name} (original: {original_value})...")

        # Compute source term with ablated coefficient
        J_source = modified_bridge.compute_source_term(self.Z_profile)

        # Solve field equation
        field_solution = modified_bridge.solve_compression_field(
            self.Z_profile, domain_radius=domain_radius, grid_points=grid_points
        )

        # Extract three channels
        mass_effect = modified_bridge._extract_mass_effect(field_solution, self.Z_profile) if hasattr(modified_bridge, '_extract_mass_effect') else None

        # Use unified solver for consistency
        unified = UnifiedCompressionSolver()
        unified.bridge = modified_bridge

        # Re-solve with modified bridge
        modified_solution = unified.solve_unified_field(
            self.Z_profile, domain_radius=domain_radius, grid_points=grid_points
        )

        ablation_result = {
            'coefficient': coefficient_name,
            'original_value': float(original_value),
            'ablated_value': 0.0,
            'mass_effect': modified_solution['mass_effect']['mass_effect'],
            'gravity_local': max(abs(float(x)) for x in modified_solution['gravity_dark_matter']['acceleration_local']),
            'gravity_wake': max(abs(float(x)) for x in modified_solution['gravity_dark_matter']['acceleration_wake']),
            'mirror_gate': modified_solution['mirror_gate']['E_MG_normalized'],
        }

        print(f"  Ablation impact:")
        print(f"    m_eff: baseline={self.baseline['mass_effect']['mass_effect']:.6f} → ablated={ablation_result['mass_effect']:.6f}")
        print(f"    g_local: {self.baseline['gravity_dark_matter']['acceleration_local'][0]:.6f} → {ablation_result['gravity_local']:.6f}") if self.baseline else None
        print(f"    E_MG: {self.baseline['mirror_gate']['E_MG_normalized']:.6f} → {ablation_result['mirror_gate']:.6f}")

        self.ablations[coefficient_name] = ablation_result
        return ablation_result

    def run_ablation_suite(self, coefficients_to_test: List[str] = None,
                          domain_radius: float = 4.0, grid_points: int = 256) -> Dict:
        """
        Run full ablation test suite.

        Args:
            coefficients_to_test: List of coefficient names to ablate
            domain_radius: Field solver domain radius
            grid_points: Field solver grid resolution

        Returns:
            Summary of ablation results
        """
        if coefficients_to_test is None:
            coefficients_to_test = ['s_K', 's_E', 's_M', 's_T', 'c_cross']

        print(f"Running ablation suite ({len(coefficients_to_test)} tests)...")

        for coeff in coefficients_to_test:
            self.ablate_coefficient(coeff, domain_radius, grid_points)

        return self.ablations

    def verify_unification(self) -> Dict:
        """
        Verify that the three channels are truly unified.

        Success criteria:
        1. All three channels present in baseline
        2. Removing any coefficient degrades all three
        3. No coefficient is dedicated to a single channel
        4. Same Z, same coefficients, three measurement views
        """
        if not self.baseline:
            raise ValueError("Must run compute_baseline() first")
        if not self.ablations:
            raise ValueError("Must run ablation suite first")

        verification = {
            'baseline_channels_present': True,
            'load_bearing_terms': [],
            'per_channel_tuning_detected': False,
            'unification_status': 'PENDING',
        }

        # Check baseline channels
        baseline = self.baseline
        channels = [
            ('mass_effect', baseline['mass_effect']['mass_effect']),
            ('gravity_local', max(abs(float(x)) for x in baseline['gravity_dark_matter']['acceleration_local'])),
            ('gravity_wake', max(abs(float(x)) for x in baseline['gravity_dark_matter']['acceleration_wake'])),
            ('mirror_gate', baseline['mirror_gate']['E_MG_normalized']),
        ]

        for ch_name, ch_value in channels:
            if ch_value < 1e-10:
                verification['baseline_channels_present'] = False
                print(f"⚠ Channel {ch_name} missing in baseline")

        # Check coefficient dependencies
        print("\nVerification: Load-bearing coefficient analysis")
        for coeff_name, ablation_data in self.ablations.items():
            # Check if all three channels degrade
            mass_degrades = ablation_data['mass_effect'] < baseline['mass_effect']['mass_effect'] * 0.9
            gravity_degrades = (ablation_data['gravity_local'] + ablation_data['gravity_wake']) < \
                             (channels[1][1] + channels[2][1]) * 0.9
            mirror_degrades = ablation_data['mirror_gate'] < baseline['mirror_gate']['E_MG_normalized'] * 0.9

            all_degrade = mass_degrades and gravity_degrades and mirror_degrades

            if all_degrade:
                verification['load_bearing_terms'].append(coeff_name)
                print(f"  ✓ {coeff_name}: load-bearing (all three channels degrade)")
            else:
                degradation = {
                    'mass': mass_degrades,
                    'gravity': gravity_degrades,
                    'mirror': mirror_degrades,
                }
                print(f"  ⚠ {coeff_name}: selective impact {degradation}")
                if (mass_degrades and not gravity_degrades) or (mass_degrades and not mirror_degrades):
                    verification['per_channel_tuning_detected'] = True

        # Overall unification status
        all_present = verification['baseline_channels_present']
        all_load_bearing = len(verification['load_bearing_terms']) == len(self.ablations)
        no_per_channel = not verification['per_channel_tuning_detected']

        if all_present and all_load_bearing and no_per_channel:
            verification['unification_status'] = 'CONFIRMED'
        elif all_present and len(verification['load_bearing_terms']) >= 3:
            verification['unification_status'] = 'STRONG'
        else:
            verification['unification_status'] = 'PARTIAL'

        return verification

    def calibrate_energy_scale(self, target_higgs_mass: float = 125.0,
                              calibration_path: str = 'B') -> Dict:
        """
        Calibrate global energy scale to match experimental constraints.

        Path A: Fix ε_lat from independent observable (e.g., lattice dispersion)
                → predict 125 GeV Higgs mass
        Path B: Use 125 GeV as calibration anchor
                → predict particle spectrum

        Args:
            target_higgs_mass: Target mass for Mirror-Gate Higgs (GeV)
            calibration_path: 'A' (predict from lattice) or 'B' (use as anchor)

        Returns:
            Calibration results and spectrum predictions
        """
        print(f"\nEnergy scale calibration (Path {calibration_path})...")

        if not self.baseline:
            raise ValueError("Must compute baseline first")

        # Current dimensionless energy scale from E_MG
        E_MG_dimensionless = self.baseline['mirror_gate']['E_MG_normalized']

        if E_MG_dimensionless < 1e-10:
            print("⚠ Warning: E_MG is zero or near-zero; cannot calibrate")
            return {
                'path': calibration_path,
                'status': 'BLOCKED',
                'reason': 'E_MG dimensionless value too small',
            }

        if calibration_path == 'B':
            # Use 125 GeV as calibration anchor
            scale_factor = target_higgs_mass / E_MG_dimensionless

            print(f"  Calibration: E_MG = {E_MG_dimensionless:.6f} (dimensionless)")
            print(f"  Target Higgs mass: {target_higgs_mass} GeV")
            print(f"  Scale factor: λ = {scale_factor:.6f}")

            # Predict particle spectrum
            mass_effect = self.baseline['mass_effect']['mass_effect']
            m_eff_physical = mass_effect * scale_factor

            # Simple spectrum prediction: electron, muon, tau based on mass-effect hierarchy
            spectrum = {
                'higgs_mass': target_higgs_mass,
                'scale_factor': float(scale_factor),
                'electron_mass_estimate': float(m_eff_physical * 0.5e-3),  # Placeholder scaling
                'muon_mass_estimate': float(m_eff_physical * 0.1),  # Placeholder
                'tau_mass_estimate': float(m_eff_physical * 1.8),  # Placeholder
            }

            print(f"\n  Predicted spectrum (placeholder scaling):")
            print(f"    e mass: {spectrum['electron_mass_estimate']:.6f} GeV")
            print(f"    μ mass: {spectrum['muon_mass_estimate']:.6f} GeV")
            print(f"    τ mass: {spectrum['tau_mass_estimate']:.6f} GeV")

        elif calibration_path == 'A':
            print(f"  Path A: Requires independent lattice dispersion relation")
            print(f"  (Not yet implemented; waiting for ε_lat input)")
            spectrum = {
                'path': 'A',
                'status': 'PENDING_LATTICE_DATA',
                'current_E_MG': float(E_MG_dimensionless),
            }

        else:
            raise ValueError(f"Unknown calibration path: {calibration_path}")

        return spectrum


def main():
    """Run Phase 5C three-view verification demonstration."""
    print("=" * 70)
    print("Phase 5C: Three-View Verification - Unified Coefficient Set")
    print("=" * 70)
    print()

    # Initialize verifier
    print("1. Initializing three-view verifier...")
    verifier = ThreeViewVerifier()
    print()

    # TEST 1: Native D-409 ground state (K-M coupling only)
    print("=" * 70)
    print("TEST 1: Native D-409 Ground State Profile (K-M only)")
    print("=" * 70)
    print()

    print("2a. Computing baseline with native Z_0...")
    baseline_native = verifier.compute_baseline(synthetic_profile=False)
    print()

    print("3a. Running ablation suite on native profile...")
    ablations_native = verifier.run_ablation_suite()
    print(f"   Ablated {len(ablations_native)} coefficients")
    print()

    print("4a. Verifying unification with native profile...")
    verification_native = verifier.verify_unification()
    print(f"\n   Unification status: {verification_native['unification_status']}")
    print(f"   Load-bearing terms for native: {len(verification_native['load_bearing_terms'])} of {len(ablations_native)}")
    print(f"   Note: Native profile has E=0, T=0 → only K,M coefficients affect output")
    print()

    # TEST 2: Synthetic full-component profile (all K,E,M,T present)
    print("=" * 70)
    print("TEST 2: Synthetic Full-Component Profile (K,E,M,T all present)")
    print("=" * 70)
    print()

    # Reset ablations for new test
    verifier.ablations = {}

    print("2b. Computing baseline with synthetic full-component profile...")
    baseline_synthetic = verifier.compute_baseline(synthetic_profile=True)
    print()

    print("3b. Running ablation suite on synthetic profile...")
    ablations_synthetic = verifier.run_ablation_suite()
    print(f"   Ablated {len(ablations_synthetic)} coefficients")
    print()

    print("4b. Verifying unification with synthetic profile...")
    verification_synthetic = verifier.verify_unification()
    print(f"\n   Unification status: {verification_synthetic['unification_status']}")
    print(f"   Load-bearing terms for synthetic: {len(verification_synthetic['load_bearing_terms'])} of {len(ablations_synthetic)}")
    print(f"   Per-channel tuning: {'DETECTED' if verification_synthetic['per_channel_tuning_detected'] else 'NOT DETECTED'}")
    print()

    # Calibrate energy scale
    print("5. Calibrating energy scale (Path B)...")
    spectrum = verifier.calibrate_energy_scale(target_higgs_mass=125.0, calibration_path='B')
    print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Native D-409 profile: {verification_native['unification_status']}")
    print(f"  → K-M coupling only (E=0, T=0) means s_E, s_T inactive for this state")
    print(f"Synthetic full profile: {verification_synthetic['unification_status']}")
    print(f"  → All coefficients should be load-bearing for general case")
    print()
    print("Ready for Phase 5D: D-416 planetary falsification tests")
    print("=" * 70)


if __name__ == "__main__":
    main()
