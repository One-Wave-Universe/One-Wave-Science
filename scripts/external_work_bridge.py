#!/usr/bin/env python3
"""Bidirectional bridge between repo-tracked external-work handoff and Jetson workspace.

GitHub -> Jetson:
  External_Work/inbox/ -> ~/One-Wave-External-Work/inbox/

Jetson -> GitHub staging:
  ~/One-Wave-External-Work/outbox/ -> External_Work/outbox/

The bridge copies regular files only, refuses symlinks, never commits, never
pushes, and never writes directly to main. Git review remains explicit.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import os
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_INBOX = REPO_ROOT / "External_Work" / "inbox"
REPO_OUTBOX = REPO_ROOT / "External_Work" / "outbox"
LOCAL_ROOT = Path(os.environ.get("ONE_WAVE_EXTERNAL_WORK", "~/One-Wave-External-Work")).expanduser().resolve()
LOCAL_INBOX = LOCAL_ROOT / "inbox"
LOCAL_WORK = LOCAL_ROOT / "work"
LOCAL_OUTBOX = LOCAL_ROOT / "outbox"
MAX_FILE_BYTES = 64 * 1024 * 1024


def ensure_dirs() -> None:
    for path in (REPO_INBOX, REPO_OUTBOX, LOCAL_INBOX, LOCAL_WORK, LOCAL_OUTBOX):
        path.mkdir(parents=True, exist_ok=True)


def iter_regular_files(root: Path):
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlink refused: {path}")
        if path.is_file():
            if path.stat().st_size > MAX_FILE_BYTES:
                raise ValueError(f"file exceeds {MAX_FILE_BYTES} bytes: {path}")
            yield path


def copy_tree(source: Path, destination: Path) -> list[str]:
    ensure_dirs()
    copied: list[str] = []
    for source_path in iter_regular_files(source):
        relative = source_path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target)
        copied.append(str(relative))
    return copied


def status() -> int:
    ensure_dirs()
    print(f"repo_root={REPO_ROOT}")
    print(f"repo_inbox={REPO_INBOX}")
    print(f"repo_outbox={REPO_OUTBOX}")
    print(f"local_root={LOCAL_ROOT}")
    print(f"local_inbox={LOCAL_INBOX}")
    print(f"local_work={LOCAL_WORK}")
    print(f"local_outbox={LOCAL_OUTBOX}")
    print(f"repo_inbox_files={sum(1 for _ in iter_regular_files(REPO_INBOX))}")
    print(f"repo_outbox_files={sum(1 for _ in iter_regular_files(REPO_OUTBOX))}")
    print(f"local_inbox_files={sum(1 for _ in iter_regular_files(LOCAL_INBOX))}")
    print(f"local_outbox_files={sum(1 for _ in iter_regular_files(LOCAL_OUTBOX))}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("pull", "publish", "status"))
    args = parser.parse_args()
    try:
        if args.mode == "status":
            return status()
        if args.mode == "pull":
            copied = copy_tree(REPO_INBOX, LOCAL_INBOX)
            print(f"EXTERNAL_WORK_PULL copied={len(copied)}")
            for path in copied:
                print(path)
            return 0
        copied = copy_tree(LOCAL_OUTBOX, REPO_OUTBOX)
        print(f"EXTERNAL_WORK_PUBLISH copied={len(copied)}")
        for path in copied:
            print(path)
        print("Review with: git status --short External_Work/outbox")
        print("Commit/push only from a task branch; never auto-write main.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"EXTERNAL_WORK_BRIDGE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
