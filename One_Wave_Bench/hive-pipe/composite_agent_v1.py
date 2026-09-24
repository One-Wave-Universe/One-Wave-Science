#!/usr/bin/env python3
"""Runnable composite Field/Void state-machine loop.

Provider-neutral runtime: Field and Void are adapters over the same persistent
state. Void is admin/inner oversight. Field owns senses, speech, and actions.
The controller advances one bounded cycle at a time and records every transition.
"""

from __future__ import annotations
import argparse, json, os, sys, time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

STATE_PATH = Path(os.environ.get("ONE_WAVE_COMPOSITE_STATE", str(Path.home()/".local/state/one-wave-composite/state.json"))).expanduser()
LEDGER_PATH = Path(os.environ.get("ONE_WAVE_COMPOSITE_LEDGER", str(Path.home()/".local/state/one-wave-composite/transitions.jsonl"))).expanduser()

PHASES = ("INPUT","FIELD_PERCEIVE","VOID_ADMIN","FIELD_ACT","RESULT","VOID_COMMIT","OUTPUT","HOLD")

@dataclass
class CompositeState:
    session_id: str
    phase: str = "INPUT"
    cycle: int = 0
    goal: str = ""
    reference: str = ""
    world: dict[str,Any] = field(default_factory=dict)
    plan: dict[str,Any] = field(default_factory=dict)
    permissions: dict[str,Any] = field(default_factory=dict)
    field: dict[str,Any] = field(default_factory=dict)
    void: dict[str,Any] = field(default_factory=dict)
    action: dict[str,Any] = field(default_factory=dict)
    result: dict[str,Any] = field(default_factory=dict)
    output: str = ""
    protected: list[str] = field(default_factory=list)
    strikes: int = 0
    token_budget: int = 1200
    updated_at: str = ""

    def touch(self):
        self.updated_at=datetime.now(timezone.utc).isoformat()

class AgentAdapter(Protocol):
    def call(self, role: str, packet: dict[str,Any]) -> dict[str,Any]: ...

class ToolAdapter(Protocol):
    def execute(self, action: dict[str,Any], state: CompositeState) -> dict[str,Any]: ...

class JsonLineAgent:
    """Simple stdio adapter for testing or external model wrappers.

    Writes one JSON request to stdout and reads one JSON response from stdin.
    In production this interface can be replaced by OpenClaw, MCP, API, or local
    model adapters without changing the state machine.
    """
    def call(self, role: str, packet: dict[str,Any]) -> dict[str,Any]:
        print(json.dumps({"type":"agent_call","role":role,"packet":packet}, separators=(",",":")), flush=True)
        line=sys.stdin.readline()
        if not line: raise RuntimeError(f"{role} adapter returned no response")
        data=json.loads(line)
        if not isinstance(data,dict): raise RuntimeError(f"{role} response must be object")
        return data

class NoopTools:
    def execute(self, action: dict[str,Any], state: CompositeState) -> dict[str,Any]:
        return {"ok":True,"kind":"noop","action":action,"evidence":"NOOP_EXECUTED"}

def save_state(state: CompositeState):
    state.touch(); STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp=STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(asdict(state), indent=2, sort_keys=True)+"\n", encoding="utf-8")
    tmp.replace(STATE_PATH)

def load_state(session_id: str="default") -> CompositeState:
    if not STATE_PATH.exists(): return CompositeState(session_id=session_id)
    return CompositeState(**json.loads(STATE_PATH.read_text(encoding="utf-8")))

def receipt(state: CompositeState, event: str, detail: dict[str,Any]):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    row={"timestamp":datetime.now(timezone.utc).isoformat(),"session_id":state.session_id,"cycle":state.cycle,"phase":state.phase,"event":event,"detail":detail}
    with LEDGER_PATH.open("a",encoding="utf-8") as f: f.write(json.dumps(row,sort_keys=True)+"\n")

def compact_packet(state: CompositeState, include: tuple[str,...]) -> dict[str,Any]:
    raw=asdict(state)
    base={"session_id":state.session_id,"cycle":state.cycle,"goal":state.goal,"reference":state.reference,"phase":state.phase,"protected":state.protected,"token_budget":state.token_budget}
    for k in include:
        v=raw.get(k)
        if v not in ({},[],None,""): base[k]=v
    return base

