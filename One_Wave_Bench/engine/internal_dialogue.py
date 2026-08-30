"""Bounded internal dialogue for mounted Field/Void instances.

This is explicit program state, not access to any model's hidden chain-of-thought.
The goal is to give mounted instances a reproducible deliberation protocol:
Field proposes, Void challenges/checks, Field revises, and M4 routes the exchange
until commit/defer/deny or a hard turn limit.
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
    PROPOSE = "PROPOSE"
    CHALLENGE = "CHALLENGE"
    REVISE = "REVISE"
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
    allow_revision: bool = True
    allow_defer: bool = True


class InternalDialogue:
    """Run a bounded Field/Void exchange with M4 as the explicit router."""

    def __init__(self, policy: Optional[DialoguePolicy] = None) -> None:
        self.policy = policy or DialoguePolicy()

    def run(
        self,
        cue: Any,
        *,
        field_propose: Callable[[Any], Any],
        void_review: Callable[[Any, Any], tuple[DialogueAction, Any]],
        field_revise: Optional[Callable[[Any, Any], Any]] = None,
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

        proposal = field_propose(cue)
        field_used += 1
        append(DialogueRole.FIELD, DialogueAction.PROPOSE, proposal)

        current = proposal
        while turn_no < self.policy.max_turns:
            routed = m4_route(DialogueRole.FIELD, DialogueRole.VOID, current) if m4_route else current
            append(DialogueRole.M4, DialogueAction.ROUTE, routed, source="FIELD", target="VOID")
            if turn_no >= self.policy.max_turns:
                break

            if void_used >= self.policy.void_budget:
                break

            verdict, response = void_review(cue, routed)
            void_used += 1
            append(DialogueRole.VOID, verdict, response)

            if verdict in (DialogueAction.CONFIRM, DialogueAction.DENY):
                return DialogueResult(turns, verdict, response, exhausted=False)

            if verdict == DialogueAction.DEFER and not self.policy.allow_revision:
                return DialogueResult(turns, verdict, response, exhausted=False)

            if verdict not in (DialogueAction.CHALLENGE, DialogueAction.DEFER):
                raise ValueError(f"Unsupported Void dialogue action: {verdict}")

            if not self.policy.allow_revision or field_revise is None or field_used >= self.policy.field_budget:
                return DialogueResult(turns, DialogueAction.DEFER, response, exhausted=False)

            routed_back = m4_route(DialogueRole.VOID, DialogueRole.FIELD, response) if m4_route else response
            append(DialogueRole.M4, DialogueAction.ROUTE, routed_back, source="VOID", target="FIELD")
            if turn_no >= self.policy.max_turns:
                break

            current = field_revise(current, routed_back)
            field_used += 1
            append(DialogueRole.FIELD, DialogueAction.REVISE, current)

        return DialogueResult(
            turns=turns,
            outcome=DialogueAction.DEFER,
            final_payload=current,
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
        allow_revision=field_budget > 1,
        allow_defer=True,
    )
