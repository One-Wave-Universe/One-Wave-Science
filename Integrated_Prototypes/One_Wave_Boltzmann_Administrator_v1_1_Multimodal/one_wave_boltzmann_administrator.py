#!/usr/bin/env python3
"""
ONE-WAVE BOLTZMANN ADMINISTRATOR v1.1 MULTIMODAL
=====================================

A tested Boltzmann-style compressive Administrator for the One-Wave
three-brain architecture.

Scope intentionally stays on the Administrator side:
- five signed duplex pathways arrive as NEW oversight moving upward;
- five signed reference pathways arrive as OLD oversight moving downward;
- both use the same -5.5 .. +5.5 bridge coordinates;
- a joint Restricted Boltzmann Machine learns state/action relationships;
- the six-line loop enforces: 4 tells 5, 5 tells 6, 6 tells everybody;
- Gate 6 broadcasts the resolved state and returns the next OLD reference;
- waking, daydream, and dream-sleep modes alter temperature/output gating;
- M4 and Hopfield are external peers connected through explicit packets.

This is not a claim of consciousness or biological equivalence. It is a
reference implementation and audit harness for the compressive memory layer.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Canonical bridge contract
# ---------------------------------------------------------------------------

PATHWAY_COUNT = 5
GROUND_MIN = -5.5
GROUND_MAX = 5.5
GROUND_STEP = 0.5
ACTION_NAMES: Tuple[str, ...] = (
    "HOLD",
    "CONSERVE",
    "GATHER",
    "MOVE_TO_MEMORY",
    "EXPLORE",
    "SHARE",
)


class BrainMode(str, Enum):
    WAKING = "waking"
    DAYDREAM = "daydream"
    DREAM_SLEEP = "dream_sleep"


@dataclass(frozen=True)
class BridgePacket:
    """Shared numeric packet expected from M4/Hopfield-facing adapters.

    new_up:
        Five signed values carrying current/new oversight upward.
    old_down:
        Five signed values carrying the previous resolved reference downward.

    Values are continuous bridge coordinates, not hard binary states.
    """

    new_up: Tuple[float, float, float, float, float]
    old_down: Tuple[float, float, float, float, float]
    tick: int
    flip_phase: int = 0
    mode: BrainMode = BrainMode.WAKING
    source: str = "M4"
    loop_id: str = "default"
    state_label: str = "ACTIVE"
    scale: float = 1.0
    caution: float = 0.0
    drive: float = 0.0
    external_output_requested: bool = False

    def validate(self) -> None:
        if len(self.new_up) != PATHWAY_COUNT or len(self.old_down) != PATHWAY_COUNT:
            raise ValueError("BridgePacket requires exactly five new and five old pathways")
        for group_name, values in (("new_up", self.new_up), ("old_down", self.old_down)):
            for index, value in enumerate(values):
                if not math.isfinite(value):
                    raise ValueError(f"{group_name}[{index}] is not finite")
                if value < GROUND_MIN or value > GROUND_MAX:
                    raise ValueError(
                        f"{group_name}[{index}]={value} outside [{GROUND_MIN}, {GROUND_MAX}]"
                    )
        if self.flip_phase not in (0, 1):
            raise ValueError("flip_phase must be 0 or 1")
        if self.tick < 0:
            raise ValueError("tick must be non-negative")
        if not math.isfinite(self.scale) or self.scale <= 0:
            raise ValueError("scale must be finite and positive")


@dataclass
class GateEvent:
    gate: int
    name: str
    message: str
    new_up: List[float]
    old_down: List[float]
    temperature: float
    action_distribution: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0
    free_energy: Optional[float] = None


@dataclass
class AdministratorResult:
    tick: int
    loop_id: str
    mode: str
    committed_action: str
    confidence: float
    temperature: float
    loop_exists: bool
    external_release_recommended: bool
    next_old_reference: Tuple[float, float, float, float, float]
    hidden_activation: List[float]
    reconstructed_new: Tuple[float, float, float, float, float]
    reconstructed_old: Tuple[float, float, float, float, float]
    gate_events: List[GateEvent]
    broadcast: Dict[str, Any]

    def to_jsonable(self) -> Dict[str, Any]:
        data = asdict(self)
        return data


# ---------------------------------------------------------------------------
# Signed bridge codec
# ---------------------------------------------------------------------------


class SignedBridgeCodec:
    """Encodes continuous signed pathways as bipolar thermometer rails.

    Every pathway receives:
    - 11 negative magnitude bits (0.5 through 5.5),
    - one center bit,
    - 11 positive magnitude bits (0.5 through 5.5).

    This preserves sign, magnitude, range width, and graceful neighborhood
    generalization while still giving the Bernoulli RBM binary visible units.
    """

    magnitudes = np.arange(GROUND_STEP, GROUND_MAX + 1e-9, GROUND_STEP)
    bits_per_path = len(magnitudes) * 2 + 1

    def __init__(self, pathways: int = PATHWAY_COUNT):
        self.pathways = pathways
        self.group_count = pathways * 2  # NEW + OLD
        self.state_bits = self.group_count * self.bits_per_path
        self.action_bits = len(ACTION_NAMES)
        self.visible_bits = self.state_bits + self.action_bits

    @staticmethod
    def _clip(value: float) -> float:
        return float(np.clip(value, GROUND_MIN, GROUND_MAX))

    def encode_value(self, value: float) -> np.ndarray:
        value = self._clip(value)
        out = np.zeros(self.bits_per_path, dtype=np.float64)
        split = len(self.magnitudes)
        if abs(value) < GROUND_STEP / 2:
            out[split] = 1.0
            return out
        count = int(np.clip(math.ceil(abs(value) / GROUND_STEP), 1, split))
        if value < 0:
            out[:count] = 1.0
        else:
            out[split + 1 : split + 1 + count] = 1.0
        return out

    def decode_value(self, bits: Sequence[float]) -> float:
        arr = np.asarray(bits, dtype=np.float64)
        split = len(self.magnitudes)
        neg = float(np.sum(arr[:split] >= 0.5))
        pos = float(np.sum(arr[split + 1 :] >= 0.5))
        if neg == 0 and pos == 0:
            return 0.0
        return float(np.clip((pos - neg) * GROUND_STEP, GROUND_MIN, GROUND_MAX))

    def encode_state(self, new_up: Sequence[float], old_down: Sequence[float]) -> np.ndarray:
        if len(new_up) != self.pathways or len(old_down) != self.pathways:
            raise ValueError("State requires five NEW and five OLD values")
        chunks = [self.encode_value(v) for v in (*new_up, *old_down)]
        return np.concatenate(chunks)

    def decode_state(self, state_bits: Sequence[float]) -> Tuple[Tuple[float, ...], Tuple[float, ...]]:
        arr = np.asarray(state_bits, dtype=np.float64)
        if arr.shape != (self.state_bits,):
            raise ValueError(f"Expected {self.state_bits} state bits, got {arr.shape}")
        values: List[float] = []
        for i in range(self.group_count):
            start = i * self.bits_per_path
            values.append(self.decode_value(arr[start : start + self.bits_per_path]))
        return tuple(values[: self.pathways]), tuple(values[self.pathways :])

    def encode_joint(
        self,
        new_up: Sequence[float],
        old_down: Sequence[float],
        action_index: int,
    ) -> np.ndarray:
        state = self.encode_state(new_up, old_down)
        action = np.zeros(self.action_bits, dtype=np.float64)
        action[action_index] = 1.0
        return np.concatenate([state, action])

    def state_only_joint(self, new_up: Sequence[float], old_down: Sequence[float]) -> np.ndarray:
        return np.concatenate(
            [self.encode_state(new_up, old_down), np.zeros(self.action_bits, dtype=np.float64)]
        )


# ---------------------------------------------------------------------------
# Restricted Boltzmann Machine
# ---------------------------------------------------------------------------


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))


class JointRBM:
    """Bernoulli-Bernoulli RBM over signed-state encoding plus action bits."""

    def __init__(
        self,
        n_visible: int,
        n_hidden: int = 64,
        seed: int = 2026,
    ) -> None:
        self.n_visible = n_visible
        self.n_hidden = n_hidden
        self.rng = np.random.default_rng(seed)
        self.W = self.rng.normal(0.0, 0.02, size=(n_visible, n_hidden))
        self.vbias = np.zeros(n_visible, dtype=np.float64)
        self.hbias = np.zeros(n_hidden, dtype=np.float64)
        self.training_history: List[Dict[str, float]] = []

    def hidden_prob(self, visible: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        return sigmoid((visible @ self.W + self.hbias) / max(temperature, 1e-6))

    def visible_prob(self, hidden: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        return sigmoid((hidden @ self.W.T + self.vbias) / max(temperature, 1e-6))

    def sample(self, probs: np.ndarray) -> np.ndarray:
        return (self.rng.random(probs.shape) < probs).astype(np.float64)

    def free_energy(self, visible: np.ndarray) -> np.ndarray:
        v = np.atleast_2d(visible)
        hidden_term = np.sum(np.logaddexp(0.0, v @ self.W + self.hbias), axis=1)
        visible_term = v @ self.vbias
        energy = -visible_term - hidden_term
        return energy if visible.ndim > 1 else energy[0]

    def fit(
        self,
        data: np.ndarray,
        epochs: int = 80,
        batch_size: int = 64,
        learning_rate: float = 0.04,
        k: int = 1,
        weight_decay: float = 1e-4,
        momentum: float = 0.5,
        verbose: bool = False,
    ) -> List[Dict[str, float]]:
        if data.ndim != 2 or data.shape[1] != self.n_visible:
            raise ValueError("Training data shape does not match RBM visible width")
        n = data.shape[0]
        dW = np.zeros_like(self.W)
        dvb = np.zeros_like(self.vbias)
        dhb = np.zeros_like(self.hbias)

        self.training_history = []
        for epoch in range(epochs):
            order = self.rng.permutation(n)
            reconstruction_total = 0.0
            batches = 0
            for start in range(0, n, batch_size):
                v0 = data[order[start : start + batch_size]]
                ph0 = self.hidden_prob(v0)
                h = self.sample(ph0)
                vk = v0.copy()
                phk = ph0
                for _ in range(k):
                    pvk = self.visible_prob(h)
                    vk = self.sample(pvk)
                    phk = self.hidden_prob(vk)
                    h = self.sample(phk)

                positive = v0.T @ ph0 / len(v0)
                negative = vk.T @ phk / len(v0)
                grad_W = positive - negative - weight_decay * self.W
                grad_v = np.mean(v0 - vk, axis=0)
                grad_h = np.mean(ph0 - phk, axis=0)

                dW = momentum * dW + learning_rate * grad_W
                dvb = momentum * dvb + learning_rate * grad_v
                dhb = momentum * dhb + learning_rate * grad_h
                self.W += dW
                self.vbias += dvb
                self.hbias += dhb

                reconstruction_total += float(np.mean((v0 - pvk) ** 2))
                batches += 1

            mse = reconstruction_total / max(batches, 1)
            record = {"epoch": float(epoch + 1), "reconstruction_mse": mse}
            self.training_history.append(record)
            if verbose and ((epoch + 1) % 10 == 0 or epoch == 0):
                print(f"epoch={epoch+1:3d} reconstruction_mse={mse:.6f}")
        return self.training_history

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path,
            W=self.W,
            vbias=self.vbias,
            hbias=self.hbias,
            n_visible=np.array([self.n_visible]),
            n_hidden=np.array([self.n_hidden]),
        )

    @classmethod
    def load(cls, path: Path, seed: int = 2026) -> "JointRBM":
        with np.load(path) as data:
            model = cls(int(data["n_visible"][0]), int(data["n_hidden"][0]), seed=seed)
            model.W = data["W"].astype(np.float64)
            model.vbias = data["vbias"].astype(np.float64)
            model.hbias = data["hbias"].astype(np.float64)
        return model


# ---------------------------------------------------------------------------
# Training scenarios (test adapter, not canonical pathway semantics)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Scenario:
    new_up: Tuple[float, float, float, float, float]
    old_down: Tuple[float, float, float, float, float]
    action: str


class SurvivalScenarioFactory:
    """Creates a five-path Goblin survival adapter for testing.

    Test-only pathway meanings:
      1 energy reserve
      2 immediate resource evidence
      3 danger pressure
      4 memory reliability
      5 social corroboration

    Canonical code exposes generic pathway numbers; these labels only make the
    audit interpretable and can later be replaced by M4-derived signals.
    """

    def __init__(self, seed: int = 2026):
        self.rng = np.random.default_rng(seed)

    @staticmethod
    def oracle(new: Sequence[float], old: Sequence[float]) -> str:
        energy, resource, danger, memory, social = new
        old_energy, old_resource, old_danger, old_memory, old_social = old

        # Simultaneous new-up / old-down comparison. Old reference matters most
        # near ambiguous boundaries, preventing a purely reactive classifier.
        e = energy + 0.25 * old_energy
        r = resource + 0.35 * old_resource
        d = danger + 0.30 * old_danger
        m = memory + 0.35 * old_memory
        s = social + 0.20 * old_social

        if d >= 3.0:
            return "HOLD"
        if r >= 2.2 and d < 2.0:
            return "GATHER"
        if e <= -2.5 and r < 1.0:
            return "CONSERVE"
        if m >= 2.2 and r < 2.2 and d < 2.0:
            return "MOVE_TO_MEMORY"
        if s >= 3.0 and e > -1.0 and (r > 1.0 or m > 1.0):
            return "SHARE"
        return "EXPLORE"

    def make(self, count: int) -> List[Scenario]:
        scenarios: List[Scenario] = []
        for _ in range(count):
            old = self.rng.uniform(GROUND_MIN, GROUND_MAX, size=PATHWAY_COUNT)
            drift = self.rng.normal(0.0, 1.35, size=PATHWAY_COUNT)
            new = np.clip(old * 0.45 + drift, GROUND_MIN, GROUND_MAX)
            action = self.oracle(new, old)
            scenarios.append(
                Scenario(
                    tuple(float(x) for x in new),
                    tuple(float(x) for x in old),
                    action,
                )
            )
        return scenarios


# ---------------------------------------------------------------------------
# Six-line Administrator
# ---------------------------------------------------------------------------


class BoltzmannAdministrator:
    def __init__(
        self,
        rbm: JointRBM,
        codec: Optional[SignedBridgeCodec] = None,
        confidence_threshold: float = 0.34,
        speech_threshold: float = 0.62,
        seed: int = 2026,
    ) -> None:
        self.codec = codec or SignedBridgeCodec()
        self.rbm = rbm
        self.confidence_threshold = confidence_threshold
        self.speech_threshold = speech_threshold
        self.rng = np.random.default_rng(seed)
        self.last_action = "HOLD"
        self.last_reference: Tuple[float, ...] = (0.0,) * PATHWAY_COUNT
        self.loop_counter = 0

    @staticmethod
    def mode_temperature(mode: BrainMode) -> float:
        return {
            BrainMode.WAKING: 0.72,
            BrainMode.DAYDREAM: 1.15,
            BrainMode.DREAM_SLEEP: 1.45,
        }[mode]

    def action_distribution(
        self,
        new_up: Sequence[float],
        old_down: Sequence[float],
        temperature: float,
    ) -> Tuple[np.ndarray, np.ndarray]:
        energies = []
        state = self.codec.encode_state(new_up, old_down)
        for action_idx in range(len(ACTION_NAMES)):
            action = np.zeros(len(ACTION_NAMES), dtype=np.float64)
            action[action_idx] = 1.0
            visible = np.concatenate([state, action])
            energies.append(float(self.rbm.free_energy(visible)))
        e = np.asarray(energies, dtype=np.float64)
        logits = -(e - np.min(e)) / max(temperature, 1e-6)
        logits -= np.max(logits)
        probs = np.exp(logits)
        probs /= np.sum(probs)
        return probs, e

    def reconstruct_state(
        self,
        new_up: Sequence[float],
        old_down: Sequence[float],
        action_index: int,
        temperature: float,
    ) -> Tuple[Tuple[float, ...], Tuple[float, ...], np.ndarray]:
        visible = self.codec.encode_joint(new_up, old_down, action_index)
        hprob = self.rbm.hidden_prob(visible, temperature=temperature)
        vprob = self.rbm.visible_prob(hprob, temperature=temperature)
        new_rec, old_rec = self.codec.decode_state(vprob[: self.codec.state_bits])
        return new_rec, old_rec, hprob

    def _next_reference(
        self,
        new_up: Sequence[float],
        old_down: Sequence[float],
        action: str,
        confidence: float,
    ) -> Tuple[float, ...]:
        # Gate 6 does not erase history. It compresses current + previous into a
        # bounded next OLD reference. Confidence controls how much new state is
        # permitted to overwrite established reference.
        blend = float(np.clip(0.25 + 0.60 * confidence, 0.25, 0.85))
        action_bias = {
            "HOLD": -0.10,
            "CONSERVE": -0.18,
            "GATHER": 0.18,
            "MOVE_TO_MEMORY": 0.08,
            "EXPLORE": 0.05,
            "SHARE": 0.10,
        }[action]
        out = []
        for current, previous in zip(new_up, old_down):
            value = blend * current + (1.0 - blend) * previous + action_bias
            out.append(float(np.clip(value, GROUND_MIN, GROUND_MAX)))
        return tuple(out)

    def run_cycle(self, packet: BridgePacket) -> AdministratorResult:
        packet.validate()
        self.loop_counter += 1
        base_temp = self.mode_temperature(packet.mode)
        events: List[GateEvent] = []

        # Gate 1: BEGIN
        events.append(
            GateEvent(
                gate=1,
                name="BEGIN",
                message="Received five NEW-up and five OLD-down reference pathways.",
                new_up=list(packet.new_up),
                old_down=list(packet.old_down),
                temperature=base_temp,
            )
        )

        # Gate 2: BUILD
        build_probs, build_energies = self.action_distribution(
            packet.new_up, packet.old_down, temperature=base_temp * 1.12
        )
        build_dist = {a: float(p) for a, p in zip(ACTION_NAMES, build_probs)}
        events.append(
            GateEvent(
                gate=2,
                name="BUILD",
                message="Generated stochastic candidate actions from joint free energies.",
                new_up=list(packet.new_up),
                old_down=list(packet.old_down),
                temperature=base_temp * 1.12,
                action_distribution=build_dist,
                confidence=float(np.max(build_probs)),
            )
        )

        # Gate 3: HOLD
        # Preserve candidate diversity while adding a small previous-action prior.
        hold_probs = build_probs.copy()
        prior_idx = ACTION_NAMES.index(self.last_action)
        hold_probs[prior_idx] += 0.035
        hold_probs /= np.sum(hold_probs)
        events.append(
            GateEvent(
                gate=3,
                name="HOLD",
                message="Held multiple candidates and compared them with the previous resolved action.",
                new_up=list(packet.new_up),
                old_down=list(packet.old_down),
                temperature=base_temp,
                action_distribution={a: float(p) for a, p in zip(ACTION_NAMES, hold_probs)},
                confidence=float(np.max(hold_probs)),
            )
        )

        # Gate 4: BUILD AGAIN. Four tells five.
        refined_temp = max(0.42, base_temp * 0.78)
        refined_probs, refined_energies = self.action_distribution(
            packet.new_up, packet.old_down, temperature=refined_temp
        )
        mixed = 0.35 * hold_probs + 0.65 * refined_probs
        mixed /= np.sum(mixed)
        events.append(
            GateEvent(
                gate=4,
                name="BUILD_AGAIN",
                message="4 tells 5: rebuilt candidates at lower temperature using old reference oversight.",
                new_up=list(packet.new_up),
                old_down=list(packet.old_down),
                temperature=refined_temp,
                action_distribution={a: float(p) for a, p in zip(ACTION_NAMES, mixed)},
                confidence=float(np.max(mixed)),
            )
        )

        # Gate 5: BREAK. Five tells six.
        candidate_idx = int(np.argmax(mixed))
        confidence = float(mixed[candidate_idx])
        chosen_idx = candidate_idx
        break_message = "5 tells 6: candidate accepted for closure."
        if confidence < self.confidence_threshold:
            chosen_idx = ACTION_NAMES.index("HOLD")
            break_message = "5 tells 6: confidence below threshold; candidate rejected and HOLD substituted."
        chosen_action = ACTION_NAMES[chosen_idx]
        chosen_energy = float(refined_energies[chosen_idx])
        events.append(
            GateEvent(
                gate=5,
                name="BREAK",
                message=break_message,
                new_up=list(packet.new_up),
                old_down=list(packet.old_down),
                temperature=refined_temp,
                action_distribution={a: float(p) for a, p in zip(ACTION_NAMES, mixed)},
                confidence=confidence,
                free_energy=chosen_energy,
            )
        )

        # Gate 6: LOOP. Six tells everybody.
        rec_new, rec_old, hidden = self.reconstruct_state(
            packet.new_up, packet.old_down, chosen_idx, temperature=refined_temp
        )
        next_reference = self._next_reference(
            packet.new_up, packet.old_down, chosen_action, confidence
        )
        external_release = (
            packet.mode == BrainMode.WAKING
            and packet.external_output_requested
            and confidence >= self.speech_threshold
        )
        loop_exists = bool(np.all(np.isfinite(hidden)) and hidden.size == self.rbm.n_hidden)
        broadcast = {
            "rule": "6 tells everybody",
            "tick": packet.tick,
            "loop_id": packet.loop_id,
            "committed_action": chosen_action,
            "confidence": confidence,
            "next_old_reference": list(next_reference),
            "internal_dialogue_summary": f"Administrator resolved {chosen_action} at confidence {confidence:.3f}.",
            "image_summary_channel": "available_for_compressed_scene_summary",
            "sound_summary_channel": "available_for_compressed_sound_summary",
            "external_release_recommended": external_release,
            "loop_exists": loop_exists,
        }
        events.append(
            GateEvent(
                gate=6,
                name="LOOP",
                message="6 tells everybody: broadcast resolved state and returned the next OLD reference downward.",
                new_up=list(packet.new_up),
                old_down=list(next_reference),
                temperature=refined_temp,
                action_distribution={a: float(p) for a, p in zip(ACTION_NAMES, mixed)},
                confidence=confidence,
                free_energy=chosen_energy,
            )
        )

        self.last_action = chosen_action
        self.last_reference = next_reference

        return AdministratorResult(
            tick=packet.tick,
            loop_id=packet.loop_id,
            mode=packet.mode.value,
            committed_action=chosen_action,
            confidence=confidence,
            temperature=refined_temp,
            loop_exists=loop_exists,
            external_release_recommended=external_release,
            next_old_reference=tuple(float(x) for x in next_reference),
            hidden_activation=[float(x) for x in hidden],
            reconstructed_new=tuple(float(x) for x in rec_new),
            reconstructed_old=tuple(float(x) for x in rec_old),
            gate_events=events,
            broadcast=broadcast,
        )


# ---------------------------------------------------------------------------
# Goblin test arena
# ---------------------------------------------------------------------------


@dataclass
class ArenaResult:
    policy: str
    seeds: int
    ticks: int
    survived_runs: int
    mean_final_energy: float
    mean_food_gathered: float
    mean_bad_actions: float
    mean_gate6_broadcasts: float


class GoblinAdministratorArena:
    """Small behavior shell for testing Administrator decisions."""

    def __init__(self, administrator: BoltzmannAdministrator, seed: int = 2026):
        self.administrator = administrator
        self.seed = seed

    @staticmethod
    def _scale_energy(energy: float) -> float:
        return float(np.clip((energy - 50.0) / 50.0 * GROUND_MAX, GROUND_MIN, GROUND_MAX))

    def run(self, seeds: int = 30, ticks: int = 160, random_policy: bool = False) -> ArenaResult:
        survived = 0
        final_energy: List[float] = []
        gathered: List[float] = []
        bad_actions: List[float] = []
        broadcasts: List[float] = []

        for seed_offset in range(seeds):
            rng = np.random.default_rng(self.seed + seed_offset)
            energy = 72.0
            resource = float(rng.uniform(-1.5, 4.5))
            danger = float(rng.uniform(-1.5, 2.5))
            memory = float(rng.uniform(-2.0, 3.5))
            social = float(rng.uniform(-2.0, 3.0))
            old = (0.0,) * PATHWAY_COUNT
            food_total = 0.0
            bad = 0
            gate6 = 0

            for tick in range(ticks):
                if energy <= 0:
                    break
                # World drift.
                resource = float(np.clip(resource + rng.normal(0.0, 0.7), GROUND_MIN, GROUND_MAX))
                danger = float(np.clip(danger * 0.72 + rng.normal(0.0, 0.9), GROUND_MIN, GROUND_MAX))
                memory = float(np.clip(memory * 0.92 + rng.normal(0.0, 0.45), GROUND_MIN, GROUND_MAX))
                social = float(np.clip(social * 0.90 + rng.normal(0.0, 0.45), GROUND_MIN, GROUND_MAX))
                new = (self._scale_energy(energy), resource, danger, memory, social)

                oracle = SurvivalScenarioFactory.oracle(new, old)
                if random_policy:
                    action = str(rng.choice(ACTION_NAMES))
                    next_old = tuple(0.65 * n + 0.35 * o for n, o in zip(new, old))
                else:
                    packet = BridgePacket(
                        new_up=tuple(float(x) for x in new),
                        old_down=tuple(float(x) for x in old),
                        tick=tick,
                        flip_phase=tick % 2,
                        mode=BrainMode.WAKING,
                        loop_id=f"arena-{seed_offset}",
                    )
                    result = self.administrator.run_cycle(packet)
                    action = result.committed_action
                    next_old = result.next_old_reference
                    gate6 += int(result.broadcast.get("rule") == "6 tells everybody")

                if action != oracle:
                    bad += 1

                # Energy and world consequences.
                energy -= 1.0
                if danger >= 3.0 and action != "HOLD":
                    energy -= 7.0
                elif action == "HOLD":
                    energy -= 0.2
                    danger -= 1.0
                elif action == "CONSERVE":
                    energy += 1.2
                elif action == "GATHER":
                    if resource >= 1.5 and danger < 2.5:
                        gain = min(10.0, 3.0 + resource)
                        energy += gain
                        food_total += gain
                        resource -= 2.4
                        memory = min(GROUND_MAX, memory + 1.2)
                    else:
                        energy -= 2.5
                elif action == "MOVE_TO_MEMORY":
                    if memory >= 1.5:
                        energy += 4.0
                        resource = min(GROUND_MAX, resource + 1.4)
                        memory -= 0.8
                    else:
                        energy -= 2.5
                elif action == "EXPLORE":
                    energy -= 1.2
                    if rng.random() < 0.34:
                        resource = min(GROUND_MAX, resource + 2.8)
                        memory = min(GROUND_MAX, memory + 1.5)
                elif action == "SHARE":
                    energy -= 1.0
                    social = min(GROUND_MAX, social + 1.4)
                    memory = min(GROUND_MAX, memory + 0.8)

                energy = float(np.clip(energy, 0.0, 100.0))
                old = tuple(float(np.clip(x, GROUND_MIN, GROUND_MAX)) for x in next_old)

            survived += int(energy > 0)
            final_energy.append(energy)
            gathered.append(food_total)
            bad_actions.append(float(bad))
            broadcasts.append(float(gate6))

        return ArenaResult(
            policy="random" if random_policy else "boltzmann",
            seeds=seeds,
            ticks=ticks,
            survived_runs=survived,
            mean_final_energy=float(np.mean(final_energy)),
            mean_food_gathered=float(np.mean(gathered)),
            mean_bad_actions=float(np.mean(bad_actions)),
            mean_gate6_broadcasts=float(np.mean(broadcasts)),
        )


# ---------------------------------------------------------------------------
# Training and audit helpers
# ---------------------------------------------------------------------------


def scenarios_to_matrix(scenarios: Sequence[Scenario], codec: SignedBridgeCodec) -> np.ndarray:
    rows = []
    for scenario in scenarios:
        action_idx = ACTION_NAMES.index(scenario.action)
        rows.append(codec.encode_joint(scenario.new_up, scenario.old_down, action_idx))
    return np.asarray(rows, dtype=np.float64)


def train_default_model(
    seed: int = 2026,
    train_count: int = 6000,
    epochs: int = 85,
    verbose: bool = False,
) -> Tuple[JointRBM, SignedBridgeCodec, List[Scenario], List[Scenario]]:
    codec = SignedBridgeCodec()
    factory = SurvivalScenarioFactory(seed=seed)
    all_scenarios = factory.make(train_count + 1600)
    train = all_scenarios[:train_count]
    test = all_scenarios[train_count:]
    data = scenarios_to_matrix(train, codec)
    model = JointRBM(codec.visible_bits, n_hidden=72, seed=seed)
    model.fit(
        data,
        epochs=epochs,
        batch_size=96,
        learning_rate=0.035,
        k=1,
        weight_decay=1e-4,
        momentum=0.55,
        verbose=verbose,
    )
    return model, codec, train, test


def evaluate_accuracy(
    administrator: BoltzmannAdministrator,
    scenarios: Sequence[Scenario],
    temperature: float = 0.72,
) -> Dict[str, Any]:
    correct = 0
    confusion: Dict[str, Dict[str, int]] = {
        expected: {pred: 0 for pred in ACTION_NAMES} for expected in ACTION_NAMES
    }
    confidences = []
    for scenario in scenarios:
        probs, _ = administrator.action_distribution(
            scenario.new_up, scenario.old_down, temperature=temperature
        )
        predicted = ACTION_NAMES[int(np.argmax(probs))]
        correct += int(predicted == scenario.action)
        confusion[scenario.action][predicted] += 1
        confidences.append(float(np.max(probs)))
    return {
        "count": len(scenarios),
        "correct": correct,
        "accuracy": correct / max(1, len(scenarios)),
        "mean_confidence": float(np.mean(confidences)),
        "confusion": confusion,
    }


def audit(
    out_dir: Path,
    seed: int = 2026,
    verbose: bool = False,
) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    model, codec, train, test = train_default_model(seed=seed, verbose=verbose)
    model_path = out_dir / "boltzmann_administrator_weights.npz"
    model.save(model_path)

    admin = BoltzmannAdministrator(model, codec=codec, seed=seed)
    accuracy = evaluate_accuracy(admin, test)

    # Persistence audit.
    loaded = JointRBM.load(model_path, seed=seed)
    loaded_admin = BoltzmannAdministrator(loaded, codec=codec, seed=seed)
    persistence_probe = test[:100]
    original_eval = evaluate_accuracy(admin, persistence_probe)
    loaded_eval = evaluate_accuracy(loaded_admin, persistence_probe)
    persistence_ok = original_eval["confusion"] == loaded_eval["confusion"]

    # Temperature diversity / concentration audit.
    probe = test[7]
    cold_probs, _ = admin.action_distribution(probe.new_up, probe.old_down, temperature=0.45)
    warm_probs, _ = admin.action_distribution(probe.new_up, probe.old_down, temperature=1.45)
    cold_entropy = float(-np.sum(cold_probs * np.log(cold_probs + 1e-12)))
    warm_entropy = float(-np.sum(warm_probs * np.log(warm_probs + 1e-12)))

    # Six-gate and mode audit.
    mode_results = {}
    for mode in BrainMode:
        scenario = test[23]
        packet = BridgePacket(
            new_up=scenario.new_up,
            old_down=scenario.old_down,
            tick=23,
            flip_phase=1,
            mode=mode,
            loop_id=f"mode-{mode.value}",
            external_output_requested=True,
        )
        result = admin.run_cycle(packet)
        mode_results[mode.value] = {
            "action": result.committed_action,
            "confidence": result.confidence,
            "external_release": result.external_release_recommended,
            "gate_order": [event.gate for event in result.gate_events],
            "gate_messages": [event.message for event in result.gate_events],
            "broadcast_rule": result.broadcast["rule"],
            "loop_exists": result.loop_exists,
        }

    # Constant loop stress: feed Gate-6 reference back down for many cycles.
    reference = tuple(0.0 for _ in range(PATHWAY_COUNT))
    stress_ok = True
    stress_actions: Dict[str, int] = {a: 0 for a in ACTION_NAMES}
    for tick in range(1200):
        scenario = test[tick % len(test)]
        packet = BridgePacket(
            new_up=scenario.new_up,
            old_down=reference,
            tick=tick,
            flip_phase=tick % 2,
            mode=BrainMode.WAKING,
            loop_id="stress",
        )
        result = admin.run_cycle(packet)
        reference = result.next_old_reference
        stress_actions[result.committed_action] += 1
        if not result.loop_exists or not np.all(np.isfinite(reference)):
            stress_ok = False
            break

    # Codec round-trip.
    roundtrip_values = (-5.5, -4.5, -1.0, 0.0, 3.5)
    encoded = codec.encode_state(roundtrip_values, tuple(-x for x in roundtrip_values))
    decoded_new, decoded_old = codec.decode_state(encoded)
    roundtrip_error = float(
        np.mean(np.abs(np.asarray(decoded_new) - np.asarray(roundtrip_values)))
    )

    # Arena comparison.
    arena_admin = BoltzmannAdministrator(loaded, codec=codec, seed=seed + 90)
    arena = GoblinAdministratorArena(arena_admin, seed=seed + 100)
    boltzmann_arena = arena.run(seeds=40, ticks=160, random_policy=False)
    random_arena = arena.run(seeds=40, ticks=160, random_policy=True)

    summary: Dict[str, Any] = {
        "engine": "One_Wave_Boltzmann_Administrator_v1_1_Multimodal",
        "memory_type": "Joint Restricted Boltzmann Machine",
        "canonical_scope": "Compressive six-line Administrator only",
        "visible_bits": codec.visible_bits,
        "state_bits": codec.state_bits,
        "hidden_units": model.n_hidden,
        "training_examples": len(train),
        "heldout_examples": len(test),
        "heldout_accuracy": accuracy["accuracy"],
        "heldout_correct": accuracy["correct"],
        "mean_confidence": accuracy["mean_confidence"],
        "persistence_ok": persistence_ok,
        "codec_roundtrip_mean_abs_error": roundtrip_error,
        "warm_entropy_greater_than_cold": warm_entropy > cold_entropy,
        "cold_entropy": cold_entropy,
        "warm_entropy": warm_entropy,
        "six_gate_order_ok": all(
            result["gate_order"] == [1, 2, 3, 4, 5, 6] for result in mode_results.values()
        ),
        "gate6_broadcast_ok": all(
            result["broadcast_rule"] == "6 tells everybody" for result in mode_results.values()
        ),
        "dream_modes_external_inhibited": (
            not mode_results[BrainMode.DAYDREAM.value]["external_release"]
            and not mode_results[BrainMode.DREAM_SLEEP.value]["external_release"]
        ),
        "constant_loop_1200_ticks_ok": stress_ok,
        "stress_action_counts": stress_actions,
        "mode_results": mode_results,
        "arena_boltzmann": asdict(boltzmann_arena),
        "arena_random": asdict(random_arena),
        "training_final_reconstruction_mse": model.training_history[-1]["reconstruction_mse"],
        "confusion": accuracy["confusion"],
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "training_history.json").write_text(
        json.dumps(model.training_history, indent=2), encoding="utf-8"
    )
    sample_result = admin.run_cycle(
        BridgePacket(
            new_up=test[0].new_up,
            old_down=test[0].old_down,
            tick=0,
            mode=BrainMode.WAKING,
            loop_id="sample",
            external_output_requested=True,
        )
    )
    (out_dir / "sample_gate_trace.json").write_text(
        json.dumps(sample_result.to_jsonable(), indent=2), encoding="utf-8"
    )

    report = f"""# One-Wave Boltzmann Administrator v1.1 Multimodal Audit

