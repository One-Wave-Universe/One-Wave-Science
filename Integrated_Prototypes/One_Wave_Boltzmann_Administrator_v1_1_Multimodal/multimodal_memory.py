#!/usr/bin/env python3
"""Equal-reserve multimodal Hopfield companion for One-Wave.

This module does not replace the existing Hopfield musical brain. It adds a
second, generic Hopfield-style attractor bank that can hold five forms of the
same memory:

1. internal dialogue / language-like trace
2. sound / rhythm / auditory abstraction
3. image / spatial scene
4. body pressure / breath / interoceptive state
5. movement / gaze / proprioceptive trace

Each modality owns an equal 20 percent reserved block in the stored attractor.
Live attention is allowed to redistribute dynamically, so a memory can be
recalled mainly through dialogue, sound, pressure, or movement while a weak
visual trace remains present instead of being deleted from the architecture.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional, Sequence, Tuple

import numpy as np


class MemoryModality(str, Enum):
    DIALOGUE = "dialogue"
    SOUND = "sound"
    IMAGE = "image"
    BODY_PRESSURE = "body_pressure"
    MOVEMENT_GAZE = "movement_gaze"


MODALITIES: Tuple[MemoryModality, ...] = tuple(MemoryModality)
BASE_RESERVE_PERCENT = 20.0


@dataclass(frozen=True)
class ModalityFrame:
    """One representation of a memory.

    `features` is deliberately generic. It may later come from text embeddings,
    event-audio features, a persistent visual field, breath/pressure sensors, or
    gaze/movement state. The current simulator only requires finite signed
    numbers and therefore does not pretend that one encoding is already final.
    """

    features: Tuple[float, ...]
    confidence: float = 1.0
    label: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.features:
            raise ValueError("ModalityFrame requires at least one feature")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be within 0..1")
        if not all(math.isfinite(float(x)) for x in self.features):
            raise ValueError("features must be finite")


@dataclass(frozen=True)
class MemoryTrace:
    memory_id: str
    modalities: Mapping[MemoryModality, ModalityFrame]
    state_label: str = ""
    scale: float = 1.0
    caution: float = 0.0
    drive: float = 0.0

    def validate(self) -> None:
        if not self.memory_id:
            raise ValueError("memory_id cannot be empty")
        if not math.isfinite(self.scale) or self.scale <= 0:
            raise ValueError("scale must be positive and finite")
        for modality, frame in self.modalities.items():
            if modality not in MODALITIES:
                raise ValueError(f"unsupported modality {modality}")
            frame.validate()


@dataclass(frozen=True)
class AllocationProfile:
    """Reserved storage stays equal while live access can be uneven."""

    reserved_percent: Mapping[MemoryModality, float] = field(
        default_factory=lambda: {m: BASE_RESERVE_PERCENT for m in MODALITIES}
    )
    access_bias: Mapping[MemoryModality, float] = field(
        default_factory=lambda: {m: 1.0 for m in MODALITIES}
    )
    minimum_live_percent: float = 2.0

    def validate(self) -> None:
        missing = set(MODALITIES) - set(self.reserved_percent)
        if missing:
            raise ValueError(f"missing reserved modalities: {sorted(m.value for m in missing)}")
        total = sum(float(self.reserved_percent[m]) for m in MODALITIES)
        if not math.isclose(total, 100.0, abs_tol=1e-6):
            raise ValueError(f"reserved allocation must total 100, got {total}")
        for modality in MODALITIES:
            if self.reserved_percent[modality] <= 0:
                raise ValueError("every modality requires positive reserved capacity")
            if self.access_bias.get(modality, 0.0) <= 0:
                raise ValueError("every modality requires positive access bias")
        if not 0.0 <= self.minimum_live_percent < 20.0:
            raise ValueError("minimum_live_percent must be within 0..<20")

    def effective_attention(
        self,
        salience: Optional[Mapping[MemoryModality, float]] = None,
        mode: str = "waking",
        caution: float = 0.0,
        drive: float = 0.0,
    ) -> Dict[MemoryModality, float]:
        """Return a live 100-percent attention mix.

        Reserved capacity is not changed. This only determines how strongly each
        modality participates in the present cue/recall cycle.
        """

        self.validate()
        salience = salience or {}
        mode_factors: Dict[str, Dict[MemoryModality, float]] = {
            "waking": {
                MemoryModality.DIALOGUE: 1.10,
                MemoryModality.SOUND: 1.00,
                MemoryModality.IMAGE: 0.95,
                MemoryModality.BODY_PRESSURE: 1.05,
                MemoryModality.MOVEMENT_GAZE: 1.00,
            },
            "daydream": {
                MemoryModality.DIALOGUE: 1.15,
                MemoryModality.SOUND: 1.10,
                MemoryModality.IMAGE: 1.20,
                MemoryModality.BODY_PRESSURE: 0.95,
                MemoryModality.MOVEMENT_GAZE: 1.00,
            },
            "dream_sleep": {
                MemoryModality.DIALOGUE: 1.00,
                MemoryModality.SOUND: 1.20,
                MemoryModality.IMAGE: 1.30,
                MemoryModality.BODY_PRESSURE: 1.10,
                MemoryModality.MOVEMENT_GAZE: 0.85,
            },
        }
        factors = mode_factors.get(mode, mode_factors["waking"])

        # Caution slightly favors body pressure and dialogue checking. Drive
        # slightly favors movement and sound. These are provisional M4-facing
        # modulation hooks, not a claim that the final pathway semantics are set.
        caution_n = float(np.clip(caution / 5.5, -1.0, 1.0))
        drive_n = float(np.clip(drive / 5.5, -1.0, 1.0))
        pressure_factor = {
            MemoryModality.DIALOGUE: 1.0 + 0.12 * max(caution_n, 0.0),
            MemoryModality.SOUND: 1.0 + 0.10 * max(drive_n, 0.0),
            MemoryModality.IMAGE: 1.0,
            MemoryModality.BODY_PRESSURE: 1.0 + 0.20 * max(caution_n, 0.0),
            MemoryModality.MOVEMENT_GAZE: 1.0 + 0.18 * max(drive_n, 0.0),
        }

        raw: Dict[MemoryModality, float] = {}
        for modality in MODALITIES:
            s = float(np.clip(salience.get(modality, 0.5), 0.0, 1.0))
            # A nonzero floor lets faint imagery or sound remain available.
            raw[modality] = (
                float(self.reserved_percent[modality])
                * float(self.access_bias[modality])
                * factors[modality]
                * pressure_factor[modality]
                * (0.25 + 0.75 * s)
            )

        minimum = self.minimum_live_percent
        remaining = 100.0 - minimum * len(MODALITIES)
        total_raw = sum(raw.values())
        if total_raw <= 0:
            return {m: 20.0 for m in MODALITIES}
        return {
            modality: minimum + remaining * raw[modality] / total_raw
            for modality in MODALITIES
        }

    @classmethod
    def dialogue_sound_pressure_profile(cls) -> "AllocationProfile":
        """Example profile matching a dialogue-heavy, faint-image memory style.

        Storage remains 20 percent each. Only live access bias differs.
        """

        return cls(
            access_bias={
                MemoryModality.DIALOGUE: 2.00,
                MemoryModality.SOUND: 1.45,
                MemoryModality.IMAGE: 0.30,
                MemoryModality.BODY_PRESSURE: 1.30,
                MemoryModality.MOVEMENT_GAZE: 1.05,
            }
        )


@dataclass
class MultimodalRecall:
    expected_memory: str
    selected_memory: str
    correct_attractor: bool
    converged: bool
    sweeps: int
    initial_energy: float
    final_energy: float
    weighted_overlap: float
    modality_overlap: Dict[str, float]
    live_attention_percent: Dict[str, float]
    missing_modalities: Tuple[str, ...]

    def to_jsonable(self) -> Dict[str, Any]:
        return asdict(self)


class EqualReserveHopfieldMemory:
    """Five equal-width modality blocks in one Hopfield attractor.

    This is a companion to, not a replacement for, the original musical
    HopfieldBrain. Equal block width enforces the 20/20/20/20/20 reserved
    capacity rule. Weighted recall changes access, not stored capacity.
    """

    def __init__(self, block_width: int = 32, seed: int = 2026):
        if block_width < 4:
            raise ValueError("block_width must be at least 4")
        self.block_width = block_width
        self.vector_size = block_width * len(MODALITIES)
        self.seed = seed
        self.patterns: Dict[str, np.ndarray] = {}
        self.traces: Dict[str, MemoryTrace] = {}
        self.weights = np.zeros((self.vector_size, self.vector_size), dtype=np.float64)

    def _resample(self, values: Sequence[float]) -> np.ndarray:
        arr = np.asarray(values, dtype=np.float64)
        if arr.ndim != 1 or arr.size == 0:
            raise ValueError("features must be a non-empty one-dimensional sequence")
        if arr.size == self.block_width:
            resized = arr
        elif arr.size == 1:
            resized = np.repeat(arr, self.block_width)
        else:
            source_x = np.linspace(0.0, 1.0, arr.size)
            target_x = np.linspace(0.0, 1.0, self.block_width)
            resized = np.interp(target_x, source_x, arr)
        # Preserve zero as a valid absence only in cues. Stored memory uses
        # bipolar values so the attractor remains stable.
        return np.where(resized >= 0.0, 1.0, -1.0)

    def encode_trace(self, trace: MemoryTrace, allow_missing: bool = False) -> np.ndarray:
        trace.validate()
        blocks = []
        for modality in MODALITIES:
            frame = trace.modalities.get(modality)
            if frame is None:
                if not allow_missing:
                    raise ValueError(f"stored trace {trace.memory_id} missing {modality.value}")
                blocks.append(np.zeros(self.block_width, dtype=np.float64))
            else:
                block = self._resample(frame.features)
                # Confidence does not delete the block; it can flip low-certainty
                # cue positions to unknown when used as a partial cue.
                blocks.append(block)
        return np.concatenate(blocks)

    def store(self, trace: MemoryTrace, retrain: bool = True) -> None:
        pattern = self.encode_trace(trace, allow_missing=False)
        self.patterns[trace.memory_id] = pattern
        self.traces[trace.memory_id] = trace
        if retrain:
            self.retrain()

    def store_many(self, traces: Iterable[MemoryTrace]) -> None:
        for trace in traces:
            self.store(trace, retrain=False)
        self.retrain()

    def retrain(self) -> None:
        self.weights.fill(0.0)
        if not self.patterns:
            return
        scale = 1.0 / self.vector_size
        for pattern in self.patterns.values():
            self.weights += scale * np.outer(pattern, pattern)
        np.fill_diagonal(self.weights, 0.0)

    def energy(self, state: np.ndarray) -> float:
        return float(-0.5 * state @ self.weights @ state)

    def _block_slice(self, modality: MemoryModality) -> slice:
        idx = MODALITIES.index(modality)
        return slice(idx * self.block_width, (idx + 1) * self.block_width)

    def partial_cue(
        self,
        trace: MemoryTrace,
        available: Iterable[MemoryModality],
        confidence_threshold: float = 0.15,
    ) -> Tuple[np.ndarray, set[int], Tuple[str, ...]]:
        available_set = set(available)
        cue = np.zeros(self.vector_size, dtype=np.float64)
        clamped: set[int] = set()
        missing = []
        for modality in MODALITIES:
            sl = self._block_slice(modality)
            frame = trace.modalities.get(modality)
            if modality not in available_set or frame is None or frame.confidence < confidence_threshold:
                missing.append(modality.value)
                continue
            cue[sl] = self._resample(frame.features)
            clamped.update(range(sl.start, sl.stop))
        return cue, clamped, tuple(missing)

    def _source_weights(self, attention: Mapping[MemoryModality, float]) -> np.ndarray:
        out = np.zeros(self.vector_size, dtype=np.float64)
        for modality in MODALITIES:
            sl = self._block_slice(modality)
            out[sl] = max(float(attention.get(modality, 20.0)), 0.01) / 20.0
        return out

    def settle(
        self,
        initial: np.ndarray,
        clamped: set[int],
        attention: Mapping[MemoryModality, float],
        label: str,
        max_sweeps: int = 80,
    ) -> Tuple[np.ndarray, list[float], int, bool]:
        if initial.shape != (self.vector_size,):
            raise ValueError("initial cue has wrong width")
        state = initial.copy()
        rng = random.Random((hash(label) ^ self.seed) & 0xFFFFFFFF)
        mutable = [i for i in range(self.vector_size) if i not in clamped]
        source_weight = self._source_weights(attention)
        energies = [self.energy(state)]
        for sweep in range(1, max_sweeps + 1):
            rng.shuffle(mutable)
            changed = 0
            weighted_state = state * source_weight
            for i in mutable:
                h = float(self.weights[i] @ weighted_state)
                new = 1.0 if h >= 0.0 else -1.0
                if new != state[i]:
                    state[i] = new
                    changed += 1
                    weighted_state[i] = new * source_weight[i]
            energies.append(self.energy(state))
            if changed == 0:
                return state, energies, sweep, True
        return state, energies, max_sweeps, False

    def modality_overlap(self, a: np.ndarray, b: np.ndarray) -> Dict[MemoryModality, float]:
        result: Dict[MemoryModality, float] = {}
        for modality in MODALITIES:
            sl = self._block_slice(modality)
            result[modality] = float(np.mean(a[sl] == b[sl]))
        return result

    def weighted_overlap(
        self,
        a: np.ndarray,
        b: np.ndarray,
        attention: Mapping[MemoryModality, float],
    ) -> float:
        per = self.modality_overlap(a, b)
        total = sum(float(attention[m]) for m in MODALITIES)
        return sum(per[m] * float(attention[m]) for m in MODALITIES) / max(total, 1e-9)

    def recall(
        self,
        expected_memory: str,
        cue: MemoryTrace,
        available: Iterable[MemoryModality],
        profile: Optional[AllocationProfile] = None,
        salience: Optional[Mapping[MemoryModality, float]] = None,
        mode: str = "waking",
    ) -> MultimodalRecall:
        if expected_memory not in self.patterns:
            raise KeyError(expected_memory)
        profile = profile or AllocationProfile()
        attention = profile.effective_attention(
            salience=salience,
            mode=mode,
            caution=cue.caution,
            drive=cue.drive,
        )
        initial, clamped, missing = self.partial_cue(cue, available)
        settled, energies, sweeps, converged = self.settle(
            initial,
            clamped,
            attention,
            label=f"{expected_memory}|{mode}|{','.join(sorted(missing))}",
        )
        selected = max(
            self.patterns,
            key=lambda name: self.weighted_overlap(settled, self.patterns[name], attention),
        )
        selected_pattern = self.patterns[selected]
        per = self.modality_overlap(settled, selected_pattern)
        return MultimodalRecall(
            expected_memory=expected_memory,
            selected_memory=selected,
            correct_attractor=selected == expected_memory,
            converged=converged,
            sweeps=sweeps,
            initial_energy=energies[0],
            final_energy=energies[-1],
            weighted_overlap=self.weighted_overlap(settled, selected_pattern, attention),
            modality_overlap={m.value: per[m] for m in MODALITIES},
            live_attention_percent={m.value: attention[m] for m in MODALITIES},
            missing_modalities=missing,
        )

    def save(self, path: Path) -> None:
        payload: Dict[str, Any] = {
            "version": "1.0",
            "block_width": self.block_width,
            "seed": self.seed,
            "traces": {},
            "weights": self.weights.tolist(),
        }
        for memory_id, trace in self.traces.items():
            payload["traces"][memory_id] = {
                "state_label": trace.state_label,
                "scale": trace.scale,
                "caution": trace.caution,
                "drive": trace.drive,
                "modalities": {
                    modality.value: {
                        "features": list(frame.features),
                        "confidence": frame.confidence,
                        "label": frame.label,
                        "metadata": dict(frame.metadata),
                    }
                    for modality, frame in trace.modalities.items()
                },
            }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Example traces used by the audit, not canonical encodings.
# ---------------------------------------------------------------------------


def _frame(values: Sequence[float], label: str, confidence: float = 1.0) -> ModalityFrame:
    return ModalityFrame(tuple(float(x) for x in values), confidence=confidence, label=label)


def example_traces() -> Tuple[MemoryTrace, ...]:
    """Small numerical stand-ins for multimodal memory experiments."""

    return (
        MemoryTrace(
            memory_id="COMPRESS_RELEASE",
            state_label="RELIEF",
            scale=1.0,
            caution=1.0,
            drive=0.5,
            modalities={
                MemoryModality.DIALOGUE: _frame(
                    [-1, -0.8, -0.3, 0.2, 0.8, 1.0],
                    "running internal transcript: hold, release, safe",
                ),
                MemoryModality.SOUND: _frame(
                    [-1, -0.7, -0.2, 0.4, 0.9, 0.2],
                    "compressed sound abstraction opening into relief",
                ),
                MemoryModality.IMAGE: _frame(
                    [-0.2, 0.1, 0.2, 0.0, 0.1, 0.2],
                    "faint overlapping movement image",
                    confidence=0.25,
                ),
                MemoryModality.BODY_PRESSURE: _frame(
                    [-1, -1, -0.8, -0.2, 0.6, 1.0],
                    "breath held/compressed then expressive exhale relief",
                ),
                MemoryModality.MOVEMENT_GAZE: _frame(
                    [-0.8, -0.2, 0.5, 1.0, 0.4, -0.2],
                    "eye movement and vague motion trace",
                ),
            },
        ),
        MemoryTrace(
            memory_id="CAUTION_HOLD",
            state_label="CAUTION",
            scale=1.2,
            caution=4.2,
            drive=-0.5,
            modalities={
                MemoryModality.DIALOGUE: _frame([1, 1, 0.7, 0.3, -0.4, -1], "check before acting"),
                MemoryModality.SOUND: _frame([0.8, 0.4, -0.2, -0.8, -1, -0.7], "damped warning rhythm"),
                MemoryModality.IMAGE: _frame([0.1, 0.2, -0.1, -0.2, 0.1, 0.0], "faint blocked path", 0.20),
                MemoryModality.BODY_PRESSURE: _frame([1, 0.9, 0.8, 0.7, 0.5, 0.4], "held pressure"),
                MemoryModality.MOVEMENT_GAZE: _frame([1, 0.5, 0, -0.5, -1, -0.5], "scan and stop"),
            },
        ),
        MemoryTrace(
            memory_id="DRIVE_APPROACH",
            state_label="DRIVE",
            scale=1.1,
            caution=0.2,
            drive=4.0,
            modalities={
                MemoryModality.DIALOGUE: _frame([-1, -0.3, 0.3, 0.8, 1, 1], "go toward target"),
                MemoryModality.SOUND: _frame([-0.8, -0.2, 0.3, 0.7, 1, 0.7], "rising approach rhythm"),
                MemoryModality.IMAGE: _frame([-0.1, 0.0, 0.1, 0.2, 0.3, 0.2], "faint target movement", 0.30),
                MemoryModality.BODY_PRESSURE: _frame([-0.3, 0.1, 0.4, 0.6, 0.9, 1], "forward pressure"),
                MemoryModality.MOVEMENT_GAZE: _frame([-1, -0.4, 0.2, 0.7, 1, 1], "eyes and body approach"),
            },
        ),
    )
