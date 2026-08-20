"""Deterministic one-task intake contract for Field Coder Step 03."""

from __future__ import annotations

from dataclasses import dataclass


class TaskIntakeError(ValueError):
    """Raised when a coding goal does not resolve to one bounded task."""


@dataclass(frozen=True)
class TaskSpec:
    summary: str
    scope: tuple[str, ...]
    success_criteria: tuple[str, ...]

    def validate(self) -> None:
        if not self.summary.strip():
            raise TaskIntakeError("task summary must not be empty")
        if not self.scope:
            raise TaskIntakeError("task scope must not be empty")
        if any(not item.strip() for item in self.scope):
            raise TaskIntakeError("task scope contains an empty item")
        if not self.success_criteria:
            raise TaskIntakeError("success criteria must not be empty")
        if any(not item.strip() for item in self.success_criteria):
            raise TaskIntakeError("success criteria contains an empty item")


_PREFIXES = {
    "TASK:": "task",
    "SCOPE:": "scope",
    "SUCCESS:": "success",
}


def parse_task_intake(goal_text: str) -> TaskSpec:
    """Parse exactly one explicit bounded task from a broader goal description."""
    if not isinstance(goal_text, str) or not goal_text.strip():
        raise TaskIntakeError("goal text must not be empty")

    found: dict[str, list[str]] = {"task": [], "scope": [], "success": []}

    for raw_line in goal_text.splitlines():
        line = raw_line.strip()
        for prefix, key in _PREFIXES.items():
            if line.startswith(prefix):
                found[key].append(line[len(prefix):].strip())
                break

    for key, label in (("task", "TASK"), ("scope", "SCOPE"), ("success", "SUCCESS")):
        if len(found[key]) == 0:
            raise TaskIntakeError(f"missing required {label} declaration")
        if len(found[key]) > 1:
            raise TaskIntakeError(f"multiple {label} declarations are ambiguous")
        if not found[key][0]:
            raise TaskIntakeError(f"{label} declaration must not be empty")

    summary = found["task"][0]
    scope = tuple(item.strip() for item in found["scope"][0].split(",") if item.strip())
    success_criteria = tuple(
        item.strip() for item in found["success"][0].split(";") if item.strip()
    )

    spec = TaskSpec(
        summary=summary,
        scope=scope,
        success_criteria=success_criteria,
    )
    spec.validate()
    return spec
