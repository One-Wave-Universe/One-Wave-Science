#!/usr/bin/env python3
"""
ONE-WAVE HOPFIELD BRAIN v2.1 FINAL
===================================

Hopfield-only associative musical memory architecture.

This program completes the first Hopfield brain layer by adding:
- overlapping melodies and ambiguous single-tone cues;
- rhythm and ordered temporal positions;
- two grounds: local note center and relational melody ground;
- explicit five-state and six-direction representations;
- asynchronous energy-descending recall;
- exact recall, overlap, false-attractor, ambiguity, and capacity audits;
- forgetting / replacement;
- persistence to and from JSON;
- direct pattern damage and weight-matrix damage;
- an autonomous playback agent that acts from reconstructed memory.

It intentionally does NOT contain Boltzmann sampling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple, Optional, Iterable, Any


# ---------------------------------------------------------------------------
# Canonical musical state
# ---------------------------------------------------------------------------
PITCHES: Tuple[str, ...] = (
    "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"
)
FIFTHS: Tuple[str, ...] = (
    "C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"
)
NORMALIZE = {
    "C": "C", "B#": "C",
    "C#": "Db", "Db": "Db",
    "D": "D",
    "D#": "Eb", "Eb": "Eb",
    "E": "E", "Fb": "E",
    "F": "F", "E#": "F",
    "F#": "F#", "Gb": "F#",
    "G": "G",
    "G#": "Ab", "Ab": "Ab",
    "A": "A",
    "A#": "Bb", "Bb": "Bb",
    "B": "B", "Cb": "B",
}

# Five states remain separate from six directions.
FIVE_STATES: Tuple[str, ...] = ("BEGIN", "BUILD", "HOLD", "BREAK", "STABLE")
SIX_DIRECTIONS: Tuple[int, ...] = (-3, -2, -1, 1, 2, 3)
RHYTHMS: Tuple[float, ...] = (0.25, 0.5, 1.0, 1.5, 2.0)

EMBED = 16
MELODY_LENGTH = 8
MAX_SWEEPS = 60
DEFAULT_SEED = 2026


DEFAULT_SONGS: Dict[str, Dict[str, Any]] = {
    # Deliberately overlapping notes and cue tones.
    "RETURN_HOME": {
        "notes":   ["C", "G", "D", "G", "C", "E", "D", "C"],
        "rhythm":  [1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 2.0],
        "states":  ["BEGIN", "BUILD", "BUILD", "HOLD", "BREAK", "BUILD", "HOLD", "STABLE"],
    },
    "FALL_AND_RISE": {
        "notes":   ["C", "E", "G", "E", "D", "F", "G", "C"],
        "rhythm":  [1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 2.0],
        "states":  ["BEGIN", "BUILD", "HOLD", "BUILD", "BREAK", "BUILD", "HOLD", "STABLE"],
    },
    "MIRROR_WALK": {
        "notes":   ["E", "B", "F#", "B", "E", "G", "F#", "E"],
        "rhythm":  [1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 2.0],
        "states":  ["BEGIN", "BUILD", "BUILD", "HOLD", "BREAK", "BUILD", "HOLD", "STABLE"],
    },
    "FIFTHS_ARC": {
        "notes":   ["F", "C", "G", "D", "G", "C", "F", "C"],
        "rhythm":  [0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 1.0, 2.0],
        "states":  ["BEGIN", "BUILD", "HOLD", "BUILD", "BREAK", "BUILD", "HOLD", "STABLE"],
    },
    "COMMON_CUE_A": {
        "notes":   ["G", "D", "E", "C", "G", "A", "D", "G"],
        "rhythm":  [1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 2.0],
        "states":  ["BEGIN", "BUILD", "HOLD", "BUILD", "BREAK", "BUILD", "HOLD", "STABLE"],
    },
    "COMMON_CUE_B": {
        "notes":   ["G", "B", "D", "F", "E", "C", "D", "G"],
        "rhythm":  [1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 2.0],
        "states":  ["BEGIN", "BUILD", "HOLD", "BUILD", "BREAK", "BUILD", "HOLD", "STABLE"],
    },
}


def stable_seed(label: str) -> int:
    return int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest()[:8], "little")


def bipolar_code(label: str, size: int = EMBED) -> List[int]:
    rng = random.Random(stable_seed(label))
    return [1 if rng.random() >= 0.5 else -1 for _ in range(size)]


PITCH_CODE = {p: bipolar_code(f"pitch:{p}") for p in PITCHES}
RHYTHM_CODE = {r: bipolar_code(f"rhythm:{r}") for r in RHYTHMS}
STATE_CODE = {s: bipolar_code(f"state:{s}") for s in FIVE_STATES}
DIR_CODE = {d: bipolar_code(f"direction:{d}") for d in SIX_DIRECTIONS}
GROUND_CODE = {d: bipolar_code(f"ground:{d}") for d in range(-6, 6)}


def normalize_note(note: str) -> str:
    if note not in NORMALIZE:
        raise ValueError(f"Unsupported note: {note}")
    # PITCH_CODE uses C# rather than Db for pitch identity.
    normalized = NORMALIZE[note]
    return "C#" if normalized == "Db" else normalized


def fifth_name(note: str) -> str:
    return NORMALIZE[note]


def signed_fifths(tonic: str, note: str) -> int:
    ti = FIFTHS.index(fifth_name(tonic))
    ni = FIFTHS.index(fifth_name(note))
    raw = (ni - ti) % 12
    return raw - 12 if raw >= 6 else raw


def six_direction(displacement: int) -> int:
    """
    Compress signed fifth displacement to one of six mirrored directions.
    Ground 0 is reference, not counted as a direction.
    """
    if displacement == 0:
        return 1  # stable forward reference channel; ground is encoded separately.
    mag = min(3, abs(displacement))
    return mag if displacement > 0 else -mag


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def overlap(a: Sequence[float], b: Sequence[float]) -> float:
    den = norm(a) * norm(b)
    return dot(a, b) / den if den else 0.0


@dataclass
class Song:
    name: str
    notes: List[str]
    rhythm: List[float]
    states: List[str]

    def validate(self) -> None:
        if not (len(self.notes) == len(self.rhythm) == len(self.states) == MELODY_LENGTH):
            raise ValueError(f"{self.name}: every song must have {MELODY_LENGTH} slots")
        for note in self.notes:
            normalize_note(note)
        for r in self.rhythm:
            if r not in RHYTHMS:
                raise ValueError(f"{self.name}: unsupported rhythm {r}")
        for state in self.states:
            if state not in FIVE_STATES:
                raise ValueError(f"{self.name}: unsupported state {state}")


@dataclass
class Recall:
    expected: str
    cue_description: str
    decoded_song: str
    correct_attractor: bool
    exact_notes: int
    exact_rhythm: int
    exact_states: int
    raw_full_exact: bool
    committed_full_exact: bool
    committed_notes: List[str]
    committed_rhythm: List[float]
    committed_states: List[str]
    sweeps: int
    converged: bool
    initial_energy: float
    final_energy: float
    energy_nonincreasing: bool
    expected_overlap: float
    false_attractor: bool


class HarmonicCodec:
    """
    Two-ground, five-state, six-direction pattern encoder.

    Local ground:
        distributed identity of each individual note.

    Relational ground:
        signed Circle-of-Fifths displacement from the song tonic.

    Per slot:
        note identity
        rhythm
        five-state condition
        six-direction orientation
        signed ground displacement
    """

    def __init__(self):
        self.slot_fields = 5
        self.slot_size = EMBED * self.slot_fields
        self.cue_size = EMBED
        self.vector_size = self.cue_size + MELODY_LENGTH * self.slot_size

    def encode(self, song: Song) -> List[int]:
        tonic = song.notes[0]
        vec: List[int] = []
        vec.extend(PITCH_CODE[normalize_note(tonic)])
        for note, rhythm, state in zip(song.notes, song.rhythm, song.states):
            disp = signed_fifths(tonic, note)
            vec.extend(PITCH_CODE[normalize_note(note)])
            vec.extend(RHYTHM_CODE[rhythm])
            vec.extend(STATE_CODE[state])
            vec.extend(DIR_CODE[six_direction(disp)])
            vec.extend(GROUND_CODE[disp])
        return vec

    def partial(
        self,
        cue_note: str,
        known_slots: Dict[int, Tuple[str, float, str]],
    ) -> Tuple[List[int], set[int]]:
        state = [0] * self.vector_size
        clamped: set[int] = set()

        state[:EMBED] = PITCH_CODE[normalize_note(cue_note)]
        clamped.update(range(EMBED))

        tonic = known_slots.get(0, (cue_note, 1.0, "BEGIN"))[0]
        for slot, (note, rhythm, phase) in known_slots.items():
            start = EMBED + slot * self.slot_size
            disp = signed_fifths(tonic, note)
            fields = (
                PITCH_CODE[normalize_note(note)],
                RHYTHM_CODE[rhythm],
                STATE_CODE[phase],
                DIR_CODE[six_direction(disp)],
                GROUND_CODE[disp],
            )
            for field_idx, code in enumerate(fields):
                fstart = start + field_idx * EMBED
                state[fstart:fstart + EMBED] = code
                clamped.update(range(fstart, fstart + EMBED))
        return state, clamped

    def _decode_field(self, values: Sequence[int], mapping: Dict[Any, List[int]]) -> Any:
        return max(mapping, key=lambda k: dot(values, mapping[k]))

    def decode(self, state: Sequence[int], name: str = "RECALLED") -> Song:
        notes, rhythm, states = [], [], []
        for slot in range(MELODY_LENGTH):
            start = EMBED + slot * self.slot_size
            notes.append(self._decode_field(state[start:start+EMBED], PITCH_CODE))
            rhythm.append(self._decode_field(state[start+EMBED:start+2*EMBED], RHYTHM_CODE))
            states.append(self._decode_field(state[start+2*EMBED:start+3*EMBED], STATE_CODE))
        return Song(name=name, notes=notes, rhythm=rhythm, states=states)


class HopfieldBrain:
    def __init__(self, songs: Iterable[Song], seed: int = DEFAULT_SEED):
        self.codec = HarmonicCodec()
        self.seed = seed
        self.songs: Dict[str, Song] = {}
        self.patterns: Dict[str, List[int]] = {}
        self.weights: List[List[float]] = []
        for song in songs:
            self.add_song(song, retrain=False)
        self.retrain()

    def add_song(self, song: Song, retrain: bool = True) -> None:
        song.validate()
        self.songs[song.name] = song
        self.patterns[song.name] = self.codec.encode(song)
        if retrain:
            self.retrain()

    def forget_song(self, name: str) -> None:
        if name not in self.songs:
            raise KeyError(name)
        del self.songs[name]
        del self.patterns[name]
        self.retrain()

    def retrain(self) -> None:
        n = self.codec.vector_size
        self.weights = [[0.0] * n for _ in range(n)]
        if not self.patterns:
            return
        scale = 1.0 / n
        for pattern in self.patterns.values():
            for i, si in enumerate(pattern):
                row = self.weights[i]
                for j, sj in enumerate(pattern):
                    if i != j:
                        row[j] += scale * si * sj
        for i in range(n):
            self.weights[i][i] = 0.0

    def energy(self, state: Sequence[int]) -> float:
        total = 0.0
        for i, si in enumerate(state):
            if si == 0:
                continue
            total += si * dot(self.weights[i], state)
        return -0.5 * total

    def settle(
        self,
        initial: Sequence[int],
        clamped: set[int],
        label: str,
        max_sweeps: int = MAX_SWEEPS,
    ) -> Tuple[List[int], List[float], int, bool]:
        state = list(initial)
        mutable = [i for i in range(len(state)) if i not in clamped]
        rng = random.Random(stable_seed(label) ^ self.seed)
        energies = [self.energy(state)]

        for sweep in range(1, max_sweeps + 1):
            changed = 0
            rng.shuffle(mutable)
            for i in mutable:
                h = dot(self.weights[i], state)
                new = 1 if h >= 0 else -1
                if new != state[i]:
                    state[i] = new
                    changed += 1
            energies.append(self.energy(state))
            if changed == 0:
                return state, energies, sweep, True
        return state, energies, max_sweeps, False

    def closest(self, state: Sequence[int]) -> Tuple[str, float]:
        if not self.patterns:
            return "NONE", 0.0
        name = max(self.patterns, key=lambda n: overlap(state, self.patterns[n]))
        return name, overlap(state, self.patterns[name])

    def recall(
        self,
        expected_name: str,
        cue_note: str,
        known_slots: Dict[int, Tuple[str, float, str]],
        cue_description: str,
    ) -> Recall:
        initial, clamped = self.codec.partial(cue_note, known_slots)
        settled, energies, sweeps, converged = self.settle(
            initial, clamped, f"{expected_name}|{cue_description}"
        )
        decoded_name, expected_overlap = self.closest(settled)
        decoded = self.codec.decode(settled, decoded_name)
        expected = self.songs[expected_name]
        exact_notes = sum(a == b for a, b in zip(decoded.notes, expected.notes))
        exact_rhythm = sum(a == b for a, b in zip(decoded.rhythm, expected.rhythm))
        exact_states = sum(a == b for a, b in zip(decoded.states, expected.states))
        noninc = all(b <= a + 1e-9 for a, b in zip(energies, energies[1:]))
        raw_full_exact = (
            exact_notes == MELODY_LENGTH
            and exact_rhythm == MELODY_LENGTH
            and exact_states == MELODY_LENGTH
        )
        correct = decoded_name == expected_name

        # Hopfield recall has two layers:
        # 1. raw settled state, useful for measuring noise and interference;
        # 2. committed attractor, the exact stored pattern selected by the basin.
        #
        # We report both. The committed output is not counted as raw exact recall.
        committed = self.songs[decoded_name]
        committed_full_exact = (
            committed.notes == expected.notes
            and committed.rhythm == expected.rhythm
            and committed.states == expected.states
        )

        return Recall(
            expected=expected_name,
            cue_description=cue_description,
            decoded_song=decoded_name,
            correct_attractor=correct,
            exact_notes=exact_notes,
            exact_rhythm=exact_rhythm,
            exact_states=exact_states,
            raw_full_exact=raw_full_exact,
            committed_full_exact=committed_full_exact,
            committed_notes=list(committed.notes),
            committed_rhythm=list(committed.rhythm),
            committed_states=list(committed.states),
            sweeps=sweeps,
            converged=converged,
            initial_energy=energies[0],
            final_energy=energies[-1],
            energy_nonincreasing=noninc,
            expected_overlap=expected_overlap,
            false_attractor=not correct,
        )

    def damage_weights(self, fraction: float, seed: int) -> List[Tuple[int, int, float]]:
        """
        Zero a symmetric fraction of upper-triangle weights.
        Returns a patch that can restore the exact matrix.
        """
        if not 0.0 <= fraction <= 1.0:
            raise ValueError("fraction must be 0..1")
        rng = random.Random(seed)
        n = len(self.weights)
        candidates = [(i, j) for i in range(n) for j in range(i+1, n)]
        rng.shuffle(candidates)
        count = int(len(candidates) * fraction)
        patch = []
        for i, j in candidates[:count]:
            old = self.weights[i][j]
            patch.append((i, j, old))
            self.weights[i][j] = 0.0
            self.weights[j][i] = 0.0
        return patch

    def restore_weight_patch(self, patch: Sequence[Tuple[int, int, float]]) -> None:
        for i, j, value in patch:
            self.weights[i][j] = value
            self.weights[j][i] = value

    def save(self, path: Path) -> None:
        payload = {
            "version": "2.1",
            "seed": self.seed,
            "songs": {
                name: {"notes": s.notes, "rhythm": s.rhythm, "states": s.states}
                for name, s in self.songs.items()
            },
            "weights": self.weights,
        }
        path.write_text(json.dumps(payload), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "HopfieldBrain":
        payload = json.loads(path.read_text(encoding="utf-8"))
        songs = [
            Song(name, data["notes"], data["rhythm"], data["states"])
            for name, data in payload["songs"].items()
        ]
        brain = cls(songs, seed=int(payload["seed"]))
        brain.weights = payload["weights"]
        return brain


class AutonomousPlaybackCell:
    """Small observer-shell agent that acts from a reconstructed attractor."""

    def __init__(self, brain: HopfieldBrain):
        self.brain = brain
        self.play_log: List[Dict[str, Any]] = []

    def cue_and_play(
        self,
        expected_name: str,
        cue_note: str,
        known_slots: Dict[int, Tuple[str, float, str]],
        label: str,
    ) -> Recall:
        result = self.brain.recall(expected_name, cue_note, known_slots, label)
        song = self.brain.songs[result.decoded_song]
        self.play_log = [
            {
                "step": i,
                "note": note,
                "duration": duration,
                "state": state,
            }
            for i, (note, duration, state) in enumerate(
                zip(song.notes, song.rhythm, song.states)
            )
        ]
        return result


def make_songs(raw: Dict[str, Dict[str, Any]]) -> List[Song]:
    return [
        Song(name, list(data["notes"]), list(data["rhythm"]), list(data["states"]))
        for name, data in raw.items()
    ]


def synthetic_song(index: int) -> Song:
    rng = random.Random(9000 + index)
    tonic = PITCHES[index % len(PITCHES)]
    notes = [tonic] + [rng.choice(PITCHES) for _ in range(MELODY_LENGTH - 2)] + [tonic]
    rhythm = [rng.choice(RHYTHMS) for _ in range(MELODY_LENGTH)]
    states = [
        "BEGIN", "BUILD", "HOLD", "BUILD",
        "BREAK", "BUILD", "HOLD", "STABLE",
    ]
    return Song(f"SYNTH_{index:02d}", notes, rhythm, states)


def run_complete_audit(out_dir: Path, seed: int = DEFAULT_SEED) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    songs = make_songs(DEFAULT_SONGS)
    brain = HopfieldBrain(songs, seed=seed)
    agent = AutonomousPlaybackCell(brain)
    recalls: List[Recall] = []

    # A. Unique or mostly unique one-tone cue.
    for name in ("MIRROR_WALK", "FIFTHS_ARC"):
        s = brain.songs[name]
        recalls.append(agent.cue_and_play(
            name, s.notes[0], {0: (s.notes[0], s.rhythm[0], s.states[0])},
            "single-tone cue"
        ))

    # B. Shared G cue: one tone alone is deliberately ambiguous.
    for name in ("COMMON_CUE_A", "COMMON_CUE_B"):
        s = brain.songs[name]
        recalls.append(agent.cue_and_play(
            name, "G", {0: ("G", s.rhythm[0], s.states[0])},
            "ambiguous shared-G cue"
        ))

    # C. Shared cue plus one context slot should select the right song.
    for name in ("COMMON_CUE_A", "COMMON_CUE_B"):
        s = brain.songs[name]
        recalls.append(agent.cue_and_play(
            name,
            "G",
            {
                0: ("G", s.rhythm[0], s.states[0]),
                1: (s.notes[1], s.rhythm[1], s.states[1]),
            },
            "shared-G plus slot-1 context"
        ))

    # D. Missing internal melody fields.
    for name, s in brain.songs.items():
        recalls.append(agent.cue_and_play(
            name,
            s.notes[0],
            {
                0: (s.notes[0], s.rhythm[0], s.states[0]),
                4: (s.notes[4], s.rhythm[4], s.states[4]),
                7: (s.notes[7], s.rhythm[7], s.states[7]),
            },
            "three-anchor damaged pattern"
        ))

    # E. Persistence.
    memory_path = out_dir / "brain_memory.json"
    brain.save(memory_path)
    reloaded = HopfieldBrain.load(memory_path)
    persistence_ok = all(
        reloaded.patterns[name] == brain.patterns[name] for name in brain.patterns
    ) and all(
        reloaded.weights[i][j] == brain.weights[i][j]
        for i in range(len(brain.weights))
        for j in range(len(brain.weights))
    )

    # F. Forgetting.
    forgotten = "FIFTHS_ARC"
    pre_forget_count = len(brain.songs)
    brain.forget_song(forgotten)
    forgetting_ok = forgotten not in brain.songs and len(brain.songs) == pre_forget_count - 1
    brain.add_song(next(s for s in songs if s.name == forgotten))

    # G. Weight-damage recovery.
    damage_levels = (0.01, 0.03, 0.05, 0.10)
    weight_damage = []
    for frac in damage_levels:
        patch = brain.damage_weights(frac, seed=stable_seed(f"damage:{frac}"))
        test_song = brain.songs["RETURN_HOME"]
        result = brain.recall(
            "RETURN_HOME",
            test_song.notes[0],
            {
                0: (test_song.notes[0], test_song.rhythm[0], test_song.states[0]),
                4: (test_song.notes[4], test_song.rhythm[4], test_song.states[4]),
            },
            f"{frac:.0%} symmetric weight damage"
        )
        weight_damage.append({
            "fraction": frac,
            "correct_attractor": result.correct_attractor,
            "raw_full_exact": result.raw_full_exact,
            "committed_full_exact": result.committed_full_exact,
            "exact_notes": result.exact_notes,
            "expected_overlap": result.expected_overlap,
        })
        brain.restore_weight_patch(patch)

    # H. Capacity sweep. Same architecture, increasing number of synthetic patterns.
    capacity = []
    for count in (2, 4, 6, 8, 10, 12):
        synth = [synthetic_song(i) for i in range(count)]
        cap_brain = HopfieldBrain(synth, seed=seed)
        correct = 0
        exact = 0
        false = 0
        for song in synth:
            result = cap_brain.recall(
                song.name,
                song.notes[0],
                {
                    0: (song.notes[0], song.rhythm[0], song.states[0]),
                    3: (song.notes[3], song.rhythm[3], song.states[3]),
                    7: (song.notes[7], song.rhythm[7], song.states[7]),
                },
                f"capacity-{count}"
            )
            correct += int(result.correct_attractor)
            exact += int(result.raw_full_exact)
            false += int(result.false_attractor)
        capacity.append({
            "stored_patterns": count,
            "correct_attractors": correct,
            "exact_patterns": exact,
            "false_attractors": false,
            "correct_rate": correct / count,
            "exact_rate": exact / count,
        })

    ambiguous = [r for r in recalls if r.cue_description == "ambiguous shared-G cue"]
    contextual = [r for r in recalls if r.cue_description == "shared-G plus slot-1 context"]
    damaged = [r for r in recalls if r.cue_description == "three-anchor damaged pattern"]

    summary = {
        "engine": "One_Wave_Hopfield_Brain_v2_1_Final",
        "memory_type": "Hopfield only",
        "songs_stored": len(DEFAULT_SONGS),
        "vector_size": brain.codec.vector_size,
        "recall_trials": len(recalls),
        "correct_attractors": sum(r.correct_attractor for r in recalls),
        "raw_full_exact_patterns": sum(r.raw_full_exact for r in recalls),
        "committed_full_exact_patterns": sum(r.committed_full_exact for r in recalls),
        "false_attractors": sum(r.false_attractor for r in recalls),
        "energy_nonincreasing_trials": sum(r.energy_nonincreasing for r in recalls),
        "ambiguous_single_tone_correct": sum(r.correct_attractor for r in ambiguous),
        "ambiguous_single_tone_trials": len(ambiguous),
        "context_resolved_correct": sum(r.correct_attractor for r in contextual),
        "context_resolved_trials": len(contextual),
        "damaged_pattern_correct": sum(r.correct_attractor for r in damaged),
        "damaged_pattern_trials": len(damaged),
        "persistence_ok": persistence_ok,
        "forgetting_ok": forgetting_ok,
        "weight_damage": weight_damage,
        "capacity_sweep": capacity,
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "recall_trials.json").write_text(
        json.dumps([asdict(r) for r in recalls], indent=2), encoding="utf-8"
    )
    (out_dir / "playback_log.json").write_text(
        json.dumps(agent.play_log, indent=2), encoding="utf-8"
    )

    report = [
        "# One-Wave Hopfield Brain v2 Complete Audit",
        "",
        "## Scope",
        "",
        "Hopfield-only musical associative memory. No Boltzmann system is included.",
        "",
        "## Core results",
        "",
        f"- Stored songs: {summary['songs_stored']}",
        f"- Pattern vector size: {summary['vector_size']}",
        f"- Recall trials: {summary['recall_trials']}",
        f"- Correct attractors: {summary['correct_attractors']}/{summary['recall_trials']}",
        f"- Raw fully exact note/rhythm/state patterns: {summary['raw_full_exact_patterns']}/{summary['recall_trials']}",
        f"- Committed exact stored patterns: {summary['committed_full_exact_patterns']}/{summary['recall_trials']}",
        f"- False attractors: {summary['false_attractors']}",
        f"- Energy non-increasing: {summary['energy_nonincreasing_trials']}/{summary['recall_trials']}",
        "",
        "## Ambiguity",
        "",
        f"- Shared one-tone cue correct: {summary['ambiguous_single_tone_correct']}/{summary['ambiguous_single_tone_trials']}",
        f"- Same cue plus one context slot correct: {summary['context_resolved_correct']}/{summary['context_resolved_trials']}",
        "",
        "A shared single tone is inherently ambiguous when multiple stored songs use it.",
        "The audit therefore reports ambiguity rather than pretending one note uniquely identifies",
        "every song. One additional contextual slot is tested as the disambiguating cue.",
        "",
        "## Damage and persistence",
        "",
        f"- Damaged-pattern recall: {summary['damaged_pattern_correct']}/{summary['damaged_pattern_trials']}",
        f"- Persistence round-trip: {summary['persistence_ok']}",
        f"- Forget/retrain test: {summary['forgetting_ok']}",
        "",
        "### Symmetric weight damage",
        "",
        "| Weight loss | Correct attractor | Full exact | Exact notes | Overlap |",
        "|---:|:---:|:---:|---:|---:|",
    ]
    for row in weight_damage:
        report.append(
            f"| {row['fraction']:.0%} | {row['correct_attractor']} | {row['raw_full_exact']} | "
            f"{row['exact_notes']}/{MELODY_LENGTH} | {row['expected_overlap']:.3f} |"
        )
    report.extend([
        "",
        "## Capacity sweep",
        "",
        "| Patterns | Correct attractors | Exact patterns | False attractors |",
        "|---:|---:|---:|---:|",
    ])
    for row in capacity:
        report.append(
            f"| {row['stored_patterns']} | {row['correct_attractors']} | "
            f"{row['exact_patterns']} | {row['false_attractors']} |"
        )
    report.extend([
        "",
        "## Architecture included",
        "",
        "- local pitch ground;",
        "- relational Circle-of-Fifths ground;",
        "- five states kept separate from six mirrored directions;",
        "- note, rhythm, state, direction, and ground-displacement fields;",
        "- symmetric Hebbian weights with zero diagonal;",
        "- seeded asynchronous settling;",
        "- Hopfield energy audit;",
        "- false-attractor reporting;",
        "- forgetting and persistence;",
        "- weight-matrix damage;",
        "- autonomous playback from the recalled attractor.",
        "",
        "## Deliberate boundary",
        "",
        "This completes the Hopfield-only architecture layer. It does not claim arbitrary",
        "audio recognition, unlimited song capacity, biological equivalence, or a",
        "Boltzmann reconstruction layer.",
    ])
    (out_dir / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    return summary


def load_song_file(path: Optional[Path]) -> List[Song]:
    raw = DEFAULT_SONGS if path is None else json.loads(path.read_text(encoding="utf-8"))
    return make_songs(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description="One-Wave Hopfield musical memory brain")
    parser.add_argument("--out", type=Path, default=Path("hopfield_brain_v2_results"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--songs", type=Path, default=None)
    parser.add_argument("--audit", action="store_true", help="Run complete architecture audit")
    args = parser.parse_args()

    if args.songs is not None:
        songs = load_song_file(args.songs)
        brain = HopfieldBrain(songs, seed=args.seed)
        brain.save(args.out / "brain_memory.json")
        print(f"Stored {len(songs)} songs in {args.out / 'brain_memory.json'}")
        return

    summary = run_complete_audit(args.out, seed=args.seed)
    print("=" * 78)
    print("ONE-WAVE HOPFIELD BRAIN v2.1 FINAL")
    print("=" * 78)
    print(f"Stored songs:                {summary['songs_stored']}")
    print(f"Recall trials:               {summary['recall_trials']}")
    print(f"Correct attractors:          {summary['correct_attractors']}/{summary['recall_trials']}")
    print(f"Raw fully exact patterns:       {summary['raw_full_exact_patterns']}/{summary['recall_trials']}")
    print(f"Committed exact patterns:       {summary['committed_full_exact_patterns']}/{summary['recall_trials']}")
    print(f"False attractors:               {summary['false_attractors']}")
    print(f"Energy non-increasing:       {summary['energy_nonincreasing_trials']}/{summary['recall_trials']}")
    print(
        f"Ambiguous one-tone correct:  "
        f"{summary['ambiguous_single_tone_correct']}/{summary['ambiguous_single_tone_trials']}"
    )
    print(
        f"Context-resolved correct:    "
        f"{summary['context_resolved_correct']}/{summary['context_resolved_trials']}"
    )
    print(
        f"Damaged-pattern correct:     "
        f"{summary['damaged_pattern_correct']}/{summary['damaged_pattern_trials']}"
    )
    print(f"Persistence:                 {summary['persistence_ok']}")
    print(f"Forgetting:                  {summary['forgetting_ok']}")
    print(f"Results:                     {args.out}")
    print("=" * 78)


if __name__ == "__main__":
    main()
