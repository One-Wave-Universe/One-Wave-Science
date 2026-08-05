#!/usr/bin/env python3
"""
ONE-WAVE VIRTUAL LENS v1.0
==========================

A synthetic event-vision brain with its own continuous local loop and local
Hopfield-style associative memory. It does not use a physical camera and it
does not modify the finished One-Wave Hopfield Brain.

Core loop:
    synthetic world
      -> limited 64x64 virtual lens
      -> local brightness-change events
      -> persistent 256x256 internal visual field
      -> confidence / age / motion prediction
      -> compact visual pattern
      -> local Hopfield reconstruction
      -> repeat

The local visual brain exports a compact state packet for later M4 routing.
It does not claim its five visual metrics are the five canonical M4 pathways.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np


WORLD_SHAPE = (256, 256)
LENS_SHAPE = (64, 64)
DEFAULT_SEED = 2026


def stable_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "little")


@dataclass(frozen=True)
class VisualEvent:
    local_x: int
    local_y: int
    world_x: int
    world_y: int
    time: int
    polarity: int
    magnitude: float


@dataclass
class VisualStatePacket:
    tick: int
    loop_exists: bool
    reference_phase: int
    gaze_x: int
    gaze_y: int
    event_count: int
    positive_events: int
    negative_events: int
    observed_x: Optional[float]
    observed_y: Optional[float]
    predicted_x: Optional[float]
    predicted_y: Optional[float]
    velocity_x: float
    velocity_y: float
    mean_confidence: float
    active_confidence: float
    prediction_confidence: float
    local_change_pressure: float
    occluded: bool
    memory_attractor: Optional[str]
    memory_overlap: Optional[float]


class SyntheticVisualWorld:
    """A deterministic black world with one moving white dot and a fixed wall."""

    def __init__(self, shape: Tuple[int, int] = WORLD_SHAPE):
        self.height, self.width = shape
        self.dot_y = 128
        self.wall = (126, 112, 138, 144)  # x0, y0, x1, y1

    def dot_position(self, tick: int) -> Tuple[int, int]:
        # Triangle wave from x=100 to x=156 and back. The fixed 64x64 lens
        # centered at 128 sees the full route.
        period = 112
        phase = tick % period
        x = 100 + phase if phase <= 56 else 156 - (phase - 56)
        return int(x), self.dot_y

    def is_occluded(self, tick: int) -> bool:
        x, y = self.dot_position(tick)
        x0, y0, x1, y1 = self.wall
        return x0 <= x <= x1 and y0 <= y <= y1

    @staticmethod
    def _draw_disk(frame: np.ndarray, x: int, y: int, radius: int, value: float) -> None:
        yy, xx = np.ogrid[: frame.shape[0], : frame.shape[1]]
        mask = (xx - x) ** 2 + (yy - y) ** 2 <= radius ** 2
        frame[mask] = value

    def render(self, tick: int, with_wall: bool = True) -> np.ndarray:
        frame = np.zeros((self.height, self.width), dtype=np.float32)
        x, y = self.dot_position(tick)
        self._draw_disk(frame, x, y, radius=3, value=1.0)
        if with_wall:
            x0, y0, x1, y1 = self.wall
            # Draw after the dot so the wall genuinely occludes it.
            frame[y0:y1, x0:x1] = 0.22
        return frame


class VirtualLens:
    """A bounded gaze window. It never exposes the entire synthetic world."""

    def __init__(
        self,
        world_shape: Tuple[int, int] = WORLD_SHAPE,
        lens_shape: Tuple[int, int] = LENS_SHAPE,
        gaze: Tuple[int, int] = (128, 128),
    ):
        self.world_h, self.world_w = world_shape
        self.lens_h, self.lens_w = lens_shape
        self.gaze_x, self.gaze_y = gaze

    def move_gaze(self, dx: int, dy: int) -> None:
        half_w = self.lens_w // 2
        half_h = self.lens_h // 2
        self.gaze_x = int(np.clip(self.gaze_x + dx, half_w, self.world_w - half_w))
        self.gaze_y = int(np.clip(self.gaze_y + dy, half_h, self.world_h - half_h))

    def bounds(self) -> Tuple[int, int, int, int]:
        x0 = self.gaze_x - self.lens_w // 2
        y0 = self.gaze_y - self.lens_h // 2
        return x0, y0, x0 + self.lens_w, y0 + self.lens_h

    def capture(self, world: np.ndarray) -> np.ndarray:
        x0, y0, x1, y1 = self.bounds()
        return world[y0:y1, x0:x1].copy()

    def local_to_world(self, x: int, y: int) -> Tuple[int, int]:
        x0, y0, _, _ = self.bounds()
        return x0 + x, y0 + y


class EventEncoder:
    """Brightness-change sensor with ON/OFF polarity events."""

    def __init__(self, threshold: float = 0.15):
        if threshold <= 0:
            raise ValueError("threshold must be positive")
        self.threshold = float(threshold)
        self.previous: Optional[np.ndarray] = None

    def initialize(self, view: np.ndarray) -> None:
        self.previous = view.astype(np.float32, copy=True)

    def encode(self, view: np.ndarray, lens: VirtualLens, tick: int) -> List[VisualEvent]:
        if self.previous is None:
            self.initialize(view)
            return []
        diff = view.astype(np.float32) - self.previous
        ys, xs = np.nonzero(np.abs(diff) > self.threshold)
        events: List[VisualEvent] = []
        for y, x in zip(ys.tolist(), xs.tolist()):
            wx, wy = lens.local_to_world(x, y)
            delta = float(diff[y, x])
            events.append(
                VisualEvent(
                    local_x=x,
                    local_y=y,
                    world_x=wx,
                    world_y=wy,
                    time=tick,
                    polarity=1 if delta > 0 else -1,
                    magnitude=abs(delta),
                )
            )
        self.previous = view.astype(np.float32, copy=True)
        return events


class PersistentVisualField:
    """
    One persistent internal visual world with confidence, age, and prediction.

    The initial lens view establishes the first local reference. Later updates
    are event-driven. No full external frame is copied after initialization.
    """

    def __init__(self, shape: Tuple[int, int] = WORLD_SHAPE):
        self.height, self.width = shape
        self.field = np.zeros(shape, dtype=np.float32)
        self.confidence = np.zeros(shape, dtype=np.float32)
        self.age = np.full(shape, 65535, dtype=np.uint16)
        self.prediction = np.zeros(shape, dtype=np.float32)
        self.initialized = False

        self.last_observed: Optional[np.ndarray] = None
        self.previous_observed: Optional[np.ndarray] = None
        self.velocity = np.zeros(2, dtype=np.float32)
        self.predicted_position: Optional[np.ndarray] = None
        self.ticks_since_observation = 0
        self.prediction_confidence = 0.0

    def initialize_from_view(self, view: np.ndarray, lens: VirtualLens) -> None:
        x0, y0, x1, y1 = lens.bounds()
        self.field[y0:y1, x0:x1] = view
        self.confidence[y0:y1, x0:x1] = 0.85
        self.age[y0:y1, x0:x1] = 0
        self.initialized = True

    @staticmethod
    def _event_centroid(events: Sequence[VisualEvent]) -> Optional[np.ndarray]:
        positive = [e for e in events if e.polarity > 0 and e.magnitude >= 0.5]
        if not positive:
            return None
        weights = np.array([e.magnitude for e in positive], dtype=np.float32)
        xs = np.array([e.world_x for e in positive], dtype=np.float32)
        ys = np.array([e.world_y for e in positive], dtype=np.float32)
        total = float(weights.sum())
        if total <= 0:
            return None
        return np.array([(xs * weights).sum() / total, (ys * weights).sum() / total], dtype=np.float32)

    def _draw_prediction(self, x: float, y: float, confidence: float) -> None:
        self.prediction.fill(0.0)
        radius = 4
        xi, yi = int(round(x)), int(round(y))
        x0, x1 = max(0, xi - radius), min(self.width, xi + radius + 1)
        y0, y1 = max(0, yi - radius), min(self.height, yi + radius + 1)
        if x0 >= x1 or y0 >= y1:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1]
        sigma = 2.0
        gaussian = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma * sigma))
        self.prediction[y0:y1, x0:x1] = (gaussian * confidence).astype(np.float32)

    def update(self, events: Sequence[VisualEvent]) -> None:
        if not self.initialized:
            raise RuntimeError("visual field must be initialized first")

        # Confidence ages globally but slowly. Brightness is persistent and only
        # changes where events report a local difference.
        self.confidence *= 0.998
        active_age = self.age < np.iinfo(np.uint16).max
        self.age[active_age] += 1

        for event in events:
            y, x = event.world_y, event.world_x
            signed_delta = event.polarity * event.magnitude
            self.field[y, x] = float(np.clip(self.field[y, x] + signed_delta, 0.0, 1.0))
            self.confidence[y, x] = float(np.clip(self.confidence[y, x] + 0.18, 0.0, 1.0))
            self.age[y, x] = 0

        observed = self._event_centroid(events)
        if observed is not None:
            self.previous_observed = None if self.last_observed is None else self.last_observed.copy()
            self.last_observed = observed
            if self.previous_observed is not None:
                measured = self.last_observed - self.previous_observed
                # Smooth enough to avoid one event burst steering the whole world.
                self.velocity = 0.65 * self.velocity + 0.35 * measured
            self.ticks_since_observation = 0
            self.predicted_position = self.last_observed.copy()
            self.prediction_confidence = min(1.0, self.prediction_confidence + 0.22)
        else:
            self.ticks_since_observation += 1
            if self.predicted_position is not None:
                self.predicted_position = self.predicted_position + self.velocity
            self.prediction_confidence *= 0.94

        if self.predicted_position is not None:
            self.predicted_position[0] = np.clip(self.predicted_position[0], 0, self.width - 1)
            self.predicted_position[1] = np.clip(self.predicted_position[1], 0, self.height - 1)
            self._draw_prediction(
                float(self.predicted_position[0]),
                float(self.predicted_position[1]),
                self.prediction_confidence,
            )
        else:
            self.prediction.fill(0.0)

    def local_maps(self, lens: VirtualLens) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        x0, y0, x1, y1 = lens.bounds()
        return (
            self.field[y0:y1, x0:x1].copy(),
            self.confidence[y0:y1, x0:x1].copy(),
            self.prediction[y0:y1, x0:x1].copy(),
        )

    def ram_bytes(self) -> Dict[str, int]:
        return {
            "persistent_field": int(self.field.nbytes),
            "confidence_map": int(self.confidence.nbytes),
            "age_map": int(self.age.nbytes),
            "prediction_map": int(self.prediction.nbytes),
        }


class VisualPatternCodec:
    """
    Compresses one local visual state into a 512-unit bipolar pattern.

    Four equal 128-unit blocks:
      1. persistent occupancy
      2. current event polarity
      3. predicted position
      4. distributed motion/context state

    Each sensory block contains 64 coarse spatial bits plus 64 deterministic
    distributed bits derived from the actual pooled content. The distributed
    half removes the huge shared "mostly empty" bias that otherwise makes
    sparse visual snapshots collapse into one Hopfield attractor. It is content
    encoding, not random uncertainty fill.

    This is local visual memory only. It does not overwrite the five equal
    multimodal memory banks used by the higher Dream Engine.
    """

    GRID = 8
    COARSE = GRID * GRID
    BLOCK = COARSE * 2
    VECTOR_SIZE = BLOCK * 4

    @staticmethod
    def _pool_mean(array: np.ndarray) -> np.ndarray:
        h, w = array.shape
        if h % VisualPatternCodec.GRID or w % VisualPatternCodec.GRID:
            raise ValueError("local map must divide evenly into 8x8 blocks")
        bh, bw = h // VisualPatternCodec.GRID, w // VisualPatternCodec.GRID
        return array.reshape(VisualPatternCodec.GRID, bh, VisualPatternCodec.GRID, bw).mean(axis=(1, 3))

    @staticmethod
    def _balanced_code(label: str, size: int = COARSE) -> np.ndarray:
        """Deterministic exactly balanced bipolar distributed code."""
        rng = np.random.default_rng(stable_seed(label))
        code = np.array([1] * (size // 2) + [-1] * (size - size // 2), dtype=np.int8)
        rng.shuffle(code)
        return code

    @staticmethod
    def _content_fingerprint(prefix: str, pooled: np.ndarray) -> np.ndarray:
        # Quantize the actual local content, then map that content to a balanced
        # distributed code. Identical content yields identical bits.
        quantized = np.clip(np.round(pooled * 31.0), -31, 31).astype(np.int8)
        digest = hashlib.sha256(prefix.encode("utf-8") + quantized.tobytes()).hexdigest()
        return VisualPatternCodec._balanced_code(f"{prefix}:{digest}")

    @staticmethod
    def _coarse_bits(values: np.ndarray, threshold: float, signed: bool = False) -> np.ndarray:
        if signed:
            return np.where(values >= threshold, 1, -1).astype(np.int8).ravel()
        return np.where(values > threshold, 1, -1).astype(np.int8).ravel()

    def encode(
        self,
        local_field: np.ndarray,
        local_event_map: np.ndarray,
        local_prediction: np.ndarray,
        velocity: Sequence[float],
        predicted_position: Optional[Sequence[float]],
        lens: VirtualLens,
        occluded: bool = False,
    ) -> np.ndarray:
        occupancy = self._pool_mean(local_field)
        event = self._pool_mean(local_event_map)
        prediction = self._pool_mean(local_prediction)

        occupancy_block = np.concatenate([
            self._coarse_bits(occupancy, 0.04),
            self._content_fingerprint("occupancy", occupancy),
        ])
        event_block = np.concatenate([
            self._coarse_bits(event, 0.01, signed=True),
            self._content_fingerprint("event", event),
        ])
        prediction_block = np.concatenate([
            self._coarse_bits(prediction, 0.025),
            self._content_fingerprint("prediction", prediction),
        ])

        vx, vy = float(velocity[0]), float(velocity[1])
        if abs(vx) < 0.15 and abs(vy) < 0.15:
            direction = "STILL"
        elif abs(vx) >= abs(vy):
            direction = "RIGHT" if vx > 0 else "LEFT"
        else:
            direction = "DOWN" if vy > 0 else "UP"

        if predicted_position is None:
            zone = "UNKNOWN"
        else:
            x0, y0, _, _ = lens.bounds()
            lx = float(predicted_position[0]) - x0
            ly = float(predicted_position[1]) - y0
            zx = int(np.clip(lx // 8, 0, 7))
            zy = int(np.clip(ly // 8, 0, 7))
            zone = f"{zx}:{zy}"
        context_label = f"visual:{direction}:{zone}:occluded={int(occluded)}"
        context_block = np.concatenate([
            self._balanced_code(context_label + ":a"),
            self._balanced_code(context_label + ":b"),
        ])

        return np.concatenate(
            [occupancy_block, event_block, prediction_block, context_block]
        ).astype(np.int8)

    def damage(self, pattern: np.ndarray, fraction: float, label: str) -> np.ndarray:
        if not 0 <= fraction <= 1:
            raise ValueError("fraction must be 0..1")
        damaged = pattern.copy()
        rng = np.random.default_rng(stable_seed(label))
        count = int(round(len(pattern) * fraction))
        indices = rng.choice(len(pattern), size=count, replace=False)
        damaged[indices] = 0
        return damaged


class VisualHopfieldMemory:
    """Local visual attractor memory using the finished Hopfield core rules."""

    def __init__(self, vector_size: int = VisualPatternCodec.VECTOR_SIZE, seed: int = DEFAULT_SEED):
        self.vector_size = int(vector_size)
        self.seed = int(seed)
        self.patterns: Dict[str, np.ndarray] = {}
        self.weights = np.zeros((self.vector_size, self.vector_size), dtype=np.float32)

    def add(self, name: str, pattern: np.ndarray, retrain: bool = True) -> None:
        p = np.asarray(pattern, dtype=np.int8)
        if p.shape != (self.vector_size,):
            raise ValueError(f"pattern must have shape {(self.vector_size,)}")
        if not np.all(np.isin(p, [-1, 1])):
            raise ValueError("stored patterns must be bipolar")
        self.patterns[name] = p.copy()
        if retrain:
            self.retrain()

    def retrain(self) -> None:
        self.weights.fill(0.0)
        if not self.patterns:
            return
        scale = 1.0 / self.vector_size
        for pattern in self.patterns.values():
            self.weights += np.outer(pattern, pattern).astype(np.float32) * scale
        np.fill_diagonal(self.weights, 0.0)

    def energy(self, state: np.ndarray) -> float:
        s = np.asarray(state, dtype=np.float32)
        return float(-0.5 * s @ self.weights @ s)

    def settle(
        self,
        initial: np.ndarray,
        label: str,
        clamped: Optional[Set[int]] = None,
        max_sweeps: int = 60,
    ) -> Tuple[np.ndarray, List[float], int, bool]:
        state = np.asarray(initial, dtype=np.int8).copy()
        if state.shape != (self.vector_size,):
            raise ValueError("wrong initial shape")
        clamped = clamped or set()
        mutable = [i for i in range(self.vector_size) if i not in clamped]
        rng = random.Random(stable_seed(label) ^ self.seed)
        energies = [self.energy(state)]

        for sweep in range(1, max_sweeps + 1):
            rng.shuffle(mutable)
            changed = 0
            for i in mutable:
                h = float(self.weights[i] @ state)
                new = 1 if h >= 0 else -1
                if new != state[i]:
                    state[i] = new
                    changed += 1
            energies.append(self.energy(state))
            if changed == 0:
                return state, energies, sweep, True
        return state, energies, max_sweeps, False

    def closest(self, state: np.ndarray) -> Tuple[Optional[str], float]:
        if not self.patterns:
            return None, 0.0
        s = np.asarray(state, dtype=np.float32)
        denom_s = float(np.linalg.norm(s))
        best_name: Optional[str] = None
        best_overlap = -math.inf
        for name, pattern in self.patterns.items():
            denom = denom_s * float(np.linalg.norm(pattern))
            ov = float(s @ pattern / denom) if denom else 0.0
            if ov > best_overlap:
                best_name, best_overlap = name, ov
        return best_name, best_overlap

    def recall(self, cue: np.ndarray, label: str) -> Dict[str, object]:
        settled, energies, sweeps, converged = self.settle(cue, label)
        name, overlap = self.closest(settled)
        committed = None if name is None else self.patterns[name]
        return {
            "decoded": name,
            "overlap": overlap,
            "sweeps": sweeps,
            "converged": converged,
            "initial_energy": energies[0],
            "final_energy": energies[-1],
            "energy_nonincreasing": all(b <= a + 1e-6 for a, b in zip(energies, energies[1:])),
            "raw_exact": bool(committed is not None and np.array_equal(settled, committed)),
            "settled": settled,
        }

    def ram_bytes(self) -> Dict[str, int]:
        return {
            "visual_hopfield_weights": int(self.weights.nbytes),
            "visual_hopfield_patterns": int(sum(p.nbytes for p in self.patterns.values())),
        }


class VirtualLensBrain:
    """Runs the visual loop and exposes compact packets for future M4 routing."""

    def __init__(self, threshold: float = 0.15, seed: int = DEFAULT_SEED):
        self.world = SyntheticVisualWorld()
        self.lens = VirtualLens()
        self.events = EventEncoder(threshold=threshold)
        self.internal = PersistentVisualField()
        self.codec = VisualPatternCodec()
        self.memory = VisualHopfieldMemory(seed=seed)
        self.reference_phase = -1
        self.last_packet: Optional[VisualStatePacket] = None
        self.last_pattern: Optional[np.ndarray] = None
        self.last_view: Optional[np.ndarray] = None
        self.last_world: Optional[np.ndarray] = None
        self.last_event_map = np.zeros(LENS_SHAPE, dtype=np.float32)

    def _event_map(self, events: Sequence[VisualEvent]) -> np.ndarray:
        event_map = np.zeros(LENS_SHAPE, dtype=np.float32)
        for event in events:
            event_map[event.local_y, event.local_x] += event.polarity * event.magnitude
        return np.clip(event_map, -1.0, 1.0)

    def step(self, tick: int) -> VisualStatePacket:
        world = self.world.render(tick)
        view = self.lens.capture(world)
        if not self.internal.initialized:
            self.internal.initialize_from_view(view, self.lens)
            self.events.initialize(view)
            events: List[VisualEvent] = []
        else:
            events = self.events.encode(view, self.lens, tick)
            self.internal.update(events)

        event_map = self._event_map(events)
        local_field, local_conf, local_prediction = self.internal.local_maps(self.lens)
        pattern = self.codec.encode(
            local_field,
            event_map,
            local_prediction,
            self.internal.velocity,
            self.internal.predicted_position,
            self.lens,
            occluded=self.world.is_occluded(tick),
        )

        memory_name: Optional[str] = None
        memory_overlap: Optional[float] = None
        if self.memory.patterns:
            memory_name, memory_overlap = self.memory.closest(pattern)

        self.reference_phase *= -1
        observed = self.internal.last_observed
        predicted = self.internal.predicted_position
        active = local_conf[local_conf > 0.05]
        packet = VisualStatePacket(
            tick=tick,
            loop_exists=True,
            reference_phase=self.reference_phase,
            gaze_x=self.lens.gaze_x,
            gaze_y=self.lens.gaze_y,
            event_count=len(events),
            positive_events=sum(e.polarity > 0 for e in events),
            negative_events=sum(e.polarity < 0 for e in events),
            observed_x=None if observed is None else float(observed[0]),
            observed_y=None if observed is None else float(observed[1]),
            predicted_x=None if predicted is None else float(predicted[0]),
            predicted_y=None if predicted is None else float(predicted[1]),
            velocity_x=float(self.internal.velocity[0]),
            velocity_y=float(self.internal.velocity[1]),
            mean_confidence=float(local_conf.mean()),
            active_confidence=float(active.mean()) if active.size else 0.0,
            prediction_confidence=float(self.internal.prediction_confidence),
            local_change_pressure=float(np.mean(np.abs(event_map))),
            occluded=self.world.is_occluded(tick),
            memory_attractor=memory_name,
            memory_overlap=memory_overlap,
        )
        self.last_packet = packet
        self.last_pattern = pattern
        self.last_view = view
        self.last_world = world
        self.last_event_map = event_map
        return packet

    def store_current(self, name: str) -> None:
        if self.last_pattern is None:
            raise RuntimeError("step the visual brain before storing")
        self.memory.add(name, self.last_pattern)

    def ram_report(self) -> Dict[str, int]:
        report = {}
        report.update(self.internal.ram_bytes())
        report.update(self.memory.ram_bytes())
        report["lens_view"] = int(0 if self.last_view is None else self.last_view.nbytes)
        report["event_map"] = int(self.last_event_map.nbytes)
        report["current_pattern"] = int(0 if self.last_pattern is None else self.last_pattern.nbytes)
        report["total_tracked_bytes"] = int(sum(report.values()))
        return report


def _to_uint8(array: np.ndarray) -> np.ndarray:
    a = np.asarray(array, dtype=np.float32)
    amin, amax = float(a.min()), float(a.max())
    if amax - amin < 1e-9:
        return np.zeros(a.shape, dtype=np.uint8)
    return np.clip((a - amin) / (amax - amin) * 255.0, 0, 255).astype(np.uint8)


def make_panel(brain: VirtualLensBrain, tick: int):
    from PIL import Image, ImageDraw

    if brain.last_world is None or brain.last_view is None:
        raise RuntimeError("brain has no frame")
    local_field, local_conf, local_pred = brain.internal.local_maps(brain.lens)
    arrays = [
        ("External world", brain.last_world),
        ("64x64 lens", brain.last_view),
        ("Persistent internal", brain.internal.field),
        ("Confidence", brain.internal.confidence),
        ("Prediction", brain.internal.prediction),
        ("Event polarity", brain.last_event_map),
    ]
    tiles = []
    for title, arr in arrays:
        image = Image.fromarray(_to_uint8(arr), mode="L").convert("RGB").resize((192, 192))
        canvas = Image.new("RGB", (192, 216), "white")
        canvas.paste(image, (0, 24))
        ImageDraw.Draw(canvas).text((6, 5), title, fill="black")
        tiles.append(canvas)

    panel = Image.new("RGB", (576, 432), "white")
    for i, tile in enumerate(tiles):
        panel.paste(tile, ((i % 3) * 192, (i // 3) * 216))
    draw = ImageDraw.Draw(panel)
    packet = brain.last_packet
    if packet:
        text = (
            f"tick={tick} events={packet.event_count} phase={packet.reference_phase:+d} "
            f"occluded={packet.occluded} pred_conf={packet.prediction_confidence:.2f}"
        )
        draw.rectangle((0, 408, 576, 432), fill="white")
        draw.text((6, 412), text, fill="black")
    return panel


def run_demo(out_dir: Path, ticks: int = 90, make_gif: bool = True) -> Dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    brain = VirtualLensBrain()
    packets: List[VisualStatePacket] = []
    panels = []
    snapshot_ticks = {8: "LEFT", 20: "APPROACH", 33: "OCCLUDED", 48: "RIGHT"}
    occlusion_errors: List[float] = []

    for tick in range(ticks):
        packet = brain.step(tick)
        packets.append(packet)
        if tick in snapshot_ticks:
            name = snapshot_ticks[tick]
            brain.store_current(name)
            if make_gif:
                make_panel(brain, tick).save(out_dir / f"snapshot_{tick:03d}_{name.lower()}.png")
        if packet.occluded and packet.predicted_x is not None and packet.predicted_y is not None:
            tx, ty = brain.world.dot_position(tick)
            occlusion_errors.append(math.hypot(packet.predicted_x - tx, packet.predicted_y - ty))
        if make_gif and tick % 2 == 0:
            panels.append(make_panel(brain, tick))

    recall_trials = []
    for name, pattern in brain.memory.patterns.items():
        cue = brain.codec.damage(pattern, fraction=0.35, label=f"damage:{name}")
        result = brain.memory.recall(cue, label=f"recall:{name}")
        recall_trials.append(
            {
                "expected": name,
                "decoded": result["decoded"],
                "correct": result["decoded"] == name,
                "overlap": result["overlap"],
                "sweeps": result["sweeps"],
                "converged": result["converged"],
                "energy_nonincreasing": result["energy_nonincreasing"],
                "raw_exact": result["raw_exact"],
            }
        )

    gif_path = out_dir / "virtual_lens_demo.gif"
    final_path = out_dir / "virtual_lens_final.png"
    if panels:
        panels[0].save(
            gif_path,
            save_all=True,
            append_images=panels[1:],
            duration=90,
            loop=0,
            optimize=False,
        )
        panels[-1].save(final_path)

    summary = {
        "version": "1.0",
        "ticks": ticks,
        "world_shape": list(WORLD_SHAPE),
        "lens_shape": list(LENS_SHAPE),
        "persistent_field_shape": list(WORLD_SHAPE),
        "total_events": sum(p.event_count for p in packets),
        "positive_events": sum(p.positive_events for p in packets),
        "negative_events": sum(p.negative_events for p in packets),
        "reference_flips": ticks,
        "loop_exists_all_ticks": all(p.loop_exists for p in packets),
        "occluded_ticks": sum(p.occluded for p in packets),
        "occlusion_prediction_mean_error_px": (
            float(np.mean(occlusion_errors)) if occlusion_errors else None
        ),
        "occlusion_prediction_max_error_px": (
            float(np.max(occlusion_errors)) if occlusion_errors else None
        ),
        "stored_visual_attractors": sorted(brain.memory.patterns),
        "recall_trials": recall_trials,
        "recall_correct": sum(t["correct"] for t in recall_trials),
        "recall_total": len(recall_trials),
        "ram": brain.ram_report(),
        "m4_status": "not integrated; compact visual state packet only",
        "boltzmann_status": "not integrated; bridge contract retained as reference",
        "physical_camera": False,
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "packets.json").write_text(
        json.dumps([asdict(p) for p in packets], indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="One-Wave Virtual Lens v1.0")
    parser.add_argument("--out", type=Path, default=Path("results"))
    parser.add_argument("--ticks", type=int, default=90)
    parser.add_argument("--no-gif", action="store_true")
    args = parser.parse_args()
    summary = run_demo(args.out, ticks=args.ticks, make_gif=not args.no_gif)
    print("ONE-WAVE VIRTUAL LENS v1.0")
    print(f"ticks: {summary['ticks']}")
    print(f"events: {summary['total_events']}")
    print(
        "visual recall: "
        f"{summary['recall_correct']}/{summary['recall_total']} damaged cues"
    )
    print(
        "occlusion prediction mean error: "
        f"{summary['occlusion_prediction_mean_error_px']:.2f}px"
        if summary["occlusion_prediction_mean_error_px"] is not None
        else "occlusion prediction mean error: n/a"
    )
    print(f"tracked RAM: {summary['ram']['total_tracked_bytes']} bytes")


if __name__ == "__main__":
    main()
