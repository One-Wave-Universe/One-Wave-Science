"""Step 01 executable shell verification.

Run from repository root:
    python3 Field_Coder/tests/test_shell.py
"""

from pathlib import Path
import subprocess
import sys

FIELD_ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = FIELD_ROOT / "field" / "controller.py"
COMPONENT = FIELD_ROOT / "field" / "shell_component.py"
BACKUP = FIELD_ROOT / "field" / "shell_component.py.step01-test-backup"


def run_controller() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CONTROLLER)],
        cwd=FIELD_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(COMPONENT.is_file(), "required shell component missing before test")
    require(not BACKUP.exists(), "stale Step 01 backup exists")

    initial = run_controller()
    require(initial.returncode == 0, f"initial shell failed: {initial.stderr}")
    require(initial.stdout.strip() == "FIELD_SHELL_READY", initial.stdout)
    print("PASS: initial FIELD_SHELL_READY")

    COMPONENT.rename(BACKUP)
    try:
        missing = run_controller()
        require(missing.returncode != 0, "missing component was not rejected")
        require(
            missing.stdout.strip()
            == "FIELD_SHELL_MISSING_COMPONENT: shell_component.py",
            missing.stdout,
        )
        print("PASS: deliberate missing component detected")
    finally:
        if BACKUP.exists():
            BACKUP.rename(COMPONENT)

    restored = run_controller()
    require(restored.returncode == 0, f"restored shell failed: {restored.stderr}")
    require(restored.stdout.strip() == "FIELD_SHELL_READY", restored.stdout)
    print("PASS: restored FIELD_SHELL_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
