#!/usr/bin/env python3
"""Bidirectional peer bridge for authorized One-Wave hosts.

Each host can be both a caller and a target. Peer definitions stay outside git
under ~/.config/one-wave-bridge/peers.json. Supported routes are authenticated
Hive Pipe MCP and SSH. The bridge tries routes in order and returns only a real
receipt; it never treats configuration as proof of execution.
"""

from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
import urllib.request, urllib.error

CONFIG = Path(os.environ.get("ONE_WAVE_PEERS_FILE", str(Path.home()/".config/one-wave-bridge/peers.json"))).expanduser()

def load_peers():
    return json.loads(CONFIG.read_text(encoding="utf-8"))

def run_mcp(route, argv, cwd, timeout, intention, consequence):
    token_file = Path(route["token_file"]).expanduser()
    token = token_file.read_text(encoding="utf-8").strip()
    args = {"argv": argv, "timeout": timeout, "intention": intention, "consequence": consequence}
    if cwd: args["cwd"] = cwd
    payload = {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"terminal_run","arguments":args}}
    req = urllib.request.Request(route["url"].rstrip("/")+"/mcp", data=json.dumps(payload).encode(),
        headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout+15) as r:
        env = json.load(r)
    if "error" in env: raise RuntimeError(json.dumps(env["error"]))
    result = env.get("result",{}).get("structuredContent",{})
    if not result.get("ok") and result.get("exit_code") not in (0,):
        raise RuntimeError(result.get("error") or result.get("stderr") or "MCP command failed")
    return {"route":"mcp","receipt":result}

def run_ssh(route, argv, timeout):
    host = route["host"]
    cmd = ["ssh","-o","BatchMode=yes","-o",f"ConnectTimeout={min(timeout,15)}"]
    if route.get("identity_file"): cmd += ["-i", str(Path(route["identity_file"]).expanduser())]
    cmd += [host, "--"] + argv
    r = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, check=False)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or f"ssh exit={r.returncode}")
    return {"route":"ssh","receipt":{"ok":True,"exit_code":r.returncode,"stdout":r.stdout,"stderr":r.stderr}}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("peer")
    p.add_argument("--cwd", default="")
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--intention", required=True)
    p.add_argument("--consequence", required=True)
    p.add_argument("argv", nargs=argparse.REMAINDER)
    a=p.parse_args()
    if a.argv and a.argv[0]=="--": a.argv=a.argv[1:]
    if not a.argv: p.error("command argv required after --")
    peers=load_peers()
    peer=peers["peers"][a.peer]
    errors=[]
    for route in peer.get("routes",[]):
        try:
            kind=route["type"]
            if kind=="mcp": out=run_mcp(route,a.argv,a.cwd,a.timeout,a.intention,a.consequence)
            elif kind=="ssh": out=run_ssh(route,a.argv,a.timeout)
            else: raise RuntimeError(f"unsupported route type {kind}")
            out["peer"]=a.peer
            print(json.dumps(out, indent=2))
            return 0
        except Exception as e:
            errors.append({"type":route.get("type"),"error":f"{type(e).__name__}: {e}"})
    print(json.dumps({"peer":a.peer,"ok":False,"errors":errors}, indent=2), file=sys.stderr)
    return 1

if __name__=="__main__": raise SystemExit(main())
