#!/usr/bin/env python3
"""
Hadron Knot Geometry Mapper — Three-Vortex Structure and Binding

Purpose: Map the internal geometry of hadrons as bounded three-vortex (or quark-vortex)
knots held together by the Boundary-Tension Weave.

One-Wave Framework (from C-317 and C-318):
- Quarks are Vortex Phases (ψ₁, ψ₂, ψ₃) inside a bounded region Ω_p
- The Boundary-Tension Weave is the 3D surface-volume coupling that holds them
- Confinement is Knot Lock: linear extraction cost τ_T (no falloff)
- Mass emerges from four-interaction carried-pattern resistance

Key insight (from mirrored structure analysis):
- Particles are not fundamental objects
- Particles = peaks and excitation points where mirrored structures interact
- There is ONE wave field ψ; what we call "particles" are standing patterns,
  interference peaks, and resonances in this field's compression/expression cycles
- The "mirror" refers to the reversal structure: particles arise at boundaries
  where the field structure flips from compression to expression (Mirror Gate)

Hadron Classes:
1. BARYONS (3 quarks = 3-vortex knot)
   - Nucleons: proton (uud), neutron (udd)
   - Hyperons: Λ, Σ, Ξ, Ω (with strange, charm, bottom content)
2. MESONS (quark-antiquark = 2-vortex knot)
   - Pions, Kaons, D-mesons, B-mesons

Status: Framework skeleton (C-317 equations)
Gate: YELLOW (geometry simulation pending)
"""

import numpy as np
import json
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


# ============================================================================
# C-317 BOUNDARY-TENSION WEAVE CONSTANTS
# ============================================================================

@dataclass
class WeaveDensity:
    """Surface and volume tension coefficients (C-317)"""
    sigma_T: float = 1.0  # Surface tension (J/m²) — unknown, to be calibrated
    kappa_T: float = 1.0  # Phase-locking coupling (unknown)
    eta_T: float = 1.0    # Twist/vorticity coefficient (unknown)

    # Confinement parameters
    neck_radius: float = 0.1  # Neck radius when quark extracted (unknown)
    break_threshold: float = 5.0  # Energy above which neck breaks (unknown)


# ============================================================================
# VORTEX PHASE REPRESENTATION
# ============================================================================

@dataclass
class VortexPhase:
    """One component of a multi-vortex knot"""
    label: str              # "q1", "q2", "q3" for three-vortex
    flavor: str             # "up", "down", "strange", "charm", etc.
    color: str              # "red", "green", "blue" (gauge color charge)

    # Spatial distribution (spherical harmonics)
    amplitude: float        # A_ℓm (relative magnitude)
    ell: int                # Angular momentum quantum number
    em: int                 # Magnetic quantum number

    # Phase structure
    phase_offset: float     # Global phase rotation

    def spherical_harmonic(self, theta: float, phi: float) -> complex:
        """Evaluate Y_ℓm at (θ, φ) — simplified approximation

        Full spherical harmonic includes Legendre polynomials,
        but for framework purposes we use normalized geometric form
        """
        # Simplified form: angular momentum contribution
        # Y_ℓm ∝ exp(i*m*φ) * Legendre(ℓ, cos θ)

        # Simple normalized version
        if self.ell == 0 and self.em == 0:
            # s-wave (isotropic)
            return self.amplitude / np.sqrt(4 * np.pi) * np.exp(1j * self.phase_offset)
        elif self.ell == 1:
            # p-wave (dipole-like)
            if self.em == 0:
                return self.amplitude * np.cos(theta) * np.exp(1j * self.phase_offset) / 2
            elif self.em == 1:
                return self.amplitude * np.sin(theta) * np.exp(1j * phi) * np.exp(1j * self.phase_offset) / 2
            elif self.em == -1:
                return self.amplitude * np.sin(theta) * np.exp(-1j * phi) * np.exp(1j * self.phase_offset) / 2

        return self.amplitude * np.exp(1j * self.phase_offset)


