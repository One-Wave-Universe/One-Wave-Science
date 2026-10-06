"""Phase 3 acceptance tests (issue #45): architecture, router authority,
six-step recall, embedding/compounding, evidence boundary, determinism,
and failure behavior -- exercised through the Phase 2 RouterLoop extended
with recall tracking."""

from __future__ import annotations

import inspect
import unittest
from pathlib import Path

from Learner_App.parser.adapter import unregister_adapter
from Learner_App.parser.adapters import MATH_BASIC_EQUATIONS_DOMAIN, register_default_adapters
from Learner_App.parser.adapters.math_basic_equations import (
    EQ_ADD_INVERSE,
    EQ_DIV_INVERSE,
    EQ_IDENTITY,
    EQ_MUL_INVERSE,
    EQ_SUB_INVERSE,
)
from Learner_App.recall import worker as recall_worker
from Learner_App.recall.models import (
    DIRECTION_FORWARD,
    DIRECTION_REVERSE,
    MAX_RECALL_STEP,
    MalformedRecallRecordError,
    RecallConfig,
    UnknownRuleError,
)
from Learner_App.router import recall_integration
from Learner_App.router.models import LearnerAttempt
from Learner_App.router.policy import PolicyConfig
from Learner_App.router.router_loop import RouterLoop

RECALL_SOURCE_FILES = [
    Path(inspect.getfile(recall_worker)),
    Path(recall_worker.__file__).with_name("models.py"),
]

FAST_CONFIG = RecallConfig(gaps_by_step=(1, 1, 1, 1, 1, 1))

# A curriculum that never combines ADD+MUL on its own, so recall injection
# is the only way they ever appear together -- makes the "combined
# preferred / infeasible fallback" behavior directly observable.
SEPARATE_CURRICULUM = (
    ((EQ_ADD_INVERSE,), ()),
    ((EQ_MUL_INVERSE,), ()),
)


def _fresh_math_adapter():
    unregister_adapter(MATH_BASIC_EQUATIONS_DOMAIN)
    register_default_adapters()


def _correct(problem):
    return LearnerAttempt(
        problem_id=problem.problem_id, outcome="correct", reported_rules_used=problem.rules_used
    )


def _incorrect(problem):
    return LearnerAttempt(problem_id=problem.problem_id, outcome="incorrect", reported_rules_used=())


def _partial(missing_rule_id):
    def attempt(problem):
        demonstrated = tuple(r for r in problem.rules_used if r != missing_rule_id)
        return LearnerAttempt(
            problem_id=problem.problem_id, outcome="incorrect", reported_rules_used=demonstrated
        )

    return attempt


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_still_exactly_two_lifecycle_enums(self):
        from Learner_App.router import models as router_models
        import enum

        lifecycle_enums = [
            name
            for name, obj in vars(router_models).items()
            if isinstance(obj, type) and issubclass(obj, enum.Enum) and "Lifecycle" in name
        ]
        self.assertEqual(sorted(lifecycle_enums), ["EvaluationLifecycle", "TaskLifecycle"])

    def test_recall_worker_defines_no_lifecycle_class(self):
        for path in RECALL_SOURCE_FILES:
            self.assertNotIn("Lifecycle", path.read_text())

    def test_recall_worker_never_imports_router_package(self):
        for path in RECALL_SOURCE_FILES:
            text = path.read_text()
            self.assertNotIn("from ..router", text)
            self.assertNotIn("from .router", text)
            self.assertNotIn("Learner_App.router", text)

    def test_recall_worker_never_imports_parser_package(self):
        # The worker is domain-agnostic: it never needs to know about
        # RulePacket/adapters/build_problem.
        for path in RECALL_SOURCE_FILES:
            text = path.read_text()
            self.assertNotIn("parser", text)

    def test_parser_still_never_imports_router_or_recall(self):
        from Learner_App.parser import adapter as parser_adapter_module
        from Learner_App.parser import core as parser_core_module

        for path in (
            Path(inspect.getfile(parser_core_module)),
            Path(inspect.getfile(parser_adapter_module)),
        ):
            text = path.read_text()
            self.assertNotIn("Learner_App.router", text)
            self.assertNotIn("Learner_App.recall", text)


class RouterAuthorityTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_recall_worker_functions_return_only_records_or_facts(self):
        # due_rules/is_due/overdue_amount/ready_for_reverse are the
        # worker's whole public surface for "what should happen next" --
        # none of them return anything resembling a routing decision.
        import Learner_App.recall as recall_pkg

        forbidden_names = {"RouteDecision", "RouteAction", "RulePacket"}
        self.assertFalse(forbidden_names & set(dir(recall_pkg)))

    def test_router_not_worker_picks_which_due_rule_to_inject(self):
        # Two rules both due; the worker just reports them in priority
        # order (due_rules()) -- inject_due_recall (router-side) is what
        # actually walks that list and decides, trying the next candidate
        # when the top one is infeasible. Prove the worker's list alone
        # doesn't determine the outcome by handing inject_due_recall a
        # deliberately reordered list and confirming it still picks
        # whichever is feasible, not just "the first one handed to it
        # blindly" -- i.e. it makes its own feasibility judgment call.
        route = PolicyConfig().curriculum
        from Learner_App.router.models import RouteAction, RouteDecision

        base = RouteDecision(
            action=RouteAction.ADVANCE,
            target_rules=(EQ_MUL_INVERSE,),
            allowed_support_rules=(),
            forbidden_rules=(),
            difficulty=1,
            domain=MATH_BASIC_EQUATIONS_DOMAIN,
            seed=1,
            reason_code="test",
        )
        # DIV_INVERSE first (infeasible with MUL alone), ADD_INVERSE second
        # (feasible) -- router must fall through to ADD_INVERSE.
        result = recall_integration.inject_due_recall(base, (EQ_DIV_INVERSE, EQ_ADD_INVERSE))
        self.assertEqual(result.recall_injected_rule_id, EQ_ADD_INVERSE)


class SixStepRecallTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_newly_learned_rule_starts_at_first_recall_stage(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=100, recall_config=FAST_CONFIG)
        loop.run_one_cycle(_correct)
        record = loop.recall_records[EQ_ADD_INVERSE]
        self.assertEqual(record.current_recall_step, 1)
        self.assertEqual(record.direction, DIRECTION_FORWARD)

    def test_success_advances_recall_step(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=101, recall_config=FAST_CONFIG
        )
        loop.run_one_cycle(_correct)  # learns ADD
        loop.run_one_cycle(_correct)  # learns MUL, may inject ADD
        step_before = loop.recall_records[EQ_ADD_INVERSE].current_recall_step
        # Keep cycling until ADD gets recalled again.
        for _ in range(10):
            if loop.recall_records[EQ_ADD_INVERSE].current_recall_step > step_before:
                break
            loop.run_one_cycle(_correct)
        self.assertGreater(loop.recall_records[EQ_ADD_INVERSE].current_recall_step, step_before)

    def test_miss_retreats_recall_step(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=102, recall_config=FAST_CONFIG
        )
        loop.run_one_cycle(_correct)  # learn ADD (step 1)
        loop.run_one_cycle(_correct)  # learn MUL; ADD due -> injected, target=(MUL, ADD)
        loop.run_one_cycle(_correct)  # ADD demonstrated again -> advances to step 2+
        step_before = loop.recall_records[EQ_ADD_INVERSE].current_recall_step
        self.assertGreater(step_before, 1)

        # Get ADD back into the active target set, then deliberately miss
        # it specifically (MUL still demonstrated).
        for _ in range(10):
            if EQ_ADD_INVERSE in loop.route.target_rules:
                break
            loop.run_one_cycle(_correct)
        self.assertIn(EQ_ADD_INVERSE, loop.route.target_rules)

        loop.run_one_cycle(_partial(EQ_ADD_INVERSE))
        record = loop.recall_records[EQ_ADD_INVERSE]
        self.assertLess(record.current_recall_step, step_before)
        self.assertEqual(record.error_streak, 1)
        self.assertEqual(record.success_streak, 0)

    def test_step_bounds_never_violated_through_many_cycles(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=103, recall_config=FAST_CONFIG
        )
        for i in range(60):
            attempt_fn = _incorrect if i % 5 == 0 else _correct
            loop.run_one_cycle(attempt_fn)
        for record in loop.recall_records.values():
            self.assertGreaterEqual(record.current_recall_step, 1)
            self.assertLessEqual(record.current_recall_step, MAX_RECALL_STEP)

    def test_stage_six_schedules_reverse_only_with_real_inverse(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=104, recall_config=FAST_CONFIG
        )
        for _ in range(40):
            loop.run_one_cycle(_correct)
            if EQ_SUB_INVERSE in loop.recall_records or EQ_DIV_INVERSE in loop.recall_records:
                break
        reverse_records = [r for r in loop.recall_records.values() if r.direction == DIRECTION_REVERSE]
        self.assertTrue(reverse_records)
        for r in reverse_records:
            self.assertIn(r.rule_id, (EQ_SUB_INVERSE, EQ_DIV_INVERSE))

    def test_rule_without_inverse_never_gets_reverse_scheduled(self):
        # EQ_IDENTITY has no configured inverse -- even if it reached
        # step 6, no reverse record should ever appear for it.
        loop = RouterLoop(config=PolicyConfig(), base_seed=105, recall_config=FAST_CONFIG)
        record = recall_worker.learn_rule(EQ_IDENTITY, cycle=0, config=FAST_CONFIG)
        for cycle in range(1, 20):
            record = recall_worker.record_success(record, cycle=cycle, config=FAST_CONFIG)
        self.assertEqual(record.current_recall_step, MAX_RECALL_STEP)
        self.assertIsNone(recall_worker.ready_for_reverse(record, inverses=loop.recall_inverses))


class EmbeddingCompoundingTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_due_old_rule_injected_alongside_new_target(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=200, recall_config=FAST_CONFIG
        )
        loop.run_one_cycle(_correct)  # learn ADD
        _, _, decision = loop.run_one_cycle(_correct)  # learn MUL; ADD due -> inject
        self.assertEqual(decision.recall_injected_rule_id, EQ_ADD_INVERSE)
        self.assertIn(EQ_ADD_INVERSE, decision.target_rules)
        self.assertIn(EQ_MUL_INVERSE, decision.target_rules)

    def test_generated_combined_problem_is_phase1_verified(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=201, recall_config=FAST_CONFIG
        )
        loop.run_one_cycle(_correct)
        loop.run_one_cycle(_correct)
        problem = loop.generate_problem()
        self.assertTrue(problem.verification.passed)
        self.assertEqual(set(problem.rules_requested), {EQ_ADD_INVERSE, EQ_MUL_INVERSE})

    def test_infeasible_combination_falls_back_cleanly(self):
        # MUL_INVERSE + DIV_INVERSE is never a supported Phase 1 combo.
        loop = RouterLoop(config=PolicyConfig(), base_seed=202, recall_config=FAST_CONFIG)
        route = loop.route
        from Learner_App.router.models import RouteDecision

        base = RouteDecision(
            action=route.action,
            target_rules=(EQ_MUL_INVERSE,),
            allowed_support_rules=(),
            forbidden_rules=(),
            difficulty=1,
            domain=MATH_BASIC_EQUATIONS_DOMAIN,
            seed=1,
            reason_code="test",
        )
        result = recall_integration.inject_due_recall(base, (EQ_DIV_INVERSE,))
        self.assertIsNone(result.recall_injected_rule_id)
        self.assertEqual(result.target_rules, (EQ_MUL_INVERSE,))  # unchanged, not forced

    def test_forbidden_rule_never_injected_even_if_due(self):
        from Learner_App.router.models import RouteDecision, RouteAction

        base = RouteDecision(
            action=RouteAction.ADVANCE,
            target_rules=(EQ_MUL_INVERSE,),
            allowed_support_rules=(),
            forbidden_rules=(EQ_ADD_INVERSE,),
            difficulty=1,
            domain=MATH_BASIC_EQUATIONS_DOMAIN,
            seed=1,
            reason_code="test",
        )
        result = recall_integration.inject_due_recall(base, (EQ_ADD_INVERSE,))
        self.assertIsNone(result.recall_injected_rule_id)
        self.assertNotIn(EQ_ADD_INVERSE, result.target_rules)


class EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_recall_state_unchanged_until_route_next_consumes_evidence(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=300, recall_config=FAST_CONFIG)
        problem = loop.generate_problem()
        before = dict(loop.recall_records)
        loop.submit_attempt(_correct(problem))
        self.assertEqual(loop.recall_records, before)  # not yet updated
        loop.route_next()
        self.assertNotEqual(loop.recall_records, before)  # updated only now

    def test_forged_evidence_cannot_reach_recall_update(self):
        # route_next() takes no evidence argument at all (Phase 2), so
        # there is no way to hand it forged evidence to update recall
        # state with in the first place.
        loop = RouterLoop(config=PolicyConfig(), base_seed=301, recall_config=FAST_CONFIG)
        problem = loop.generate_problem()
        loop.submit_attempt(_correct(problem))
        with self.assertRaises(TypeError):
            loop.route_next(object())  # type: ignore[call-arg]

    def test_stale_evidence_cannot_update_recall_state(self):
        import dataclasses

        loop = RouterLoop(config=PolicyConfig(), base_seed=302, recall_config=FAST_CONFIG)
        problem = loop.generate_problem()
        evidence = loop.submit_attempt(_correct(problem))
        tampered = dataclasses.replace(evidence, problem_id="fabricated")
        loop.evaluator_state = dataclasses.replace(loop.evaluator_state, last_evidence=tampered)
        before = dict(loop.recall_records)
        with self.assertRaises(Exception):
            loop.route_next()
        self.assertEqual(loop.recall_records, before)

    def test_correct_outcome_with_missing_rule_does_not_advance_that_rules_recall(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=303, recall_config=FAST_CONFIG
        )
        loop.run_one_cycle(_correct)  # learn ADD
        loop.run_one_cycle(_correct)  # learn MUL; ADD injected -> target=(MUL, ADD)
        self.assertIn(EQ_ADD_INVERSE, loop.route.target_rules)
        add_step_before = loop.recall_records[EQ_ADD_INVERSE].current_recall_step
        # Demonstrate MUL but not ADD this cycle.
        loop.run_one_cycle(_partial(EQ_ADD_INVERSE))
        add_record = loop.recall_records[EQ_ADD_INVERSE]
        self.assertLessEqual(add_record.current_recall_step, add_step_before)
        self.assertEqual(add_record.error_streak, 1)

    def test_ambiguous_multi_rule_evidence_updates_each_rule_independently(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=304, recall_config=FAST_CONFIG
        )
        loop.run_one_cycle(_correct)
        loop.run_one_cycle(_correct)  # target now includes ADD (injected) + MUL
        self.assertEqual(set(loop.route.target_rules), {EQ_ADD_INVERSE, EQ_MUL_INVERSE})
        loop.run_one_cycle(_partial(EQ_MUL_INVERSE))  # ADD demonstrated, MUL missing
        self.assertEqual(loop.recall_records[EQ_ADD_INVERSE].error_streak, 0)
        self.assertEqual(loop.recall_records[EQ_MUL_INVERSE].error_streak, 1)


class DeterminismTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_same_config_seed_and_attempts_produce_same_recall_state(self):
        def run():
            loop = RouterLoop(
                config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=400, recall_config=FAST_CONFIG
            )
            for i in range(15):
                loop.run_one_cycle(_incorrect if i == 5 else _correct)
            return recall_worker.snapshot(loop.recall_records)

        self.assertEqual(run(), run())

    def test_no_hidden_global_recall_state_leaks_between_instances(self):
        first = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=401, recall_config=FAST_CONFIG
        )
        for _ in range(10):
            first.run_one_cycle(_correct)

        fresh = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=401, recall_config=FAST_CONFIG
        )
        baseline = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=401, recall_config=FAST_CONFIG
        )
        self.assertEqual(fresh.recall_records, baseline.recall_records)  # both empty, unaffected by `first`

    def test_snapshot_restore_round_trip_gives_identical_future_decisions(self):
        loop = RouterLoop(
            config=PolicyConfig(curriculum=SEPARATE_CURRICULUM), base_seed=402, recall_config=FAST_CONFIG
        )
        for _ in range(6):
            loop.run_one_cycle(_correct)

        snap = loop.recall_snapshot()
        due_before = recall_worker.due_rules(loop.recall_records, cycle=loop.cycle_count + 5)

        restored_records = recall_worker.restore(snap)
        due_after = recall_worker.due_rules(restored_records, cycle=loop.cycle_count + 5)

        self.assertEqual(due_before, due_after)


class FailureBehaviorTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_malformed_recall_record_rejected_on_restore(self):
        with self.assertRaises(MalformedRecallRecordError):
            RouterLoop(config=PolicyConfig(), base_seed=500).restore_recall(
                [{"rule_id": "X", "current_recall_step": 999}]
            )

    def test_unknown_rule_id_cannot_be_scheduled_silently(self):
        with self.assertRaises(UnknownRuleError):
            recall_integration.schedule_learned_rule(
                "NOT.A.REAL.RULE", cycle=1, config=FAST_CONFIG, known_rules=frozenset({EQ_ADD_INVERSE})
            )

    def test_impossible_inverse_mapping_rejected_cleanly(self):
        from Learner_App.recall.models import InvalidInverseMappingError

        with self.assertRaises(InvalidInverseMappingError):
            recall_worker.require_inverse_rule_id(EQ_IDENTITY, inverses=recall_integration.RULE_INVERSES)

    def test_impossible_combination_falls_back_without_corrupting_recall_state(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=501, recall_config=FAST_CONFIG)
        loop.recall_records[EQ_DIV_INVERSE] = recall_worker.learn_rule(
            EQ_DIV_INVERSE, cycle=0, config=FAST_CONFIG
        )
        before = dict(loop.recall_records)
        route = loop.route
        from Learner_App.router.models import RouteDecision

        mul_only = RouteDecision(
            action=route.action,
            target_rules=(EQ_MUL_INVERSE,),
            allowed_support_rules=(),
            forbidden_rules=(),
            difficulty=1,
            domain=MATH_BASIC_EQUATIONS_DOMAIN,
            seed=1,
            reason_code="test",
        )
        recall_integration.inject_due_recall(mul_only, (EQ_DIV_INVERSE,))
        self.assertEqual(loop.recall_records, before)  # inject_due_recall never touches loop state directly

    def test_recall_update_failure_does_not_partially_mutate_state(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=502, recall_config=FAST_CONFIG)
        problem = loop.generate_problem()
        loop.submit_attempt(_correct(problem))
        before = dict(loop.recall_records)
        # Force schedule_learned_rule to fail for this cycle's rule by
        # shrinking the known-rules universe after construction.
        loop._known_recall_rule_ids = frozenset()
        with self.assertRaises(UnknownRuleError):
            loop.route_next()
        self.assertEqual(loop.recall_records, before)


if __name__ == "__main__":
    unittest.main()
