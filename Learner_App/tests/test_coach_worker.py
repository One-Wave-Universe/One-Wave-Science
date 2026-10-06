from __future__ import annotations

import json
import unittest

from Learner_App.coach.models import (
    AnswerLeakError,
    CircularPrerequisiteError,
    RuleExplanation,
    UnknownRuleError,
)
from Learner_App.coach.registry import (
    register_rule_explanation,
    unregister_rule_explanation,
)
from Learner_App.coach.worker import (
    check_no_answer_leak,
    explain_rule,
    explain_rules_used,
    next_prerequisite_to_explain,
    to_explanation_payload,
)


def _explanation(rule_id: str, **overrides) -> RuleExplanation:
    kwargs = dict(
        rule_id=rule_id,
        title="Title",
        pattern="pattern",
        if_text="IF x",
        then_text="THEN y",
        why_text="WHY z",
        only_when_text="ONLY WHEN w",
        do_not_use_when_text="DO NOT USE WHEN v",
    )
    kwargs.update(overrides)
    return RuleExplanation(**kwargs)


class RegistryTests(unittest.TestCase):
    def tearDown(self):
        for rule_id in ("A", "B", "C"):
            unregister_rule_explanation(rule_id)

    def test_unknown_rule_id_rejected_cleanly(self):
        with self.assertRaises(UnknownRuleError):
            explain_rule("NOPE")

    def test_registered_rule_is_returned(self):
        register_rule_explanation(_explanation("A"))
        self.assertEqual(explain_rule("A").rule_id, "A")

    def test_double_register_without_replace_raises(self):
        from Learner_App.coach.registry import RuleExplanationAlreadyRegisteredError

        register_rule_explanation(_explanation("A"))
        with self.assertRaises(RuleExplanationAlreadyRegisteredError):
            register_rule_explanation(_explanation("A"))

    def test_replace_true_overwrites(self):
        register_rule_explanation(_explanation("A", title="First"))
        register_rule_explanation(_explanation("A", title="Second"), replace=True)
        self.assertEqual(explain_rule("A").title, "Second")


class PrerequisiteWalkTests(unittest.TestCase):
    def tearDown(self):
        for rule_id in ("A", "B", "C", "D"):
            unregister_rule_explanation(rule_id)

    def test_no_prerequisites_returns_none(self):
        register_rule_explanation(_explanation("A"))
        self.assertIsNone(next_prerequisite_to_explain("A"))

    def test_single_unexplained_prerequisite_returned(self):
        register_rule_explanation(_explanation("A", prerequisites=("B",)))
        register_rule_explanation(_explanation("B"))
        self.assertEqual(next_prerequisite_to_explain("A"), "B")

    def test_already_explained_prerequisite_is_skipped(self):
        register_rule_explanation(_explanation("A", prerequisites=("B",)))
        register_rule_explanation(_explanation("B"))
        self.assertIsNone(
            next_prerequisite_to_explain("A", already_explained=frozenset({"B"}))
        )

    def test_deep_chain_returns_deepest_unexplained_prerequisite_first(self):
        register_rule_explanation(_explanation("A", prerequisites=("B",)))
        register_rule_explanation(_explanation("B", prerequisites=("C",)))
        register_rule_explanation(_explanation("C"))
        self.assertEqual(next_prerequisite_to_explain("A"), "C")

    def test_deep_chain_partially_explained_returns_next_unexplained(self):
        register_rule_explanation(_explanation("A", prerequisites=("B",)))
        register_rule_explanation(_explanation("B", prerequisites=("C",)))
        register_rule_explanation(_explanation("C"))
        result = next_prerequisite_to_explain("A", already_explained=frozenset({"C"}))
        self.assertEqual(result, "B")

    def test_circular_prerequisite_chain_detected_cleanly(self):
        register_rule_explanation(_explanation("A", prerequisites=("B",)))
        register_rule_explanation(_explanation("B", prerequisites=("A",)))
        with self.assertRaises(CircularPrerequisiteError):
            next_prerequisite_to_explain("A")

    def test_self_referential_prerequisite_detected_cleanly(self):
        register_rule_explanation(_explanation("A", prerequisites=("A",)))
        with self.assertRaises(CircularPrerequisiteError):
            next_prerequisite_to_explain("A")

    def test_unregistered_prerequisite_raises_unknown_rule(self):
        register_rule_explanation(_explanation("A", prerequisites=("GHOST",)))
        with self.assertRaises(UnknownRuleError):
            next_prerequisite_to_explain("A")


class NoAnswerLeakTests(unittest.TestCase):
    def test_clean_examples_pass(self):
        explanation = _explanation("A", examples=("y + 5 = 12 -> ...",))
        check_no_answer_leak(explanation, active_artifact_text="x + 7 = 15")

    def test_exact_text_match_raises(self):
        explanation = _explanation("A", examples=("x + 7 = 15",))
        with self.assertRaises(AnswerLeakError):
            check_no_answer_leak(explanation, active_artifact_text="x + 7 = 15")

    def test_whitespace_insensitive_match_raises(self):
        explanation = _explanation("A", examples=("x+7=15 is the setup",))
        with self.assertRaises(AnswerLeakError):
            check_no_answer_leak(explanation, active_artifact_text="x + 7 = 15")

    def test_counterexample_match_also_raises(self):
        explanation = _explanation("A", counterexamples=("x + 7 = 15 is not like this",))
        with self.assertRaises(AnswerLeakError):
            check_no_answer_leak(explanation, active_artifact_text="x + 7 = 15")

    def test_empty_active_text_never_raises(self):
        explanation = _explanation("A", examples=("anything",))
        check_no_answer_leak(explanation, active_artifact_text="")


class ExplainRulesUsedTests(unittest.TestCase):
    def tearDown(self):
        for rule_id in ("A", "B"):
            unregister_rule_explanation(rule_id)

    def test_returns_explanations_in_requested_order(self):
        register_rule_explanation(_explanation("A"))
        register_rule_explanation(_explanation("B"))
        result = explain_rules_used(("A", "B"))
        self.assertEqual([e.rule_id for e in result], ["A", "B"])

    def test_leak_check_applies_to_every_returned_explanation(self):
        register_rule_explanation(_explanation("A", examples=("x + 1 = 2",)))
        with self.assertRaises(AnswerLeakError):
            explain_rules_used(("A",), active_artifact_text="x + 1 = 2")

    def test_unknown_rule_id_rejected_cleanly(self):
        with self.assertRaises(UnknownRuleError):
            explain_rules_used(("GHOST",))


class PayloadDeterminismTests(unittest.TestCase):
    def test_payload_is_json_serializable_and_deterministic(self):
        explanation = _explanation("A", examples=("e1",), prerequisites=("P",))
        payload1 = json.dumps(to_explanation_payload(explanation))
        payload2 = json.dumps(to_explanation_payload(explanation))
        self.assertEqual(payload1, payload2)

    def test_payload_contains_no_metadata_field(self):
        explanation = _explanation("A")
        payload = to_explanation_payload(explanation)
        self.assertNotIn("metadata", payload)
        self.assertNotIn("answer", payload)


if __name__ == "__main__":
    unittest.main()
