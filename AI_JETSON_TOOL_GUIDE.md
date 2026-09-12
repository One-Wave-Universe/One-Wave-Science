# AI Jetson Tool Guide

This is the shortest correct guide for a fresh AI/Claude/Codex/Gemini instance.

## Start here

The canonical Jetson tool path is:

```text
client -> HTTPS/MCP -> hive-pipe/gateway.py -> terminal_parser.py -> Jetson process
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
```

Do not assume the old `/v1/exec` gateway is active. Do not start
`scripts/jetson_gateway.py` beside Hive Pipe; it uses the same port 8765.

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

Normal AI terminal access blocks:

```text
sudo / su / doas / pkexec
raw disk formatting/partition tools
mount/unmount
shutdown/reboot/poweroff
shell -c / -lc strings
credential/private-key paths
```

The service sandbox permits writes to the One-Wave checkout and the explicit
`~/One-Wave-External-Work` workspace. System paths remain read-only.

## Full reference

Read `JETSON_AI_ACCESS.md` for setup, tokens, tunnel configuration, all paths,
and the ten-step acceptance test.
