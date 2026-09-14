# One-Wave Access — Entry Point for Any AI or Human Working on This Repo

**Purpose:** one place to answer "how do I actually reach and work on
this repository," including the specific case of an AI worker that has
no GitHub API/tool access but does have a terminal, and needs to reach
the Jetson and the repo through it. This file summarizes; it does not
replace the fuller docs it links to.

## The short answer

Yes — there is a working (not just planned) path for an AI without
GitHub access to use a terminal and the Jetson to reach this repo. Two
of the three documented routes specifically do not require GitHub at
all.

## The three access routes (`JETSON_AI_ACCESS.md`, full detail)

```text
AI / operator
   +-- 1. SSH terminal ------------------> Jetson login shell
   +-- 2. GitHub workflow_dispatch ------> GitHub-hosted runner -> gateway
   +-- 3. HTTPS gateway / Cloudflare ----> 127.0.0.1:8765 -> Jetson user shell
```

| Route | Needs GitHub? | What it gives you |
|---|---|---|
| 1. Direct SSH | No | Full normal-user shell on the Jetson. Ordinary `git status`/`pull`/`push` works exactly as for a human, once authorized. Setup: `scripts/enable_jetson_ssh.sh`, optionally with `AI_SSH_PUBLIC_KEY` to authorize a specific client key. |
| 2. GitHub `workflow_dispatch` | Yes | Dispatches `.github/workflows/jetson-command.yml`, which sends an authenticated command to the same gateway as route 3. Only useful if you *do* have GitHub Actions access. |
| 3. Direct HTTPS gateway | No | Any HTTPS-capable client hits the bearer-token-authenticated `/v1/exec` endpoint directly, no GitHub involved: `scripts/jetson_remote.sh --cwd /home/Scales/One-Wave-Science -- 'git status --short'`. |

For an AI with a terminal but no GitHub tool access, routes 1 and 3 are
the ones that matter. Route 1 is the simplest and most direct: SSH in,
you have a real shell, `git` works normally.

## Two gateway implementations exist — they are not duplicates

Checked directly (2026-09) after noticing both exist:

- **`scripts/jetson_gateway.py`** — the gateway `JETSON_AI_ACCESS.md`
  describes. Runs **arbitrary shell commands** via `/v1/exec`, behind a
  Cloudflare tunnel, bearer-token authenticated, bound to loopback,
  refuses to run as root.
- **`hive-pipe/gateway.py`** — a separate, more restricted system.
  Deliberately accepts only a small set of **named, non-shell actions**
  from a job queue (`queue/pending/ -> agent.sh -> mudl.py run ->
  queue/results/`), not arbitrary shell text. Its own README states
  this restriction as a deliberate v1 design choice, not a limitation
  to work around. See `hive-pipe/README.md` for the actions list
  (`python3 hive-pipe/mudl.py actions`).

These are two different trust levels for two different situations, not
competing implementations of the same thing — the raw-shell gateway for
trusted full-command access, the bounded queue for a lower-trust,
more auditable action set. Do not merge them or treat one as
superseding the other without a deliberate decision to do so.

## Safety notes that apply to all routes

- All three routes run as a **normal non-root user**. `sudo` stays an
  explicit human-controlled escalation, never automated.
- `scripts/jetson_gateway.py` supports an emergency stop:
  `touch ~/.config/hive-pipe/DISABLED` fails closed on `/v1/exec` (health
  endpoint stays up) without touching configuration; `rm` the file to
  resume. SSH remains independent of this and keeps working regardless.
- Never guess a Jetson IP, username, or checkout path — `JETSON_ACCESS_AND_TERMINAL.md`
  gives the exact `whoami`/`hostname`/`find` commands to verify each
  before connecting or editing.
- Do not put the gateway bearer token in the repository or a workflow
  input; it lives in `~/.config/hive-pipe/gateway.token` on the Jetson
  and as a GitHub Actions secret if route 2 is used.

## If you're an AI session without a Jetson connection at all

This document assumes network/SSH reachability to a specific Jetson
device exists for your session. If it doesn't (e.g. a sandboxed cloud
session with no route to that hardware), none of the three routes
apply — you're limited to whatever git remote access your own
environment already provides (an HTTPS git remote, a GitHub App/MCP
integration, etc.), which is a separate question from what this file
covers.

## Full detail

- `JETSON_AI_ACCESS.md` — the three routes, setup commands, acceptance
  test (7 steps), logs, emergency stop/recovery.
- `JETSON_ACCESS_AND_TERMINAL.md` — safe first-contact rules (don't
  guess IPs/usernames/paths, don't format drives, verify before editing),
  repository entry, external-drive discovery.
- `hive-pipe/README.md` — the bounded named-action queue protocol.
- `JETSON_OPENCLAW_RUNTIME.md`, `JETSON_GEMINI_MINIMAL.md` — related
  runtime/agent-specific setup, not access-path documents.

Any contributor who finds a more reliable path should update
`JETSON_ACCESS_AND_TERMINAL.md` directly (it already asks for this) and
update this summary to match.
