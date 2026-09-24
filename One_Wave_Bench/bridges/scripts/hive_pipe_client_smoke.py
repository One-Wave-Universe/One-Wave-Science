#!/usr/bin/env python3
import argparse, json, os, re
from pathlib import Path
from urllib.request import Request, urlopen

p=argparse.ArgumentParser()
p.add_argument('client')
p.add_argument('--url', default=os.environ.get('HIVE_PIPE_MCP_URL','http://127.0.0.1:8765/mcp'))
a=p.parse_args()
if not re.fullmatch(r'[A-Za-z0-9._-]+', a.client):
    raise SystemExit('invalid client name')
path=Path(os.environ.get('HIVE_PIPE_TOKEN_FILE', str(Path.home()/'.config/hive-pipe/tokens'/f'{a.client}.token')))
if not path.is_file():
    raise SystemExit(f'missing token file: {path}')
token=path.read_text(encoding='utf-8').strip()
if not token:
    raise SystemExit(f'empty token file: {path}')
marker=f'{a.client.upper().replace("-","_")}_TERMINAL_OK'
payload={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'terminal_run','arguments':{'argv':['printf',marker],'timeout':30}}}
req=Request(a.url.rstrip('/'), data=json.dumps(payload).encode(), headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'}, method='POST')
with urlopen(req,timeout=35) as resp:
    envelope=json.load(resp)
result=envelope.get('result',{}).get('structuredContent',{})
ok=result.get('stdout')==marker and result.get('exit_code')==0
print(json.dumps({'client':a.client,'url':a.url,'ok':ok,'stdout':result.get('stdout'),'exit_code':result.get('exit_code')},sort_keys=True))
raise SystemExit(0 if ok else 1)
