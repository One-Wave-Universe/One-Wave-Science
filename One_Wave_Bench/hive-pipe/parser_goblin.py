#!/usr/bin/env python3
"""Parser Goblin two-state relay and bridge-mesh foreman.

STATE ISSUE:
  validate reference/intention/consequence, classify current obstacles, and
  issue the exact request through the next authorized route.

STATE RETURN:
  require a matching receipt, relay stdout/stderr/exit/guidance durably, then
  flip back to ISSUE.

It never invents command success, never widens permissions, and never advances
without a matching receipt. Obstacles are classified and routed around when an
already-authorized alternate route exists.
"""
from __future__ import annotations

from datetime import datetime, timezone
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path
from typing import Any

SCRIPT_DIR=Path(__file__).resolve().parent
REPO_ROOT=Path(os.environ.get("ONE_WAVE_PROJECT_ROOT", str(SCRIPT_DIR.parent.parent))).expanduser().resolve()
sys.path.insert(0,str(SCRIPT_DIR))
import terminal_parser  # noqa:E402
import reference_receipt  # noqa:E402

STATE_ROOT=Path(os.environ.get("PARSER_GOBLIN_STATE_ROOT",str(Path.home()/".local/state/one-wave-parser-goblin"))).expanduser()
STATE_FILE=STATE_ROOT/"state.json"
INBOX=STATE_ROOT/"inbox"
OUTBOX=STATE_ROOT/"outbox"
POLL=max(2,int(os.environ.get("PARSER_GOBLIN_POLL_SECONDS","5")))
ISSUE="ISSUE"
RETURN="RETURN"

def now(): return datetime.now(timezone.utc).isoformat()

def atomic_json(path:Path,obj:dict[str,Any]):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(tmp,path)

def load_json(path:Path,default):
    try:
        v=json.loads(path.read_text(encoding="utf-8"))
        return v if isinstance(v,dict) else default
    except Exception:
        return default

def key_path(root:Path,rid:str):
    return root/(hashlib.sha256(rid.encode()).hexdigest()+".json")

def sh(args:list[str],cwd:Path|None=None,timeout:int=20):
    return subprocess.run(args,cwd=str(cwd or REPO_ROOT),text=True,capture_output=True,timeout=timeout,check=False)

def classify_obstacle(text:str)->dict[str,Any]:
    t=(text or "").lower()
    if "reference watcher hold" in t or "reference goblin hold" in t:
        return {"code":"REFERENCE_HOLD","retryable":False,"next":"Inspect/reconcile watcher/reference HOLD; do not bypass it."}
    if any(x in t for x in ["could not read username","authentication failed","publickey","repository not found"]):
        return {"code":"AUTHENTICATION","retryable":False,"next":"Repair existing route authentication outside payloads."}
    if any(x in t for x in ["permission denied","operation not permitted","read-only file system"]):
        return {"code":"PERMISSION_BOUNDARY","retryable":False,"next":"Use another already-authorized route or request the smallest operator action."}
    if any(x in t for x in ["no such file or directory","cwd is not a directory","path authorization"]):
        return {"code":"PATH","retryable":True,"next":"Inspect/correct path; do not guess."}
    if any(x in t for x in ["command not found","not found on path","executable file not found"]):
        return {"code":"MISSING_TOOL","retryable":False,"next":"Use another route with the tool or install it explicitly."}
    if any(x in t for x in ["timed out","timeout"]):
        return {"code":"TIMEOUT","retryable":True,"next":"Retry through next route or narrower bounded command."}
    if any(x in t for x in ["connection refused","network is unreachable","could not resolve host","connection reset"]):
        return {"code":"TRANSPORT","retryable":True,"next":"Fail over to the next authorized route."}
    if "repo-cleanup-inventory-20260924-01" in t or "pending=" in t:
        return {"code":"STALE_STATE","retryable":True,"next":"Run stale-state reconciler, then retry without reissuing completed work."}
    return {"code":"UNKNOWN","retryable":True,"next":"Preserve evidence and try the next authorized route once."}

