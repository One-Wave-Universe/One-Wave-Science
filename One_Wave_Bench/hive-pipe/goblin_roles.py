#!/usr/bin/env python3
"""Goblin role layer for the One-Wave bridge mesh.

These roles do not bypass authentication or safety gates. They coordinate
reference, diagnosis, parsing, execution, message carrying, and alternate-route
discovery around the existing bridge modules.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from typing import Any

@dataclass
class GoblinEvent:
    goblin: str
    state: str
    detail: str
    next_action: str = ""
    timestamp: str = ""
    def to_dict(self):
        data=asdict(self)
        if not data["timestamp"]: data["timestamp"]=datetime.now(timezone.utc).isoformat()
        return data

class ReferenceGoblin:
    name="reference-goblin"
    required=("source","target","direction","reference","intention","consequence")
    def inspect(self, card: dict[str,Any]) -> GoblinEvent:
        missing=[k for k in self.required if not isinstance(card.get(k),str) or not card[k].strip()]
        if missing:
            return GoblinEvent(self.name,"HOLD","missing reference fields: "+", ".join(missing),"complete reference card")
        return GoblinEvent(self.name,"READY","reference card complete","hand to parser goblin")

class ParserGoblin:
    name="parser-goblin"
    def inspect(self, request: dict[str,Any]) -> GoblinEvent:
        argv=request.get("argv")
        if not isinstance(argv,list) or not argv or not all(isinstance(x,str) and x for x in argv):
            return GoblinEvent(self.name,"HOLD","argv must be a non-empty list of strings","repair request shape")
        return GoblinEvent(self.name,"READY",f"parsed {len(argv)} argv tokens","hand to reference state")

class DoctorGoblin:
    name="doctor-goblin"
    def diagnose(self, evidence: dict[str,Any]) -> GoblinEvent:
        if evidence.get("receipt_ok"):
            return GoblinEvent(self.name,"PASS","matching receipt observed","update route memory")
        if evidence.get("service_state") not in (None,"active"):
            return GoblinEvent(self.name,"REPAIR","known user service inactive","restart known service, then reprobe")
        return GoblinEvent(self.name,"DEGRADE","route lacks a matching receipt","decrease route weight and choose alternate family")

class ReferenceWorkerMachine:
    """Two-state bridge machine: REFERENCE -> WORKER -> REFERENCE."""
    def __init__(self): self.state="REFERENCE"
    def advance(self, reference_ready: bool=False, worker_receipt: bool=False) -> GoblinEvent:
        if self.state=="REFERENCE":
            if not reference_ready:
                return GoblinEvent("reference-worker","REFERENCE_HOLD","reference not yet complete","stay in REFERENCE")
            self.state="WORKER"
            return GoblinEvent("reference-worker","WORKER","reference approved","execute exactly one bounded action")
        if not worker_receipt:
            return GoblinEvent("reference-worker","WORKER_HOLD","worker has no matching receipt","do not commit; diagnose route")
        self.state="REFERENCE"
        return GoblinEvent("reference-worker","REFERENCE","worker receipt returned","compare consequence, update memory, choose next action")

class CarrierPigeonGoblin:
    name="carrier-pigeon-goblin"
    def carry(self, message_id: str, source: str, target: str, route: str) -> GoblinEvent:
        if not all(isinstance(v,str) and v.strip() for v in (message_id,source,target,route)):
            return GoblinEvent(self.name,"HOLD","message envelope incomplete","supply id/source/target/route")
        return GoblinEvent(self.name,"IN_FLIGHT",f"{message_id}: {source} -> {target} via {route}","wait for matching return receipt")

class GoblinRaccoon:
    name="goblin-raccoon"
    def scout(self, failures: list[dict[str,Any]], candidates: list[dict[str,Any]]) -> GoblinEvent:
        failed_families={str(f.get("family","")) for f in failures if f.get("family")}
        alternatives=[c for c in candidates if c.get("family") not in failed_families and c.get("configured")]
        if alternatives:
            pick=sorted(alternatives,key=lambda c: float(c.get("score",0.5)),reverse=True)[0]
            return GoblinEvent(self.name,"FOUND",f"alternate family {pick.get('family')} route {pick.get('name')}","probe alternate before execution")
        return GoblinEvent(self.name,"BUILD","no independent configured route remains","create a bounded adapter/setup task; do not invent connectivity")

def event_json(event: GoblinEvent) -> str:
    return json.dumps(event.to_dict(), sort_keys=True)
