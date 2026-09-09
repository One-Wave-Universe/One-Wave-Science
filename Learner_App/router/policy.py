"""Deterministic v1 routing policy for the Phase 2 proof loop.

The routing ALGORITHM in decide_next_route() is domain-agnostic: it only
ever compares rule-ID strings and advances an index into a curriculum
sequence, never inspecting problem structure or answers. DEFAULT_CURRICULUM
below is demo *configuration* for the one adapter Phase 1 ships
(math/basic_equations) -- swapping to a different domain means swapping
this sequence and PolicyConfig.domain, not rewriting the algorithm.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import RouteAction, RouteDecision
from ..parser.adapters.math_basic_equations import DOMAIN as MATH_DOMAIN
from ..parser.adapters.math_basic_equations import EQ_ADD_INVERSE, EQ_MUL_INVERSE

MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 5
REPEATED_ERROR_THRESHOLD = 2  # same error_kind this many times in a row -> EXPLAIN

REASON_INITIAL = "initial"
REASON_CORRECT_ADVANCE = "correct_advance"
REASON_INCORRECT_REPEAT = "incorrect_repeat"
REASON_INCORRECT_REDUCE_DIFFICULTY = "incorrect_reduce_difficulty"
REASON_REPEATED_ERROR_EXPLAIN = "repeated_error_explain"

# A curriculum step is (target_rules, allowed_support_rules). The router's
# progression through this tuple is the "prerequisite sequencing" it owns.
CurriculumStep = tuple[tuple[str, ...], tuple[str, ...]]

DEFAULT_CURRICULUM: tuple[CurriculumStep, ...] = (
    ((EQ_ADD_INVERSE,), ()),
    ((EQ_MUL_INVERSE,), ()),
    ((EQ_ADD_INVERSE, EQ_MUL_INVERSE), ()),
)


@dataclass(frozen=True)
class PolicyConfig:
    """Explicit configuration -- no magic numbers scattered through the
    routing algorithm itself."""

    domain: str = MATH_DOMAIN
    curriculum: tuple[CurriculumStep, ...] = DEFAULT_CURRICULUM
    forbidden_rules: tuple[str, ...] = ()
    min_difficulty: int = MIN_DIFFICULTY
    max_difficulty: int = MAX_DIFFICULTY
    repeated_error_threshold: int = REPEATED_ERROR_THRESHOLD


def initial_route_decision(config: PolicyConfig, *, seed: int) -> RouteDecision:
    target_rules, allowed_support_rules = config.curriculum[0]
    return RouteDecision(
        action=RouteAction.ADVANCE,
        target_rules=target_rules,
        allowed_support_rules=allowed_support_rules,
        forbidden_rules=config.forbidden_rules,
        difficulty=config.min_difficulty,
        domain=config.domain,
        seed=seed,
        reason_code=REASON_INITIAL,
    )


def decide_next_route(
    *,
    config: PolicyConfig,
    current: RouteDecision,
    curriculum_index: int,
    outcome: str,
    consecutive_same_error: int,
    seed: int,
) -> tuple[RouteDecision, int]:
    """Pure function: the same arguments always produce the same
    (RouteDecision, next curriculum_index). No state is read or mutated
    outside these arguments.

    IF correct              -> ADVANCE: next curriculum step, harder.
    IF incorrect/incomplete:
      IF same error repeated >= threshold -> EXPLAIN: hold rules/difficulty.
      ELIF difficulty can drop            -> REDUCE_DIFFICULTY: hold rules.
      ELSE                                -> REPEAT: hold rules/difficulty.
    """
    if outcome == "correct":
        next_index = min(curriculum_index + 1, len(config.curriculum) - 1)
        target_rules, allowed_support_rules = config.curriculum[next_index]
        decision = RouteDecision(
            action=RouteAction.ADVANCE,
            target_rules=target_rules,
            allowed_support_rules=allowed_support_rules,
            forbidden_rules=config.forbidden_rules,
            difficulty=min(config.max_difficulty, current.difficulty + 1),
            domain=config.domain,
            seed=seed,
            reason_code=REASON_CORRECT_ADVANCE,
        )
        return decision, next_index

    target_rules, allowed_support_rules = config.curriculum[curriculum_index]

    if consecutive_same_error >= config.repeated_error_threshold:
        decision = RouteDecision(
            action=RouteAction.EXPLAIN,
            target_rules=target_rules,
            allowed_support_rules=allowed_support_rules,
            forbidden_rules=config.forbidden_rules,
            difficulty=current.difficulty,
            domain=config.domain,
            seed=seed,
            reason_code=REASON_REPEATED_ERROR_EXPLAIN,
        )
    elif current.difficulty > config.min_difficulty:
        decision = RouteDecision(
            action=RouteAction.REDUCE_DIFFICULTY,
            target_rules=target_rules,
            allowed_support_rules=allowed_support_rules,
            forbidden_rules=config.forbidden_rules,
            difficulty=max(config.min_difficulty, current.difficulty - 1),
            domain=config.domain,
            seed=seed,
            reason_code=REASON_INCORRECT_REDUCE_DIFFICULTY,
        )
    else:
        decision = RouteDecision(
            action=RouteAction.REPEAT,
            target_rules=target_rules,
            allowed_support_rules=allowed_support_rules,
            forbidden_rules=config.forbidden_rules,
            difficulty=current.difficulty,
            domain=config.domain,
            seed=seed,
            reason_code=REASON_INCORRECT_REPEAT,
        )
    return decision, curriculum_index
