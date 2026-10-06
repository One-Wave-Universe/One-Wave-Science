"""Phase 4 acceptance tests (issue #47): architecture, rule format,
triggering, no-answer-leakage, determinism, and failure behavior --
exercised through the Phase 2/3 RouterLoop extended with Coach Worker
integration."""

from __future__ import annotations

import inspect
import unittest
from pathlib import Path

from Learner_App.coach import models as coach_models_module
from Learner_App.coach import worker as coach_worker_module
from Learner_App.coach.fixtures.math_basic_equations import (
    CONCEPT_INVERSE_OPERATION,
    EQ_ADD_INVERSE,
    EQ_DIV_INVERSE,
    EQ_MUL_INVERSE,
    register_default_explanations,
)
from Learner_App.coach.models import (
    TRIGGER_EXPLICIT_REQUEST,
    TRIGGER_REPEATED_ERROR,
    AnswerLeakError,
    RuleExplanation,
    UnknownRuleError,
)
from Learner_App.coach.registry import register_rule_explanation, unregister_rule_explanation
from Learner_App.parser.adapter import unregister_adapter
from Learner_App.parser.adapters import MATH_BASIC_EQUATIONS_DOMAIN, register_default_adapters
from Learner_App.router.coach_integration import CoachRequest
from Learner_App.router.models import LearnerAttempt, RouteAction
from Learner_App.router.policy import PolicyConfig
from Learner_App.router.router_loop import NoCoachRequestPendingError, RouterLoop

COACH_SOURCE_FILES = [
    Path(inspect.getfile(coach_worker_module)),
    Path(coach_worker_module.__file__).with_name("models.py"),
    Path(coach_worker_module.__file__).with_name("registry.py"),
]

ALL_FIXTURE_IDS = (
    "EQ.CONCEPT.COEFFICIENT",
    "EQ.CONCEPT.WHOLE_EQUATION_SCALING",
    CONCEPT_INVERSE_OPERATION,
    "EQ.IDENTITY",
    EQ_ADD_INVERSE,
    "EQ.SUB_INVERSE",
    EQ_MUL_INVERSE,
    EQ_DIV_INVERSE,
)


def _fresh_math_adapter():
    unregister_adapter(MATH_BASIC_EQUATIONS_DOMAIN)
    register_default_adapters()


def _fresh_coach_fixtures():
    for rule_id in ALL_FIXTURE_IDS:
        unregister_rule_explanation(rule_id)
    register_default_explanations()


def _correct(problem):
    return LearnerAttempt(
        problem_id=problem.problem_id, outcome="correct", reported_rules_used=problem.rules_used
    )


def _incorrect(problem):
    return LearnerAttempt(problem_id=problem.problem_id, outcome="incorrect", reported_rules_used=())


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()
        _fresh_coach_fixtures()

    def test_still_exactly_two_lifecycle_enums(self):
        import enum

        from Learner_App.router import models as router_models

        lifecycle_enums = [
            name
            for name, obj in vars(router_models).items()
            if isinstance(obj, type) and issubclass(obj, enum.Enum) and "Lifecycle" in name
        ]
        self.assertEqual(sorted(lifecycle_enums), ["EvaluationLifecycle", "TaskLifecycle"])

    def test_coach_defines_no_lifecycle_class(self):
        import enum

        lifecycle_classes = [
            name
            for name, obj in vars(coach_models_module).items()
            if isinstance(obj, type) and issubclass(obj, enum.Enum)
        ]
        self.assertEqual(lifecycle_classes, [])

    def test_coach_never_imports_router_package(self):
        for path in COACH_SOURCE_FILES:
            text = path.read_text()
            self.assertNotIn("from ..router", text)
            self.assertNotIn("Learner_App.router", text)

    def test_coach_never_imports_parser_package(self):
        for path in COACH_SOURCE_FILES:
            text = path.read_text()
            self.assertNotIn("from ..parser", text)
            self.assertNotIn("Learner_App.parser", text)

    def test_coach_worker_functions_return_only_facts_never_a_route_decision(self):
        from Learner_App.router.models import RouteDecision

        loop = RouterLoop(config=PolicyConfig(repeated_error_threshold=2), base_seed=1)
        problem = loop.generate_problem()
        loop.submit_attempt(_correct(problem))
        loop.request_explanation(EQ_ADD_INVERSE)
        explanation = loop.explain()
        self.assertIsInstance(explanation, RuleExplanation)
        self.assertNotIsInstance(explanation, RouteDecision)

    def test_coach_cannot_mutate_recall_state(self):
        loop = RouterLoop(config=PolicyConfig(repeated_error_threshold=2), base_seed=2)
        problem = loop.generate_problem()
        loop.submit_attempt(_correct(problem))
        before = dict(loop.recall_records)
        loop.request_explanation(EQ_ADD_INVERSE)
        loop.explain()
        self.assertEqual(loop.recall_records, before)

    def test_coach_cannot_mutate_task_or_evaluator_state(self):
        loop = RouterLoop(config=PolicyConfig(repeated_error_threshold=2), base_seed=3)
        problem = loop.generate_problem()
        task_before = loop.task_state
        evaluator_before = loop.evaluator_state
        loop.request_explanation(EQ_ADD_INVERSE)
        loop.explain()
        self.assertEqual(loop.task_state, task_before)
        self.assertEqual(loop.evaluator_state, evaluator_before)


