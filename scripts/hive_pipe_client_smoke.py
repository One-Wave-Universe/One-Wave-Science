#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
parser.add_argument("client")
parser.add_argument("--url", default=os.environ.get("HIVE_PIPE_MCP_URL", "http://127.0.0.1:8765/mcp"))
args = parser.parse_args()

if not re.fullmatch(r"[A-Za-z0-9._-]+", args.client):
    raise SystemExit("invalid client name")

token_file = Path(
    os.environ.get(
        "HIVE_PIPE_TOKEN_FILE",
        str(Path.home() / ".config/hive-pipe/tokens" / f"{args.client}.token"),
    )
)
if not token_file.is_file():
    raise SystemExit(f"missing token file: {token_file}")

token = token_file.read_text(encoding="utf-8").strip()
if not token:
    raise SystemExit(f"empty token file: {token_file}")

marker = f"{args.client.upper().replace('-', '_')}_TERMINAL_OK"
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "terminal_run",
        "arguments": {"argv": ["printf", marker], "timeout": 30,
                      "intention": f"Verify {args.client} terminal route",
                      "consequence": f"Expect {marker} and exit zero without repository changes"},
    },
}
request = Request(
    args.url.rstrip("/"),
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    },
    method="POST",
)
with urlopen(request, timeout=35) as response:
    envelope = json.load(response)

result = envelope.get("result", {}).get("structuredContent", {})
ok = result.get("stdout") == marker and result.get("exit_code") == 0
print(
    json.dumps(
        {
            "client": args.client,
            "url": args.url,
            "ok": ok,
            "stdout": result.get("stdout"),
            "exit_code": result.get("exit_code"),
        },
        sort_keys=True,
    )
)
raise SystemExit(0 if ok else 1)
