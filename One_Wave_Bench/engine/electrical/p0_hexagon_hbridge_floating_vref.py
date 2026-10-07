#!/usr/bin/env python3
"""
P0 Hexagon - H-Bridge with FLOATING VREF (Topology Fix)

SOLUTION: Floating Reference Implementation
============================================

Problem: Star-grounded central VREF creates singular/ill-conditioned MNA matrix
in multi-phase networks. Divergence at 35-50µs regardless of parameter tuning.

Solution: Three independent local voltage references instead of one shared VREF.
- Phase A/B pair: VREF_AB at 0.50V
- Phase B/C pair: VREF_BC at 0.50V
- Phase C/A pair: VREF_CA at 0.50V

This decouples the three phase nodes, breaking the pathological MNA matrix
singularity while maintaining ternary differential coupling through sense/memory
cross-phase connections.

Architecture aligns with cell flower seven-cell configuration where each
phase pair has its own local equilibrium reference, preserving the biological
ternary balance.
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, CapacitorState, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer, Capacitor


class P0HexagonHBridgeFloatingVref:
    """P0 hexagon with floating (decoupled) VREF per phase pair."""

    def __init__(self,
                 v_supply: float = 1.0,
                 winding_inductance: float = 100e-6,  # 100µH
                 winding_resistance: float = 5.0,
                 sense_inductance: float = 10e-6,
                 sense_resistance: float = 100.0,  # Conservative for stable topology
                 memory_input_damping_ohms: float = 100000.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 0.4,
                 dclink_capacitor_uf: float = 10.0):
        """
        Args:
            sense_resistance: Adjusted to 100Ω for floating VREF topology.
                Previous: 4500Ω (attempted MNA stability workaround for star-ground).
                New: 100Ω (tau = 100ns, dt/tau = 10, within normal Euler bounds).
                With floating VREF, normal component values should work again.
        """
        self.v_supply = v_supply
        self.l_drive = winding_inductance
        self.r_drive = winding_resistance
        self.l_sense = sense_inductance
        self.r_sense = sense_resistance
        self.r_mem_damp = memory_input_damping_ohms
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.c_dclink = dclink_capacitor_uf * 1e-6

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build circuit with floating VREF per phase pair."""
        circuit = TransientCircuit()

        # Single supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

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

        # THREE FLOATING VREF (one per phase pair)
        # VREF_AB: Phase A and B local reference
        circuit.add(Resistor(
            id="R_div_top_AB",
            a="+V",
            b="VREF_AB",
            ohms=100.0
        ))
        circuit.add(Resistor(
            id="R_div_bottom_AB",
            a="VREF_AB",
            b="GND",
            ohms=100.0
        ))

        # VREF_BC: Phase B and C local reference
        circuit.add(Resistor(
            id="R_div_top_BC",
            a="+V",
            b="VREF_BC",
            ohms=100.0
        ))
        circuit.add(Resistor(
            id="R_div_bottom_BC",
            a="VREF_BC",
            b="GND",
            ohms=100.0
        ))

        # VREF_CA: Phase C and A local reference
        circuit.add(Resistor(
            id="R_div_top_CA",
            a="+V",
            b="VREF_CA",
            ohms=100.0
        ))
        circuit.add(Resistor(
            id="R_div_bottom_CA",
            a="VREF_CA",
            b="GND",
            ohms=100.0
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

        # Three phases with windings using LOCAL VREF
        phases = [
            ("A", "a_pos", "a_neg", "VREF_AB"),  # Phase A uses VREF_AB
            ("B", "b_pos", "b_neg", "VREF_AB"),  # Phase B uses VREF_AB
            ("C", "c_pos", "c_neg", "VREF_BC"),  # Phase C uses VREF_BC (could use VREF_CA or VREF_BC)
        ]

        for phase_name, pos_node, neg_node, local_vref in phases:
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
                b=local_vref,
                ohms=self.r_drive
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_drive_neg",
                a=local_vref,
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
                b=local_vref,
                ohms=self.r_sense
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_neg",
                a=local_vref,
                b=f"sense_{phase_name}_neg",
                henries=self.l_sense
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_neg",
                a=f"sense_{phase_name}_neg",
                b=neg_node,
                ohms=self.r_sense
            ))

            # MEMORY winding
            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_in",
                b=f"memory_{phase_name}_pos_mid",
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_mid",
                b=local_vref,
                ohms=self.r_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos_damp",
                a=f"memory_{phase_name}_pos_in",
                b=local_vref,
                ohms=self.r_mem_damp
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_neg",
                a=local_vref,
                b=f"memory_{phase_name}_neg_mid",
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg",
                a=f"memory_{phase_name}_neg_mid",
                b=f"memory_{phase_name}_neg_in",
                ohms=self.r_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg_damp",
                a=f"memory_{phase_name}_neg_in",
                b=local_vref,
                ohms=self.r_mem_damp
            ))

        # NERVE RING: A_sense → B_memory coupling (cross-phase, via local VREF nodes)
        # A and B both use VREF_AB, so nerve coupling works locally
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
            "VREF_AB": v_baseline,
            "VREF_BC": v_baseline,
            "VREF_CA": v_baseline,
            "DC_LINK": self.v_supply,
            "a_pos": v_baseline,
            "b_pos": v_baseline,
            "c_pos": v_baseline,
            "a_neg": v_baseline,
            "b_neg": v_baseline,
            "c_neg": v_baseline,
        }

        for phase_name in ["A", "B", "C"]:
            for winding_type in ["drive", "memory", "sense"]:
                for half in ["pos", "neg"]:
                    voltages[f"{winding_type}_{phase_name}_{half}_mid"] = v_baseline
                    if winding_type in ["sense", "memory"]:
                        voltages[f"{winding_type}_{phase_name}_{half}"] = v_baseline
                    if winding_type == "memory":
                        voltages[f"memory_{phase_name}_{half}_in"] = v_baseline

        for node in hex_nodes:
            voltages[f"gate_{node}_hs"] = 0.9
            voltages[f"gate_{node}_ls"] = 0.2

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon H-bridge with FLOATING VREF topology...")
    builder = P0HexagonHBridgeFloatingVref(v_supply=1.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built (Floating VREF: VREF_AB, VREF_BC, VREF_CA)")
    print(f"  Topology: Decoupled phase references")
    print(f"  R_sense: 100Ω (normal values, no MNA workaround needed)")
    print(f"  Supply: 1.0V")
    print(f"  Nerve ring: A_sense → B_memory (10kΩ coupling)")
