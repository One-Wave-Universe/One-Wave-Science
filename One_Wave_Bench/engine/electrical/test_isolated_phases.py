#!/usr/bin/env python3
"""Test completely isolated phases to identify the coupling source."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import Inductor, NMOS, PMOS, Capacitor
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class IsolatedTriplePhasesTest:
    """Three phases, completely electrically isolated except for shared supply."""

    def __init__(self):
        self.v_supply = 1.0

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build three isolated phase circuits."""
        circuit = TransientCircuit()

        # Single shared supply and ground
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        # DC-LINK (shared)
        circuit.add(Capacitor(
            id="C_dclink",
            a="DC_LINK",
            b="GND",
            farads=10e-6
        ))
        circuit.add(Resistor(
            id="R_dclink_init",
            a="+V",
            b="DC_LINK",
            ohms=100000.0
        ))

        # THREE PHASES - COMPLETELY ISOLATED
        # Each has its own local resistor divider VREF
        phases = [
            ("A", "a_pos", "a_neg", "VREF_A"),
            ("B", "b_pos", "b_neg", "VREF_B"),
            ("C", "c_pos", "c_neg", "VREF_C"),
        ]

        for phase_name, pos_node, neg_node, local_vref in phases:
            # Local VREF for this phase
            circuit.add(Resistor(
                id=f"R_div_top_{phase_name}",
                a="+V",
                b=local_vref,
                ohms=100.0
            ))
            circuit.add(Resistor(
                id=f"R_div_bottom_{phase_name}",
                a=local_vref,
                b="GND",
                ohms=100.0
            ))

            # H-bridge
            circuit.add(PMOS(
                id=f"{pos_node}_HS",
                gate=f"gate_{pos_node}_hs",
                drain="+V",
                source=pos_node,
                Vth=0.4,
                Rds_on=0.5
            ))
            circuit.add(NMOS(
                id=f"{pos_node}_LS",
                gate=f"gate_{pos_node}_ls",
                drain=pos_node,
                source="GND",
                Vth=0.4,
                Rds_on=0.5
            ))
            circuit.add(PMOS(
                id=f"{neg_node}_HS",
                gate=f"gate_{neg_node}_hs",
                drain="+V",
                source=neg_node,
                Vth=0.4,
                Rds_on=0.5
            ))
            circuit.add(NMOS(
                id=f"{neg_node}_LS",
                gate=f"gate_{neg_node}_ls",
                drain=neg_node,
                source="GND",
                Vth=0.4,
                Rds_on=0.5
            ))

            # SENSE winding (no coupling to other phases)
            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_pos",
                a=pos_node,
                b=f"sense_{phase_name}_pos",
                henries=10e-6
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_pos",
                a=f"sense_{phase_name}_pos",
                b=local_vref,
                ohms=100.0
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_neg",
                a=local_vref,
                b=f"sense_{phase_name}_neg",
                henries=10e-6
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_neg",
                a=f"sense_{phase_name}_neg",
                b=neg_node,
                ohms=100.0
            ))

            # DRIVE winding (no coupling)
            circuit.add(Inductor(
                id=f"L_{phase_name}_drive_pos",
                a=pos_node,
                b=f"drive_{phase_name}_pos",
                henries=100e-6
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_drive_pos",
                a=f"drive_{phase_name}_pos",
                b=local_vref,
                ohms=5.0
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_drive_neg",
                a=local_vref,
                b=f"drive_{phase_name}_neg",
                henries=100e-6
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_drive_neg",
                a=f"drive_{phase_name}_neg",
                b=neg_node,
                ohms=5.0
            ))

            # Memory winding (isolated)
            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_in",
                b=f"memory_{phase_name}_pos_mid",
                henries=100e-6
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_mid",
                b=local_vref,
                ohms=5.0
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos_damp",
                a=f"memory_{phase_name}_pos_in",
                b=local_vref,
                ohms=100000.0
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_neg",
                a=local_vref,
                b=f"memory_{phase_name}_neg_mid",
                henries=100e-6
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg",
                a=f"memory_{phase_name}_neg_mid",
                b=f"memory_{phase_name}_neg_in",
                ohms=5.0
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg_damp",
                a=f"memory_{phase_name}_neg_in",
                b=local_vref,
                ohms=100000.0
            ))

        # Initial state
        cap_states = {"C_dclink": CapacitorState(id="C_dclink", voltage=self.v_supply)}

        ind_states = {}
        for phase_name in ["A", "B", "C"]:
            for winding_type in ["drive", "sense", "memory"]:
                for half in ["pos", "neg"]:
                    ind_id = f"L_{phase_name}_{winding_type}_{half}"
                    ind_states[ind_id] = InductorState(id=ind_id, current=0.0)

        v_baseline = 0.50
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "VREF_A": v_baseline,
            "VREF_B": v_baseline,
            "VREF_C": v_baseline,
            "DC_LINK": self.v_supply,
        }

        for phase_name in ["A", "B", "C"]:
            pos_node = f"{phase_name.lower()}_pos"
            neg_node = f"{phase_name.lower()}_neg"
            voltages[pos_node] = v_baseline
            voltages[neg_node] = v_baseline
            voltages[f"gate_{pos_node}_hs"] = 0.9
            voltages[f"gate_{pos_node}_ls"] = 0.2
            voltages[f"gate_{neg_node}_hs"] = 0.9
            voltages[f"gate_{neg_node}_ls"] = 0.2

            for winding_type in ["drive", "sense", "memory"]:
                voltages[f"{winding_type}_{phase_name}_pos"] = v_baseline
                voltages[f"{winding_type}_{phase_name}_neg"] = v_baseline
                voltages[f"{winding_type}_{phase_name}_pos_mid"] = v_baseline
                voltages[f"{winding_type}_{phase_name}_neg_mid"] = v_baseline
                voltages[f"memory_{phase_name}_pos_in"] = v_baseline
                voltages[f"memory_{phase_name}_neg_in"] = v_baseline

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


