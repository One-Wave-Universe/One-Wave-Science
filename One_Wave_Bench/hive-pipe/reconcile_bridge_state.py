#!/usr/bin/env python3
"""Safely reconcile stale One-Wave pull-bridge journal entries.

This does not delete the bridge state file and does not re-run commands.
A request is marked acknowledged only when:
- it is pending in the local journal,
- it is no longer the current request on either transport branch, and
- no durable result remains in the local outbox for delivery.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

STATE = Path.home()/".local/state/one-wave-chatgpt-terminal/bridge_state.json"
OUTBOX = Path.home()/".local/state/one-wave-chatgpt-terminal/outbox"
ROUTES = ["origin:chatgpt-terminal","origin:chatgpt-terminal-backup"]
REQUEST_PATH = ".chatgpt-terminal/request.json"

def now():
    return datetime.now(timezone.utc).isoformat()

def git_show(ref: str) -> dict | None:
    r=subprocess.run(["git","show",f"{ref}:{REQUEST_PATH}"],text=True,capture_output=True,check=False)
    if r.returncode:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None

def load_state():
    return json.loads(STATE.read_text())

def save_state(data):
    tmp=STATE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    tmp.replace(STATE)

def result_exists(request_id: str) -> bool:
    return (OUTBOX/f"{request_id}.json").exists()

def main():
    data=load_state()
    current_ids={r:(git_show(r) or {}).get("id") for r in ROUTES}
    changed=[]
    skipped=[]
    reqs=data.setdefault("requests",{})
    for rid, entry in reqs.items():
        phase=entry.get("phase")
        if phase=="acknowledged":
            continue
        if rid in current_ids.values():
            skipped.append({"id":rid,"reason":"still current on a transport route","phase":phase})
            continue
        if result_exists(rid):
            skipped.append({"id":rid,"reason":"durable result still awaits delivery","phase":phase})
            continue
        entry["phase"]="acknowledged"
        entry["reconciled_as_stale"]=True
        entry["reconciled_at"]=now()
        entry["reconcile_reason"]="request no longer present on transport routes and no durable result remains"
        changed.append(rid)

    if changed:
        data["updated_at"]=now()
        save_state(data)

    print(json.dumps({
        "transport_request_ids":current_ids,
        "acknowledged_stale":changed,
        "skipped":skipped,
        "state_file":str(STATE),
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
