# ChatGPT -> Jetson Pull Terminal Bridge

This is the no-GitHub-Actions-secret path for ChatGPT terminal work.

## Path

```text
ChatGPT GitHub connector
  -> chatgpt-terminal branch
  -> .chatgpt-terminal/request.json
  -> Jetson user service polls GitHub
  -> hive-pipe/terminal_parser.py
  -> local non-root command
  -> .chatgpt-terminal/result.json
  -> Jetson git push
  -> ChatGPT GitHub connector reads result
```

The worker does not use the remote MCP bearer token because execution occurs on the Jetson itself. It deliberately reuses `hive-pipe/terminal_parser.py`, so blocked programs, sensitive-path checks, timeout/output limits, and authorized work-root checks remain in force.

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

## One-time Jetson activation from a diverged checkout

From inside the existing Jetson checkout:

```bash
cd "$HOME/One-Wave-Science"
git fetch origin main
git show origin/main:hive-pipe/install_chatgpt_terminal_pull.sh | ONE_WAVE_PROJECT_ROOT="$PWD" bash
```

This reads the current installer directly from `origin/main` without merging `main` into the active Jetson branch.

Verify:

```bash
systemctl --user is-active one-wave-chatgpt-terminal-pull.service
```

Expected:

```text
active
```

This activation does not need a Cloudflare tunnel or GitHub Actions secrets. It does require the Jetson's existing GitHub read/write authentication so the runtime can fetch the command branch and push result commits.

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
