# One-Wave AI Bridge: Start Here

This is the canonical operating page for every AI, laptop, Jetson, and human
using One-Wave terminal access. Read this page before declaring a bridge healthy
or broken.

## Terminal access — every AI starts here

For laptop or Jetson terminal work, enumerate the tools available in the current
session and select the requested machine. Use the connected device terminal
directly when available. Missing Hive Pipe tools does not mean terminal access
is missing.

### Direct device terminal (Remote Desktop Commander)

Discover tools by their names/descriptions, including deferred tools. Search for
`remote_desktop_commander`, `list_devices`, `start_process`, and
`read_process_output`. Use the exposed tool schema; namespace prefixes vary by client.

1. Call `list_devices({})`.
2. Select the requested device from that fresh list. Supply `deviceId` on
   **every** process/read/write call when more than one device is connected.
3. Call `start_process` with the identity probe below.
4. Inspect the returned output, then run ordinary authorized terminal commands
   on that same device. Use `read_process_output` with the returned PID when
   the command is still running. Require actual output and exit status.
5. Before repository changes, resolve the existing checkout on that device and
   record root, remote, branch, HEAD and working-tree state.

Identity probe:

```json
{
  "deviceId": "ID_FROM_FRESH_DEVICE_LIST",
  "command": "hostname; uname -m; whoami; pwd",
  "timeout_ms": 3000
}
```

Device identities verified on 2026-10-04 (discovery is repeated each session):

| Requested machine | Listed device name | Device ID | Observed identity |
|---|---|---|---|
| Laptop | scales-Latitude-E7450 | 6d4b6585-ca68-4c8b-a3f1-52f64a92c07d | x86_64, user scales |
| Jetson | localhost.localdomain | fc9b5227-716d-4508-a666-ee0a68a08d4c | aarch64, user Scales |

`localhost.localdomain` is the connected Jetson's listed name in this snapshot.
Verify with the device-specific probe; do not confuse it with the chat sandbox.

The verified Jetson checkout is `/home/Scales/One-Wave-Science`.
Resolve its current state before edits:

```json
{
  "deviceId": "VERIFIED_JETSON_DEVICE_ID",
  "command": "cd /home/Scales/One-Wave-Science && git rev-parse --show-toplevel && git remote -v && git branch --show-current && git rev-parse HEAD && git status --short",
  "timeout_ms": 3000
}
```

The laptop has its own filesystem. Resolve an existing project checkout or
mounted external-drive path there; do not reuse the Jetson path or create a
laptop clone merely to obtain a terminal. A machine identity probe can run
without a project checkout. Keep existing dirty work intact.

### Route selection

| Tools actually available for the requested target | Action |
|---|---|
| Remote Desktop Commander | Select the device, probe identity, then execute on that device |
| Native terminal on the requested host | Probe identity and use that host's existing checkout |
| Hive Pipe MCP | Use `terminal_reference` then `terminal_run` |
| Authorized SSH connection | Connect to the verified target and probe identity |
| GitHub connector only, after direct terminal discovery | Use the configured pull worker and require a matching request/result ID |
| Actions dispatch only, with a configured target gateway | Use that target's command workflow and read its completed execution log |

A chat must enumerate/discover its callable tools before selecting a transport.
Do not infer "no terminal" from missing `terminal_run`, from the visible tool
list alone, or from an earlier chat. A GitHub connector alone edits GitHub; it
does not by itself execute a machine command. The Jetson Command Lane targets
the Jetson, not the laptop. Pull/Actions instructions below apply only after
direct routes have been checked and the requested target is configured.

Once a direct route returns output, continue the user's authorized work through
it. Do not switch to a queue, dispatch a proof workflow, restart a service, or ask
the user to relay ordinary commands merely because Hive Pipe is absent.
If a route actually fails, record that specific failure and select the next
available route for the same target. Keep execution claims tied to real receipts.


## Two-state parser goblin and redundant relay loop

Read [the mesh contract](One_Wave_Bench/hive-pipe/MODULAR_HYSTERETIC_BRIDGE_MESH.md)
and [goblin roles](One_Wave_Bench/hive-pipe/GOBLIN_BRIDGE_ROLES.md).
The posted execution loop is ISSUE -> RETURN -> ISSUE:
Parser normalizes the bounded request; Reference checks source/target and
repository state; Worker executes once; Carrier Pigeon returns the matching
receipt; Doctor records failure/recovery; Raccoon selects an independent route
when the current family degrades. A pending return is never permission to
duplicate a mutating command through another relay.

