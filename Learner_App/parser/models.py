"""Generic, domain-agnostic data contracts for the learner problem-builder core.

These types know nothing about algebra, music, or any other domain. Domain
knowledge belongs in adapters (see parser/adapters/).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


def _as_tuple(value: Any) -> tuple[str, ...]:
    return tuple(value) if value else ()


def _deep_freeze(value: Any) -> Any:
    """Recursively snapshot standard mutable containers (mapping, list,
    tuple, set) into read-only/hashable equivalents. An arbitrary custom
    object nested inside a constraint value is returned as-is -- the core
    freezes the container shapes it can recognize generically; it cannot
    know how to snapshot an arbitrary domain-specific object graph."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _deep_freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_deep_freeze(v) for v in value)
    return value


def _freeze_mapping(value: Mapping[str, Any] | None) -> MappingProxyType:
    """Snapshot `value` into a read-only mapping so a RulePacket stays a
    fixed instruction once built: neither mutating the caller's original
    dict (at any nesting depth) after construction, nor mutating
    packet.constraints/metadata directly, can change what a later
    build_problem() call sees."""
    items = dict(value) if value else {}
    return MappingProxyType({k: _deep_freeze(v) for k, v in items.items()})


@dataclass(frozen=True)
class RulePacket:
    """A router-issued request to build one problem.

    The router owns curriculum authority: which rules to target, which
    supporting rules are allowed, which are forbidden, difficulty, and
    domain/adapter selection. This object only carries that decision; it
    does not make it. Domain-specific knobs (e.g. a coefficient range for
    math) belong in `constraints`, not as dedicated fields here, so this
    type never has to grow per-domain fields.

    A RulePacket is meant to be a fixed instruction: build_problem() must
    produce the same result for the same packet and seed every time, so
    `constraints` and `metadata` are snapshotted into read-only mappings
    at construction (see _freeze_mapping()) rather than staying plain,
    mutable dicts a caller could change out from under a stored packet.
    """

    packet_id: str
    seed: int
    domain: str
    target_rules: tuple[str, ...]
    allowed_support_rules: tuple[str, ...] = ()
    forbidden_rules: tuple[str, ...] = ()
    difficulty: int = 1
    constraints: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_rules", _as_tuple(self.target_rules))
        object.__setattr__(self, "allowed_support_rules", _as_tuple(self.allowed_support_rules))
        object.__setattr__(self, "forbidden_rules", _as_tuple(self.forbidden_rules))
        object.__setattr__(self, "constraints", _freeze_mapping(self.constraints))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))


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
