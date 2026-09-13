#!/usr/bin/env python3
"""Deterministic sandbox lattice + synthetic internal body-state testbed.

This module is software-only. It models a fixed hex-lattice reference, a moving
active frame, scalar disturbances, virtual sensors, and bounded synthetic body
telemetry. It does NOT claim a physical lattice or subjective AI sensation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import copy
import hashlib
import math
import random
from typing import Iterable

HEX_DIRS = ((1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1))


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def hex_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    aq, ar = a
    bq, br = b
    ax, az = aq, ar
    ay = -ax - az
    bx, bz = bq, br
    by = -bx - bz
    return max(abs(ax - bx), abs(ay - by), abs(az - bz))


@dataclass(frozen=True)
class LatticeCell:
    q: int
    r: int
    rest_x: float
    rest_y: float

    @property
    def id(self) -> str:
        return f"H:{self.q}:{self.r}"


class HexLattice:
    """Fixed topology / rest geometry. Dynamic fields live separately."""

    def __init__(self, radius: int = 4) -> None:
        self.radius = radius
        self.cells: dict[tuple[int, int], LatticeCell] = {}
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                if max(abs(q), abs(r), abs(-q - r)) <= radius:
                    x = q + r / 2.0
                    y = r * math.sqrt(3.0) / 2.0
                    self.cells[(q, r)] = LatticeCell(q, r, x, y)
        self._neighbors = {
            pos: tuple((pos[0] + dq, pos[1] + dr) for dq, dr in HEX_DIRS if (pos[0] + dq, pos[1] + dr) in self.cells)
            for pos in self.cells
        }
        self._baseline = self.topology_digest()

    def neighbors(self, pos: tuple[int, int]) -> tuple[tuple[int, int], ...]:
        return self._neighbors[pos]

    def step(self, pos: tuple[int, int], direction: int) -> tuple[int, int] | None:
        dq, dr = HEX_DIRS[direction % 6]
        nxt = (pos[0] + dq, pos[1] + dr)
        return nxt if nxt in self.cells else None

    def topology_digest(self) -> str:
        payload: list[str] = []
        for pos in sorted(self.cells):
            c = self.cells[pos]
            payload.append(f"{c.id}:{c.rest_x:.12f}:{c.rest_y:.12f}")
            for nbr in sorted(self._neighbors[pos]):
                payload.append(f"{c.id}->{self.cells[nbr].id}")
        return hashlib.sha256("|".join(payload).encode()).hexdigest()

    def rest_unchanged(self) -> bool:
        return self.topology_digest() == self._baseline


@dataclass
class ActiveFrame:
    cell: tuple[int, int] = (0, 0)
    orientation: int = 0
    mirrored: bool = False
    scale: int = 1
    route: list[tuple[tuple[int, int], int, bool]] = field(default_factory=list)

    def local_to_world_dir(self, local_dir: int) -> int:
        local_dir %= 6
        if self.mirrored:
            local_dir = (-local_dir) % 6
        return (local_dir + self.orientation) % 6

    def rotate(self, steps: int) -> None:
        self.orientation = (self.orientation + steps) % 6

    def mirror(self) -> None:
        self.mirrored = not self.mirrored

    def move_local(self, lattice: HexLattice, local_dir: int) -> bool:
        old = (self.cell, self.orientation, self.mirrored)
        world_dir = self.local_to_world_dir(local_dir)
        nxt = lattice.step(self.cell, world_dir)
        if nxt is None:
            return False
        self.route.append(old)
        self.cell = nxt
        return True

    def undo(self) -> bool:
        if not self.route:
            return False
        self.cell, self.orientation, self.mirrored = self.route.pop()
        return True


@dataclass
class BodyTelemetry:
    """Synthetic control telemetry, not a claim of subjective sensation."""

    energy: float = 1.0
    thermal_load: float = 0.0
    actuator_strain: float = 0.0
    integrity: float = 1.0
    uncertainty: float = 0.0
    attention_budget: float = 1.0
    sensor_confidence: float = 1.0
    clock_drift: float = 0.0
    lifecycle: str = "Idle"
    generation: int = 0

    def snapshot(self) -> dict:
        return asdict(self)

    def update_from_action(self, effort: float, moved: bool) -> None:
        self.lifecycle = "Executing"
        self.energy = _clamp(self.energy - 0.015 * effort)
        self.thermal_load = _clamp(self.thermal_load + 0.02 * effort)
        self.actuator_strain = _clamp(0.8 * self.actuator_strain + (0.10 if moved else 0.18) * effort)
        self.attention_budget = _clamp(self.attention_budget - 0.008 * effort)
        self.lifecycle = "Resolving"

    def recover(self, amount: float = 0.05) -> None:
        self.energy = _clamp(self.energy + amount)
        self.thermal_load = _clamp(self.thermal_load - amount * 0.8)
        self.actuator_strain = _clamp(self.actuator_strain - amount)
        self.attention_budget = _clamp(self.attention_budget + amount)
        self.uncertainty = _clamp(self.uncertainty - amount * 0.5)


@dataclass
class SensorReading:
    value: float
    confidence: float
    source: str
    sample_index: int


class LatticeWorld:
    """Scalar disturbance simulator over a fixed hex graph."""

    def __init__(self, radius: int = 4, wave_gain: float = 0.11, damping: float = 0.035, seed: int = 0) -> None:
        self.lattice = HexLattice(radius)
        self.wave_gain = wave_gain
        self.damping = damping
        self.rng = random.Random(seed)
        self.value = {pos: 0.0 for pos in self.lattice.cells}
        self.prev = dict(self.value)
        self.velocity = dict(self.value)
        self.sources: dict[tuple[int, int], str] = {}
        self.tick_index = 0
        self.generation = 0
        self.checkpoints: dict[int, dict] = {}

    def clone(self) -> "LatticeWorld":
        return copy.deepcopy(self)

    def inject(self, pos: tuple[int, int], amplitude: float, source: str = "external") -> None:
        if pos not in self.value:
            raise KeyError(pos)
        self.value[pos] += amplitude
        self.sources[pos] = source

    def step(self, forcing: dict[tuple[int, int], float] | None = None) -> None:
        forcing = forcing or {}
        new: dict[tuple[int, int], float] = {}
        for pos, u in self.value.items():
            nbrs = self.lattice.neighbors(pos)
            avg = sum(self.value[n] for n in nbrs) / len(nbrs) if nbrs else u
            lap = avg - u
            vel = u - self.prev[pos]
            nxt = u + (1.0 - self.damping) * vel + self.wave_gain * lap + forcing.get(pos, 0.0)
            new[pos] = nxt
        self.prev = self.value
        self.value = new
        self.velocity = {p: self.value[p] - self.prev[p] for p in self.value}
        self.tick_index += 1

    def run(self, steps: int, forcing_fn=None) -> None:
        for i in range(steps):
            forcing = forcing_fn(i, self) if forcing_fn else None
            self.step(forcing)

    def energy(self) -> float:
        return sum(v * v + 0.5 * self.velocity[p] * self.velocity[p] for p, v in self.value.items())

    def max_abs(self) -> float:
        return max(abs(v) for v in self.value.values())

    def sensor(self, pos: tuple[int, int], *, noise: float = 0.0, quant: float | None = None,
               dropout: bool = False, saturation: float | None = None, source: str = "field") -> SensorReading:
        if dropout:
            return SensorReading(0.0, 0.0, source, self.tick_index)
        v = self.value[pos]
        if noise:
            v += self.rng.gauss(0.0, noise)
        if saturation is not None:
            v = max(-saturation, min(saturation, v))
        if quant:
            v = round(v / quant) * quant
        confidence = _clamp(1.0 - noise * 4.0)
        return SensorReading(v, confidence, source, self.tick_index)

    def local_gradient(self, pos: tuple[int, int]) -> tuple[int, float]:
        best_dir, best_delta = 0, 0.0
        base = self.value[pos]
        for d in range(6):
            nbr = self.lattice.step(pos, d)
            if nbr is None:
                continue
            delta = self.value[nbr] - base
            if abs(delta) > abs(best_delta):
                best_dir, best_delta = d, delta
        return best_dir, best_delta

    def checkpoint(self) -> int:
        self.generation += 1
        self.checkpoints[self.generation] = {
            "value": dict(self.value),
            "prev": dict(self.prev),
            "velocity": dict(self.velocity),
            "tick": self.tick_index,
            "topology": self.lattice.topology_digest(),
        }
        return self.generation

    def recall(self, generation: int) -> None:
        cp = self.checkpoints[generation]
        if cp["topology"] != self.lattice.topology_digest():
            raise RuntimeError("topology mismatch")
        self.value = dict(cp["value"])
        self.prev = dict(cp["prev"])
        self.velocity = dict(cp["velocity"])
        self.tick_index = cp["tick"]


@dataclass
class SandboxAgent:
    world: LatticeWorld
    frame: ActiveFrame = field(default_factory=ActiveFrame)
    body: BodyTelemetry = field(default_factory=BodyTelemetry)
    baseline: dict = field(default_factory=dict)
    receipts: list[dict] = field(default_factory=list)
    escalations: list[dict] = field(default_factory=list)
    self_source_history: set[tuple[int, tuple[int, int]]] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.baseline:
            self.baseline = self.body.snapshot()

    def act_move(self, local_dir: int, effort: float = 1.0, self_wave: float = 0.25) -> bool:
        old = self.frame.cell
        moved = self.frame.move_local(self.world.lattice, local_dir)
        self.body.update_from_action(effort, moved)
        if moved:
            self.world.inject(self.frame.cell, self_wave, source="self")
            self.self_source_history.add((self.world.tick_index, self.frame.cell))
        self.receipts.append({"kind": "action", "from": old, "to": self.frame.cell, "moved": moved, "tick": self.world.tick_index})
        return moved

    def sense_touch(self, **kwargs) -> SensorReading:
        reading = self.world.sensor(self.frame.cell, source="touch", **kwargs)
        self.body.sensor_confidence = reading.confidence
        return reading

    def fuse(self, readings: Iterable[SensorReading]) -> SensorReading:
        readings = list(readings)
        total = sum(r.confidence for r in readings)
        if total <= 1e-12:
            self.body.uncertainty = 1.0
            return SensorReading(0.0, 0.0, "fusion", self.world.tick_index)
        value = sum(r.value * r.confidence for r in readings) / total
        spread = max((abs(r.value - value) for r in readings), default=0.0)
        conf = _clamp((total / len(readings)) * (1.0 / (1.0 + 4.0 * spread)))
        self.body.uncertainty = _clamp(spread * 2.0)
        self.body.sensor_confidence = conf
        return SensorReading(value, conf, "fusion", self.world.tick_index)

    def why_forward(self, reason: str, urgency: float, evidence: dict) -> dict:
        packet = {
            "source": "sandbox.internal_world",
            "local_timestamp": self.world.tick_index,
            "change": evidence.get("change", 0.0),
            "confidence": evidence.get("confidence", self.body.sensor_confidence),
            "why_forward": reason,
            "urgency": urgency,
            "current_body_state_refs": self.body.snapshot(),
            "evidence_refs": evidence,
        }
        self.escalations.append(packet)
        return packet

    def baseline_delta(self) -> dict[str, float]:
        now = self.body.snapshot()
        out: dict[str, float] = {}
        for key, base in self.baseline.items():
            if isinstance(base, (int, float)) and isinstance(now[key], (int, float)):
                out[key] = float(now[key]) - float(base)
        return out

    def reset_body_to_baseline(self) -> None:
        keep_generation = self.body.generation
        for k, v in self.baseline.items():
            if hasattr(self.body, k):
                setattr(self.body, k, copy.deepcopy(v))
        self.body.generation = keep_generation
