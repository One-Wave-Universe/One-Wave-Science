"""Explicit registry of RuleExplanation records.

Mirrors parser/adapter.py's adapter registry: there is no plugin discovery
magic. A rule_id's explanation is only available after something calls
register_rule_explanation() (directly, or via a fixtures module's
register_default_explanations()-style helper, the same convention
parser/adapters/__init__.py uses for register_default_adapters()).
"""

from __future__ import annotations

from .models import RuleExplanation, UnknownRuleError

_REGISTRY: dict[str, RuleExplanation] = {}


class RuleExplanationAlreadyRegisteredError(Exception):
    """Raised when a rule_id is registered twice without explicit replace."""


def register_rule_explanation(explanation: RuleExplanation, *, replace: bool = False) -> None:
    if not replace and explanation.rule_id in _REGISTRY:
        raise RuleExplanationAlreadyRegisteredError(
            f"rule_id {explanation.rule_id!r} is already registered; "
            "pass replace=True to override"
        )
    _REGISTRY[explanation.rule_id] = explanation


def get_rule_explanation(rule_id: str) -> RuleExplanation:
    try:
        return _REGISTRY[rule_id]
    except KeyError as exc:
        raise UnknownRuleError(f"no RuleExplanation registered for rule_id {rule_id!r}") from exc


def known_explained_rule_ids() -> frozenset[str]:
    return frozenset(_REGISTRY)


def unregister_rule_explanation(rule_id: str) -> None:
    """Remove a registration. Mainly useful for test isolation."""
    _REGISTRY.pop(rule_id, None)
