"""Reference simulator for recursive Field/Void routing.

This is an executable architecture probe, not a claim that the transition rules
are final hardware.

Five-scale ladder:
    Micro -> Small -> Medium -> Large -> Macro

Critical correction:
- Micro is the Cell / parser machine itself.
- A Cell is already a complete minimum Field/Void loop.
- M4/Dream/Admin/Executor belong to higher organization built from Cell output;
  they are not stuffed into the Cell just to make the code look uniform.

Known identities retained above the Cell layer:
- Field = Dream / expressive side
- Void = Administrator = Checker / compressive side
- M4 = brainstem router
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional
import json


class Scale(str, Enum):
    MICRO = "Micro"
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    MACRO = "Macro"


SCALE_ORDER = [Scale.MICRO, Scale.SMALL, Scale.MEDIUM, Scale.LARGE, Scale.MACRO]


class FieldMove(str, Enum):
    COMPRESS = "COMPRESS"
    HOLD = "HOLD"
    EXPRESS = "EXPRESS"


class VoidMove(str, Enum):
    DENY = "DENY"
    DEFER = "DEFER"
    CONFIRM = "CONFIRM"


class Lifecycle(str, Enum):
    IDLE = "Idle"
    PRIMED = "Primed"
    EXECUTING = "Executing"
    VECTORING = "Vectoring"
    RESOLVING = "Resolving"


@dataclass
class CellState:
    reference: str = "CENTER"
    last_input: str = ""
    last_field: FieldMove = FieldMove.HOLD
    last_void: VoidMove = VoidMove.DEFER
    cycle: int = 0


@dataclass
class CellReceipt:
    scale: Scale
    cycle: int
    raw_input: str
    reference_before: str
    binary_choice: str
    field_move: str
    void_check: str
    output: str
    reference_after: str
    compressed_summary: str


@dataclass
class HigherReceipt:
    scale: Scale
    cue: str
    lifecycle: Lifecycle
    field_proposal: str
    m4_route: str
    void_resolution: str
    committed: bool
    action: str
    next_reference: str
    compressed_summary: str


class CellParser:
    """Minimum Micro Field/Void machine.

    Jobs intentionally kept primitive:
      1. read one local input;
      2. compare it with the current local reference;
      3. form one opposed binary orientation;
      4. resolve one ternary Field move;
      5. let Void confirm/defer/deny;
      6. update or preserve the local reference;
      7. emit an auditable receipt.

    The Cell does not plan, imagine, globally route, or command a body.
    """

    def __init__(self) -> None:
        self.state = CellState()

    @staticmethod
    def _binary_choice(text: str) -> str:
        if any(word in text for word in ("no", "stop", "deny", "unsafe", "reject")):
            return "NO"
        if text:
            return "YES"
        return "GROUND"

    @staticmethod
    def _field_move(text: str) -> FieldMove:
        if any(word in text for word in ("go", "run", "faster", "expand", "express", "up")):
            return FieldMove.EXPRESS
        if any(word in text for word in ("slow", "compress", "reduce", "down")):
            return FieldMove.COMPRESS
        return FieldMove.HOLD

    @staticmethod
    def _void_check(text: str, binary_choice: str) -> VoidMove:
        if binary_choice == "NO":
            return VoidMove.DENY
        if not text or any(word in text for word in ("unknown", "maybe", "unclear")):
            return VoidMove.DEFER
        return VoidMove.CONFIRM

    def cycle(self, raw_input: str) -> CellReceipt:
        text = raw_input.strip().lower()
        reference_before = self.state.reference
        binary = self._binary_choice(text)
        field = self._field_move(text)
        void = self._void_check(text, binary)

        if void == VoidMove.DENY:
            output = "STOP"
            reference_after = reference_before
        elif void == VoidMove.DEFER:
            output = "HOLD"
            reference_after = reference_before
        else:
            output = field.value
            reference_after = f"{binary}:{field.value}"

        self.state.cycle += 1
        self.state.last_input = raw_input
        self.state.last_field = field
        self.state.last_void = void
        self.state.reference = reference_after

        summary = (
            f"Micro|B={binary}|F={field.value}|V={void.value}|"
            f"OUT={output}|REF={reference_after}"
        )

        return CellReceipt(
            scale=Scale.MICRO,
            cycle=self.state.cycle,
            raw_input=raw_input,
            reference_before=reference_before,
            binary_choice=binary,
            field_move=field.value,
            void_check=void.value,
            output=output,
            reference_after=reference_after,
            compressed_summary=summary,
        )


class FieldStateMachine:
    """Higher-scale Field / Dream side: proposes from compressed Cell state."""

    def step(self, cue: str) -> str:
        return f"PROPOSE:{cue}"


class M4Router:
    """Higher-scale brainstem router."""

    def route(self, scale: Scale, proposal: str) -> str:
        return f"{scale.value}:ROUTE:{proposal}"


class VoidStateMachine:
    """Higher-scale Void = Administrator = Checker."""

    def check(self, cue: str) -> VoidMove:
        lowered = cue.lower()
        if "v=deny" in lowered or "out=stop" in lowered:
            return VoidMove.DENY
        if "v=defer" in lowered or "out=hold" in lowered:
            return VoidMove.DEFER
        return VoidMove.CONFIRM


class ExecutorWorker:
    def execute(self, resolution: VoidMove) -> str:
        if resolution == VoidMove.DENY:
            return "OVERRIDE_STOP"
        if resolution == VoidMove.DEFER:
            return "HOLD"
        return "COMMIT"


class RecursiveFieldVoidSimulator:
    """Cell-first recursion through Micro -> Small -> Medium -> Large -> Macro."""

    def __init__(self) -> None:
        self.cell = CellParser()
        self.field = FieldStateMachine()
        self.m4 = M4Router()
        self.void = VoidStateMachine()
        self.executor = ExecutorWorker()

    def run_higher_scale(self, scale: Scale, cue: str) -> HigherReceipt:
        proposal = self.field.step(cue)
        routed = self.m4.route(scale, proposal)
        resolution = self.void.check(cue)
        action = self.executor.execute(resolution)
        committed = resolution != VoidMove.DEFER

        lifecycle = {
            VoidMove.DEFER: Lifecycle.PRIMED,
            VoidMove.CONFIRM: Lifecycle.EXECUTING,
            VoidMove.DENY: Lifecycle.RESOLVING,
        }[resolution]

        next_reference = f"{scale.value}:{resolution.value}:{action}"
        compressed_summary = (
            f"{scale.value}|V={resolution.value}|A={action}|SRC={cue}"
        )

        return HigherReceipt(
            scale=scale,
            cue=cue,
            lifecycle=lifecycle,
            field_proposal=proposal,
            m4_route=routed,
            void_resolution=resolution.value,
            committed=committed,
            action=action,
            next_reference=next_reference,
            compressed_summary=compressed_summary,
        )

    def run(self, cue: str) -> List[object]:
        receipts: List[object] = []
        micro = self.cell.cycle(cue)
        receipts.append(micro)
        upward = micro.compressed_summary

        for scale in SCALE_ORDER[1:]:
            higher = self.run_higher_scale(scale, upward)
            receipts.append(higher)
            upward = higher.compressed_summary
        return receipts


def main() -> None:
    sim = RecursiveFieldVoidSimulator()
    for cue in ("go forward", "slow down", "unknown signal", "stop"):
        print(f"\n=== {cue} ===")
        for receipt in sim.run(cue):
            print(json.dumps(asdict(receipt), indent=2))


if __name__ == "__main__":
    main()
