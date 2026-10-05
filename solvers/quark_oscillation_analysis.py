#!/usr/bin/env python3
"""
Quark Oscillation Analysis: How Mass-Dependent Oscillations Explain Binding Errors

Core insight from user feedback: "its osscilating at middle its phase shift and 
conncetion. its boundry condtions"

This suggests:
1. Quarks oscillate internally with frequency ω ∝ 1/m (lighter quarks oscillate faster)
2. Oscillation modulates the effective phase-locking configuration
3. Different oscillation frequencies create different time-averaged phase differences
4. This changes the effective binding energy independently of the static phase geometry

The fact that all hadrons have IDENTICAL static phase configuration [0°, 60°, 120°]
but DIFFERENT errors suggests the mechanism is purely dynamic (oscillation frequency dependent).
"""

import sys
sys.path.insert(0, "/home/claude/one-wave-science/solvers")

import numpy as np
from hadron_knot_geometry import create_proton, create_neutron, create_lambda

QUARK_MASSES_MEV = {
    "up": 2.16,
    "down": 4.67,
    "strange": 95.0,
}

# Current predictions vs experimental
EXPERIMENTAL_MASSES = {
    "proton": 938.3,
    "neutron": 939.6,
    "Lambda": 1115.7,
}

PREDICTED_MASSES = {
    "proton": 914.4,
    "neutron": 967.3,
    "Lambda": 1319.2,
}

ERRORS_MEV = {
    "proton": 914.4 - 938.3,      # -23.9 MeV
    "neutron": 967.3 - 939.6,     # +27.7 MeV
    "Lambda": 1319.2 - 1115.7,    # +203.5 MeV
}


def compute_oscillation_frequency(quark_mass_mev):
    """
    Oscillation frequency scales inversely with quark mass.
    
    Light quarks (u, d ~ 2-5 MeV): oscillate FASTER
    Heavy quarks (s ~ 95 MeV): oscillate SLOWER
    
    Physical basis: ω ~ κ_T / m (effective spring constant / mass)
    where κ_T ~ 0.297 GeV is the phase-locking coupling
    """
    hbar_c = 197.3  # MeV·fm
    
    # Phase-locking coupling strength
    kappa_T = 0.297  # GeV = 297 MeV
    
    # Oscillation frequency (energy units)
    # ω = κ_T / m in natural units
    omega = kappa_T * 1000 / quark_mass_mev  # Convert to MeV
    
    return omega


def compute_oscillation_amplitude(quark_mass_mev, boundary_radius_fm=0.85):
    """
    Oscillation amplitude is determined by confinement boundary.
    
    For a quark confined to radius R:
    - Uncertainty principle: Δx·Δp ~ ℏ
    - Δx ~ R → Δp ~ ℏ/R
    - Amplitude A ~ Δp/ω (momentum / frequency)
    
    Heavier quarks: larger amplitude (slower oscillation, larger displacement)
    Lighter quarks: smaller amplitude (faster oscillation, smaller displacement)
    """
    hbar_c = 197.3  # MeV·fm
    
    # Momentum uncertainty from confinement
    delta_p = hbar_c / (2 * boundary_radius_fm)  # ~116 MeV for R=0.85 fm
    
    # Oscillation frequency
    omega = compute_oscillation_frequency(quark_mass_mev)
    
    # Amplitude in phase space
    amplitude = delta_p / omega  # rad/fm
    
    return amplitude, omega, delta_p


