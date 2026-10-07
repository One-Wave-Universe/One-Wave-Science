#!/usr/bin/env python3
"""
P0 Hexagon - H-Bridge with Damped Memory Inputs

Same as p0_hexagon_hbridge_reduced_L.py but with additional
damping resistors at the memory input nodes to prevent ringing
from the nerve ring coupling.

The memory_X_pos_in and memory_X_neg_in nodes act as the inlet
to the memory inductors. Without damping, the inductor can create
high-voltage transients when current is forced to change rapidly
via the nerve ring coupling.

Solution: Add parallel resistors from memory inputs to VREF
to provide a high-impedance bias/damping path.
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, CapacitorState, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer, Capacitor


class P0HexagonHBridgeDamped:
    """P0 hexagon H-bridge with damped memory input nodes."""

    def __init__(self,
                 v_supply: float = 1.0,
                 winding_inductance: float = 100e-6,  # 100µH
                 winding_resistance: float = 5.0,
                 sense_inductance: float = 10e-6,     # 10µH
                 sense_resistance: float = 10.0,
                 memory_input_damping_ohms: float = 100000.0,  # 100kΩ damping
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 0.4,
                 buffer_rout: float = 0.1,
                 dclink_capacitor_uf: float = 10.0):
        """
        Args:
            memory_input_damping_ohms: Damping resistor at memory input (to VREF)
                Higher value = less damping, lower value = more damping
                Typical range: 10kΩ to 1MΩ
        """
        self.v_supply = v_supply
        self.l_drive = winding_inductance
        self.r_drive = winding_resistance
        self.l_sense = sense_inductance
        self.r_sense = sense_resistance
        self.r_mem_damp = memory_input_damping_ohms
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.buffer_rout = buffer_rout
        self.c_dclink = dclink_capacitor_uf * 1e-6

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build circuit with damped memory inputs."""
        circuit = TransientCircuit()

        # Single supply
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

        circuit.add(Resistor(
            id="R_dclink_init",
            a="+V",
            b="DC_LINK",
            ohms=100000.0
        ))

        # Six hex vertices
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]

        # Independent H-bridge at each vertex
        for node in hex_nodes:
            circuit.add(PMOS(
                id=f"{node}_HS",
                gate=f"gate_{node}_hs",
                drain="+V",
                source=node,
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            circuit.add(NMOS(
                id=f"{node}_LS",
                gate=f"gate_{node}_ls",
                drain=node,
                source="GND",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

        # Three phases with Drive, Memory, Sense windings
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
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_drive_pos",
                a=f"mid_{phase_name}_drive_pos",
                b="VREF",
                ohms=self.r_drive
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_drive_neg",
                a="VREF",
                b=f"mid_{phase_name}_drive_neg",
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_drive_neg",
                a=f"mid_{phase_name}_drive_neg",
                b=neg_node,
                ohms=self.r_drive
            ))

            # SENSE winding
            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_pos",
                a=pos_node,
                b=f"sense_{phase_name}_pos",
                henries=self.l_sense
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_pos",
                a=f"sense_{phase_name}_pos",
                b="VREF",
                ohms=self.r_sense
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_neg",
                a="VREF",
                b=f"sense_{phase_name}_neg",
                henries=self.l_sense
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_neg",
                a=f"sense_{phase_name}_neg",
                b=neg_node,
                ohms=self.r_sense
            ))

            # MEMORY winding with DAMPING RESISTORS at inputs
            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_in",
                b=f"memory_{phase_name}_pos_mid",
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_mid",
                b="VREF",
                ohms=self.r_drive
            ))
            # Damping resistor at input
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos_damp",
                a=f"memory_{phase_name}_pos_in",
                b="VREF",
                ohms=self.r_mem_damp
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_neg",
                a="VREF",
                b=f"memory_{phase_name}_neg_mid",
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg",
                a=f"memory_{phase_name}_neg_mid",
                b=f"memory_{phase_name}_neg_in",
                ohms=self.r_drive
            ))
            # Damping resistor at input
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg_damp",
                a=f"memory_{phase_name}_neg_in",
                b="VREF",
                ohms=self.r_mem_damp
            ))

        # NERVE RING: A_sense → B_memory coupling
        r_nerve = 10000.0
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
            "C_dclink": CapacitorState(id="C_dclink", voltage=self.v_supply),
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
            "DC_LINK": self.v_supply,
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
                    voltages[f"{winding_type}_{phase_name}_{half}_mid"] = v_baseline
                    if winding_type in ["sense", "memory"]:
                        voltages[f"{winding_type}_{phase_name}_{half}"] = v_baseline
                    if winding_type == "memory":
                        voltages[f"memory_{phase_name}_{half}_in"] = v_baseline

        # Initialize gate nodes
        for node in hex_nodes:
            voltages[f"gate_{node}_hs"] = 0.9
            voltages[f"gate_{node}_ls"] = 0.2

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon H-bridge with damped memory inputs...")
    builder = P0HexagonHBridgeDamped(
        v_supply=1.0,
        memory_input_damping_ohms=100000.0
    )
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built")
    print(f"  Memory input damping: 100kΩ to VREF")
    print(f"  Reduces inductor transient ringing")
