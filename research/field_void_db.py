#!/usr/bin/env python3
"""Field/Void reference database builder. Stdlib only; no inference of physical truth."""
import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources(
 id INTEGER PRIMARY KEY, path TEXT UNIQUE NOT NULL, sha256 TEXT NOT NULL, text TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS nodes(
 id INTEGER PRIMARY KEY, source_id INTEGER NOT NULL REFERENCES sources(id),
 label TEXT NOT NULL, kind TEXT NOT NULL, field_text TEXT NOT NULL,
 void_text TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'UNVERIFIED',
 UNIQUE(source_id,label,kind));
CREATE TABLE IF NOT EXISTS links(
 from_id INTEGER NOT NULL REFERENCES nodes(id),
 to_id INTEGER NOT NULL REFERENCES nodes(id), relation TEXT NOT NULL,
 PRIMARY KEY(from_id,to_id,relation));
CREATE INDEX IF NOT EXISTS node_labels ON nodes(label);
"""
HEAD = re.compile(r"^(#{1,6})\s+(.+)$", re.M)
REF = re.compile(r"\b(?:A|W|D|G)-\d{1,4}\b")
SKIP = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}

def chunks(text):
    matches = list(HEAD.finditer(text))
    if not matches:
        return [("document", text)]
    out = []
    if text[:matches[0].start()].strip():
        out.append(("preamble", text[:matches[0].start()]))
    for i, m in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        out.append((m.group(2).strip()[:200], text[m.end():end].strip()))
    return out

def build(root, dest):
    root, dest = Path(root).resolve(), Path(dest).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(dest))
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    count = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt"} or any(x in SKIP for x in p.relative_to(root).parts):
            continue
        if p.resolve() == dest or p.stat().st_size > 2_000_000:
            continue
        raw = p.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        path = str(p.relative_to(root))
        digest = hashlib.sha256(raw).hexdigest()
        conn.execute("INSERT INTO sources(path,sha256,text) VALUES(?,?,?) ON CONFLICT(path) DO UPDATE SET sha256=excluded.sha256,text=excluded.text", (path,digest,text))
        source_id = conn.execute("SELECT id FROM sources WHERE path=?", (path,)).fetchone()[0]
        conn.execute("DELETE FROM links WHERE from_id IN (SELECT id FROM nodes WHERE source_id=?) OR to_id IN (SELECT id FROM nodes WHERE source_id=?)", (source_id,source_id))
        conn.execute("DELETE FROM nodes WHERE source_id=?", (source_id,))
        for index,(label,body) in enumerate(chunks(text)):
            # Field is the verbatim claim; Void is the explicitly unresolved check.
            status = "UNVERIFIED"
            if re.search(r"\b(rejected|dismissed)\b",body[:500],re.I): status="REVIEW_STATUS"
            conn.execute("INSERT INTO nodes(source_id,label,kind,field_text,void_text,status) VALUES(?,?,?,?,?,?)",
                         (source_id,f"{index:04d} {label}","section",body,
                          "Check source authority, assumptions, units, counterexamples, evidence and falsification.",status))
        count += 1
    # Exact ID references only; links are references, not causal proof.
    by_ref = {}
    rows = conn.execute("SELECT id,label,field_text FROM nodes").fetchall()
    for node_id,label,body in rows:
        for key in set(REF.findall(label)):
            by_ref.setdefault(key,set()).add(node_id)
    for node_id,label,body in rows:
        for key in set(REF.findall(body)):
            for target in by_ref.get(key,set()):
                if target != node_id:
                    conn.execute("INSERT OR IGNORE INTO links VALUES(?,?,?)",(node_id,target,"mentions"))
    conn.commit()
    result = {"sources":count,"nodes":conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0],
              "links":conn.execute("SELECT COUNT(*) FROM links").fetchone()[0],"database":str(dest)}
    conn.close()
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("root",help="Path to One-Wave Science checkout")
    p.add_argument("--db",default="field_void.sqlite")
    p.add_argument("--search",help="Search stored Field text and labels")
    args=p.parse_args()
    if args.search:
        with sqlite3.connect(args.db) as conn:
            rows=conn.execute("""SELECT sources.path,nodes.label,nodes.status FROM nodes JOIN sources ON sources.id=nodes.source_id
               WHERE nodes.field_text LIKE ? OR nodes.label LIKE ? LIMIT 40""",('%'+args.search+'%','%'+args.search+'%')).fetchall()
        print(json.dumps(rows,indent=2))
    else:
        print(json.dumps(build(args.root,args.db),indent=2))
if __name__=="__main__": main()
