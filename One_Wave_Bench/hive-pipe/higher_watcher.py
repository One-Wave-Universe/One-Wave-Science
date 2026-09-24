#!/usr/bin/env python3
"""Higher-level anti-drift checker and commit gate for One-Wave repositories."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

WATCHER_DIRNAME=".watcher"
HOLD_NAME="HOLD.json"
INDEX_NAME="index.json"

def now():
    return datetime.now(timezone.utc).isoformat()

def run(root: Path, *args: str, check: bool=True):
    r=subprocess.run(['git','-C',str(root),*args],text=True,capture_output=True,check=False)
    if check and r.returncode:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or f"git failed: {args}")
    return r

def repo_root(path: Path) -> Path:
    return Path(run(path,'rev-parse','--show-toplevel').stdout.strip()).resolve()

def holds(root: Path):
    out=[]
    for p in root.rglob(f'{WATCHER_DIRNAME}/{HOLD_NAME}'):
        try: d=json.loads(p.read_text())
        except Exception: d={'status':'HOLD','reason':'Unreadable HOLD'}
        if d.get('status')=='HOLD': out.append({'path':str(p),**d})
    return out

def indexes(root: Path):
    out=[]
    for p in root.rglob(f'{WATCHER_DIRNAME}/{INDEX_NAME}'):
        try: out.append(json.loads(p.read_text()))
        except Exception: pass
    return out

def changed_paths(root: Path):
    r=run(root,'status','--porcelain',check=True)
    paths=[]
    for line in r.stdout.splitlines():
        if not line: continue
        path=line[3:].strip()
        if ' -> ' in path: path=path.split(' -> ',1)[1]
        if '/.watcher/' in path or path.startswith('.watcher/'): continue
        paths.append(path)
    return sorted(set(paths))

def receipt_ledger():
    return Path(os.environ.get('REFERENCE_GATE_LEDGER', str(Path.home()/'.local/state/one-wave/reference-receipts.jsonl'))).expanduser()

def latest_valid_receipt(ledger: Path):
    if not ledger.is_file(): return None
    for line in reversed(ledger.read_text(errors='replace').splitlines()):
        try:e=json.loads(line)
        except Exception: continue
        if e.get('phase') not in {'issued','observed'}: continue
        card=e.get('reference_card') or {}
        if card.get('intention') and card.get('consequence'): return {'event':e,'card':card}
    return None

def path_within_any(path: str, allowed: list[str]):
    return any(path==a or path.startswith(a.rstrip('/')+'/') for a in allowed)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', default=os.environ.get('ONE_WAVE_PROJECT_ROOT','.'))
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--commit-message')
    ap.add_argument('--scope', action='append', default=[], help='Allowed path/folder for this change; repeatable')
    args=ap.parse_args()
    root=repo_root(Path(args.root).expanduser().resolve())
    active_holds=holds(root)
    changed=changed_paths(root)
    receipt=latest_valid_receipt(receipt_ledger())
    result={
      'at':now(),'root':str(root),'changed_paths':changed,
      'active_holds':active_holds,'watcher_indexes':len(indexes(root)),
      'receipt_present':bool(receipt),'requested_scope':args.scope,
    }
    if active_holds:
        result['status']='HOLD'
        result['reason']='One or more folder watchers are holding unreferenced or unreconciled changes.'
        print(json.dumps(result,indent=2,sort_keys=True))
        return 2
    if changed and not receipt:
        result['status']='HOLD'
        result['reason']='Repository has changes but no valid reference receipt with intention and consequence.'
        print(json.dumps(result,indent=2,sort_keys=True))
        return 2
    if args.scope:
        outside=[p for p in changed if not path_within_any(p,args.scope)]
        if outside:
            result['status']='HOLD'
            result['reason']='Changes exist outside the explicitly authorized scope.'
            result['outside_scope']=outside
            print(json.dumps(result,indent=2,sort_keys=True))
            return 2
    result['status']='CLEAN'
    print(json.dumps(result,indent=2,sort_keys=True))
    if args.commit_message:
        if not changed:
            print('NO_CHANGES_TO_COMMIT')
            return 0
        run(root,'add','--',*changed)
        diff=run(root,'diff','--cached','--check',check=False)
        if diff.returncode:
            sys.stderr.write(diff.stdout+diff.stderr)
            return 3
        msg=args.commit_message.strip()
        if not msg:
            raise SystemExit('commit message required')
        meta='\n\nWatcher-Gate: clean\nReference-Receipt: present\n'
        if args.scope:
            meta+='Watcher-Scope: '+','.join(args.scope)+'\n'
        c=run(root,'commit','-m',msg+meta,check=False)
        sys.stdout.write(c.stdout)
        sys.stderr.write(c.stderr)
        return c.returncode
    return 0

if __name__=='__main__':
    raise SystemExit(main())
