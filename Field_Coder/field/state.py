"""Persistent Field working state for Step 02."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any


class StateValidationError(ValueError):
    """Raised when persisted Field state violates the Step 02 contract."""


@dataclass(frozen=True)
class FieldState:
    goal: str
    current_task: str
    attempt: int
    max_attempts: int
    last_action: str
    last_result: Any
    next_action: str
    active_branch: str
    active_step: str

    @classmethod
    def required_fields(cls) -> tuple[str, ...]:
        return tuple(cls.__dataclass_fields__.keys())

    def validate(self) -> None:
        string_fields = {
            "goal": self.goal,
            "current_task": self.current_task,
            "last_action": self.last_action,
            "next_action": self.next_action,
            "active_branch": self.active_branch,
            "active_step": self.active_step,
        }
        for name, value in string_fields.items():
            if not isinstance(value, str):
                raise StateValidationError(f"{name} must be a string")

        if not isinstance(self.attempt, int) or isinstance(self.attempt, bool):
            raise StateValidationError("attempt must be an integer")
        if not isinstance(self.max_attempts, int) or isinstance(self.max_attempts, bool):
            raise StateValidationError("max_attempts must be an integer")
        if self.max_attempts < 1:
            raise StateValidationError("max_attempts must be at least 1")
        if self.attempt < 0 or self.attempt > self.max_attempts:
            raise StateValidationError("attempt must be between 0 and max_attempts")
        if not self.active_branch:
            raise StateValidationError("active_branch must not be empty")
        if not self.active_step:
            raise StateValidationError("active_step must not be empty")

        try:
            json.dumps(self.last_result)
        except (TypeError, ValueError) as exc:
            raise StateValidationError("last_result must be JSON serializable") from exc

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FieldState":
        if not isinstance(data, dict):
            raise StateValidationError("state root must be an object")

        required = set(cls.required_fields())
        received = set(data)
        missing = sorted(required - received)
        extra = sorted(received - required)
        if missing:
            raise StateValidationError(
                "missing required field(s): " + ", ".join(missing)
            )
        if extra:
            raise StateValidationError(
                "unexpected field(s): " + ", ".join(extra)
            )

        state = cls(**data)
        state.validate()
        return state

    @classmethod
    def load(cls, path: str | Path) -> "FieldState":
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise StateValidationError(f"unable to load state: {exc}") from exc
        return cls.from_dict(data)
