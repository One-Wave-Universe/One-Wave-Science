#!/usr/bin/env python3
"""Reduced lattice-body sandbox for Miniverse room.

Software coordination model only. Bodies apply load to occupied lattice sites;
the stationary triangular lattice stores scalar displacement/compression and
relaxes through neighbor coupling. Derived pressure/strain are fed back to bodies.
This follows D-412 simulation-governance requirements but does not claim physical
validation of One-Wave gravity or CELL_V1.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any
import math

@dataclass
class CellState:
    u: float = 0.0
    v: float = 0.0
    chi: float = 0.0
    pressure: float = 0.0
    strain: float = 0.0
    load: float = 0.0

@dataclass
class BodySense:
    agent_id: str
    cell: str
    mass: float
    displacement: float
    pressure: float
    strain: float
    support: float
    weight_signal: float

class LatticeBodySandbox:
    def __init__(self, manifest: dict[str,Any], *, stiffness: float=0.34, damping: float=0.18, retention: float=0.92, dt: float=0.2):
        self.cells={c["id"]:c for c in manifest["cells"]}
        self.state={cid:CellState() for cid in self.cells}
        self.stiffness=stiffness; self.damping=damping; self.retention=retention; self.dt=dt

    def body_mass(self, agent: dict[str,Any]) -> float:
        body=agent.get("body") or {}
        scale=float(body.get("scale",agent.get("scale",1.0) or 1.0))
        parts=body.get("parts") or []
        volume=0.0
        for p in parts:
            size=p.get("size",[0.5,0.5,0.5])
            try: volume += max(0.001,float(size[0])*float(size[1])*float(size[2]))
            except Exception: volume += 0.125
        if not parts: volume=1.0
        return max(0.1,min(20.0,volume*(scale**3)))

    def apply_bodies(self, agents: dict[str,dict[str,Any]]) -> None:
        for s in self.state.values(): s.load=0.0
        for agent in agents.values():
            cell=agent.get("cell")
            if cell in self.state and agent.get("connected",True):
                self.state[cell].load += self.body_mass(agent)

    def step(self, agents: dict[str,dict[str,Any]], steps: int=1) -> None:
        for _ in range(max(1,steps)):
            self.apply_bodies(agents)
            nxt={}
            for cid,cell in self.cells.items():
                s=self.state[cid]
                nbr_ids=list(cell.get("neighbors",{}).values())
                nbr_u=sum(self.state[n].u for n in nbr_ids)/len(nbr_ids) if nbr_ids else s.u
                restoring=self.stiffness*(nbr_u-s.u)
                load_force=-s.load
                accel=load_force+restoring-self.damping*s.v
                v=(s.v+accel*self.dt)*self.retention
                u=s.u+v*self.dt
                chi=max(0.0,-u)
                edge_diffs=[abs(u-self.state[n].u) for n in nbr_ids]
                strain=sum(edge_diffs)/len(edge_diffs) if edge_diffs else 0.0
                pressure=s.load+chi+self.stiffness*strain
                nxt[cid]=CellState(u=u,v=v,chi=chi,pressure=pressure,strain=strain,load=s.load)
            self.state=nxt

    def senses(self, agents: dict[str,dict[str,Any]]) -> dict[str,dict[str,Any]]:
        out={}
        for aid,agent in agents.items():
            cid=agent.get("cell")
            if cid not in self.state: continue
            s=self.state[cid]; mass=self.body_mass(agent)
            support=max(0.0,min(1.0,1.0/(1.0+abs(s.u)+s.strain)))
            sense=BodySense(
              agent_id=aid,cell=cid,mass=mass,displacement=s.u,pressure=s.pressure,
              strain=s.strain,support=support,weight_signal=mass*(1.0+s.pressure)
            )
            out[aid]=asdict(sense)
        return out

    def snapshot(self) -> dict[str,Any]:
        return {cid:asdict(s) for cid,s in self.state.items()}
