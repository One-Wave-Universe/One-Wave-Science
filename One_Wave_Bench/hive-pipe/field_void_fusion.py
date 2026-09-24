#!/usr/bin/env python3
"""Novelty breaker and compact Field/Void fusion protocol.

This module coordinates two authorized AI workers without pretending they are
one consciousness. Void supplies compact inner oversight; Field supplies the
outer proposal/action voice. Shared state is intentionally small to reduce
repeated context and token use.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict, field
import json
from typing import Any

@dataclass
class Attempt:
    approach: str
    route_family: str
    tool_family: str
    result: str

class StubbornBreaker:
    def __init__(self, limit: int = 3):
        self.limit = limit
        self.attempts: list[Attempt] = []
    def add(self, attempt: Attempt) -> None:
        self.attempts.append(attempt)
    def must_change(self) -> dict[str, Any]:
        recent=self.attempts[-self.limit:]
        if len(recent) < self.limit:
            return {"required":False,"reason":"strike budget not exhausted"}
        same_route=len({a.route_family for a in recent})==1
        same_tool=len({a.tool_family for a in recent})==1
        same_approach=len({a.approach for a in recent})==1
        failed=all(a.result not in ("pass","success") for a in recent)
        required=failed and (same_route or same_tool or same_approach)
        return {
            "required":required,
            "change_route_family":required and same_route,
            "change_tool_family":required and same_tool,
            "change_approach":required and same_approach,
            "reason":"three repeated evidence-bearing failures" if required else "novelty change not required",
        }

@dataclass
class FusionPacket:
    goal: str
    reference: str
    known_good: str = ""
    delta: str = ""
    evidence: str = ""
    void_inner: str = ""
    field_outer: str = ""
    disagreement: str = ""
    next_move: str = ""
    protected: list[str] = field(default_factory=list)
    token_budget: int = 1200

    def compact(self) -> dict[str, Any]:
        return {k:v for k,v in asdict(self).items() if v not in ("", [], None)}

class FieldVoidFusion:
    """Temporary paired operating mode.

    VOID is the inner oversight channel.
    FIELD is the only outward action/response channel.
    Both read the same compact packet; neither repeats full history.
    """
    def __init__(self, packet: FusionPacket):
        self.packet=packet
        self.phase="VOID_INNER"
    def void(self, oversight: str, disagreement: str = "") -> dict[str, Any]:
        self.packet.void_inner=oversight.strip()
        self.packet.disagreement=disagreement.strip()
        self.phase="FIELD_OUTER"
        return {"phase":self.phase,"packet":self.packet.compact()}
    def field(self, outward: str, next_move: str = "") -> dict[str, Any]:
        if self.phase != "FIELD_OUTER":
            raise RuntimeError("Void inner pass must occur before Field outer pass")
        self.packet.field_outer=outward.strip()
        self.packet.next_move=next_move.strip()
        self.phase="REFERENCE_RETURN"
        return {"phase":self.phase,"packet":self.packet.compact()}
    def reset_cycle(self, delta: str = "", evidence: str = "") -> dict[str, Any]:
        self.packet.delta=delta.strip()
        self.packet.evidence=evidence.strip()
        self.packet.void_inner=""
        self.packet.field_outer=""
        self.packet.disagreement=""
        self.packet.next_move=""
        self.phase="VOID_INNER"
        return {"phase":self.phase,"packet":self.packet.compact()}

def encode_packet(packet: FusionPacket) -> str:
    return json.dumps(packet.compact(), separators=(",",":"), ensure_ascii=False)
