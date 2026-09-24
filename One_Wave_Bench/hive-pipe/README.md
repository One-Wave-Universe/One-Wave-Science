# Hive Pipe v3

Start with [`One_Wave_Bench/AI_BRIDGE_START_HERE.md`](../AI_BRIDGE_START_HERE.md) and [`BRIDGE_DIRECTIONS.md`](BRIDGE_DIRECTIONS.md). It contains
the supported route order, exact smoke tests, pull-bridge request/result format,
and the unified read-only health command:

```bash
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile all
```

Hive Pipe is the authenticated Jetson-side tool gateway used by AI clients,
GitHub Actions, and direct remote clients.

It exposes:

```text
MCP / authenticated HTTP
        |
        +-- terminal_reference
        +-- terminal_pwd
        +-- terminal_which
        +-- terminal_run(argv, cwd?, timeout?)
        +-- python_run(code, args?, cwd?, timeout?)
        +-- cpp_compile_run(code, args?, cwd?, timeout?, standard?)
        |
        +-- bounded named queue actions
                |
                v
          agent.sh -> mudl.py
```

## Canonical gateway

Use:

```text
One_Wave_Bench/hive-pipe/gateway.py
One_Wave_Bench/hive-pipe/terminal_parser.py
One_Wave_Bench/hive-pipe/install_gateway.sh
```

The gateway binds to `127.0.0.1:8765` and exposes MCP at `/mcp`.
Do not run the legacy `scripts/jetson_gateway.py` beside Hive Pipe; it uses the
same port. `scripts/install_jetson_gateway.sh` delegates to this installer.

## Install on the Jetson

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/hive-pipe/install_gateway.sh
```

This installs/restarts `hive-pipe-agent.service` and
`hive-pipe-gateway.service`, creates the external-work workspace, and creates
separate client tokens for:

```text
codex
claude
gemini
perplexity
```

Tokens live under `~/.config/hive-pipe/tokens/` and remain outside git.
Add another client with:

```bash
bash One_Wave_Bench/hive-pipe/create_client_token.sh CLIENT_NAME
```

## Authentication

The gateway accepts any configured client token through common MCP/API-key
forms:

```text
Authorization: Bearer <token>
Authorization: ApiKey <token>
X-API-Key: <token>
Api-Key: <token>
```

This makes clients such as Perplexity remote custom MCP connectors usable
without forcing one provider-specific header format.

## Terminal parser

Call `terminal_reference` first when an AI needs the parser workflow, current
authorized roots and limits, or a structured explanation of where path,
authentication, package, or human/root intervention is required.

`terminal_run` accepts a structured argv array. It also permits normal shell
wrappers such as:

```json
["bash", "-lc", "git status --short --branch"]
```

That compatibility matters for AI clients that routinely wrap terminal work in
`bash -lc`.

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

Direct invocation of a small set of high-risk system programs remains blocked,
including privilege escalation, raw-device/formatting tools, mounting, and
power-control commands. Credential/private-key paths are also rejected. These
checks are secondary guardrails; the primary boundaries are authenticated
per-client tokens, normal non-root execution, `NoNewPrivileges`,
`ProtectSystem=strict`, and explicit writable directories.

Normal development commands, shell pipelines/wrappers, `git`, `python3`, test
runners, compilers, and project scripts are supported.


## Direct Python and C++

Authorized MCP clients can execute bounded source directly without a human
copying commands into the terminal. `python_run` executes temporary Python
source; `cpp_compile_run` compiles temporary C++ with `g++`, executes it, and
returns both compile and runtime receipts. Temporary files are removed after the
request. The tools use the same non-root service sandbox and authorized work
roots as `terminal_run`. See `AI_CODE_BRIDGE.md`.

## Perplexity test

After installing the current gateway:

```bash
TOKEN="$(cat "$HOME/.config/hive-pipe/tokens/perplexity.token")"

curl -sS \
  -H "X-API-Key: $TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"terminal_run","arguments":{"argv":["bash","-lc","printf PERPLEXITY_TERMINAL_OK"],"intention":"Verify Perplexity terminal route","consequence":"Expect PERPLEXITY_TERMINAL_OK and exit zero"}}}' \
  http://127.0.0.1:8765/mcp
```

Expected output contains `PERPLEXITY_TERMINAL_OK` and exit code `0`.

For a Perplexity remote custom connector use:

```text
URL: https://YOUR-TUNNEL/mcp
Transport: Streamable HTTP
Authentication: API Key
Key: contents of ~/.config/hive-pipe/tokens/perplexity.token
```

## Remote paths

Keep Hive Pipe bound to loopback and expose it only through the authenticated
reverse tunnel. The same parser is used by GitHub -> Jetson, direct HTTPS
clients, and connected MCP-capable AI clients. SSH remains the independent
recovery path.

## External drives

The default terminal roots are the canonical checkout and
`~/One-Wave-External-Work`. To authorize dedicated work directories on mounted
external drives, reinstall with an explicit colon-separated list:

```bash
HIVE_PIPE_ALLOWED_ROOTS="/home/Scales/One-Wave-Science:/mnt/lattice:/mnt/sandbox" \
  bash One_Wave_Bench/hive-pipe/install_gateway.sh
```

Only name the dedicated work directories, never a whole drive root. Each path
must already exist and be writable by `Scales`. The installer accepts roots
under the user's home, `/mnt`, `/media`, or `/run/media`; it refuses broad
system roots. The same list is enforced twice: by the terminal parser and by
the systemd `ReadWritePaths` sandbox. Raw-device, formatting, mounting, sudo,
and power commands remain blocked.

Use `inventory_block_devices` first to identify the two drives. Keep persistent
lattice work and disposable experiments in separate authorized directories.

## External work

See `External_Work/README.md` and `scripts/external_work_bridge.py` for the
bidirectional GitHub <-> Jetson-local external-work handoff.

## Full directions

See:

```text
AI_JETSON_TOOL_GUIDE.md
JETSON_AI_ACCESS.md
```