# Run test
print("\n" + "="*80)
print("ISOLATED PHASES TEST: Three phases with NO cross-phase coupling")
print("="*80)
print("\nEach phase has:")
print("  - Local independent VREF (100Ω divider)")
print("  - Drive, Sense, Memory windings")
print("  - H-bridge to +V and GND")
print("  - NO electrical connection to other phases")
print("  - NO nerve ring coupling\n")

builder = IsolatedTriplePhasesTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)

dt_s = 1e-6
duration_us = 500.0
n_steps = int(duration_us * 1e-6 / dt_s)

print(f"{'Time (µs)':<15} {'V_A_pos':<15} {'V_B_pos':<15} {'V_C_pos':<15} {'Status':<20}")
print("-" * 80)

for step in range(n_steps):
    try:
        controller.run_step(dt_s)
        state = controller._make_state()

        a_pos = state.node_voltages.get('a_pos', 0.5)
        b_pos = state.node_voltages.get('b_pos', 0.5)
        c_pos = state.node_voltages.get('c_pos', 0.5)

        max_delta = max(abs(a_pos - 0.5), abs(b_pos - 0.5), abs(c_pos - 0.5))
        if max_delta > 1.5:
            divergence_time = step * dt_s * 1e6
            print(f"{divergence_time:<15.1f} {a_pos:<15.4f} {b_pos:<15.4f} {c_pos:<15.4f} DIVERGED!")
            break

        if (step + 1) % 50 == 0:
            time_us = (step + 1) * dt_s * 1e6
            status = "OK" if max_delta < 0.1 else f"DRIFT({max_delta:.3f})"
            print(f"{time_us:<15.1f} {a_pos:<15.4f} {b_pos:<15.4f} {c_pos:<15.4f} {status:<20}")

    except Exception as e:
        divergence_time = step * dt_s * 1e6
        print(f"{divergence_time:<15.1f} ERROR: {str(e)[:50]}")
        break
else:
    print("-" * 80)
    print(f"✓ STABLE for entire {duration_us}µs")
    print(f"\nFINDING: Three isolated phases ARE stable.")
    print(f"The divergence requires cross-phase coupling to manifest.")

print("="*80 + "\n")
