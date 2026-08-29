from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from enum import Enum
import re
from typing import Deque, Dict, List, Optional, Tuple

TOKEN_RE = re.compile(r"[A-Za-z0-9_'-]+")

class State(str, Enum):
    FIELD = "FIELD"
    VOID = "VOID"

class Verdict(str, Enum):
    ACCEPT = "ACCEPT"
    HOLD = "HOLD"
    REJECT = "REJECT"

@dataclass
class Proposal:
    intent: str
    confidence: float
    tokens: List[str]
    evidence: Dict[str, float]

@dataclass
class Result:
    intent: str
    verdict: Verdict
    confidence: float
    reason: str
    subconscious_ticks: int

class AssociativeSubconscious:
    def __init__(self, max_memory: int = 64):
        self.memory: Deque[Tuple[Tuple[str, ...], str, float]] = deque(maxlen=max_memory)
        self.salience: Counter[str] = Counter()

    @staticmethod
    def tokens(text: str) -> List[str]:
        return [x.lower() for x in TOKEN_RE.findall(text)]

    def run(self, text: str, ticks: int) -> Dict[str, float]:
        tokens = self.tokens(text)
        scores: Counter[str] = Counter()
        for _ in range(max(1, ticks)):
            for t in tokens:
                self.salience[t] = self.salience[t] * 0.90 + 1.0
            ts = set(tokens)
            for old_tokens, intent, weight in self.memory:
                old = set(old_tokens)
                overlap = len(ts & old)
                if overlap:
                    jaccard = overlap / max(1, len(ts | old))
                    scores[intent] += jaccard * weight
            for key in list(scores):
                scores[key] *= 0.96
        total = sum(scores.values())
        return {k: v / total for k, v in scores.items()} if total else {}

    def learn(self, tokens: List[str], intent: str, weight: float = 1.0):
        if tokens and intent != "unknown":
            self.memory.append((tuple(tokens), intent, max(0.1, min(2.0, weight))))

class ParserA:
    """Rule-first Field/Void parser with associative subconscious recall."""

    RULES = {
        "question": {"what", "why", "how", "when", "where", "who", "which"},
        "request": {"make", "build", "move", "show", "create", "change", "add", "remove", "please"},
        "stop": {"stop", "cancel", "abort", "quit"},
        "confirm": {"yes", "correct", "right", "confirm", "agree"},
        "reject": {"no", "wrong", "reject", "disagree"},
    }

    def __init__(self, subconscious_ticks: int = 3):
        self.state = State.FIELD
        self.subconscious_ticks = subconscious_ticks
        self.subconscious = AssociativeSubconscious()
        self.pending: Optional[Proposal] = None

    def field(self, text: str) -> Proposal:
        assert self.state is State.FIELD
        assoc = self.subconscious.run(text, self.subconscious_ticks)
        tokens = self.subconscious.tokens(text)
        bag = set(tokens)
        evidence: Counter[str] = Counter()
        for intent, words in self.RULES.items():
            evidence[intent] += len(bag & words)
        for intent, score in assoc.items():
            evidence[intent] += score * 1.35
        if evidence and evidence.most_common(1)[0][1] > 0:
            ranked = evidence.most_common(2)
            intent, best = ranked[0]
            second = ranked[1][1] if len(ranked) > 1 else 0.0
            confidence = min(0.98, 0.42 + best * 0.15 + max(0, best-second) * 0.08)
        else:
            intent = "unknown"
            confidence = 0.20 if tokens else 0.0
        self.pending = Proposal(intent, confidence, tokens, dict(evidence))
        self.state = State.VOID
        return self.pending

    def void(self) -> Result:
        assert self.state is State.VOID and self.pending is not None
        p = self.pending
        if not p.tokens:
            verdict, reason = Verdict.REJECT, "empty input"
        elif p.intent == "unknown":
            verdict, reason = Verdict.HOLD, "insufficient evidence"
        elif p.confidence < 0.52:
            verdict, reason = Verdict.HOLD, "weak interpretation"
        else:
            verdict, reason = Verdict.ACCEPT, "rule and context agree"
        if verdict is Verdict.ACCEPT:
            self.subconscious.learn(p.tokens, p.intent, p.confidence)
        result = Result(p.intent, verdict, p.confidence, reason, self.subconscious_ticks)
        self.pending = None
        self.state = State.FIELD
        return result

    def parse(self, text: str) -> Result:
        self.field(text)
        return self.void()
