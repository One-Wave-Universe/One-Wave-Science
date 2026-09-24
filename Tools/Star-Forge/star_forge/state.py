from __future__ import annotations
import json
import os
import hashlib
import subprocess
import shutil
import time
import uuid
from pathlib import Path

LEVELS = {
    1: "Action",
    2: "Step",
    3: "Layer",
    4: "Build Phase",
    5: "Project State",
    6: "Project Loop",
}

DEFAULT_STATE = {
    "project": {
        "name": "Star Forge",
        "repo": "https://github.com/One-Wave-Universe/One-Wave-Science",
        "repo_path": "",
        "base_branch": "main",
        "base_head": "",
        "goal": "",
        "plan": [],
        "active_level": 1,
        "active_step_id": None,
        "checkpoint": None,
        "status": "IDLE",
        "loop_enabled": True,
        "standards": {
            "reference_required": True,
            "tests_required": True,
            "independent_void_required": True,
            "anti_drift_required": True,
            "simplicity_first": True,
            "ease_of_use_first": True,
            "usefulness_required": True,
            "reality_validation_required": True,
            "targeted_local_fixes": True,
            "explicit_layer_branch_scope": True,
        },
    },
    "bridges": {},
    "assignments": [],
    "council": [],
    "journal": [],
    "toc": [],
    "validation": {
        "stage": "CONCEPT",
        "stages": [
            "CONCEPT",
            "VIRTUAL_BREADBOARD",
            "CIRCUIT_SIMULATION",
            "VIRTUAL_PCB",
            "MANUFACTURABLE_DESIGN",
            "BENCH_TEST_PLAN",
            "PHYSICAL_BREADBOARD",
            "MEASURED_PHYSICAL",
            "SIMULATION_MEASUREMENT_COMPARE",
            "VALIDATED"
        ],
        "evidence": [],
        "usefulness": {
            "problem": "",
            "expected_user_value": "",
            "simplest_usable_outcome": "",
            "observed_value": "",
            "status": "UNPROVEN"
        }
    },
}

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def checked_repo_reference(state):
    """Read the real checkout; never accept a typed HEAD as reference proof."""
    raw = state["project"].get("repo_path", "")
    if not raw or not Path(raw).is_dir():
        raise ValueError("Reference HOLD: choose an existing local repository checkout.")
    path = Path(raw).expanduser().resolve()
    def git(*args):
        result = subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True, timeout=10)
        if result.returncode:
            raise ValueError(f"Reference HOLD: git {' '.join(args)} failed: {result.stderr.strip()}")
        return result.stdout.strip()
    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    if root != path:
        raise ValueError("Reference HOLD: select the repository root, not a subdirectory.")
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    status = git("status", "--porcelain", "-uno")
    if not branch:
        raise ValueError("Reference HOLD: choose a named branch or worktree.")
    authority = root / "AGENTS.md"
    if not authority.is_file():
        raise ValueError("Reference HOLD: AGENTS.md is missing from the checkout.")
    return {"time": now(), "root": str(root), "branch": branch, "head": head,
            "status": status, "agents_sha256": hashlib.sha256(authority.read_bytes()).hexdigest()}

def app_data_dir():
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    path = base / "branch-bridge-council"
    path.mkdir(parents=True, exist_ok=True)
    return path

def state_path():
    return app_data_dir() / "state.json"

def clone_default():
    return json.loads(json.dumps(DEFAULT_STATE))

def load_state():
    path = state_path()
    state = clone_default() if not path.exists() else json.loads(path.read_text())
    for key, value in DEFAULT_STATE.items():
        state.setdefault(key, json.loads(json.dumps(value)))
    for key, value in DEFAULT_STATE["project"].items():
        state["project"].setdefault(key, json.loads(json.dumps(value)))
    state.setdefault("toc", [])
    state.setdefault("validation", json.loads(json.dumps(DEFAULT_STATE["validation"])))
    for key, value in DEFAULT_STATE["validation"].items():
        state["validation"].setdefault(key, json.loads(json.dumps(value)))
    detect_builtin_bridges(state)
    save_state(state)
    return state

def save_state(state):
    path = state_path()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)