class RuleFormatTests(unittest.TestCase):
    def setUp(self):
        _fresh_coach_fixtures()
        self.addCleanup(lambda: [unregister_rule_explanation(r) for r in ALL_FIXTURE_IDS])

    def test_every_registered_rule_produces_full_card(self):
        for rule_id in ALL_FIXTURE_IDS:
            explanation = coach_worker_module.explain_rule(rule_id)
            self.assertTrue(explanation.if_text)
            self.assertTrue(explanation.then_text)
            self.assertTrue(explanation.why_text)
            self.assertTrue(explanation.only_when_text)
            self.assertTrue(explanation.do_not_use_when_text)

    def test_prerequisite_links_are_deterministic_and_inspectable(self):
        explanation = coach_worker_module.explain_rule(EQ_ADD_INVERSE)
        self.assertEqual(explanation.prerequisites, (CONCEPT_INVERSE_OPERATION,))


class TriggeringTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()
        _fresh_coach_fixtures()

    def test_repeated_same_category_error_produces_pending_coach_request(self):
        loop = RouterLoop(
            config=PolicyConfig(repeated_error_threshold=2),
            base_seed=11,
            coach_prerequisite_first=False,
        )
        decision = None
        for _ in range(2):
            problem = loop.generate_problem()
            loop.submit_attempt(_incorrect(problem))
            decision = loop.route_next()
        self.assertEqual(decision.action, RouteAction.EXPLAIN)
        self.assertIsNotNone(loop.pending_coach_request)
        self.assertEqual(loop.pending_coach_request.rule_id, EQ_ADD_INVERSE)
        self.assertEqual(loop.pending_coach_request.trigger_reason, TRIGGER_REPEATED_ERROR)

    def test_correct_attempt_never_produces_pending_coach_request(self):
        loop = RouterLoop(config=PolicyConfig(repeated_error_threshold=2), base_seed=12)
        problem = loop.generate_problem()
        loop.submit_attempt(_correct(problem))
        loop.route_next()
        self.assertIsNone(loop.pending_coach_request)

    def test_explicit_request_does_not_grade_the_in_progress_attempt(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=13)
        problem = loop.generate_problem()
        from Learner_App.router.models import TaskLifecycle

        task_before = loop.task_state
        request = loop.request_explanation()
        self.assertEqual(request.trigger_reason, TRIGGER_EXPLICIT_REQUEST)
        self.assertEqual(loop.task_state, task_before)
        self.assertEqual(loop.task_state.lifecycle_state, TaskLifecycle.EXECUTING)

    def test_explicit_request_defaults_to_current_target_rule(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=14)
        loop.generate_problem()
        request = loop.request_explanation()
        self.assertEqual(request.rule_id, loop.route.target_rules[0])

    def test_prerequisite_first_redirects_when_configured(self):
        loop = RouterLoop(
            config=PolicyConfig(), base_seed=15, coach_prerequisite_first=True
        )
        loop.generate_problem()
        loop.request_explanation(EQ_ADD_INVERSE)
        explanation = loop.explain()
        self.assertEqual(explanation.rule_id, CONCEPT_INVERSE_OPERATION)

    def test_prerequisite_first_disabled_explains_rule_directly(self):
        loop = RouterLoop(
            config=PolicyConfig(), base_seed=16, coach_prerequisite_first=False
        )
        loop.generate_problem()
        loop.request_explanation(EQ_ADD_INVERSE)
        explanation = loop.explain()
        self.assertEqual(explanation.rule_id, EQ_ADD_INVERSE)

    def test_already_explained_prerequisite_is_not_repeated(self):
        loop = RouterLoop(
            config=PolicyConfig(), base_seed=17, coach_prerequisite_first=True
        )
        loop.generate_problem()
        loop.request_explanation(EQ_ADD_INVERSE)
        first = loop.explain()
        self.assertEqual(first.rule_id, CONCEPT_INVERSE_OPERATION)

        loop.request_explanation(EQ_ADD_INVERSE)
        second = loop.explain()
        self.assertEqual(second.rule_id, EQ_ADD_INVERSE)

    def test_coach_completion_returns_control_to_router(self):
        loop = RouterLoop(
            config=PolicyConfig(), base_seed=18, coach_prerequisite_first=False
        )
        loop.generate_problem()
        loop.request_explanation(EQ_ADD_INVERSE)
        self.assertIsNotNone(loop.pending_coach_request)
        loop.explain()
        self.assertIsNone(loop.pending_coach_request)


