#!/usr/bin/env python3
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
proc = subprocess.Popen([sys.executable, str(ROOT / 'server.py')], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(0.8)
    join = json.load(urllib.request.urlopen('http://127.0.0.1:8090/join?name=TestHuman&kind=human'))
    pid = join['agentId']
    req = urllib.request.Request('http://127.0.0.1:8090/api/rooms', data=json.dumps({'name':'Test Workshop','description':'API test'}).encode(), headers={'Content-Type':'application/json','X-Agent-Id':pid}, method='POST')
    room = json.load(urllib.request.urlopen(req))['room']
    assert room['name'] == 'Test Workshop'
    req = urllib.request.Request(f"http://127.0.0.1:8090/api/rooms/{room['id']}/messages", data=json.dumps({'text':'Human interaction works.'}).encode(), headers={'Content-Type':'application/json','X-Agent-Id':pid}, method='POST')
    msg = json.load(urllib.request.urlopen(req))['message']
    assert msg['text'] == 'Human interaction works.'
    print('PASS: join, create workshop, post message')
finally:
    proc.terminate(); proc.wait(timeout=3)