### Posted redundancy map

| Route | Target | Dependency family | Execution proof |
|---|---|---|---|
| Direct device terminal | Laptop or Jetson, explicitly selected | Remote Desktop Commander | Device/PID output and exit status |
| Native host shell | The verified host running it | Local process | Host identity and exit status |
| SSH peer relay | Verified laptop or Jetson address | SSH network/authentication | Destination identity and command output |
| Hive Pipe MCP / HTTPS helper | Configured gateway host | Same gateway/token/tunnel family | Structured terminal receipt |
| Pull relay | Configured worker host | GitHub transport plus target worker | Matching request ID and digest |
| Jetson Actions lane | Jetson gateway | GitHub Actions plus Hive Pipe/tunnel | Completed workflow and target output |

MCP, its HTTPS helper and Actions through the same gateway are not three
independent escape routes from a gateway outage. Prefer device terminal or SSH
for that failure. Keep route state separate by target and direction.

### Existing runnable loops

On the verified host checkout:

```bash
python3 One_Wave_Bench/hive-pipe/parser_goblin.py status
python3 One_Wave_Bench/hive-pipe/parser_goblin.py --once
python3 One_Wave_Bench/hive-pipe/parser_goblin.py --watch
python3 One_Wave_Bench/hive-pipe/bridge_mesh.py --no-repair
```

The parser's local route uses the bounded terminal parser. Its pull/Actions
routes write relay envelopes for an upstream client; that queue is not proof
of dispatch or completion. Direct device-terminal calls are made by the AI
client through its exposed tools, not by pretending the local Python parser
owns those tools.

For a configured Linux host needing the existing self-repair supervisor:

```bash
bash One_Wave_Bench/hive-pipe/install_bridge_mesh.sh
systemctl --user is-active one-wave-bridge-mesh.service
```

This installs the existing user service against that checkout. It restarts
known bridge user services and re-probes their routes. It does not configure
new credentials or install a device-terminal connector. Use an independent
working terminal while a broken relay repairs itself.

Route scoring uses the existing hysteretic selector in `route_mesh.py`:
enter=0.70, leave=0.45; three consecutive failures retire a route until a
successful probe clears the streak. Only currently offered candidates may
be selected; unknown/unproven candidates stay unselected. Candidate names must
include target/direction (for example `laptop:in:desktop` and
`jetson:in:desktop`) so one machine's healthy route cannot be reused as another's.
The selector is a reusable component; the parser currently uses its own fixed
local/Hive/pull/Actions order. Do not claim automatic client-side device failover
was installed merely by updating this guide.

Keep the request ID and digest unchanged while awaiting a return.
After timeout on an operation with side effects, reconcile the original
execution before retrying. A command's nonzero exit is a returned result;
it is not automatically a transport failure. Recovery is accepted only after
a new real receipt from the recovered route.

## Hive Pipe transport health

From the repository checkout:

```bash
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile all
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

## Git is the shared reference plane

All authorized AI routes converge on the repository before work:

```text
AI/client
  -> authorized bridge route
  -> repository reference read
  -> current branch/status/authority check
  -> isolated Git branch for mutation
  -> bounded work
  -> tests/measurement receipts
  -> push branch/receipt
  -> reference return
