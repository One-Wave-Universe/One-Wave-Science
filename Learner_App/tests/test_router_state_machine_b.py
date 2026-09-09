from __future__ import annotations

import unittest

from Learner_App.router.models import (
    EvaluationLifecycle,
    LearnerAttempt,
    LearnerTaskState,
    TaskLifecycle,
    initial_evaluator_state,
)
from Learner_App.router.state_machine_b import (
    IllegalEvaluationTransitionError,
    MalformedAttemptError,
    StaleAttemptError,
    acknowledge,
    begin_evaluation,
    emit_evidence,
    evaluate_attempt,
    validate_attempt,
)


def _executing_task_state(problem_id="p1", targets=("EQ.ADD_INVERSE",)) -> LearnerTaskState:
    return LearnerTaskState(
        lifecycle_state=TaskLifecycle.EXECUTING,
        current_problem_id=problem_id,
        current_rule_targets=targets,
        attempt_count=0,
        waiting_for_input=True,
    )


class HappyPathTests(unittest.TestCase):
    def test_full_cycle_advances_through_all_three_states_in_order(self):
        state = initial_evaluator_state()
        self.assertEqual(state.lifecycle_state, EvaluationLifecycle.IDLE)

        state = begin_evaluation(state)
        self.assertEqual(state.lifecycle_state, EvaluationLifecycle.EVALUATING)

        task_state = _executing_task_state()
        attempt = LearnerAttempt(problem_id="p1", outcome="correct", reported_rules_used=("EQ.ADD_INVERSE",))
        evidence = evaluate_attempt(attempt, task_state)

        state = emit_evidence(state, evidence)
        self.assertEqual(state.lifecycle_state, EvaluationLifecycle.EMITTED)
        self.assertIs(state.last_evidence, evidence)
        self.assertEqual(state.evaluation_count, 1)

        state = acknowledge(state)
        self.assertEqual(state.lifecycle_state, EvaluationLifecycle.IDLE)


class IllegalTransitionTests(unittest.TestCase):
    def test_emit_evidence_requires_evaluating(self):
        with self.assertRaises(IllegalEvaluationTransitionError):
            emit_evidence(initial_evaluator_state(), evidence=None)

    def test_acknowledge_requires_emitted(self):
        with self.assertRaises(IllegalEvaluationTransitionError):
            acknowledge(initial_evaluator_state())

    def test_begin_evaluation_requires_idle(self):
        state = begin_evaluation(initial_evaluator_state())
        with self.assertRaises(IllegalEvaluationTransitionError):
            begin_evaluation(state)


class ValidateAttemptTests(unittest.TestCase):
    def test_matching_problem_id_and_valid_outcome_passes(self):
        validate_attempt(LearnerAttempt(problem_id="p1", outcome="correct"), _executing_task_state())

    def test_invalid_outcome_is_malformed(self):
        with self.assertRaises(MalformedAttemptError):
            validate_attempt(
                LearnerAttempt(problem_id="p1", outcome="definitely_maybe"), _executing_task_state()
            )

    def test_empty_problem_id_is_malformed(self):
        with self.assertRaises(MalformedAttemptError):
            validate_attempt(LearnerAttempt(problem_id="", outcome="correct"), _executing_task_state())

    def test_mismatched_problem_id_is_stale(self):
        with self.assertRaises(StaleAttemptError):
            validate_attempt(
                LearnerAttempt(problem_id="wrong-id", outcome="correct"), _executing_task_state()
            )

    def test_no_active_problem_is_stale(self):
        idle_task_state = LearnerTaskState(
            lifecycle_state=TaskLifecycle.IDLE,
            current_problem_id=None,
            current_rule_targets=(),
            attempt_count=0,
            waiting_for_input=False,
        )
        with self.assertRaises(StaleAttemptError):
            validate_attempt(LearnerAttempt(problem_id="p1", outcome="correct"), idle_task_state)


class EvaluateAttemptTests(unittest.TestCase):
    def test_correct_with_all_target_rules_demonstrated(self):
        task_state = _executing_task_state(targets=("EQ.ADD_INVERSE", "EQ.MUL_INVERSE"))
        attempt = LearnerAttempt(
            problem_id="p1",
            outcome="correct",
            reported_rules_used=("EQ.ADD_INVERSE", "EQ.MUL_INVERSE"),
        )
        evidence = evaluate_attempt(attempt, task_state)
        self.assertEqual(evidence.outcome, "correct")
        self.assertIsNone(evidence.error_kind)
        self.assertEqual(evidence.missing_rules, ())
        self.assertEqual(evidence.confidence, "high")

    def test_incorrect_with_missing_target_rule_reports_it(self):
        task_state = _executing_task_state(targets=("EQ.ADD_INVERSE", "EQ.MUL_INVERSE"))
        attempt = LearnerAttempt(
            problem_id="p1", outcome="incorrect", reported_rules_used=("EQ.ADD_INVERSE",)
        )
        evidence = evaluate_attempt(attempt, task_state)
        self.assertEqual(evidence.missing_rules, ("EQ.MUL_INVERSE",))
        self.assertEqual(evidence.error_kind, "missing_rule:EQ.MUL_INVERSE")
        self.assertEqual(evidence.confidence, "low")

    def test_correct_outcome_with_missing_target_rule_still_reports_error_kind(self):
        # error_kind reflects missing_rules regardless of outcome -- a
        # "correct" attempt that didn't demonstrate every target rule is
        # still an incomplete demonstration the router needs to see.
        task_state = _executing_task_state(targets=("EQ.ADD_INVERSE", "EQ.MUL_INVERSE"))
        attempt = LearnerAttempt(
            problem_id="p1", outcome="correct", reported_rules_used=("EQ.ADD_INVERSE",)
        )
        evidence = evaluate_attempt(attempt, task_state)
        self.assertEqual(evidence.missing_rules, ("EQ.MUL_INVERSE",))
        self.assertEqual(evidence.error_kind, "missing_rule:EQ.MUL_INVERSE")

    def test_incomplete_outcome_is_passed_through(self):
        task_state = _executing_task_state()
        attempt = LearnerAttempt(problem_id="p1", outcome="incomplete")
        evidence = evaluate_attempt(attempt, task_state)
        self.assertEqual(evidence.outcome, "incomplete")

    def test_extra_demonstrated_rule_beyond_targets_does_not_add_missing(self):
        task_state = _executing_task_state(targets=("EQ.ADD_INVERSE",))
        attempt = LearnerAttempt(
            problem_id="p1", outcome="correct", reported_rules_used=("EQ.ADD_INVERSE", "EQ.MUL_INVERSE")
        )
        evidence = evaluate_attempt(attempt, task_state)
        self.assertEqual(evidence.missing_rules, ())

    def test_evidence_carries_no_answer_field(self):
        import dataclasses

        task_state = _executing_task_state()
        attempt = LearnerAttempt(problem_id="p1", outcome="correct", reported_rules_used=("EQ.ADD_INVERSE",))
        evidence = evaluate_attempt(attempt, task_state)
        field_names = {f.name for f in dataclasses.fields(evidence)}
        self.assertFalse(field_names & {"answer", "solution", "solved_value"})


if __name__ == "__main__":
    unittest.main()
