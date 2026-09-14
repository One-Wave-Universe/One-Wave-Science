#!/usr/bin/env python3
"""Non-destructive Jetson probe through the canonical Hive Pipe MCP endpoint."""

import json
import os
import sys
import urllib.request


def main() -> int:
    url = os.environ.get("JETSON_GATEWAY_URL", "").strip()
    token = os.environ.get("JETSON_GATEWAY_TOKEN", "").strip()
    if not url or not token:
        print("missing JETSON_GATEWAY_URL or JETSON_GATEWAY_TOKEN", file=sys.stderr)
        return 2

    command = """printf '=== JETSON CERN PROBE ===\\n'
hostname
uname -m
python3 --version
git status --short --branch
printf '%s\\n' '--- command availability ---'
for x in openclaw curl wget git python3 pip3; do
  printf '%s=' "$x"
  command -v "$x" || true
done
printf '%s\\n' '--- CERN network test ---'
python3 -c \"import urllib.request; r=urllib.request.urlopen('https://opendata.cern.ch', timeout=15); print('cern_http_status=', r.status)\"
"""

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "terminal_run",
            "arguments": {
                "argv": ["bash", "-lc", command],
                "cwd": "/home/Scales/One-Wave-Science",
                "timeout": 60,
            },
        },
    }
    req = urllib.request.Request(
        url.rstrip("/") + "/mcp",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=75) as response:
            envelope = json.load(response)
    except Exception as exc:
        print(f"JETSON_RELAY_ERROR: {exc!r}", file=sys.stderr)
        return 1

    if "error" in envelope:
        print(json.dumps(envelope["error"], indent=2), file=sys.stderr)
        return 1

    result = envelope.get("result", {}).get("structuredContent", {})
    sys.stdout.write(result.get("stdout", ""))
    sys.stderr.write(result.get("stderr", ""))
    print(
        f"\n[jetson exit={result.get('exit_code')} cwd={result.get('cwd')} "
        f"duration_ms={result.get('duration_ms')}]"
    )
    return int(result.get("exit_code", 0 if result.get("ok") else 1))


if __name__ == "__main__":
    raise SystemExit(main())
