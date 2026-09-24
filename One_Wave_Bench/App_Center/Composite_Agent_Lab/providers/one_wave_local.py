#!/usr/bin/env python3
"""One-Wave Local AI provider.

This is the project-owned cognitive shell. A local text model supplies language
completion, but role separation, M4 state, hysteresis, memory, reference rules,
quality gates, and action authority remain outside the model.
"""
from __future__ import annotations
import json, os, urllib.request, urllib.error
from typing import Any

PLUGIN={
  "id":"one-wave-local",
  "name":"One-Wave Local AI",
  "kind":"local",
  "roles":["field","void"],
  "description":"Project-owned Field/Void cognitive shell over a local JSON chat endpoint.",
}

URL=os.environ.get("ONE_WAVE_LOCAL_AI_URL","http://127.0.0.1:11434/v1/chat/completions")
MODEL=os.environ.get("ONE_WAVE_LOCAL_AI_MODEL","local-model")
TIMEOUT=int(os.environ.get("ONE_WAVE_LOCAL_AI_TIMEOUT","90"))
MAX_TOKENS=int(os.environ.get("ONE_WAVE_LOCAL_AI_MAX_TOKENS","500"))

ROLE_INSTRUCTIONS={
  "FIELD_PERCEIVE": """You are FIELD: senses, perception, proposal, speech preparation. Read only the compact shared state. Return JSON only with perception, proposal, plan, speech_draft, drive (0..1), friction (0..1). Do not authorize yourself. Do not repeat full references or history.""",
  "FIELD_ACT": """You are FIELD: outward action and speech. Void/M4 constraints are authoritative. Return JSON only with action and speech. Keep action structured and bounded. Do not claim execution that has not happened.""",
  "VOID_ADMIN": """You are VOID: admin, inner voice, inhibition, continuity, reference authority. Return JSON only with decision (ALLOW/CORRECT/OVERRIDE/HOLD/ESCALATE), inner_voice, correction, reason, permissions, brake (0..1), support (0..1), contradiction (0..1). Be compact. Do not speak outward unless holding/escalating.""",
  "VOID_COMMIT": """You are VOID post-action commit authority. Compare result to reference, protected state, and expected consequence. Return JSON only with commit boolean, reason, next_state, and optional goal/reference updates. No self-congratulation; require evidence.""",
}

def _extract_json(text: str) -> dict[str,Any]:
    text=text.strip()
    if text.startswith("```"):
        text=text.strip("`")
        if text.startswith("json"): text=text[4:].lstrip()
    start=text.find("{"); end=text.rfind("}")
    if start<0 or end<start: raise ValueError("local model returned no JSON object")
    data=json.loads(text[start:end+1])
    if not isinstance(data,dict): raise ValueError("local model JSON must be an object")
    return data

def _post(messages: list[dict[str,str]]) -> dict[str,Any]:
    payload={
      "model":MODEL,
      "messages":messages,
      "temperature":0.2,
      "max_tokens":MAX_TOKENS,
      "response_format":{"type":"json_object"},
    }
    req=urllib.request.Request(URL,data=json.dumps(payload).encode("utf-8"),headers={"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=TIMEOUT) as response:
            env=json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8",errors="replace")) from exc
    choices=env.get("choices",[])
    if not choices: raise RuntimeError("local endpoint returned no choices")
    content=choices[0].get("message",{}).get("content","")
    return _extract_json(content)

def call(role: str, packet: dict[str,Any]) -> dict[str,Any]:
    instruction=ROLE_INSTRUCTIONS.get(role)
    if not instruction: raise ValueError(f"unsupported role {role}")
    compact=json.dumps(packet,separators=(",",":"),ensure_ascii=False)
    messages=[
      {"role":"system","content":instruction},
      {"role":"user","content":compact},
    ]
    return _post(messages)
