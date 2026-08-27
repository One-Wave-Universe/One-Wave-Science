"""Receipt-rebuildable verbal command memory for the M4 CPU reference.

This module is deliberately upstream of speech recognition and downstream of
no physical actuator.  It turns normalized text into a *proposed* six-route
address.  A safety/CPU layer must still authorize any motor command.

The processing chain is kept explicit:

BC-DC  binary choice / direct command selection
TC-AC  ternary direction / actuator tendency
QC-RC  four-view computation / rotational-phase routing

Hopfield-style prototype attraction supplies associative recall.  A bounded
Boltzmann distribution exposes ambiguity instead of sampling an action.
Append-only learning receipts are the authoritative archive; all derived
prototypes can be rebuilt from them after restart.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from math import exp, pi
import re
from typing import Iterable, Mapping

from One_Wave_Bench.logic_core.six_route_logic import (
    BinaryChoice,
    LogicRoute,
    TernaryMove,
)


class VerbalCommand(str, Enum):
    FOLLOW = "follow"
    HURRY_UP = "hurry up"
    SLOW_DOWN = "slow down"
    STOP = "stop"


class DifferentialDirection(Enum):
    """The only three directional words exposed by the command brain."""

    COMPRESS = -1
    HOLD = 0
    EXPRESS = 1


@dataclass(frozen=True, slots=True)
class CommandDefinition:
    command: VerbalCommand
    polarity: BinaryChoice
    direction: DifferentialDirection
    octave: int
    phase_quadrant: int
    # Inward, Outward, Across, Over.  These are routing views, not new choices.
    quadratic_views: tuple[int, int, int, int]

    @property
    def rotational_phase(self) -> float:
        return self.phase_quadrant * pi / 2.0

    @property
    def route(self) -> LogicRoute:
        """Project the locked vocabulary into the settled six-address core."""

        return LogicRoute(self.polarity, TernaryMove(self.direction.value))


COMMANDS: Mapping[VerbalCommand, CommandDefinition] = {
    VerbalCommand.STOP: CommandDefinition(
        VerbalCommand.STOP,
        BinaryChoice.NO,
        DifferentialDirection.HOLD,
        octave=0,
        phase_quadrant=0,
        quadratic_views=(1, 0, 0, 1),
    ),
    VerbalCommand.FOLLOW: CommandDefinition(
        VerbalCommand.FOLLOW,
        BinaryChoice.YES,
        DifferentialDirection.HOLD,
        octave=0,
        phase_quadrant=1,
        quadratic_views=(0, 1, 1, 0),
    ),
    VerbalCommand.HURRY_UP: CommandDefinition(
        VerbalCommand.HURRY_UP,
        BinaryChoice.YES,
        DifferentialDirection.EXPRESS,
        octave=1,
        phase_quadrant=2,
        quadratic_views=(0, 1, 0, 1),
    ),
    VerbalCommand.SLOW_DOWN: CommandDefinition(
        VerbalCommand.SLOW_DOWN,
        BinaryChoice.YES,
        DifferentialDirection.COMPRESS,
        octave=-1,
        phase_quadrant=3,
        quadratic_views=(1, 0, 1, 0),
    ),
}


DEFAULT_PHRASES: Mapping[VerbalCommand, tuple[str, ...]] = {
    VerbalCommand.FOLLOW: ("follow", "follow me"),
    VerbalCommand.HURRY_UP: ("hurry up", "faster"),
    VerbalCommand.SLOW_DOWN: ("slow down", "slower"),
    VerbalCommand.STOP: ("stop", "halt", "emergency stop"),
}


def normalize_phrase(phrase: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", phrase.lower()))


@dataclass(frozen=True, slots=True)
class LearningReceipt:
    sequence: int
    phrase: str
    command: str
    previous_digest: str
    digest: str

    @classmethod
    def create(
        cls,
        sequence: int,
        phrase: str,
        command: VerbalCommand,
        previous_digest: str,
    ) -> "LearningReceipt":
        phrase = normalize_phrase(phrase)
        payload = f"{sequence}|{phrase}|{command.value}|{previous_digest}"
        digest = sha256(payload.encode("utf-8")).hexdigest()
        return cls(sequence, phrase, command.value, previous_digest, digest)

    def verify(self) -> None:
        try:
            command = VerbalCommand(self.command)
        except ValueError as exc:
            raise ValueError(f"unknown command in receipt: {self.command!r}") from exc
        expected = self.create(
            self.sequence, self.phrase, command, self.previous_digest
        )
        if self != expected:
            raise ValueError(f"invalid learning receipt at sequence {self.sequence}")

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_json(cls, line: str) -> "LearningReceipt":
        receipt = cls(**json.loads(line))
        receipt.verify()
        return receipt


@dataclass(frozen=True, slots=True)
class RecallReceipt:
    phrase: str
    command: VerbalCommand | None
    confidence: float
    probabilities: tuple[tuple[VerbalCommand, float], ...]
    executable: bool
    reason: str

    @property
    def definition(self) -> CommandDefinition | None:
        return None if self.command is None else COMMANDS[self.command]


@dataclass(frozen=True, slots=True)
class ExpressiveState:
    """Dream Engine / Field state: interprets and proposes; never commits."""

    cycle: int = 0
    device: str = "JETSON_GPU"
    proposed_command: VerbalCommand | None = None
    route_address: int | None = None
    rotational_phase: float = 0.0
    quadratic_views: tuple[int, int, int, int] = (0, 0, 0, 0)


@dataclass(frozen=True, slots=True)
class CompressiveState:
    """Administrator / Void state: preserves continuity and authorizes."""

    cycle: int = 0
    device: str = "JETSON_CPU"
    committed_command: VerbalCommand = VerbalCommand.STOP
    permission: bool = False
    consequence_error: float = 0.0
    reason: str = "reference hold"


@dataclass(frozen=True, slots=True)
class DualBrainReceipt:
    cue: str
    recall: RecallReceipt
    expressive_before: ExpressiveState
    expressive_after: ExpressiveState
    compressive_before: CompressiveState
    compressive_after: CompressiveState
    m4_device: str = "CPU_REFERENCE"

    @property
    def committed_definition(self) -> CommandDefinition:
        return COMMANDS[self.compressive_after.committed_command]


class M4DualStateRouter:
    """Fast router between expressive Dream Engine and compressive Administrator.

    The expressive side can propose.  The compressive side alone can commit.
    Consequence error is carried into the next routing cycle but does not edit
    the exact command archive.
    """

    def __init__(
        self,
        memory: "CommandMemory",
        *,
        m4_device: str = "CPU_REFERENCE",
        expressive_device: str = "JETSON_GPU",
        compressive_device: str = "JETSON_CPU",
    ):
        if not all((m4_device, expressive_device, compressive_device)):
            raise ValueError("all device provenance fields are required")
        self.memory = memory
        self.m4_device = m4_device
        self.expressive_device = expressive_device
        self.compressive_device = compressive_device
        self.expressive = ExpressiveState(device=expressive_device)
        self.compressive = CompressiveState(device=compressive_device)

    def route(
        self,
        cue: str,
        *,
        actuator_ready: bool = True,
        boundary_clear: bool = True,
        consequence_error: float = 0.0,
    ) -> DualBrainReceipt:
        if not isinstance(consequence_error, (int, float)) or consequence_error < 0:
            raise ValueError("consequence_error must be a nonnegative number")

        recall = self.memory.recall(cue)
        expressive_before = self.expressive
        compressive_before = self.compressive
        definition = recall.definition

        self.expressive = ExpressiveState(
            cycle=expressive_before.cycle + 1,
            device=self.expressive_device,
            proposed_command=recall.command,
            route_address=None if definition is None else definition.route.address,
            rotational_phase=0.0 if definition is None else definition.rotational_phase,
            quadratic_views=(0, 0, 0, 0) if definition is None else definition.quadratic_views,
        )

        # STOP is an explicit compressive safety commitment and requires no
        # actuator-ready permission.  Every movement proposal requires both
        # valid recall and current boundary permission.
        if recall.command is VerbalCommand.STOP:
            committed = VerbalCommand.STOP
            permission = True
            reason = "Administrator safety commit"
        elif not recall.executable:
            committed = VerbalCommand.STOP
            permission = False
            reason = "Administrator hold: recall unresolved"
        elif not actuator_ready:
            committed = VerbalCommand.STOP
            permission = False
            reason = "Administrator hold: actuator unavailable"
        elif not boundary_clear:
            committed = VerbalCommand.STOP
            permission = False
            reason = "Administrator hold: boundary blocked"
        else:
            committed = recall.command
            permission = True
            reason = "Administrator committed expressive proposal"

        self.compressive = CompressiveState(
            cycle=compressive_before.cycle + 1,
            device=self.compressive_device,
            committed_command=committed,
            permission=permission,
            consequence_error=float(consequence_error),
            reason=reason,
        )
        return DualBrainReceipt(
            cue=normalize_phrase(cue),
            recall=recall,
            expressive_before=expressive_before,
            expressive_after=self.expressive,
            compressive_before=compressive_before,
            compressive_after=self.compressive,
            m4_device=self.m4_device,
        )


class CommandMemory:
    """Exact archive plus rebuildable associative command recall."""

    def __init__(self, *, temperature: float = 0.35, execute_threshold: float = 0.72):
        if temperature <= 0:
            raise ValueError("temperature must be positive")
        if not 0.5 < execute_threshold <= 1.0:
            raise ValueError("execute_threshold must be in (0.5, 1]")
        self.temperature = temperature
        self.execute_threshold = execute_threshold
        self._receipts: list[LearningReceipt] = []
        self._phrase_to_command: dict[str, VerbalCommand] = {}

    @property
    def receipts(self) -> tuple[LearningReceipt, ...]:
        return tuple(self._receipts)

    def teach(self, phrase: str, command: VerbalCommand) -> LearningReceipt:
        normalized = normalize_phrase(phrase)
        if not normalized:
            raise ValueError("learned phrase cannot be empty")
        previous = self._receipts[-1].digest if self._receipts else "GENESIS"
        receipt = LearningReceipt.create(
            len(self._receipts), normalized, command, previous
        )
        self._apply_verified(receipt)
        return receipt

    def _apply_verified(self, receipt: LearningReceipt) -> None:
        receipt.verify()
        expected_sequence = len(self._receipts)
        expected_previous = self._receipts[-1].digest if self._receipts else "GENESIS"
        if receipt.sequence != expected_sequence:
            raise ValueError("learning receipts must be contiguous and ordered")
        if receipt.previous_digest != expected_previous:
            raise ValueError("learning receipt chain is broken")
        command = VerbalCommand(receipt.command)
        existing = self._phrase_to_command.get(receipt.phrase)
        if existing is not None and existing is not command:
            raise ValueError("a phrase cannot silently change command identity")
        self._receipts.append(receipt)
        self._phrase_to_command[receipt.phrase] = command

    @classmethod
    def defaults(cls, **kwargs) -> "CommandMemory":
        memory = cls(**kwargs)
        for command, phrases in DEFAULT_PHRASES.items():
            for phrase in phrases:
                memory.teach(phrase, command)
        return memory

    @classmethod
    def rebuild(
        cls, receipts: Iterable[LearningReceipt | str], **kwargs
    ) -> "CommandMemory":
        memory = cls(**kwargs)
        for item in receipts:
            receipt = LearningReceipt.from_json(item) if isinstance(item, str) else item
            memory._apply_verified(receipt)
        return memory

    def _token_vocabulary(self) -> tuple[str, ...]:
        return tuple(sorted({
            token
            for phrase in self._phrase_to_command
            for token in phrase.split()
        }))

    @staticmethod
    def _bipolar(phrase: str, vocabulary: tuple[str, ...]) -> tuple[int, ...]:
        tokens = set(phrase.split())
        return tuple(1 if token in tokens else -1 for token in vocabulary)

    def _hopfield_scores(self, phrase: str) -> dict[VerbalCommand, float]:
        vocabulary = self._token_vocabulary()
        if not vocabulary:
            return {command: 0.0 for command in VerbalCommand}
        cue = self._bipolar(phrase, vocabulary)
        scores: dict[VerbalCommand, float] = {}
        for command in VerbalCommand:
            patterns = [
                self._bipolar(stored_phrase, vocabulary)
                for stored_phrase, stored_command in self._phrase_to_command.items()
                if stored_command is command
            ]
            if not patterns:
                scores[command] = -1.0
                continue
            # Best prototype attraction preserves distinct aliases instead of
            # averaging their absent tokens into a fabricated memory.
            scores[command] = max(
                sum(a * b for a, b in zip(cue, pattern)) / len(vocabulary)
                for pattern in patterns
            )
        return scores

    def recall(self, phrase: str) -> RecallReceipt:
        normalized = normalize_phrase(phrase)
        if not normalized:
            return RecallReceipt(normalized, None, 0.0, (), False, "empty cue")

        # Stop aliases are checked before associative processing.  Safety is a
        # direct BC-DC route and never competes in a stochastic selection.
        exact = self._phrase_to_command.get(normalized)
        if exact is VerbalCommand.STOP:
            return RecallReceipt(
                normalized, exact, 1.0, ((exact, 1.0),), True,
                "direct safety command",
            )
        if exact is not None:
            return RecallReceipt(
                normalized, exact, 1.0, ((exact, 1.0),), True,
                "exact archive recall",
            )

        scores = self._hopfield_scores(normalized)
        peak = max(scores.values())
        weights = {
            command: exp((score - peak) / self.temperature)
            for command, score in scores.items()
        }
        total = sum(weights.values())
        probabilities = tuple(sorted(
            ((command, weight / total) for command, weight in weights.items()),
            key=lambda pair: (-pair[1], pair[0].value),
        ))
        command, confidence = probabilities[0]
        executable = confidence >= self.execute_threshold
        return RecallReceipt(
            normalized,
            command if executable else None,
            confidence,
            probabilities,
            executable,
            "associative recall" if executable else "ambiguous cue; hold for teaching",
        )


def octave_ratio(octave: int) -> float:
    """Harmonic scaling carried as a ratio; not an actuator speed command."""

    return 2.0 ** octave
