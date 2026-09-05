"""Runnable shared-state Dream/Admin coding-loop MVP.

The host owns one state, one reference, and one loop. Dream and Administrator
are roles that receive different views of the same state. M4 is deterministic:
it routes state, tools, measurements, receipts, and token accounting; it is not
an LLM.

This module intentionally does not choose a model vendor. A local or cloud
worker can be connected through the small worker adapter in ``local_pair.py``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
from pathlib import Path
import shlex
import subprocess
from typing import Any


class LoopStep(str, Enum):
    BEGIN = "BEGIN"
    BUILD_1 = "BUILD_1"
    HOLD = "HOLD"
    BUILD_2 = "BUILD_2"
    BREAK = "BREAK"
    LOOP = "LOOP"


@dataclass(slots=True)
class ToolAction:
    """One bounded Dream request to the deterministic tool broker."""

    kind: str
    path: str = ""
    content: str = ""
    command: str = ""
    query: str = ""
    note: str = ""


@dataclass(slots=True)
class ToolResult:
    ok: bool
    kind: str
    output: str
    changed: bool = False


@dataclass(slots=True)
class AdminDecision:
    """Administrator view of measured reality, not a replacement target."""

    direction: str = "0"  # - / 0 / + relative to root reference
    relation: str = ""
    dimensional_view: str = ""
    oversight: str = ""
    override: bool = False
    override_instruction: str = ""


@dataclass
class SharedState:
    root_reference: str
    cycle: int = 1
    step: LoopStep = LoopStep.BEGIN
    choice_space: str = "ON"
    direction: str = "0"
    quadratic_relation: str = ""
    dimensional_view: str = ""
    inherited_state: list[str] = field(default_factory=list)
    measurements: list[str] = field(default_factory=list)
    receipts: list[dict[str, Any]] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    local_tokens: int = 0
    oversight_tokens: int = 0
    override_tokens: int = 0

    def dream_view(self) -> dict[str, Any]:
        """Small working packet for Dream; exact archive stays out of prompt."""

        return {
            "reference": self.root_reference,
            "cycle": self.cycle,
            "step": self.step.value,
            "2_choice_space": self.choice_space,
            "3_direction": self.direction,
            "4_relation": self.quadratic_relation,
            "5_view": self.dimensional_view,
            "inherited": self.inherited_state[-8:],
            "last_measurements": self.measurements[-4:],
            "unresolved": self.unresolved[-6:],
        }

    def admin_view(self) -> dict[str, Any]:
        """Compressed oversight packet; source files are omitted by default."""

        return {
            "reference": self.root_reference,
            "cycle": self.cycle,
            "step": self.step.value,
            "2_choice_space": self.choice_space,
            "3_direction": self.direction,
            "4_relation": self.quadratic_relation,
            "5_view": self.dimensional_view,
            "inherited": self.inherited_state[-6:],
            "last_measurement": self.measurements[-1:] or [""],
            "unresolved": self.unresolved[-4:],
            "token_use": {
                "local": self.local_tokens,
                "oversight": self.oversight_tokens,
                "override": self.override_tokens,
            },
        }

    def save(self, path: Path) -> None:
        data = asdict(self)
        data["step"] = self.step.value
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "SharedState":
        data = json.loads(path.read_text(encoding="utf-8"))
        data["step"] = LoopStep(data["step"])
        return cls(**data)


class ToolBroker:
    """Workspace-scoped coding tools owned by M4, not by either AI."""

    _DENIED_FRAGMENTS = (
        "sudo ",
        "rm -rf /",
        "git push",
        "git reset --hard",
        "mkfs",
        ":(){:|:&};:",
    )

    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        if not self.workspace.exists():
            raise FileNotFoundError(self.workspace)

    def _path(self, relative: str) -> Path:
        candidate = (self.workspace / relative).resolve()
        try:
            candidate.relative_to(self.workspace)
        except ValueError as exc:
            raise ValueError("path escapes workspace") from exc
        return candidate

    def execute(self, action: ToolAction) -> ToolResult:
        kind = action.kind.lower().strip()
        if kind == "read":
            path = self._path(action.path)
            return ToolResult(True, kind, path.read_text(encoding="utf-8"))

        if kind == "search":
            needle = action.query
            matches: list[str] = []
            for path in self.workspace.rglob("*"):
                if not path.is_file() or ".git" in path.parts:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                for line_no, line in enumerate(text.splitlines(), 1):
                    if needle.lower() in line.lower():
                        rel = path.relative_to(self.workspace)
                        matches.append(f"{rel}:{line_no}:{line.strip()}")
                        if len(matches) >= 80:
                            return ToolResult(True, kind, "\n".join(matches))
            return ToolResult(True, kind, "\n".join(matches))

        if kind == "write":
            path = self._path(action.path)
            path.parent.mkdir(parents=True, exist_ok=True)
            before = path.read_text(encoding="utf-8") if path.exists() else None
            path.write_text(action.content, encoding="utf-8")
            return ToolResult(True, kind, str(path.relative_to(self.workspace)), before != action.content)

        if kind == "command":
            command = action.command.strip()
            lower = command.lower()
            if not command:
                return ToolResult(False, kind, "empty command")
            if any(fragment in lower for fragment in self._DENIED_FRAGMENTS):
                return ToolResult(False, kind, "command denied by workspace broker")
            completed = subprocess.run(
                command,
                cwd=self.workspace,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=120,
            )
            return ToolResult(
                completed.returncode == 0,
                kind,
                f"exit={completed.returncode}\n{completed.stdout[-12000:]}",
                changed=False,
            )

        return ToolResult(False, kind, f"unknown tool action: {kind}")


class M4Host:
    """Deterministic owner of shared state, loop position, tools and receipts."""

    def __init__(self, state: SharedState, workspace: Path, state_path: Path | None = None):
        self.state = state
        self.tools = ToolBroker(workspace)
        self.state_path = state_path or (workspace / ".onewave" / "shared_state.json")
        self._persist()

    def _receipt(self, event: str, **payload: Any) -> None:
        self.state.receipts.append(
            {"cycle": self.state.cycle, "step": self.state.step.value, "event": event, **payload}
        )
        self._persist()

    def _persist(self) -> None:
        self.state.save(self.state_path)

    def begin(self, observation: str) -> None:
        if self.state.step is not LoopStep.BEGIN:
            raise RuntimeError(f"BEGIN required, current step is {self.state.step.value}")
        self.state.measurements.append(observation)
        self._receipt("begin_observation", observation=observation)
        self.state.step = LoopStep.BUILD_1
        self._persist()

    def dream_tool(self, action: ToolAction) -> ToolResult:
        """Allow inspection in BUILD; first mutating action advances the macro loop."""

        if self.state.step not in (LoopStep.BUILD_1, LoopStep.BUILD_2):
            raise RuntimeError(f"Dream tools are only available in BUILD, not {self.state.step.value}")
        result = self.tools.execute(action)
        self._receipt(
            "dream_tool",
            action=asdict(action),
            result={"ok": result.ok, "kind": result.kind, "output": result.output[-4000:], "changed": result.changed},
        )
        mutating = action.kind.lower() in {"write", "command"}
        if mutating:
            self.state.step = LoopStep.HOLD if self.state.step is LoopStep.BUILD_1 else LoopStep.BREAK
            self._persist()
        return result

    def hold(self, measurement: str, admin: AdminDecision) -> None:
        if self.state.step is not LoopStep.HOLD:
            raise RuntimeError(f"HOLD required, current step is {self.state.step.value}")
        self._apply_admin(measurement, admin, "hold")
        self.state.step = LoopStep.BUILD_2
        self._persist()

    def break_step(self, measurement: str, admin: AdminDecision) -> None:
        if self.state.step is not LoopStep.BREAK:
            raise RuntimeError(f"BREAK required, current step is {self.state.step.value}")
        self._apply_admin(measurement, admin, "break")
        self.state.step = LoopStep.LOOP
        self._persist()

    def _apply_admin(self, measurement: str, admin: AdminDecision, event: str) -> None:
        self.state.measurements.append(measurement)
        self.state.direction = admin.direction
        self.state.quadratic_relation = admin.relation
        self.state.dimensional_view = admin.dimensional_view
        if admin.override and admin.override_instruction:
            self.state.unresolved.append(admin.override_instruction)
        self._receipt(event, measurement=measurement, admin=asdict(admin))

    def complete_loop(self, compressed_state: str, unresolved: list[str] | None = None) -> None:
        if self.state.step is not LoopStep.LOOP:
            raise RuntimeError(f"LOOP required, current step is {self.state.step.value}")
        self.state.inherited_state.append(compressed_state)
        if unresolved is not None:
            self.state.unresolved = list(unresolved)
        self._receipt("loop_complete", compressed_state=compressed_state, unresolved=self.state.unresolved)
        self.state.cycle += 1
        self.state.step = LoopStep.BEGIN
        self._persist()

    def add_token_use(self, role: str, tokens: int) -> None:
        if tokens < 0:
            raise ValueError("tokens must be non-negative")
        role = role.lower()
        if role == "local":
            self.state.local_tokens += tokens
        elif role == "oversight":
            self.state.oversight_tokens += tokens
        elif role == "override":
            self.state.override_tokens += tokens
        else:
            raise ValueError(f"unknown token role: {role}")
        self._persist()
