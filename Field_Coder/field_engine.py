"""Minimal executable shell for the Field coding engine.

Step 01 scope only: prove the Field engine can start deterministically.
No state memory, repository inspection, model calls, editing, diffing,
retry logic, or Void behavior belongs in this module yet.
"""

from __future__ import annotations

from dataclasses import dataclass


SHELL_READY = "FIELD_SHELL_READY"


@dataclass(frozen=True)
class FieldShellStatus:
    """Deterministic startup result for the Step 01 Field shell."""

    role: str
    step: int
    ready: bool
    status: str


def start_field_shell() -> FieldShellStatus:
    """Start the minimum Field engine shell and report a stable status."""
    return FieldShellStatus(
        role="field",
        step=1,
        ready=True,
        status=SHELL_READY,
    )


def main() -> int:
    """CLI entry point for the Step 01 shell."""
    state = start_field_shell()
    print(f"{state.status} role={state.role} step={state.step} ready={state.ready}")
    return 0 if state.ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
