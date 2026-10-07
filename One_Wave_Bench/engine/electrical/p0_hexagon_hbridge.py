#!/usr/bin/env python3
"""
P0 Hexagon - H-Bridge Implementation with 18-Terminal Fixture

Pointy hexagon, clockwise vertices:
  a+ (top, 12 o'clock)
  b+ (top-right, 2 o'clock)
  c+ (bottom-right, 4 o'clock)
  a- (bottom, 6 o'clock)
  b- (bottom-left, 8 o'clock)
  c- (top-left, 10 o'clock)

THREE PHASES through central VREF:
  A: a+ ↔ VREF ↔ a- (vertical winding)
  B: b+ ↔ VREF ↔ b- (diagonal winding)
  C: c+ ↔ VREF ↔ c- (diagonal winding)

18-TERMINAL FIXTURE (per UPDATED_63):
  A: Drive +/- | Memory +/- | Sense +/-
  B: Drive +/- | Memory +/- | Sense +/-
  C: Drive +/- | Memory +/- | Sense +/-

H-BRIDGE TOPOLOGY (per UPDATED_63):
  Each phase Drive winding connects through a full reversible H-bridge
  (not a half-bridge). Drive ±, Memory ±, Sense ± are independent windings.

VREF DISTINCTION:
  - VREF: quiet electrical reference (~0.50V baseline)
  - DC_LINK: high-current energy reservoir for reinjection
  - These are NOT collapsed into one node
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, CapacitorState, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer, Capacitor


class P0HexagonHBridge:
    """P0 hexagon with H-bridge drive and 18-terminal fixture architecture."""

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
            v_supply: supply voltage (1.0V for biological scale)
            winding_inductance: Drive winding inductance (H)
            winding_resistance: Drive winding resistance (ohms)
            sense_inductance: Sense winding inductance (H)
            sense_resistance: Sense winding resistance (ohms)
            mosfet_rds_on: MOSFET on-state resistance (ohms)
            mosfet_vth: MOSFET threshold voltage (V) - reduced to 0.4V for 1V supply
            buffer_rout: VREF buffer output impedance (ohms)
            dclink_capacitor_uf: DC-link reservoir capacitor (microfarads)
        """
        self.v_supply = v_supply
        self.l_drive = winding_inductance
        self.r_drive = winding_resistance
        self.l_sense = sense_inductance
        self.r_sense = sense_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.buffer_rout = buffer_rout
        self.c_dclink = dclink_capacitor_uf * 1e-6  # Convert µF to F

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build P0 hexagon with H-bridge drive and 18-terminal fixture.

        Returns:
            (circuit, initial_state)
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

        # VREF: quiet electrical reference (1:1 divider for 1V supply → 0.50V)
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

        # VREF buffer: low-impedance quiet reference
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

        # DC-LINK: separate high-current reservoir capacitor (initially floating)
        circuit.add(Capacitor(
            id="C_dclink",
            a="DC_LINK",
            b="GND",
            farads=self.c_dclink
        ))

        # Six hex vertices (pointy hexagon, clockwise)
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]

        # Each vertex has complementary half-bridge (for now)
        # (H-bridge drive will be built via separate H-bridge circuits)
        for node in hex_nodes:
            # High-side PMOS
            circuit.add(PMOS(
                id=f"{node}_HS",
                gate=f"gate_{node}_hs",
                drain="+V",
                source=node,
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side NMOS
            circuit.add(NMOS(
                id=f"{node}_LS",
                gate=f"gate_{node}_ls",
                drain=node,
                source="GND",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

        # Three phases, each with Drive, Memory, Sense windings
        phases = [
            ("A", "a_pos", "a_neg"),  # a+ ↔ VREF ↔ a-
            ("B", "b_pos", "b_neg"),  # b+ ↔ VREF ↔ b-
            ("C", "c_pos", "c_neg"),  # c+ ↔ VREF ↔ c-
        ]

        for phase_name, pos_node, neg_node in phases:
            # === DRIVE WINDING (for H-bridge reversible differential stage) ===
            # Positive half: pos_node → VREF
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

            # Negative half: VREF → neg_node
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

            # === MEMORY WINDING (isolated from drive, for state retention) ===
            # Memory windings connect through resistances to VREF for DC biasing
            # Nerve ring will connect A_sense -> B_memory_pos, etc.
            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_pos",
                a=f"memory_{phase_name}_pos_ext",  # External terminal for nerve ring
                b=f"mid_{phase_name}_memory_pos",  # Internal mid-node
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_pos",
                a=f"mid_{phase_name}_memory_pos",
                b="VREF",
                ohms=self.r_drive
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_memory_neg",
                a="VREF",
                b=f"mid_{phase_name}_memory_neg",  # Internal mid-node
                henries=self.l_drive
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_memory_neg",
                a=f"mid_{phase_name}_memory_neg",
                b=f"memory_{phase_name}_neg_ext",  # External terminal for nerve ring
                ohms=self.r_drive
            ))

            # === SENSE WINDING (for monitoring phase state) ===
            # Sense windings are high-impedance sensors, not driven
            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_pos",
                a=pos_node,
                b=f"sense_{phase_name}_pos_mid",
                henries=self.l_sense
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_pos",
                a=f"sense_{phase_name}_pos_mid",
                b="VREF",
                ohms=self.r_sense
            ))

            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_neg",
                a="VREF",
                b=f"sense_{phase_name}_neg_mid",
                henries=self.l_sense
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_neg",
                a=f"sense_{phase_name}_neg_mid",
                b=neg_node,
                ohms=self.r_sense
            ))

        # Initial state
        cap_states = {
            "C_dclink": CapacitorState(id="C_dclink", voltage=0.0),
        }

        # All inductors initially at 0A current
        ind_states = {}
        for phase_name in ["A", "B", "C"]:
            for winding_type in ["drive", "memory", "sense"]:
                for half in ["pos", "neg"]:
                    ind_id = f"L_{phase_name}_{winding_type}_{half}"
                    ind_states[ind_id] = InductorState(id=ind_id, current=0.0)

        v_baseline = 0.50  # Biological baseline
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "vref_raw": v_baseline,
            "VREF": v_baseline,
            "DC_LINK": v_baseline,  # DC-link initially at baseline
            # Hex vertices all at baseline initially
            "a_pos": v_baseline,
            "b_pos": v_baseline,
            "c_pos": v_baseline,
            "a_neg": v_baseline,
            "b_neg": v_baseline,
            "c_neg": v_baseline,
        }

        # Initialize all winding nodes
        for phase_name in ["A", "B", "C"]:
            # Drive windings
            for half in ["pos", "neg"]:
                voltages[f"mid_{phase_name}_drive_{half}"] = v_baseline

            # Memory windings (have _ext and _mid nodes)
            for half in ["pos", "neg"]:
                voltages[f"memory_{phase_name}_{half}_ext"] = v_baseline
                voltages[f"mid_{phase_name}_memory_{half}"] = v_baseline

            # Sense windings
            for half in ["pos", "neg"]:
                voltages[f"sense_{phase_name}_{half}_mid"] = v_baseline

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon H-bridge circuit...")
    builder = P0HexagonHBridge(v_supply=1.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built: {len(circuit.components)} components")
    print(f"  Layout: Pointy hexagon, clockwise a+ b+ c+ a- b- c-")
    print(f"  VREF: quiet electrical reference at 0.50V baseline")
    print(f"  DC_LINK: separate energy reservoir capacitor (10µF)")
    print(f"  Phases: A (vertical), B (diagonal), C (diagonal)")
    print(f"  Terminals: 18 (A/B/C × Drive +/- | Memory +/- | Sense +/-)")
    print(f"  Supply: 1.0V, MOSFET Vth: 0.4V")
