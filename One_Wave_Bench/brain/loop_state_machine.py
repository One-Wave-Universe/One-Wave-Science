"""Domain-neutral parser, mirrored loop state machine, and exact replay core.

This module is the Micro programming build underneath command-specific brains.
It deliberately contains no chess, motor, speech, or physics-domain rules.

Canonical loop contract:
    Micro -> Small -> Mid -> Large -> Macro
    -> mirror -> release
    -> Large -> Mid -> Small -> Micro
    -> phase -> next compression

Expression is required to return along the compression path in exact reverse
order. Event receipts are append-only and digest chained so active process
state can be rebuilt deterministically after restart.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
import shlex
from typing import Iterable


class Profile(str, Enum):
    FIELD = "field"
    VOID = "void"


class Scale(str, Enum):
    MICRO = "micro"
    SMALL = "small"
    MID = "mid"
    LARGE = "large"
    MACRO = "macro"


SCALE_UP = (Scale.MICRO, Scale.SMALL, Scale.MID, Scale.LARGE, Scale.MACRO)
SCALE_RETURN = tuple(reversed(SCALE_UP[:-1]))


class Lifecycle(str, Enum):
    IDLE = "idle"
    PRIMED = "primed"
    EXECUTING = "executing"
    VECTORING = "vectoring"
    RESOLVING = "resolving"


LIFECYCLE_NEXT = {
    Lifecycle.IDLE: Lifecycle.PRIMED,
    Lifecycle.PRIMED: Lifecycle.EXECUTING,
    Lifecycle.EXECUTING: Lifecycle.VECTORING,
    Lifecycle.VECTORING: Lifecycle.RESOLVING,
    Lifecycle.RESOLVING: Lifecycle.IDLE,
}


class LoopPhase(str, Enum):
    READY = "ready"
    COMPRESS = "compress"
    MIRROR = "mirror"
    RELEASE = "release"
    EXPRESS = "express"
    PHASE = "phase"


class EventOp(str, Enum):
    PROFILE = "profile"
    STATE = "state"
    COMPRESS = "compress"
    MIRROR = "mirror"
    RELEASE = "release"
    EXPRESS = "express"
    PHASE = "phase"
    REMEMBER = "remember"
    FORGET = "forget"


@dataclass(frozen=True, slots=True)
class LoopEvent:
    op: EventOp
    value: str | None = None
    key: str | None = None

    def canonical_json(self) -> str:
        return json.dumps(
            {"key": self.key, "op": self.op.value, "value": self.value},
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_canonical_json(cls, payload: str) -> "LoopEvent":
        raw = json.loads(payload)
        if set(raw) != {"key", "op", "value"}:
            raise ValueError("event payload has unexpected fields")
        return cls(EventOp(raw["op"]), value=raw["value"], key=raw["key"])


def _enum_value(enum_cls, token: str):
    try:
        return enum_cls(token.lower()).value
    except ValueError as exc:
        allowed = ", ".join(item.value for item in enum_cls)
        raise ValueError(f"expected one of: {allowed}") from exc


def parse_line(line: str) -> LoopEvent | None:
    """Parse one small deterministic loop DSL statement."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    tokens = shlex.split(stripped, comments=True, posix=True)
    if not tokens:
        return None

    try:
        op = EventOp(tokens[0].lower())
    except ValueError as exc:
        raise ValueError(f"unknown loop operation: {tokens[0]!r}") from exc

    if op is EventOp.PROFILE:
        if len(tokens) != 2:
            raise ValueError("PROFILE requires exactly one value")
        return LoopEvent(op, _enum_value(Profile, tokens[1]))

    if op is EventOp.STATE:
        if len(tokens) != 2:
            raise ValueError("STATE requires exactly one value")
        return LoopEvent(op, _enum_value(Lifecycle, tokens[1]))

    if op in (EventOp.COMPRESS, EventOp.EXPRESS):
        if len(tokens) != 2:
            raise ValueError(f"{op.value.upper()} requires exactly one scale")
        scale = _enum_value(Scale, tokens[1])
        if op is EventOp.EXPRESS and scale == Scale.MACRO.value:
            raise ValueError("EXPRESS starts below the Macro mirror; Macro is not repeated")
        return LoopEvent(op, scale)

    if op in (EventOp.MIRROR, EventOp.RELEASE, EventOp.PHASE):
        if len(tokens) != 1:
            raise ValueError(f"{op.value.upper()} takes no arguments")
        return LoopEvent(op)

    if op is EventOp.REMEMBER:
        if len(tokens) < 3:
            raise ValueError("REMEMBER requires a key and value")
        return LoopEvent(op, value=" ".join(tokens[2:]), key=tokens[1])

    if op is EventOp.FORGET:
        if len(tokens) != 2:
            raise ValueError("FORGET requires exactly one key")
        return LoopEvent(op, key=tokens[1])

    raise AssertionError("unreachable")


