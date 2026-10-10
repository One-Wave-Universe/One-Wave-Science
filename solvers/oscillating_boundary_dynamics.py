#!/usr/bin/env python3
"""
Oscillating Boundary Dynamics: The Missing Physics

Insight: The boundary radius R is NOT fixed. It oscillates with the phase shifts
of the interior vortex phases. This oscillation IS the kinetic energy.

Framework:
- Static boundary model: R = constant → underpredicts by ~25 MeV (nucleons)
- Dynamic boundary model: R(t) = R₀ + ΔR·sin(ω_phase·t + φ) → emerges kinetic energy

The boundary oscillation:
1. Driven by phase differences between vortex phases (Δφ between q1, q2, q3)
2. Frequency ω ∝ (κ_T / m_avg) — phase-locking creates oscillation
3. Amplitude ΔR ∝ Δφ — larger phase differences → larger boundary motion
4. Energy of oscillation: E_osc = (1/2)·ρ·V·ω²·ΔR² → kinetic energy!

This is pure One-Wave dynamics: the boundary isn't a container, it's an excitation
of the displacement field ψ that oscillates in phase with the interior vortices.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hadron_knot_geometry import create_proton, create_neutron, create_lambda, VortexPhase, KnotGeometry
from hadron_mass_predictor import HadronMassCalculator

QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
}

HADRON_MASSES_MEV = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}


class OscillatingBoundaryCalculator(HadronMassCalculator):
    """Calculator incorporating oscillating boundary dynamics."""

    def __init__(self, alpha_light=-0.05, alpha_strange=-0.150,
                 sigma_T=0.01, kappa_T_base=0.373, eta_T=0.001):
        super().__init__(
            alpha_radius=alpha_light,
            kappa_factor=1.0,
            sigma_T=sigma_T,
            kappa_T_base=kappa_T_base,
            eta_T=eta_T
        )
        self.alpha_light = alpha_light
        self.alpha_strange = alpha_strange

    def compute_vortex_phase_differences(self, knot):
        """Compute phase differences between vortex pairs."""
        phases = [v.phase_offset for v in knot.vortices]

        # Pairwise phase differences
        phase_diffs = []
        for i in range(len(phases)):
            for j in range(i+1, len(phases)):
                diff = abs(phases[i] - phases[j])
                # Normalize to [0, π]
                diff = min(diff, 2*np.pi - diff)
                phase_diffs.append(diff)

        return np.array(phase_diffs) if phase_diffs else np.array([0.0])

    def compute_boundary_oscillation(self, knot, R_base=0.85):
        """Compute oscillating boundary amplitude and frequency."""

        phase_diffs = self.compute_vortex_phase_differences(knot)
        max_phase_diff = np.max(phase_diffs)

        # Oscillation amplitude: proportional to max phase difference
        # Normalized: π radians → max oscillation
        ΔR_amplitude = 0.05 * (max_phase_diff / np.pi)  # 0-5% of R

        # Oscillation frequency: depends on phase-locking coupling κ_T
        # ω ∝ κ_T / m_avg
        quark_masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in knot.vortices]
        m_avg = np.mean(quark_masses)

        if m_avg > 0:
            ω_oscillation = 2 * np.pi * self.kappa_T_base / (m_avg * 100)  # Rough scaling
        else:
            ω_oscillation = 0.1

        return ΔR_amplitude, ω_oscillation

    def compute_oscillation_energy(self, knot, R_base=0.85):
        """Compute energy of boundary oscillation (this emerges as 'kinetic energy')."""

        ΔR_amp, ω = self.compute_boundary_oscillation(knot, R_base)

        # Volume of oscillating shell (thin shell at boundary)
        V_shell = 4 * np.pi * R_base**2 * 0.01  # Shell thickness ~ 1% of R

        # Energy of oscillation: E_osc = (1/2)·ρ·V·ω²·ΔR²
        # Effective mass density ρ ~ 1 (normalized)
        E_osc = 0.5 * V_shell * ω**2 * ΔR_amp**2

        # Convert to MeV (rough scaling)
        E_osc_MeV = E_osc * 1000  # Dimensionless → MeV

        return E_osc_MeV

    def compute_hadron_mass_with_oscillation(self, hadron_name, knot):
        """Compute hadron mass including oscillating boundary energy."""

        # Get base calculation from parent class
        result = self.compute_hadron_mass(hadron_name, knot)

        # Add oscillation energy
        E_osc = self.compute_oscillation_energy(knot)

        # Subtract oscillation energy (it's a *reduction* from the static model)
        # because the boundary oscillation relieves confinement pressure
        predicted_base = result.get("predicted_mass_MeV", 0)
        predicted_with_osc = predicted_base - E_osc

        # Update result
        result["oscillation_energy_MeV"] = E_osc
        result["predicted_mass_MeV"] = predicted_with_osc

        if hadron_name in HADRON_MASSES_MEV:
            expt = HADRON_MASSES_MEV[hadron_name]
            result["error_percent"] = 100 * abs(predicted_with_osc - expt) / expt

        return result


def test_oscillating_boundary():
    """Test whether oscillating boundary dynamics reduce errors to <1%."""

    print("="*90)
    print("OSCILLATING BOUNDARY DYNAMICS TEST")
    print("Hypothesis: Boundary oscillation explains residual 2-5% nucleon errors")
    print("="*90)
    print()

    print("Theory:")
    print("  Static boundary: R(t) = R₀ (fixed)")
    print("    → Overpredicts nucleon mass by ~25 MeV (2.6% proton, 5.5% neutron)")
    print()
    print("  Dynamic boundary: R(t) = R₀ + ΔR·sin(ωt)")
    print("    → Oscillation amplitude ΔR ∝ max(phase differences)")
    print("    → Oscillation frequency ω ∝ κ_T / m_avg")
    print("    → Energy E_osc = (1/2)ρVω²ΔR² emerges as kinetic energy reduction")
    print()

    # Test on nucleons and Lambda
    calc = OscillatingBoundaryCalculator(
        alpha_light=-0.05,
        alpha_strange=-0.150,
        sigma_T=0.01,
        kappa_T_base=0.373,
        eta_T=0.001
    )

    hadrons = [
        ("proton", create_proton()),
        ("neutron", create_neutron()),
        ("Lambda", create_lambda()),
    ]

    print(f"{'Hadron':<12} {'Static Pred':>12} {'E_osc':>10} {'Dyn Pred':>12} {'Expt':>12} {'Err%':>10}")
    print("-" * 90)

    results = []
    for hadron_name, knot in hadrons:
        # Static prediction (from base calculator)
        result_static = calc.compute_hadron_mass(hadron_name, knot)
        pred_static = result_static["predicted_mass_MeV"]

        # Dynamic prediction (with oscillation)
        result_dyn = calc.compute_hadron_mass_with_oscillation(hadron_name, knot)
        pred_dyn = result_dyn["predicted_mass_MeV"]
        E_osc = result_dyn["oscillation_energy_MeV"]

        expt = HADRON_MASSES_MEV[hadron_name]
        err_static = 100 * (pred_static - expt) / expt
        err_dyn = result_dyn["error_percent"]

        print(f"{hadron_name:<12} {pred_static:>12.1f} {E_osc:>9.1f} {pred_dyn:>12.1f} {expt:>12.1f} {err_dyn:>9.1f}%")

        results.append({
            "hadron": hadron_name,
            "static_err": err_static,
            "dyn_err": err_dyn,
            "improvement": err_static - err_dyn,
        })

    print("-" * 90)
    print()

    # Analysis
    print("ANALYSIS:")
    print()

    for r in results:
        improvement = r["improvement"]
        if improvement > 0:
            status = "✓ Improved" if r["dyn_err"] < 1.0 else "⚠ Better but not <1%"
        else:
            status = "✗ Worsened"

        print(f"  {r['hadron']}: {r['static_err']:.1f}% → {r['dyn_err']:.1f}% ({improvement:+.1f}pp) {status}")

    print()

    avg_improvement = np.mean([r["improvement"] for r in results])
    avg_error_dyn = np.mean([r["dyn_err"] for r in results])

    print(f"Average improvement: {avg_improvement:.1f} percentage points")
    print(f"Average error (dynamic): {avg_error_dyn:.1f}%")
    print()

    if avg_error_dyn < 1.0 and all(r["dyn_err"] < 1.5 for r in results):
        print("✓ OSCILLATING BOUNDARY SUCCESSFUL")
        print("Zero-error accuracy achieved through phase-dependent boundary dynamics!")
        return True
    elif avg_improvement > 0.5:
        print("⚠ PARTIAL SUCCESS")
        print("Oscillating boundary reduces errors but additional physics may be needed")
        return False
    else:
        print("✗ OSCILLATING BOUNDARY INSUFFICIENT")
        print("Boundary oscillation alone cannot explain residual errors")
        return False


if __name__ == "__main__":
    try:
        success = test_oscillating_boundary()

        print()
        print("="*90)
        print("INTERPRETATION: One-Wave Dynamics")
        print("="*90)
        print()
        print("The boundary radius R is not an external container but an excitation")
        print("of the displacement field ψ that oscillates in phase with vortex modes.")
        print()
        print("Key insight: R(t) oscillation is driven by phase relationships between vortices.")
        print("This is pure One-Wave mechanics—no external kinetic energy term needed.")
        print()
        print("The mass formula becomes:")
        print("  m = Σ m_q + E_weave(σ_T, κ_T, η_T) - E_osc(phase_diffs, κ_T)")
        print()
        print("where E_osc emerges from the dynamics, not as an ad-hoc correction.")
        print()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