## Locked scope

This package implements the **compressive six-line Administrator** and ships an
equal-reserve multimodal Hopfield companion. It does not implement the M4 operator. It exposes a shared signed packet
so those systems can connect later without changing rulers at the bridge.

## Core architecture

- five NEW oversight pathways rise;
- five OLD/reference pathways descend simultaneously;
- all pathways use continuous `-5.5 .. +5.5` signed coordinates;
- a joint Restricted Boltzmann Machine learns state/action relationships;
- Gate 4 tells Gate 5;
- Gate 5 tells Gate 6;
- Gate 6 tells everybody and returns the next OLD reference downward;
- waking, daydream, and dream-sleep temperatures are distinct;
- external release is inhibited in daydream and dream sleep.

## Audit results

- Training examples: {len(train)}
- Held-out examples: {len(test)}
- Held-out action accuracy: {accuracy['correct']}/{len(test)} ({accuracy['accuracy']:.1%})
- Mean confidence: {accuracy['mean_confidence']:.3f}
- Visible bits: {codec.visible_bits}
- Hidden units: {model.n_hidden}
- Final reconstruction MSE: {model.training_history[-1]['reconstruction_mse']:.6f}
- Weight persistence round-trip: {persistence_ok}
- Signed codec mean absolute round-trip error: {roundtrip_error:.6f}
- Warmer temperature produced greater candidate entropy: {warm_entropy > cold_entropy}
- Six gates ran in order: {summary['six_gate_order_ok']}
- Gate 6 broadcast rule passed: {summary['gate6_broadcast_ok']}
- Daydream/dream-sleep external inhibition passed: {summary['dream_modes_external_inhibited']}
- Constant reference loop survived 1,200 cycles: {stress_ok}

