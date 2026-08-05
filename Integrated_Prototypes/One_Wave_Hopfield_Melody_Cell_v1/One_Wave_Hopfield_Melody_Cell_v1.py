#!/usr/bin/env python3
"""
ONE-WAVE HOPFIELD MELODY CELL v1
================================

First strict memory brick:

    one cue tone
    -> Hopfield attractor settling
    -> full stored melody
    -> exact note/order verification

This build intentionally includes Hopfield only.
It does NOT include Boltzmann sampling, survival behavior, or route memory.

Architecture:
- A deterministic distributed bipolar code represents each pitch.
- A melody pattern contains:
    cue-tone field
    + five ordered note fields
    + ground-relative Circle-of-Fifths direction fields
- Hebbian symmetric weights store complete patterns.
- A partial cue activates one tone and leaves the melody unknown.
- Asynchronous updates settle toward a stored attractor.
- Energy, overlap, exact notes, wrong-attractor rate, and damaged-note recovery
  are measured.

The Circle of Fifths is used as the ground-reference relationship:
each note is encoded by signed movement from the melody tonic around the fifths
wheel. It is not a separate memory algorithm.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


PITCHES: Tuple[str, ...] = (
    "C", "C#", "D", "Eb", "E", "F",
    "F#", "G", "Ab", "A", "Bb", "B",
)

# Circle-of-Fifths ordering. Enharmonic spellings are normalized to this wheel.
FIFTHS: Tuple[str, ...] = (
    "C", "G", "D", "A", "E", "B",
    "F#", "Db", "Ab", "Eb", "Bb", "F",
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

DEFAULT_MELODIES: Dict[str, List[str]] = {
    # Unique cue tone in the first position for the strict one-tone test.
    "C_FIFTH_RETURN": ["C", "G", "D", "G", "C"],
    "E_FIFTH_RETURN": ["E", "B", "F#", "B", "E"],
    "F_FIFTH_RETURN": ["F", "C", "G", "C", "F"],
}

MELODY_LENGTH = 5
EMBEDDING_SIZE = 32
MAX_SWEEPS = 40


def stable_seed(label: str) -> int:
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "little", signed=False)


def deterministic_bipolar(label: str, size: int = EMBEDDING_SIZE) -> List[int]:
    rng = random.Random(stable_seed(label))
    return [1 if rng.random() >= 0.5 else -1 for _ in range(size)]


PITCH_CODE: Dict[str, List[int]] = {
    pitch: deterministic_bipolar(f"pitch:{pitch}") for pitch in PITCHES
}

# Signed fifth-distance values -6..+5, represented by distributed codes.
FIFTH_CODE: Dict[int, List[int]] = {
    displacement: deterministic_bipolar(f"fifths:{displacement}")
    for displacement in range(-6, 6)
}


def normalize_pitch(note: str) -> str:
    try:
        return NORMALIZE[note]
    except KeyError as exc:
        raise ValueError(f"Unsupported note spelling: {note!r}") from exc


def signed_fifths_displacement(tonic: str, note: str) -> int:
    """
    Return the shortest signed movement from tonic around the Circle of Fifths.

    Ground/reference is 0.
    Positive and negative values are the mirrored directions.
    For the tritone/opposite point, +6 is normalized to -6 so the range remains
    [-6, +5] with one unambiguous representation.
    """
    t = FIFTHS.index(normalize_pitch(tonic))
    n = FIFTHS.index(normalize_pitch(note))
    raw = (n - t) % 12
    return raw - 12 if raw >= 6 else raw


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def cosine_overlap(a: Sequence[float], b: Sequence[float]) -> float:
    denom = norm(a) * norm(b)
    return dot(a, b) / denom if denom else 0.0


@dataclass
class RecallResult:
    melody_name: str
    cue_tone: str
    cue_slot: int
    recalled_notes: List[str]
    expected_notes: List[str]
    exact_notes: int
    exact_sequence: bool
    attractor_name: str
    correct_attractor: bool
    sweeps: int
    converged: bool
    initial_energy: float
    final_energy: float
    energy_nonincreasing: bool
    overlap_with_expected: float
    damaged_slots: List[int]


class MelodyCodec:
    """
    Distributed representation with two nested grounds:

    1. Local pitch identity field for each note.
    2. Relational Circle-of-Fifths displacement from the melody tonic.

    Layout:
        cue pitch code
        + [pitch code, fifth-displacement code] for each melody slot
    """

    def __init__(self, melody_length: int = MELODY_LENGTH, embedding_size: int = EMBEDDING_SIZE):
        self.melody_length = melody_length
        self.embedding_size = embedding_size
        self.cue_size = embedding_size
        self.slot_size = embedding_size * 2
        self.vector_size = self.cue_size + self.melody_length * self.slot_size

    def encode(self, notes: Sequence[str]) -> List[int]:
        if len(notes) != self.melody_length:
            raise ValueError(
                f"Expected {self.melody_length} notes, received {len(notes)}"
            )
        tonic = notes[0]
        vector: List[int] = []
        vector.extend(PITCH_CODE[tonic])
        for note in notes:
            vector.extend(PITCH_CODE[note])
            vector.extend(FIFTH_CODE[signed_fifths_displacement(tonic, note)])
        return vector

    def cue_vector(
        self,
        cue_tone: str,
        cue_slot: int = 0,
        known_notes: Dict[int, str] | None = None,
    ) -> Tuple[List[int], set[int]]:
        """
        Build a partial state.

        The cue-tone field is clamped. Optional known melody slots can also be
        clamped. Unknown fields begin at 0, the active hold/reference state.
        """
        if cue_slot < 0 or cue_slot >= self.melody_length:
            raise ValueError("cue_slot outside melody")
        state = [0] * self.vector_size
        clamped: set[int] = set()

        cue_code = PITCH_CODE[cue_tone]
        state[: self.cue_size] = cue_code
        clamped.update(range(self.cue_size))

        known_notes = dict(known_notes or {})
        known_notes[cue_slot] = cue_tone
        tonic = known_notes.get(0, cue_tone if cue_slot == 0 else None)

        for slot, note in known_notes.items():
            pitch_start = self.cue_size + slot * self.slot_size
            state[pitch_start : pitch_start + self.embedding_size] = PITCH_CODE[note]
            clamped.update(range(pitch_start, pitch_start + self.embedding_size))

            if tonic is not None:
                fifth_start = pitch_start + self.embedding_size
                disp = signed_fifths_displacement(tonic, note)
                state[fifth_start : fifth_start + self.embedding_size] = FIFTH_CODE[disp]
                clamped.update(range(fifth_start, fifth_start + self.embedding_size))

        return state, clamped

    def decode_notes(self, state: Sequence[int]) -> List[str]:
        notes: List[str] = []
        for slot in range(self.melody_length):
            start = self.cue_size + slot * self.slot_size
            pitch_slice = state[start : start + self.embedding_size]
            note = max(PITCHES, key=lambda candidate: dot(pitch_slice, PITCH_CODE[candidate]))
            notes.append(note)
        return notes


class HopfieldMelodyCell:
    def __init__(self, melodies: Dict[str, Sequence[str]], seed: int = 2026):
        if not melodies:
            raise ValueError("At least one melody is required")
        self.codec = MelodyCodec()
        self.melodies = {name: list(notes) for name, notes in melodies.items()}
        self.patterns = {
            name: self.codec.encode(notes)
            for name, notes in self.melodies.items()
        }
        self.vector_size = self.codec.vector_size
        self.weights = [
            [0.0 for _ in range(self.vector_size)]
            for _ in range(self.vector_size)
        ]
        self.seed = seed
        self._train_hebbian()

    def _train_hebbian(self) -> None:
        """Classic symmetric Hebbian storage with W_ii = 0."""
        scale = 1.0 / self.vector_size
        for pattern in self.patterns.values():
            for i, si in enumerate(pattern):
                row = self.weights[i]
                for j, sj in enumerate(pattern):
                    if i != j:
                        row[j] += scale * si * sj
        for i in range(self.vector_size):
            self.weights[i][i] = 0.0

    def energy(self, state: Sequence[int]) -> float:
        total = 0.0
        for i, si in enumerate(state):
            if si == 0:
                continue
            for j, sj in enumerate(state):
                if i != j and sj != 0:
                    total += self.weights[i][j] * si * sj
        return -0.5 * total

    def settle(
        self,
        initial_state: Sequence[int],
        clamped: set[int],
        seed_label: str,
        max_sweeps: int = MAX_SWEEPS,
    ) -> Tuple[List[int], List[float], int, bool]:
        """
        Seeded asynchronous settling.

        Unknown 0 components are allowed initially. Once updated, a component
        takes -1 or +1 according to its local field. Clamped cue components are
        never changed.
        """
        state = list(initial_state)
        rng = random.Random(stable_seed(seed_label) ^ self.seed)
        energies = [self.energy(state)]

        mutable = [i for i in range(self.vector_size) if i not in clamped]
        converged = False

        for sweep in range(1, max_sweeps + 1):
            changed = 0
            rng.shuffle(mutable)
            for i in mutable:
                field = dot(self.weights[i], state)
                new_value = 1 if field >= 0 else -1
                if new_value != state[i]:
                    state[i] = new_value
                    changed += 1
            energies.append(self.energy(state))
            if changed == 0:
                converged = True
                return state, energies, sweep, converged

        return state, energies, max_sweeps, converged

    def closest_attractor(self, state: Sequence[int]) -> Tuple[str, float]:
        name = max(
            self.patterns,
            key=lambda candidate: cosine_overlap(state, self.patterns[candidate]),
        )
        return name, cosine_overlap(state, self.patterns[name])

    def recall(
        self,
        expected_name: str,
        cue_tone: str,
        cue_slot: int = 0,
        known_notes: Dict[int, str] | None = None,
        damaged_slots: Sequence[int] | None = None,
    ) -> RecallResult:
        expected = self.melodies[expected_name]
        known_notes = dict(known_notes or {})

        # Damaged slots are deliberately removed from the cue.
        for slot in damaged_slots or []:
            known_notes.pop(slot, None)

        initial, clamped = self.codec.cue_vector(
            cue_tone=cue_tone,
            cue_slot=cue_slot,
            known_notes=known_notes,
        )
        settled, energies, sweeps, converged = self.settle(
            initial,
            clamped,
            seed_label=f"{expected_name}:{cue_tone}:{cue_slot}:{sorted(known_notes.items())}",
        )
        recalled = self.codec.decode_notes(settled)
        attractor_name, _ = self.closest_attractor(settled)
        exact_notes = sum(a == b for a, b in zip(recalled, expected))
        nonincreasing = all(
            later <= earlier + 1e-9
            for earlier, later in zip(energies, energies[1:])
        )

        return RecallResult(
            melody_name=expected_name,
            cue_tone=cue_tone,
            cue_slot=cue_slot,
            recalled_notes=recalled,
            expected_notes=expected,
            exact_notes=exact_notes,
            exact_sequence=recalled == expected,
            attractor_name=attractor_name,
            correct_attractor=attractor_name == expected_name,
            sweeps=sweeps,
            converged=converged,
            initial_energy=energies[0],
            final_energy=energies[-1],
            energy_nonincreasing=nonincreasing,
            overlap_with_expected=cosine_overlap(settled, self.patterns[expected_name]),
            damaged_slots=list(damaged_slots or []),
        )


def run_audit(
    melodies: Dict[str, Sequence[str]],
    out_dir: Path,
    seed: int = 2026,
) -> Dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cell = HopfieldMelodyCell(melodies, seed=seed)
    trials: List[RecallResult] = []

    # Test A: one cue tone reconstructs the complete melody.
    for name, notes in melodies.items():
        trials.append(
            cell.recall(
                expected_name=name,
                cue_tone=notes[0],
                cue_slot=0,
                known_notes={},
                damaged_slots=[1, 2, 3, 4],
            )
        )

    # Test B: middle-note damage. First and last notes remain as partial context.
    for name, notes in melodies.items():
        trials.append(
            cell.recall(
                expected_name=name,
                cue_tone=notes[0],
                cue_slot=0,
                known_notes={4: notes[4]},
                damaged_slots=[2],
            )
        )

    # Test C: two internal notes removed.
    for name, notes in melodies.items():
        trials.append(
            cell.recall(
                expected_name=name,
                cue_tone=notes[0],
                cue_slot=0,
                known_notes={3: notes[3], 4: notes[4]},
                damaged_slots=[1, 2],
            )
        )

    exact_sequences = sum(t.exact_sequence for t in trials)
    correct_attractors = sum(t.correct_attractor for t in trials)
    energy_valid = sum(t.energy_nonincreasing for t in trials)

    summary = {
        "engine": "One_Wave_Hopfield_Melody_Cell_v1",
        "memory_type": "Hopfield only",
        "melodies_stored": len(melodies),
        "trials": len(trials),
        "exact_sequence_recall": exact_sequences,
        "exact_sequence_rate": exact_sequences / len(trials),
        "correct_attractor_recall": correct_attractors,
        "correct_attractor_rate": correct_attractors / len(trials),
        "wrong_attractor_count": len(trials) - correct_attractors,
        "energy_nonincreasing_trials": energy_valid,
        "energy_nonincreasing_rate": energy_valid / len(trials),
        "mean_sweeps": sum(t.sweeps for t in trials) / len(trials),
        "vector_size": cell.vector_size,
        "stored_patterns": list(melodies),
    }

    with (out_dir / "trials.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(trials[0]).keys()))
        writer.writeheader()
        for trial in trials:
            row = asdict(trial)
            for key in ("recalled_notes", "expected_notes", "damaged_slots"):
                row[key] = json.dumps(row[key])
            writer.writerow(row)

    with (out_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    report = [
        "# One-Wave Hopfield Melody Cell v1",
        "",
        "## Purpose",
        "",
        "Test whether one cue tone can settle a Hopfield memory cell into the full",
        "stored melody attractor. This build contains no Boltzmann system.",
        "",
        "## Results",
        "",
        f"- Stored melodies: {summary['melodies_stored']}",
        f"- Audit trials: {summary['trials']}",
        f"- Exact melody recall: {summary['exact_sequence_recall']}/{summary['trials']} "
        f"({summary['exact_sequence_rate']:.1%})",
        f"- Correct attractor: {summary['correct_attractor_recall']}/{summary['trials']} "
        f"({summary['correct_attractor_rate']:.1%})",
        f"- Wrong attractors: {summary['wrong_attractor_count']}",
        f"- Energy non-increasing: {summary['energy_nonincreasing_trials']}/{summary['trials']}",
        f"- Mean settling sweeps: {summary['mean_sweeps']:.2f}",
        "",
        "## Stored melodies",
        "",
    ]
    for name, notes in melodies.items():
        report.append(f"- `{name}`: {' → '.join(notes)}")
    report.extend([
        "",
        "## What this proves",
        "",
        "It proves only the first brick: deterministic associative recall of short",
        "stored musical patterns from a partial tone cue in this controlled test.",
        "It does not yet prove long-song recall, audio recognition, biological memory,",
        "or autonomous goblin behavior.",
        "",
    ])
    (out_dir / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    return summary


def load_melodies(path: Path | None) -> Dict[str, List[str]]:
    if path is None:
        return {name: list(notes) for name, notes in DEFAULT_MELODIES.items()}
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, dict):
        raise ValueError("Melody JSON must be an object mapping names to note lists")
    melodies: Dict[str, List[str]] = {}
    for name, notes in raw.items():
        if not isinstance(name, str) or not isinstance(notes, list):
            raise ValueError("Each melody must map a string name to a note list")
        if len(notes) != MELODY_LENGTH:
            raise ValueError(f"{name}: expected exactly {MELODY_LENGTH} notes")
        for note in notes:
            if note not in PITCHES:
                raise ValueError(f"{name}: unsupported note {note!r}")
        melodies[name] = notes
    return melodies


def main() -> None:
    parser = argparse.ArgumentParser(
        description="One tone cues a complete melody through Hopfield recall."
    )
    parser.add_argument(
        "--melodies",
        type=Path,
        default=None,
        help="Optional JSON mapping melody names to five-note note lists.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("hopfield_melody_results"),
        help="Output directory.",
    )
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    melodies = load_melodies(args.melodies)
    summary = run_audit(melodies, args.out, seed=args.seed)

    print("=" * 72)
    print("ONE-WAVE HOPFIELD MELODY CELL v1")
    print("=" * 72)
    print(f"Stored melodies:       {summary['melodies_stored']}")
    print(f"Audit trials:          {summary['trials']}")
    print(
        f"Exact melody recall:   {summary['exact_sequence_recall']}/"
        f"{summary['trials']} ({summary['exact_sequence_rate']:.1%})"
    )
    print(
        f"Correct attractor:     {summary['correct_attractor_recall']}/"
        f"{summary['trials']} ({summary['correct_attractor_rate']:.1%})"
    )
    print(f"Wrong attractors:      {summary['wrong_attractor_count']}")
    print(
        f"Energy non-increasing: {summary['energy_nonincreasing_trials']}/"
        f"{summary['trials']}"
    )
    print(f"Mean settling sweeps:  {summary['mean_sweeps']:.2f}")
    print(f"Results:               {args.out}")
    print("=" * 72)


if __name__ == "__main__":
    main()
