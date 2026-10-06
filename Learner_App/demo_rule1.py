#!/usr/bin/env python3
"""Headless first-lesson pass for Rule 1 — Balanced Change.

    python3 -m Learner_App.demo_rule1
"""

from __future__ import annotations

from Learner_App.curriculum.rule_01_balanced_change import (
    FORBIDDEN_TEACHING,
    RULE_STATEMENT,
    RULE_TITLE,
    check_answer,
    lesson_sequence,
)


def main() -> None:
    print(f"Rule 1 — {RULE_TITLE}")
    print(RULE_STATEMENT)
    print(FORBIDDEN_TEACHING)
    for i, problem in enumerate(lesson_sequence(), start=1):
        print(f"\n--- {i}/6 {problem.problem_id} ({problem.stage}) ---")
        print(f"  start:     {problem.start}")
        print(f"  operation: {problem.operation}")
        print(f"  prompt:    {problem.prompt}")
        if problem.show_worked_path:
            print(f"  both sides:{problem.both_sides_line}")
            print(f"  closes as: {problem.teacher_close}")
        else:
            print("  live card hides the close line")
        ok = check_answer(problem, problem.accept[0])
        print(f"  self-check canonical accept: {ok}")


if __name__ == "__main__":
    main()
