#!/usr/bin/env python3
"""Headless demonstration of one full Phase 2 deterministic learning cycle.

Run from the repository root:

    python3 -m Learner_App.demo_phase2

Registers the Phase 1 math/basic_equations adapter, then drives a
RouterLoop through several cycles -- a correct attempt, an incorrect
attempt, and a repeated same-category incorrect attempt -- printing the
GeneratedProblem, EvaluationEvidence, and next RouteDecision at each step.
No UI, no LLM/network calls; everything here is deterministic given the
seed (run twice, get byte-identical output).
"""

from __future__ import annotations

from Learner_App.parser.adapter import registered_domains
from Learner_App.parser.adapters import register_default_adapters
from Learner_App.router import LearnerAttempt, PolicyConfig, RouterLoop


def _print_cycle(n: int, problem, evidence, decision) -> None:
    print(f"\n--- cycle {n} ---")
    print(f"  generated:  {problem.artifact_text!r}  (rules_used={problem.rules_used}, "
          f"verified={problem.verification.passed})")
    print(f"  attempt:    outcome={evidence.outcome!r} error_kind={evidence.error_kind!r} "
          f"missing_rules={evidence.missing_rules} confidence={evidence.confidence!r}")
    print(f"  next route: action={decision.action.value} reason_code={decision.reason_code!r} "
          f"target_rules={decision.target_rules} difficulty={decision.difficulty} seed={decision.seed}")


def main() -> None:
    if not registered_domains():
        register_default_adapters()

    loop = RouterLoop(config=PolicyConfig(), base_seed=1000)

    def correct_attempt(problem):
        return LearnerAttempt(
            problem_id=problem.problem_id,
            outcome="correct",
            reported_rules_used=problem.rules_used,
        )

    def incorrect_attempt(problem):
        return LearnerAttempt(
            problem_id=problem.problem_id, outcome="incorrect", reported_rules_used=()
        )

    print("Phase 2 deterministic router-loop demo (base_seed=1000)")
    print(f"task_state before cycle 1: {loop.task_state}")

    problem, evidence, decision = loop.run_one_cycle(correct_attempt)
    _print_cycle(1, problem, evidence, decision)

    problem, evidence, decision = loop.run_one_cycle(incorrect_attempt)
    _print_cycle(2, problem, evidence, decision)

    problem, evidence, decision = loop.run_one_cycle(incorrect_attempt)
    _print_cycle(3, problem, evidence, decision)

    print(f"\ntask_state after cycle 3 (clean boundary): {loop.task_state}")
    print(f"evaluator_state after cycle 3 (clean boundary): {loop.evaluator_state}")


if __name__ == "__main__":
    main()
