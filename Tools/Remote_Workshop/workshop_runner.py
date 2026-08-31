#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

WORKSHOP = Path.home() / ".onewave_workshop"
STATE = WORKSHOP / ".relay_last_id"


def safe_path(rel: str) -> Path:
    p = (WORKSHOP / (rel or ".")).resolve()
    if p != WORKSHOP and WORKSHOP not in p.parents:
        raise ValueError("path escapes workshop")
    return p


def run(argv, cwd=None, timeout=120):
    p = subprocess.run(argv, cwd=cwd or WORKSHOP, text=True, capture_output=True, timeout=timeout)
    return {
        "returncode": p.returncode,
        "stdout": p.stdout[-20000:],
        "stderr": p.stderr[-20000:],
    }


def execute(cmd):
    op = cmd.get("op")
    if op == "list":
        p = safe_path(cmd.get("path", "."))
        return {
            "path": str(p.relative_to(WORKSHOP)),
            "items": [
                {
                    "name": x.name,
                    "type": "dir" if x.is_dir() else "file",
                    "size": None if x.is_dir() else x.stat().st_size,
                }
                for x in sorted(p.iterdir(), key=lambda z: (not z.is_dir(), z.name.lower()))
            ],
        }
    if op == "read":
        p = safe_path(cmd["path"])
        return {"path": cmd["path"], "content": p.read_text(errors="replace")[:200000]}
    if op == "write":
        p = safe_path(cmd["path"])
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(cmd.get("content", ""))
        return {"ok": True, "path": cmd["path"]}
    if op == "mkdir":
        p = safe_path(cmd["path"])
        p.mkdir(parents=True, exist_ok=True)
        return {"ok": True, "path": cmd["path"]}
    if op == "run":
        p = safe_path(cmd["path"])
        if not p.is_file():
            raise ValueError("file not found")
        if p.suffix == ".py":
            return run(["python3", str(p)], cwd=p.parent)
        if p.suffix in (".sh", ".bash"):
            return run(["bash", str(p)], cwd=p.parent)
        raise ValueError("only .py/.sh files inside workshop can run")
    if op == "command":
        name = cmd.get("name")
        allowed = {
            "pwd": ["pwd"],
            "ls": ["ls", "-la"],
            "git-status": ["git", "status", "--short", "--branch"],
            "git-diff": ["git", "diff", "--"],
            "pytest": ["python3", "-m", "pytest", "-q"],
        }
        if name not in allowed:
            raise ValueError("command not allowed")
        return run(allowed[name])
    raise ValueError(f"unknown op: {op}")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: workshop_runner.py COMMAND_JSON RESULT_JSON")
    command_file = Path(sys.argv[1])
    result_file = Path(sys.argv[2])
    WORKSHOP.mkdir(parents=True, exist_ok=True)
    cmd = json.loads(command_file.read_text())
    cid = str(cmd.get("id", ""))
    if not cid:
        return 0
    if STATE.exists() and STATE.read_text().strip() == cid:
        return 0
    try:
        result = {"id": cid, "ok": True, "result": execute(cmd)}
    except Exception as e:
        result = {"id": cid, "ok": False, "error": str(e)}
    result_file.write_text(json.dumps(result, indent=2) + "\n")
    STATE.write_text(cid + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
