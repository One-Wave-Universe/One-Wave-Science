from __future__ import annotations

import unittest

from Learner_App.coach.models import MalformedRuleExplanationError, RuleExplanation

_REQUIRED_KWARGS = dict(
    rule_id="R",
    title="Title",
    pattern="pattern",
    if_text="IF x",
    then_text="THEN y",
    why_text="WHY z",
    only_when_text="ONLY WHEN w",
    do_not_use_when_text="DO NOT USE WHEN v",
)


class RuleExplanationValidationTests(unittest.TestCase):
    def test_minimal_valid_explanation_constructs(self):
        explanation = RuleExplanation(**_REQUIRED_KWARGS)
        self.assertEqual(explanation.rule_id, "R")
        self.assertEqual(explanation.prerequisites, ())
        self.assertEqual(explanation.source_kind, "fixture")

    def test_list_like_fields_are_coerced_to_tuples(self):
        explanation = RuleExplanation(
            **_REQUIRED_KWARGS,
            prerequisites=["P1", "P2"],
            uses_with=["U1"],
            examples=["ex1"],
            counterexamples=["counter1"],
            formal_terms=["term1"],
        )
        self.assertEqual(explanation.prerequisites, ("P1", "P2"))
        self.assertEqual(explanation.uses_with, ("U1",))
        self.assertEqual(explanation.examples, ("ex1",))
        self.assertEqual(explanation.counterexamples, ("counter1",))
        self.assertEqual(explanation.formal_terms, ("term1",))

    def test_missing_required_field_fails_loudly(self):
        kwargs = dict(_REQUIRED_KWARGS)
        kwargs["why_text"] = ""
        with self.assertRaises(MalformedRuleExplanationError):
            RuleExplanation(**kwargs)

    def test_whitespace_only_required_field_fails_loudly(self):
        kwargs = dict(_REQUIRED_KWARGS)
        kwargs["only_when_text"] = "   "
        with self.assertRaises(MalformedRuleExplanationError):
            RuleExplanation(**kwargs)

    def test_multiple_missing_fields_reported_together(self):
        kwargs = dict(_REQUIRED_KWARGS)
        kwargs["why_text"] = ""
        kwargs["pattern"] = ""
        with self.assertRaises(MalformedRuleExplanationError) as ctx:
            RuleExplanation(**kwargs)
        self.assertIn("why_text", str(ctx.exception))
        self.assertIn("pattern", str(ctx.exception))

    def test_optional_fields_default_sensibly(self):
        explanation = RuleExplanation(**_REQUIRED_KWARGS)
        self.assertEqual(explanation.concept_first_note, "")
        self.assertEqual(explanation.examples, ())
        self.assertEqual(explanation.counterexamples, ())


if __name__ == "__main__":
    unittest.main()
