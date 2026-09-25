#!/usr/bin/env python3
"""Goblin Folder type manager.

Creates and recognizes two installed directory types:
- goblin-holder: supervisory foreman over child watched folders
- owatch: locally watched editing folder

Type identity is stored in Linux extended attributes when supported and mirrored
to hidden marker files for portability through Git and filesystems without xattr.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

XATTR_KEY = "user.onewave.folder_type"
HOLDER_TYPE = "goblin-holder"
OWATCH_TYPE = "owatch"
REGISTRY_PATH = Path(os.environ.get(
    "GOBLIN_FOLDER_REGISTRY",
    str(Path.home()/".local/share/goblin-folder/registry.json"),
)).expanduser()

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _load_registry() -> dict:
    try:
        doc=json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        if isinstance(doc, dict):
            doc.setdefault("schema","one-wave-folder-registry-v1")
            doc.setdefault("folders",{})
            return doc
    except (OSError, json.JSONDecodeError):
        pass
    return {"schema":"one-wave-folder-registry-v1","folders":{}}

def _save_registry(doc: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(doc, indent=2, sort_keys=True)+"\n", encoding="utf-8")

def _nearest_holder(path: Path) -> str | None:
    current=path.resolve().parent
    while True:
        if (current/".goblin-holder"/"holder.json").is_file():
            return str(current)
        if current.parent == current:
            return None
        current=current.parent

def _register(path: Path, kind: str, *, xattr: bool) -> dict:
    real=path.resolve()
    doc=_load_registry()
    marker = ".goblin-holder/holder.json" if kind == HOLDER_TYPE else ".owatch/folder.json"
    doc["folders"][str(real)] = {
        "path": str(real),
        "type": kind,
        "marker": marker,
        "xattr": bool(xattr),
        "holder": None if kind == HOLDER_TYPE else _nearest_holder(real),
        "registered_at": _now(),
        "last_verified_at": _now(),
    }
    _save_registry(doc)
    return doc["folders"][str(real)]

def registry_list() -> dict:
    doc=_load_registry()
    live={}
    stale={}
    for path, entry in sorted(doc.get("folders",{}).items()):
        p=Path(path)
        marker=p/entry.get("marker","")
        (live if p.is_dir() and marker.is_file() else stale)[path]=entry
    return {"registry":str(REGISTRY_PATH),"live":live,"stale":stale}


def _set_xattr(path: Path, value: str) -> bool:
    try:
        os.setxattr(path, XATTR_KEY, value.encode())
        return True
    except (AttributeError, OSError):
        return False

def _get_xattr(path: Path) -> str | None:
    try:
        return os.getxattr(path, XATTR_KEY).decode()
    except (AttributeError, OSError, UnicodeDecodeError):
        return None

def _write_json(path: Path, doc: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def make_holder(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    xattr = _set_xattr(path, HOLDER_TYPE)
    _write_json(path/".goblin-holder"/"holder.json", {
        "schema":"one-wave-goblin-folder-holder-v1",
        "type":HOLDER_TYPE,
        "display_name":"Goblin Folder Holder",
        "role":"foreman",
        "discovers":".owatch/folder.json",
        "mode":"fail_closed",
        "reference_required":True,
        "intention_required":True,
        "consequence_required":True,
        "commit_gate":True,
        "filesystem_xattr": XATTR_KEY if xattr else None,
    })
    (path/".goblin-holder"/".gitignore").write_text("group-index.json\nevents.jsonl\nHOLD.json\n", encoding="utf-8")
    entry=_register(path,HOLDER_TYPE,xattr=xattr)
    return {"path":str(path),"type":HOLDER_TYPE,"xattr":xattr,"registry":entry}

def make_owatch(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    xattr = _set_xattr(path, OWATCH_TYPE)
    _write_json(path/".owatch"/"folder.json", {
        "schema":"one-wave-watched-folder-v1",
        "type":OWATCH_TYPE,
        "mode":"fail_closed",
        "editing_granularity":["word","sentence","line","section","file"],
        "reference_required":True,
        "intention_required":True,
        "consequence_required":True,
        "source_files_authoritative":True,
        "filesystem_xattr": XATTR_KEY if xattr else None,
    })
    (path/".owatch"/".gitignore").write_text("state.json\nevents.jsonl\nHOLD.json\nindex.json\n", encoding="utf-8")
    entry=_register(path,OWATCH_TYPE,xattr=xattr)
    return {"path":str(path),"type":OWATCH_TYPE,"xattr":xattr,"registry":entry}

def detect(path: Path) -> dict:
    if not path.is_dir():
        raise SystemExit(f"not a directory: {path}")
    value = _get_xattr(path)
    if value in {HOLDER_TYPE, OWATCH_TYPE}:
        return {"path":str(path),"type":value,"source":"xattr"}
    if (path/".goblin-holder"/"holder.json").is_file():
        return {"path":str(path),"type":HOLDER_TYPE,"source":"marker"}
    if (path/".owatch"/"folder.json").is_file():
        return {"path":str(path),"type":OWATCH_TYPE,"source":"marker"}
    return {"path":str(path),"type":"ordinary-folder","source":"none"}

def adopt(path: Path, kind: str):
    if kind == HOLDER_TYPE:
        return make_holder(path)
    if kind == OWATCH_TYPE:
        return make_owatch(path)
    raise SystemExit(f"unknown kind: {kind}")

def main():
    ap=argparse.ArgumentParser(prog="goblin-folder")
    sub=ap.add_subparsers(dest="cmd", required=True)

    p=sub.add_parser("create-holder")
    p.add_argument("path")
    p=sub.add_parser("create-watch")
    p.add_argument("path")
    p=sub.add_parser("adopt")
    p.add_argument("kind", choices=[HOLDER_TYPE,OWATCH_TYPE])
    p.add_argument("path")
    p=sub.add_parser("type")
    p.add_argument("path")
    p=sub.add_parser("children")
    p.add_argument("path")
    sub.add_parser("registry")

    a=ap.parse_args()
    if a.cmd=="registry":
        print(json.dumps(registry_list(), indent=2, sort_keys=True))
        return
    path=Path(getattr(a,"path",".")).expanduser().resolve()
    if a.cmd=="create-holder":
        result=make_holder(path)
    elif a.cmd=="create-watch":
        result=make_owatch(path)
    elif a.cmd=="adopt":
        result=adopt(path,a.kind)
    elif a.cmd=="type":
        result=detect(path)
    elif a.cmd=="children":
        if detect(path)["type"] != HOLDER_TYPE:
            raise SystemExit("target is not a Goblin Folder Holder")
        children=[]
        for marker in path.rglob(".owatch/folder.json"):
            child=marker.parent.parent
            children.append(detect(child))
        result={"path":str(path),"children":children}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__=="__main__":
    main()
