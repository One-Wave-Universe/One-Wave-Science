#!/usr/bin/env python3
"""Directory-scoped drift/reference watcher for One-Wave repositories."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

WATCHER_DIRNAME = ".watcher"
POLICY_NAME = "policy.json"
STATE_NAME = "state.json"
EVENTS_NAME = "events.jsonl"
HOLD_NAME = "HOLD.json"
INDEX_NAME = "index.json"

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def git(root: Path, *args: str) -> str:
    r = subprocess.run(['git','-C',str(root),*args], text=True, capture_output=True, check=False)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or f"git failed: {args}")
    return r.stdout.strip()

def repo_root(path: Path) -> Path:
    return Path(git(path, 'rev-parse', '--show-toplevel')).resolve()

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def snapshot(folder: Path) -> dict:
    root=repo_root(folder)
    rel=folder.resolve().relative_to(root)
    status_lines=git(root,'status','--porcelain','--',str(rel) if str(rel)!='.' else '.').splitlines()
    status='\n'.join(
        line for line in status_lines
        if '/.watcher/state.json' not in line
        and '/.watcher/events.jsonl' not in line
        and '/.watcher/HOLD.json' not in line
        and not line.endswith('.watcher/state.json')
        and not line.endswith('.watcher/events.jsonl')
        and not line.endswith('.watcher/HOLD.json')
    )
    tracked=git(root,'ls-files','--',str(rel) if str(rel)!='.' else '.').splitlines()
    files={}
    for item in tracked:
        p=root/item
        if p.is_file(): files[item]=sha256_file(p)
    return {
      'at':utc_now(), 'repo':str(root), 'folder':str(folder.resolve()),
      'branch':git(root,'branch','--show-current'), 'head':git(root,'rev-parse','HEAD'),
      'status':status, 'files':files
    }


def classify_file(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if name in {"agents.md", "readme.md", "ai_bridge_start_here.md", "ai_canonical_start_here.md"}:
        return "authority_or_entrypoint"
    if "grant" in name or "evidence" in name or "verification" in name:
        return "evidence_or_validation"
    if suffix in {".py", ".sh", ".js", ".ts", ".cpp", ".c", ".h", ".hpp"}:
        return "executable_or_source"
    if suffix in {".json", ".yaml", ".yml", ".toml", ".ini"}:
        return "configuration_or_data"
    if suffix in {".md", ".txt", ".rst"}:
        return "documentation_or_canon"
    return "artifact"



def text_anchors(path: Path) -> list[dict]:
    """Compact anchors for exact word/sentence/line edits without whole-file rewrite."""
    if path.suffix.lower() not in {".md", ".txt", ".rst", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"}:
        return []
    try:
        lines=path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    anchors=[]
    for idx,line in enumerate(lines, start=1):
        stripped=line.strip()
        if not stripped:
            continue
        digest=hashlib.sha256(line.encode("utf-8")).hexdigest()
        anchors.append({
            "line":idx,
            "sha256":digest,
            "preview":stripped[:180],
            "kind":"heading" if stripped.startswith("#") else "line",
        })
        if len(anchors)>=400:
            break
    return anchors

def first_heading(path: Path) -> str | None:
    if path.suffix.lower() not in {".md", ".txt", ".rst"}:
        return None
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:80]:
            stripped=line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()[:200] or None
    except OSError:
        return None
    return None


def build_index(folder: Path, snap: dict) -> dict:
    root=Path(snap["repo"])
    base=folder.resolve()
    child_dirs={}
    files=[]
    for repo_rel, digest in sorted(snap.get("files", {}).items()):
        p=root/repo_rel
        try:
            rel=p.resolve().relative_to(base)
        except ValueError:
            continue
        if any(part == WATCHER_DIRNAME for part in rel.parts):
            continue
        top = rel.parts[0] if len(rel.parts) > 1 else None
        if top:
            child_dirs.setdefault(top, {"file_count":0, "roles":{}})
            child_dirs[top]["file_count"] += 1
            role=classify_file(p)
            child_dirs[top]["roles"][role]=child_dirs[top]["roles"].get(role,0)+1
        files.append({
            "path": str(rel),
            "role": classify_file(p),
            "heading": first_heading(p),
            "sha256": digest,
            "bytes": p.stat().st_size if p.exists() else None,
            "anchors": text_anchors(p),
        })
    authorities=[
        item["path"] for item in files
        if item["role"] == "authority_or_entrypoint"
    ]
    return {
        "schema":"one-wave-watcher-index-v1",
        "generated_at":utc_now(),
        "folder":str(base),
        "repo":snap["repo"],
        "branch":snap["branch"],
        "head":snap["head"],
        "authority_files":authorities,
        "layers":{
            "folder_summary":{
                "file_count":len(files),
                "child_directory_count":len(child_dirs),
                "status":snap.get("status",""),
            },
            "subfolders":child_dirs,
            "files":files,
        },
        "editing_rule":"Descend folder -> subfolder -> file. Source files remain authoritative; this index is navigation only.",
    }


def refresh_index(folder: Path, snap: dict) -> None:
    wd=folder/WATCHER_DIRNAME
    wd.mkdir(parents=True, exist_ok=True)
    (wd/INDEX_NAME).write_text(
        json.dumps(build_index(folder, snap), indent=2, sort_keys=True)+"\n",
        encoding="utf-8",
    )

def load_json(path: Path, default):
    try:return json.loads(path.read_text())
    except Exception:return default

def append_event(path: Path, event: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(event, sort_keys=True)+'\n')

def watcher_dirs(root: Path):
    return [p.parent for p in root.rglob(f'{WATCHER_DIRNAME}/{POLICY_NAME}')]

def valid_receipt_after(ledger: Path, baseline_at: str, folder: Path) -> bool:
    if not ledger.is_file(): return False
    for line in reversed(ledger.read_text(errors='replace').splitlines()):
        try:e=json.loads(line)
        except Exception: continue
        if e.get('phase') not in {'issued','observed'}: continue
        card=e.get('reference_card') or {}
        ts=card.get('stamped_at') or e.get('at') or ''
        if ts <= baseline_at: break
        repo=(card.get('repository') or {}).get('root')
        if repo and str(folder.resolve()).startswith(str(Path(repo).resolve())):
            if card.get('intention') and card.get('consequence'): return True
    return False

def check_folder(folder: Path, ledger: Path) -> dict:
    wd=folder/WATCHER_DIRNAME
    policy=load_json(wd/POLICY_NAME,{})
    state=load_json(wd/STATE_NAME,{})
    current=snapshot(folder)
    baseline=state.get('baseline')
    if not baseline:
        refresh_index(folder, current)
        state={'baseline':current,'status':'BASELINED'}
        (wd/STATE_NAME).write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
        append_event(wd/EVENTS_NAME,{'type':'BASELINE','at':utc_now(),'snapshot':current})
        return {'folder':str(folder),'status':'BASELINED'}
    changed = current.get('files') != baseline.get('files') or current.get('status') != baseline.get('status')
    if not changed:
        refresh_index(folder, current)
        hold=wd/HOLD_NAME
        return {'folder':str(folder),'status':'HOLD' if hold.exists() else 'CLEAN'}
    if valid_receipt_after(ledger, baseline.get('at',''), folder):
        refresh_index(folder, current)
        state={'baseline':current,'status':'RECONCILED'}
        (wd/STATE_NAME).write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
        append_event(wd/EVENTS_NAME,{'type':'RECONCILED_CHANGE','at':utc_now(),'snapshot':current})
        try:(wd/HOLD_NAME).unlink()
        except FileNotFoundError:pass
        return {'folder':str(folder),'status':'RECONCILED'}
    refresh_index(folder, current)
    hold={
      'status':'HOLD','at':utc_now(),'folder':str(folder.resolve()),
      'reason':'File or Git state changed without a matching post-baseline reference receipt containing intention and consequence.',
      'baseline':baseline,'observed':current,
      'required_action':'Inspect the change, identify its source, issue a valid reference card, then reconcile before further mutation.'
    }
    (wd/HOLD_NAME).write_text(json.dumps(hold,indent=2,sort_keys=True)+'\n')
    append_event(wd/EVENTS_NAME,{'type':'UNREFERENCED_CHANGE','at':utc_now(),'hold':hold})
    return {'folder':str(folder),'status':'HOLD','reason':hold['reason']}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', default=os.environ.get('ONE_WAVE_PROJECT_ROOT','.'))
    ap.add_argument('--ledger', default=os.environ.get('REFERENCE_GATE_LEDGER',str(Path.home()/'.local/state/one-wave/reference-receipts.jsonl')))
    ap.add_argument('--watch', action='store_true')
    ap.add_argument('--interval', type=int, default=5)
    args=ap.parse_args()
    root=Path(args.root).expanduser().resolve()
    ledger=Path(args.ledger).expanduser()
    while True:
        results=[]
        for folder in watcher_dirs(root):
            try: results.append(check_folder(folder,ledger))
            except Exception as e: results.append({'folder':str(folder),'status':'ERROR','error':str(e)})
        print(json.dumps({'at':utc_now(),'results':results},sort_keys=True), flush=True)
        if not args.watch: return 1 if any(r.get('status') in {'HOLD','ERROR'} for r in results) else 0
        time.sleep(max(1,args.interval))

if __name__=='__main__':
    raise SystemExit(main())
