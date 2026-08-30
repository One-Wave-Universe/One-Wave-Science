"""Reference simulator for recursive Field/Void routing.

This is an executable architecture probe, not a claim that the transition rules
are final hardware. It preserves the current identities and five-scale ladder:

Micro -> Small -> Medium -> Large -> Macro

Known identities used here:
- Field = Dream / expressive side
- Void = Administrator = Checker / compressive side
- M4 = brainstem router

The simulator keeps two distinct state machines (Field and Void), routes through
M4, records a receipt, and compresses the accepted result upward one scale.
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
class Packet:
    scale: Scale
    cue: str
    field_move: FieldMove
    confidence: float
    urgency: float
    prior_receipt: Optional[Dict] = None


@dataclass
class Receipt:
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


class ParserWorker:
    """Tiny deterministic parser / cell layer."""

    def parse(self, scale: Scale, cue: str, prior_receipt: Optional[Dict] = None) -> Packet:
        text = cue.strip().lower()
        if any(word in text for word in ("stop", "deny", "unsafe")):
            move = FieldMove.HOLD
            confidence = 0.95
            urgency = 1.0
        elif any(word in text for word in ("go", "run", "faster", "expand", "express")):
            move = FieldMove.EXPRESS
            confidence = 0.8
            urgency = 0.75
        elif any(word in text for word in ("slow", "compress", "reduce")):
            move = FieldMove.COMPRESS
            confidence = 0.8
            urgency = 0.5
        else:
            move = FieldMove.HOLD
            confidence = 0.5
            urgency = 0.25
        return Packet(scale, cue, move, confidence, urgency, prior_receipt)


class FieldStateMachine:
    """Dream / Field: generates the expressive proposal."""

    def step(self, packet: Packet) -> str:
        return f"{packet.field_move.value}:{packet.cue}"


class M4Router:
    """Brainstem router: fast routing, timing, scale and compression boundary."""

    def route(self, packet: Packet, proposal: str) -> str:
        lane = "FAST" if packet.urgency >= 0.75 else "NORMAL"
        return f"{packet.scale.value}:{lane}:{proposal}"


class VoidStateMachine:
    """Void = Administrator = Checker: confirms, defers, or denies."""

    def check(self, packet: Packet, routed: str) -> VoidMove:
        text = packet.cue.lower()
        if any(word in text for word in ("stop", "deny", "unsafe")):
            return VoidMove.DENY
        if packet.confidence < 0.6:
            return VoidMove.DEFER
        return VoidMove.CONFIRM


class ExecutorWorker:
    """Commits only what Void/Admin/Checker allows."""

    def execute(self, field_move: FieldMove, resolution: VoidMove) -> str:
        if resolution == VoidMove.DENY:
            return "OVERRIDE_STOP"
        if resolution == VoidMove.DEFER:
            return "HOLD"
        return field_move.value


class RecursiveFieldVoidSimulator:
    """Five-worker reference flow across Micro->Small->Medium->Large->Macro."""

    def __init__(self) -> None:
        self.parser = ParserWorker()          # Cells / parser
        self.field = FieldStateMachine()      # Dream / Field
        self.m4 = M4Router()                  # M4 brainstem router
        self.void = VoidStateMachine()        # Void/Admin/Checker
        self.executor = ExecutorWorker()      # Executor

    def run_scale(self, scale: Scale, cue: str, prior: Optional[Receipt]) -> Receipt:
        prior_dict = asdict(prior) if prior else None
        packet = self.parser.parse(scale, cue, prior_dict)
        proposal = self.field.step(packet)
        routed = self.m4.route(packet, proposal)
        resolution = self.void.check(packet, routed)
        action = self.executor.execute(packet.field_move, resolution)
        committed = resolution == VoidMove.CONFIRM or resolution == VoidMove.DENY

        lifecycle = {
            VoidMove.DEFER: Lifecycle.PRIMED,
            VoidMove.CONFIRM: Lifecycle.EXECUTING,
            VoidMove.DENY: Lifecycle.RESOLVING,
        }[resolution]

        next_reference = f"{scale.value}:{resolution.value}:{action}"
        compressed_summary = (
            f"{scale.value}|F={packet.field_move.value}|V={resolution.value}|A={action}"
        )

        return Receipt(
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

    def run(self, cue: str) -> List[Receipt]:
        receipts: List[Receipt] = []
        prior: Optional[Receipt] = None
        for scale in SCALE_ORDER:
            scale_cue = cue if prior is None else prior.compressed_summary
            prior = self.run_scale(scale, scale_cue, prior)
            receipts.append(prior)
        return receipts


def main() -> None:
    sim = RecursiveFieldVoidSimulator()
    for cue in ("go forward", "slow down", "unknown signal", "stop"):
        print(f"\n=== {cue} ===")
        for receipt in sim.run(cue):
            print(json.dumps(asdict(receipt), indent=2))


if __name__ == "__main__":
    main()