## Goblin arena

| Policy | Survived | Mean final energy | Mean food | Mean bad actions | Mean Gate-6 broadcasts |
|---|---:|---:|---:|---:|---:|
| Boltzmann | {boltzmann_arena.survived_runs}/{boltzmann_arena.seeds} | {boltzmann_arena.mean_final_energy:.2f} | {boltzmann_arena.mean_food_gathered:.2f} | {boltzmann_arena.mean_bad_actions:.2f} | {boltzmann_arena.mean_gate6_broadcasts:.2f} |
| Random | {random_arena.survived_runs}/{random_arena.seeds} | {random_arena.mean_final_energy:.2f} | {random_arena.mean_food_gathered:.2f} | {random_arena.mean_bad_actions:.2f} | {random_arena.mean_gate6_broadcasts:.2f} |

## Honest boundary

The five pathway meanings in the arena are a **test adapter**, not canonical M4
semantics. M4 will eventually supply State, Scale, Caution, Drive, timing, and
routing. The RBM itself accepts generic signed pathways and does not hard-code
those meanings. The synthetic training oracle provides experience labels for
this first survival test; later runs should train from actual consequences.
"""
    (out_dir / "REPORT.md").write_text(report, encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", action="store_true", help="Train and run the full audit")
    parser.add_argument("--out", type=Path, default=Path("results"))
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.audit:
        summary = audit(args.out, seed=args.seed, verbose=args.verbose)
        print(json.dumps(summary, indent=2))
    else:
        parser.error("Use --audit for the reference build")


if __name__ == "__main__":
    main()
