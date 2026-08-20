"""Step 03 one-task intake verification.

Run from repository root:
    python3 Field_Coder/tests/test_task_intake.py
"""

from pathlib import Path
import sys

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.task_intake import TaskIntakeError, parse_task_intake


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_error(text: str, fragment: str) -> None:
    try:
        parse_task_intake(text)
    except TaskIntakeError as exc:
        require(fragment in str(exc), str(exc))
    else:
        raise AssertionError("expected TaskIntakeError")


def main() -> int:
    broad_goal = """
Improve calculator reliability without rewriting working arithmetic.
The first bounded change is multiplication support.
TASK: add multiplication while preserving addition and subtraction
SCOPE: calculator.py, tests/test_calculator.py
SUCCESS: multiplication test passes; existing addition test passes; existing subtraction test passes
Later ideas are out of scope for this task.
"""

    task = parse_task_intake(broad_goal)
    require(
        task.summary == "add multiplication while preserving addition and subtraction",
        task.summary,
    )
    require(
        task.scope == ("calculator.py", "tests/test_calculator.py"),
        repr(task.scope),
    )
    require(len(task.success_criteria) == 3, repr(task.success_criteria))
    print("PASS: broad goal resolved to exactly one bounded TaskSpec")

    multi_task = """
TASK: add multiplication
TASK: refactor parser
SCOPE: calculator.py
SUCCESS: tests pass
"""
    expect_error(multi_task, "multiple TASK declarations are ambiguous")
    print("PASS: multiple tasks rejected")

    unbounded = """
TASK: add multiplication
SUCCESS: multiplication test passes
"""
    expect_error(unbounded, "missing required SCOPE declaration")
    print("PASS: unbounded task rejected")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
