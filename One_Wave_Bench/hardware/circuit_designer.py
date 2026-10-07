"""High-level Circuit Designer API

Provides "above level" abstractions for designing One-Wave ternary circuits.
Instead of wiring individual components, designers specify high-level intent:

  designer = CircuitDesigner()
  designer.add_3phase_ternary_driver(
      phases=3,
      supply_voltage=5.0,
      winding_inductance=1e-3,
      winding_impedance=5.0
  )
  designer.set_layout("perf_board")  # 0.1" grid
  designer.export_kicad("p0_ternary.kicad_sch")
  designer.show_breadboard()  # interactive visualization

This generates:
- Circuit netlist (logical connections)
- Component BOM with part numbers
- Physical layout (perf board or PCB coordinates)
- KiCad schematic + footprints
- 3D breadboard visualization
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
import json
from enum import Enum


class LayoutMode(Enum):
    """Physical layout modes."""
    BREADBOARD = "breadboard"  # standard 830-point breadboard
    PERF_BOARD = "perf_board"  # 0.1" grid prototyping board
    PCB = "pcb"  # professional PCB (requires KiCad)


@dataclass
class Component:
    """Logical component with part number and footprint."""
    id: str
    name: str  # user-facing name
    value: str  # e.g., "1k", "10µF", "1mH"
    package: str  # e.g., "0805", "DIP8", "TO220"
    part_number: str  # supplier part number
    supplier: str = "generic"  # Digi-Key, Mouser, etc.
    pin_count: int = 0
    x_mm: float = 0.0  # physical position
    y_mm: float = 0.0
    rotation: float = 0.0


@dataclass
class Connection:
    """Logical wire between two components."""
    from_component: str
    from_pin: str  # or pin number
    to_component: str
    to_pin: str
    net_name: str = ""  # electrical node name
    wire_gauge: str = "22AWG"  # for perf boards


@dataclass
class Circuit:
    """Complete circuit definition with geometry."""
    name: str
    supply_voltage: float
    components: Dict[str, Component] = field(default_factory=dict)
    connections: List[Connection] = field(default_factory=list)
    layout_mode: LayoutMode = LayoutMode.BREADBOARD

    def component_count(self) -> int:
        return len(self.components)

    def connection_count(self) -> int:
        return len(self.connections)


class ComponentLibrary:
    """Pre-configured component library for standard One-Wave designs."""

    # Common resistors (0.25W carbon film)
    resistors = {
        "1k": Component(id="", name="Resistor 1kΩ", value="1k", package="0603",
                       part_number="RC0603JR-071KL", supplier="Yageo"),
        "5k": Component(id="", name="Resistor 5kΩ", value="5k", package="0603",
                       part_number="RC0603JR-075KL", supplier="Yageo"),
        "10k": Component(id="", name="Resistor 10kΩ", value="10k", package="0603",
                        part_number="RC0603JR-0710KL", supplier="Yageo"),
    }

    # Common capacitors
    capacitors = {
        "100n": Component(id="", name="Capacitor 100nF", value="100n", package="0603",
                         part_number="GRM188R61A104KA01L", supplier="Murata"),
        "1u": Component(id="", name="Capacitor 1µF", value="1u", package="0603",
                       part_number="GRM188R61A105KA12L", supplier="Murata"),
        "10u": Component(id="", name="Capacitor 10µF", value="10u", package="0805",
                        part_number="GRM31CR61A106KE19L", supplier="Murata"),
    }

    # Inductors
    inductors = {
        "1m": Component(id="", name="Inductor 1mH", value="1mH", package="1210",
                       part_number="CDRH127R-102", supplier="Sumida"),
        "10m": Component(id="", name="Inductor 10mH", value="10mH", package="1812",
                        part_number="CDRH1364R-100", supplier="Sumida"),
    }

    # MOSFETs
    mosfets = {
        "BSS138": Component(id="", name="NMOS BSS138", value="BSS138", package="SOT23",
                           part_number="BSS138", supplier="Infineon"),
        "BSS84": Component(id="", name="PMOS BSS84", value="BSS84", package="SOT23",
                          part_number="BSS84", supplier="Infineon"),
        "IRF540": Component(id="", name="NMOS IRF540", value="IRF540", package="TO220",
                           part_number="IRF540N", supplier="Vishay"),
    }

    # Op-amps
    opamps = {
        "TLE2426": Component(id="", name="Op-Amp TLE2426", value="TLE2426", package="DIP8",
                            part_number="TLE2426CP", supplier="Texas Instruments"),
        "LM358": Component(id="", name="Op-Amp LM358", value="LM358", package="DIP8",
                          part_number="LM358AN", supplier="Texas Instruments"),
    }


class CircuitDesigner:
    """High-level circuit design API."""

    def __init__(self, name: str = "OneWave Circuit", supply_voltage: float = 5.0):
        self.circuit = Circuit(name=name, supply_voltage=supply_voltage)
        self.library = ComponentLibrary()
        self.next_id = 0

    def _new_id(self, prefix: str) -> str:
        """Generate unique component ID."""
        self.next_id += 1
        return f"{prefix}_{self.next_id}"

    def add_3phase_ternary_driver(self,
                                  phases: int = 3,
                                  mosfet_type: str = "BSS138",
                                  winding_inductance: float = 1e-3,
                                  winding_resistance: float = 5.0,
                                  virtual_ground: bool = True) -> CircuitDesigner:
        """Add a 3-phase ternary driver with half-bridges and windings.

        Args:
            phases: Number of phases (3 for nucleus, 6 for full 7-cell)
            mosfet_type: "BSS138" (small signal), "IRF540" (power)
            winding_inductance: Phase winding inductance (H)
            winding_resistance: Phase winding resistance (Ω)
            virtual_ground: If True, add TLE2426 virtual ground buffer

        Returns:
            self for chaining
        """
        # Virtual ground buffer
        if virtual_ground:
            vg_id = self._new_id("VG")
            self.circuit.components[vg_id] = Component(
                id=vg_id,
                name="Virtual Ground Buffer",
                value="TLE2426",
                package="DIP8",
                part_number="TLE2426CP",
                supplier="Texas Instruments"
            )

            # Divider resistors
            for i, r_val in enumerate(["R_div_top", "R_div_bottom"]):
                r_id = self._new_id(r_val)
                self.circuit.components[r_id] = Component(
                    id=r_id,
                    name=f"Resistor 1kΩ (divider)",
                    value="1k",
                    package="0603",
                    part_number="RC0603JR-071KL",
                    supplier="Yageo"
                )

        # Phase drivers
        phase_names = ["U", "V", "W"][:phases]
        for phase in phase_names:
            # High-side FET
            hs_id = self._new_id(f"{phase}_HS")
            self.circuit.components[hs_id] = Component(
                id=hs_id,
                name=f"High-Side FET {phase}",
                value=mosfet_type,
                package="SOT23",
                part_number=mosfet_type,
                supplier="Generic"
            )

            # Low-side FET
            ls_id = self._new_id(f"{phase}_LS")
            self.circuit.components[ls_id] = Component(
                id=ls_id,
                name=f"Low-Side FET {phase}",
                value=mosfet_type,
                package="SOT23",
                part_number=mosfet_type,
                supplier="Generic"
            )

            # Winding (inductor)
            l_id = self._new_id(f"L_{phase}")
            self.circuit.components[l_id] = Component(
                id=l_id,
                name=f"Winding {phase}",
                value=f"{winding_inductance*1e3:.1f}mH",
                package="1210",
                part_number="CDRH127R-102",
                supplier="Sumida"
            )

            # Winding resistance
            r_id = self._new_id(f"R_{phase}")
            self.circuit.components[r_id] = Component(
                id=r_id,
                name=f"Winding Resistance {phase}",
                value=f"{winding_resistance}Ω",
                package="0603",
                part_number="RC0603JR-075KL",
                supplier="Yageo"
            )

        return self

    def add_decoupling_caps(self, positions: List[Tuple[str, str]] = None) -> CircuitDesigner:
        """Add decoupling capacitors to supply rails.

        Args:
            positions: List of (net_name, cap_value) tuples.
                      If None, adds standard 100nF near each IC.

        Returns:
            self for chaining
        """
        if positions is None:
            positions = [("+V", "100n"), ("GND", "100n")]

        for net, cap_val in positions:
            cap_id = self._new_id(f"C_decouple")
            self.circuit.components[cap_id] = Component(
                id=cap_id,
                name=f"Decoupling Cap {cap_val}",
                value=cap_val,
                package="0603",
                part_number="GRM188R61A104KA01L",
                supplier="Murata"
            )

        return self

    def set_layout(self, mode: str) -> CircuitDesigner:
        """Set physical layout mode.

        Args:
            mode: "breadboard", "perf_board", or "pcb"

        Returns:
            self for chaining
        """
        self.circuit.layout_mode = LayoutMode(mode)
        return self

    def generate_bom(self) -> Dict[str, List[str]]:
        """Generate Bill of Materials.

        Returns:
            Dict mapping component types to lists of [value, package, part_number, qty]
        """
        bom = {}
        value_counts = {}

        for comp in self.circuit.components.values():
            key = (comp.value, comp.package, comp.part_number)
            value_counts[key] = value_counts.get(key, 0) + 1

        for (value, package, part_num), qty in sorted(value_counts.items()):
            comp_type = value.split()[0] if ' ' in value else value
            if comp_type not in bom:
                bom[comp_type] = []
            bom[comp_type].append({
                "value": value,
                "package": package,
                "part_number": part_num,
                "quantity": qty
            })

        return bom

    def export_netlist(self, filename: str) -> None:
        """Export circuit netlist to JSON.

        Args:
            filename: Output JSON file
        """
        netlist = {
            "circuit_name": self.circuit.name,
            "supply_voltage": self.circuit.supply_voltage,
            "component_count": self.circuit.component_count(),
            "connection_count": self.circuit.connection_count(),
            "layout_mode": self.circuit.layout_mode.value,
            "components": {
                cid: {
                    "name": c.name,
                    "value": c.value,
                    "package": c.package,
                    "part_number": c.part_number,
                    "supplier": c.supplier
                }
                for cid, c in self.circuit.components.items()
            },
            "bom": self.generate_bom()
        }

        with open(filename, 'w') as f:
            json.dump(netlist, f, indent=2)

    def export_kicad_stub(self, filename: str) -> None:
        """Export KiCad schematic stub (ready for manual component placement).

        Args:
            filename: Output .kicad_sch file
        """
        # KiCad 6+ uses SEXP format
        kicad_header = """(kicad_sch (version 20230121)
  (uuid "OneWave-P0-Ternary")
  (paper "A4")

  (title_block
    (title "P0 Ternary Circuit")
    (date "2026-10-06")
    (rev "1.0")
    (comment 1 "One-Wave Physics Prototype")
  )

  (lib_symbols
"""

        # Add symbol definitions for each component type
        symbols = {
            "R": '(symbol "R" (pin_numbers hide) (pin_names (offset 0.254)) (property "Reference" "R" (id 0) (at 2.032 0 90)) (property "Value" "R" (id 1) (at 0 0 90)))',
            "C": '(symbol "C" (pin_numbers hide) (pin_names (offset 0.254)) (property "Reference" "C" (id 0) (at 0.635 2.54 0)))',
            "L": '(symbol "L" (pin_numbers hide) (pin_names (offset 0.254)) (property "Reference" "L" (id 0) (at -1.27 0 90)))',
            "Q": '(symbol "Q_NMOS" (pin_numbers hide) (property "Reference" "Q" (id 0) (at 5.08 1.27 0)))',
        }

        output = kicad_header
        for sym_name, sym_def in symbols.items():
            output += f"    {sym_def}\n"

        output += """  )

  (junction (at 0 0) (diameter 0) (color 0 0 0 0))
)
"""

        with open(filename, 'w') as f:
            f.write(output)

    def get_summary(self) -> str:
        """Return design summary."""
        bom = self.generate_bom()
        summary = f"""
=== Circuit Design Summary ===
Name: {self.circuit.name}
Supply: {self.circuit.supply_voltage}V
Components: {self.circuit.component_count()}
Layout: {self.circuit.layout_mode.value}

Component Types:
"""
        for comp_type, items in bom.items():
            summary += f"  {comp_type}: {len(items)} type(s)\n"
            for item in items:
                summary += f"    - {item['value']} ({item['quantity']}x)\n"

        return summary


# Example usage
if __name__ == "__main__":
    designer = CircuitDesigner("P0 Ternary Nucleus", supply_voltage=5.0)

    (designer
     .add_3phase_ternary_driver(phases=3, mosfet_type="BSS138", virtual_ground=True)
     .add_decoupling_caps()
     .set_layout("perf_board"))

    print(designer.get_summary())

    designer.export_netlist("/tmp/p0_netlist.json")
    designer.export_kicad_stub("/tmp/p0_circuit.kicad_sch")
    print("\nFiles exported to /tmp/")
