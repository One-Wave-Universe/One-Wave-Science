from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import Callable, List, Sequence, Tuple


class State(str, Enum):
    FIELD = "FIELD"
    VOID = "VOID"


class Verdict(str, Enum):
    ACCEPT = "ACCEPT"
    HOLD = "HOLD"
    REJECT = "REJECT"


@dataclass
class RankedChoice:
    choice: object
    score: float


class PredictiveSubconscious:
    """Fast loop that repeatedly perturbs/ranks candidates before conscious choice."""

    def __init__(self, seed: int = 2):
        self.rng = random.Random(seed)
        self.bias = {}

    def rank(self, choices: Sequence[object], scorer: Callable[[object], float], ticks: int = 3) -> List[RankedChoice]:
        totals = {id(c): 0.0 for c in choices}
        objects = {id(c): c for c in choices}
        for _ in range(max(1, ticks)):
            for c in choices:
                key = id(c)
                learned = self.bias.get(repr(c), 0.0)
                jitter = self.rng.uniform(-0.03, 0.03)
                totals[key] += scorer(c) + learned + jitter
        return sorted(
            (RankedChoice(objects[k], v / max(1, ticks)) for k, v in totals.items()),
            key=lambda x: x.score,
            reverse=True,
        )

    def reinforce(self, choice: object, reward: float) -> None:
        key = repr(choice)
        old = self.bias.get(key, 0.0)
        self.bias[key] = max(-1.0, min(1.0, old * 0.9 + reward * 0.1))


class ParserB:
    """Predictive Field/Void chooser.

    FIELD generates/ranks candidate moves.
    VOID validates the best candidate against legality and ambiguity.
    HOLD remains an outcome, never a third conscious state.
    """

    def __init__(self, subconscious_ticks: int = 3, seed: int = 2):
        self.state = State.FIELD
        self.subconscious_ticks = subconscious_ticks
        self.subconscious = PredictiveSubconscious(seed)
        self.pending: List[RankedChoice] = []

    def choose(self, choices: Sequence[object], scorer: Callable[[object], float]) -> Tuple[Verdict, object | None, float]:
        if not choices:
            return Verdict.REJECT, None, 0.0
        self.state = State.FIELD
        self.pending = self.subconscious.rank(choices, scorer, self.subconscious_ticks)
        self.state = State.VOID
        best = self.pending[0]
        if len(self.pending) > 1:
            margin = best.score - self.pending[1].score
        else:
            margin = abs(best.score) + 1.0
        if margin < 0.015:
            verdict = Verdict.HOLD
        else:
            verdict = Verdict.ACCEPT
        self.state = State.FIELD
        return verdict, best.choice if verdict is Verdict.ACCEPT else None, best.score

    def feedback(self, choice: object, reward: float) -> None:
        self.subconscious.reinforce(choice, reward)