def detect_builtin_bridges(state):
    bridges = state["bridges"]
    bridges["github"] = {
        "name": "GitHub",
        "kind": "repository",
        "available": shutil.which("git") is not None,
        "capabilities": ["reference", "branches", "commits", "pull_requests"],
        "executable": shutil.which("git") or "",
    }
    bridges["python"] = {
        "name": "Python",
        "kind": "runtime",
        "available": shutil.which("python3") is not None,
        "capabilities": ["python", "scripts", "tests"],
        "executable": shutil.which("python3") or "",
    }
    bridges["powershell"] = {
        "name": "PowerShell",
        "kind": "runtime",
        "available": shutil.which("pwsh") is not None,
        "capabilities": ["powershell", "scripts"],
        "executable": shutil.which("pwsh") or "",
    }
    bridges["terminal"] = {
        "name": "Shell / Terminal",
        "kind": "runtime",
        "available": shutil.which("bash") is not None,
        "capabilities": ["shell", "terminal", "process"],
        "executable": shutil.which("bash") or "",
    }

def add_plan_step(state, title, goal, level):
    step = {
        "id": uuid.uuid4().hex[:10],
        "title": title.strip(),
        "goal": goal.strip(),
        "level": int(level),
        "status": "planned",
        "created_at": now(),
        "quality_gates": {
            "reference_supplied": True,
            "tests_required": True,
            "independent_void_required": True,
            "anti_drift_required": True,
            "simplicity_first": True,
            "ease_of_use_first": True,
        },
        "layer": int(level),
        "branch_scope": "",
        "allowed_files": [],
        "protected_files": [],
        "validation_stage": None,
    }
    state["project"]["plan"].append(step)
    if not state["project"].get("active_step_id"):
        state["project"]["active_step_id"] = step["id"]
        state["project"]["active_level"] = step["level"]
        state["project"]["status"] = "READY"
    return step

def active_step(state):
    sid = state["project"].get("active_step_id")
    return next((s for s in state["project"]["plan"] if s["id"] == sid), None)

def choose_bridge(state, step):
    text = (step.get("title", "") + " " + step.get("goal", "")).lower()
    prefs = []
    if "powershell" in text or "windows" in text:
        prefs.append("powershell")
    if "python" in text:
        prefs.append("python")
    if any(x in text for x in ("git", "github", "branch", "pull request", "pr ")):
        prefs.append("github")
    if any(x in text for x in ("shell", "terminal", "command", "process")):
        prefs.append("terminal")
    prefs += ["github", "python", "terminal", "powershell"]
    seen = set()
    for key in prefs:
        if key in seen:
            continue
        seen.add(key)
        bridge = state["bridges"].get(key)
        if bridge and bridge.get("available"):
            return key
    return None

def mediator_reference(state):
    step = active_step(state)
    return {
        "repo": state["project"].get("repo"),
        "base_branch": state["project"].get("base_branch"),
        "base_head": state["project"].get("base_head"),
        "project_goal": state["project"].get("goal"),
        "checkpoint": state["project"].get("checkpoint"),
        "active_level": state["project"].get("active_level"),
        "active_level_name": LEVELS.get(state["project"].get("active_level")),
        "active_step": step,
        "plan": state["project"].get("plan", []),
        "journal_head": state["journal"][0] if state["journal"] else None,
        "standards": state["project"].get("standards", {}),
        "validation": state.get("validation", {}),
        "project_map": project_map(state),
    }

def assign_pair(state, field_name, void_name):
    step = active_step(state)
    if not step:
        raise ValueError("No active project step.")
    verified_reference = checked_repo_reference(state)
    state["project"]["base_branch"] = verified_reference["branch"]
    state["project"]["base_head"] = verified_reference["head"]
    bridge = choose_bridge(state, step)
    if not bridge:
        state["project"]["status"] = "HOLD"
        raise ValueError("No authorized bridge is currently available.")
    assignment = {
        "id": uuid.uuid4().hex[:10],
        "step_id": step["id"],
        "level": step["level"],
        "field": field_name.strip(),
        "void": void_name.strip(),
        "bridge": bridge,
        "branch": step.get("branch_scope") or f"field/{step['id']}-{step['title'].lower().replace(' ', '-')[:32]}",
        "layer": step.get("layer", step["level"]),
        "allowed_files": step.get("allowed_files", []),
        "protected_files": step.get("protected_files", []),
        "validation_stage": step.get("validation_stage") or state.get("validation", {}).get("stage"),
        "status": "assigned",
        "reference": {**mediator_reference(state), "verified_checkout": verified_reference},
        "created_at": now(),
    }
    state["assignments"].append(assignment)
    step["status"] = "assigned"
    state["project"]["status"] = "EXECUTING"
    state["council"].append({
        "time": now(),
        "role": "MEDIATOR",
        "text": f"Assigned {step['title']} to FIELD={assignment['field']} / VOID={assignment['void']} via {bridge}.",
    })
    return assignment

