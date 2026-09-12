# Hive Pipe v3

Hive Pipe is the authenticated Jetson-side tool gateway used by AI clients,
GitHub Actions, and direct remote clients.

It has two layers:

```text
MCP / authenticated HTTP
        |
        +-- terminal_pwd
        +-- terminal_which
        +-- terminal_run(argv, cwd?, timeout?)
        |
        +-- bounded named queue actions
                |
                v
          agent.sh -> mudl.py
```

## Canonical gateway

Use:

```text
hive-pipe/gateway.py
hive-pipe/terminal_parser.py
hive-pipe/install_gateway.sh
```

The gateway binds to `127.0.0.1:8765` and exposes MCP at `/mcp`.

Do not run the legacy `scripts/jetson_gateway.py` beside Hive Pipe; it uses the
same port. `scripts/install_jetson_gateway.sh` now delegates to this installer.

## Install on the Jetson

```bash
cd "$HOME/One-Wave-Science"
bash hive-pipe/install_gateway.sh
```

This installs and restarts:

```text
hive-pipe-agent.service
hive-pipe-gateway.service
```

It creates separate client tokens under:

```text
~/.config/hive-pipe/tokens/
```

and an explicit external-work area at:

```text
~/One-Wave-External-Work/
```

The systemd sandbox keeps system paths read-only while allowing writes to the
One-Wave checkout and that explicit external-work directory.

## Terminal parser

`terminal_run` accepts a structured argv array. Example MCP call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "terminal_run",
    "arguments": {
      "argv": ["git", "status", "--short", "--branch"],
      "cwd": "/home/Scales/One-Wave-Science",
      "timeout": 60
    }
  }
}
```

The result contains:

```text
stdout
stderr
exit_code
cwd
duration_ms
output_clipped
timed_out (when applicable)
```

The parser runs with `shell=False`. It blocks normal AI access to privilege
escalation, raw-device/formatting tools, power commands, credential/private-key
paths, and shell `-c/-lc` command strings.

It is intentionally usable for normal development commands such as `git`,
`python3`, test runners, compilers, and project scripts.

## Named queue actions

The older bounded queue remains for simple named actions:

```text
queue/pending/<job-id>.json
        -> agent.sh
        -> mudl.py run
        -> queue/results/<job-id>.json
        -> queue/done/<job-id>.json
```

List enabled actions with:

```bash
python3 hive-pipe/mudl.py actions
```

## Local test

```bash
TOKEN="$(cat "$HOME/.config/hive-pipe/tokens/codex.token")"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"terminal_run","arguments":{"argv":["printf","AI_TERMINAL_OK"]}}}' \
  http://127.0.0.1:8765/mcp
```

Expected structured output contains `AI_TERMINAL_OK` and exit code `0`.

## Remote paths

Hive Pipe can be reached through an authenticated reverse tunnel. Keep the
server bound to loopback and point Cloudflare/another trusted tunnel at:

```text
http://127.0.0.1:8765
```

Remote MCP URL:

```text
https://YOUR-TUNNEL/mcp
```

Every request still requires a Hive Pipe bearer token.

The same MCP terminal parser is used by:

- `.github/workflows/jetson-command.yml` for GitHub -> Jetson;
- `scripts/jetson_remote.sh` for direct HTTPS client -> Jetson;
- connected MCP-capable AI clients.

SSH remains a separate recovery path and does not depend on Hive Pipe.

## External work

See `External_Work/README.md` and `scripts/external_work_bridge.py` for the
bidirectional GitHub <-> Jetson-local external-work handoff.

## Full directions

See:

```text
AI_JETSON_TOOL_GUIDE.md
JETSON_AI_ACCESS.md
```
