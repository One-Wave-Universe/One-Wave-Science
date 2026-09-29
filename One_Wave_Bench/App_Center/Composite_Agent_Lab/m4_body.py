#!/usr/bin/env python3
"""M4 software-body state for Composite Agent Lab.

This is a software simulation of the project architecture, not a claim about
physical CELL_V1 behavior. M4 owns the persistent body/process state. Field and
Void read from it and propose updates; only M4 commits thresholded transitions.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
import json, math, os
from pathlib import Path
from typing import Any

STATE_PATH=Path(os.environ.get("ONE_WAVE_M4_STATE", str(Path.home()/".local/state/one-wave-composite/m4_body.json"))).expanduser()

@dataclass
class HysteresisBand:
    enter: float
    leave: float
    active: bool=False
    def update(self, value: float) -> bool:
        if self.active:
            if value <= self.leave: self.active=False
        elif value >= self.enter:
            self.active=True
        return self.active

@dataclass
class M4Memory:
    retained_reference: dict[str,Any]=field(default_factory=dict)
    working: dict[str,Any]=field(default_factory=dict)
    last_result: dict[str,Any]=field(default_factory=dict)
    successful_patterns: list[dict[str,Any]]=field(default_factory=list)
    failed_patterns: list[dict[str,Any]]=field(default_factory=list)

@dataclass
class M4Body:
    cycle: int=0
    polarity: float=0.0
    lean: float=0.0
    pressure: float=0.0
    resistance: float=0.0
    confidence: float=0.5
    arousal: float=0.0
    field_drive: float=0.0
    void_brake: float=0.0
    action_gate: HysteresisBand=field(default_factory=lambda:HysteresisBand(0.65,0.40))
    commit_gate: HysteresisBand=field(default_factory=lambda:HysteresisBand(0.72,0.46))
    novelty_gate: HysteresisBand=field(default_factory=lambda:HysteresisBand(0.70,0.35))
    memory: M4Memory=field(default_factory=M4Memory)
    mode: str="HOLD"

    def snapshot(self) -> dict[str,Any]: return asdict(self)

    def ingest(self, stimulus: dict[str,Any]) -> None:
        self.cycle += 1
        magnitude=float(stimulus.get("magnitude",0.5))
        novelty=float(stimulus.get("novelty",0.0))
        conflict=float(stimulus.get("conflict",0.0))
        self.pressure=max(0.0,min(1.0,0.70*self.pressure+0.30*magnitude))
        self.arousal=max(0.0,min(1.0,0.75*self.arousal+0.25*(magnitude+conflict)/2))
        self.novelty_gate.update(novelty)

    def integrate(self, field_signal: dict[str,Any], void_signal: dict[str,Any]) -> dict[str,Any]:
        self.field_drive=max(0.0,min(1.0,float(field_signal.get("drive",0.0))))
        self.void_brake=max(0.0,min(1.0,float(void_signal.get("brake",0.0))))
        support=float(void_signal.get("support",0.0))
        contradiction=float(void_signal.get("contradiction",0.0))
        friction=float(field_signal.get("friction",0.0))
        self.resistance=max(0.0,min(1.0,0.65*self.resistance+0.35*(friction+contradiction)/2))
        raw=(self.field_drive+support)-(self.void_brake+self.resistance)
        self.lean=max(-1.0,min(1.0,0.60*self.lean+0.40*raw))
        self.polarity=1.0 if self.lean>0.12 else -1.0 if self.lean<-0.12 else 0.0
        action_strength=max(0.0,self.lean)*(1.0-self.void_brake)
        action_open=self.action_gate.update(action_strength)
        self.mode="ACT" if action_open else "HOLD"
        return {"action_open":action_open,"action_strength":action_strength,"lean":self.lean,"mode":self.mode}

    def reinject(self, result: dict[str,Any]) -> dict[str,Any]:
        ok=bool(result.get("ok",False))
        evidence=float(result.get("evidence_strength",1.0 if ok else 0.0))
        expected=float(result.get("expected_match",1.0 if ok else 0.0))
        commit_strength=max(0.0,min(1.0,(evidence+expected)/2))
        committed=self.commit_gate.update(commit_strength)
        self.memory.last_result=result
        if committed and ok:
            self.confidence=min(1.0,0.80*self.confidence+0.20*commit_strength)
            self.memory.successful_patterns=(self.memory.successful_patterns+[{"cycle":self.cycle,"result":result}])[-12:]
            self.memory.retained_reference={"cycle":self.cycle,"result":result}
        else:
            self.confidence=max(0.0,0.85*self.confidence-0.15*(1.0-commit_strength))
            self.memory.failed_patterns=(self.memory.failed_patterns+[{"cycle":self.cycle,"result":result}])[-12:]
        self.field_drive*=0.5
        self.void_brake*=0.5
        self.pressure*=0.85
        return {"committed":committed,"commit_strength":commit_strength,"confidence":self.confidence}

def load_body() -> M4Body:
    if not STATE_PATH.exists(): return M4Body()
    raw=json.loads(STATE_PATH.read_text(encoding="utf-8"))
    raw["action_gate"]=HysteresisBand(**raw.get("action_gate",{"enter":0.65,"leave":0.40}))
    raw["commit_gate"]=HysteresisBand(**raw.get("commit_gate",{"enter":0.72,"leave":0.46}))
    raw["novelty_gate"]=HysteresisBand(**raw.get("novelty_gate",{"enter":0.70,"leave":0.35}))
    raw["memory"]=M4Memory(**raw.get("memory",{}))
    return M4Body(**raw)

def save_body(body: M4Body) -> None:
    STATE_PATH.parent.mkdir(parents=True,exist_ok=True)
    tmp=STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(body.snapshot(),indent=2,sort_keys=True)+"\n",encoding="utf-8")
    tmp.replace(STATE_PATH)
