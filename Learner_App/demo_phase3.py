#!/usr/bin/env python3
"""Headless demonstration of Phase 3's six-step recursive recall.

Run from the repository root:

    python3 -m Learner_App.demo_phase3

Extends the Phase 2 RouterLoop (unchanged) with recall tracking: as the
curriculum advances, mastered rules enter a six-step recall schedule.
When an older rule comes due, the router folds it into the next problem
alongside whatever the curriculum is currently teaching -- when that
combination is feasible; otherwise it skips cleanly and tries again once
the combination (or a later cycle) allows it. A rule that completes all
six forward steps and has a real configured inverse gets that inverse
scheduled for reverse-direction recall.

Uses a small demo-only curriculum (ADD only -> MUL only, then MUL forever)
and shortened gaps so the six-step journey completes in a legible number
of cycles -- production configuration would use policy.DEFAULT_CURRICULUM
and router.recall.models.RecallConfig()'s real gaps. No UI, no LLM/network;
running this script twice produces byte-identical output.
"""

from __future__ import annotations

from Learner_App.parser.adapter import registered_domains
from Learner_App.parser.adapters import register_default_adapters
from Learner_App.parser.adapters.math_basic_equations import EQ_ADD_INVERSE, EQ_MUL_INVERSE
from Learner_App.router import LearnerAttempt, PolicyConfig, RouterLoop
from Learner_App.recall import RecallConfig

DEMO_CURRICULUM = (
    ((EQ_ADD_INVERSE,), ()),
    ((EQ_MUL_INVERSE,), ()),
)
FAST_RECALL_CONFIG = RecallConfig(gaps_by_step=(1, 1, 1, 1, 1, 1))


def _print_recall_state(loop: RouterLoop) -> None:
    for rule_id in sorted(loop.recall_records):
        r = loop.recall_records[rule_id]
        print(
            f"      recall[{rule_id}]: step={r.current_recall_step} direction={r.direction} "
            f"next_due={r.next_due_cycle} success_streak={r.success_streak} "
            f"error_streak={r.error_streak} times_seen={r.times_seen}"
        )


def main() -> None:
    if not registered_domains():
        register_default_adapters()

    config = PolicyConfig(curriculum=DEMO_CURRICULUM)
    loop = RouterLoop(config=config, base_seed=7000, recall_config=FAST_RECALL_CONFIG)

    print("Phase 3 deterministic recall demo (base_seed=7000, fast demo gaps)")

    # Cycle 1: miss this attempt on purpose is not useful before a rule is
    # even learned -- so cycle 1 always succeeds (first learning).
    def full_correct(problem):
        return LearnerAttempt(
            problem_id=problem.problem_id, outcome="correct", reported_rules_used=problem.rules_used
        )

    def miss(problem):
        return LearnerAttempt(problem_id=problem.problem_id, outcome="incorrect", reported_rules_used=())

    # Cycle 5 (arbitrary, mid-run) is a deliberate miss to demonstrate a
    # recall step retreating; every other cycle succeeds.
    MISS_ON_CYCLE = 5

    for cycle_number in range(1, 41):
        attempt_fn = miss if cycle_number == MISS_ON_CYCLE else full_correct
        problem, evidence, decision = loop.run_one_cycle(attempt_fn)
        print(f"\n--- cycle {cycle_number} ({'MISS' if attempt_fn is miss else 'correct'}) ---")
        print(f"    generated: {problem.artifact_text!r}  rules_used={problem.rules_used}")
        print(f"    evidence: outcome={evidence.outcome!r} missing_rules={evidence.missing_rules}")
        print(
            f"    next route: action={decision.action.value} target_rules={decision.target_rules} "
            f"recall_injected={decision.recall_injected_rule_id!r}"
        )
        _print_recall_state(loop)

        reverse_rule_ids = {
            r.rule_id for r in loop.recall_records.values() if r.direction == "reverse"
        }
        if decision.recall_injected_rule_id in reverse_rule_ids:
            # Some reverse-scheduled rule has now actually been served in
            # a real generated problem -- the demo has covered every
            # required stage (initial learning, spacing farther, a miss
            # moving closer, combination with a newer rule, and reverse
            # recall). Stop rather than padding output further.
            break

    print(f"\ntask_state (clean boundary): {loop.task_state.lifecycle_state}")
    print(f"evaluator_state (clean boundary): {loop.evaluator_state.lifecycle_state}")

    # Snapshot / restore round-trip: same future decisions either way.
    snap = loop.recall_snapshot()
    restored = {}
    from Learner_App.recall import restore as recall_restore

    restored = recall_restore(snap)
    print(f"\nrecall_snapshot() round-trips through restore(): {restored == loop.recall_records}")


if __name__ == "__main__":
    main()
