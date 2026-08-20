"""Step 02 persistent Field state verification.

Run from repository root:
    python3 Field_Coder/tests/test_state.py
"""

from pathlib import Path
import json
import subprocess
import sys
import tempfile

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.state import FieldState, StateValidationError


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_validation_error(action, expected_fragment: str) -> None:
    try:
        action()
    except StateValidationError as exc:
        require(expected_fragment in str(exc), str(exc))
    else:
        raise AssertionError("expected StateValidationError")


def sample_state() -> FieldState:
    return FieldState(
        goal="persist Field working state",
        current_task="save and restore exact state",
        attempt=1,
        max_attempts=3,
        last_action="state-save",
        last_result={"status": "pending", "code": 0},
        next_action="state-reload",
        active_branch="field-coder/02-state-memory",
        active_step="02-state-memory",
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        state_path = Path(tmp) / "field-state.json"
        original = sample_state()
        original.save(state_path)

        # Reload in this process.
        reloaded = FieldState.load(state_path)
        require(reloaded == original, "same-process reload changed state")

        # Reload in a fresh Python process to prove restart persistence.
        code = (
            "from field.state import FieldState; "
            f"print(FieldState.load({str(state_path)!r}).to_json())"
        )
        fresh = subprocess.run(
            [sys.executable, "-c", code],
            cwd=FIELD_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        require(fresh.returncode == 0, fresh.stderr)
        require(fresh.stdout.strip() == original.to_json(), fresh.stdout)
        print("PASS: exact state restored in fresh process")

        # Missing required field must fail.
        missing = original.to_dict()
        del missing["next_action"]
        state_path.write_text(json.dumps(missing), encoding="utf-8")
        expect_validation_error(
            lambda: FieldState.load(state_path),
            "missing required field(s): next_action",
        )
        print("PASS: missing required state rejected")

        # Attempt bounds must fail.
        invalid_attempt = original.to_dict()
        invalid_attempt["attempt"] = 4
        invalid_attempt["max_attempts"] = 3
        expect_validation_error(
            lambda: FieldState.from_dict(invalid_attempt),
            "attempt must be between 0 and max_attempts",
        )
        print("PASS: invalid attempt bounds rejected")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
