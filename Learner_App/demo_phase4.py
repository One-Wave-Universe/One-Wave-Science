#!/usr/bin/env python3
"""Headless demonstration of Phase 4's Coach (Explanation) Worker.

Run from the repository root:

    python3 -m Learner_App.demo_phase4

Extends the Phase 2/3 RouterLoop (unchanged lifecycle/recall contracts)
with a Coach Worker call: when the learner repeats the same missing-rule
error twice in a row, policy.py's existing EXPLAIN decision fires (exactly
as it already did in Phase 2), and the Router now resolves that into a
bounded CoachRequest -- by default redirected to an unmet prerequisite
first (coach_prerequisite_first=True), so the learner sees the general
"inverse operation" concept before the specific add/subtract rule that
depends on it. A second repeat of the same error, after that prerequisite
is already marked explained, explains the specific rule directly.

The demo also shows the explicit "I don't understand" path
(request_explanation()), which never grades the in-progress attempt.

No UI, no LLM/network; running this script twice produces byte-identical
output.
"""

from __future__ import annotations

from Learner_App.coach import RULE_BOOK_HEADING, to_explanation_payload
from Learner_App.coach.fixtures.math_basic_equations import register_default_explanations
from Learner_App.parser.adapter import registered_domains
from Learner_App.parser.adapters import register_default_adapters
from Learner_App.parser.adapters.math_basic_equations import EQ_ADD_INVERSE
from Learner_App.router import LearnerAttempt, PolicyConfig, RouterLoop


def _print_explanation(explanation) -> None:
    payload = to_explanation_payload(explanation)
    print(f"    {RULE_BOOK_HEADING}")
    print(f"    [{payload['rule_id']}] {payload['title']} -- {payload['pattern']}")
    print(f"      {payload['if_text']}")
    print(f"      {payload['then_text']}")
    print(f"      {payload['why_text']}")
    print(f"      {payload['only_when_text']}")
    print(f"      {payload['do_not_use_when_text']}")
    if payload["concept_first_note"]:
        print(f"      concept-first: {payload['concept_first_note']}")
    if payload["examples"]:
        print(f"      example: {payload['examples'][0]}")
    if payload["formal_terms"]:
        print(f"      formal term(s) (introduced after the meaning): {payload['formal_terms']}")


def _miss(problem):
    """Reports no rules demonstrated -- deterministically the same
    error_kind ("missing_rule:<target>") every time, which is what lets
    the repeated-error threshold actually fire."""
    return LearnerAttempt(problem_id=problem.problem_id, outcome="incorrect", reported_rules_used=())


def _correct(problem):
    return LearnerAttempt(
        problem_id=problem.problem_id, outcome="correct", reported_rules_used=problem.rules_used
    )


def main() -> None:
    if not registered_domains():
        register_default_adapters()
    register_default_explanations()

    config = PolicyConfig(curriculum=(((EQ_ADD_INVERSE,), ()),), repeated_error_threshold=2)
    loop = RouterLoop(config=config, base_seed=9000)

    print("Phase 4 deterministic Coach demo (base_seed=9000)")
    print("\n=== Explicit 'I don't understand' path ===")
    problem = loop.generate_problem()
    print(f"1. Router presents a verified problem: {problem.artifact_text!r}")
    reference_links = loop.rule_explanations_for(problem)
    print(
        f"   reference link (problem.rules_used -> explanations, no answer exposed): "
        f"{[e.rule_id for e in reference_links]}"
    )
    request = loop.request_explanation()
    print(f"   explicit request: rule_id={request.rule_id!r} trigger={request.trigger_reason!r}")
    explanation = loop.explain()
    print("2. Coach returns the exact concept-first rule card (no active answer exposed):")
    _print_explanation(explanation)
    print(f"   active problem text never appears above: {problem.artifact_text!r}")

    # Finish this cycle correctly so the router returns to a clean
    # boundary before the repeated-error path below.
    loop.submit_attempt(_correct(problem))
    loop.route_next()

    print("\n=== Repeated same-category error path ===")
    decision = None
    for cycle_number in range(1, 3):
        problem = loop.generate_problem()
        print(f"\n--- cycle {cycle_number} ---")
        print(f"1. Router presents a verified problem: {problem.artifact_text!r}")
        evidence = loop.submit_attempt(_miss(problem))
        print(f"   learner misses: error_kind={evidence.error_kind!r}")
        decision = loop.route_next()
        print(f"   next route: action={decision.action.value} reason={decision.reason_code!r}")
        if loop.pending_coach_request is not None:
            print(
                f"3. Router routes to Coach: rule_id={loop.pending_coach_request.rule_id!r} "
                f"trigger={loop.pending_coach_request.trigger_reason!r}"
            )
            explanation = loop.explain()
            print("4. Coach returns the exact concept-first rule card:")
            _print_explanation(explanation)
            print(f"5. no active answer is exposed (active problem: {problem.artifact_text!r})")

    print("\n6. Router returns to the learning loop and produces an appropriate next problem:")
    next_problem = loop.generate_problem()
    print(f"   same pattern, held difficulty: {next_problem.artifact_text!r}")
    loop.submit_attempt(_correct(next_problem))
    final_decision = loop.route_next()
    print(f"   that attempt succeeds -> action={final_decision.action.value}")

    print(f"\ntask_state (clean boundary): {loop.task_state.lifecycle_state}")
    print(f"evaluator_state (clean boundary): {loop.evaluator_state.lifecycle_state}")
    print(f"pending_coach_request (clean boundary): {loop.pending_coach_request}")


if __name__ == "__main__":
    main()
