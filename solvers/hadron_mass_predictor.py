#!/usr/bin/env python3
"""
Hadron Mass Predictor — Phase 5 Combined Solution Integration

Purpose: Extend hadron knot geometry to predict hadron masses using the
Phase 5 combined solution framework (radius scaling + κ_T scaling).

Framework Integration:
- Phase 5 established: R(m) = 0.35 × m_scale^α and κ_T(m) = 1.5 × factor × √m_scale
- Balanced parameters: α = -0.05, factor = 1.0 (46% improvement on heavy quarks)
- Now apply same physics to hadrons: boundary radius scales with constituent quark content

Key Insight:
- A hadron's boundary radius reflects the spatial distribution of its constituent quarks
- Heavier quarks create smaller confinement regions (radius scaling with α < 0)
- This affects the weave energy and hence the total hadron mass

Mass Formula:
m_hadron = m_constituent_quarks + E_weave + E_binding

where:
- m_constituent_quarks = sum of constituent quark masses
- E_weave = σ_T × Area + κ_T × phase_diff + η_T × vorticity
- E_binding = confinement cost (negative, binding attraction)
"""

import sys
sys.path.insert(0, "/home/claude/one-wave-science/solvers")

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from hadron_knot_geometry import (
    VortexPhase, KnotGeometry, WeaveDensity, WeavingEnergyCalculator,
    KnotLockCalculator, HadronKnotAnalyzer, create_proton, create_neutron,
    create_pion_plus, create_lambda
)


# Quark mass table (from Phase 5 quark mass solver)
QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
    "charm": 1270.0,
    "bottom": 4180.0,
    "top": 172700.0,  # PDG value
}

# Experimental hadron masses (PDG)
HADRON_MASSES_MEV = {
    "proton": 938.3,      # PDG 2024
    "neutron": 939.6,     # PDG 2024
    "Lambda": 1115.7,     # PDG 2024
    "π⁺": 139.6,          # pion (PDG 2024)
    "π⁰": 135.0,          # neutral pion (PDG 2024)
    "K⁺": 493.7,          # kaon (PDG 2024)
    "η": 547.9,           # eta meson (PDG 2024)
}


