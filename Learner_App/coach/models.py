"""Data contracts for the Phase 4 Coach (Explanation) Worker.

The Coach Worker is a worker under Router authority -- like Phase 1's
problem builder and Phase 3's Recall Worker -- not a third state machine
and not a curriculum planner. It reports deterministic, structured
explanation content for one rule_id at a time; it never decides which
rule needs explaining, when to explain, or whether to return to a new
problem. See `Learner_App/router/coach_integration.py` for where the
Router Loop turns a repeated error / explicit request / missing
prerequisite into a bounded ask of this worker.
"""

from __future__ import annotations

from dataclasses import dataclass

# Deterministic, explicit trigger-reason vocabulary (see issue #47's
# "Trigger behavior" section). There is no opaque "AI thought the learner
# seemed confused" trigger in Phase 4 -- every CoachRequest the router
# builds carries one of these three reasons.
TRIGGER_REPEATED_ERROR = "repeated_error"
TRIGGER_EXPLICIT_REQUEST = "explicit_request"
TRIGGER_MISSING_PREREQUISITE = "missing_prerequisite"
VALID_TRIGGER_REASONS = (
    TRIGGER_REPEATED_ERROR,
    TRIGGER_EXPLICIT_REQUEST,
    TRIGGER_MISSING_PREREQUISITE,
)

# The exact heading issue #47 requires for the learner-facing reference
# view that groups rule cards. Keep this string exactly as-is unless a
# future explicit UI setting changes it (per the issue).
RULE_BOOK_HEADING = "Rules are rules… cause we’re fucking tools!"


def _as_tuple(value) -> tuple[str, ...]:
    return tuple(value) if value else ()


class CoachError(Exception):
    """Base class for Coach-worker failures."""


class MalformedRuleExplanationError(CoachError):
    """Raised when a RuleExplanation is missing a required field or a
    required field is empty -- enforced at construction, the same way
    Phase 3's RecallRecord validates itself in __post_init__, so a
    rule that can only produce vague prose fails loudly instead of being
    silently registered and only discovered later at explain-time."""


class UnknownRuleError(CoachError):
    """Raised when the router (or the worker itself, while walking a
    prerequisite chain) asks for a rule_id that has no registered
    RuleExplanation."""


class CircularPrerequisiteError(CoachError):
    """Raised when walking a rule's prerequisite chain revisits a rule_id
    already being visited in the same walk -- a clean, explicit failure
    instead of recursing forever."""


class AnswerLeakError(CoachError):
    """Raised when a RuleExplanation's own examples/counterexamples would
    leak the active problem: a same-pattern example must use different
    values/content, never the exact text of the problem in front of the
    learner right now."""


@dataclass(frozen=True)
class RuleExplanation:
    """One rule's complete, concept-first explanation card.

    Immutable and self-validating: every required field must be a
    non-empty string, or construction raises MalformedRuleExplanationError
    rather than letting an incomplete card exist. There is deliberately no
    field capable of holding a solved answer -- this type cannot leak what
    it was never given.

    `prerequisites`/`uses_with` are rule_id strings naming other
    registered RuleExplanation records (see coach/worker.py for how the
    router walks `prerequisites` to find an unmet prerequisite to explain
    first). `formal_terms` is kept separate from `concept_first_note` on
    purpose: the label comes after the meaning, not before it.
    """

    rule_id: str
    title: str
    pattern: str
    if_text: str
    then_text: str
    why_text: str
    only_when_text: str
    do_not_use_when_text: str
    prerequisites: tuple[str, ...] = ()
    uses_with: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()
    counterexamples: tuple[str, ...] = ()
    concept_first_note: str = ""
    formal_terms: tuple[str, ...] = ()
    source_kind: str = "fixture"

    _REQUIRED_TEXT_FIELDS = (
        "rule_id",
        "title",
        "pattern",
        "if_text",
        "then_text",
        "why_text",
        "only_when_text",
        "do_not_use_when_text",
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "prerequisites", _as_tuple(self.prerequisites))
        object.__setattr__(self, "uses_with", _as_tuple(self.uses_with))
        object.__setattr__(self, "examples", _as_tuple(self.examples))
        object.__setattr__(self, "counterexamples", _as_tuple(self.counterexamples))
        object.__setattr__(self, "formal_terms", _as_tuple(self.formal_terms))

        missing = [
            name
            for name in self._REQUIRED_TEXT_FIELDS
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip()
        ]
        if missing:
            raise MalformedRuleExplanationError(
                f"RuleExplanation is missing required field(s): {missing!r}"
            )