def next_planned_step(state):
    return next((s for s in state["project"]["plan"] if s["status"] == "planned"), None)

def resolve_active(state, verdict, evidence, unresolved=""):
    step = active_step(state)
    if not step:
        raise ValueError("No active project step.")
    assignment = next((a for a in reversed(state["assignments"]) if a["step_id"] == step["id"]), None)
    observed = None

    if verdict == "ALLOW":
        if not assignment:
            raise ValueError("Mediator cannot ALLOW without a Field/Void assignment.")
        if not assignment.get("reference"):
            raise ValueError("Mediator cannot ALLOW without a supplied reference packet.")
        if not assignment["reference"].get("verified_checkout"):
            raise ValueError("Mediator cannot ALLOW without a verified checkout reference.")
        if not assignment.get("field") or not assignment.get("void"):
            raise ValueError("Mediator requires both Field and Void.")
        if assignment.get("field").strip().lower() == assignment.get("void").strip().lower():
            raise ValueError("Field and Void must be independent identities.")
        if not evidence.strip():
            raise ValueError("Mediator cannot ALLOW without test/check evidence.")
        observed = checked_repo_reference(state)
        original = assignment["reference"]["verified_checkout"]
        if observed["root"] != original["root"] or observed["agents_sha256"] != original["agents_sha256"]:
            raise ValueError("Reference HOLD: checkout or governing instructions changed.")
        if observed["branch"] != assignment["branch"]:
            raise ValueError("Reference HOLD: Field has not reached its assigned branch.")
        if observed["head"] == original["head"] and observed["status"] == original["status"]:
            raise ValueError("Reference HOLD: no observable change from the assigned baseline.")
    journal = {
        "time": now(),
        "step_id": step["id"],
        "level": step["level"],
        "title": step["title"],
        "field": assignment.get("field") if assignment else "",
        "void": assignment.get("void") if assignment else "",
        "bridge": assignment.get("bridge") if assignment else "",
        "branch": assignment.get("branch") if assignment else "",
        "verdict": verdict,
        "evidence": evidence.strip(),
        "unresolved": unresolved.strip(),
        "starting_checkpoint": state["project"].get("checkpoint"),
        "original_reference": assignment.get("reference") if assignment else None,
        "observed_checkout": observed,
        "layer": assignment.get("layer") if assignment else step.get("layer"),
        "branch_scope": assignment.get("branch") if assignment else step.get("branch_scope", ""),
        "allowed_files": assignment.get("allowed_files", []) if assignment else step.get("allowed_files", []),
        "protected_files": assignment.get("protected_files", []) if assignment else step.get("protected_files", []),
        "validation_stage": assignment.get("validation_stage") if assignment else step.get("validation_stage"),
        "toc_count": len(state.get("toc", [])),
        "quality_gate": {
            "reference_checked": bool(assignment and assignment.get("reference")),
            "tests_evidenced": bool(evidence.strip()),
            "independent_void": bool(
                assignment and assignment.get("field") and assignment.get("void")
                and assignment.get("field").strip().lower() != assignment.get("void").strip().lower()
            ),
            "anti_drift": "bounded to mediator-assigned step and project plan",
            "simplicity": "prefer smallest working change; complexity requires evidence",
            "ease_of_use": "prefer the least user-friction path that satisfies the step",
            "targeted_local_fix": "change only the mediator-released layer/branch/files unless evidence requires escalation",
        },
    }

    if verdict == "ALLOW":
        step["status"] = "resolved"
        checkpoint = f"{step['id']}:{now()}"
        journal["resulting_checkpoint"] = checkpoint
        state["project"]["checkpoint"] = checkpoint
        nxt = next_planned_step(state)
        if nxt:
            state["project"]["active_step_id"] = nxt["id"]
            state["project"]["active_level"] = nxt["level"]
            state["project"]["status"] = "READY"
            journal["next_step_id"] = nxt["id"]
        else:
            state["project"]["active_step_id"] = None
            state["project"]["status"] = "COMPLETE"
            journal["next_step_id"] = None
    else:
        step["status"] = verdict.lower()
        journal["resulting_checkpoint"] = state["project"].get("checkpoint")
        state["project"]["status"] = "HOLD" if verdict in ("HOLD", "ESCALATE") else "READY"

    state["journal"].insert(0, journal)
    state["council"].append({
        "time": now(),
        "role": "MEDIATOR",
        "text": f"Resolved {step['title']}: {verdict}. Canonical journal updated.",
    })
    return journal

