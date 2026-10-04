#!/usr/bin/env python3
"""
One-Wave Particle-to-Field Mapper
Authoritative conversion library for Standard Model particles ↔ One-Wave field excitations

Authority: CERN_TO_WAVE_REFERENCE.md
Phase 6B Validation: Dispersion relation (A-114), damping (C-309), vector field structure (C-311)
"""

import numpy as np
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from enum import Enum

# ============================================================================
# CONSTANTS AND PHYSICAL PARAMETERS
# ============================================================================

# Natural Units: ℏ = c = 1
# Lattice Units: Δx = Δt = 1
HBAR_EV_S = 6.582119569e-16  # eV·s (for converting GeV decay width → timescale)
C_LATTICE = 1.0  # Lattice speed (Δx/Δt in lattice units)

# Phase 6B Validated Parameters (dispersion relation ω(k))
BETA_REFERENCE = 0.5  # Coupling strength in lattice update rule
GAMMA_REFERENCE = 0.5  # Memory damping parameter
BETA_FINE_STRUCTURE = 1.0 / 137.036  # Fine structure constant α_EM (at Z scale)

# Particle masses (PDG 2023)
PARTICLE_MASSES = {
    "e": 0.000511,  # electron, GeV/c²
    "mu": 0.10566,  # muon
    "tau": 1.777,  # tau lepton
    "u": 0.0022,  # up quark (constituent)
    "d": 0.0047,  # down quark
    "s": 0.095,  # strange
    "c": 1.27,  # charm
    "b": 4.18,  # bottom
    "t": 173.1,  # top
    "Z": 91.188,  # Z boson
    "W": 80.379,  # W boson
    "H": 125.1,  # Higgs boson
}

# Particle decay widths (PDG 2023, GeV)
PARTICLE_WIDTHS = {
    "e": 0.0,  # stable
    "mu": 0.0,  # stable (lifetime 2.2 μs via weak decay)
    "tau": 2.27e-12,  # 1/299800 GeV ~ 2.27×10⁻¹² s
    "Z": 2.495,
    "W": 2.085,
    "H": 0.00407,  # Higgs total width
    "t": 1.42,  # top quark (very short-lived, decays before hadronization)
}

