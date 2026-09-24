#!/usr/bin/env python3
"""Hysteretic route selector for authorized One-Wave bridge routes."""
from __future__ import annotations
import json, os, time
from dataclasses import dataclass, asdict
from pathlib import Path
STATE = Path(os.environ.get("ONE_WAVE_ROUTE_STATE", str(Path.home()/".local/state/one-wave-bridge-mesh/routes.json"))).expanduser()
ENTER = float(os.environ.get("ONE_WAVE_ROUTE_ENTER", "0.70"))
LEAVE = float(os.environ.get("ONE_WAVE_ROUTE_LEAVE", "0.45"))
FAIL_PENALTY = float(os.environ.get("ONE_WAVE_ROUTE_FAIL_PENALTY", "0.18"))
PASS_GAIN = float(os.environ.get("ONE_WAVE_ROUTE_PASS_GAIN", "0.08"))
@dataclass
class RouteState:
    name: str
    family: str
    score: float = 0.5
    successes: int = 0
    failures: int = 0
    last_ok: float = 0.0
    last_fail: float = 0.0
def load():
    if not STATE.exists(): return {"active": None, "routes": {}}
    return json.loads(STATE.read_text(encoding="utf-8"))
def save(data):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp=STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    tmp.replace(STATE)
def update(name, family, ok):
    data=load(); routes=data.setdefault("routes",{})
    raw=routes.get(name, {"name":name,"family":family})
    rs=RouteState(**{**asdict(RouteState(name,family)), **raw})
    now=time.time()
    if ok:
        rs.successes += 1; rs.last_ok=now; rs.score=min(1.0, rs.score+PASS_GAIN)
    else:
        rs.failures += 1; rs.last_fail=now; rs.score=max(0.0, rs.score-FAIL_PENALTY)
    routes[name]=asdict(rs); save(data); return asdict(rs)
def choose(candidates):
    data=load(); routes=data.setdefault("routes",{}); active=data.get("active")
    if active and active in routes and routes[active].get("score",0) >= LEAVE: return active
    ranked=sorted(candidates, key=lambda n: routes.get(n,{}).get("score",0.5), reverse=True)
    selected=next((n for n in ranked if routes.get(n,{}).get("score",0.5) >= ENTER), ranked[0] if ranked else None)
    data["active"]=selected; save(data); return selected
def snapshot(): return load()