@dataclass
class HadronMassCalculator:
    """Compute hadron mass using combined solution framework"""

    alpha_radius: float = -0.05        # Phase 5: radius scaling exponent
    kappa_factor: float = 1.0          # Phase 5: κ_T scaling multiplier
    sigma_T: float = 0.01              # Surface tension (GeV/fm²)
    kappa_T_base: float = 1.5          # Base κ_T coupling (GeV)
    eta_T: float = 0.01                # Twist coefficient

    def compute_boundary_radius(self, knot: KnotGeometry,
                               flavor_masses: Optional[Dict[str, float]] = None) -> float:
        """Compute boundary radius with Phase 5 radius scaling.

        For a hadron composed of quarks with flavors f1, f2, f3,
        the effective m_scale is the average mass scale of constituents.

        R(m_scale) = base_radius × m_scale^α

        where m_scale = sqrt(m_q1 × m_q2 × m_q3) / m_up
        """
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        # Extract constituent masses
        masses = []
        for vortex in knot.vortices:
            if vortex.flavor in flavor_masses:
                masses.append(flavor_masses[vortex.flavor])

        if not masses:
            return knot.boundary_radius  # Fallback to default

        # Geometric mean of constituent masses (normalized by up quark)
        geometric_mean = np.prod(masses) ** (1.0 / len(masses))
        m_scale = geometric_mean / flavor_masses["up"]

        # Base radius is empirically 0.85 fm for nucleons
        base_radius = 0.85

        # Phase 5 radius scaling
        if abs(self.alpha_radius) > 1e-6:
            radius = base_radius * (m_scale ** self.alpha_radius)
        else:
            radius = base_radius

        return radius

    def compute_kappa_T(self, knot: KnotGeometry,
                       flavor_masses: Optional[Dict[str, float]] = None) -> float:
        """Compute κ_T with Phase 5 scaling.

        κ_T(m_scale) = 1.5 × factor × √m_scale

        Applied only when radius scaling is active (α ≠ 0).
        """
        if abs(self.alpha_radius) < 1e-6:
            # Baseline (no radius scaling) → constant κ_T
            return 1.0

        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        # Compute m_scale as before
        masses = []
        for vortex in knot.vortices:
            if vortex.flavor in flavor_masses:
                masses.append(flavor_masses[vortex.flavor])

        if not masses:
            return 1.0

        geometric_mean = np.prod(masses) ** (1.0 / len(masses))
        m_scale = geometric_mean / flavor_masses["up"]

        # Phase 5 κ_T scaling
        kappa_T = self.kappa_T_base * self.kappa_factor * np.sqrt(m_scale)

        return kappa_T

    def compute_weave_energy(self, knot: KnotGeometry,
                            flavor_masses: Optional[Dict[str, float]] = None) -> float:
        """Compute total weave energy with scaled parameters.

        E_weave = σ_T × Area + κ_T × phase_diff + η_T × vorticity
        """
        # Update knot radius using combined solution
        knot.boundary_radius = self.compute_boundary_radius(knot, flavor_masses)

        # Create weave density with scaled κ_T
        kappa_T = self.compute_kappa_T(knot, flavor_masses)

        weave = WeaveDensity(
            sigma_T=self.sigma_T,
            kappa_T=kappa_T,
            eta_T=self.eta_T,
            neck_radius=0.1,
            break_threshold=5.0
        )

        weave_calc = WeavingEnergyCalculator(weave)
        total_energy = weave_calc.total_weave_energy(knot)

        return total_energy

    def compute_hadron_mass(self, hadron_name: str,
                           knot: KnotGeometry,
                           flavor_masses: Optional[Dict[str, float]] = None) -> Dict:
        """Compute complete hadron mass including constituents and binding.

        Returns:
            Dict with predicted mass, constituent masses, weave energy, error
        """
        if flavor_masses is None:
            flavor_masses = QUARK_MASSES_MEV

        # Sum constituent quark masses
        constituent_mass = sum(
            flavor_masses.get(v.flavor, 0) for v in knot.vortices
        )

        # Compute weave energy
        weave_energy = self.compute_weave_energy(knot, flavor_masses)

        # Binding energy (negative, attractive)
        # Empirically, nucleon binding ~5-10 MeV for light quarks
        # For mesons, binding ~20-50 MeV
        num_vortices = knot.num_vortices
        if num_vortices == 3:
            # Baryons: 3-quark binding
            binding_energy = -8.0  # MeV (empirical)
        elif num_vortices == 2:
            # Mesons: quark-antiquark binding
            binding_energy = -30.0  # MeV (empirical)
        else:
            binding_energy = 0.0

        # Total mass
        total_mass = constituent_mass + weave_energy * 1000 + binding_energy  # Convert weave to MeV

        # Compute error vs. experimental mass
        if hadron_name in HADRON_MASSES_MEV:
            experimental_mass = HADRON_MASSES_MEV[hadron_name]
            error_mev = abs(total_mass - experimental_mass)
            error_percent = (error_mev / experimental_mass) * 100
        else:
            experimental_mass = None
            error_mev = None
            error_percent = None

        return {
            "hadron_name": hadron_name,
            "num_vortices": num_vortices,
            "constituent_mass_MeV": constituent_mass,
            "weave_energy_MeV": weave_energy * 1000,
            "binding_energy_MeV": binding_energy,
            "predicted_mass_MeV": total_mass,
            "experimental_mass_MeV": experimental_mass,
            "error_MeV": error_mev,
            "error_percent": error_percent,
            "boundary_radius_fm": knot.boundary_radius,
        }