def validate(raw:dict[str,Any])->dict[str,Any]:
    rid=raw.get("id"); argv=raw.get("argv"); cwd=raw.get("cwd") or str(REPO_ROOT); timeout=raw.get("timeout",120)
    intention=reference_receipt.required_text(raw.get("intention"),"intention")
    consequence=reference_receipt.required_text(raw.get("consequence"),"consequence")
    if not isinstance(rid,str) or not rid.strip() or len(rid)>128: raise ValueError("id must be non-empty <=128 chars")
    if not isinstance(argv,list) or not argv or not all(isinstance(x,str) and x for x in argv): raise ValueError("argv must be non-empty string array")
    if not isinstance(cwd,str) or not cwd.startswith("/"): raise ValueError("cwd must be absolute")
    if not isinstance(timeout,int) or not 1<=timeout<=terminal_parser.MAX_TIMEOUT: raise ValueError("timeout outside parser bounds")
    n={"id":rid.strip(),"argv":argv,"cwd":cwd,"timeout":timeout,"intention":intention,"consequence":consequence}
    n["digest"]=hashlib.sha256(json.dumps(n,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return n

def load_state():
    s=load_json(STATE_FILE,{})
    s.setdefault("version",1); s.setdefault("state",ISSUE); s.setdefault("active",None); s.setdefault("routes",{})
    return s

def save_state(s):
    s["updated_at"]=now(); atomic_json(STATE_FILE,s)

def route_local(req):
    try:
        reference_receipt.require_no_watcher_hold(REPO_ROOT)
        r=terminal_parser.run(req["argv"],cwd=req["cwd"],timeout=req["timeout"])
        return {"route":"local-parser","accepted":True,"completed":True,"receipt":r}
    except Exception as e:
        msg=f"{type(e).__name__}: {e}"
        return {"route":"local-parser","accepted":False,"completed":False,"error":msg,"obstacle":classify_obstacle(msg)}

def route_hive(req):
    # Use local Hive Pipe only if endpoint/token are already configured.
    token=Path.home()/".config/hive-pipe/tokens/codex.token"
    if not token.is_file():
        return {"route":"hive-mcp","accepted":False,"completed":False,"error":"codex token not configured","obstacle":{"code":"NOT_CONFIGURED","retryable":True}}
    py=(
      "import json,urllib.request,pathlib;"
      "tok=pathlib.Path.home().joinpath('.config/hive-pipe/tokens/codex.token').read_text().strip();"
      f"p={json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'terminal_run','arguments':{'argv':req['argv'],'cwd':req['cwd'],'timeout':req['timeout'],'intention':req['intention'],'consequence':req['consequence']}}})};"
      "d=json.dumps(p).encode();"
      "q=urllib.request.Request('http://127.0.0.1:8765/mcp',data=d,headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json'});"
      "print(urllib.request.urlopen(q,timeout=30).read().decode())"
    )
    r=sh(["python3","-c",py],timeout=min(req["timeout"]+10,300))
    if r.returncode:
        msg=r.stderr or r.stdout
        return {"route":"hive-mcp","accepted":False,"completed":False,"error":msg[-2000:],"obstacle":classify_obstacle(msg)}
    try:
        env=json.loads(r.stdout); sc=env.get("result",{}).get("structuredContent")
        if not isinstance(sc,dict): raise ValueError("missing structuredContent")
        return {"route":"hive-mcp","accepted":True,"completed":True,"receipt":sc}
    except Exception as e:
        msg=f"{type(e).__name__}: {e}"
        return {"route":"hive-mcp","accepted":False,"completed":False,"error":msg,"obstacle":classify_obstacle(msg)}

def route_pull(req):
    service=sh(["systemctl","--user","is-active","one-wave-chatgpt-terminal-pull.service"])
    if service.returncode:
        msg=service.stderr or service.stdout or "pull service inactive"
        return {"route":"pull-bridge","accepted":False,"completed":False,"error":msg,"obstacle":classify_obstacle(msg)}
    # This coordinator cannot mutate the remote transport branch itself on the target.
    # Persist a relay envelope for an authorized upstream bridge client to pick up.
    relay=STATE_ROOT/"relay"/"pull"
    atomic_json(key_path(relay,req["id"]),req)
    return {"route":"pull-bridge","accepted":True,"completed":False,"relay_file":str(key_path(relay,req["id"]))}

def route_github_actions(req):
    # Optional route only if gh exists and is already authenticated.
    if sh(["bash","-lc","command -v gh"]).returncode:
        return {"route":"github-actions","accepted":False,"completed":False,"error":"gh unavailable","obstacle":{"code":"NOT_CONFIGURED","retryable":True}}
    auth=sh(["gh","auth","status"])
    if auth.returncode:
        return {"route":"github-actions","accepted":False,"completed":False,"error":auth.stderr[-1500:],"obstacle":classify_obstacle(auth.stderr)}
    relay=STATE_ROOT/"relay"/"github-actions"
    atomic_json(key_path(relay,req["id"]),req)
    return {"route":"github-actions","accepted":True,"completed":False,"relay_file":str(key_path(relay,req["id"]))}

def try_routes(req,state):
    routes=[route_local,route_hive,route_pull,route_github_actions]
    attempts=[]
    for fn in routes:
        res=fn(req); attempts.append(res)
        state["routes"][res["route"]]={"at":now(),"accepted":res.get("accepted"),"completed":res.get("completed"),"error":res.get("error"),"obstacle":res.get("obstacle")}
        save_state(state)
        if res.get("completed"): return res,attempts
        if res.get("accepted"): return res,attempts
    return {"route":"durable-queue","accepted":True,"completed":False},attempts

def write_response(req,route,receipt,attempts):
    resp={"id":req["id"],"request_digest":req["digest"],"state":RETURN,"route":route,"received_at":now(),
          "ok":bool(receipt.get("ok")),"exit_code":receipt.get("exit_code"),"stdout":receipt.get("stdout",""),
          "stderr":receipt.get("stderr",""),"guidance":receipt.get("guidance"),"receipt":receipt,"attempts":attempts}
    atomic_json(key_path(OUTBOX,req["id"]),resp); return resp

def issue_once(state):
    files=sorted(INBOX.glob("*.json"),key=lambda p:p.stat().st_mtime)
    if not files:return False
    raw=load_json(files[0],{})
    req=validate(raw)
    reference_receipt.record({"phase":"issued","goblin":"parser-goblin","request_id":req["id"],"request_digest":req["digest"],
                              "intention":req["intention"],"consequence":req["consequence"],"reference":terminal_parser._project_reference(),"at":now()})
    res,attempts=try_routes(req,state)
    state["state"]=RETURN
    state["active"]={"id":req["id"],"digest":req["digest"],"request_file":str(files[0]),"route":res["route"],"attempts":attempts,"issued_at":now()}
    save_state(state)
    if res.get("completed"):
        resp=write_response(req,res["route"],res["receipt"],attempts)
        reference_receipt.record({"phase":"observed","goblin":"parser-goblin","request_id":req["id"],"request_digest":req["digest"],"response":resp,"at":now()})
    return True

def import_external_receipts(state):
    active=state.get("active")
    if not isinstance(active,dict): return False
    rid=active["id"]; digest=active["digest"]
    # Any authorized bridge can drop a matching receipt here.
    relay_receipts=STATE_ROOT/"relay-receipts"
    p=key_path(relay_receipts,rid)
    if not p.is_file(): return False
    receipt=load_json(p,{})
    if receipt.get("id")!=rid or receipt.get("request_digest") not in {None,digest}:
        return False
    req=load_json(Path(active["request_file"]),{})
    req=validate(req)
    resp=write_response(req,receipt.get("route","external-relay"),receipt,active.get("attempts",[]))
    reference_receipt.record({"phase":"observed","goblin":"parser-goblin","request_id":rid,"request_digest":digest,"response":resp,"at":now()})
    return True

def return_once(state):
    active=state.get("active")
    if not isinstance(active,dict):
        state["state"]=ISSUE; save_state(state); return True
    import_external_receipts(state)
    p=key_path(OUTBOX,active["id"])
    if not p.is_file(): return False
    resp=load_json(p,{})
    if resp.get("request_digest")!=active["digest"]: return False
    rf=Path(active["request_file"]); rf.unlink(missing_ok=True)
    state["last_response"]={"id":resp.get("id"),"ok":resp.get("ok"),"exit_code":resp.get("exit_code"),"route":resp.get("route"),"received_at":resp.get("received_at")}
    state["active"]=None; state["state"]=ISSUE; save_state(state); return True

def cycle(state): return issue_once(state) if state.get("state")==ISSUE else return_once(state)

def submit(a):
    req=validate({"id":a.id,"argv":a.argv,"cwd":a.cwd or str(REPO_ROOT),"timeout":a.timeout,"intention":a.intention,"consequence":a.consequence})
    atomic_json(key_path(INBOX,req["id"]),req)
    print(json.dumps({"queued":True,"id":req["id"],"digest":req["digest"]},indent=2)); return 0

def main():
    ap=argparse.ArgumentParser(description="Parser Goblin two-state bridge relay")
    sub=ap.add_subparsers(dest="cmd")
    s=sub.add_parser("submit"); s.add_argument("--id",required=True); s.add_argument("--cwd"); s.add_argument("--timeout",type=int,default=120)
    s.add_argument("--intention",required=True); s.add_argument("--consequence",required=True); s.add_argument("argv",nargs=argparse.REMAINDER)
    sub.add_parser("status")
    ap.add_argument("--watch",action="store_true"); ap.add_argument("--once",action="store_true")
    a=ap.parse_args()
    for d in [STATE_ROOT,INBOX,OUTBOX,STATE_ROOT/"relay",STATE_ROOT/"relay-receipts"]: d.mkdir(parents=True,exist_ok=True)
    if a.cmd=="submit":
        if not a.argv: ap.error("submit requires argv")
        return submit(a)
    if a.cmd=="status":
        print(json.dumps(load_state(),indent=2,sort_keys=True)); return 0
    state=load_state()
    if a.once:
        return 0 if cycle(state) else 2
    while True:
        state=load_state()
        cycle(state)
        if not a.watch: break
        time.sleep(POLL)
    return 0

if __name__=="__main__": raise SystemExit(main())
