#!/usr/bin/env python3
"""Council protocol for Miniverse / Composite Agent Lab.

Multiple AI participants deliberate over one shared task. M4 is chair/body state,
Void is admin/inner oversight, Field is the sole outward voice, and specialists
contribute bounded evidence/proposals. The council stores structured turns, not
free-form cross-talk.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
import json, os
from pathlib import Path
from typing import Any

STATE=Path(os.environ.get("ONE_WAVE_COUNCIL_STATE", str(Path.home()/".local/state/one-wave-council/state.json"))).expanduser()

@dataclass
class Seat:
    id: str
    role: str
    authority: str
    provider: str = ""
    enabled: bool = True

@dataclass
class CouncilSession:
    id: str
    goal: str
    reference: str
    round: int = 0
    phase: str = "REFERENCE"
    seats: list[Seat] = field(default_factory=list)
    evidence: list[dict[str,Any]] = field(default_factory=list)
    proposals: list[dict[str,Any]] = field(default_factory=list)
    void_review: dict[str,Any] = field(default_factory=dict)
    m4_state: dict[str,Any] = field(default_factory=dict)
    field_output: str = ""
    status: str = "OPEN"

DEFAULT_SEATS=[
 Seat("m4","chair/body","state-and-threshold authority"),
 Seat("void","inner/admin","hold/correct/override/commit"),
 Seat("field","outer/senses","sole outward speech/action"),
 Seat("reference","reference","source/evidence gate"),
 Seat("doctor","diagnostic","failure diagnosis"),
 Seat("parser","parser","input/action normalization"),
 Seat("raccoon","scout","alternate approach discovery"),
]

def load_all():
    if not STATE.exists(): return {}
    return json.loads(STATE.read_text(encoding="utf-8"))

def save_all(data):
    STATE.parent.mkdir(parents=True,exist_ok=True)
    tmp=STATE.with_suffix(".tmp"); tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8"); tmp.replace(STATE)

def new_session(session_id: str, goal: str, reference: str) -> CouncilSession:
    return CouncilSession(id=session_id,goal=goal,reference=reference,seats=[Seat(**asdict(s)) for s in DEFAULT_SEATS])

def add_evidence(s: CouncilSession, seat: str, evidence_id: str, summary: str, source: str):
    s.evidence.append({"seat":seat,"id":evidence_id,"summary":summary,"source":source,"ts":datetime.now(timezone.utc).isoformat()})

def add_proposal(s: CouncilSession, seat: str, proposal: str, basis: list[str]):
    s.proposals.append({"round":s.round,"seat":seat,"proposal":proposal,"basis":basis})

def next_round(s: CouncilSession):
    s.round += 1; s.phase="DELIBERATE"

def void_decide(s: CouncilSession, decision: str, reason: str, selected: str = ""):
    decision=decision.upper()
    if decision not in ("ALLOW","CORRECT","OVERRIDE","HOLD","ESCALATE"): raise ValueError(decision)
    s.void_review={"decision":decision,"reason":reason,"selected":selected,"round":s.round}
    s.phase="M4_GATE"

def m4_gate(s: CouncilSession, action_open: bool, state: dict[str,Any]):
    s.m4_state=state
    s.phase="FIELD_OUTPUT" if action_open and s.void_review.get("decision")=="ALLOW" else "DELIBERATE"

def field_speak(s: CouncilSession, text: str):
    if s.phase!="FIELD_OUTPUT": raise RuntimeError("Field cannot speak before Void ALLOW + M4 gate")
    s.field_output=text; s.phase="REFERENCE_RETURN"

def close(s: CouncilSession):
    s.status="CLOSED"; s.phase="CLOSED"
