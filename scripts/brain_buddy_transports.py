#!/usr/bin/env python3
"""Brain Buddy transport adapters.

Prefer local authenticated model clients. Fall back only to configured supported
routes. This module never stores credentials.
"""
from __future__ import annotations
import json, os, shutil, subprocess
from pathlib import Path
from typing import Any

class TransportError(RuntimeError): pass

def _run(cmd: list[str], root: Path, timeout: int) -> str:
    try:
        p=subprocess.run(cmd,cwd=root,text=True,capture_output=True,timeout=timeout,check=False)
    except subprocess.TimeoutExpired as exc:
        raise TransportError(f"transport timeout after {timeout}s") from exc
    if p.returncode:
        raise TransportError((p.stderr or p.stdout or f"exit {p.returncode}").strip())
    return p.stdout.strip()

def _gemini_text(raw: str) -> str:
    try: obj=json.loads(raw)
    except json.JSONDecodeError: return raw.strip()
    if isinstance(obj,str): return obj
    if isinstance(obj,dict):
        for key in ("response","text","content","output"):
            if isinstance(obj.get(key),str) and obj[key].strip(): return obj[key].strip()
    return raw.strip()

def gemini(root: Path, prompt: str, timeout: int) -> str:
    exe=shutil.which("gemini")
    if not exe:
        local=Path.home()/".local/bin/gemini"
        exe=str(local) if local.exists() else ""
    if not exe: raise TransportError("Gemini CLI unavailable")
    raw=_run([exe,"--skip-trust","--extensions","none","--model","flash-lite",
              "--approval-mode","default","--output-format","json","--prompt",prompt],root,timeout)
    return _gemini_text(raw)

def deepseek(root: Path, prompt: str, timeout: int) -> str:
    if os.environ.get("DEEPSEEK_API_KEY"):
        raw=_run(["python3","One_Wave_Bench/hive-pipe/deepseek_bridge.py",
                  "--max-tool-rounds","12",prompt],root,timeout)
        return raw
    base=os.environ.get("DEEPSEEK_WEB_BASE_URL","http://192.168.55.100:3000")
    env=os.environ.copy(); env["DEEPSEEK_WEB_BASE_URL"]=base
    env.setdefault("DEEPSEEK_WEB_API_KEY","usb-local")
    try:
        p=subprocess.run(["python3","One_Wave_Bench/hive-pipe/deepseek_web_bridge.py",
                          "--max-tool-rounds","12",prompt],cwd=root,text=True,capture_output=True,
                         timeout=timeout,check=False,env=env)
    except subprocess.TimeoutExpired as exc:
        raise TransportError(f"DeepSeek transport timeout after {timeout}s") from exc
    if p.returncode:
        raise TransportError("DeepSeek has no reachable configured route: "+(p.stderr or p.stdout).strip())
    return p.stdout.strip()

def run(root: Path, worker: str, prompt: str, timeout: int) -> str:
    if worker=="gemini": return gemini(root,prompt,timeout)
    if worker=="deepseek": return deepseek(root,prompt,timeout)
    raise TransportError(f"unknown worker: {worker}")
