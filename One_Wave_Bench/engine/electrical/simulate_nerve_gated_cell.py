#!/usr/bin/env python3
"""
Nerve-Gated Cell Simulation: Full P0 Ternary Circuit with Resonance Tuning

Simulates the P0 circuit under closed-loop nerve-gated resonance control:
- Virtual ground maintained at 2.5V via proportional feedback
- Three-phase gates driven by resonance-tuning PID control
- Tracks resonance state and energy coupling
- Displays cascading effects (point → path → field rotations)
"""
from __future__ import annotations
import sys
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

# Add repo root to path
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_ternary_circuit import P0TernaryCircuit
from One_Wave_Bench.engine.electrical.circuit_controller import (
    CircuitController, ControlMode, CircuitState
)
from One_Wave_Bench.engine.electrical.nerve_gate_resonance import (
    NerveGateResonanceTuner, ResonanceState
)


@dataclass
class CellSimulationSnapshot:
    """Snapshot of cell state at one timestep."""
    time_us: float
    step: int

    # Virtual ground
    v_0: float
    v_0_error: float

    # Gate state
    gate_u: float
    gate_v: float
    gate_w: float

    # Resonance state
    omega_0: float  # Target frequency
    omega_gate: float  # Current gate rotation frequency
    frequency_error: float
    resonance_amplitude: float
    energy_circulating: float
    q_factor: float

    # Field state
    field_energy: float
    three_phase_balance: float  # Should be 0.0 when balanced


