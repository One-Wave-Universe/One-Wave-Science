from __future__ import annotations

import unittest

from Learner_App.router.models import TaskLifecycle, initial_task_state
from Learner_App.router.state_machine_a import (
    IllegalTaskTransitionError,
    apply_route_decision,
    assign_problem,
    present_to_learner,
    receive_attempt,
    resolve_cycle,
)


class HappyPathTests(unittest.TestCase):
    def test_full_cycle_advances_through_all_five_states_in_order(self):
        state = initial_task_state()
        self.assertEqual(state.lifecycle_state, TaskLifecycle.IDLE)

        state = assign_problem(state, "p1", ("EQ.ADD_INVERSE",))
        self.assertEqual(state.lifecycle_state, TaskLifecycle.PRIMED)
        self.assertEqual(state.current_problem_id, "p1")
        self.assertEqual(state.current_rule_targets, ("EQ.ADD_INVERSE",))
        self.assertEqual(state.attempt_count, 0)

        state = present_to_learner(state)
        self.assertEqual(state.lifecycle_state, TaskLifecycle.EXECUTING)
        self.assertTrue(state.waiting_for_input)

        state = receive_attempt(state)
        self.assertEqual(state.lifecycle_state, TaskLifecycle.VECTORING)
        self.assertEqual(state.attempt_count, 1)
        self.assertFalse(state.waiting_for_input)

        state = apply_route_decision(state)
        self.assertEqual(state.lifecycle_state, TaskLifecycle.RESOLVING)

        state = resolve_cycle(state)
        self.assertEqual(state.lifecycle_state, TaskLifecycle.IDLE)

    def test_resolve_returns_to_a_clean_boundary_state(self):
        state = initial_task_state()
        state = assign_problem(state, "p1", ("EQ.ADD_INVERSE", "EQ.MUL_INVERSE"))
        state = present_to_learner(state)
        state = receive_attempt(state)
        state = apply_route_decision(state)
        state = resolve_cycle(state)

        self.assertEqual(state, initial_task_state())

    def test_multiple_attempts_increment_attempt_count(self):
        state = initial_task_state()
        state = assign_problem(state, "p1", ("EQ.ADD_INVERSE",))
        state = present_to_learner(state)
        state = receive_attempt(state)
        self.assertEqual(state.attempt_count, 1)


class IllegalTransitionTests(unittest.TestCase):
    def test_present_to_learner_requires_primed(self):
        with self.assertRaises(IllegalTaskTransitionError):
            present_to_learner(initial_task_state())

    def test_receive_attempt_requires_executing(self):
        with self.assertRaises(IllegalTaskTransitionError):
            receive_attempt(initial_task_state())

    def test_apply_route_decision_requires_vectoring(self):
        with self.assertRaises(IllegalTaskTransitionError):
            apply_route_decision(initial_task_state())

    def test_resolve_cycle_requires_resolving(self):
        with self.assertRaises(IllegalTaskTransitionError):
            resolve_cycle(initial_task_state())

    def test_assign_problem_requires_idle(self):
        state = assign_problem(initial_task_state(), "p1", ("EQ.ADD_INVERSE",))
        with self.assertRaises(IllegalTaskTransitionError):
            assign_problem(state, "p2", ("EQ.ADD_INVERSE",))

    def test_illegal_transition_does_not_mutate_state(self):
        state = initial_task_state()
        try:
            present_to_learner(state)
        except IllegalTaskTransitionError:
            pass
        self.assertEqual(state, initial_task_state())

    def test_illegal_transition_error_names_expected_and_actual(self):
        try:
            present_to_learner(initial_task_state())
            self.fail("expected IllegalTaskTransitionError")
        except IllegalTaskTransitionError as exc:
            self.assertEqual(exc.expected, TaskLifecycle.PRIMED)
            self.assertEqual(exc.actual, TaskLifecycle.IDLE)


if __name__ == "__main__":
    unittest.main()
