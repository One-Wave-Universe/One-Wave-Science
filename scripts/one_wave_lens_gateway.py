#!/usr/bin/env python3
"""Persistent One-Wave Lens app: canonical repo -> Field/Void -> validation -> receipt."""
from __future__ import annotations
import argparse, json, os, re, subprocess, time, urllib.request, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANDATORY=("GENERAL_REFERENCE_RULES.md","AI_CANONICAL_START_HERE.md")
TEXT_EXT={".md",".txt",".json",".yaml",".yml",".py"}
STOP={"this","that","with","from","have","what","when","where","which","your","about","into","through","using","does","will","would","could","should"}

def git_sha():
    return subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip()

def safe_file(rel):
    p=(ROOT/rel).resolve()
    if p!=ROOT and ROOT not in p.parents: raise ValueError("path escaped repo")
    if not p.is_file(): raise FileNotFoundError(rel)
    return p

def terms(q):
    return [x for x in re.findall(r"[A-Za-z0-9_+-]{3,}",q.lower()) if x not in STOP][:30]

def retrieve(q, explicit=(), limit=8):
    """Select canonical files; content is read fresh every turn, never cached as canon."""
    chosen=list(MANDATORY)
    for x in explicit:
        if x not in chosen: chosen.append(x)
    scored=[]
    ts=terms(q)
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix.lower() not in TEXT_EXT: continue
        rel=str(p.relative_to(ROOT))
        if rel in chosen: continue
        try: body=p.read_text(encoding="utf-8",errors="ignore")[:100000].lower()
        except OSError: continue
        name=rel.lower()
        score=sum((8 if t in name else 0)+(1 if t in body else 0) for t in ts)
        if score: scored.append((score,rel))
    for _,rel in sorted(scored,key=lambda x:(-x[0],x[1]))[:limit]:
        chosen.append(rel)
    refs=[]
    for rel in chosen:
        try:
            txt=safe_file(rel).read_text(encoding="utf-8",errors="replace")
            refs.append({"path":rel,"text":txt[:18000]})
        except (OSError,ValueError): pass
    return refs

def lens(question, explicit=()):
    return {"repo_sha":git_sha(),"question":question,"references":retrieve(question,explicit),
      "law":"Repository authority first. Memory and model priors are context only. External tools/data are optional evidence. Never silently replace missing repo evidence with a standard assumption."}

def prompt(role,pkt,peer=""):
    refs="\n\n".join(f"=== {r['path']} ===\n{r['text']}" for r in pkt["references"])
    return f"""ONE-WAVE LENS — FORCED REFERENCE
ROLE: {role}
CANONICAL REPO SHA: {pkt['repo_sha']}
QUESTION: {pkt['question']}
LAW: {pkt['law']}

Read the references before reasoning. For One-Wave-specific claims, the references outrank your pretrained assumptions. If repo authority and conventional knowledge differ, report the difference; do not silently normalize One-Wave into a standard architecture. External data/tools are optional and remain external evidence.

{refs}
{("\n=== PEER STATE ===\n"+peer) if peer else ""}

Output plain text with: ANSWER; REPO REFERENCES USED; EXTERNAL EVIDENCE/TOOLS (or none); UNRESOLVED/CONFLICTS (or none).
"""

class Provider:
    def __init__(self,name,url,token=""):
        self.name,self.url,self.token=name,url.rstrip("/"),token
    def ask(self,text):
        body=json.dumps({"messages":[{"role":"user","content":text}],"tools":[]}).encode()
        headers={"Content-Type":"application/json"}
        if self.token: headers["Authorization"]="Bearer "+self.token
        req=urllib.request.Request(self.url+"/v1/chat/completions",data=body,headers=headers)
        with urllib.request.urlopen(req,timeout=240) as r: obj=json.loads(r.read())
        msg=obj["choices"][0]["message"]
        out=msg.get("content")
        if not out or msg.get("tool_calls"): raise RuntimeError(f"{self.name}: non-text/tool response")
        return out.strip()

def providers():
    return {
      "gemini":Provider("gemini",os.getenv("OWL_GEMINI_URL","http://192.168.55.100:3001"),os.getenv("OWL_GEMINI_TOKEN","")),
      "deepseek":Provider("deepseek",os.getenv("OWL_DEEPSEEK_URL","http://192.168.55.100:3000"),os.getenv("OWL_DEEPSEEK_TOKEN","")),
    }

def validate(text,pkt):
    """Mechanical receipt validation: answer must identify at least one supplied repo path."""
    used=[r["path"] for r in pkt["references"] if r["path"] in text]
    return {"ok":bool(used),"used":used,"reason":"" if used else "answer named no supplied canonical reference"}

def run(question,field="gemini",void="deepseek",center="gemini",explicit=()):
    ps=providers(); pkt=lens(question,explicit)
    f=ps[field].ask(prompt("FIELD — construct from reference",pkt))
    fv=validate(f,pkt)
    v=ps[void].ask(prompt("VOID — attack Field for drift, unsupported assumptions, contradictions and missing controls",pkt,f))
    vv=validate(v,pkt)
    c=ps[center].ask(prompt("CENTER — recombine Field/Void and revalidate against the SAME reference",pkt,"FIELD:\n"+f+"\n\nVOID:\n"+v))
    cv=validate(c,pkt)
    receipt={"id":uuid.uuid4().hex,"time":time.time(),"repo_sha":pkt["repo_sha"],"question":question,
      "roles":{"field":field,"void":void,"center":center},"reference_paths":[r["path"] for r in pkt["references"]],
      "validation":{"field":fv,"void":vv,"center":cv},"field":f,"void":v,"answer":c}
    if not all(x["ok"] for x in (fv,vv,cv)):
        receipt["status"]="REJECTED_REFERENCE_BYPASS"
    else: receipt["status"]="PASS"
    return receipt

class API(BaseHTTPRequestHandler):
    def sendj(self,n,obj):
        b=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(n); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self,*a): pass
    def do_GET(self):
        if self.path=="/health": return self.sendj(200,{"ok":True,"repo_sha":git_sha(),"app":"one-wave-lens"})
        return self.sendj(404,{"error":"not found"})
    def do_POST(self):
        if self.path!="/ask": return self.sendj(404,{"error":"not found"})
        try:
            n=int(self.headers.get("Content-Length","0")); p=json.loads(self.rfile.read(n))
            q=str(p["question"]).strip()
            if not q: raise ValueError("empty question")
            out=run(q,p.get("field","gemini"),p.get("void","deepseek"),p.get("center","gemini"),p.get("references",[]))
            self.sendj(200,out)
        except Exception as e: self.sendj(500,{"error":str(e)})

def main():
    ap=argparse.ArgumentParser(description="One-Wave Lens app")
    sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("ask"); a.add_argument("question",nargs="+"); a.add_argument("--field",default="gemini"); a.add_argument("--void",default="deepseek"); a.add_argument("--center",default="gemini"); a.add_argument("--reference",action="append",default=[])
    s=sub.add_parser("serve"); s.add_argument("--bind",default="127.0.0.1"); s.add_argument("--port",type=int,default=3030)
    p=sub.add_parser("packet"); p.add_argument("question",nargs="+"); p.add_argument("--reference",action="append",default=[])
    x=ap.parse_args()
    if x.cmd=="serve": ThreadingHTTPServer((x.bind,x.port),API).serve_forever(); return
    q=" ".join(x.question)
    if x.cmd=="packet": print(json.dumps(lens(q,x.reference),indent=2)); return
    print(json.dumps(run(q,x.field,x.void,x.center,x.reference),indent=2,ensure_ascii=False))
if __name__=="__main__": main()
