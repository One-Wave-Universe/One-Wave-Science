#!/usr/bin/env python3
"""
P0 Hexagon - Passive Version (No MOSFETs)

Simplified circuit for testing nerve ring coupling without switching element issues.

Three phases with Drive, Sense, and Memory windings, all connected through VREF.
Nerve ring pre-wired: A_sense → B_memory.

This version eliminates MOSFET gate control issues and focuses on:
1. Proving nerve ring coupling works
2. Demonstrating state transfer through inductive coupling
3. Validating the circuit architecture before adding active drive
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, CapacitorState, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, OpAmpBuffer, Capacitor


class P0HexagonPassive:
    """Passive hexagon with nerve ring, no switching elements."""

    def __init__(self,
                 v_supply: float = 1.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 buffer_rout: float = 0.1,
                 dclink_capacitor_uf: float = 10.0):
        self.v_supply = v_supply
        self.l_winding = winding_inductance
        self.r_winding = winding_resistance
        self.buffer_rout = buffer_rout
        self.c_dclink = dclink_capacitor_uf * 1e-6

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build passive circuit with nerve ring coupling."""
        circuit = TransientCircuit()

        # Supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

        # VREF
        r_div = 100.0
        circuit.add(Resistor(
            id="R_div_top",
            a="+V",
            b="vref_raw",
            ohms=r_div
        ))
        circuit.add(Resistor(
            id="R_div_bottom",
            a="vref_raw",
            b="GND",
            ohms=r_div
        ))

        circuit.add(OpAmpBuffer(
            id="vref_buffer",
            v_in="vref_raw",
            v_out="VREF",
            gnd="GND",
            gain=1.0,
            Rout=self.buffer_rout,
            max_sourcing_mA=500.0,
            max_sinking_mA=500.0
        ))

        # DC-LINK
        circuit.add(Capacitor(
            id="C_dclink",
            a="DC_LINK",
            b="GND",
            farads=self.c_dclink
        ))

        # Simplified phase nodes (just points, no switching)
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]
        for node in hex_nodes:
            # Just a 10kΩ biasing resistor to VREF for each node
            circuit.add(Resistor(
                id=f"R_bias_{node}",
                a=node,
                b="VREF",
                ohms=10000.0
            ))

        # Three phases with Drive, Sense, Memory windings
        phases = [
            ("A", "a_pos", "a_neg"),
            ("B", "b_pos", "b_neg"),
            ("C", "c_pos", "c_neg"),
        ]

        for phase_name, pos_node, neg_node in phases:
            # DRIVE winding
            circuit.add(Inductor(
                id=f"L_{phase_name}_drive_pos",
                a=pos_node,
                b=f"mid_{phase_name}_drive_pos",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_drive_pos",
                a=f"mid_{phase_name}_drive_pos",
                b="VREF",
                ohms=self.r_winding
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_drive_neg",
                a="VREF",
                b=f"mid_{phase_name}_drive_neg",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_drive_neg",
                a=f"mid_{phase_name}_drive_neg",
                b=neg_node,
                ohms=self.r_winding
            ))

            # SENSE winding
            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_pos",
                a=pos_node,
                b=f"sense_{phase_name}_pos",
                henries=self.l_winding / 10.0
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_pos",
                a=f"sense_{phase_name}_pos",
                b="VREF",
                ohms=self.r_winding
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_neg",
                a="VREF",
                b=f"sense_{phase_name}_neg",
                henries=self.l_winding / 10.0
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_neg",
                a=f"sense_{phase_name}_neg",
                b=neg_node,
                ohms=self.r_winding
            ))

            # MEMORY winding
            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_in",
                b=f"memory_{phase_name}_pos_mid",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_mid",
                b="VREF",
                ohms=self.r_winding
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_neg",
                a="VREF",
                b=f"memory_{phase_name}_neg_mid",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg",
                a=f"memory_{phase_name}_neg_mid",
                b=f"memory_{phase_name}_neg_in",
                ohms=self.r_winding
            ))

        # NERVE RING: A_sense → B_memory via resistive coupling
        r_nerve = 1000.0  # Lower impedance for better coupling
        circuit.add(Resistor(
            id="R_nerve_A_sense_to_B_memory_pos",
            a="sense_A_pos",
            b="memory_B_pos_in",
            ohms=r_nerve
        ))
        circuit.add(Resistor(
            id="R_nerve_A_sense_to_B_memory_neg",
            a="sense_A_neg",
            b="memory_B_neg_in",
            ohms=r_nerve
        ))

        # Initial state
        cap_states = {
            "C_dclink": CapacitorState(id="C_dclink", voltage=0.0),
        }

        ind_states = {}
        for phase_name in ["A", "B", "C"]:
            for winding_type in ["drive", "memory", "sense"]:
                for half in ["pos", "neg"]:
                    ind_id = f"L_{phase_name}_{winding_type}_{half}"
                    ind_states[ind_id] = InductorState(id=ind_id, current=0.0)

        v_baseline = 0.50
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "vref_raw": v_baseline,
            "VREF": v_baseline,
            "DC_LINK": v_baseline,
            # Hex phase nodes
            "a_pos": v_baseline,
            "b_pos": v_baseline,
            "c_pos": v_baseline,
            "a_neg": v_baseline,
            "b_neg": v_baseline,
            "c_neg": v_baseline,
        }

        # Initialize all winding nodes
        for phase_name in ["A", "B", "C"]:
            for winding_type in ["drive", "memory", "sense"]:
                for half in ["pos", "neg"]:
                    voltages[f"{winding_type}_{phase_name}_{half}"] = v_baseline
                    voltages[f"{winding_type}_{phase_name}_{half}_mid"] = v_baseline
                    if winding_type == "memory":
                        voltages[f"memory_{phase_name}_{half}_in"] = v_baseline

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon passive circuit...")
    builder = P0HexagonPassive(v_supply=1.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built (passive, no MOSFETs)")
    print(f"  Nerve ring: A_sense → B_memory (1kΩ coupling)")
    print(f"  VREF: 0.50V")
    print(f"  Supply: 1.0V")
