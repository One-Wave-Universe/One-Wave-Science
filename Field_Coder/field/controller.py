"""Minimal executable controller for Field Coder Step 01."""

from pathlib import Path

READY_STATUS = "FIELD_SHELL_READY"
MISSING_STATUS = "FIELD_SHELL_MISSING_COMPONENT"
REQUIRED_COMPONENT = Path(__file__).with_name("shell_component.py")


def shell_status() -> tuple[bool, str]:
    """Return deterministic Step 01 shell readiness."""
    if not REQUIRED_COMPONENT.is_file():
        return False, f"{MISSING_STATUS}: shell_component.py"
    return True, READY_STATUS


def main() -> int:
    ready, status = shell_status()
    print(status)
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
