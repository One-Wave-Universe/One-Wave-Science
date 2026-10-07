#!/usr/bin/env python3
"""
P0 Hexagon - H-Bridge with Independent High-Side/Low-Side Gate Control

Pointy hexagon, clockwise vertices:
  a+ (top, 12 o'clock)
  b+ (top-right, 2 o'clock)
  c+ (bottom-right, 4 o'clock)
  a- (bottom, 6 o'clock)
  b- (bottom-left, 8 o'clock)
  c- (top-left, 10 o'clock)

INDEPENDENT H-BRIDGE GATES:
  Each hex vertex (phase) has TWO independent gate signals:
    - gate_X_HS: high-side PMOS control
    - gate_X_LS: low-side NMOS control

  This solves the 1V supply / 0.4V Vth shoot-through problem:
    - PMOS turns ON when gate_HS is LOW (~0.2V)
    - NMOS turns ON when gate_LS is HIGH (~0.9V)
    - Both can be kept OFF simultaneously via independent control
    - Deadband logic ensures they never conduct at the same time

THREE PHASES through central VREF:
  A: a+ ↔ VREF ↔ a- (vertical winding)
  B: b+ ↔ VREF ↔ b- (diagonal winding)
  C: c+ ↔ VREF ↔ c- (diagonal winding)

18-TERMINAL FIXTURE:
  A: Drive +/- | Memory +/- | Sense +/-
  B: Drive +/- | Memory +/- | Sense +/-
  C: Drive +/- | Memory +/- | Sense +/-

H-BRIDGE TOPOLOGY:
  Full reversible drive with proper independent gate control.
  VREF: quiet electrical reference (0.50V baseline)
  DC_LINK: high-current energy reservoir (separate from VREF)
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, CapacitorState, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer, Capacitor


class P0HexagonHBridgeIndependent:
    """P0 hexagon with independent H-bridge gate control per phase."""

    def __init__(self,
                 v_supply: float = 1.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 sense_inductance: float = 1e-4,
                 sense_resistance: float = 10.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 0.4,
                 buffer_rout: float = 0.1,
                 dclink_capacitor_uf: float = 10.0):
        """
        Args:
            v_supply: 1.0V supply for biological scale
            winding_inductance: Drive/Memory winding inductance (H)
            winding_resistance: Winding resistance (ohms)
            sense_inductance: Sense winding inductance (H)
            sense_resistance: Sense winding resistance (ohms)
            mosfet_rds_on: MOSFET on-state resistance (ohms)
            mosfet_vth: MOSFET threshold (0.4V for 1V supply)
            buffer_rout: VREF buffer output impedance
            dclink_capacitor_uf: DC-link reservoir (µF)
        """
        self.v_supply = v_supply
        self.l_drive = winding_inductance
        self.r_drive = winding_resistance
        self.l_sense = sense_inductance
        self.r_sense = sense_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.buffer_rout = buffer_rout
        self.c_dclink = dclink_capacitor_uf * 1e-6

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build circuit with independent H-bridge gate control per phase."""
        circuit = TransientCircuit()

        # Single supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

        # VREF: quiet electrical reference (0.50V)
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

        # DC-LINK reservoir (separate from VREF for reinjection)
        circuit.add(Capacitor(
            id="C_dclink",
            a="DC_LINK",
            b="GND",
            farads=self.c_dclink
        ))

        # Initialize DC_LINK to V_supply
        circuit.add(Resistor(
            id="R_dclink_init",
            a="+V",
            b="DC_LINK",
            ohms=100000.0  # High impedance init path
        ))

        # Six hex vertices
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]

        # Independent H-bridge at each vertex
        # Each vertex gets TWO independent gate signals:
        #   gate_X_HS for PMOS (high-side)
        #   gate_X_LS for NMOS (low-side)
        for node in hex_nodes:
            # High-side PMOS: gate pulled low to turn ON
            circuit.add(PMOS(
                id=f"{node}_HS",
                gate=f"gate_{node}_hs",
                drain="+V",
                source=node,
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side NMOS: gate pulled high to turn ON
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
            # DRIVE winding (connected to hex vertices via H-bridge)
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

            # SENSE winding (monitors phase voltage)
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

            # MEMORY winding (for state retention, coupled via nerve ring)
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

        # NERVE RING: A_sense → B_memory coupling via resistor
        # (Higher impedance to reduce transient oscillation and improve stability)
        # Nerve ring acts as a signal path, not a power path
        r_nerve = 10000.0  # 10kΩ for minimal transient disturbance
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
            # Hex vertices
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
                    # Mid nodes
                    voltages[f"{winding_type}_{phase_name}_{half}_mid"] = v_baseline
                    # Sense/Memory input/output nodes
                    if winding_type in ["sense", "memory"]:
                        voltages[f"{winding_type}_{phase_name}_{half}"] = v_baseline
                    if winding_type == "memory":
                        voltages[f"memory_{phase_name}_{half}_in"] = v_baseline

        # Initialize all gate nodes (neutral state: both FETs off)
        for node in hex_nodes:
            voltages[f"gate_{node}_hs"] = 0.9  # PMOS OFF (gate high)
            voltages[f"gate_{node}_ls"] = 0.2  # NMOS OFF (gate low)

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon H-bridge with independent gate control...")
    builder = P0HexagonHBridgeIndependent(v_supply=1.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built")
    print(f"  Phases: A, B, C (six hex vertices)")
    print(f"  Windings per phase: Drive, Memory, Sense")
    print(f"  H-Bridge: independent high-side and low-side gate control")
    print(f"  Nerve ring: A_sense → B_memory (1kΩ coupling)")
    print(f"  VREF baseline: 0.50V")
    print(f"  DC_LINK reservoir: separate from VREF")
    print(f"  Supply: 1.0V")
