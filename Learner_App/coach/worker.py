"""The Coach (Explanation) Worker: pure functions over RuleExplanation.

Every function here is deterministic and side-effect free except the
explicit registry in registry.py (populated only by an explicit
register_rule_explanation() call, never import-time magic -- see that
module's docstring). The worker never decides curriculum: it has no
concept of "target rules", "difficulty", "domain", repeated-error
thresholds, or what triggered the request. It only answers "what is the
explanation for this exact rule_id" and "does this explanation leak the
active problem". See router/coach_integration.py for the router-side
trigger policy built on top of these facts.
"""

from __future__ import annotations

from .models import AnswerLeakError, CircularPrerequisiteError, RuleExplanation
from .registry import get_rule_explanation


def explain_rule(rule_id: str) -> RuleExplanation:
    """Return the registered RuleExplanation for `rule_id`, or raise
    UnknownRuleError. A thin, named entry point so router-side code never
    has to import coach.registry directly."""
    return get_rule_explanation(rule_id)


def next_prerequisite_to_explain(
    rule_id: str, *, already_explained: frozenset[str] = frozenset()
) -> str | None:
    """Walk `rule_id`'s prerequisite chain and return the deepest
    not-yet-explained prerequisite -- the one furthest from `rule_id`
    itself along an unexplained chain -- or None if every prerequisite
    (if any) is already in `already_explained`.

    Recursing into a prerequisite's own prerequisites means a multi-level
    chain is explained foundation-first, not just one level up. A rule_id
    revisited within the same walk means the registered prerequisite data
    is circular; that raises CircularPrerequisiteError cleanly rather than
    recursing until Python's own stack gives out.
    """
    return _next_prerequisite(rule_id, already_explained=already_explained, visiting=frozenset())


def _next_prerequisite(
    rule_id: str, *, already_explained: frozenset[str], visiting: frozenset[str]
) -> str | None:
    if rule_id in visiting:
        raise CircularPrerequisiteError(
            f"circular prerequisite chain detected at rule_id {rule_id!r}"
        )
    explanation = get_rule_explanation(rule_id)
    visiting = visiting | {rule_id}
    for prereq_id in explanation.prerequisites:
        if prereq_id in already_explained:
            continue
        deeper = _next_prerequisite(
            prereq_id, already_explained=already_explained, visiting=visiting
        )
        return deeper if deeper is not None else prereq_id
    return None


def _normalize(text: str) -> str:
    return "".join(text.split())


def check_no_answer_leak(explanation: RuleExplanation, *, active_artifact_text: str) -> None:
    """Raise AnswerLeakError if any of `explanation`'s examples or
    counterexamples would expose the active problem: an exact match (after
    whitespace-insensitive normalization) against the active problem's own
    artifact text, in whole or as a contained substring. A same-pattern
    example is expected to differ in its actual values/content -- this is
    the deterministic, inspectable check for that requirement, not a
    judgment call."""
    if not active_artifact_text:
        return
    needle = _normalize(active_artifact_text)
    if not needle:
        return
    for text in explanation.examples + explanation.counterexamples:
        if needle in _normalize(text):
            raise AnswerLeakError(
                f"rule {explanation.rule_id!r} explanation example contains the active "
                "problem's own text"
            )


def explain_rules_used(
    rule_ids: tuple[str, ...], *, active_artifact_text: str = ""
) -> tuple[RuleExplanation, ...]:
    """The deterministic `problem.rules_used[] -> rule explanation
    record(s)` lookup path: every generated problem can reference the
    exact rule explanation(s) it uses (e.g. a "rule help" link) without
    exposing its own answer. Each explanation is leak-checked against
    `active_artifact_text` exactly as explain_rule()'s callers already do
    for the in-progress-explanation path -- a reference link is still a
    link into the same Coach content, so it is held to the same
    no-answer-leak standard, not a looser one."""
    explanations = tuple(explain_rule(rule_id) for rule_id in rule_ids)
    for explanation in explanations:
        check_no_answer_leak(explanation, active_artifact_text=active_artifact_text)
    return explanations


def to_explanation_payload(explanation: RuleExplanation) -> dict:
    """A JSON-serializable, deterministic snapshot of `explanation` -- the
    exact structured content a caller (demo, future UI, tests) should
    render. Field order is fixed so two calls for the same rule_id are
    byte-identical once serialized."""
    return {
        "rule_id": explanation.rule_id,
        "title": explanation.title,
        "pattern": explanation.pattern,
        "if_text": explanation.if_text,
        "then_text": explanation.then_text,
        "why_text": explanation.why_text,
        "only_when_text": explanation.only_when_text,
        "do_not_use_when_text": explanation.do_not_use_when_text,
        "prerequisites": list(explanation.prerequisites),
        "uses_with": list(explanation.uses_with),
        "examples": list(explanation.examples),
        "counterexamples": list(explanation.counterexamples),
        "concept_first_note": explanation.concept_first_note,
        "formal_terms": list(explanation.formal_terms),
        "source_kind": explanation.source_kind,
    }
