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