def mediator_continue(state, field_name="Field AI", void_name="Void AI"):
    """One deterministic continuation turn owned by Mediator.

    Re-reference -> select current step -> choose bridge -> assign Field/Void.
    Stops only at COMPLETE or a real HOLD/ESCALATE condition.
    """
    if not state["project"].get("loop_enabled", True):
        return {"state": "HOLD", "reason": "Mediator loop disabled."}

    step = active_step(state)
    if not step:
        step = next_planned_step(state)
        if step:
            state["project"]["active_step_id"] = step["id"]
            state["project"]["active_level"] = step["level"]
            state["project"]["status"] = "READY"
        else:
            state["project"]["status"] = "COMPLETE"
            return {"state": "COMPLETE", "reference": mediator_reference(state)}

    if state["project"]["status"] in ("HOLD", "ESCALATE"):
        return {"state": state["project"]["status"], "reference": mediator_reference(state)}

    current = active_step(state)
    existing = next(
        (a for a in reversed(state["assignments"]) if a["step_id"] == current["id"] and a["status"] == "assigned"),
        None,
    )
    if existing:
        return {"state": "WAITING_FOR_FIELD_VOID", "assignment": existing, "reference": mediator_reference(state)}

    assignment = assign_pair(state, field_name, void_name)
    return {"state": "DISPATCHED", "assignment": assignment, "reference": mediator_reference(state)}


def set_step_scope(state, step_id, branch_scope="", allowed_files=None, protected_files=None, validation_stage=None):
    step = next((x for x in state["project"]["plan"] if x["id"] == step_id), None)
    if not step:
        raise ValueError("Unknown step.")
    if validation_stage and validation_stage not in state["validation"]["stages"]:
        raise ValueError("Unknown validation stage.")
    step["branch_scope"] = branch_scope.strip()
    step["allowed_files"] = list(allowed_files or [])
    step["protected_files"] = list(protected_files or [])
    step["validation_stage"] = validation_stage
    return step

def upsert_toc_entry(state, entry_id, name, kind, path="", layer=None, branch="", program="", tests=None, validation_stage="", purpose="", protected=False, notes=""):
    entry = next((x for x in state["toc"] if x["id"] == entry_id), None)
    payload = {
        "id": entry_id,
        "name": name.strip(),
        "kind": kind.strip(),
        "path": path.strip(),
        "layer": layer,
        "branch": branch.strip(),
        "program": program.strip(),
        "tests": list(tests or []),
        "validation_stage": validation_stage.strip(),
        "purpose": purpose.strip(),
        "protected": bool(protected),
        "notes": notes.strip(),
        "updated_at": now(),
    }
    if entry:
        entry.update(payload)
        return entry
    state["toc"].append(payload)
    return payload

def project_map(state):
    return {
        "project": {
            "goal": state["project"].get("goal"),
            "repo": state["project"].get("repo"),
            "base_branch": state["project"].get("base_branch"),
            "base_head": state["project"].get("base_head"),
            "checkpoint": state["project"].get("checkpoint"),
            "status": state["project"].get("status"),
        },
        "active_step": active_step(state),
        "toc": state.get("toc", []),
        "validation": state.get("validation", {}),
        "journal_head": state["journal"][0] if state["journal"] else None,
    }

def record_validation_evidence(state, stage, evidence, source="", measured=False):
    if stage not in state["validation"]["stages"]:
        raise ValueError("Unknown validation stage.")
    item = {"time": now(), "stage": stage, "evidence": evidence.strip(), "source": source.strip(), "measured": bool(measured)}
    state["validation"]["evidence"].append(item)
    state["validation"]["stage"] = stage
    return item

def set_usefulness(state, problem="", expected_user_value="", simplest_usable_outcome="", observed_value="", status=None):
    u = state["validation"]["usefulness"]
    if problem: u["problem"] = problem.strip()
    if expected_user_value: u["expected_user_value"] = expected_user_value.strip()
    if simplest_usable_outcome: u["simplest_usable_outcome"] = simplest_usable_outcome.strip()
    if observed_value: u["observed_value"] = observed_value.strip()
    if status:
        if status not in ("UNPROVEN", "PROMISING", "USEFUL", "NOT_USEFUL"):
            raise ValueError("Invalid usefulness status.")
        u["status"] = status
    return u

def bridge_receipt(state):
    detect_builtin_bridges(state)
    out = []
    for key, bridge in state["bridges"].items():
        out.append({
            "id": key,
            "name": bridge.get("name", key),
            "available": bool(bridge.get("available")),
            "executable": bridge.get("executable", ""),
            "capabilities": bridge.get("capabilities", []),
        })
    return out
