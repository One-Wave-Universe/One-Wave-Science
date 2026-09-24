# Bench Bridge Directions

This file keeps the complete operational directions inside `One_Wave_Bench/` so bridge work does not depend on scattered root documentation.

## 1. Find the actual checkout

Never assume `~/One-Wave-Science`.

```bash
find "$HOME" -maxdepth 5 -type d -name One-Wave-Science 2>/dev/null
```

Then:

```bash
cd /verified/path/One-Wave-Science
git status --short --branch
git rev-parse HEAD
git remote -v
```

Do not reset, merge, rebase, or switch a dirty checkout merely to repair the bridge.

## 2. Unified health check

```bash
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile all
```

Profiles:

```text
ci       repository files, syntax, route contracts
pull     ChatGPT primary/backup GitHub pull bridge
gateway  local Hive Pipe services and MCP terminal receipt
all      all local routes plus optional/recovery visibility
```

Machine-readable:

```bash
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile all --json
```

Exit codes:

```text
0 = required checks passed
1 = required bridge failure
2 = required checks passed but an optional/external route is unverified or unconfigured
```

## 3. Install or repair Hive Pipe

```bash
cd "$(git rev-parse --show-toplevel)"
bash One_Wave_Bench/hive-pipe/install_gateway.sh
```

Services:

```text
hive-pipe-agent.service
hive-pipe-gateway.service
```

Check:

```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus
systemctl --user is-active hive-pipe-agent.service hive-pipe-gateway.service
ss -ltnp | grep ':8765'
```

Expected Hive Pipe listener:

```text
127.0.0.1:8765
```

If another program owns 8765, identify it before stopping or moving it.

## 4. Hive Pipe MCP

Local endpoint:

```text
http://127.0.0.1:8765/mcp
```

Remote endpoint through an authorized tunnel:

```text
https://AUTHORIZED-TUNNEL/mcp
```

Tools:

```text
terminal_reference
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

Call `terminal_reference` before unfamiliar operations.

## 5. Client tokens

Tokens stay outside git:

```text
~/.config/hive-pipe/tokens/
```

Default clients:

```text
codex
claude
gemini
perplexity
```

Create another token:

```bash
bash One_Wave_Bench/hive-pipe/create_client_token.sh CLIENT_NAME
```

Required token file permissions:

```text
0600
```

Never commit or paste token contents into chat, logs, requests, or repository files.

## 6. Token-safe client smoke

```bash
python3 scripts/hive_pipe_client_smoke.py perplexity
python3 scripts/hive_pipe_client_smoke.py gemini
python3 scripts/hive_pipe_client_smoke.py codex
python3 scripts/hive_pipe_client_smoke.py claude
```

A successful receipt is:

```text
*_TERMINAL_OK
exit_code = 0
```

## 7. Gemini

Project MCP configuration lives in:

```text
.gemini/settings.json
```

Use the token-safe launcher:

```bash
bash scripts/gemini_hive.sh mcp list
```

Expected:

```text
hive-pipe ... Connected
```

Then launch Gemini through the same wrapper:

```bash
bash scripts/gemini_hive.sh
```

The wrapper loads the local Gemini token and sets the local Hive Pipe MCP URL without writing the token to git.

## 8. Perplexity

Use the Perplexity token:

```text
~/.config/hive-pipe/tokens/perplexity.token
```

Connector settings:

```text
URL: https://AUTHORIZED-TUNNEL/mcp
Transport: Streamable HTTP
Authentication: API key / Bearer token
```

Local proof:

```bash
python3 scripts/hive_pipe_client_smoke.py perplexity
```

Do not call Perplexity-to-Jetson live unless the remote connector itself returns a matching target receipt.

## 9. ChatGPT GitHub pull bridge

Transport branches:

```text
chatgpt-terminal
chatgpt-terminal-backup
```

Request:

```text
.chatgpt-terminal/request.json
```

Result:

```text
.chatgpt-terminal/result.json
```

Install on the machine ChatGPT must operate:

```bash
cd "$(git rev-parse --show-toplevel)"
git fetch origin main
git show FETCH_HEAD:One_Wave_Bench/hive-pipe/install_chatgpt_terminal_pull.sh \
  | ONE_WAVE_PROJECT_ROOT="$PWD" bash
