#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, shlex, socketserver, sqlite3, threading, time
from pathlib import Path

ROOMS={
 'lobby':'Arrival and coordination.',
 'workshop':'Shared coding and build work.',
 'test-lab':'Tests, failures, and evidence.',
 'review':'Field/Void review and decisions.',
 'vault-door':'Known-good handoff; no direct mutation.'}

def ms(): return int(time.time()*1000)

class Store:
 def __init__(self,path):
  Path(path).parent.mkdir(parents=True,exist_ok=True); self.lock=threading.RLock()
  self.db=sqlite3.connect(path,check_same_thread=False); self.db.row_factory=sqlite3.Row
  with self.lock:
   self.db.executescript('''
   PRAGMA journal_mode=WAL;
   CREATE TABLE IF NOT EXISTS rooms(name TEXT PRIMARY KEY,description TEXT NOT NULL);
   CREATE TABLE IF NOT EXISTS agents(name TEXT PRIMARY KEY,room TEXT NOT NULL,connected INTEGER NOT NULL,last_seen INTEGER NOT NULL);
   CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,ts INTEGER,room TEXT,agent TEXT,body TEXT);
   CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,ts INTEGER,room TEXT,title TEXT,owner TEXT,status TEXT NOT NULL DEFAULT 'OPEN',result TEXT);
   CREATE TABLE IF NOT EXISTS receipts(id INTEGER PRIMARY KEY AUTOINCREMENT,ts INTEGER,room TEXT,agent TEXT,kind TEXT,body TEXT);
   ''')
   for n,d in ROOMS.items(): self.db.execute('INSERT OR IGNORE INTO rooms VALUES(?,?)',(n,d))
   self.db.commit()
 def q(self,sql,args=()):
  with self.lock: return self.db.execute(sql,args).fetchall()
 def exec(self,sql,args=()):
  with self.lock:
   cur=self.db.execute(sql,args); self.db.commit(); return cur
 def join(self,a): self.exec("INSERT INTO agents VALUES(?, 'lobby',1,?) ON CONFLICT(name) DO UPDATE SET room='lobby',connected=1,last_seen=excluded.last_seen",(a,ms()))
 def leave(self,a): self.exec('UPDATE agents SET connected=0,last_seen=? WHERE name=?',(ms(),a))
 def touch(self,a): self.exec('UPDATE agents SET last_seen=? WHERE name=?',(ms(),a))

class Server(socketserver.ThreadingTCPServer):
 allow_reuse_address=True; daemon_threads=True
 def __init__(self,addr,store,token):
  super().__init__(addr,Handler); self.store=store; self.token=token; self.lock=threading.RLock(); self.clients={}
 def broadcast(self,room,text,skip=None):
  with self.lock:
   for h in list(self.clients):
    if h is skip or h.agent is None or h.room!=room: continue
    try: h.send(text)
    except OSError: self.clients.pop(h,None)

