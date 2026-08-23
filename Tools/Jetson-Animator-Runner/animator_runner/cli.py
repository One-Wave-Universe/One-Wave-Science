#!/usr/bin/env python3
import argparse,json,os,shutil,sys,time,traceback
from datetime import datetime,timezone
from pathlib import Path
APP_NAME="one-wave-animator-runner"
DEFAULT_HOME=Path(os.environ.get("ONE_WAVE_RUNNER_HOME", Path.home()/".local/share/one-wave/animator-runner"))
def now(): return datetime.now(timezone.utc).isoformat()
def ensure(home):
    d={k:home/k for k in ("jobs","results","logs","state")}
    home.mkdir(parents=True,exist_ok=True)
    [p.mkdir(parents=True,exist_ok=True) for p in d.values()]
    d["home"]=home; return d
def writej(p,x):
    t=p.with_suffix(p.suffix+".tmp"); t.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n"); t.replace(p)
def log(d,event,**kw):
    with (d["logs"]/"runner.jsonl").open("a") as f: f.write(json.dumps({"time":now(),"event":event,**kw},sort_keys=True)+"\n")
def safe(root,rel):
    root=root.resolve(); p=(root/rel).resolve()
    if p!=root and root not in p.parents: raise ValueError("path escapes project_root")
    return p
def health(job,d):
    return {"runner":APP_NAME,"status":"ok","home":str(d["home"]),"python":sys.version.split()[0],"pid":os.getpid()}
def manifest(job,d):
    q=job.get("payload") or {}; root=Path(os.path.expandvars(q.get("project_root","."))).expanduser().resolve(); target=safe(root,q.get("path","."))
    if not target.exists(): raise FileNotFoundError(str(target))
    maxn=int(q.get("max_entries",500)); out=[]; seq=[target] if target.is_file() else sorted(target.rglob("*"))
    for p in seq[:maxn]: out.append({"path":str(p.relative_to(root)),"type":"dir" if p.is_dir() else "file","size":None if p.is_dir() else p.stat().st_size})
    return {"project_root":str(root),"requested_path":q.get("path","."),"count":len(out),"truncated":len(seq)>maxn,"entries":out}
def copyfile(job,d):
    q=job.get("payload") or {}; root=Path(os.path.expandvars(q["project_root"])).expanduser().resolve(); s=safe(root,q["source"]); t=safe(root,q["destination"])
    if not s.is_file(): raise FileNotFoundError(str(s))
    t.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(s,t)
    return {"source":str(s.relative_to(root)),"destination":str(t.relative_to(root)),"bytes":t.stat().st_size}
ACTIONS={"health":health,"project.manifest":manifest,"file.copy":copyfile}
def execute(job,d):
    jid=str(job.get("id") or "").strip(); action=str(job.get("action") or "").strip()
    if not jid: raise ValueError("job.id is required")
    if action not in ACTIONS: raise ValueError(f"unsupported action: {action}")
    started=now(); log(d,"job_start",job_id=jid,action=action)
    try:
        out=ACTIONS[action](job,d); r={"id":jid,"action":action,"status":"pass","started_at":started,"finished_at":now(),"output":out}; log(d,"job_pass",job_id=jid,action=action); return r
    except Exception as e:
        r={"id":jid,"action":action,"status":"fail","started_at":started,"finished_at":now(),"error":f"{type(e).__name__}: {e}","traceback":traceback.format_exc()}; log(d,"job_fail",job_id=jid,action=action,error=r["error"]); return r
def runfile(p,d):
    job=json.loads(Path(p).read_text()); r=execute(job,d); writej(d["results"]/(str(r["id"]).replace("/","_")+".result.json"),r); return r
def worker(d,once,interval):
    while True:
        jobs=sorted(d["jobs"].glob("*.json"))
        for p in jobs:
            q=p.with_suffix(".processing"); p.replace(q)
            try: r=runfile(q,d); print(json.dumps(r,indent=2))
            finally: q.unlink(missing_ok=True)
        if once:return 0
        if not jobs: time.sleep(interval)
def main(argv=None):
    p=argparse.ArgumentParser(prog="animator-runner"); p.add_argument("--home",default=str(DEFAULT_HOME)); s=p.add_subparsers(dest="cmd",required=True)
    s.add_parser("init"); a=s.add_parser("run"); a.add_argument("job"); w=s.add_parser("worker"); w.add_argument("--once",action="store_true"); w.add_argument("--interval",type=float,default=2.0); s.add_parser("actions")
    x=p.parse_args(argv); d=ensure(Path(x.home).expanduser())
    if x.cmd=="init": print(json.dumps({k:str(v) for k,v in d.items()},indent=2)); return 0
    if x.cmd=="run":
        r=runfile(x.job,d); print(json.dumps(r,indent=2)); return 0 if r["status"]=="pass" else 1
    if x.cmd=="worker": return worker(d,x.once,x.interval)
    if x.cmd=="actions": print("\n".join(sorted(ACTIONS))); return 0
if __name__=="__main__": raise SystemExit(main())