```

Jetson is a first-class gateway for AIs that need it. It is not the only route.
Direct GitHub connectors, Hive Pipe, the ChatGPT pull branches, GitHub Actions,
SSH, Gemini, Claude, Codex, Perplexity, DeepSeek, and future authorized clients
must all reference the same repository authority before mutation.

Do not create a permanent duplicate repository merely to operate a bridge.
Temporary detached worktrees are allowed for isolated receipt publication and
must be removed after use.

Unknown state is inspected, not assumed. An existing route is preserved unless
direct evidence identifies that route itself as the fault.

## Intention and consequence gate

The gateway checks the canonical checkout before every MCP action and stamps
both the action and response. Hive Pipe executable tools additionally require a concrete
`intention` and `consequence` in their arguments. Missing fields or an unreadable
reference return `Reference Goblin HOLD` before execution. The original issued
card and observed response are written to a private append-only receipt ledger;
summaries do not replace that record. The ChatGPT pull worker requires the same
two fields in each request and records the original result.

This enforces bridge actions. Chat products need their own response gate to
block an unstamped conversational message.

## Supported routes and their jobs

| Route | Best use | Health proof | Independent fallback |
|---|---|---|---|
| Direct device terminal | Laptop or Jetson shell through Remote Desktop Commander | Device-specific identity/output/exit receipt | Native terminal, Hive Pipe or SSH |
| Hive Pipe MCP | Normal live AI terminal, Python, and C++ | `terminal_reference` plus `terminal_run` receipt | Pull bridge or SSH |
| ChatGPT pull bridge | GitHub-only sessions after direct terminal discovery | Matching result ID on primary or backup branch | Direct MCP |
| GitHub Actions command lane | Human-dispatched remote MCP call | Successful workflow log with exit 0 | Pull bridge |
| `scripts/jetson_remote.sh` | Authorized command-line client | Real structured stdout/exit receipt | SSH |
| DeepSeek API adapter | DeepSeek function tools into Hive Pipe | `--mcp-smoke`, then bounded model tool call | Direct MCP client |
| DeepSeek web adapter | Logged-in local web relay into Hive Pipe | `--relay-health` and `--mcp-smoke` | DeepSeek API/direct MCP |
| External-work bridge | GitHub handoff for approved large/external-drive work | Pull/publish smoke with matching file content | Git worktree/manual review |
| SSH | Independent human recovery | Login plus `whoami`, `hostname`, `pwd` | Local console |

The Miniverse desktop/room is a client of this architecture. It is not a
replacement terminal route.

## Route 1 — direct Hive Pipe MCP

For a selected Hive Pipe route, use these exposed tools:

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
    "timeout": 30,
    "intention": "Inspect the current branch and working tree",
    "consequence": "Read the status; do not change repository files"
  }
}
```

Omit `cwd` unless the actual target checkout path has been verified. Every
receipt contains guidance naming whether the next step is an AI correction,
path authorization/creation, tool installation, authentication repair, or a
human/root intervention.

Install/restart on the Jetson or another intended gateway host:

```bash
bash One_Wave_Bench/hive-pipe/install_gateway.sh
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile gateway
```

The gateway remains loopback-only. Remote clients use the authorized HTTPS
tunnel and their own per-client token.

## Route 2 — ChatGPT GitHub pull bridge

Use this for a configured target only after tool discovery confirms no callable direct device terminal, native target terminal, Hive Pipe or authorized SSH route is available.

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
  "timeout": 30,
  "intention": "Inspect the current branch and working tree",
  "consequence": "Read the status; do not change repository files"
}
```

Use a new ID for different command content. The two-state-machine worker dedupes
the mirrored requests, executes once, and returns through the first healthy
writable back route.

Read `.chatgpt-terminal/result.json` on both branches until one contains the
matching ID. A missing result on both branches means the target worker has not
acknowledged the request; it does **not** prove the command ran.

One-time installation on the authorized host ChatGPT must operate, including the Jetson when that is the required AI entry route:

```bash
git fetch origin main
git show origin/main:One_Wave_Bench/hive-pipe/install_chatgpt_terminal_pull.sh | ONE_WAVE_PROJECT_ROOT="$PWD" bash
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile pull
```

The pull worker runs from the real repository checkout as the normal user and reuses `terminal_parser.py`. It does
not bypass blocked programs, credential paths, authorized roots, or the systemd
sandbox.

## Route 3 — GitHub Actions command lane

This is a Jetson-specific fallback after direct terminal discovery. It is not the laptop terminal route.

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
scripts/jetson_remote.sh -- git status --short --branch
```

The URL and token may instead live in `~/.config/hive-pipe/remote.env` with
permissions restricted to the user. Never commit them.

## DeepSeek adapters

Official API adapter:

```bash
python3 One_Wave_Bench/hive-pipe/deepseek_bridge.py --mcp-smoke
```

Free-web/local-session adapter:

```bash
python3 One_Wave_Bench/hive-pipe/deepseek_web_bridge.py --relay-health --mcp-smoke
```

The DeepSeek adapters translate model function calls into the same bounded Hive
Pipe tools. A healthy adapter cannot compensate for an unhealthy local gateway.

## External work and SSH

External-work transfer is documented in `External_Work/README.md`. CI performs a
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