def analyze_oscillations():
    """Analyze how quark mass affects oscillation and phase-locking."""
    
    print("="*90)
    print("QUARK OSCILLATION ANALYSIS: Mass-Dependent Phase Modulation")
    print("="*90)
    print()
    
    print("KEY PRINCIPLE:")
    print("-"*90)
    print("Quarks oscillate at frequency ω ∝ κ_T/m")
    print("  Light quarks (u, d): fast oscillation → phases average to smaller difference")
    print("  Heavy quarks (s): slow oscillation → phases maintain larger separation")
    print()
    print("This creates a MASS-DEPENDENT CORRECTION to binding energy.")
    print()
    
    # Analyze each hadron
    hadrons = [
        ("proton", create_proton(), [-23.9, "underpredicted (too strong binding)"]),
        ("neutron", create_neutron(), [+27.7, "overpredicted (too weak binding)"]),
        ("Lambda", create_lambda(), [+203.5, "overpredicted (too weak binding)"]),
    ]
    
    print("DETAILED OSCILLATION ANALYSIS:")
    print("="*90)
    print()
    
    for hadron_name, knot, error_info in hadrons:
        print(f"{hadron_name.upper()}")
        print("-"*90)
        print()
        
        error_mev, error_desc = error_info
        
        # Get quark composition
        masses = []
        avg_mass = 0
        for v in knot.vortices:
            m = QUARK_MASSES_MEV.get(v.flavor, 0)
            masses.append(m)
            avg_mass += m
        avg_mass /= len(masses)
        
        print(f"  Quark composition: {', '.join([f'{v.flavor}({QUARK_MASSES_MEV.get(v.flavor, 0):.1f} MeV)' for v in knot.vortices])}")
        print(f"  Average mass: {avg_mass:.2f} MeV")
        print()
        
        # Compute oscillation parameters for each quark
        print(f"  Oscillation parameters:")
        print(f"  {'Quark':<12} {'Mass (MeV)':>12} {'ω (MeV)':>12} {'Amplitude':>12}")
        print(f"  " + "-"*50)
        
        omegas = []
        amplitudes = []
        
        for v in knot.vortices:
            m = QUARK_MASSES_MEV.get(v.flavor, 0)
            amp, omega, dp = compute_oscillation_amplitude(m)
            omegas.append(omega)
            amplitudes.append(amp)
            
            print(f"  {v.flavor:<12} {m:>12.2f} {omega:>12.2f} {amp:>12.6f}")
        
        print()
        
        # Oscillation frequency dispersion
        omega_min, omega_max = min(omegas), max(omegas)
        omega_ratio = omega_max / omega_min if omega_min > 0 else 1
        
        print(f"  Frequency dispersion:")
        print(f"    ω_min: {omega_min:.2f} MeV (for heaviest quark)")
        print(f"    ω_max: {omega_max:.2f} MeV (for lightest quark)")
        print(f"    Ratio: {omega_ratio:.1f}x")
        print()
        
        # Correlate with error
        print(f"  Prediction error: {error_mev:+.1f} MeV ({error_desc})")
        print()
        
        # Hypothesis: error scales with oscillation frequency dispersion
        # or average mass
        print(f"  Oscillation-error correlation:")
        print(f"    ω_dispersion × avg_mass: {omega_ratio * avg_mass:.2f}")
        print(f"    √(avg_mass): {np.sqrt(avg_mass):.2f}")
        print(f"    1/avg_mass: {1/avg_mass:.4f}")
        print()
    
    print("="*90)
    print("SYSTEMATIC ANALYSIS: Error vs Oscillation Parameters")
    print("="*90)
    print()
    
    # Collect data for correlation analysis
    hadron_data = []
    for hadron_name, knot, error_info in hadrons:
        error_mev, _ = error_info
        
        masses = [QUARK_MASSES_MEV.get(v.flavor, 0) for v in knot.vortices]
        avg_mass = np.mean(masses)
        
        # Compute oscillation parameters
        omegas = [compute_oscillation_frequency(m) for m in masses]
        omega_dispersion = max(omegas) / min(omegas) if min(omegas) > 0 else 1
        
        hadron_data.append({
            "name": hadron_name,
            "error_mev": error_mev,
            "avg_mass": avg_mass,
            "omega_dispersion": omega_dispersion,
            "max_mass": max(masses),
            "mass_range": max(masses) - min(masses),
        })
    
    print("Hypothesis Test: Error ∝ oscillation frequency dispersion")
    print()
    print(f"{'Hadron':<12} {'Error (MeV)':>12} {'ω_dispersion':>15} {'Correlation?':>15}")
    print("-"*60)
    
    for data in hadron_data:
        marker = "***" if abs(data["error_mev"]) > 20 and data["omega_dispersion"] > 100 else "   "
        print(f"{data['name']:<12} {data['error_mev']:>+11.1f} {data['omega_dispersion']:>15.1f} {marker}")
    
    print()
    print("Hypothesis Test: Error ∝ max quark mass")
    print()
    print(f"{'Hadron':<12} {'Error (MeV)':>12} {'Max mass (MeV)':>15} {'Correlation?':>15}")
    print("-"*60)
    
    for data in hadron_data:
        marker = "***" if data["max_mass"] > 80 and abs(data["error_mev"]) > 20 else "   "
        print(f"{data['name']:<12} {data['error_mev']:>+11.1f} {data['max_mass']:>15.1f} {marker}")
    
    print()
    print("="*90)
    print("CONCLUSION")
    print("="*90)
    print()
    
    print("The error pattern suggests:")
    print("1. Light quark systems (proton, neutron): small errors (-2.5% to +2.9%)")
    print("2. Heavy quark systems (Lambda with s quark): large errors (+18.2%)")
    print()
    print("This CORRELATES with quark mass: heavier constituent mass → larger error")
    print()
    print("Next step: Determine exact correction formula")
    print("  ΔE_binding ∝ f(m_avg) or g(m_max) or h(ω_dispersion)")
    print()


if __name__ == "__main__":
    analyze_oscillations()
