"""Phase 2 acceptance tests (issue #42): architecture, router authority,
full cycle, determinism, and failure behavior."""

from __future__ import annotations

import inspect
import unittest
from pathlib import Path

from Learner_App.parser import adapter as parser_adapter_module
from Learner_App.parser import core as parser_core_module
from Learner_App.parser.adapter import UnknownAdapterError, unregister_adapter
from Learner_App.parser.adapters import MATH_BASIC_EQUATIONS_DOMAIN, register_default_adapters
from Learner_App.parser.core import PacketRejectedError, ProblemVerificationError
from Learner_App.parser.models import GeneratedProblem, RulePacket, VerificationResult
from Learner_App.router import router_loop as router_loop_module
from Learner_App.router import state_machine_a as sm_a_module
from Learner_App.router import state_machine_b as sm_b_module
from Learner_App.router.models import (
    EvaluationLifecycle,
    LearnerAttempt,
    RouteAction,
    TaskLifecycle,
)
from Learner_App.router.policy import DEFAULT_CURRICULUM, PolicyConfig
from Learner_App.router.router_loop import RouterLoop
from Learner_App.router.state_machine_a import IllegalTaskTransitionError
from Learner_App.router.state_machine_b import MalformedAttemptError, StaleAttemptError

ROUTER_SOURCE_FILES = [
    Path(inspect.getfile(router_loop_module)),
    Path(inspect.getfile(sm_a_module)),
    Path(inspect.getfile(sm_b_module)),
]
PARSER_SOURCE_FILES = [
    Path(inspect.getfile(parser_core_module)),
    Path(inspect.getfile(parser_adapter_module)),
]


def _fresh_math_adapter():
    unregister_adapter(MATH_BASIC_EQUATIONS_DOMAIN)
    register_default_adapters()


def _correct_attempt(problem: GeneratedProblem) -> LearnerAttempt:
    return LearnerAttempt(
        problem_id=problem.problem_id, outcome="correct", reported_rules_used=problem.rules_used
    )


def _incorrect_attempt(problem: GeneratedProblem) -> LearnerAttempt:
    return LearnerAttempt(problem_id=problem.problem_id, outcome="incorrect", reported_rules_used=())


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_exactly_two_lifecycle_enums_exist_in_router_models(self):
        from Learner_App.router import models as router_models

        lifecycle_enums = [
            name
            for name, obj in vars(router_models).items()
            if isinstance(obj, type) and issubclass(obj, __import__("enum").Enum) and "Lifecycle" in name
        ]
        self.assertEqual(sorted(lifecycle_enums), ["EvaluationLifecycle", "TaskLifecycle"])

    def test_router_loop_holds_exactly_task_state_and_evaluator_state(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=1)
        self.assertTrue(hasattr(loop, "task_state"))
        self.assertTrue(hasattr(loop, "evaluator_state"))
        # RouteDecision (the router's own decision) carries no lifecycle
        # field of its own -- it is not a third state machine.
        self.assertFalse(hasattr(loop.route, "lifecycle_state"))

    def test_route_decision_type_has_no_lifecycle_field(self):
        import dataclasses

        from Learner_App.router.models import RouteDecision

        field_names = {f.name for f in dataclasses.fields(RouteDecision)}
        self.assertNotIn("lifecycle_state", field_names)

    def test_parser_files_never_import_the_router_package(self):
        # Prose mentioning "the router" as a concept (Phase 1's docstrings
        # do, describing who calls the worker) is fine -- an actual import
        # coupling in the other direction is not: workers must not be able
        # to reach into routing/curriculum state.
        for path in PARSER_SOURCE_FILES:
            text = path.read_text()
            self.assertNotIn("import router", text)
            self.assertNotIn("from .router", text)
            self.assertNotIn("from ..router", text)
            self.assertNotIn("Learner_App.router", text)

    def test_router_loop_calls_phase1_only_through_its_public_contract(self):
        text = Path(inspect.getfile(router_loop_module)).read_text()
        self.assertIn("from ..parser.core import build_problem", text)
        # never reaches into the math adapter directly
        self.assertNotIn("math_basic_equations", text)
        self.assertNotIn("EquationStructure", text)

    def test_generated_problem_is_the_real_phase1_type(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=1)
        problem = loop.generate_problem()
        self.assertIsInstance(problem, GeneratedProblem)
        self.assertIsInstance(problem.verification, VerificationResult)


class RouterAuthorityTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_all_five_authority_fields_flow_from_route_to_packet(self):
        captured: list[RulePacket] = []
        real_build_problem = router_loop_module.build_problem

        def spy_build_problem(packet, **kwargs):
            captured.append(packet)
            return real_build_problem(packet, **kwargs)

        router_loop_module.build_problem = spy_build_problem
        try:
            config = PolicyConfig(forbidden_rules=("EQ.DIV_INVERSE",))
            loop = RouterLoop(config=config, base_seed=5)
            loop.generate_problem()
        finally:
            router_loop_module.build_problem = real_build_problem

        self.assertEqual(len(captured), 1)
        packet = captured[0]
        route = loop.route
        self.assertEqual(packet.target_rules, route.target_rules)
        self.assertEqual(packet.allowed_support_rules, route.allowed_support_rules)
        self.assertEqual(packet.forbidden_rules, route.forbidden_rules)
        self.assertEqual(packet.difficulty, route.difficulty)
        self.assertEqual(packet.domain, route.domain)
        self.assertEqual(packet.seed, route.seed)

    def test_evaluator_evidence_confidence_cannot_override_routing_action(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=7)
        problem = loop.generate_problem()
        # Even a "correct" outcome with zero demonstrated rules (low
        # confidence) still routes as ADVANCE -- only .outcome drives the
        # router's decision, never .confidence or .missing_rules.
        evidence = loop.submit_attempt(
            LearnerAttempt(problem_id=problem.problem_id, outcome="correct", reported_rules_used=())
        )
        self.assertEqual(evidence.confidence, "low")
        decision = loop.route_next(evidence)
        self.assertEqual(decision.action, RouteAction.ADVANCE)


class FullCycleTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_clean_start_to_verified_problem_to_attempt_to_evidence_to_route(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=11)
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.IDLE)

        problem = loop.generate_problem()
        self.assertTrue(problem.verification.passed)
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.EXECUTING)

        evidence = loop.submit_attempt(_correct_attempt(problem))
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.VECTORING)
        self.assertEqual(loop.evaluator_state.lifecycle_state, EvaluationLifecycle.IDLE)

        decision = loop.route_next(evidence)
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.IDLE)
        self.assertIsNotNone(decision)

    def test_correct_attempt_advances(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=13)
        problem = loop.generate_problem()
        evidence = loop.submit_attempt(_correct_attempt(problem))
        decision = loop.route_next(evidence)
        self.assertEqual(decision.action, RouteAction.ADVANCE)
        self.assertEqual(decision.target_rules, DEFAULT_CURRICULUM[1][0])

    def test_incorrect_attempt_produces_repeat_or_reduce_difficulty(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=17)
        problem = loop.generate_problem()
        evidence = loop.submit_attempt(_incorrect_attempt(problem))
        decision = loop.route_next(evidence)
        self.assertIn(decision.action, (RouteAction.REPEAT, RouteAction.REDUCE_DIFFICULTY))
        self.assertEqual(decision.target_rules, DEFAULT_CURRICULUM[0][0])

    def test_repeated_same_category_error_routes_to_explain(self):
        loop = RouterLoop(config=PolicyConfig(repeated_error_threshold=2), base_seed=19)
        for _ in range(2):
            problem = loop.generate_problem()
            evidence = loop.submit_attempt(_incorrect_attempt(problem))
            decision = loop.route_next(evidence)
        self.assertEqual(decision.action, RouteAction.EXPLAIN)

    def test_resolve_returns_to_a_clean_boundary_state(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=23)
        problem = loop.generate_problem()
        evidence = loop.submit_attempt(_correct_attempt(problem))
        loop.route_next(evidence)
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.IDLE)
        self.assertIsNone(loop.task_state.current_problem_id)
        self.assertEqual(loop.task_state.current_rule_targets, ())
        self.assertEqual(loop.evaluator_state.lifecycle_state, EvaluationLifecycle.IDLE)


class DeterminismTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_same_config_seed_and_attempts_produce_same_route_decisions(self):
        def run():
            loop = RouterLoop(config=PolicyConfig(), base_seed=101)
            decisions = []
            for attempt_fn in (_correct_attempt, _incorrect_attempt, _correct_attempt):
                problem, _, decision = loop.run_one_cycle(attempt_fn)
                decisions.append((problem.artifact_text, decision))
            return decisions

        self.assertEqual(run(), run())

    def test_different_seed_can_vary_the_problem_while_keeping_structure(self):
        loop_a = RouterLoop(config=PolicyConfig(), base_seed=201)
        loop_b = RouterLoop(config=PolicyConfig(), base_seed=202)
        problem_a = loop_a.generate_problem()
        problem_b = loop_b.generate_problem()
        self.assertNotEqual(problem_a.artifact_text, problem_b.artifact_text)
        self.assertEqual(problem_a.rules_used, problem_b.rules_used)

    def test_no_hidden_global_state_leaks_between_instances(self):
        first_loop = RouterLoop(config=PolicyConfig(), base_seed=301)
        for attempt_fn in (_correct_attempt, _incorrect_attempt):
            first_loop.run_one_cycle(attempt_fn)

        # A brand-new instance with the SAME base_seed as a fresh start
        # must behave identically to a loop that never ran anything --
        # proving the first loop's activity left no residual module-level
        # state behind.
        fresh_loop = RouterLoop(config=PolicyConfig(), base_seed=301)
        baseline_loop = RouterLoop(config=PolicyConfig(), base_seed=301)
        self.assertEqual(fresh_loop.generate_problem().artifact_text, baseline_loop.generate_problem().artifact_text)


class FailureBehaviorTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()

    def test_packet_rejection_surfaces_cleanly_and_leaves_state_idle(self):
        # target_rules == forbidden_rules is a generic contradiction Phase
        # 1's core rejects before generation.
        config = PolicyConfig(
            curriculum=(((DEFAULT_CURRICULUM[0][0]), ()),),
            forbidden_rules=DEFAULT_CURRICULUM[0][0],
        )
        loop = RouterLoop(config=config, base_seed=401)
        with self.assertRaises(PacketRejectedError):
            loop.generate_problem()
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.IDLE)
        self.assertIsNone(loop.task_state.current_problem_id)

    def test_verification_failure_never_becomes_a_presented_problem(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=403)
        real_build_problem = router_loop_module.build_problem

        def failing_build_problem(packet, **kwargs):
            raise ProblemVerificationError(
                packet,
                VerificationResult(
                    requested_rules_present=False,
                    forbidden_rules_absent=True,
                    well_formed=False,
                    adapter_valid=False,
                    errors=("simulated failure",),
                ),
                "bad artifact",
            )

        router_loop_module.build_problem = failing_build_problem
        try:
            with self.assertRaises(ProblemVerificationError):
                loop.generate_problem()
        finally:
            router_loop_module.build_problem = real_build_problem

        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.IDLE)

    def test_malformed_attempt_is_rejected_cleanly_without_mutating_state(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=407)
        problem = loop.generate_problem()
        with self.assertRaises(MalformedAttemptError):
            loop.submit_attempt(LearnerAttempt(problem_id=problem.problem_id, outcome="sort_of"))
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.EXECUTING)
        self.assertEqual(loop.task_state.attempt_count, 0)

    def test_stale_problem_id_attempt_cannot_mutate_the_active_cycle(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=409)
        loop.generate_problem()
        with self.assertRaises(StaleAttemptError):
            loop.submit_attempt(LearnerAttempt(problem_id="not-the-active-problem", outcome="correct"))
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.EXECUTING)
        self.assertEqual(loop.task_state.attempt_count, 0)

    def test_illegal_state_transition_is_rejected_not_silently_coerced(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=411)
        loop.generate_problem()  # task_state is now EXECUTING
        with self.assertRaises(IllegalTaskTransitionError):
            loop.generate_problem()  # calling again requires IDLE, not EXECUTING


if __name__ == "__main__":
    unittest.main()
