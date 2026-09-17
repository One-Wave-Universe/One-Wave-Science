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

## Files

- `hive-pipe/chatgpt_terminal_pull.py` — polling/execution/result worker
- `hive-pipe/install_chatgpt_terminal_pull.sh` — user-systemd installer
- dedicated transport branch: `chatgpt-terminal`
- request: `.chatgpt-terminal/request.json`
- result: `.chatgpt-terminal/result.json`

## One-time Jetson activation

From the canonical Jetson checkout:

```bash
cd "$HOME/One-Wave-Science"
git pull --ff-only origin main
bash hive-pipe/install_chatgpt_terminal_pull.sh
```

Verify:

```bash
systemctl --user is-active one-wave-chatgpt-terminal-pull.service
```

Expected:

```text
active
```

This activation does not need a Cloudflare tunnel or GitHub Actions secrets. It does require the Jetson checkout's existing GitHub read/write authentication so it can fetch the command branch and push result commits.

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

## Smoke test

Write this to `.chatgpt-terminal/request.json` on `chatgpt-terminal`:

```json
{
  "id": "pull-smoke-001",
  "argv": ["printf", "CHATGPT_JETSON_PULL_OK"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Expected `.chatgpt-terminal/result.json`:

```text
ok = true
exit_code = 0
stdout = CHATGPT_JETSON_PULL_OK
```

## Printer diagnostics

After the smoke test, use separate bounded requests so one missing command does not hide other evidence:

1. `systemctl --user` is not appropriate for system CUPS; query `systemctl is-active cups` as ordinary user.
2. `lpstat -t`
3. `lsusb`
4. `lpinfo -v` if available

Do not add `sudo` or weaken the terminal parser to repair a printer. If a repair requires root package/service changes, report the exact required privileged action to the operator.

## Safety / branch isolation

The worker fetches `origin/chatgpt-terminal`, executes only the structured `argv` through the existing parser, then uses a temporary detached git worktree to write `result.json`. The user's active branch/worktree is not switched or reset.

The service runs as the normal user with `NoNewPrivileges=true`, `ProtectSystem=strict`, and a narrow writable state/repo scope.