@dataclass
class KnotGeometry:
    """Three-vortex (or multi-vortex) bounded knot"""
    name: str                               # "proton", "neutron", etc.
    boundary_radius: float = 1.0            # R_p (fm)
    vortices: List[VortexPhase] = field(default_factory=list)

    # Configuration energies (C-317)
    E_skin: float = 0.0                     # Surface energy (σ_T * Area)
    E_phase: float = 0.0                    # Phase-locking energy
    E_twist: float = 0.0                    # Vorticity energy
    E_total: float = 0.0                    # Total weave energy

    def add_vortex(self, vortex: VortexPhase):
        """Add a vortex phase to the knot"""
        self.vortices.append(vortex)

    @property
    def num_vortices(self) -> int:
        return len(self.vortices)

    @property
    def boundary_area(self) -> float:
        """Surface area of spherical boundary"""
        return 4 * np.pi * self.boundary_radius**2


# ============================================================================
# WEAVE ENERGY CALCULATION (C-317)
# ============================================================================

class WeavingEnergyCalculator:
    """Compute Boundary-Tension Weave energy for bounded knot"""

    def __init__(self, density: WeaveDensity):
        self.density = density

    def surface_energy(self, boundary_area: float) -> float:
        """E_skin = σ_T * ∫ dA

        For spherical boundary with radius R:
        E_skin = σ_T * 4π * R²
        """
        return self.density.sigma_T * boundary_area

    def phase_locking_energy(self, vortices: List[VortexPhase],
                            boundary_radius: float,
                            num_sample_points: int = 100) -> float:
        """E_phase = (κ_T/2) * Σ_{a<b} ∫ |ψ_a - ψ_b|² dV

        Simplified: sample phase difference on a grid inside the sphere
        """
        energy = 0.0

        # Monte Carlo sampling inside sphere
        np.random.seed(42)

        for idx in range(num_sample_points):
            # Random point inside sphere
            r = boundary_radius * np.random.uniform(0, 1)**(1/3)
            theta = np.arccos(np.random.uniform(-1, 1))
            phi = np.random.uniform(0, 2*np.pi)

            # Pairwise phase differences
            for i in range(len(vortices)):
                for j in range(i+1, len(vortices)):
                    psi_i = vortices[i].spherical_harmonic(theta, phi)
                    psi_j = vortices[j].spherical_harmonic(theta, phi)
                    phase_diff = abs(psi_i - psi_j)**2
                    energy += phase_diff

        # Volume element (normalize by sphere volume)
        volume = (4/3) * np.pi * boundary_radius**3
        energy *= self.density.kappa_T * volume / num_sample_points

        return energy

    def twist_energy(self, vortices: List[VortexPhase],
                    boundary_radius: float) -> float:
        """E_twist = (η_T/2) * Σ_a ∫ |∇ × v_a|² dV

        Simplified: vorticity estimated from phase gradient
        For Y_ℓm, typical vorticity scales as ℓ(ℓ+1)/R²
        """
        energy = 0.0
        volume = (4/3) * np.pi * boundary_radius**3

        for vortex in vortices:
            # Vorticity scale from angular momentum
            vorticity_scale = vortex.ell * (vortex.ell + 1) / boundary_radius**2
            energy += vorticity_scale

        energy *= self.density.eta_T * volume / len(vortices)

        return energy

    def total_weave_energy(self, knot: KnotGeometry) -> float:
        """Compute complete weave energy: E_weave = E_skin + E_phase + E_twist"""
        E_skin = self.surface_energy(knot.boundary_area)
        E_phase = self.phase_locking_energy(knot.vortices, knot.boundary_radius)
        E_twist = self.twist_energy(knot.vortices, knot.boundary_radius)

        knot.E_skin = E_skin
        knot.E_phase = E_phase
        knot.E_twist = E_twist
        knot.E_total = E_skin + E_phase + E_twist

        return knot.E_total