class CompositeLoop:
    def __init__(self, field_agent: AgentAdapter, void_agent: AgentAdapter, tools: ToolAdapter):
        self.field_agent=field_agent; self.void_agent=void_agent; self.tools=tools

    def ingest(self, state: CompositeState, user_input: str, sensor: dict[str,Any]|None=None):
        state.cycle += 1; state.phase="FIELD_PERCEIVE"; state.output=""
        state.world={"input":user_input,"sensor":sensor or {}}
        state.result={}; state.action={}
        receipt(state,"input",state.world); save_state(state)

    def field_perceive(self, state: CompositeState):
        packet=compact_packet(state,("world","permissions","result","plan"))
        out=self.field_agent.call("FIELD_PERCEIVE",packet)
        state.field={"perception":out.get("perception",""),"proposal":out.get("proposal",{}),"speech_draft":out.get("speech_draft","")}
        state.plan=out.get("plan",state.plan) if isinstance(out.get("plan",state.plan),dict) else state.plan
        state.phase="VOID_ADMIN"; receipt(state,"field_perceive",state.field); save_state(state)

    def void_admin(self, state: CompositeState):
        packet=compact_packet(state,("world","field","plan","result"))
        out=self.void_agent.call("VOID_ADMIN",packet)
        decision=str(out.get("decision","HOLD")).upper()
        state.void={"decision":decision,"inner_voice":out.get("inner_voice",""),"correction":out.get("correction",""),"reason":out.get("reason","")}
        state.permissions=out.get("permissions",{}) if isinstance(out.get("permissions",{}),dict) else {}
        if decision in ("HOLD","ESCALATE"):
            state.phase="OUTPUT"; state.output=out.get("outward_instruction") or state.void["reason"] or decision
        else:
            state.phase="FIELD_ACT"
        receipt(state,"void_admin",state.void); save_state(state)

    def field_act(self, state: CompositeState):
        packet=compact_packet(state,("world","field","void","permissions","plan"))
        out=self.field_agent.call("FIELD_ACT",packet)
        state.action=out.get("action",{}) if isinstance(out.get("action",{}),dict) else {}
        state.output=str(out.get("speech",""))
        state.phase="RESULT"; receipt(state,"field_act",{"action":state.action,"speech":state.output}); save_state(state)

    def execute(self, state: CompositeState):
        state.result=self.tools.execute(state.action,state)
        state.phase="VOID_COMMIT"; receipt(state,"result",state.result); save_state(state)

    def void_commit(self, state: CompositeState):
        packet=compact_packet(state,("world","field","void","action","result","plan"))
        out=self.void_agent.call("VOID_COMMIT",packet)
        commit=bool(out.get("commit",False))
        if commit:
            state.strikes=0
        else:
            state.strikes += 1
        state.void.update({"commit":commit,"post_reason":out.get("reason",""),"next_state":out.get("next_state","")})
        if out.get("goal") is not None: state.goal=str(out.get("goal"))
        if out.get("reference") is not None: state.reference=str(out.get("reference"))
        state.phase="OUTPUT"; receipt(state,"void_commit",{"commit":commit,"strikes":state.strikes,"reason":out.get("reason","")}); save_state(state)

    def cycle_once(self, state: CompositeState, user_input: str, sensor: dict[str,Any]|None=None) -> CompositeState:
        self.ingest(state,user_input,sensor)
        self.field_perceive(state)
        self.void_admin(state)
        if state.phase=="FIELD_ACT":
            self.field_act(state)
            self.execute(state)
            self.void_commit(state)
        receipt(state,"output",{"text":state.output}); save_state(state)
        return state

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--session",default="default")
    p.add_argument("--goal",default="")
    p.add_argument("--reference",default="")
    p.add_argument("--input",required=True)
    p.add_argument("--noop-tools",action="store_true")
    args=p.parse_args()
    state=load_state(args.session)
    if args.goal: state.goal=args.goal
    if args.reference: state.reference=args.reference
    loop=CompositeLoop(JsonLineAgent(),JsonLineAgent(),NoopTools())
    loop.cycle_once(state,args.input)
    print(json.dumps({"type":"composite_output","state":asdict(state)},indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
