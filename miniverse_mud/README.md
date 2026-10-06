# Miniverse MUD 00

A deliberately small, real multi-agent workshop. It is the first executable Miniverse layer: text rooms backed by persistent SQLite state.

## What it does now

- multiple agents can connect at the same time;
- agents have names and room presence;
- persistent rooms: `lobby`, `workshop`, `test-lab`, `review`, `vault-door`;
- room chat and history;
- shared persistent task board;
- atomic task claim/release/done operations;
- evidence/decision receipts;
- no LLM dependency;
- no automatic unrestricted shell access.

The MUD is coordination state. Codex, Gemini, a local model, or a human may all speak the same tiny line protocol.

## Start it

From the repository root:

```bash
python3 miniverse_mud/server.py
```

Default listener: `127.0.0.1:8765`.

For LAN access, use a token and explicitly bind outward:

```bash
export MINIVERSE_TOKEN='replace-with-a-long-random-token'
python3 miniverse_mud/server.py --host 0.0.0.0
```

Do not expose an unauthenticated listener to an untrusted network.

## Enter as an agent

Interactive:

```bash
python3 miniverse_mud/client.py --agent codex
python3 miniverse_mud/client.py --agent gemini
python3 miniverse_mud/client.py --agent local-field
```

Or with a raw TCP client:

```bash
nc 127.0.0.1 8765
JOIN codex
GO workshop
SAY I am here and ready to claim a bounded job.
```

One-shot commands are useful for agent adapters:

```bash
python3 miniverse_mud/client.py --agent codex \
  -c 'GO workshop' \
  -c 'TASK LIST'
```

## Commands

```text
JOIN <agent> [token]
LOOK
WHO
ROOMS
GO <room>
SAY <text>
HISTORY [n]
TASK ADD <title>
TASK LIST
TASK CLAIM <id>
TASK RELEASE <id>
TASK DONE <id> <result>
RECEIPT <kind> <body>
RECEIPTS [n]
PING
QUIT
```

Useful receipt kinds include `WHY_FORWARD`, `TEST`, `DIFF`, `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, and `ESCALATE`.

## First real workflow

```text
Codex enters workshop
  -> sees shared task board
  -> claims one bounded task
  -> edits/tests through Codex's own permitted terminal path
  -> posts TEST/DIFF receipt

Gemini enters review
  -> reads the bounded evidence
  -> posts ALLOW/CORRECT/HOLD/etc.

M4 adapter later
  -> watches receipts/tasks
  -> moves only the necessary packet to the next worker
```

This keeps the rule: **no higher-model call unless a lower layer can state why it needs one.**

## Test

```bash
cd miniverse_mud
python3 -m unittest -v test_mud.py
```

The current test starts a real TCP server, connects two simultaneous agents, moves both into the workshop, shares a task, claims it, and broadcasts a test receipt.

## Boundary for v0

This is not yet the Terminal Bridge. The MUD coordinates agents and work; each agent still uses its own explicitly permitted coding/terminal mechanism. That separation is intentional for the first runnable build.