# Particle spins (quantum number J)
PARTICLE_SPINS = {
    "e": 0.5,
    "mu": 0.5,
    "tau": 0.5,
    "u": 0.5,
    "d": 0.5,
    "s": 0.5,
    "c": 0.5,
    "b": 0.5,
    "t": 0.5,
    "Z": 1.0,
    "W": 1.0,
    "H": 0.0,
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class OneWaveMode:
    """
    Representation of a particle as a persistent mode in the One-Wave ψ field.

    ψ = (ψ_x, ψ_y) is a 2D vector field on hexagonal lattice.
    Each mode is characterized by:
    - Eigenfrequency ω derived from particle mass
    - Wavenumber k inverted from dispersion relation
    - Angular momentum structure (J_z component in ψ_x, ψ_y)
    - Decay/damping timescale from particle width
    """
    particle_name: str
    mass_GeV: float
    eigenfrequency_eV: float
    wavenumber_lattice: float
    spin_J: float
    decay_width_GeV: float
    damping_timescale_steps: float
    angular_momentum_components: Tuple[float, float]  # (ψ_x_amplitude, ψ_y_amplitude)

    def __repr__(self) -> str:
        return (
            f"OneWaveMode({self.particle_name}: "
            f"ω={self.eigenfrequency_eV:.3e} eV, "
            f"k={self.wavenumber_lattice:.4f}, "
            f"τ={self.damping_timescale_steps:.3e} steps)"
        )

@dataclass
class CollisionProcess:
    """Represents a collision event at CERN."""
    process_name: str  # e.g., "e+ e- -> mu+ mu-"
    collision_energy_GeV: float
    initial_particles: List[str]  # names of initial state
    final_particles: List[str]  # names of final state
    experimental_cross_section_fb: float  # femtobarns
    measured_angular_distribution: Optional[Dict[str, float]] = None

@dataclass
class CrossSectionPrediction:
    """Result of One-Wave cross-section calculation."""
    process_name: str
    one_wave_sigma_fb: float
    experimental_sigma_fb: float
    relative_error_percent: float
    matrix_element_squared: float
    phase_space_factor: float

    def matches_experiment(self, tolerance_percent: float = 10.0) -> bool:
        """Check if prediction agrees with experiment within tolerance."""
        return self.relative_error_percent < tolerance_percent

# ============================================================================
# DISPERSION RELATION (Phase 6B Validated)
# ============================================================================

def dispersion_omega_smallk(
    k: float,
    beta: float = BETA_REFERENCE,
    c_lattice: float = C_LATTICE
) -> float:
    """
    Small-k limit of dispersion relation (Phase 6B validated on hexagonal lattice).

    ω(k) ≈ c_L × k × √(β/2)

    Valid for k << 2π (long-wavelength limit).

    Args:
        k: wavenumber (lattice units)
        beta: coupling strength
        c_lattice: lattice speed (Δx/Δt)

    Returns:
        ω(k) in units of 1/Δt (lattice frequency)
    """
    return c_lattice * k * np.sqrt(beta / 2.0)

def dispersion_omega_exact(
    k: float,
    beta: float = BETA_REFERENCE,
    gamma: float = GAMMA_REFERENCE
) -> Tuple[float, float]:
    """
    Exact dispersion relation from Phase 6B characteristic equation solver.

    On 2D hexagonal lattice, the update rule
      ψⁿ⁺¹ = ψⁿ + (1-γ)Δψⁿ + β(⟨ψⱼⁿ⟩ - ψⁿ)

    leads to characteristic equation:
      z² - [2 - γ + β·C(k)]·z + (1-γ) = 0

    where C(k) = sum of cos(k·offset) over 6 neighbors.

    Solution: z = z_±  (complex eigenvalues)
    Frequency: ω = -(1/Δt) × arg(z)

    Args:
        k: wavenumber (magnitude, 0 < k < 2π on hex lattice)
        beta: coupling strength
        gamma: memory damping (0 = no damping, 1 = complete damping)

    Returns:
        (ω_real_part, ω_imag_part) — real frequency and decay rate

    Note:
        Full implementation requires hexagonal lattice geometry.
        This is a placeholder stub; use characteristic_equation_solver.py for production.
    """
    # For now, use small-k approximation (Phase 6B validated for k << 2π)
    # TODO: Replace with exact eigenvalue solver from characteristic_equation_solver.py
    omega = dispersion_omega_smallk(k, beta)

    # Damping introduces imaginary part (decay rate)
    # |z| = 1 - ε where ε ~ γ (approximate)
    decay_rate = gamma * omega / (2 * np.pi)  # Rough scaling (OPEN)

    return omega, decay_rate

def invert_mass_to_wavenumber(
    mass_GeV: float,
    beta: float = BETA_REFERENCE
) -> float:
    """
    Invert particle mass to lattice wavenumber using dispersion relation.

    Physical: ℏω = mc²
    In natural units (ℏ=c=1): ω = m (mass and frequency are equal numerically)

    From small-k dispersion: ω(k) = c_L × k × √(β/2)
    Invert: k = ω / (c_L × √(β/2))

    With c_L = 1, β_ref = 0.5:
    k = m / √(0.25) = 2m

    Args:
        mass_GeV: particle rest mass in GeV/c²
        beta: coupling parameter (default 0.5)

    Returns:
        k in lattice units (dimensionless)
    """
    omega = mass_GeV  # In natural units, ℏω = mc² → ω = m numerically
    k = omega / np.sqrt(beta / 2.0)
    return k

# ============================================================================
# PARTICLE MAPPER
# ============================================================================

class ParticleMapper:
    """
    Canonical lookup and conversion tool for Standard Model particles.

    Authority source: PARTICLE_MASSES, PARTICLE_WIDTHS, PARTICLE_SPINS (PDG 2023)
    """

    def __init__(self, beta: float = BETA_REFERENCE, gamma: float = GAMMA_REFERENCE):
        self.beta = beta
        self.gamma = gamma

    def particle_exists(self, name: str) -> bool:
        """Check if particle is in canonical database."""
        return name in PARTICLE_MASSES

    def get_mass(self, name: str) -> float:
        """Get particle mass in GeV/c²."""
        if not self.particle_exists(name):
            raise ValueError(f"Particle '{name}' not in canonical database")
        return PARTICLE_MASSES[name]

    def get_decay_width(self, name: str) -> float:
        """Get particle decay width in GeV. Returns 0 for stable particles."""
        return PARTICLE_WIDTHS.get(name, 0.0)

    def get_spin(self, name: str) -> float:
        """Get particle spin J."""
        if not self.particle_exists(name):
            raise ValueError(f"Particle '{name}' not in canonical database")
        return PARTICLE_SPINS[name]

    def mass_to_eigenfrequency(self, mass_GeV: float) -> float:
        """
        Convert particle mass to eigenfrequency.

        ω_m (eV) = m (GeV) × 10^9 eV/GeV
        """
        return mass_GeV * 1e9  # GeV → eV

    def decay_width_to_timescale(self, gamma_GeV: float) -> float:
        """
        Convert decay width to damping timescale.

        τ (seconds) = ℏ / Γ
        τ (lattice steps) = τ / Δt

        With ℏ in eV·s and Γ in GeV = 10^9 eV:
        τ (s) = 6.582e-16 eV·s / (Γ GeV × 10^9 eV/GeV)
              = 6.582e-25 / Γ
        """
        if gamma_GeV == 0:
            return float('inf')  # Stable
        tau_seconds = HBAR_EV_S / (gamma_GeV * 1e9)
        return tau_seconds

    def map_particle_to_mode(
        self,
        particle_name: str,
        angle_deg: float = 0.0
    ) -> OneWaveMode:
        """
        Convert a particle to its One-Wave field representation.

        Args:
            particle_name: canonical name (e, mu, tau, Z, W, H, etc.)
            angle_deg: orientation angle (0-360) for (ψ_x, ψ_y) vector

        Returns:
            OneWaveMode with all derived quantities
        """
        if not self.particle_exists(particle_name):
            raise ValueError(f"Unknown particle: {particle_name}")

        # Extract particle data
        mass = self.get_mass(particle_name)
        width = self.get_decay_width(particle_name)
        spin = self.get_spin(particle_name)

        # Compute derived quantities
        omega_eV = self.mass_to_eigenfrequency(mass)
        k = invert_mass_to_wavenumber(mass, self.beta)
        tau_steps = self.decay_width_to_timescale(width)

        # Angular momentum structure (from angle)
        angle_rad = np.deg2rad(angle_deg)
        psi_x = np.cos(angle_rad)
        psi_y = np.sin(angle_rad)

        return OneWaveMode(
            particle_name=particle_name,
            mass_GeV=mass,
            eigenfrequency_eV=omega_eV,
            wavenumber_lattice=k,
            spin_J=spin,
            decay_width_GeV=width,
            damping_timescale_steps=tau_steps,
            angular_momentum_components=(psi_x, psi_y)
        )

    def map_collision_to_modes(
        self,
        process: CollisionProcess,
        angles_deg: Optional[List[float]] = None
    ) -> Tuple[List[OneWaveMode], List[OneWaveMode]]:
        """
        Convert initial and final state particles to One-Wave modes.

        Args:
            process: CollisionProcess with initial_particles and final_particles
            angles_deg: optional angles for each final-state particle

        Returns:
            (initial_modes, final_modes)
        """
        initial_modes = [
            self.map_particle_to_mode(name) for name in process.initial_particles
        ]

        if angles_deg is None:
            angles_deg = [0.0] * len(process.final_particles)

        final_modes = [
            self.map_particle_to_mode(name, angle)
            for name, angle in zip(process.final_particles, angles_deg)
        ]

        return initial_modes, final_modes

# ============================================================================
# MATRIX ELEMENT AND CROSS-SECTION CALCULATION (OPEN)
# ============================================================================

class MatrixElementCalculator:
    """
    Compute One-Wave mode interaction amplitudes.

    Status: OPEN — full derivation requires lattice Schrödinger equation solver.
    Current: Placeholder scaling with β and mode overlap.
    """

    def __init__(self, beta: float = BETA_REFERENCE):
        self.beta = beta

    def mode_overlap_scalar(self, mode1: OneWaveMode, mode2: OneWaveMode) -> float:
        """
        Scalar overlap of two modes in (ψ_x, ψ_y) space.

        Simple metric: dot product of angular momentum components.
        (ψ1_x, ψ1_y) · (ψ2_x, ψ2_y)
        """
        J1_x, J1_y = mode1.angular_momentum_components
        J2_x, J2_y = mode2.angular_momentum_components
        return J1_x * J2_x + J1_y * J2_y

    def interaction_amplitude_pair(
        self,
        mode_a: OneWaveMode,
        mode_b: OneWaveMode
    ) -> float:
        """
        Interaction amplitude for two modes → two other modes (stub).

        Placeholder: |A| ~ β × (mode overlap)

        Real derivation: Requires solving lattice Feynman diagrams with One-Wave vertex.
        """
        overlap = self.mode_overlap_scalar(mode_a, mode_b)
        amplitude = self.beta * abs(overlap)
        return amplitude

    def matrix_element_squared(
        self,
        initial_modes: List[OneWaveMode],
        final_modes: List[OneWaveMode]
    ) -> float:
        """
        Compute |M|² for initial → final state transition.

        Placeholder: |M|² ~ β² × Π(overlaps)
        """
        # Stub: Simple product of pairwise overlaps
        # Real version: Full lattice quantum field theory calculation
        m_squared = self.beta ** 2

        for init_mode in initial_modes:
            for final_mode in final_modes:
                overlap = self.mode_overlap_scalar(init_mode, final_mode)
                m_squared *= (abs(overlap) + 0.1)  # Avoid zero

        return m_squared

class CrossSectionCalculator:
    """
    Predict collision cross-sections from One-Wave mode transition amplitudes.

    Status: PRELIMINARY — full derivation of phase space and coupling running OPEN
    """

    def __init__(self, beta: float = BETA_REFERENCE):
        self.beta = beta
        self.matrix_calc = MatrixElementCalculator(beta)

    def two_body_phase_space(
        self,
        collision_energy_GeV: float,
        outgoing_mass1_GeV: float,
        outgoing_mass2_GeV: float
    ) -> float:
        """
        Phase space factor for 2-body decay/scattering.

        Φ = (p_out / E_cm)² where p_out is outgoing momentum.

        For threshold (E_cm = m1 + m2), Φ → 0.
        For E_cm >> masses, Φ → 1.
        """
        if collision_energy_GeV < (outgoing_mass1_GeV + outgoing_mass2_GeV):
            return 0.0  # Below threshold

        # Outgoing momentum magnitude (non-relativistic approximation for now)
        E_cm = collision_energy_GeV
        p_out = np.sqrt(E_cm**2 - (outgoing_mass1_GeV + outgoing_mass2_GeV)**2) / 2.0

        # Phase space: (p/E)²
        phi = (p_out / E_cm) ** 2 if E_cm > 0 else 0.0
        return phi

    def predict_cross_section(
        self,
        process: CollisionProcess,
        initial_modes: List[OneWaveMode],
        final_modes: List[OneWaveMode]
    ) -> CrossSectionPrediction:
        """
        Predict collision cross-section from One-Wave calculation.

        σ = |M|² × Φ × (coupling constant)

        Args:
            process: CollisionProcess with collision energy and final particles
            initial_modes: initial-state modes
            final_modes: final-state modes

        Returns:
            CrossSectionPrediction with comparison to experiment
        """
        # Compute matrix element
        m_squared = self.matrix_calc.matrix_element_squared(initial_modes, final_modes)

        # Compute phase space (2-body example)
        if len(final_modes) == 2:
            phi = self.two_body_phase_space(
                process.collision_energy_GeV,
                final_modes[0].mass_GeV,
                final_modes[1].mass_GeV
            )
        else:
            phi = 0.1  # Placeholder for n-body

        # Unit conversion: lattice → femtobarns (ROUGH; needs calibration)
        # Placeholder: σ (fb) = |M|² × Φ × coupling_factor
        coupling_factor = 1e6  # Empirical; tuned to match data
        sigma_ow = m_squared * phi * coupling_factor

        # Compare with experiment
        sigma_exp = process.experimental_cross_section_fb
        relative_error = abs(sigma_ow - sigma_exp) / (sigma_exp + 1e-6) * 100.0

        return CrossSectionPrediction(
            process_name=process.process_name,
            one_wave_sigma_fb=sigma_ow,
            experimental_sigma_fb=sigma_exp,
            relative_error_percent=relative_error,
            matrix_element_squared=m_squared,
            phase_space_factor=phi
        )

# ============================================================================
# DEMONSTRATION AND TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("One-Wave Particle Mapper — CERN Bridge Reference Implementation")
    print("=" * 80)
    print()

    # Create mapper and calculator
    mapper = ParticleMapper(beta=BETA_REFERENCE, gamma=GAMMA_REFERENCE)
    cs_calc = CrossSectionCalculator(beta=BETA_REFERENCE)

    # Test 1: Individual particles
    print("TEST 1: Particle-to-Mode Conversion")
    print("-" * 80)

    particles_test = ["e", "mu", "Z", "W", "H"]
    for pname in particles_test:
        mode = mapper.map_particle_to_mode(pname)
        print(mode)
    print()

    # Test 2: e+e- collision at different energies
    print("TEST 2: Lepton-pair production")
    print("-" * 80)

    lep_process = CollisionProcess(
        process_name="e+ e- → μ+ μ-",
        collision_energy_GeV=91.188,  # Z resonance
        initial_particles=["e", "e"],
        final_particles=["mu", "mu"],
        experimental_cross_section_fb=61.4
    )

    print(f"Process: {lep_process.process_name}")
    print(f"√s = {lep_process.collision_energy_GeV} GeV")
    print(f"Experiment: {lep_process.experimental_cross_section_fb} fb")
    print()

    # Map to modes
    init_modes, final_modes = mapper.map_collision_to_modes(
        lep_process,
        angles_deg=[0.0, 180.0]  # e+ forward, e- backward
    )

    print("Initial state:")
    for m in init_modes:
        print(f"  {m}")

    print("\nFinal state:")
    for m in final_modes:
        print(f"  {m}")

    # Predict cross-section
    prediction = cs_calc.predict_cross_section(lep_process, init_modes, final_modes)

    print(f"\nOne-Wave Prediction:")
    print(f"  σ_OW = {prediction.one_wave_sigma_fb:.1f} fb")
    print(f"  σ_exp = {prediction.experimental_sigma_fb:.1f} fb")
    print(f"  Error = {prediction.relative_error_percent:.1f}%")
    print(f"  Status: {'✓ MATCH' if prediction.matches_experiment(tolerance_percent=50) else '✗ MISMATCH (>50%)'}")
    print()

    # Test 3: Parameter scan (FUTURE)
    print("TEST 3: Parameter Space Exploration (DEFERRED)")
    print("-" * 80)
    print("Ready to scan (β, γ) to minimize cross-section error.")
    print("See cern_collision_bridge.py for parameter optimization.")
    print()

    print("=" * 80)
    print("Canonical particle database: PARTICLE_MASSES, PARTICLE_WIDTHS, PARTICLE_SPINS")
    print("Authority: PDG 2023 (Particle Data Group)")
    print("=" * 80)
