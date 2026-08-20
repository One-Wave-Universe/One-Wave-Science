"""Canonical executable Field state primitives for Branch 15."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, IntEnum
from typing import Tuple


class CycleStep(IntEnum):
    BEGIN = 1
    BUILD_OUT = 2
    HOLD = 3
    BUILD_RETURN = 4
    BREAK = 5
    LOOP = 6


class ScaleBand(IntEnum):
    MICRO_FLOOR = 0
    SMALL_LOW = 25
    MEDIUM_MID = 50
    LARGE_HIGH = 75
    MACRO_EXTREME = 100


class View(str, Enum):
    INWARD = "inward"
    OUTWARD = "outward"
    ACROSS = "across"
    OVER = "over"


class Operator(str, Enum):
    MINUS = "-"
    PLUS = "+"
    DIVIDE = "/"
    MULTIPLY = "x"


class Move(IntEnum):
    COMPRESS = -1
    HOLD = 0
    EXPAND = 1


class FieldChoice(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


class Gate(IntEnum):
    GATE_1 = 1
    GATE_2 = 2
    GATE_3 = 3
    MIRROR_4 = 4
    GATE_5 = 5
    GATE_6 = 6

    @property
    def boundary_alias(self) -> int:
        """Gate 4 is also the mirror/null boundary Gate 0."""
        return 0 if self is Gate.MIRROR_4 else int(self)


class MotionMode(str, Enum):
    POINT = "point"
    PATH = "path"
    FIELD_ROTATION = "field_rotation"


class Modulation(str, Enum):
    CARRIER = "carrier"
    BREATHING = "breathing"
    PHASE = "phase"


_FORWARD_GATES: Tuple[Gate, ...] = (
    Gate.GATE_1,
    Gate.GATE_2,
    Gate.GATE_3,
    Gate.MIRROR_4,
    Gate.GATE_5,
    Gate.GATE_6,
)
_REVERSE_GATES: Tuple[Gate, ...] = tuple(reversed(_FORWARD_GATES))


def gate_sequence(direction: int) -> Tuple[Gate, ...]:
    """Return the canonical gate traversal for +1 forward or -1 reverse."""
    if direction == 1:
        return _FORWARD_GATES
    if direction == -1:
        return _REVERSE_GATES
    raise ValueError("direction must be +1 or -1")


def advance_gate(gate: Gate, direction: int) -> Gate:
    """Advance one gate inside the canonical six-gate loop."""
    sequence = gate_sequence(direction)
    index = sequence.index(Gate(gate))
    return sequence[(index + 1) % len(sequence)]


def move_from_differential(differential: float, *, epsilon: float = 0.0) -> Move:
    """Map a signed differential to Compress/Hold/Expand deterministically."""
    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")
    if differential > epsilon:
        return Move.EXPAND
    if differential < -epsilon:
        return Move.COMPRESS
    return Move.HOLD


@dataclass(frozen=True)
class FieldMachineState:
    """Minimal canonical state carried by the Field computation."""

    active_field: str
    reference: float
    differential: float
    cycle_step: CycleStep
    scale: ScaleBand
    view: View
    operator: Operator
    move: Move
    choice: FieldChoice
    gate: Gate
    motion: MotionMode
    modulation: Modulation
    history: Tuple[str, ...] = ()

    def validate(self) -> None:
        if not isinstance(self.active_field, str) or not self.active_field.strip():
            raise ValueError("active_field must be a non-empty field identity")
        CycleStep(self.cycle_step)
        ScaleBand(self.scale)
        View(self.view)
        Operator(self.operator)
        Move(self.move)
        FieldChoice(self.choice)
        Gate(self.gate)
        MotionMode(self.motion)
        Modulation(self.modulation)
        if not isinstance(self.history, tuple):
            raise ValueError("history must be a tuple")
        if any(not isinstance(item, str) for item in self.history):
            raise ValueError("history entries must be strings")

    def with_differential(self, differential: float, *, epsilon: float = 0.0) -> "FieldMachineState":
        """Return a new state whose move is derived from the new differential."""
        next_state = replace(
            self,
            differential=differential,
            move=move_from_differential(differential, epsilon=epsilon),
        )
        next_state.validate()
        return next_state

    def advance(self, direction: int) -> "FieldMachineState":
        """Return a new state advanced one canonical gate."""
        next_state = replace(self, gate=advance_gate(self.gate, direction))
        next_state.validate()
        return next_state
