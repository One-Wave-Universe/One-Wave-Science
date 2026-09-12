# Hive Pipe

Hive Pipe is the bounded queue between an assistant and the Jetson terminal.
Version 1 deliberately accepts named, read-only actions instead of arbitrary
shell text.

## Protocol

```text
queue/pending/<job-id>.json
        -> agent.sh
        -> mudl.py run
        -> queue/results/<job-id>.json
        -> queue/done/<job-id>.json
```

A request is JSON:

```json
{
  "version": 1,
  "id": "20260912T170000Z-drive-inventory",
  "action": "inventory_block_devices",
  "created_utc": "2026-09-12T17:00:00Z"
}
```

The runner rejects unknown keys, malformed IDs, duplicate results, symlinks,
and all actions not listed by `python3 hive-pipe/mudl.py actions`.

## Install on the Jetson

From the canonical checkout:

```bash
cd "$HOME/One-Wave-Science"
chmod +x hive-pipe/agent.sh hive-pipe/queue_self.sh
```

Run one queued job:

```bash
bash hive-pipe/agent.sh --once
```

Or keep the local runner waiting for jobs:

```bash
bash hive-pipe/agent.sh --watch
```

## First safe job

```bash
bash hive-pipe/queue_self.sh inventory_block_devices
bash hive-pipe/agent.sh --once
ls hive-pipe/queue/results/
```

`inventory_block_devices` calls `lsblk` with explicit read-only reporting
columns. It does not mount, unmount, format, partition, repair, or write to a
device.

## Transport boundary

This directory defines and tests the Jetson-side queue. A remote assistant can
submit requests only when `queue/pending` and `queue/results` are exposed by an
explicit synchronization transport. Do not use `main` as a live command bus and
do not auto-commit results into the science repository. Transport credentials,
SSH keys, API tokens, and device secrets must stay outside this repository.

Until a transport is configured, Hive Pipe is a verified local Jetson runner,
not a claim of remote terminal access.

## Agent Gateway

`gateway.py` exposes the same named-action queue over authenticated HTTP. It
binds only to `127.0.0.1:8765`; never bind it directly to a public interface.

Install both per-user services (queue worker plus gateway) and create separate
local tokens for Codex, Claude, and Gemini:

```bash
bash hive-pipe/install_gateway.sh
```

Verify that both halves are running:

```bash
systemctl --user status hive-pipe-agent.service hive-pipe-gateway.service
```

Check the localhost endpoint with one token:

```bash
TOKEN="$(cat "$HOME/.config/hive-pipe/tokens/codex.token")"
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8765/v1/health
```

An authenticated reverse tunnel may publish this localhost endpoint. Configure
the tunnel provider outside the repository, keep its credentials outside the
repository, require HTTPS, and retain the gateway bearer token as a second
authentication layer. Each AI gets a different token so access can be revoked
individually.

The gateway still does not accept raw command strings. Broader terminal actions
must be added as named actions with their own validation and tests.

## MCP adapter

The same gateway provides a sessionless Streamable HTTP MCP endpoint at `/mcp`.
It supports `initialize`, `ping`, `tools/list`, and `tools/call`. Every MCP tool
maps one-to-one to the existing `mudl.ACTIONS` allowlist, takes no arguments, and
waits for the queue worker's result. Raw shell text and arbitrary paths remain
invalid, so the adapter cannot write to `Virtual_Breadboard/` or to a disk.

Use the public HTTPS tunnel URL plus `/mcp` when adding the connector. Supply the
Codex bearer token through the connector's secret/authentication UI; never put
the token in a chat message, URL, repository file, or Cloudflare command line.