def parse_program(text: str) -> tuple[LoopEvent, ...]:
    events = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        try:
            event = parse_line(line)
        except ValueError as exc:
            raise ValueError(f"line {line_number}: {exc}") from exc
        if event is not None:
            events.append(event)
    return tuple(events)


@dataclass(frozen=True, slots=True)
class EventReceipt:
    sequence: int
    event_json: str
    previous_digest: str
    digest: str

    @classmethod
    def create(cls, sequence: int, event: LoopEvent, previous_digest: str) -> "EventReceipt":
        event_json = event.canonical_json()
        material = f"{sequence}|{event_json}|{previous_digest}"
        digest = sha256(material.encode("utf-8")).hexdigest()
        return cls(sequence, event_json, previous_digest, digest)

    def event(self) -> LoopEvent:
        return LoopEvent.from_canonical_json(self.event_json)

    def verify(self) -> None:
        expected = self.create(self.sequence, self.event(), self.previous_digest)
        if self != expected:
            raise ValueError(f"invalid event receipt at sequence {self.sequence}")

    def to_json(self) -> str:
        return json.dumps(
            {
                "digest": self.digest,
                "event_json": self.event_json,
                "previous_digest": self.previous_digest,
                "sequence": self.sequence,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_json(cls, line: str) -> "EventReceipt":
        receipt = cls(**json.loads(line))
        receipt.verify()
        return receipt


@dataclass(slots=True)
class LoopState:
    profile: Profile | None = None
    lifecycle: Lifecycle = Lifecycle.IDLE
    phase: LoopPhase = LoopPhase.READY
    compression_route: list[Scale] = field(default_factory=list)
    expression_route: list[Scale] = field(default_factory=list)
    memory: dict[str, str] = field(default_factory=dict)
    cycle: int = 0

    def snapshot(self) -> dict[str, object]:
        return {
            "compression_route": [scale.value for scale in self.compression_route],
            "cycle": self.cycle,
            "expression_route": [scale.value for scale in self.expression_route],
            "lifecycle": self.lifecycle.value,
            "memory": dict(sorted(self.memory.items())),
            "phase": self.phase.value,
            "profile": None if self.profile is None else self.profile.value,
        }


class LoopStateMachine:
    """Strict state machine for the shared Micro loop build."""

    def __init__(self):
        self.state = LoopState()
        self._receipts: list[EventReceipt] = []

    @property
    def receipts(self) -> tuple[EventReceipt, ...]:
        return tuple(self._receipts)

    def _apply(self, event: LoopEvent) -> None:
        state = self.state

        if event.op is EventOp.PROFILE:
            profile = Profile(event.value)
            if state.profile is None:
                state.profile = profile
            elif state.profile is not profile:
                raise ValueError("Field/Void profile cannot silently change inside a build")
            return

        if event.op is EventOp.STATE:
            target = Lifecycle(event.value)
            expected = LIFECYCLE_NEXT[state.lifecycle]
            if target is not expected:
                raise ValueError(
                    f"illegal lifecycle transition: {state.lifecycle.value} -> {target.value}; expected {expected.value}"
                )
            state.lifecycle = target
            return

        if event.op is EventOp.REMEMBER:
            assert event.key is not None and event.value is not None
            state.memory[event.key] = event.value
            return

        if event.op is EventOp.FORGET:
            assert event.key is not None
            state.memory.pop(event.key, None)
            return

        if event.op is EventOp.COMPRESS:
            if state.phase not in (LoopPhase.READY, LoopPhase.PHASE, LoopPhase.COMPRESS):
                raise ValueError(f"cannot COMPRESS during {state.phase.value}")
            expected_index = len(state.compression_route)
            if expected_index >= len(SCALE_UP):
                raise ValueError("compression already reached Macro; MIRROR is required")
            scale = Scale(event.value)
            expected = SCALE_UP[expected_index]
            if scale is not expected:
                raise ValueError(f"compression route must rise in order; expected {expected.value}")
            if expected_index == 0:
                state.expression_route.clear()
            state.compression_route.append(scale)
            state.phase = LoopPhase.COMPRESS
            return

        if event.op is EventOp.MIRROR:
            if state.phase is not LoopPhase.COMPRESS or tuple(state.compression_route) != SCALE_UP:
                raise ValueError("MIRROR requires complete Micro->Macro compression")
            state.phase = LoopPhase.MIRROR
            return

        if event.op is EventOp.RELEASE:
            if state.phase is not LoopPhase.MIRROR:
                raise ValueError("RELEASE requires the mirror turnaround")
            state.phase = LoopPhase.RELEASE
            return

        if event.op is EventOp.EXPRESS:
            if state.phase not in (LoopPhase.RELEASE, LoopPhase.EXPRESS):
                raise ValueError("EXPRESS requires RELEASE and then exact reverse return")
            expected_index = len(state.expression_route)
            if expected_index >= len(SCALE_RETURN):
                raise ValueError("expression already returned to Micro; PHASE is required")
            scale = Scale(event.value)
            expected = SCALE_RETURN[expected_index]
            if scale is not expected:
                raise ValueError(
                    "expression must retrace compression in reverse; "
                    f"expected {expected.value}"
                )
            state.expression_route.append(scale)
            state.phase = LoopPhase.EXPRESS
            return

        if event.op is EventOp.PHASE:
            if state.phase is not LoopPhase.EXPRESS or tuple(state.expression_route) != SCALE_RETURN:
                raise ValueError("PHASE requires complete Large->Micro expression return")
            state.cycle += 1
            state.phase = LoopPhase.PHASE
            state.compression_route.clear()
            state.expression_route.clear()
            return

        raise AssertionError("unreachable")

    def apply(self, event: LoopEvent) -> EventReceipt:
        self._apply(event)
        previous = self._receipts[-1].digest if self._receipts else "GENESIS"
        receipt = EventReceipt.create(len(self._receipts), event, previous)
        self._receipts.append(receipt)
        return receipt

    def run(self, text: str) -> tuple[EventReceipt, ...]:
        for event in parse_program(text):
            self.apply(event)
        return self.receipts

    @classmethod
    def rebuild(cls, receipts: Iterable[EventReceipt | str]) -> "LoopStateMachine":
        machine = cls()
        for item in receipts:
            receipt = EventReceipt.from_json(item) if isinstance(item, str) else item
            receipt.verify()
            expected_sequence = len(machine._receipts)
            previous = machine._receipts[-1].digest if machine._receipts else "GENESIS"
            if receipt.sequence != expected_sequence:
                raise ValueError("event receipts must be contiguous and ordered")
            if receipt.previous_digest != previous:
                raise ValueError("event receipt chain is broken")
            machine._apply(receipt.event())
            machine._receipts.append(receipt)
        return machine


def canonical_cycle(profile: Profile) -> str:
    """Return a complete minimal loop program for smoke tests and examples."""
    lines = [
        f"PROFILE {profile.value}",
        "STATE primed",
        "STATE executing",
        "COMPRESS micro",
        "COMPRESS small",
        "COMPRESS mid",
        "COMPRESS large",
        "COMPRESS macro",
        "MIRROR",
        "RELEASE",
        "EXPRESS large",
        "EXPRESS mid",
        "EXPRESS small",
        "EXPRESS micro",
        "PHASE",
        "STATE vectoring",
        "STATE resolving",
        "STATE idle",
    ]
    return "\n".join(lines)
