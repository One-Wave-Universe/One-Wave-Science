#!/usr/bin/env python3
"""
P0 Hexagon - Direct Phase Connections

Pointy hexagon, clockwise vertices:
  a+ (top, 12 o'clock)
  b+ (top-right, 2 o'clock)
  c+ (bottom-right, 4 o'clock)
  a- (bottom, 6 o'clock)
  b- (bottom-left, 8 o'clock)
  c- (top-left, 10 o'clock)

THREE INDEPENDENT PHASES - direct letter-to-letter connections:
  A: a+ ↔ a- (vertical winding)
  B: b+ ↔ b- (diagonal winding)
  C: c+ ↔ c- (diagonal winding)

NO central nucleus. Each phase is independently connected.

Each hex vertex: half-bridge (PMOS high, NMOS low) with gate control.
Gate voltage controls whether current flows through the phase winding.
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS


class P0HexagonDirect:
    """P0 hexagon with direct phase-to-phase connections (no central nucleus)."""

    def __init__(self,
                 v_supply: float = 5.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 1.0):
        self.v_supply = v_supply
        self.l_winding = winding_inductance
        self.r_winding = winding_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build P0 hexagon with direct phase connections."""
        circuit = TransientCircuit()

        # Single supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

        # Six hex vertices (pointy hexagon, clockwise)
        # a+ (top), b+ (tr), c+ (br), a- (bottom), b- (bl), c- (tl)
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]

        # Each vertex has complementary half-bridge
        for node in hex_nodes:
            # High-side PMOS
            circuit.add(PMOS(
                id=f"{node}_HS",
                gate=f"gate_{node}",
                drain="+V",
                source=node,
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side NMOS
            circuit.add(NMOS(
                id=f"{node}_LS",
                gate=f"gate_{node}",
                drain=node,
                source="GND",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

        # Three independent phases - direct connections between opposite vertices
        phases = [
            ("A", "a_pos", "a_neg"),  # a+ ↔ a- (top ↔ bottom, vertical)
            ("B", "b_pos", "b_neg"),  # b+ ↔ b- (tr ↔ bl, diagonal)
            ("C", "c_pos", "c_neg"),  # c+ ↔ c- (br ↔ tl, diagonal)
        ]

        for phase_name, pos_node, neg_node in phases:
            # Single winding directly connecting pos to neg node
            circuit.add(Inductor(
                id=f"L_{phase_name}",
                a=pos_node,
                b=f"mid_{phase_name}",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}",
                a=f"mid_{phase_name}",
                b=neg_node,
                ohms=self.r_winding
            ))

        # Initial state
        cap_states = {}
        ind_states = {
            "L_A": InductorState(id="L_A", current=0.0),
            "L_B": InductorState(id="L_B", current=0.0),
            "L_C": InductorState(id="L_C", current=0.0),
        }

        v_baseline = 0.50  # Biological baseline: 0.50V (not 2.5V)
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            # Hex vertices all at baseline initially
            "a_pos": v_baseline,
            "b_pos": v_baseline,
            "c_pos": v_baseline,
            "a_neg": v_baseline,
            "b_neg": v_baseline,
            "c_neg": v_baseline,
            # Winding midpoints
            "mid_A": v_baseline,
            "mid_B": v_baseline,
            "mid_C": v_baseline,
        }

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon direct phase circuit...")
    builder = P0HexagonDirect(v_supply=5.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built: {len(circuit.components)} components")
    print(f"  Layout: Pointy hexagon, clockwise a+ b+ c+ a- b- c-")
    print(f"  Phases: A (a+↔a-), B (b+↔b-), C (c+↔c-)")
    print(f"  No central nucleus - direct letter-to-letter connections")
    print(f"  Gate control: shared gate per vertex (PMOS + NMOS together)")
