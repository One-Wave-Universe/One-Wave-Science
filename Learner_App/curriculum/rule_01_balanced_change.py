"""Rule 1 — Balanced Change.

If two sides are equal, the same operation on both whole sides keeps them equal.

This is a fixed first lesson, not a random generator. No coefficients.
No move-across shortcut. Cancellation-as-shortcut is later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RULE_ID = "RULE.BALANCED_CHANGE"
RULE_TITLE = "Balanced Change"
RULE_STATEMENT = (
    "If two sides are equal, you can do the same operation to both "
    "whole sides — the whole left and the whole right — and they stay equal."
)

FORBIDDEN_TEACHING = (
    "Teacher note only: do not use the later shortcut of relocating a term "
    "and reversing its operation. The learner is preserving the relationship."
)

Stage = Literal["build_up", "lock_down"]


@dataclass(frozen=True)
class Rule1Problem:
    problem_id: str
    stage: Stage
    title: str
    start: str
    operation: str
    prompt: str
    both_sides_line: str
    teacher_close: str
    accept: tuple[str, ...]
    show_worked_path: bool


def _norm(text: str) -> str:
    return " ".join(text.lower().replace("−", "-").split())


PROBLEMS: tuple[Rule1Problem, ...] = (
    Rule1Problem(
        problem_id="R1-BU-1",
        stage="build_up",
        title="Add the same amount to both whole sides",
        start="3 + 2 = 5",
        operation="add 4 to both whole sides",
        prompt="Both sides start equal. Add 4 to the whole left and the whole right.",
        both_sides_line="3 + 2 + 4 = 5 + 4",
        teacher_close="9 = 9",
        accept=("3 + 2 + 4 = 5 + 4", "3+2+4=5+4"),
        show_worked_path=True,
    ),
    Rule1Problem(
        problem_id="R1-BU-2",
        stage="build_up",
        title="Subtract the same amount from both whole sides",
        start="10 = 7 + 3",
        operation="subtract 2 from both whole sides",
        prompt="Sides look different, values match. Subtract 2 from each whole side.",
        both_sides_line="10 - 2 = 7 + 3 - 2",
        teacher_close="8 = 8",
        accept=("10 - 2 = 7 + 3 - 2", "10-2=7+3-2"),
        show_worked_path=True,
    ),
    Rule1Problem(
        problem_id="R1-BU-3",
        stage="build_up",
        title="Same change when the writing already looks different",
        start="2 + 3 = 6 - 1",
        operation="add 1 to both whole sides",
        prompt="The writing does not match. The values do. Add 1 to each whole side.",
        both_sides_line="2 + 3 + 1 = 6 - 1 + 1",
        teacher_close="6 = 6",
        accept=("2 + 3 + 1 = 6 - 1 + 1", "2+3+1=6-1+1"),
        show_worked_path=True,
    ),
    Rule1Problem(
        problem_id="R1-LD-1",
        stage="lock_down",
        title="Keep the relationship, then the unknown is obvious",
        start="x + 3 = 8",
        operation="subtract 3 from both whole sides",
        prompt=(
            "Write the next line only: the same subtraction on the whole left "
            "and the whole right. Do not skip to a shortcut."
        ),
        both_sides_line="x + 3 - 3 = 8 - 3",
        teacher_close="x = 5",
        accept=("x + 3 - 3 = 8 - 3", "x+3-3=8-3"),
        show_worked_path=False,
    ),
    Rule1Problem(
        problem_id="R1-LD-2",
        stage="lock_down",
        title="Add the same amount to both whole sides",
        start="x - 4 = 6",
        operation="add 4 to both whole sides",
        prompt="Write the next line only: add 4 to the whole left and the whole right.",
        both_sides_line="x - 4 + 4 = 6 + 4",
        teacher_close="x = 10",
        accept=("x - 4 + 4 = 6 + 4", "x-4+4=6+4"),
        show_worked_path=False,
    ),
    Rule1Problem(
        problem_id="R1-LD-3",
        stage="lock_down",
        title="Catch a one-sided change",
        start="5 = 5",
        operation="someone wrote 5 + 2 = 5",
        prompt=(
            "Someone changed only the left side. Does the relationship still hold? "
            "Answer yes or no, then say why in one short line."
        ),
        both_sides_line="no",
        teacher_close="Only one side changed, so equality broke.",
        accept=("no", "n", "false", "not equal"),
        show_worked_path=False,
    ),
)


def lesson_sequence() -> tuple[Rule1Problem, ...]:
    build = tuple(p for p in PROBLEMS if p.stage == "build_up")
    lock = tuple(p for p in PROBLEMS if p.stage == "lock_down")
    if len(build) != 3 or len(lock) != 3:
        raise RuntimeError("Rule 1 must be exactly 3 build-up then 3 lock-down")
    return build + lock


def check_answer(problem: Rule1Problem, raw: str) -> bool:
    got = _norm(raw)
    if not got:
        return False
    if problem.problem_id == "R1-LD-3":
        compact = got.replace(" ", "").replace(",", "")
        return compact == "no" or compact.startswith("no") or compact in {"n", "false", "notequal"}
    compact = got.replace(" ", "")
    return any(compact == _norm(a).replace(" ", "") for a in problem.accept)
