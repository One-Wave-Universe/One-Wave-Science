"""Router-side decisions for when/what to ask the Coach Worker to explain
(Phase 4).

Everything domain-agnostic lives in `Learner_App/coach/` (the worker): it
only ever sees rule_id strings and an already-explained set. Deciding
*when* an explanation is needed, *which* rule, and whether to detour
through an unmet prerequisite first is router-side decision logic, kept
separate the same way recall_integration.py keeps RULE_INVERSES/injection
policy separate from the Recall Worker itself.

The Coach is never triggered by an opaque "the learner seemed confused"
guess: decide_coach_request() only ever fires off the Router's own
existing, already-deterministic policy decision (RouteAction.EXPLAIN,
produced by policy.decide_next_route()'s repeated-error threshold -- see
policy.REASON_REPEATED_ERROR_EXPLAIN). The explicit "I don't understand"
path is a separate, equally explicit entry point (see
RouterLoop.request_explanation()), not a variant of this one.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import EvaluationEvidence, RouteAction, RouteDecision
from ..coach.models import TRIGGER_MISSING_PREREQUISITE, TRIGGER_REPEATED_ERROR
from ..coach.worker import next_prerequisite_to_explain

_MISSING_RULE_PREFIX = "missing_rule:"


@dataclass(frozen=True)
class CoachRequest:
    """One bounded ask to the Coach Worker: explain exactly this rule, for
    exactly this reason. The Router builds these; the Coach never invents
    its own request."""

    rule_id: str
    trigger_reason: str


def rule_to_explain_from_error_kind(error_kind: str | None) -> str | None:
    """Deterministically recover the rule_id State Machine B encoded into
    `error_kind` (see state_machine_b.evaluate_attempt's
    f"missing_rule:{missing[0]}"), or None if error_kind isn't that exact
    shape. No inference beyond string-prefix matching -- either the
    rule_id is right there or this returns None."""
    if error_kind is None or not error_kind.startswith(_MISSING_RULE_PREFIX):
        return None
    rule_id = error_kind[len(_MISSING_RULE_PREFIX):]
    return rule_id or None


def decide_coach_request(
    route: RouteDecision, evidence: EvaluationEvidence | None
) -> CoachRequest | None:
    """Whether this cycle's RouteDecision calls for a Coach explanation,
    and for which rule. Only ever non-None when the Router's own policy
    already decided action == EXPLAIN -- this function does not invent a
    reason to explain on its own, it only resolves *which rule* given one
    the Router already made."""
    if route.action != RouteAction.EXPLAIN:
        return None
    rule_id = rule_to_explain_from_error_kind(evidence.error_kind) if evidence else None
    if rule_id is None and route.target_rules:
        rule_id = route.target_rules[0]
    if rule_id is None:
        return None
    return CoachRequest(rule_id=rule_id, trigger_reason=TRIGGER_REPEATED_ERROR)


def apply_prerequisite_first(
    request: CoachRequest,
    *,
    already_explained: frozenset[str],
    prefer_prerequisite_first: bool,
) -> CoachRequest:
    """If configured and `request.rule_id` has an unexplained prerequisite,
    redirect the request to that prerequisite instead -- what the learner
    (or the repeated error) actually pointed at stays recorded in
    `trigger_reason` becoming TRIGGER_MISSING_PREREQUISITE. May raise
    UnknownRuleError (propagated from coach.worker) if `request.rule_id`
    itself has no registered explanation; callers that want that rejected
    at a specific, obvious boundary should look it up via
    coach.worker.explain_rule() right after this returns."""
    if not prefer_prerequisite_first:
        return request
    prereq_id = next_prerequisite_to_explain(request.rule_id, already_explained=already_explained)
    if prereq_id is None:
        return request
    return CoachRequest(rule_id=prereq_id, trigger_reason=TRIGGER_MISSING_PREREQUISITE)
