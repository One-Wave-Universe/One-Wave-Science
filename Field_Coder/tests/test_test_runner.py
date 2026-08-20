"""Step 08 bounded success-test execution verification."""

from pathlib import Path
import sys
import tempfile

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.proposal import ImplementationProposal
from field.test_runner import run_success_test


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def proposal(command: str) -> ImplementationProposal:
    return ImplementationProposal(
        intended_change="fixture",
        reason="test runner fixture",
        files_expected=("fixture.py",),
        invariants=("runner returns evidence",),
        expected_result="command evidence captured",
        success_test=command,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "fixture.py").write_text("# fixture\n", encoding="utf-8")

        passing = run_success_test(
            root,
            proposal("python3 -c \"print('runner-pass')\""),
            timeout_seconds=2.0,
        )
        require(passing.passed, repr(passing))
        require(passing.exit_code == 0, repr(passing.exit_code))
        require(passing.stdout.strip() == "runner-pass", passing.stdout)
        require(not passing.timed_out, repr(passing))
        print("PASS: successful command captured as passing evidence")

        failing = run_success_test(
            root,
            proposal("python3 -c \"import sys; print('runner-fail'); sys.exit(3)\""),
            timeout_seconds=2.0,
        )
        require(not failing.passed, repr(failing))
        require(failing.exit_code == 3, repr(failing.exit_code))
        require(failing.stdout.strip() == "runner-fail", failing.stdout)
        require(not failing.timed_out, repr(failing))
        print("PASS: nonzero command captured as failure evidence")

        timeout = run_success_test(
            root,
            proposal("python3 -c \"import time; print('before-timeout', flush=True); time.sleep(1)\""),
            timeout_seconds=0.05,
        )
        require(not timeout.passed, repr(timeout))
        require(timeout.timed_out, repr(timeout))
        require(timeout.exit_code is None, repr(timeout.exit_code))
        print("PASS: timeout captured as bounded failure evidence")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
