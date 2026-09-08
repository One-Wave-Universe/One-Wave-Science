#!/usr/bin/env python3
"""Miniverse self-loop: no permission ask per tick.

Permission is the contract loaded at boot.
Local Void is a function, not a conversation.
Avatar / human is only called on WHY FORWARD.
Durable Baseline Zero is never rewritten by this loop.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
import time
from typing import Iterable


LIFECYCLE = ("Idle", "Primed", "Executing", "Vectoring", "Resolving")


class Route(str, Enum):
    DROP = "DROP"
    LOCAL = "LOCAL"
    HOLD = "HOLD"
    FORWARD = "FORWARD"


class Move(str, Enum):
    DOWN = "DOWN"
    HOLD = "HOLD"
    UP = "UP"


@dataclass(frozen=True)
class Event:
    source: str
    change: float
    confidence: float
    urgency: float
    evidence: str
    ts: float = field(default_factory=time.time)

    def receipt(self, why_forward: str | None, route: Route) -> dict:
        return {
            "source": self.source,
            "local_timestamp": self.ts,
            "change": self.change,
            "confidence": self.confidence,
            "urgency": self.urgency,
            "evidence_refs": self.evidence,
            "why_forward": why_forward,
            "route": route.value,
        }


@dataclass
class BodyState:
    lifecycle: str = "Idle"
    detections: int = 0
    dropped: int = 0
    local_acts: int = 0
    holds: int = 0
    forwards: int = 0
    last_move: str = Move.HOLD.value
    generation: int = 0

    def snapshot(self) -> dict:
        return asdict(self)


LOCAL_CONTRACT = {
    "mic.onset": {"min_change": 0.35, "min_conf": 0.6, "act": Move.HOLD},
    "vision.motion": {"min_change": 0.25, "min_conf": 0.55, "act": Move.HOLD},
    "body.heat": {"min_change": 0.4, "min_conf": 0.7, "act": Move.DOWN},
    "nerve.rest": {"min_change": 0.0, "min_conf": 0.0, "act": Move.HOLD},
}

FORWARD_CONTRACT = {
    "speech.command": {"min_change": 0.5, "min_conf": 0.8},
    "vision.approach": {"min_change": 0.6, "min_conf": 0.75},
}


class LocalVoid:
    """Oversight without a chat. ALLOW local contract. HOLD baseline. FORWARD only with why."""

    def decide(self, event: Event) -> tuple[Route, Move, str | None]:
        if event.source in FORWARD_CONTRACT:
            spec = FORWARD_CONTRACT[event.source]
            if event.change >= spec["min_change"] and event.confidence >= spec["min_conf"]:
                why = f"{event.source} intersects live body; structured, not noise"
                return Route.FORWARD, Move.HOLD, why
            return Route.DROP, Move.HOLD, None

        spec = LOCAL_CONTRACT.get(event.source)
        if spec is None:
            return Route.HOLD, Move.HOLD, None

        if event.change < spec["min_change"] or event.confidence < spec["min_conf"]:
            return Route.DROP, Move.HOLD, None

        return Route.LOCAL, spec["act"], None


class SelfLoop:
    def __init__(self, void: LocalVoid | None = None) -> None:
        self.void = void or LocalVoid()
        self.body = BodyState()
        self.escalations: list[dict] = []

    def tick(self, event: Event) -> dict:
        self.body.lifecycle = "Primed"
        self.body.detections += 1
        route, move, why = self.void.decide(event)
        self.body.lifecycle = "Executing"

        if route is Route.DROP:
            self.body.dropped += 1
            self.body.last_move = Move.HOLD.value
            self.body.lifecycle = "Resolving"
            return event.receipt(None, route)

        if route is Route.HOLD:
            self.body.holds += 1
            self.body.last_move = Move.HOLD.value
            self.body.lifecycle = "Resolving"
            return event.receipt(None, route)

        if route is Route.LOCAL:
            self.body.local_acts += 1
            self.body.last_move = move.value
            self.body.lifecycle = "Resolving"
            return event.receipt(None, route)

        self.body.forwards += 1
        self.body.lifecycle = "Vectoring"
        packet = event.receipt(why, route)
        packet["body_state_refs"] = self.body.snapshot()
        self.escalations.append(packet)
        self.body.lifecycle = "Resolving"
        return packet

    def run(self, events: Iterable[Event]) -> dict:
        receipts = [self.tick(event) for event in events]
        return {
            "body": self.body.snapshot(),
            "receipts": receipts,
            "escalations": list(self.escalations),
            "asked_permission": False,
            "baseline_generation_unchanged": self.body.generation == 0,
        }


def demo_stream() -> list[Event]:
    return [
        Event("mic.onset", 0.1, 0.2, 0.1, "noise-floor"),
        Event("mic.onset", 0.5, 0.8, 0.4, "speech-like-onset"),
        Event("vision.motion", 0.3, 0.7, 0.3, "edge-delta"),
        Event("speech.command", 0.9, 0.92, 0.95, "token:stop"),
        Event("unknown.sparkle", 0.99, 0.99, 0.99, "not-in-contract"),
        Event("nerve.rest", 0.0, 1.0, 0.0, "idle"),
    ]


def main() -> int:
    result = SelfLoop().run(demo_stream())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
