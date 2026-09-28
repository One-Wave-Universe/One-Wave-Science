#!/usr/bin/env python3
"""Jetson Science Metadata Lens.

Fetches bounded PUBLIC metadata from scientific sources, normalizes it, caches
it outside Git, and exposes deterministic local search for AI/repo workers.
Raw experimental datasets are deliberately not mirrored by this program.

Sources:
- CERN Open Data records API
- GWOSC event API

The cache is evidence, not canon: repo changes must cite source URL + record ID.
"""
from __future__ import annotations
import argparse, json, os, sqlite3, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

CACHE=Path(os.environ.get("ONE_WAVE_SCIENCE_META_CACHE",
    Path.home()/".local/share/one-wave-science-metadata"))
DB=CACHE/"metadata.sqlite3"
UA="One-Wave-Science-Metadata-Lens/1.0"

SOURCES={
 "cern":"https://opendata.cern.ch/api/records/",
 "gwosc":"https://gwosc.org/api/v2/event-versions",
}

def fetch_json(url:str):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=30) as r:
  return json.load(r)

def db():
 CACHE.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(DB)
 c.execute("""create table if not exists records(
 source text not null, record_id text not null, title text, url text not null,
 payload text not null, fetched_at text not null,
 primary key(source,record_id))""")
 c.execute("create index if not exists idx_records_title on records(title)")
 return c

def text(v):
 if v is None:return ""
 if isinstance(v,str):return v
 return json.dumps(v,sort_keys=True)

def ingest_cern(limit:int):
 # Invenio records API: keep the request bounded.
 url=SOURCES["cern"]+"?"+urllib.parse.urlencode({"size":limit})
 data=fetch_json(url); hits=data.get("hits",{}).get("hits",[])
 out=[]
 for h in hits[:limit]:
  rid=str(h.get("id") or h.get("uuid") or "")
  md=h.get("metadata") or {}
  title=text(md.get("title") or md.get("titles") or rid)
  out.append((rid,title,h))
 return url,out

def ingest_gwosc(limit:int):
 url=SOURCES["gwosc"]+"?"+urllib.parse.urlencode({"page_size":limit})
 data=fetch_json(url)
 rows=data.get("results") if isinstance(data,dict) else data
 rows=rows if isinstance(rows,list) else []
 out=[]
 for h in rows[:limit]:
  rid=str(h.get("name") or h.get("event_version") or h.get("id") or "")
  title=text(h.get("name") or h.get("event") or rid)
  out.append((rid,title,h))
 return url,out

def sync(source:str,limit:int):
 fn={"cern":ingest_cern,"gwosc":ingest_gwosc}[source]
 source_url,rows=fn(limit); stamp=datetime.now(timezone.utc).isoformat()
 c=db()
 for rid,title,payload in rows:
  if not rid:continue
  c.execute("""insert into records values(?,?,?,?,?,?)
    on conflict(source,record_id) do update set
    title=excluded.title,url=excluded.url,payload=excluded.payload,fetched_at=excluded.fetched_at""",
    (source,rid,title,source_url,json.dumps(payload,sort_keys=True),stamp))
 c.commit();c.close()
 print(json.dumps({"source":source,"fetched":len(rows),"source_url":source_url,
                   "cache":str(DB),"at":stamp},sort_keys=True))

def search(q:str,limit:int):
 c=db(); needle=f"%{q}%"
 rows=c.execute("""select source,record_id,title,url,fetched_at,payload from records
  where title like ? or payload like ? order by fetched_at desc limit ?""",
  (needle,needle,limit)).fetchall();c.close()
 print(json.dumps([{"source":r[0],"record_id":r[1],"title":r[2],"source_url":r[3],
                    "fetched_at":r[4],"metadata":json.loads(r[5])} for r in rows],
                  indent=2,sort_keys=True))

def main():
 p=argparse.ArgumentParser()
 sub=p.add_subparsers(dest="cmd",required=True)
 s=sub.add_parser("sync");s.add_argument("source",choices=SOURCES);s.add_argument("--limit",type=int,default=25)
 q=sub.add_parser("search");q.add_argument("query");q.add_argument("--limit",type=int,default=10)
 a=p.parse_args()
 limit=max(1,min(a.limit,100))
 if a.cmd=="sync":sync(a.source,limit)
 else:search(a.query,limit)
if __name__=="__main__":main()