# ============================================================================
# CONFINEMENT: KNOT LOCK AND EXTRACTION COST
# ============================================================================

class KnotLockCalculator:
    """Calculate extraction cost and confinement strength (C-317 §4)"""

    def __init__(self, density: WeaveDensity):
        self.density = density

    def line_tension(self) -> float:
        """Effective line tension τ_T = 2π * a * σ_T

        where a is the neck radius when a quark is extracted
        """
        return 2 * np.pi * self.density.neck_radius * self.density.sigma_T

    def neck_energy(self, separation: float) -> float:
        """Energy of extraction vs. separation

        E_neck(L) = τ_T * L (linear confinement)
        """
        tau_T = self.line_tension()
        return tau_T * separation

    def extraction_force(self) -> float:
        """Force resisting quark extraction

        F_lock = dE_neck/dL = τ_T (constant, no falloff)
        """
        return self.line_tension()

    def break_separation(self) -> float:
        """Separation at which neck breaks and hadron reweaves

        L_break = E_break / τ_T
        """
        tau_T = self.line_tension()
        if tau_T == 0:
            return float('inf')
        return self.density.break_threshold / tau_T


# ============================================================================
# HADRON FACTORY: Build Standard Hadrons
# ============================================================================

def create_proton() -> KnotGeometry:
    """Proton: u, u, d quarks in 3-vortex knot

    Quark content: |uud⟩ (2 up, 1 down)
    Angular momentum: typically J^PC = 1/2^++
    """
    proton = KnotGeometry(name="proton", boundary_radius=0.8)  # ~0.8 fm

    # Three vortex phases for (u, u, d)
    q1 = VortexPhase(label="q1", flavor="up", color="red",
                     amplitude=1.0, ell=1, em=0, phase_offset=0.0)
    q2 = VortexPhase(label="q2", flavor="up", color="green",
                     amplitude=1.0, ell=1, em=1, phase_offset=np.pi/3)
    q3 = VortexPhase(label="q3", flavor="down", color="blue",
                     amplitude=1.0, ell=1, em=-1, phase_offset=2*np.pi/3)

    proton.add_vortex(q1)
    proton.add_vortex(q2)
    proton.add_vortex(q3)

    return proton


def create_neutron() -> KnotGeometry:
    """Neutron: u, d, d quarks in 3-vortex knot

    Quark content: |udd⟩ (1 up, 2 down)
    Angular momentum: typically J^PC = 1/2^++
    """
    neutron = KnotGeometry(name="neutron", boundary_radius=0.85)  # ~0.85 fm

    # Three vortex phases for (u, d, d)
    q1 = VortexPhase(label="q1", flavor="up", color="red",
                     amplitude=1.0, ell=1, em=0, phase_offset=0.0)
    q2 = VortexPhase(label="q2", flavor="down", color="green",
                     amplitude=1.0, ell=1, em=1, phase_offset=np.pi/3)
    q3 = VortexPhase(label="q3", flavor="down", color="blue",
                     amplitude=1.0, ell=1, em=-1, phase_offset=2*np.pi/3)

    neutron.add_vortex(q1)
    neutron.add_vortex(q2)
    neutron.add_vortex(q3)

    return neutron


def create_lambda() -> KnotGeometry:
    """Λ hyperon: u, d, s quarks (contains strange quark)

    Quark content: |uds⟩
    Angular momentum: typically J^PC = 1/2^+
    """
    lam = KnotGeometry(name="Lambda", boundary_radius=0.8)

    q1 = VortexPhase(label="q1", flavor="up", color="red",
                     amplitude=1.0, ell=1, em=0, phase_offset=0.0)
    q2 = VortexPhase(label="q2", flavor="down", color="green",
                     amplitude=1.0, ell=1, em=1, phase_offset=np.pi/3)
    q3 = VortexPhase(label="q3", flavor="strange", color="blue",
                     amplitude=1.0, ell=1, em=-1, phase_offset=2*np.pi/3)

    lam.add_vortex(q1)
    lam.add_vortex(q2)
    lam.add_vortex(q3)

    return lam


