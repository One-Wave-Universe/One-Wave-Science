"""Router-side decisions built on the Recall Worker's facts (Phase 3).

Everything domain-agnostic lives in `Learner_App/recall/` (the worker):
it only ever sees rule_id strings and cycle numbers. Everything here is
demo *configuration and decision logic* for math/basic_equations, kept
separate exactly the way policy.py keeps DEFAULT_CURRICULUM separate from
decide_next_route()'s algorithm. Swapping domains means swapping
RULE_INVERSES and known_rule_ids()'s inputs, not rewriting the Recall
Worker or this module's decision shape.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping

from . import policy
from .models import RouteDecision
from ..parser.adapter import get_adapter
from ..parser.adapters.math_basic_equations import (
    EQ_ADD_INVERSE,
    EQ_DIV_INVERSE,
    EQ_MUL_INVERSE,
    EQ_SUB_INVERSE,
)
from ..parser.models import RulePacket
from ..recall.models import RecallConfig, RecallRecord, UnknownRuleError
from ..recall.worker import learn_rule as _learn_rule

# Real, declared inverse relationships for math/basic_equations -- not
# every rule has one. EQ.IDENTITY intentionally has no entry: it must
# never get a fake inverse.
RULE_INVERSES: dict[str, str] = {
    EQ_ADD_INVERSE: EQ_SUB_INVERSE,
    EQ_SUB_INVERSE: EQ_ADD_INVERSE,
    EQ_MUL_INVERSE: EQ_DIV_INVERSE,
    EQ_DIV_INVERSE: EQ_MUL_INVERSE,
}


def known_rule_ids(config: policy.PolicyConfig, inverses: Mapping[str, str]) -> frozenset[str]:
    """The universe of rule_ids this router configuration recognizes --
    every rule any curriculum step can target or allow, plus every rule
    named on either side of an inverse mapping."""
    ids: set[str] = set()
    for target_rules, allowed_support_rules in config.curriculum:
        ids.update(target_rules)
        ids.update(allowed_support_rules)
    ids.update(inverses.keys())
    ids.update(inverses.values())
    return frozenset(ids)


def schedule_learned_rule(
    rule_id: str, *, cycle: int, config: RecallConfig, known_rules: frozenset[str]
) -> RecallRecord:
    """Create a fresh RecallRecord for a rule just mastered for the first
    time. Raises UnknownRuleError rather than silently tracking a rule_id
    outside the recognized curriculum/inverse universe."""
    if rule_id not in known_rules:
        raise UnknownRuleError(f"cannot schedule recall for unrecognized rule_id {rule_id!r}")
    return _learn_rule(rule_id, cycle=cycle, config=config)


def packet_is_feasible(
    *,
    domain: str,
    target_rules: tuple[str, ...],
    allowed_support_rules: tuple[str, ...],
    forbidden_rules: tuple[str, ...],
    difficulty: int,
    seed: int,
) -> bool:
    """Whether Phase 1 would accept a packet with these fields, without
    actually generating a problem from it. Calls only the adapter's
    public validate_packet() contract method (part of every adapter's
    required five-method interface) plus the same generic
    target/forbidden contradiction check core.py itself makes -- never
    touches adapter-internal combination tables directly."""
    if set(target_rules) & set(forbidden_rules):
        return False
    adapter = get_adapter(domain)
    candidate = RulePacket(
        packet_id="recall-feasibility-check",
        seed=seed,
        domain=domain,
        target_rules=target_rules,
        allowed_support_rules=allowed_support_rules,
        forbidden_rules=forbidden_rules,
        difficulty=difficulty,
    )
    return not adapter.validate_packet(candidate)


def inject_due_recall(route: RouteDecision, due_rule_ids: tuple[str, ...]) -> RouteDecision:
    """Return `route` with the first feasible due rule folded into
    target_rules alongside the curriculum's own target(s).

    Tries `due_rule_ids` in priority order (most overdue first, per
    recall.worker.due_rules()) rather than only ever looking at the single
    most-overdue candidate: a candidate whose combination with the
    curriculum's rule is structurally infeasible (e.g. MUL_INVERSE +
    DIV_INVERSE, which Phase 1 never supports together) must not
    permanently block every less-overdue-but-combinable candidate behind
    it -- that candidate stays overdue and keeps winning "most overdue"
    forever, starving everything else. Falling through to the next
    candidate is still a clean skip of the infeasible one, not a forced
    packet.

    Returns `route` unchanged if there is nothing due, every due candidate
    is already targeted or infeasible to add, or the due list is empty.
    Recall injection is always additive to the curriculum's target, never
    a replacement: a recall-only cycle would make the curriculum-
    advancement policy (which reads the same evidence) evaluate the wrong
    thing.
    """
    for due_rule_id in due_rule_ids:
        if due_rule_id in route.target_rules:
            continue
        combined_targets = tuple(route.target_rules) + (due_rule_id,)
        if packet_is_feasible(
            domain=route.domain,
            target_rules=combined_targets,
            allowed_support_rules=route.allowed_support_rules,
            forbidden_rules=route.forbidden_rules,
            difficulty=route.difficulty,
            seed=route.seed,
        ):
            return dataclasses.replace(
                route, target_rules=combined_targets, recall_injected_rule_id=due_rule_id
            )
    return route
