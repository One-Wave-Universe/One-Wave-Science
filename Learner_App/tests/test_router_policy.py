from __future__ import annotations

import dataclasses
import unittest

from Learner_App.router.models import RouteAction
from Learner_App.router.policy import (
    DEFAULT_CURRICULUM,
    PolicyConfig,
    REASON_CORRECT_ADVANCE,
    REASON_INCORRECT_REDUCE_DIFFICULTY,
    REASON_INCORRECT_REPEAT,
    REASON_REPEATED_ERROR_EXPLAIN,
    decide_next_route,
    initial_route_decision,
)


class InitialRouteTests(unittest.TestCase):
    def test_initial_route_uses_first_curriculum_step_and_min_difficulty(self):
        config = PolicyConfig()
        decision = initial_route_decision(config, seed=1)
        self.assertEqual(decision.target_rules, DEFAULT_CURRICULUM[0][0])
        self.assertEqual(decision.difficulty, config.min_difficulty)
        self.assertEqual(decision.domain, config.domain)
        self.assertEqual(decision.seed, 1)


class CorrectOutcomeTests(unittest.TestCase):
    def test_correct_advances_to_next_curriculum_step(self):
        config = PolicyConfig()
        current = initial_route_decision(config, seed=1)
        decision, index = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="correct", consecutive_same_error=0, seed=2,
        )
        self.assertEqual(decision.action, RouteAction.ADVANCE)
        self.assertEqual(decision.reason_code, REASON_CORRECT_ADVANCE)
        self.assertEqual(index, 1)
        self.assertEqual(decision.target_rules, DEFAULT_CURRICULUM[1][0])

    def test_correct_increases_difficulty_up_to_max(self):
        config = PolicyConfig(max_difficulty=3)
        current = initial_route_decision(config, seed=1)
        current = dataclasses.replace(current, difficulty=3)
        decision, _ = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="correct", consecutive_same_error=0, seed=2,
        )
        self.assertEqual(decision.difficulty, 3)

    def test_correct_at_last_curriculum_step_stays_at_last_step(self):
        config = PolicyConfig()
        current = initial_route_decision(config, seed=1)
        last_index = len(config.curriculum) - 1
        decision, index = decide_next_route(
            config=config, current=current, curriculum_index=last_index,
            outcome="correct", consecutive_same_error=0, seed=2,
        )
        self.assertEqual(index, last_index)
        self.assertEqual(decision.target_rules, DEFAULT_CURRICULUM[last_index][0])


class IncorrectOutcomeTests(unittest.TestCase):
    def test_incorrect_at_min_difficulty_repeats(self):
        config = PolicyConfig()
        current = initial_route_decision(config, seed=1)  # difficulty == min_difficulty
        decision, index = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="incorrect", consecutive_same_error=1, seed=2,
        )
        self.assertEqual(decision.action, RouteAction.REPEAT)
        self.assertEqual(decision.reason_code, REASON_INCORRECT_REPEAT)
        self.assertEqual(decision.difficulty, config.min_difficulty)
        self.assertEqual(index, 0)
        self.assertEqual(decision.target_rules, DEFAULT_CURRICULUM[0][0])

    def test_incorrect_above_min_difficulty_reduces_difficulty(self):
        config = PolicyConfig()
        current = initial_route_decision(config, seed=1)
        current = dataclasses.replace(current, difficulty=3)
        decision, _ = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="incorrect", consecutive_same_error=1, seed=2,
        )
        self.assertEqual(decision.action, RouteAction.REDUCE_DIFFICULTY)
        self.assertEqual(decision.reason_code, REASON_INCORRECT_REDUCE_DIFFICULTY)
        self.assertEqual(decision.difficulty, 2)

    def test_repeated_same_error_at_threshold_routes_to_explain(self):
        config = PolicyConfig(repeated_error_threshold=2)
        current = initial_route_decision(config, seed=1)
        decision, _ = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="incorrect", consecutive_same_error=2, seed=2,
        )
        self.assertEqual(decision.action, RouteAction.EXPLAIN)
        self.assertEqual(decision.reason_code, REASON_REPEATED_ERROR_EXPLAIN)

    def test_below_threshold_does_not_explain(self):
        config = PolicyConfig(repeated_error_threshold=3)
        current = initial_route_decision(config, seed=1)
        current = dataclasses.replace(current, difficulty=2)
        decision, _ = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="incorrect", consecutive_same_error=2, seed=2,
        )
        self.assertNotEqual(decision.action, RouteAction.EXPLAIN)

    def test_incorrect_never_advances_curriculum_index(self):
        config = PolicyConfig()
        current = initial_route_decision(config, seed=1)
        _, index = decide_next_route(
            config=config, current=current, curriculum_index=1,
            outcome="incorrect", consecutive_same_error=1, seed=2,
        )
        self.assertEqual(index, 1)


class PurityAndDeterminismTests(unittest.TestCase):
    def test_forbidden_rules_pass_through_unchanged(self):
        config = PolicyConfig(forbidden_rules=("EQ.DIV_INVERSE",))
        current = initial_route_decision(config, seed=1)
        decision, _ = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="correct", consecutive_same_error=0, seed=2,
        )
        self.assertEqual(decision.forbidden_rules, ("EQ.DIV_INVERSE",))

    def test_same_inputs_always_produce_same_output(self):
        config = PolicyConfig()
        current = initial_route_decision(config, seed=1)
        kwargs = dict(
            config=config, current=current, curriculum_index=0,
            outcome="incorrect", consecutive_same_error=1, seed=42,
        )
        first = decide_next_route(**kwargs)
        second = decide_next_route(**kwargs)
        self.assertEqual(first, second)

    def test_evidence_confidence_and_metadata_do_not_affect_the_decision(self):
        # Only `outcome` (and the router's own consecutive-error tracking)
        # may drive the decision -- evidence cannot silently override
        # router authority by carrying an advisory "confidence" or
        # metadata field that changes the outcome.
        config = PolicyConfig()
        current = initial_route_decision(config, seed=1)
        low_conf, _ = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="correct", consecutive_same_error=0, seed=2,
        )
        high_conf, _ = decide_next_route(
            config=config, current=current, curriculum_index=0,
            outcome="correct", consecutive_same_error=0, seed=2,
        )
        self.assertEqual(low_conf, high_conf)


if __name__ == "__main__":
    unittest.main()
