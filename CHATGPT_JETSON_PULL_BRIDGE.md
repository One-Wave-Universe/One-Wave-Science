# ChatGPT -> One-Wave Resilient Terminal Bridge

This is the no-GitHub-Actions-secret path for bounded terminal work on either
the Ubuntu laptop or the Jetson. Install it on the machine ChatGPT must operate.
It has two independent loops: a transport state machine and a request state
machine.

## Path

```text
ChatGPT GitHub connector
  -> chatgpt-terminal branch
  -> .chatgpt-terminal/request.json
  -> laptop/Jetson user service polls primary and backup Git routes
  -> hive-pipe/terminal_parser.py
  -> local non-root command on the machine running the service
  -> .chatgpt-terminal/result.json
  -> target-machine git push
  -> ChatGPT GitHub connector reads result
```

The worker does not use the remote MCP bearer token because execution occurs on
the target machine itself. It deliberately reuses `hive-pipe/terminal_parser.py`,
so blocked programs (including inside shell wrappers), sensitive-path checks,
timeout/output limits, and authorized work-root checks remain in force.

## The two state machines

1. **Transport state machine:** tries `origin:chatgpt-terminal`, then
   `origin:chatgpt-terminal-backup`, plus any configured mirror routes. Healthy
   routes gain preference. Failed routes enter exponential backoff and are
   probed again later. A result is returned through the first writable healthy
   back route.
2. **Request state machine:** journals `accepted -> executing -> completed ->
   acknowledged`. The executing phase is recorded before launch. After a crash,
   an uncertain command is not silently repeated; the bridge returns a
   reconciliation receipt and asks for inspection.

This gives failover without duplicate side effects. No finite set of routes can
promise connectivity during every provider, power, or hardware failure, so
pending results remain in a durable local outbox until a configured route heals.

## Parser reference and intervention guidance

MCP clients can call `terminal_reference` with no arguments. Every command
receipt also includes `guidance` and a reference pointer. Guidance names whether
the next action is:

- a normal AI correction;
- creation/authorization of a dedicated work path;
- tool installation;
- authentication repair; or
- an approved human/root-level action outside the parser.

The parser explains the boundary; it never bypasses it.

## Runtime isolation

The bridge no longer depends on the branch state of the user's active `~/One-Wave-Science` checkout. That checkout may be ahead, behind, dirty, or diverged.

The installer creates and owns a private runtime clone at:

```text
~/.local/share/one-wave-chatgpt-terminal-runtime
```

Only that bridge runtime is reset to `origin/main`. The user's active project checkout is never merged, reset, rebased, or switched by bridge installation or polling.

## Files

- `hive-pipe/chatgpt_terminal_pull.py` — polling/execution/result worker
- `hive-pipe/install_chatgpt_terminal_pull.sh` — isolated-runtime user-systemd installer
- `hive-pipe/bootstrap_chatgpt_terminal_pull.sh` — fetch-only bootstrap helper
- dedicated transport branch: `chatgpt-terminal`
- request: `.chatgpt-terminal/request.json`
- result: `.chatgpt-terminal/result.json`

## One-time activation on the Ubuntu laptop or Jetson

From inside the existing checkout on the machine to control:

```bash
cd "$HOME/One-Wave-Science"
git fetch origin main
git show origin/main:hive-pipe/install_chatgpt_terminal_pull.sh | ONE_WAVE_PROJECT_ROOT="$PWD" bash
```

This reads the current installer directly from `origin/main` without merging
`main` into the active laptop/Jetson branch.

Verify:

```bash
systemctl --user is-active one-wave-chatgpt-terminal-pull.service
```

Expected:

```text
active
```

This activation does not need a Cloudflare tunnel or GitHub Actions secrets. It
does require the machine's existing GitHub read/write authentication so the
runtime can fetch requests and push receipts.

The two default transport branches must exist:

```text
chatgpt-terminal
chatgpt-terminal-backup
```

To add a true provider/mirror route, configure another Git remote in the private
runtime clone and extend the service environment, for example:

```text
CHATGPT_TERMINAL_ROUTES=primary=origin:chatgpt-terminal,backup=origin:chatgpt-terminal-backup,mirror=mirror:chatgpt-terminal
```

Route errors and the required repair/path-creation action are recorded in:

```text
~/.local/state/one-wave-chatgpt-terminal/bridge_state.json
```

Status is available without executing a command:

```bash
python3 ~/.local/share/one-wave-chatgpt-terminal-runtime/hive-pipe/chatgpt_terminal_pull.py --status
journalctl --user -u one-wave-chatgpt-terminal-pull.service -n 100 --no-pager
```

## Request format

```json
{
  "id": "printer-diagnostic-001",
  "argv": ["lpstat", "-t"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

The worker records request id + request commit locally and will not rerun the same request commit.

## Printer diagnostics

The initial queued request checks CUPS status, configured queues, USB devices, and printer backends. Follow-up requests should stay bounded so one missing command does not hide other evidence.

Do not add `sudo` or weaken the terminal parser to repair a printer. If a repair requires a privileged package/service operation, the bridge reports the exact required action rather than bypassing the safety boundary.

## Safety / branch isolation

The worker fetches `origin/chatgpt-terminal`, executes only structured `argv` through the existing parser, then uses a temporary detached git worktree to write `result.json`. The user's active branch/worktree is not switched or reset.

The service runs as the normal user with `NoNewPrivileges=true`, `ProtectSystem=strict`, and explicit writable paths for the bridge runtime, bridge state, the project checkout, and the external-work directory.
