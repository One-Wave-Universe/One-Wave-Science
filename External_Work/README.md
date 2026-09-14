# External Work Handoff

This directory is the GitHub-visible handoff for work that also needs to exist in
a Jetson-local external workspace.

## Direction 1: GitHub -> Jetson external workspace

Put reviewable files in:

```text
External_Work/inbox/
```

On the Jetson run:

```bash
python3 scripts/external_work_bridge.py pull
```

That copies regular files to:

```text
~/One-Wave-External-Work/inbox/
```

The Jetson-local working area is:

```text
~/One-Wave-External-Work/work/
```

## Direction 2: Jetson external workspace -> GitHub

Place results intended for GitHub review in:

```text
~/One-Wave-External-Work/outbox/
```

Then run:

```bash
python3 scripts/external_work_bridge.py publish
```

That stages copies under:

```text
External_Work/outbox/
```

The bridge **does not commit or push**. Review the files, use a task branch, then
commit/push and open a PR. Do not silently write external results directly to
`main`.

## Status

```bash
python3 scripts/external_work_bridge.py status
```

## Rules

- Regular files only; symlinks are refused.
- Individual files larger than 64 MiB are refused by the bridge.
- Secrets, tokens, private keys, credentials, and machine identity files do not
  belong in this handoff.
- Large generated artifacts should use a deliberate artifact/storage path rather
  than being dropped into the science repository.
- `ONE_WAVE_EXTERNAL_WORK=/some/path` may override the default local workspace.
- The default `hive-pipe/install_gateway.sh` grants the AI terminal parser write
  access to `~/One-Wave-External-Work` in addition to the checked-out repo.
