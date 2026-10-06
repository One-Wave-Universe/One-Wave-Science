import socket, tempfile, threading, unittest
import server

class MudTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.s=server.Server(('127.0.0.1',0),server.Store(self.tmp.name+'/x.db'),None); self.t=threading.Thread(target=self.s.serve_forever,daemon=True); self.t.start(); self.addr=self.s.server_address
 def tearDown(self): self.s.shutdown(); self.s.server_close(); self.tmp.cleanup()
 def until(self,f,text):
  for _ in range(100):
   line=f.readline()
   if text in line: return line
  self.fail(f'did not receive {text!r}')
 def c(self,name):
  s=socket.create_connection(self.addr); f=s.makefile('rw',encoding='utf-8',buffering=1); f.readline(); f.readline(); f.write(f'JOIN {name}\n'); self.until(f,'OK look'); return s,f
 def test_two_agents_share_room_and_task(self):
  a,fa=self.c('codex'); b,fb=self.c('gemini')
  fa.write('GO workshop\n'); self.until(fa,'OK look')
  fb.write('GO workshop\n'); self.until(fb,'OK look')
  fa.write('TASK ADD fix parser\n'); self.until(fa,'TASK 1 OPEN')
  self.until(fb,'TASK 1 OPEN')
  fb.write('TASK CLAIM 1\n'); self.until(fb,'TASK 1 CLAIMED')
  self.until(fa,'TASK 1 CLAIMED')
  fb.write('RECEIPT TEST 40/40 PASS\n'); self.until(fb,'RECEIPT 1 TEST'); self.until(fa,'RECEIPT 1 TEST')
  a.close(); b.close()

if __name__=='__main__': unittest.main()