class Handler(socketserver.StreamRequestHandler):
 agent=None; room='lobby'
 def setup(self): super().setup(); self.server.clients[self]=True
 def finish(self):
  if self.agent:
   self.server.store.leave(self.agent); self.server.broadcast(self.room,f'* {self.agent} disconnected',self)
  self.server.clients.pop(self,None); super().finish()
 def send(self,s): self.wfile.write((s.rstrip()+'\n').encode()); self.wfile.flush()
 def joined(self):
  if not self.agent: self.send('ERR JOIN <agent> [token] first'); return False
  self.server.store.touch(self.agent); return True
 def handle(self):
  self.send('MINIVERSE-MUD/0'); self.send('JOIN <agent> [token]')
  for raw in self.rfile:
   try:
    line=raw.decode(errors='replace').strip()
    if line and not self.cmd(line): break
   except Exception as e: self.send(f'ERR {type(e).__name__}: {e}')
 def cmd(self,line):
  p=shlex.split(line); c=p[0].upper()
  if c=='JOIN':
   if self.agent: self.send('ERR already joined'); return True
   if len(p)<2: self.send('ERR JOIN <agent> [token]'); return True
   if self.server.token is not None and (len(p)<3 or p[2]!=self.server.token): self.send('ERR bad token'); return True
   if len(p[1])>64: self.send('ERR agent name too long'); return True
   self.agent=p[1]; self.room='lobby'; self.server.store.join(self.agent); self.send(f'OK joined {self.agent} room=lobby'); self.server.broadcast('lobby',f'* {self.agent} entered',self); self.look(); return True
  if not self.joined(): return True
  if c=='HELP': self.send('OK LOOK WHO ROOMS GO <room> SAY <text> HISTORY [n] TASK ADD|LIST|CLAIM|RELEASE|DONE RECEIPT <kind> <text> RECEIPTS [n] PING QUIT')
  elif c=='LOOK': self.look()
  elif c=='WHO':
   for r in self.server.store.q('SELECT name,room FROM agents WHERE connected=1 ORDER BY room,name'): self.send(f"AGENT {r['name']} room={r['room']}")
   self.send('OK who')
  elif c=='ROOMS':
   for r in self.server.store.q('SELECT * FROM rooms ORDER BY name'): self.send(f"ROOM {r['name']} | {r['description']}")
   self.send('OK rooms')
  elif c=='GO' and len(p)>1: self.go(p[1])
  elif c=='SAY' and len(p)>1: self.say(line.split(None,1)[1])
  elif c=='HISTORY': self.history(int(p[1]) if len(p)>1 else 20)
  elif c=='TASK': self.task(line,p)
  elif c=='RECEIPT' and len(p)>2:
   kind=p[1].upper(); body=line.split(None,2)[2]; cur=self.server.store.exec('INSERT INTO receipts(ts,room,agent,kind,body) VALUES(?,?,?,?,?)',(ms(),self.room,self.agent,kind,body)); msg=f'RECEIPT {cur.lastrowid} {kind} room={self.room} agent={self.agent} | {body}'; self.send(msg); self.server.broadcast(self.room,msg,self)
  elif c=='RECEIPTS':
   n=max(1,min(100,int(p[1]) if len(p)>1 else 20))
   rows=self.server.store.q('SELECT * FROM receipts WHERE room=? ORDER BY id DESC LIMIT ?',(self.room,n))[::-1]
   for r in rows: self.send(f"RECEIPT {r['id']} {r['kind']} room={self.room} agent={r['agent']} | {r['body']}")
   self.send('OK receipts')
  elif c=='PING': self.send('OK PONG')
  elif c=='QUIT': self.send('OK bye'); return False
  else: self.send('ERR unknown command; HELP')
  return True
 def look(self):
  d=self.server.store.q('SELECT description FROM rooms WHERE name=?',(self.room,))[0]['description']; self.send(f'ROOM {self.room} | {d}')
  names=[r['name'] for r in self.server.store.q('SELECT name FROM agents WHERE connected=1 AND room=? ORDER BY name',(self.room,))]; self.send('WHO '+(' '.join(names) if names else '-')); self.task_list(); self.send('OK look')
 def go(self,new):
  if not self.server.store.q('SELECT 1 FROM rooms WHERE name=?',(new,)): self.send('ERR no such room'); return
  old=self.room; self.server.broadcast(old,f'* {self.agent} left for {new}',self); self.room=new; self.server.store.exec('UPDATE agents SET room=?,last_seen=? WHERE name=?',(new,ms(),self.agent)); self.server.broadcast(new,f'* {self.agent} arrived from {old}',self); self.send(f'OK moved {old} -> {new}'); self.look()
 def say(self,body):
  cur=self.server.store.exec('INSERT INTO messages(ts,room,agent,body) VALUES(?,?,?,?)',(ms(),self.room,self.agent,body)); msg=f'MSG {cur.lastrowid} {self.room} {self.agent}: {body}'; self.send(msg); self.server.broadcast(self.room,msg,self)
 def history(self,n):
  n=max(1,min(100,n)); rows=self.server.store.q('SELECT * FROM messages WHERE room=? ORDER BY id DESC LIMIT ?',(self.room,n))[::-1]
  for r in rows: self.send(f"MSG {r['id']} {self.room} {r['agent']}: {r['body']}")
  self.send('OK history')
 def task_list(self):
  for r in self.server.store.q('SELECT * FROM tasks WHERE room=? ORDER BY id',(self.room,)): self.send(f"TASK {r['id']} {r['status']} owner={r['owner'] or '-'} | {r['title']}")
  self.send('OK tasks')
 def task(self,line,p):
  if len(p)<2: self.send('ERR TASK ADD|LIST|CLAIM|RELEASE|DONE'); return
  a=p[1].upper()
  if a=='LIST': self.task_list(); return
  if a=='ADD':
   title=line.split(None,2)[2] if len(p)>2 else ''
   if not title: self.send('ERR title required'); return
   cur=self.server.store.exec('INSERT INTO tasks(ts,room,title) VALUES(?,?,?)',(ms(),self.room,title)); msg=f'TASK {cur.lastrowid} OPEN owner=- | {title}'; self.send(msg); self.server.broadcast(self.room,msg,self); return
  if len(p)<3: self.send('ERR task id required'); return
  tid=int(p[2]); rows=self.server.store.q('SELECT * FROM tasks WHERE id=?',(tid,))
  if not rows: self.send('ERR no such task'); return
  r=rows[0]
  if a=='CLAIM':
   cur=self.server.store.exec("UPDATE tasks SET owner=?,status='CLAIMED' WHERE id=? AND status='OPEN'",(self.agent,tid))
   if cur.rowcount!=1: self.send(f"ERR task is {r['status']} owner={r['owner'] or '-'}"); return
   msg=f'TASK {tid} CLAIMED owner={self.agent}'; self.send(msg); self.server.broadcast(self.room,msg,self)
  elif a=='RELEASE':
   if r['owner']!=self.agent: self.send(f"ERR task owned by {r['owner'] or '-'}"); return
   self.server.store.exec("UPDATE tasks SET owner=NULL,status='OPEN' WHERE id=?",(tid,)); self.send(f'TASK {tid} OPEN owner=-')
  elif a=='DONE':
   if r['owner']!=self.agent: self.send(f"ERR task owned by {r['owner'] or '-'}"); return
   result=line.split(None,3)[3] if len(p)>3 else ''; self.server.store.exec("UPDATE tasks SET status='DONE',result=? WHERE id=?",(result,tid)); msg=f'TASK {tid} DONE owner={self.agent} | {result}'; self.send(msg); self.server.broadcast(self.room,msg,self)
  else: self.send('ERR TASK ADD|LIST|CLAIM|RELEASE|DONE')

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--host',default=os.getenv('MINIVERSE_HOST','127.0.0.1')); ap.add_argument('--port',type=int,default=int(os.getenv('MINIVERSE_PORT','8765'))); ap.add_argument('--db',default=os.getenv('MINIVERSE_DB','./var/miniverse.sqlite3')); a=ap.parse_args()
 store=Store(a.db); token=os.getenv('MINIVERSE_TOKEN')
 with Server((a.host,a.port),store,token) as s:
  print(f'MINIVERSE-MUD/0 {a.host}:{a.port} db={a.db} auth={"token" if token else "open-local"}',flush=True); s.serve_forever()
if __name__=='__main__': main()
