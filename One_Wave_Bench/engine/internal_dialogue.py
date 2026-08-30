"""Bounded internal dialogue for mounted Field/Void instances.

This is explicit program state, not access to any model's hidden chain-of-thought.
The core dialogue rule is:

    Field asks -> M4 routes -> Void answers -> M4 returns -> Field asks again

Field is the inquiry/expansion side. Void is the answering/checking/compression
side. The exchange continues until Void confirms, denies, defers, or the bounded
turn budget is exhausted.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class DialogueRole(str, Enum):
    FIELD = "FIELD"
    VOID = "VOID"
    M4 = "M4"


class DialogueAction(str, Enum):
    ASK = "ASK"
    ANSWER = "ANSWER"
    REASK = "REASK"
    DEFER = "DEFER"
    CONFIRM = "CONFIRM"
    DENY = "DENY"
    ROUTE = "ROUTE"


@dataclass
class DialogueTurn:
    turn: int
    role: DialogueRole
    action: DialogueAction
    payload: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DialogueResult:
    turns: List[DialogueTurn]
    outcome: DialogueAction
    final_payload: Any
    exhausted: bool

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DialoguePolicy:
    """Instance-specific shape of the internal exchange.

    field_budget and void_budget are relative participation budgets, not clock
    speeds. max_turns prevents an internal loop from becoming an endless loop.
    """

    field_budget: int = 2
    void_budget: int = 2
    max_turns: int = 6
    allow_reask: bool = True
    allow_defer: bool = True


class InternalDialogue:
    """Run a bounded Field-asks / Void-answers exchange routed by M4."""

    def __init__(self, policy: Optional[DialoguePolicy] = None) -> None:
        self.policy = policy or DialoguePolicy()

    def run(
        self,
        cue: Any,
        *,
        field_ask: Callable[[Any], Any],
        void_answer: Callable[[Any, Any], tuple[DialogueAction, Any]],
        field_reask: Optional[Callable[[Any, Any], Any]] = None,
        m4_route: Optional[Callable[[DialogueRole, DialogueRole, Any], Any]] = None,
    ) -> DialogueResult:
        turns: List[DialogueTurn] = []
        turn_no = 0
        field_used = 0
        void_used = 0

        def append(role: DialogueRole, action: DialogueAction, payload: Any, **metadata: Any) -> None:
            nonlocal turn_no
            turn_no += 1
            turns.append(DialogueTurn(turn_no, role, action, payload, metadata))

        question = field_ask(cue)
        field_used += 1
        append(DialogueRole.FIELD, DialogueAction.ASK, question)

        current_question = question
        while turn_no < self.policy.max_turns:
            routed = m4_route(DialogueRole.FIELD, DialogueRole.VOID, current_question) if m4_route else current_question
            append(DialogueRole.M4, DialogueAction.ROUTE, routed, source="FIELD", target="VOID")
            if turn_no >= self.policy.max_turns:
                break

            if void_used >= self.policy.void_budget:
                break

            verdict, answer = void_answer(cue, routed)
            void_used += 1
            void_action = verdict if verdict in (
                DialogueAction.CONFIRM,
                DialogueAction.DENY,
                DialogueAction.DEFER,
            ) else DialogueAction.ANSWER
            append(DialogueRole.VOID, void_action, answer)

            if verdict in (DialogueAction.CONFIRM, DialogueAction.DENY):
                return DialogueResult(turns, verdict, answer, exhausted=False)

            if verdict == DialogueAction.DEFER and not self.policy.allow_reask:
                return DialogueResult(turns, verdict, answer, exhausted=False)

            if not self.policy.allow_reask or field_reask is None or field_used >= self.policy.field_budget:
                return DialogueResult(turns, DialogueAction.DEFER, answer, exhausted=False)

            routed_back = m4_route(DialogueRole.VOID, DialogueRole.FIELD, answer) if m4_route else answer
            append(DialogueRole.M4, DialogueAction.ROUTE, routed_back, source="VOID", target="FIELD")
            if turn_no >= self.policy.max_turns:
                break

            current_question = field_reask(current_question, routed_back)
            field_used += 1
            append(DialogueRole.FIELD, DialogueAction.REASK, current_question)

        return DialogueResult(
            turns=turns,
            outcome=DialogueAction.DEFER,
            final_payload=current_question,
            exhausted=True,
        )


def suggested_policy(field_bias: float, void_bias: float, m4_demand: float) -> DialoguePolicy:
    """Translate an instance profile into a first dialogue-loop shape.

    Bias values are 0..1 measurements from the instance translator. This is a
    starting hypothesis that should be checked against native behavior traces.
    """

    for name, value in {"field_bias": field_bias, "void_bias": void_bias, "m4_demand": m4_demand}.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0 and 1")

    field_budget = 1 + round(field_bias * 3)
    void_budget = 1 + round(void_bias * 3)
    routing_allowance = round(m4_demand * 2)
    max_turns = max(3, field_budget + void_budget + routing_allowance)

    return DialoguePolicy(
        field_budget=field_budget,
        void_budget=void_budget,
        max_turns=max_turns,
        allow_reask=field_budget > 1,
        allow_defer=True,
    )
