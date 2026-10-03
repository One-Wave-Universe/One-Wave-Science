#!/usr/bin/env python3
import argparse, json, os, urllib.request
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--repo-context",required=True)
ap.add_argument("--manifest",required=True)
ap.add_argument("--question",required=True)
ap.add_argument("--out",required=True)
a=ap.parse_args()
key=os.environ["GEMINI_API_KEY"]
ctx=Path(a.repo_context).read_text(encoding="utf-8",errors="replace")
manifest=Path(a.manifest).read_text(encoding="utf-8",errors="replace")
law="""You are inside the One-Wave repository lens.
The checked-out repository is the primary authority for One-Wave-specific claims.
Read GENERAL_REFERENCE_RULES.md and AI_CANONICAL_START_HERE.md first in the supplied repository context.
Use the entire supplied repository as available reference, not model memory.
Conventional science may be used for comparison, but clearly distinguish it from One-Wave hypotheses.
External metadata/data is a tool only when needed.
Never silently replace a repository-specific concept with a standard assumption.
Cite exact repository paths for One-Wave claims and mark unresolved conflicts."""
prompt=f"{law}\n\nQUESTION:\n{a.question}\n\nFULL REPOSITORY CONTEXT:\n{ctx}\n\nREPOSITORY FILE HASH MANIFEST:\n{manifest}"
payload={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.2}}
url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key="+key
req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
try:
    with urllib.request.urlopen(req,timeout=300) as r: obj=json.loads(r.read())
except Exception:
    # Some Gemini accounts expose Flash but not Pro; retry without weakening the lens.
    url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="+key
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=300) as r: obj=json.loads(r.read())
parts=obj["candidates"][0]["content"]["parts"]
answer="\n".join(x.get("text","") for x in parts).strip()
if not answer: raise SystemExit("Gemini returned no text")
required=("GENERAL_REFERENCE_RULES.md","AI_CANONICAL_START_HERE.md")
missing=[x for x in required if x not in answer]
status="PASS" if not missing else "FAIL_REFERENCE_GATE"
receipt=f"# Gemini One-Wave Lens Receipt\n\nStatus: **{status}**\n\nQuestion: {a.question}\n\n## Gemini\n\n{answer}\n\n## Gate\n\nRequired references missing from answer: {missing or 'none'}\n"
Path(a.out).write_text(receipt,encoding="utf-8")
print(status)
if missing: raise SystemExit(3)
