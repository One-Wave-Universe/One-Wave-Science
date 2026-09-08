"""Generic, domain-agnostic data contracts for the learner problem-builder core.

These types know nothing about algebra, music, or any other domain. Domain
knowledge belongs in adapters (see parser/adapters/).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _as_tuple(value: Any) -> tuple[str, ...]:
    return tuple(value) if value else ()


@dataclass(frozen=True)
class RulePacket:
    """A router-issued request to build one problem.

    The router owns curriculum authority: which rules to target, which
    supporting rules are allowed, which are forbidden, difficulty, and
    domain/adapter selection. This object only carries that decision; it
    does not make it. Domain-specific knobs (e.g. a coefficient range for
    math) belong in `constraints`, not as dedicated fields here, so this
    type never has to grow per-domain fields.
    """

    packet_id: str
    seed: int
    domain: str
    target_rules: tuple[str, ...]
    allowed_support_rules: tuple[str, ...] = ()
    forbidden_rules: tuple[str, ...] = ()
    difficulty: int = 1
    constraints: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_rules", _as_tuple(self.target_rules))
        object.__setattr__(self, "allowed_support_rules", _as_tuple(self.allowed_support_rules))
        object.__setattr__(self, "forbidden_rules", _as_tuple(self.forbidden_rules))


@dataclass(frozen=True)
class VerificationResult:
    """The outcome of independently re-parsing and checking a candidate."""

    requested_rules_present: bool
    forbidden_rules_absent: bool
    well_formed: bool
    adapter_valid: bool
    errors: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "errors", _as_tuple(self.errors))

    @property
    def passed(self) -> bool:
        return (
            self.requested_rules_present
            and self.forbidden_rules_absent
            and self.well_formed
            and self.adapter_valid
            and not self.errors
        )


@dataclass(frozen=True)
class GeneratedProblem:
    """The public result returned to the router.

    No field on this object may carry the learner's solved answer.
    """

    problem_id: str
    seed: int
    domain: str
    artifact_text: str
    structure: Any
    rules_requested: tuple[str, ...]
    rules_used: tuple[str, ...]
    operations_present: tuple[str, ...]
    verification: VerificationResult
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "rules_requested", _as_tuple(self.rules_requested))
        object.__setattr__(self, "rules_used", _as_tuple(self.rules_used))
        object.__setattr__(self, "operations_present", _as_tuple(self.operations_present))