def test_hadron_spectrum():
    """Test hadron mass predictions with Phase 5 combined solution."""

    print("=" * 90)
    print("HADRON MASS PREDICTOR — Phase 5 Combined Solution Integration")
    print("=" * 90)
    print()

    # Initialize calculator with Phase 5 balanced parameters
    calc = HadronMassCalculator(
        alpha_radius=-0.05,
        kappa_factor=1.0,
        sigma_T=0.01,
        kappa_T_base=1.5,
        eta_T=0.01
    )

    print("Phase 5 Parameters:")
    print(f"  α (radius scaling exponent): {calc.alpha_radius}")
    print(f"  κ_T scaling factor: {calc.kappa_factor}")
    print(f"  σ_T (surface tension): {calc.sigma_T} GeV/fm²")
    print(f"  κ_T base coupling: {calc.kappa_T_base} GeV")
    print()

    # Build hadrons
    print("Building hadrons with Phase 5 geometry...")
    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
        ("π⁺", create_pion_plus()),
    ]

    # Predict masses
    print("\nComputing hadron masses...")
    print()

    results = []
    for hadron_name, knot in hadrons:
        result = calc.compute_hadron_mass(hadron_name, knot)
        results.append(result)

    # Report
    print("=" * 90)
    print("HADRON MASS SPECTRUM — Phase 5 Combined Solution")
    print("=" * 90)
    print()

    print(f"{'Hadron':<12} {'Vortices':<10} {'Constituent':<15} {'Weave':<15} {'Binding':<12} {'Total':<12} {'Expt':<12} {'Error%':<10}")
    print("-" * 90)

    for r in results:
        const_m = r["constituent_mass_MeV"]
        weave_m = r["weave_energy_MeV"]
        bind_m = r["binding_energy_MeV"]
        total_m = r["predicted_mass_MeV"]
        expt_m = r["experimental_mass_MeV"] or "—"
        err_pct = f"{r['error_percent']:.1f}%" if r["error_percent"] is not None else "—"

        print(f"{r['hadron_name']:<12} {r['num_vortices']:<10} {const_m:>13.1f} {weave_m:>13.1f} {bind_m:>10.1f} {total_m:>10.1f} {expt_m:>10} {err_pct:>8}")

    print()
    print("=" * 90)
    print("ANALYSIS")
    print("=" * 90)
    print()

    # Compute average error
    errors = [r["error_percent"] for r in results if r["error_percent"] is not None]
    if errors:
        avg_error = np.mean(errors)
        print(f"Average hadron mass error: {avg_error:.1f}%")

    print()
    print("Key Findings:")
    print()

    for r in results:
        print(f"  {r['hadron_name']:12s}: R = {r['boundary_radius_fm']:.3f} fm")

    print()
    print("Comparison with Phase 5 quark results:")
    print("  ✓ Radius scaling (α = -0.05) applied to hadron geometry")
    print("  ✓ κ_T scaling (√m_scale) applied to phase-locking energy")
    print("  ✓ Weave energy computed from C-317 equations")
    print("  ✓ Constituent masses and binding energy included")
    print()

    return results


def test_parameter_sensitivity():
    """Test sensitivity of hadron masses to radius scaling parameter."""

    print("=" * 90)
    print("PARAMETER SENSITIVITY: Radius Scaling Exponent α")
    print("=" * 90)
    print()

    alpha_values = [-0.10, -0.05, 0.0, 0.05]

    print("Testing nucleon masses with different α values...")
    print()

    for alpha in alpha_values:
        calc = HadronMassCalculator(
            alpha_radius=alpha,
            kappa_factor=1.0,
            sigma_T=0.01,
            kappa_T_base=1.5,
            eta_T=0.01
        )

        proton = create_proton()
        proton_result = calc.compute_hadron_mass("proton", proton)

        neutron = create_neutron()
        neutron_result = calc.compute_hadron_mass("neutron", neutron)

        proton_err = proton_result["error_percent"]
        neutron_err = neutron_result["error_percent"]
        avg_err = (proton_err + neutron_err) / 2

        print(f"  α = {alpha:+.2f}: proton {proton_err:>6.1f}%, neutron {neutron_err:>6.1f}%, avg {avg_err:>6.1f}%")

    print()


if __name__ == "__main__":
    try:
        results = test_hadron_spectrum()
        print()
        test_parameter_sensitivity()

        print("=" * 90)
        print("✓ Hadron mass predictor ready for calibration")
        print("=" * 90)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
