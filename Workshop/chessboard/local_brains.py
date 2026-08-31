#!/usr/bin/env python3
import json, random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST='127.0.0.1'; PORT=8788
PIECE_VALUES={'P':1,'N':3,'B':3,'R':5,'Q':9,'K':100}

class Brain:
    def __init__(self, side):
        self.side=side
        self.oversight_count=0
        self.last_action=None
        self.arousal=0.0
    def choose(self, payload):
        moves=payload.get('moves') or []
        if not moves: return {'move':None,'side':self.side}
        gate=int(payload.get('gate',0) or 0)
        sound=payload.get('sound') or {}
        diff=(sound.get('diff') or {})
        pitch=float(diff.get('pitch',0) or 0)
        pressure=float((sound.get('level') or {}).get('pressure',0) or 0)
        self.arousal=max(0.0,min(1.0,self.arousal*0.82+pressure*0.18))
        scored=[]
        for m in moves:
            cap=m.get('captureType')
            capture=PIECE_VALUES.get(cap,0)*12
            fr=m['from']; to=m['to']
            advance=(fr['r']-to['r']) if self.side=='FIELD' else (to['r']-fr['r'])
            center=3.5-(abs(3.5-to['r'])+abs(3.5-to['c']))/2
            if self.side=='FIELD': score=capture+advance*(2+gate*.25)+center*1.3+pitch*.4
            else: score=capture+center*(2+gate*.2)-advance*.4-pitch*.4
            score += random.random()*(1.5 + self.arousal)
            scored.append((score,m))
        scored.sort(key=lambda x:x[0], reverse=True)
        self.oversight_count += 1
        chosen=scored[0][1]
        response={
            'side':self.side,
            'move':chosen,
            'newOversight':self.oversight_count,
            'lastAction':self.last_action,
            'arousal':round(self.arousal,4),
            'brainMs':round(100*(1.25-0.5*self.arousal),2)
        }
        self.last_action=chosen
        return response

brains={'FIELD':Brain('FIELD'),'VOID':Brain('VOID')}

class H(BaseHTTPRequestHandler):
    def _send(self,obj,code=200):
        body=json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self): self._send({})
    def do_GET(self):
        if self.path=='/health': self._send({'ok':True,'brains':['FIELD','VOID'],'host':HOST,'port':PORT})
        else: self._send({'error':'not found'},404)
    def do_POST(self):
        if self.path!='/choose': return self._send({'error':'not found'},404)
        try:
            n=int(self.headers.get('Content-Length','0')); data=json.loads(self.rfile.read(n) or b'{}')
            side=data.get('side')
            if side not in brains: return self._send({'error':'side must be FIELD or VOID'},400)
            self._send(brains[side].choose(data))
        except Exception as e: self._send({'error':str(e)},500)
    def log_message(self,fmt,*args): pass

if __name__=='__main__':
    print(f'Local brains listening on http://{HOST}:{PORT}')
    ThreadingHTTPServer((HOST,PORT),H).serve_forever()
