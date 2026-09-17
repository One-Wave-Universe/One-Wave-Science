# ChatGPT -> Jetson Terminal Bridge

## Purpose

This bridge lets an authorized GitHub-connected ChatGPT session request a normal, non-root Jetson terminal command without exposing Hive Pipe tokens in chat or in the repository.

It does **not** replace Hive Pipe. It is a small GitHub request/result lane over the existing canonical path:

```text
ChatGPT GitHub connector
  -> chatgpt-terminal branch
  -> .chatgpt-terminal/request.json
  -> GitHub Actions
  -> authenticated Hive Pipe /mcp terminal_run
  -> Jetson terminal_parser.py
  -> .chatgpt-terminal/result.json
  -> ChatGPT GitHub connector
```

The Jetson parser remains the command safety boundary. The bridge cannot bypass parser restrictions, the Jetson service sandbox, normal-user permissions, or blocked credential/private-key paths.

## Dedicated command branch

After the bridge workflow is merged to `main`, create a dedicated branch from current `main`:

```text
chatgpt-terminal
```

Normal project work must not happen on that branch. It carries only terminal request/result traffic.

## Request format

ChatGPT writes or updates:

```text
.chatgpt-terminal/request.json
```

Example:

```json
{
  "id": "printer-check-001",
  "argv": ["lpstat", "-t"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Required:

- `id`: non-empty string, max 128 characters
- `argv`: non-empty JSON array of non-empty strings

Optional:

- `cwd`: absolute path; defaults to `/home/Scales/One-Wave-Science`
- `timeout`: integer 1..300; defaults to 120

A new commit changing only `request.json` triggers `.github/workflows/chatgpt-terminal-bridge.yml`.

## Result format

The workflow writes:

```text
.chatgpt-terminal/result.json
```

The result contains the matching request `id`, command argv, stdout, stderr, exit code, Jetson cwd/duration when provided by Hive Pipe, and bridge/RPC errors when applicable.

The result commit includes `[skip ci]`; the workflow path filter watches only `request.json`, so result commits do not recurse.

## First acceptance test

Request:

```json
{
  "id": "bridge-smoke-001",
  "argv": ["printf", "CHATGPT_JETSON_BRIDGE_OK"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Expected result:

```text
stdout = CHATGPT_JETSON_BRIDGE_OK
exit_code = 0
ok = true
```

## Printer diagnostic request

A useful non-destructive printer check is:

```json
{
  "id": "printer-diagnostic-001",
  "argv": ["bash", "-lc", "printf '\\n=== CUPS ===\\n'; systemctl is-active cups; printf '\\n=== PRINTERS ===\\n'; lpstat -t; printf '\\n=== USB ===\\n'; lsusb"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Normal-user diagnostics should work if the relevant programs are installed. Privilege escalation remains blocked by the Jetson parser; do not weaken that boundary merely to repair a printer.

## Security / anti-drift rules

1. Tokens stay in GitHub Actions secrets and on the Jetson. Never place them in request/result JSON.
2. Only the dedicated `chatgpt-terminal` branch triggers this workflow.
3. Only changes to `.chatgpt-terminal/request.json` trigger a command.
4. The bridge sends only `terminal_run` requests to the existing `/mcp` endpoint.
5. All command validation and system access restrictions already enforced by `terminal_parser.py` remain active.
6. Do not add `sudo`, root credentials, disk-management bypasses, token readers, or a second unrestricted execution path.
7. Project edits still use task branches and PRs; the terminal branch is command transport only.
