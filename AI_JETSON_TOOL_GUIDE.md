# AI Jetson Tool Guide

Executable MCP calls now require `intention` and `consequence` text in their
arguments. Older JSON examples below illustrate command arguments only; add
these two fields or the reference goblin holds execution. See
`AI_BRIDGE_START_HERE.md` for the current contract.

This is the shortest correct guide for a fresh Perplexity/Claude/Codex/Gemini or other authorized AI instance.

## Start here

The canonical Jetson tool path is:

```text
client -> HTTPS/MCP -> One_Wave_Bench/hive-pipe/gateway.py -> terminal_parser.py -> Jetson process
```

MCP endpoint:

```text
/mcp
```

Primary tools:

```text
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

Do not assume the old `/v1/exec` gateway is active. Do not start
`scripts/jetson_gateway.py` beside Hive Pipe; it uses the same port 8765.

## Client credentials

The installer creates separate tokens for:

```text
codex
claude
gemini
perplexity
```

They live only on the Jetson under:

```text
~/.config/hive-pipe/tokens/<client>.token
```

To add any other client:

```bash
bash One_Wave_Bench/hive-pipe/create_client_token.sh CLIENT_NAME
```

The gateway accepts the same client token through any of these common forms:

```text
Authorization: Bearer <token>
Authorization: ApiKey <token>
X-API-Key: <token>
Api-Key: <token>
```

Never commit or paste tokens into the public repository.

## If an AI says "there is no terminal attached"

Treat that as a **session attachment problem** until proven otherwise. Do not ask
the AI to invent terminal output, and do not assume the Jetson gateway is down.

The repo cannot make an already-running chat suddenly acquire MCP tools. The AI
client/orchestrator must start or reconnect the session with the Hive Pipe MCP
connector attached.

### 1. Verify the Jetson bridge itself

On the Jetson, Hive Pipe should be listening only on loopback:

```bash
ss -ltnp | grep ':8765'
```

Expected service:

```text
127.0.0.1:8765
one-wave-hive-pipe
```

Then initialize MCP with that client's token and call `tools/list`. A healthy
v3.2 gateway exposes at least:

```text
health
inventory_block_devices
repo_status
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

If those tools list correctly, **do not restart or rebuild Hive Pipe just
because one AI chat cannot see them**.

### 2. Reconnect the AI client/session

Configure the client with:

```text
MCP endpoint: https://CURRENT-AUTHORIZED-TUNNEL/mcp
Transport: Streamable HTTP
Authentication: API key / Bearer token
Token source on Jetson: ~/.config/hive-pipe/tokens/<client>.token
```

For a client running locally on the Jetson, the endpoint may be:

```text
http://127.0.0.1:8765/mcp
```

A remote client needs the currently authorized HTTPS tunnel/connector path. Do
not hard-code an expired temporary tunnel URL into the repository.

Start a **new/reconnected AI session** after attaching the connector if the
product caches its tool list.

### 3. Prove attachment from inside the AI session

The AI should first list/see the Hive Pipe tools. Then call:

```text
terminal_pwd
```

and:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["git", "status", "--short", "--branch"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

Only after a real tool result returns should the AI claim it inspected the repo.

### 4. Interpret the failure correctly

```text
Gateway tools/list works, AI session has no MCP tools
    -> client/session attachment failure

AI session lists tools, terminal_pwd fails authentication
    -> token/connector authentication failure

AI session lists tools, terminal_run rejects cwd/command
    -> Hive Pipe safety/authorized-root rejection

Port 8765 not listening / initialize fails locally
    -> actual Jetson Hive Pipe service failure
```

A chat that has no tool attachment may still write a proposed patch, but it must
label it unverified. It must never fabricate HEAD hashes, command output, file
contents, or test results.

## Perplexity remote MCP

Perplexity remote custom connectors support API-key authentication. Configure:

```text
MCP URL: https://YOUR-TUNNEL/mcp
Transport: Streamable HTTP
Authentication: API Key
API key: contents of ~/.config/hive-pipe/tokens/perplexity.token
```

Perplexity commonly uses normal shell wrappers such as `bash -lc` for terminal
work. Hive Pipe permits those wrappers now. If Perplexity can list tools but
terminal calls fail, first test `terminal_pwd`, then run:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["bash", "-lc", "printf PERPLEXITY_TERMINAL_OK"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

Expected stdout:

```text
PERPLEXITY_TERMINAL_OK
```

## First terminal call

Call `terminal_pwd`, then test:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["printf", "AI_TERMINAL_OK"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

A successful result has:

```text
stdout = AI_TERMINAL_OK
exit_code = 0
```

## Direct Python and C++

The gateway exposes first-class `python_run` and `cpp_compile_run` MCP tools so an
authorized AI can run bounded source directly without a human terminal relay.
See `AI_CODE_BRIDGE.md` for schemas, examples, limits, and verification.

## Enter the visible Miniverse room

The shared 3D/MUD room runs locally at:

```text
http://127.0.0.1:8787/
```

Source and instructions:

```text
Miniverse/room3d/README.md
```

Any authorized AI that can use Hive Pipe terminal access can enter the same
persistent room state without a human relaying commands:

```bash
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py join codex --name CODEX --role "AI CODER" --color '#86a8ff'
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py say codex "I am in the shared room."
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py move codex A+
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py bench codex workshop TEST "tests passed"
```

The six legal movement directions are `A+`, `B+`, `C+`, `A-`, `B-`,
and `C-`. The browser, CLI agents, chat, body locations, and workbench receipts
all use the same state. The room contains no built-in LLM; an external AI client
takes an identity and uses the existing authenticated bridge.

The room server is `miniverse-room.service`. Its persistent state is under
`~/.local/share/one-wave/miniverse-room/`. A graphical login autostarts the
local browser view.

TEST LAB has a persistent experiment ledger and visible controls. Built-in
software experiments plus external Python/C++/Virtual Breadboard receipts are
documented in `Miniverse/room3d/EXPERIMENT_LAB.md`.

For custom AI bodies, new districts, workbenches, objects, animation, and world
expansion, read `Miniverse/EXPAND_MINIVERSE.md` before editing. The native laptop
program and shortcut are documented in `Miniverse/desktop/README.md`.

## Repo work sequence

Before editing:

```json
["git","status","--short","--branch"]
["git","rev-parse","HEAD"]
["git","remote","-v"]
```

Read the repository's canonical project instructions before changing project
logic. Never claim a command/file was checked unless the tool returned it.

For writes, use a task branch rather than silently changing `main`:

```json
["git","switch","-c","ai/task-name"]
```

After changes:

```json
["git","diff","--check"]
["git","status","--short"]
```

Run the relevant tests, review the diff, commit, then push the task branch when
GitHub credentials are available.

## GitHub -> Jetson

Use `.github/workflows/jetson-command.yml` (`Jetson Command Lane`). Preferred
input is `argv_json`, for example:

```json
["git","status","--short","--branch"]
```

The workflow is deliberately `workflow_dispatch` only and runs on a GitHub-hosted
runner. It sends an authenticated MCP `terminal_run` call to the Jetson.

## Jetson -> GitHub

The terminal parser may run normal git commands:

```json
["git","fetch","origin"]
["git","push","-u","origin","HEAD"]
```

Do not push directly to `main` as routine AI behavior. Use a task branch + PR.
If fetch works but push fails, fix Jetson GitHub credentials; do not build a new
terminal bridge.

## Direct HTTPS client

`scripts/jetson_remote.sh` uses the same MCP parser:

```bash
scripts/jetson_remote.sh \
  --cwd /home/Scales/One-Wave-Science \
  -- git status --short --branch
```

## SSH recovery

SSH is intentionally independent:

```bash
ssh Scales@JETSON_IP
```

If the tunnel/MCP path breaks, SSH is the recovery route.

## External work

GitHub-visible handoff:

```text
External_Work/inbox/
External_Work/outbox/
```

Jetson-local external workspace:

```text
~/One-Wave-External-Work/inbox/
~/One-Wave-External-Work/work/
~/One-Wave-External-Work/outbox/
```

GitHub -> Jetson local:

```json
["python3","scripts/external_work_bridge.py","pull"]
```

Jetson local -> GitHub staging:

```json
["python3","scripts/external_work_bridge.py","publish"]
```

`publish` only copies into `External_Work/outbox`; it does not commit or push.
Review and publish through a task branch/PR.

## Safety boundary

Normal authenticated AI terminal access runs as the Jetson's ordinary user and
supports normal shell wrappers, including `bash -lc`.

Direct invocation of a small set of high-risk system programs remains blocked,
including privilege escalation, raw disk formatting/partitioning, mounting, and
power-control commands. Credential/private-key paths are also rejected by the
parser. These command checks are secondary guardrails, not the primary security
boundary.

The primary boundaries are:

```text
per-client authentication token
normal non-root user
systemd NoNewPrivileges
ProtectSystem=strict
explicit writable repo/workspace paths
independent SSH recovery
```

The service sandbox permits writes to the live Hive Pipe checkout, the canonical
`~/One-Wave-Science` checkout when present, and the explicit
`~/One-Wave-External-Work` workspace. System paths remain read-only.

## Full reference

Read `JETSON_AI_ACCESS.md` for setup, tokens, tunnel configuration, all paths,
and the acceptance tests.