def create_pion_plus() -> KnotGeometry:
    """π⁺ meson: u, d̄ (quark-antiquark 2-vortex knot)

    Quark content: |ud̄⟩
    Angular momentum: typically J^PC = 0^-+
    """
    pion = KnotGeometry(name="π⁺", boundary_radius=0.4)  # ~0.4 fm (smaller than nucleon)

    # Two vortex phases
    q1 = VortexPhase(label="q1", flavor="up", color="red",
                     amplitude=1.0, ell=0, em=0, phase_offset=0.0)
    q2 = VortexPhase(label="q2", flavor="down", color="red",  # Antiquark (same color for pair)
                     amplitude=1.0, ell=0, em=0, phase_offset=np.pi)  # Opposite phase

    pion.add_vortex(q1)
    pion.add_vortex(q2)

    return pion


# ============================================================================
# ANALYSIS AND REPORTING
# ============================================================================

class HadronKnotAnalyzer:
    """Analyze and report on hadron knot geometry"""

    def __init__(self, weave_density: WeaveDensity):
        self.weave_calc = WeavingEnergyCalculator(weave_density)
        self.knot_lock = KnotLockCalculator(weave_density)

    def analyze_hadron(self, knot: KnotGeometry) -> Dict:
        """Complete analysis of a hadron's knot geometry"""

        # Compute energies
        total_energy = self.weave_calc.total_weave_energy(knot)

        # Confinement properties
        line_tension = self.knot_lock.line_tension()
        extraction_force = self.knot_lock.extraction_force()
        break_sep = self.knot_lock.break_separation()

        # Vortex configuration
        vortex_info = []
        for v in knot.vortices:
            vortex_info.append({
                "label": v.label,
                "flavor": v.flavor,
                "color": v.color,
                "angular_momentum": f"ℓ={v.ell}, m={v.em}",
            })

        return {
            "hadron_name": knot.name,
            "num_vortices": knot.num_vortices,
            "boundary_radius_fm": knot.boundary_radius,
            "boundary_area": knot.boundary_area,
            "vortex_phases": vortex_info,
            "weave_energy": {
                "surface_MeV": knot.E_skin * 1000,  # Convert to MeV
                "phase_locking_MeV": knot.E_phase * 1000,
                "twist_MeV": knot.E_twist * 1000,
                "total_MeV": knot.E_total * 1000,
            },
            "confinement": {
                "line_tension_MeV_fm": line_tension * 1000,
                "extraction_force_MeV_fm": extraction_force * 1000,
                "break_separation_fm": break_sep,
            },
        }

    def report(self, analyses: List[Dict]) -> str:
        """Generate human-readable report"""

        report = """
╔════════════════════════════════════════════════════════════════╗
║           HADRON KNOT GEOMETRY MAPPING REPORT                  ║
║  Three-Vortex Structure and Boundary-Tension Weave            ║
║              (Framework from C-317, C-318)                     ║
╚════════════════════════════════════════════════════════════════╝

ONE-WAVE HADRON PICTURE:
  - Hadrons = bounded recurrent 3D knots of vortex phases
  - Quarks = Vortex Phases (ψ_a)
  - Gluons = Boundary-Tension Weave excitations (tension-links)
  - Confinement = Knot Lock (linear extraction cost)
  - Mass = four-interaction carried-pattern resistance

"""

        for analysis in analyses:
            report += f"\n{'='*70}\n"
            report += f"HADRON: {analysis['hadron_name'].upper()}\n"
            report += f"{'='*70}\n"
            report += f"  Vortex configuration: {analysis['num_vortices']}-vortex knot\n"
            report += f"  Boundary radius: {analysis['boundary_radius_fm']:.2f} fm\n"
            report += f"  Boundary area: {analysis['boundary_area']:.3f} fm²\n\n"

            report += f"VORTEX PHASES:\n"
            for vortex in analysis['vortex_phases']:
                report += f"  {vortex['label']:3s}: {vortex['flavor']:8s} "
                report += f"({vortex['color']:5s}) {vortex['angular_momentum']}\n"

            report += f"\nBOUNDARY-TENSION WEAVE ENERGY:\n"
            we = analysis['weave_energy']
            report += f"  Surface (skin):      {we['surface_MeV']:10.2f} MeV\n"
            report += f"  Phase-locking:       {we['phase_locking_MeV']:10.2f} MeV\n"
            report += f"  Twist/vorticity:     {we['twist_MeV']:10.2f} MeV\n"
            report += f"  ─────────────────────────────────\n"
            report += f"  TOTAL WEAVE:         {we['total_MeV']:10.2f} MeV\n"

            report += f"\nCONFINEMENT (KNOT LOCK):\n"
            conf = analysis['confinement']
            report += f"  Line tension τ_T:    {conf['line_tension_MeV_fm']:10.2f} MeV/fm\n"
            report += f"  Extraction force:    {conf['extraction_force_MeV_fm']:10.2f} MeV/fm\n"
            report += f"  Break separation:    {conf['break_separation_fm']:10.2f} fm\n"
            report += f"  Character: LINEAR (no falloff)\n"

        report += f"\n{'='*70}\n"
        report += f"STATUS: Framework deployed\n"
        report += f"Gate: YELLOW (calibration tuning, eigenmode spectrum pending)\n"
        report += f"{'='*70}\n"

        return report


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Build and analyze standard hadrons"""

    print("="*70)
    print("HADRON KNOT GEOMETRY MAPPER v1.0")
    print("One-Wave Three-Vortex Topology")
    print("="*70)
    print()

    # Initialize weave density (to be calibrated)
    weave = WeaveDensity(
        sigma_T=0.01,    # Surface tension (to be calibrated)
        kappa_T=0.01,    # Phase-locking (to be calibrated)
        eta_T=0.01,      # Twist term (to be calibrated)
        neck_radius=0.1,
        break_threshold=5.0
    )

    analyzer = HadronKnotAnalyzer(weave)

    # Build standard hadrons
    print("Building hadron knot geometries...\n")

    hadrons = [
        create_proton(),
        create_neutron(),
        create_lambda(),
        create_pion_plus(),
    ]

    # Analyze each
    analyses = []
    for hadron in hadrons:
        analysis = analyzer.analyze_hadron(hadron)
        analyses.append(analysis)

    # Report
    print(analyzer.report(analyses))

    # Save results
    print("\nSaving results to disk...")

    output = {
        "weave_parameters": {
            "sigma_T": weave.sigma_T,
            "kappa_T": weave.kappa_T,
            "eta_T": weave.eta_T,
            "neck_radius": weave.neck_radius,
            "break_threshold": weave.break_threshold,
        },
        "hadrons_analyzed": len(hadrons),
        "hadron_analyses": analyses,
        "gate": "YELLOW (calibration pending)",
        "open_items": [
            "Calibrate weave density parameters from QCD data",
            "Compute full eigenmode spectrum (gluon spectrum)",
            "Match Tension-Link excitations to measured gluon observables",
            "Derive Boundary Reweaving rates and hadronization products",
            "Test stability under perturbations (Monte Carlo simulation)",
            "Compare confinement force τ_T to lattice QCD measurements",
            "Extend to exotic hadrons (pentaquarks, tetraquarks)",
        ]
    }

    with open("/home/claude/one-wave-science/solvers/hadron_knot_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✓ Results saved to hadron_knot_results.json")


if __name__ == "__main__":
    main()
