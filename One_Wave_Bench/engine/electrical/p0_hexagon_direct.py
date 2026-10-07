#!/usr/bin/env python3
"""
P0 Hexagon - Active Ternary Leaning Virtual Ground

Pointy hexagon, clockwise vertices:
  a+ (top, 12 o'clock)
  b+ (top-right, 2 o'clock)
  c+ (bottom-right, 4 o'clock)
  a- (bottom, 6 o'clock)
  b- (bottom-left, 8 o'clock)
  c- (top-left, 10 o'clock)

THREE PHASES through active central reference:
  A: a+ ↔ nucleus ↔ a- (vertical winding)
  B: b+ ↔ nucleus ↔ b- (diagonal winding)
  C: c+ ↔ nucleus ↔ c- (diagonal winding)

Central nucleus is an ACTIVE REFERENCE that "leans" based on three-mode state:
  - A mode (state/DC): shifts nucleus baseline
  - B mode (rotation/AC): oscillates nucleus
  - C mode (gradient/RC): reactive biasing

Each hex vertex: half-bridge (PMOS high, NMOS low) with gate control.
Gate voltage controls current flow through phase windings to/from nucleus.
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer


class P0HexagonDirect:
    """P0 hexagon with active ternary leaning virtual ground at nucleus."""

    def __init__(self,
                 v_supply: float = 1.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 0.4,
                 buffer_rout: float = 0.1):
        self.v_supply = v_supply
        self.l_winding = winding_inductance
        self.r_winding = winding_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth  # Reduced from 1.0V to 0.4V for biological scale control
        self.buffer_rout = buffer_rout

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build P0 hexagon with star ground configuration.

        Star ground topology:
        - Six hex vertices (a+, b+, c+, a-, b-, c-)
        - Three phases (A, B, C): each has pos and neg halves
        - All six phase halves terminate at central star_ground
        - Star ground is active virtual bus reference maintained at 0.50V
        """
        circuit = TransientCircuit()

        # Single supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

        # Virtual bus ground (star ground): resistor divider + active buffer
        r_div = 100.0
        circuit.add(Resistor(
            id="R_div_top",
            a="+V",
            b="vg_raw",
            ohms=r_div
        ))
        circuit.add(Resistor(
            id="R_div_bottom",
            a="vg_raw",
            b="GND",
            ohms=r_div
        ))

        # Active op-amp buffer for star ground (low impedance, can source/sink current)
        circuit.add(OpAmpBuffer(
            id="star_ground_buffer",
            v_in="vg_raw",
            v_out="star_ground",
            gnd="GND",
            gain=1.0,
            Rout=self.buffer_rout,
            max_sourcing_mA=500.0,
            max_sinking_mA=500.0
        ))

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

        # Three phases: each phase connects both opposite vertices through star ground
        # Phase A: a+ → L → R → star_ground, and star_ground → R → L → a-
        # Phase B: b+ → L → R → star_ground, and star_ground → R → L → b-
        # Phase C: c+ → L → R → star_ground, and star_ground → R → L → c-
        phases = [
            ("A", "a_pos", "a_neg"),  # a+ ↔ star_ground ↔ a- (vertical)
            ("B", "b_pos", "b_neg"),  # b+ ↔ star_ground ↔ b- (diagonal)
            ("C", "c_pos", "c_neg"),  # c+ ↔ star_ground ↔ c- (diagonal)
        ]

        for phase_name, pos_node, neg_node in phases:
            # Positive half: pos_node → star_ground
            circuit.add(Inductor(
                id=f"L_{phase_name}_pos",
                a=pos_node,
                b=f"mid_{phase_name}_pos",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_pos",
                a=f"mid_{phase_name}_pos",
                b="star_ground",
                ohms=self.r_winding
            ))

            # Negative half: star_ground → neg_node
            circuit.add(Inductor(
                id=f"L_{phase_name}_neg",
                a="star_ground",
                b=f"mid_{phase_name}_neg",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_neg",
                a=f"mid_{phase_name}_neg",
                b=neg_node,
                ohms=self.r_winding
            ))

        # Initial state
        cap_states = {}
        ind_states = {
            "L_A_pos": InductorState(id="L_A_pos", current=0.0),
            "L_A_neg": InductorState(id="L_A_neg", current=0.0),
            "L_B_pos": InductorState(id="L_B_pos", current=0.0),
            "L_B_neg": InductorState(id="L_B_neg", current=0.0),
            "L_C_pos": InductorState(id="L_C_pos", current=0.0),
            "L_C_neg": InductorState(id="L_C_neg", current=0.0),
        }

        v_baseline = 0.50  # Biological baseline: 0.50V
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "vg_raw": v_baseline,
            "star_ground": v_baseline,  # Central active reference at baseline
            # Hex vertices all at baseline initially
            "a_pos": v_baseline,
            "b_pos": v_baseline,
            "c_pos": v_baseline,
            "a_neg": v_baseline,
            "b_neg": v_baseline,
            "c_neg": v_baseline,
            # Winding midpoints
            "mid_A_pos": v_baseline,
            "mid_A_neg": v_baseline,
            "mid_B_pos": v_baseline,
            "mid_B_neg": v_baseline,
            "mid_C_pos": v_baseline,
            "mid_C_neg": v_baseline,
        }

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon star ground circuit...")
    builder = P0HexagonDirect(v_supply=1.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built")
    print(f"  Layout: Pointy hexagon, clockwise a+ b+ c+ a- b- c-")
    print(f"  Phases: A (a+↔star_ground↔a-), B (b+↔star_ground↔b-), C (c+↔star_ground↔c-)")
    print(f"  Central star ground: active virtual bus at 0.50V baseline")
    print(f"  Topology: Six windings (three phases × pos/neg) all terminating at star ground")
    print(f"  Supply: {builder.v_supply}V, MOSFET Vth: {builder.vth}V")