class ReferenceLinkTests(unittest.TestCase):
    """problem.rules_used[] -> rule explanation record(s) (issue #47's
    "Reference-link behavior")."""

    def setUp(self):
        _fresh_math_adapter()
        _fresh_coach_fixtures()

    def test_problem_rules_used_resolve_to_explanations(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=51)
        problem = loop.generate_problem()
        explanations = loop.rule_explanations_for(problem)
        self.assertEqual(
            {e.rule_id for e in explanations}, set(problem.rules_used)
        )

    def test_reference_link_does_not_mark_anything_explained_or_pending(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=52)
        problem = loop.generate_problem()
        before = loop._coach_explained_rule_ids
        loop.rule_explanations_for(problem)
        self.assertEqual(loop._coach_explained_rule_ids, before)
        self.assertIsNone(loop.pending_coach_request)

    def test_reference_link_still_rejects_a_leaking_fixture(self):
        import dataclasses

        loop = RouterLoop(config=PolicyConfig(), base_seed=53)
        problem = loop.generate_problem()
        register_rule_explanation(
            RuleExplanation(
                rule_id="LEAKY.REF",
                title="t",
                pattern="p",
                if_text="IF",
                then_text="THEN",
                why_text="WHY",
                only_when_text="ONLY WHEN",
                do_not_use_when_text="DO NOT USE WHEN",
                examples=(problem.artifact_text,),
            )
        )
        self.addCleanup(lambda: unregister_rule_explanation("LEAKY.REF"))
        fake_problem = dataclasses.replace(problem, rules_used=("LEAKY.REF",))
        with self.assertRaises(AnswerLeakError):
            loop.rule_explanations_for(fake_problem)


class NoAnswerLeakageTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()
        self.addCleanup(lambda: unregister_rule_explanation("LEAKY"))

    def test_leaking_example_is_rejected_at_explain_time(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=21)
        problem = loop.generate_problem()
        register_rule_explanation(
            RuleExplanation(
                rule_id="LEAKY",
                title="t",
                pattern="p",
                if_text="IF",
                then_text="THEN",
                why_text="WHY",
                only_when_text="ONLY WHEN",
                do_not_use_when_text="DO NOT USE WHEN",
                examples=(problem.artifact_text,),
            )
        )
        loop.request_explanation("LEAKY")
        with self.assertRaises(AnswerLeakError):
            loop.explain()

    def test_clean_explanation_passes_for_active_problem(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=22)
        loop.generate_problem()
        register_rule_explanation(
            RuleExplanation(
                rule_id="LEAKY",
                title="t",
                pattern="p",
                if_text="IF",
                then_text="THEN",
                why_text="WHY",
                only_when_text="ONLY WHEN",
                do_not_use_when_text="DO NOT USE WHEN",
                examples=("completely different example text",),
            )
        )
        loop.request_explanation("LEAKY")
        explanation = loop.explain()
        self.assertEqual(explanation.rule_id, "LEAKY")

    def test_leak_check_still_applies_after_route_next_resets_current_problem(self):
        """The repeated-error EXPLAIN path calls explain() *after*
        route_next() has already reset task_state.current_problem_id to
        None -- the leak check must still find the just-attempted problem
        via the router's own bookkeeping, not silently skip the check."""
        loop = RouterLoop(
            config=PolicyConfig(repeated_error_threshold=2),
            base_seed=23,
            coach_prerequisite_first=False,
        )
        problem = None
        for _ in range(2):
            problem = loop.generate_problem()
            loop.submit_attempt(_incorrect(problem))
            loop.route_next()
        self.assertIsNone(loop.task_state.current_problem_id)
        register_rule_explanation(
            RuleExplanation(
                rule_id="LEAKY",
                title="t",
                pattern="p",
                if_text="IF",
                then_text="THEN",
                why_text="WHY",
                only_when_text="ONLY WHEN",
                do_not_use_when_text="DO NOT USE WHEN",
                examples=(problem.artifact_text,),
            )
        )
        with self.assertRaises(AnswerLeakError):
            loop.explain(CoachRequest(rule_id="LEAKY", trigger_reason=TRIGGER_EXPLICIT_REQUEST))


class DeterminismTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()
        _fresh_coach_fixtures()

    def test_same_rule_same_config_gives_byte_identical_payload(self):
        from Learner_App.coach.worker import to_explanation_payload
        import json

        payload1 = json.dumps(to_explanation_payload(coach_worker_module.explain_rule(EQ_ADD_INVERSE)))
        payload2 = json.dumps(to_explanation_payload(coach_worker_module.explain_rule(EQ_ADD_INVERSE)))
        self.assertEqual(payload1, payload2)

    def test_no_hidden_global_state_leaks_between_router_loop_instances(self):
        loop_a = RouterLoop(config=PolicyConfig(), base_seed=31)
        loop_a.generate_problem()
        loop_a.request_explanation(EQ_ADD_INVERSE)
        loop_a.explain()

        loop_b = RouterLoop(config=PolicyConfig(), base_seed=32)
        self.assertIsNone(loop_b.pending_coach_request)
        self.assertEqual(loop_b._coach_explained_rule_ids, frozenset())


class FailureBehaviorTests(unittest.TestCase):
    def setUp(self):
        _fresh_math_adapter()
        _fresh_coach_fixtures()

    def test_unknown_rule_id_rejected_cleanly_via_explain(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=41, coach_prerequisite_first=False)
        loop.generate_problem()
        loop.request_explanation("TOTALLY.UNKNOWN")
        with self.assertRaises(UnknownRuleError):
            loop.explain()

    def test_unknown_rule_request_does_not_mutate_state(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=42, coach_prerequisite_first=False)
        loop.generate_problem()
        loop.request_explanation("TOTALLY.UNKNOWN")
        explained_before = loop._coach_explained_rule_ids
        with self.assertRaises(UnknownRuleError):
            loop.explain()
        self.assertEqual(loop._coach_explained_rule_ids, explained_before)
        self.assertIsNotNone(loop.pending_coach_request)

    def test_explain_with_nothing_pending_raises_cleanly(self):
        loop = RouterLoop(config=PolicyConfig(), base_seed=43)
        with self.assertRaises(NoCoachRequestPendingError):
            loop.explain()

    def test_circular_prerequisite_detected_not_infinite_recursion(self):
        register_rule_explanation(
            RuleExplanation(
                rule_id="CYCLE.A",
                title="t",
                pattern="p",
                if_text="IF",
                then_text="THEN",
                why_text="WHY",
                only_when_text="ONLY WHEN",
                do_not_use_when_text="DO NOT USE WHEN",
                prerequisites=("CYCLE.B",),
            )
        )
        register_rule_explanation(
            RuleExplanation(
                rule_id="CYCLE.B",
                title="t",
                pattern="p",
                if_text="IF",
                then_text="THEN",
                why_text="WHY",
                only_when_text="ONLY WHEN",
                do_not_use_when_text="DO NOT USE WHEN",
                prerequisites=("CYCLE.A",),
            )
        )
        self.addCleanup(lambda: unregister_rule_explanation("CYCLE.A"))
        self.addCleanup(lambda: unregister_rule_explanation("CYCLE.B"))

        loop = RouterLoop(config=PolicyConfig(), base_seed=44, coach_prerequisite_first=True)
        loop.generate_problem()
        loop.request_explanation("CYCLE.A")
        from Learner_App.coach.models import CircularPrerequisiteError

        with self.assertRaises(CircularPrerequisiteError):
            loop.explain()


if __name__ == "__main__":
    unittest.main()
