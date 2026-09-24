#!/usr/bin/env python3
"""Composite Agent Lab local app.

Small local web UI for configuring Field/Void providers and running the
sandboxed COMPOSITE_AGENT_V1 loop. Uses only Python stdlib for the app shell.
"""
from __future__ import annotations
import argparse, json, os, secrets, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parent
CONFIG=Path(os.environ.get("ONE_WAVE_COMPOSITE_APP_CONFIG", str(Path.home()/".config/one-wave/composite-agent-lab.json"))).expanduser()

def load_config():
    if not CONFIG.exists():
        return {"field_provider":"mock-field","void_provider":"mock-void","parser":"json-parser","sandbox":True}
    return json.loads(CONFIG.read_text(encoding="utf-8"))

def save_config(data):
    CONFIG.parent.mkdir(parents=True,exist_ok=True)
    CONFIG.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")

class Handler(BaseHTTPRequestHandler):
    server_version="CompositeAgentLab/0.1"
    def send_json(self,obj,status=200):
        raw=json.dumps(obj).encode(); self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        p=urlparse(self.path).path
        if p=="/api/config": return self.send_json(load_config())
        if p=="/api/providers":
            from provider_registry import registry_snapshot
            return self.send_json(registry_snapshot(ROOT/"providers"))
        if p=="/api/parsers":
            from parser_registry import registry_snapshot
            return self.send_json(registry_snapshot(ROOT/"parsers"))
        target=ROOT/("index.html" if p=="/" else p.lstrip("/"))
        if not target.is_file(): self.send_error(404); return
        raw=target.read_bytes(); c="text/html" if target.suffix==".html" else "text/javascript" if target.suffix==".js" else "text/css" if target.suffix==".css" else "application/octet-stream"
        self.send_response(200); self.send_header("Content-Type",c); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        n=int(self.headers.get("Content-Length","0")); data=json.loads(self.rfile.read(n) or b"{}")
        p=urlparse(self.path).path
        if p=="/api/config": save_config(data); return self.send_json({"ok":True})
        if p=="/api/run":
            try:
                from runtime import run_once
                return self.send_json(run_once(ROOT,data,load_config()))
            except Exception as e:
                return self.send_json({"ok":False,"error":f"{type(e).__name__}: {e}"},500)
        self.send_error(404)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--host",default="127.0.0.1"); ap.add_argument("--port",type=int,default=8788); ap.add_argument("--open",action="store_true"); a=ap.parse_args()
    server=ThreadingHTTPServer((a.host,a.port),Handler)
    url=f"http://{a.host}:{a.port}/"
    print("COMPOSITE_AGENT_LAB_READY",url,flush=True)
    if a.open: threading.Timer(.4,lambda:webbrowser.open(url)).start()
    server.serve_forever()

if __name__=="__main__": main()
