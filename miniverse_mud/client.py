#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, socket, sys, threading

def reader(sock):
 f=sock.makefile('r',encoding='utf-8',errors='replace')
 try:
  for line in f: print(line.rstrip())
 except OSError: pass

def main():
 ap=argparse.ArgumentParser(description='Enter Miniverse MUD as an AI or human')
 ap.add_argument('--agent',required=True)
 ap.add_argument('--host',default=os.getenv('MINIVERSE_HOST','127.0.0.1'))
 ap.add_argument('--port',type=int,default=int(os.getenv('MINIVERSE_PORT','8765')))
 ap.add_argument('--token',default=os.getenv('MINIVERSE_TOKEN'))
 ap.add_argument('-c','--command',action='append',default=[])
 a=ap.parse_args()
 sock=socket.create_connection((a.host,a.port),timeout=10); sock.settimeout(None)
 t=threading.Thread(target=reader,args=(sock,),daemon=True); t.start()
 join=f'JOIN {a.agent}'+(f' {a.token}' if a.token else '')+'\n'; sock.sendall(join.encode())
 for cmd in a.command: sock.sendall((cmd+'\n').encode())
 if a.command:
  sock.sendall(b'QUIT\n'); t.join(timeout=2); return
 try:
  for line in sys.stdin:
   sock.sendall(line.encode())
   if line.strip().upper()=='QUIT': break
 except (KeyboardInterrupt,BrokenPipeError): pass
 finally:
  try: sock.shutdown(socket.SHUT_RDWR)
  except OSError: pass
  sock.close()

if __name__=='__main__': main()
