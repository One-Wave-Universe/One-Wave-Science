# One-Wave AI Bridge: Start Here

This is the canonical operating page for every AI, laptop, Jetson, and human
using One-Wave terminal access. Read this page before declaring a bridge healthy
or broken.

## One command that tells the truth

From the repository checkout:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile all
```

Profiles:

```text
--profile ci       repository files, syntax, and bridge contracts only
--profile pull     ChatGPT GitHub primary/backup pull bridge
--profile gateway  local Hive Pipe services and a real MCP terminal receipt
--profile all      every local route plus optional/recovery route visibility
```

Exit meanings:

```text
0  every required check in that profile passed
1  at least one required bridge check failed
2  required checks passed, but an optional/external route is unconfigured,
   warning, or cannot be proven from this machine
```

`--json` returns the same result in machine-readable form. The doctor is
read-only. It never changes services, branches, credentials, or files.

## Supported routes and their jobs

| Route | Best use | Health proof | Independent fallback |
|---|---|---|---|
| Hive Pipe MCP | Normal live AI terminal, Python, and C++ | `terminal_reference` plus `terminal_run` receipt | Pull bridge or SSH |
| ChatGPT pull bridge | ChatGPT sessions with GitHub but no attached MCP | Matching result ID on primary or backup branch | Direct MCP |
| GitHub Actions command lane | Human-dispatched remote MCP call | Successful workflow log with exit 0 | Pull bridge |
| `One_Wave_Bench/bridges/scripts/jetson_remote.sh` | Authorized command-line client | Real structured stdout/exit receipt | SSH |
| DeepSeek API adapter | DeepSeek function tools into Hive Pipe | `--mcp-smoke`, then bounded model tool call | Direct MCP client |
| DeepSeek web adapter | Logged-in local web relay into Hive Pipe | `--relay-health` and `--mcp-smoke` | DeepSeek API/direct MCP |
| External-work bridge | GitHub handoff for approved large/external-drive work | Pull/publish smoke with matching file content | Git worktree/manual review |
| SSH | Independent human recovery | Login plus `whoami`, `hostname`, `pwd` | Local console |

The Miniverse desktop/room is a client of this architecture. It is not a
replacement terminal route.

## Route 1 — direct Hive Pipe MCP

Use this first when the AI session exposes the tools:

```text
terminal_reference
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

First calls:

```json
{"name":"terminal_reference","arguments":{}}
```

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["git", "status", "--short", "--branch"],
    "timeout": 30
  }
}
```

Omit `cwd` unless the actual target checkout path has been verified. Every
receipt contains guidance naming whether the next step is an AI correction,
path authorization/creation, tool installation, authentication repair, or a
human/root intervention.

Install/restart on the Jetson or another intended gateway host:

```bash
bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
python3 One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile gateway
```

The gateway remains loopback-only. Remote clients use the authorized HTTPS
tunnel and their own per-client token.

## Route 2 — ChatGPT GitHub pull bridge

Use this when ChatGPT has the GitHub connector but no Hive Pipe MCP tools.

Transport branches:

```text
chatgpt-terminal
chatgpt-terminal-backup
```

Write the **same** request to `.chatgpt-terminal/request.json` on both branches:

```json
{
  "id": "unique-task-id-001",
  "argv": ["git", "status", "--short", "--branch"],
  "timeout": 30
}
```

Use a new ID for different command content. The two-state-machine worker dedupes
the mirrored requests, executes once, and returns through the first healthy
writable back route.

Read `.chatgpt-terminal/result.json` on both branches until one contains the
matching ID. A missing result on both branches means the target worker has not
acknowledged the request; it does **not** prove the command ran.

One-time installation on the machine ChatGPT must operate:

```bash
git fetch origin main
git show origin/main:One_Wave_Bench/bridges/hive-pipe/install_chatgpt_terminal_pull.sh | ONE_WAVE_PROJECT_ROOT="$PWD" bash
python3 ~/.local/share/one-wave-chatgpt-terminal-runtime/One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile pull
```

The pull worker runs as the normal user and reuses `terminal_parser.py`. It does
not bypass blocked programs, credential paths, authorized roots, or the systemd
sandbox.

## Route 3 — GitHub Actions command lane

Workflow: `.github/workflows/jetson-command.yml`

Dispatch **Jetson Command Lane** with:

```text
argv_json = ["printf","GITHUB_MCP_OK"]
timeout = 30
```

Blank `gateway_url` uses the configured secret. A successful workflow with
`GITHUB_MCP_OK` and exit `0` proves the current tunnel and secret together. CI
only proves the workflow contract; it cannot prove hidden secrets or a temporary
tunnel is live.

## Route 4 — command-line remote helper

```bash
export JETSON_GATEWAY_URL='https://CURRENT-AUTHORIZED-TUNNEL'
export JETSON_GATEWAY_TOKEN='client-token'
One_Wave_Bench/bridges/scripts/jetson_remote.sh -- git status --short --branch
```

The URL and token may instead live in `~/.config/hive-pipe/remote.env` with
permissions restricted to the user. Never commit them.

## DeepSeek adapters

Official API adapter:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py --mcp-smoke
```

Free-web/local-session adapter:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_web_bridge.py --relay-health --mcp-smoke
```

The DeepSeek adapters translate model function calls into the same bounded Hive
Pipe tools. A healthy adapter cannot compensate for an unhealthy local gateway.

## External work and SSH

External-work transfer is documented in `One_Wave_Bench/bridges/external-work/External_Work/README.md`. CI performs a
real temporary pull/publish content check.

SSH remains independent of GitHub, Cloudflare, and MCP:

```bash
ssh <verified-user>@<verified-host-address>
```

Never guess the username or address. Verify the destination with `whoami`,
`hostname`, and `pwd` after login.

## Health law for every AI

1. Repository tests prove code and contracts, not a live remote machine.
2. A live route requires a matching receipt from that route.
3. A queued request without a matching result is **pending/offline**, not passed.
4. Never claim a command ran from intent, documentation, or a branch write.
5. Use the next independent route only after recording why the preferred route
   failed.
6. Do not ask the human to relay ordinary commands once a live route is proven.
7. If activation or root work is genuinely required, name that single boundary
   precisely instead of pretending another route succeeded.
