"""
Electrical parts for this batch: DCVoltageSource, Resistor, Wire, Ground.

Every component references nodes by plain string name. Two components that
use the same node name are, by definition, connected there -- a Wire only
exists to explicitly union two DIFFERENT node names into one electrical
node (e.g. "top_left" and "top_right" both being the same physical rail),
matching how a real breadboard row works.

No component here knows about any other component, any build, or any
project. It knows its own pins and its own value. See
../../../Virtual_Breadboard/00_RULES/architecture.md for why that separation
matters -- the same discipline applies here.
"""
from dataclasses import dataclass

# Canonical name for the implicit reference node when no explicit Ground
# component is used and there is no voltage source to fall back on.
GROUND = "0"


@dataclass(frozen=True)
class DCVoltageSource:
    """An ideal DC voltage source: holds volts = V(pos) - V(neg) exactly,
    regardless of load (no internal resistance modeled in this batch)."""
    id: str
    pos: str
    neg: str
    volts: float


@dataclass(frozen=True)
class Resistor:
    """An ideal linear resistor: real Ohm's law, I = (V(a) - V(b)) / ohms."""
    id: str
    a: str
    b: str
    ohms: float

    def __post_init__(self):
        if self.ohms <= 0:
            raise ValueError(f"Resistor {self.id!r} must have ohms > 0, got {self.ohms!r}")


@dataclass(frozen=True)
class Wire:
    """Declares that node a and node b are the same electrical node."""
    a: str
    b: str


@dataclass(frozen=True)
class Ground:
    """Marks `node` as the circuit's explicit 0V reference.

    This exists so the reference node is a deliberate choice, not an
    accident of solver internals -- see solver.py's reference-selection
    docstring for what happens if no Ground component is present.
    """
    node: str
