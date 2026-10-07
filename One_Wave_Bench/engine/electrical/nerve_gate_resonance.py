#!/usr/bin/env python3
"""
Nerve-Gated Resonance Tuner: Feedback-based three-phase gate control

Implements bidirectional analog gate control with resonance tuning:
- 3:1 nerve gating (P/I/D feedback)
- 3 mirrored mirror gates (120° phase offset)
- 6:1 supervisor override
- Resonance tracking (ω₀ from lattice β, γ parameters)
- Virtual bus state unified view

Core principle:
  Gates drive rotating Maxwell field → Lattice ψ resonates
  Resonance feedback → Nerve gates tune frequency to ω₀
  Result: Active energy coupling at natural frequency
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional, Callable
from enum import Enum
import math
from datetime import datetime


class AlgorithmZeroPhase(Enum):
    """Algorithm Zero six-step recursive choice structure."""
    BEGIN = 0      # Initialize, gather options
    MOVE_1 = 1     # First binary choice
    HOLD = 2       # Commit choice, establish reference
    MOVE_2 = 3     # Verify or pivot
    BREAK = 4      # Resolve, close loop
    REPEAT = 5     # Recurse to next level


# Legacy alias for compatibility
SixStepPhase = AlgorithmZeroPhase


@dataclass
class ResonanceState:
    """Lattice resonance properties and current state."""
    # Lattice parameters (from One-Wave update rule)
    beta: float = 0.5  # Coupling strength to neighborhood
    gamma: float = 0.1  # Damping factor (should be small for resonance)
    c_L: float = 1.0  # Lattice constant/propagation constant
    k: float = 0.5  # Wavenumber (related to physical scale)

    # Calculated resonant frequency
    omega_0: float = field(default=0.0)  # Target resonant frequency (rad/s)

    # Current operating point
    omega_gate: float = 0.0  # Current gate rotation frequency
    frequency_error: float = 0.0  # |omega_0 - omega_gate|
    phase_offset: float = 0.0  # Current phase offset from optimal

    # Energy state
    resonance_amplitude: float = 0.0  # ψ peak amplitude
    energy_circulating: float = 0.0  # Energy flow in rotating field
    q_factor: float = 1.0  # Quality factor (resonance sharpness)

    def __post_init__(self):
        """Calculate resonant frequency from lattice parameters."""
        # ω₀ = c_L · k · √(β/2)
        self.omega_0 = self.c_L * self.k * math.sqrt(self.beta / 2.0)
        # Q-factor: how well resonance is maintained (inverse of damping)
        self.q_factor = 1.0 / (self.gamma + 1e-6)


@dataclass
class NerveSignals:
    """Three-signal nerve feedback for 3:1 gating."""
    proportional: float = 0.0  # P: frequency error (ω₀ - ω_gate)
    integral: float = 0.0  # I: accumulated frequency error over time
    derivative: float = 0.0  # D: rate of frequency change

    # Physical meaning
    v_0_error: float = 0.0  # Virtual ground voltage error
    v_0_rate: float = 0.0  # Rate of V_0 change (dV_0/dt)
    v_0_integral: float = 0.0  # Accumulated V_0 error


@dataclass
class VirtualBusState:
    """Unified system state accessible to all control levels.

    Implements four-views-up / four-actions-down architecture with M-level recursion:
    - M1 (Point): Individual node voltage (V_0)
    - M2 (Path): Gate voltage control (three phases)
    - M3 (Field): Lattice resonance and energy circulation
    - M4 (Supervisor): Six-step Algorithm Zero orchestration
    """
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    time_us: float = 0.0

    # M1: Point-level (Node voltages)
    v_0: float = 2.5  # Virtual ground voltage (point center)
    v_0_prev: float = 2.5  # Previous V_0 (for derivative)

    # M2: Path-level (Gate control addressing)
    gate_voltages: Dict[str, float] = field(default_factory=dict)  # {mosfet_id: voltage}
    gate_frequencies: Dict[str, float] = field(default_factory=dict)  # {phase: omega}

    # M3: Field-level (Resonance and energy state)
    resonance: ResonanceState = field(default_factory=ResonanceState)
    field_amplitude: float = 0.0  # Rotating field amplitude

    # M4: Supervisor-level (Algorithm Zero recursion)
    current_step: AlgorithmZeroPhase = AlgorithmZeroPhase.BEGIN
    step_counter: int = 0

    # Cross-level nerve signals (feedback flowing up from M1 → M4)
    nerve: NerveSignals = field(default_factory=NerveSignals)


class ThreeMirroredGate:
    """
    Three-phase gate with mirrored control law using Algorithm Zero structure.

    Single control law mirrored at three 120° phase offsets:
    - U phase: 0°
    - V phase: 120°
    - W phase: 240°

    Each phase implements Algorithm Zero HOLD state with circle-of-fifths-like
    asymmetric offset windows to preserve identity through transposition.
    """

    def __init__(self, phase_offset_deg: float = 0.0):
        """
        Args:
            phase_offset_deg: Phase offset in degrees (0, 120, or 240)
        """
        self.phase_offset = math.radians(phase_offset_deg)
        # Biological nerve signaling: -70mV resting → +30mV action potential
        # Operating range: 0 to ~100mV (millivolts), matching biological scales
        self.v_center = 0.05  # 50 mV center (millivolt scale) = Algorithm Zero CENTER
        self.v_max = 0.10    # 100 mV maximum (biological resting-to-action range)
        self.v_min = 0.0     # 0 mV minimum

        # Biological operating window (asymmetric for stability, wide for control range)
        # Covers full biological range: resting potential to action potential
        # -70mV → 0V, +30mV → 0.1V, total swing ~100mV
        self.v_floor = 0.0   # 0 mV floor (resting potential mapped to 0V)
        self.v_ceiling = 0.10  # 100 mV ceiling (action potential mapped to 0.1V)

        # PID gains tuned for volt-scale errors, producing biological-scale gate modulation
        # Gate modulation range: ±0.05V around 50mV center (total 0-100mV)
        # For 10mV V_0 error (0.01V): desire ~2-3mV gate swing (weak feedback)
        # K_p = 0.2 / 0.01 = 0.2 (weak proportional response for stability)
        # Reduced gains 7-10x to allow slower feedback response
        self.K_p = 0.15   # Proportional gain (very weak, let system settle)
        self.K_i = 0.01   # Integral gain (slow accumulation)
        self.K_d = 0.03   # Derivative gain (light damping)

    def compute_gate_voltage(self,
                            proportional: float,
                            integral: float,
                            derivative: float) -> float:
        """
        Compute mirrored gate voltage for this phase.

        Control law (Algorithm Zero HOLD state):
          V_gate = V_center + K_p*freq_error + K_i*integral + K_d*derivative

        Then rotate by phase_offset to create three-phase mirror.
        Asymmetric window (circle-of-fifths like) preserves control identity.
        """
        # Compute control signal (proportional + integral + derivative)
        # Note: proportional is the frequency_error passed in (already computed in extract_feedback)
        # We don't use the frequency_error parameter again—it would double-count
        control = self.K_p * proportional + self.K_i * integral + self.K_d * derivative

        # Apply phase rotation (mirror the response across three phases)
        phase_response = control * math.cos(self.phase_offset)

        # Convert to gate voltage
        v_gate = self.v_center + phase_response

        # Clamp to biological window [0.0, 0.1]V
        v_gate = max(self.v_floor, min(self.v_ceiling, v_gate))

        # As fallback, clamp to absolute limits (should be redundant)
        return max(self.v_min, min(self.v_max, v_gate))


class NerveGateResonanceTuner:
    """
    Bidirectional nerve-gated resonance tuning system.

    Architecture:
    - 4 Views Up: Field → Circuit → Gate → Supervisor
    - 4 Actions Down: Feedback extract → Gate synthesis → Output → Override
    - 5 State/Scale: Spatial, Temporal, Magnitude, Energy, Information
    - 3 Mirrored gates with 3:1 feedback
    - 6:1 Supervisor oversight
    - Resonance tracking (ω₀)
    """

    def __init__(self, resonance_params: Optional[Dict] = None):
        """
        Initialize resonance tuner.

        Args:
            resonance_params: Dict with beta, gamma, c_L, k parameters
        """
        self.resonance = ResonanceState(**(resonance_params or {}))
        self.virtual_bus = VirtualBusState()

        # Three mirrored gates at 120° intervals
        self.gates = {
            "U": ThreeMirroredGate(phase_offset_deg=0.0),
            "V": ThreeMirroredGate(phase_offset_deg=120.0),
            "W": ThreeMirroredGate(phase_offset_deg=240.0),
        }

        # Nerve signal accumulation
        self.integral_error = 0.0
        self.prev_frequency_error = 0.0
        self.prev_v_0 = 2.5

        # Supervisor state (6:1 hierarchy)
        self.supervisor_phase = SixStepPhase.BEGIN
        self.phase_counter = 0
        self.allow_override = True

    def extract_feedback(self, v_0: float, dt_s: float) -> NerveSignals:
        """
        Extract three-signal nerve feedback from V_0.

        Signals:
        - P: Frequency error (V_0 deviation from target)
        - I: Accumulated error (integral for lock)
        - D: Rate of change (derivative for damping)

        Note: Error signals are measured in volts. Gate scaling to biological range
        (0-100 mV) happens in compute_gate_voltages(), not here.
        """
        # Calculate virtual ground error (in volts)
        v_target = 2.5
        v_0_error = v_0 - v_target

        # Proportional: V_0 error in volts
        # No scaling here; PID gains will scale to appropriate control magnitude
        frequency_error = v_0_error

        # Integral: accumulate error over time
        self.integral_error += frequency_error * dt_s

        # Derivative: rate of V_0 change
        v_0_rate = (v_0 - self.prev_v_0) / dt_s if dt_s > 0 else 0.0
        self.prev_v_0 = v_0

        derivative = v_0_rate

        return NerveSignals(
            proportional=frequency_error,
            integral=self.integral_error,
            derivative=derivative,
            v_0_error=v_0_error,
            v_0_rate=v_0_rate,
            v_0_integral=self.integral_error
        )

    def compute_gate_voltages(self, nerve: NerveSignals) -> Dict[str, float]:
        """
        Compute three-phase gate voltages using 3:1 nerve gating.

        Single nerve signal (3 components) drives three mirrored gates.
        Uses V_0 feedback error (extracted as P/I/D).
        """
        voltages = {}
        mosfet_map = {
            "U": ("M_U_high", "M_U_low"),
            "V": ("M_V_high", "M_V_low"),
            "W": ("M_W_high", "M_W_low"),
        }

        for phase, (high_mosfet, low_mosfet) in mosfet_map.items():
            v_gate = self.gates[phase].compute_gate_voltage(
                proportional=nerve.proportional,
                integral=nerve.integral,
                derivative=nerve.derivative
            )
            # Apply same voltage to high and low sides for symmetric operation
            voltages[high_mosfet] = v_gate
            voltages[low_mosfet] = v_gate

        return voltages

    def supervisor_override(self, voltages: Dict[str, float]) -> Dict[str, float]:
        """
        6:1 supervisor can override direct gate control.

        Supervisor operates at six-step level, can interrupt gate control
        for safety, phase sequencing, or energy constraints.
        """
        if not self.allow_override:
            return voltages

        # Limit maximum voltage change between steps
        # At biological scales (0-100mV), this prevents wild swings
        max_v_change = 0.02  # 20 mV per timestep (biological rate limit)

        for mosfet_id, v_desired in list(voltages.items()):
            # Default to 50mV center (not 2.5V!) if gate voltage not yet set
            v_current = self.virtual_bus.gate_voltages.get(mosfet_id, 0.05)
            v_change = v_desired - v_current

            if abs(v_change) > max_v_change:
                # Supervisor limits rate of change
                sign = 1 if v_change > 0 else -1
                v_desired = v_current + sign * max_v_change
                voltages[mosfet_id] = v_desired

        return voltages

    def update_resonance_state(self, v_0: float, dt_s: float):
        """Update internal resonance tracking."""
        # Update current frequency error
        self.resonance.frequency_error = abs(self.resonance.omega_0 - self.resonance.omega_gate)

        # Update resonance amplitude based on V_0
        self.resonance.resonance_amplitude = abs(v_0 - 2.5)

        # Simple energy model: amplitude² proportional to energy
        self.resonance.energy_circulating = self.resonance.resonance_amplitude ** 2

    def step(self, v_0: float, dt_s: float) -> Dict[str, float]:
        """
        Execute one control step.

        Returns:
            Dict of {mosfet_id: gate_voltage}
        """
        # Step 1: Extract feedback (4 Actions Down - Feedback extract)
        nerve = self.extract_feedback(v_0, dt_s)
        self.virtual_bus.nerve = nerve

        # Step 2: Gate synthesis (4 Actions Down - Gate synthesis)
        gate_voltages = self.compute_gate_voltages(nerve)

        # Step 3: Supervisor override (6:1 hierarchy)
        gate_voltages = self.supervisor_override(gate_voltages)

        # Step 4: Update state tracking (4 Actions Down - Output)
        self.virtual_bus.gate_voltages = gate_voltages
        self.virtual_bus.v_0 = v_0
        self.update_resonance_state(v_0, dt_s)

        return gate_voltages


# Example usage and testing
if __name__ == "__main__":
    print("="*70)
    print("NERVE-GATED RESONANCE TUNER - Initial Test")
    print("="*70)

    # Create tuner with resonance parameters
    tuner = NerveGateResonanceTuner(
        resonance_params={
            "beta": 0.5,
            "gamma": 0.1,
            "c_L": 1.0,
            "k": 0.5,
        }
    )

    print(f"\nResonance parameters:")
    print(f"  β (coupling) = {tuner.resonance.beta}")
    print(f"  γ (damping) = {tuner.resonance.gamma}")
    print(f"  ω₀ (target frequency) = {tuner.resonance.omega_0:.6f} rad/s")
    print(f"  Q-factor = {tuner.resonance.q_factor:.2f}")

    # Simulate control loop
    print(f"\nSimulation: 100 control steps with V_0 feedback")
    print(f"{'Step':<6} {'V_0':<8} {'ω_gate':<8} {'Error':<8} {'Gate_U':<8}")

    dt_s = 1e-6  # 1 microsecond
    v_0 = 2.5

    for step in range(100):
        # Simulate V_0 with small oscillation
        v_0 = 2.5 + 0.02 * math.sin(2 * math.pi * step / 50.0)

        # Update gate frequency (simplified - normally from V_0 feedback)
        tuner.resonance.omega_gate = tuner.resonance.omega_0 * (1 + 0.1 * math.sin(step * 0.01))

        # Run control step
        gate_voltages = tuner.step(v_0, dt_s)

        # Print sample states
        if step % 25 == 0 or step < 5:
            u_voltage = gate_voltages.get("M_U_high", 0.0)
            freq_error = tuner.resonance.frequency_error
            print(f"{step:<6d} {v_0:<8.5f} {tuner.resonance.omega_gate:<8.6f} {freq_error:<8.6f} {u_voltage:<8.4f}V")

    print(f"\nFinal state:")
    print(f"  V_0 = {tuner.virtual_bus.v_0:.6f}V")
    print(f"  Resonance amplitude = {tuner.resonance.resonance_amplitude:.6f}")
    print(f"  Energy circulating = {tuner.resonance.energy_circulating:.6f}")
    print(f"  Frequency error = {tuner.resonance.frequency_error:.6f} rad/s")

    print("\n" + "="*70)