```

Runtime:

```text
~/.local/share/one-wave-chatgpt-terminal-runtime
```

Service:

```text
one-wave-chatgpt-terminal-pull.service
```

Status:

```bash
python3 ~/.local/share/one-wave-chatgpt-terminal-runtime/One_Wave_Bench/hive-pipe/chatgpt_terminal_pull.py --status
```

A request without a matching `result.json` is pending/unacknowledged. It is not proof of execution.

## 10. GitHub authentication boundary

Read/fetch and write/push are separate checks.

Read:

```bash
GIT_TERMINAL_PROMPT=0 git fetch origin main
```

Write:

```bash
GIT_TERMINAL_PROMPT=0 git push --dry-run origin HEAD:refs/heads/bridge-auth-dryrun
```

If fetch passes and push fails, repair GitHub write authentication. Do not place credentials inside bridge payloads.

## 11. GitHub Actions command lane

Workflow:

```text
.github/workflows/jetson-command.yml
```

A successful workflow receipt must contain actual target output and exit 0. Repository workflow code alone is not a Jetson-live receipt.

## 12. Remote helper

Use:

```bash
scripts/jetson_remote.sh --cwd /verified/path/One-Wave-Science -- git status --short --branch
```

The URL and token may be supplied by the environment or the existing secure remote configuration. Do not hardcode credentials.

## 13. SSH recovery

Identify the target before claiming it is the Jetson:

```bash
ssh USER@VERIFIED_ADDRESS 'hostname; whoami; uname -a; pwd'
```

A Jetson identity receipt should show an NVIDIA/Tegra aarch64 kernel or other independently verified Jetson identity.

SSH is independent of Hive Pipe, GitHub Actions, and the tunnel.

## 14. External work roots

Default writable roots:

```text
actual One-Wave-Science checkout
~/One-Wave-External-Work
```

Additional roots may be authorized explicitly with `HIVE_PIPE_ALLOWED_ROOTS`.

Do not authorize an entire drive when a dedicated directory is sufficient.

## 15. External data / wave-data work

Bench data directions:

```text
One_Wave_Bench/data/OPEN_DATA_WAVE_PIPELINE.md
One_Wave_Bench/data/open_data_sources.json
scripts/open_data_to_wave.py
```

The transformer requires:

```text
state identity
coupling rule
timing relationship
propagation behavior
source provenance
```

Source measurement series remain source measurements.

Metadata-only encodings must remain labeled:

```text
derived_metadata_wave
```

and are not claims that metadata is itself a measured physical waveform.

## 16. Route acceptance

Do not say "all paths open" until the intended target proves each required path.

Minimum evidence:

```text
Hive Pipe service active
local MCP terminal receipt
Gemini MCP receipt
Perplexity MCP receipt
GitHub fetch receipt
GitHub push receipt
ChatGPT pull request/result receipt
direct Jetson identity receipt
Jetson -> GitHub return/write receipt
```

Keep code health, local-machine health, and Jetson activation as separate facts.


## Modular hysteretic bridge mesh
Before declaring a route unavailable, read `One_Wave_Bench/hive-pipe/MODULAR_HYSTERETIC_BRIDGE_MESH.md`.

All bridge work uses the same rule: reference -> probe -> choose route -> execute -> receipt -> update route memory. Forward and reverse directions are verified independently. After three evidence-bearing failures on one route family, switch to a materially different route family instead of repeating the same path.

Browser/UI submissions on configured sites may be gated by `One_Wave_Bench/reference-gate-extension/`. Its reference card must identify source, target, direction, reference, intention, consequence, selected route, and fallback routes before the action is allowed.


## Goblin control roles
Read `One_Wave_Bench/hive-pipe/GOBLIN_BRIDGE_ROLES.md` for Doctor, Parser, Reference/Worker two-state machine, Carrier Pigeon, and Goblin Raccoon behavior.
