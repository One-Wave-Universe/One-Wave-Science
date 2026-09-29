#!/usr/bin/env python3
"""Bounded patch/update lane for One-Wave AI bridges.

Supports repository updates and user-space installers inside authorized roots.
Privileged OS package changes are delegated to a separate allowlisted helper.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path

def run(argv, cwd=None):
    r=subprocess.run(argv,cwd=cwd,text=True,capture_output=True,check=False)
    return {"argv":argv,"cwd":str(cwd) if cwd else None,"exit_code":r.returncode,"stdout":r.stdout,"stderr":r.stderr}

def repo_root(path: Path) -> Path:
    r=subprocess.run(["git","-C",str(path),"rev-parse","--show-toplevel"],text=True,capture_output=True,check=False)
    if r.returncode: raise SystemExit(r.stderr.strip() or "not a git repository")
    return Path(r.stdout.strip()).resolve()

def require_clean_scope(root: Path, scope: str):
    checker=root/"One_Wave_Bench/hive-pipe/higher_watcher.py"
    if checker.is_file():
        r=subprocess.run([sys.executable,str(checker),"--root",str(root),"--check","--scope",scope],
                         text=True,capture_output=True,check=False)
        if r.returncode:
            raise SystemExit("Goblin update HOLD:\n"+r.stdout+r.stderr)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=os.environ.get("ONE_WAVE_PROJECT_ROOT","."))
    sub=ap.add_subparsers(dest="action",required=True)

    p=sub.add_parser("git-fetch")
    p.add_argument("--remote",default="origin")
    p.add_argument("--ref",action="append",default=[])

    p=sub.add_parser("git-apply")
    p.add_argument("patch")
    p.add_argument("--scope",required=True)

    p=sub.add_parser("pip-user")
    p.add_argument("packages",nargs="+")
    p.add_argument("--upgrade",action="store_true")

    p=sub.add_parser("refresh-bridge")
    p.add_argument("--ref",default="origin/fix/no-runtime-clone")

    args=ap.parse_args()
    root=repo_root(Path(args.root).expanduser().resolve())

    if args.action=="git-fetch":
        argv=["git","-C",str(root),"fetch","--prune",args.remote,*args.ref]
        result=run(argv)
    elif args.action=="git-apply":
        require_clean_scope(root,args.scope)
        patch=Path(args.patch).expanduser().resolve()
        if not patch.is_file(): raise SystemExit("patch file missing")
        check=run(["git","-C",str(root),"apply","--check",str(patch)])
        if check["exit_code"]:
            print(json.dumps({"phase":"check","result":check},indent=2)); return check["exit_code"]
        result=run(["git","-C",str(root),"apply",str(patch)])
    elif args.action=="pip-user":
        argv=[sys.executable,"-m","pip","install","--user"]
        if args.upgrade: argv.append("--upgrade")
        argv.extend(args.packages)
        result=run(argv,cwd=root)
    elif args.action=="refresh-bridge":
        # Same repository; refresh the linked bridge worktree to the fetched ref.
        wt=Path(os.environ.get("XDG_STATE_HOME",str(Path.home()/".local/state")))/"one-wave-chatgpt-terminal/bridge-worktree"
        fetch=run(["git","-C",str(root),"fetch","origin"])
        if fetch["exit_code"]:
            print(json.dumps({"phase":"fetch","result":fetch},indent=2)); return fetch["exit_code"]
        result=run(["git","-C",str(wt),"checkout","--detach",args.ref]) if wt.is_dir() else {"exit_code":2,"stderr":"bridge worktree missing","stdout":"","argv":[],"cwd":str(wt)}
    else:
        raise SystemExit("unsupported action")

    print(json.dumps({"action":args.action,"root":str(root),"result":result},indent=2))
    return int(result.get("exit_code",1))

if __name__=="__main__":
    raise SystemExit(main())
