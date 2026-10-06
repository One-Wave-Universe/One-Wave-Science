"""Rule-format acceptance tests for the math/basic_equations Coach
fixtures (issue #47's "Example fixtures" + "Rule format" sections)."""

from __future__ import annotations

import unittest

from Learner_App.coach.fixtures.math_basic_equations import (
    CONCEPT_COEFFICIENT,
    CONCEPT_INVERSE_OPERATION,
    CONCEPT_WHOLE_EQUATION_SCALING,
    EQ_ADD_INVERSE,
    EQ_DIV_INVERSE,
    EQ_IDENTITY,
    EQ_MUL_INVERSE,
    EQ_SUB_INVERSE,
    register_default_explanations,
)
from Learner_App.coach.registry import unregister_rule_explanation
from Learner_App.coach.worker import explain_rule
from Learner_App.parser.adapters.math_basic_equations import (
    EQ_ADD_INVERSE as PARSER_EQ_ADD_INVERSE,
    EQ_DIV_INVERSE as PARSER_EQ_DIV_INVERSE,
    EQ_IDENTITY as PARSER_EQ_IDENTITY,
    EQ_MUL_INVERSE as PARSER_EQ_MUL_INVERSE,
    EQ_SUB_INVERSE as PARSER_EQ_SUB_INVERSE,
)

ALL_FIXTURE_RULE_IDS = (
    CONCEPT_COEFFICIENT,
    CONCEPT_WHOLE_EQUATION_SCALING,
    CONCEPT_INVERSE_OPERATION,
    EQ_IDENTITY,
    EQ_ADD_INVERSE,
    EQ_SUB_INVERSE,
    EQ_MUL_INVERSE,
    EQ_DIV_INVERSE,
)


class FixtureRegistrationTests(unittest.TestCase):
    def setUp(self):
        register_default_explanations()
        self.addCleanup(lambda: [unregister_rule_explanation(r) for r in ALL_FIXTURE_RULE_IDS])

    def test_rule_id_literals_match_phase1_adapter_constants(self):
        """coach fixtures deliberately never import parser (one-way
        dependency) -- this test is what keeps the hand-copied literals
        from silently drifting out of sync with Phase 1's real rule_ids."""
        self.assertEqual(EQ_IDENTITY, PARSER_EQ_IDENTITY)
        self.assertEqual(EQ_ADD_INVERSE, PARSER_EQ_ADD_INVERSE)
        self.assertEqual(EQ_SUB_INVERSE, PARSER_EQ_SUB_INVERSE)
        self.assertEqual(EQ_MUL_INVERSE, PARSER_EQ_MUL_INVERSE)
        self.assertEqual(EQ_DIV_INVERSE, PARSER_EQ_DIV_INVERSE)

    def test_every_fixture_produces_complete_if_then_why_only_when_do_not(self):
        for rule_id in ALL_FIXTURE_RULE_IDS:
            explanation = explain_rule(rule_id)
            for field_name in (
                "if_text",
                "then_text",
                "why_text",
                "only_when_text",
                "do_not_use_when_text",
            ):
                value = getattr(explanation, field_name)
                self.assertTrue(value.strip(), f"{rule_id} missing {field_name}")

    def test_inverse_operation_rules_cite_the_inverse_operation_concept(self):
        for rule_id in (EQ_ADD_INVERSE, EQ_SUB_INVERSE, EQ_MUL_INVERSE, EQ_DIV_INVERSE):
            explanation = explain_rule(rule_id)
            self.assertIn(CONCEPT_INVERSE_OPERATION, explanation.prerequisites)

    def test_coefficient_operations_cite_the_coefficient_concept(self):
        explanation = explain_rule(EQ_MUL_INVERSE)
        self.assertIn(CONCEPT_COEFFICIENT, explanation.prerequisites)

    def test_identity_rule_has_no_prerequisites(self):
        self.assertEqual(explain_rule(EQ_IDENTITY).prerequisites, ())

    def test_concept_first_note_precedes_formal_vocabulary(self):
        """Formal vocabulary lives in its own field, separate from the
        concept-first explanation -- the label never has to appear inside
        concept_first_note itself for the label-after-meaning ordering to
        hold structurally."""
        explanation = explain_rule(EQ_MUL_INVERSE)
        self.assertTrue(explanation.concept_first_note)
        self.assertIn("coefficient", explanation.formal_terms)


if __name__ == "__main__":
    unittest.main()