class NerveGatedCellSimulator:
    """
    Full P0 ternary circuit simulation with nerve-gated resonance control.

    Architecture:
    - P0 circuit with three half-bridges + virtual ground
    - NerveGateResonanceTuner drives three-phase gates
    - Virtual bus unified state tracking
    - Cascading rotations: point → path → field
    """

    def __init__(self, duration_s: float = 1e-3):
        """
        Initialize simulation.

        Args:
            duration_s: Simulation duration in seconds
        """
        self.duration_s = duration_s
        self.snapshots: List[CellSimulationSnapshot] = []

        # Build P0 circuit
        print("Building P0 ternary circuit...")
        builder = P0TernaryCircuit(v_supply=5.0)
        self.circuit, initial_state = builder.build(supply_mode="single")
        self.controller = CircuitController(self.circuit, initial_state)

        # Create nerve-gated resonance tuner
        print("Creating nerve-gated resonance tuner...")
        self.tuner = NerveGateResonanceTuner(
            resonance_params={
                "beta": 0.5,
                "gamma": 0.05,  # Lower damping for more resonance
                "c_L": 1.0,
                "k": 1.0,  # Larger wavenumber for higher frequency
            }
        )

        print(f"\nResonance parameters:")
        print(f"  Target frequency ω₀ = {self.tuner.resonance.omega_0:.6f} rad/s")
        print(f"  Q-factor = {self.tuner.resonance.q_factor:.2f}")

    def run(self, dt_s: float = 1e-6) -> List[CellSimulationSnapshot]:
        """
        Run complete simulation with nerve-gated control.

        Args:
            dt_s: Timestep in seconds

        Returns:
            List of simulation snapshots
        """
        n_steps = int(self.duration_s / dt_s)
        print(f"\nRunning {n_steps} simulation steps ({self.duration_s*1e6:.1f}µs total)")
        print(f"Timestep: {dt_s*1e6:.3f}µs")

        # Simulation loop
        for step in range(n_steps):
            # Get current circuit state
            current_state = self._make_state()
            v_0 = current_state.node_voltages.get('0', 2.5)

            # Feedback-driven gate control: extract nerve signals and compute gate voltages
            # The tuner.step() will update resonance state based on feedback
            gate_voltages = self.tuner.step(v_0, dt_s)

            # Update gate frequency tracking for measurement (feedback-driven, not sweep)
            # omega_gate follows the actual oscillation of the system in response to V_0 error
            # For now, track frequency error magnitude to guide next iteration
            if abs(self.tuner.resonance.frequency_error) > 1e-6:
                # Gate frequency adjust toward target based on error direction
                freq_adjust = 0.01 * self.tuner.resonance.frequency_error  # Slow tuning
                self.tuner.resonance.omega_gate += freq_adjust

            # Apply gate control to circuit controller
            # Interface amplification: biological nerve signal (0-100mV) → MOSFET drive (0-5V)
            # Nerve signal range: [0.02, 0.08]V = [20, 80]mV (asymmetric biological window)
            # Amplified range: [1.0, 4.0]V around nominal 2.5V bias
            # Gain: 50x (converts 100mV swing to 5V swing)
            def gate_control(mosfet_id: str, time: float) -> float:
                nerve_signal = gate_voltages.get(mosfet_id, 0.05)  # Default to 50mV center
                # Amplify biological signal to MOSFET gate drive level
                # Map: nerve_signal = 0.05V (50mV center) → gate_drive = 2.5V (nominal bias)
                #      nerve_signal ± 0.03V (±30mV) → gate_drive ± 1.5V
                gate_drive = 2.5 + (nerve_signal - 0.05) * 50.0
                # Clamp to valid MOSFET gate range [0, 5]V
                return max(0.0, min(5.0, gate_drive))

            self.controller.set_gate_control(gate_control)

            # Execute one circuit step
            try:
                self.controller.run_step(dt_s)
            except Exception as e:
                print(f"ERROR at step {step}: {e}")
                break

            # Record snapshot
            snapshot = self._create_snapshot(step, dt_s)
            self.snapshots.append(snapshot)

            # Print progress with gate control details
            if step % (n_steps // 20) == 0 or step < 10 or (35 <= step <= 45):
                progress = (step / n_steps) * 100
                gate_u = self.tuner.virtual_bus.gate_voltages.get('M_U_high', 0.05)
                gate_v = self.tuner.virtual_bus.gate_voltages.get('M_V_high', 0.05)
                gate_w = self.tuner.virtual_bus.gate_voltages.get('M_W_high', 0.05)
                drive_u = 2.5 + (gate_u - 0.05) * 50.0
                print(f"  [{progress:5.1f}%] Step {step}: V_0={v_0:.6f}V, "
                      f"nerve_U={gate_u:.4f}V({gate_u*1000:.1f}mV), "
                      f"drive_U={drive_u:.2f}V, "
                      f"Freq_err={self.tuner.resonance.frequency_error:.6f}")

        print(f"\nSimulation complete: {len(self.snapshots)} snapshots recorded")
        return self.snapshots

    def _make_state(self) -> CircuitState:
        """Get current circuit state."""
        return self.controller._make_state()

    def _create_snapshot(self, step: int, dt_s: float) -> CellSimulationSnapshot:
        """Create simulation snapshot."""
        current_state = self._make_state()
        v_0 = current_state.node_voltages.get('0', 2.5)

        # Extract gate voltages
        gate_u = self.tuner.virtual_bus.gate_voltages.get('M_U_high', 2.5)
        gate_v = self.tuner.virtual_bus.gate_voltages.get('M_V_high', 2.5)
        gate_w = self.tuner.virtual_bus.gate_voltages.get('M_W_high', 2.5)

        # Calculate three-phase balance (should be ~zero when balanced)
        # Sum of three phase voltages should rotate back to zero
        phase_angles = [0, 2*math.pi/3, 4*math.pi/3]
        phasor_sum = sum([
            math.cos(phase_angles[i]) * [gate_u, gate_v, gate_w][i]
            for i in range(3)
        ])

        return CellSimulationSnapshot(
            time_us=current_state.time_us,
            step=step,
            v_0=v_0,
            v_0_error=abs(v_0 - 2.5),
            gate_u=gate_u,
            gate_v=gate_v,
            gate_w=gate_w,
            omega_0=self.tuner.resonance.omega_0,
            omega_gate=self.tuner.resonance.omega_gate,
            frequency_error=self.tuner.resonance.frequency_error,
            resonance_amplitude=self.tuner.resonance.resonance_amplitude,
            energy_circulating=self.tuner.resonance.energy_circulating,
            q_factor=self.tuner.resonance.q_factor,
            field_energy=sum(v**2 for v in [gate_u, gate_v, gate_w]) / 3.0,
            three_phase_balance=abs(phasor_sum),
        )

    def print_summary(self):
        """Print simulation summary and statistics."""
        if not self.snapshots:
            print("No snapshots to summarize")
            return

        print("\n" + "="*70)
        print("CELL SIMULATION SUMMARY")
        print("="*70)

        # Extract time series
        times = [s.time_us for s in self.snapshots]
        v_0_values = [s.v_0 for s in self.snapshots]
        v_0_errors = [s.v_0_error for s in self.snapshots]
        freq_errors = [s.frequency_error for s in self.snapshots]
        energies = [s.energy_circulating for s in self.snapshots]

        # Calculate statistics
        v_0_min, v_0_max = min(v_0_values), max(v_0_values)
        v_0_mean = sum(v_0_values) / len(v_0_values) if v_0_values else 0
        v_0_error_max = max(v_0_errors)

        freq_error_min, freq_error_max = min(freq_errors), max(freq_errors)
        freq_error_mean = sum(freq_errors) / len(freq_errors) if freq_errors else 0

        energy_mean = sum(energies) / len(energies) if energies else 0

        print(f"\nVirtual Ground (V_0):")
        print(f"  Target: 2.5000V")
        print(f"  Range: {v_0_min:.6f}V to {v_0_max:.6f}V")
        print(f"  Mean: {v_0_mean:.6f}V")
        print(f"  Max error: {v_0_error_max:.6f}V")
        print(f"  Status: {'✓ STABLE' if v_0_error_max < 0.01 else '⚠ DRIFT'}")

        print(f"\nResonance Tuning:")
        print(f"  Target ω₀: {self.tuner.resonance.omega_0:.6f} rad/s")
        print(f"  Frequency error range: {freq_error_min:.6f} to {freq_error_max:.6f} rad/s")
        print(f"  Mean frequency error: {freq_error_mean:.6f} rad/s")
        print(f"  Q-factor: {self.tuner.resonance.q_factor:.2f}")

        print(f"\nEnergy State:")
        print(f"  Mean energy circulating: {energy_mean:.6f}")
        print(f"  Three-phase balance (last): {self.snapshots[-1].three_phase_balance:.6f}")

        # Time series statistics
        print(f"\nTimeseries:")
        print(f"  Duration: {times[-1]:.6f}µs")
        print(f"  Steps: {len(self.snapshots)}")
        print(f"  Dt average: {times[-1]/len(self.snapshots) if times else 0:.9f}µs")

        print("\n" + "="*70)

    def export_json(self, filepath: str | Path):
        """Export simulation results to JSON."""
        filepath = Path(filepath)

        data = {
            "metadata": {
                "simulation_duration_s": self.duration_s,
                "total_steps": len(self.snapshots),
            },
            "resonance_params": asdict(self.tuner.resonance),
            "snapshots": [asdict(s) for s in self.snapshots],
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Results exported to {filepath}")


def main():
    """Run nerve-gated cell simulation."""
    print("\n" + "="*70)
    print("NERVE-GATED CELL SIMULATION")
    print("="*70)

    # Create and run simulation
    sim = NerveGatedCellSimulator(duration_s=100e-6)  # 100 microseconds
    snapshots = sim.run(dt_s=1e-6)

    # Print summary
    sim.print_summary()

    # Export results
    export_path = "/tmp/nerve_gated_cell_results.json"
    sim.export_json(export_path)

    print(f"\n✓ Simulation complete and exported")
    return sim


if __name__ == "__main__":
    main()
