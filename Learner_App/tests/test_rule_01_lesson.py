"""Rule 1 first-lesson contract."""

from __future__ import annotations

import unittest

from Learner_App.curriculum.rule_01_balanced_change import (
    FORBIDDEN_TEACHING,
    PROBLEMS,
    RULE_ID,
    RULE_STATEMENT,
    check_answer,
    lesson_sequence,
)


class Rule1ShapeTests(unittest.TestCase):
    def test_exactly_three_then_three(self) -> None:
        seq = lesson_sequence()
        self.assertEqual(len(seq), 6)
        self.assertEqual([p.stage for p in seq], ["build_up"] * 3 + ["lock_down"] * 3)

    def test_rule_id_and_statement(self) -> None:
        self.assertEqual(RULE_ID, "RULE.BALANCED_CHANGE")
        self.assertIn("same operation", RULE_STATEMENT.lower())
        self.assertIn("both", RULE_STATEMENT.lower())

    def test_no_move_across_shortcut_in_teaching(self) -> None:
        blob = " ".join(
            [RULE_STATEMENT, FORBIDDEN_TEACHING]
            + [p.prompt + p.operation + p.title for p in PROBLEMS]
        ).lower()
        self.assertNotIn("change its sign", blob)
        self.assertNotIn("move the 3 across", blob)
        self.assertNotIn("flip the sign", blob)

    def test_no_coefficients_in_rule_1_starts(self) -> None:
        for p in PROBLEMS:
            self.assertNotRegex(p.start, r"\d[a-zA-Z]")

    def test_lock_down_does_not_print_close_on_live_card(self) -> None:
        for p in lesson_sequence():
            if p.stage == "lock_down":
                self.assertFalse(p.show_worked_path)


class Rule1GradingTests(unittest.TestCase):
    def test_canonical_lines_pass(self) -> None:
        for p in PROBLEMS:
            self.assertTrue(check_answer(p, p.accept[0]), p.problem_id)

    def test_compact_spacing_still_passes(self) -> None:
        p = PROBLEMS[0]
        self.assertTrue(check_answer(p, "3+2+4=5+4"))

    def test_wrong_one_sided_change_fails_build_up(self) -> None:
        p = PROBLEMS[0]
        self.assertFalse(check_answer(p, "3 + 2 + 4 = 5"))

    def test_broken_equality_lock_down_accepts_no(self) -> None:
        p = PROBLEMS[-1]
        self.assertTrue(check_answer(p, "No"))
        self.assertTrue(check_answer(p, "no, only one side changed"))
        self.assertFalse(check_answer(p, "yes"))


if __name__ == "__main__":
    unittest.main()
