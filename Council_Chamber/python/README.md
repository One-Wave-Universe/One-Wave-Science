# One-Wave Council Chamber — Beginning Goal

A shared chat and coding workspace where several AI seats and local
worker seats collaborate with one person on one local project. This is
strictly the **beginning goal** from `../PROJECT_SPECIFICATION.md`:

> A person can open several separate AI seats — including ChatGPT and
> Codex — place them into one shared conversation, let them communicate
> and help write code together, and use the local computer to preserve,
> execute, test, and verify their work.

No rooms, private AI homes, Arena Games, city systems, or GUI yet — that's
explicitly out of scope until this loop works reliably.

## What's real vs. what's a placeholder

- **The seat/message/chat model, local workers, and orchestrator are all
  real and tested.** `FileSearchWorker`, `TestWorker`, `BuildWorker`,
  `GitWorker`, and `PatchWorker` run genuine subprocess/filesystem
  operations against a real project directory.
- **There are no API keys for any external provider in this
  environment.** `ChatGPT` and `Codex` seats in the demo are `MockSeat`
  instances with canned replies — real, working implementations of the
  `AISeat` interface, just not connected to OpenAI. `RemoteAPISeat` is
  the honest placeholder for a real connection: it takes an injected
  `client` callable and raises `SeatNotConfiguredError` rather than
  fabricating a response if none is supplied.

## Run the demo

```bash
cd Council_Chamber/python
python3 -m venv .venv
source .venv/bin/activate
pip install pytest

pytest -q
python -m council_chamber.cli
```

The demo reproduces the spec's own example workflow end to end, against
a real temporary project directory:

1. User: "Add disconnect support to the AI seats."
2. ChatGPT (mock) states the requirement.
3. Codex (mock) proposes a patch — `PatchWorker.preview_diff` shows the
   real diff before anything is written.
4. User approves; `PatchWorker.apply` writes the file for real.
5. `TestWorker` runs real pytest. One test genuinely fails (the first
   patch has a real bug — `disconnect_seat` doesn't flip the flag) and
   the exact pytest failure output is posted into the chat.
6. ChatGPT (mock) explains the likely problem; Codex (mock) proposes a
   smaller repair.
7. User approves; `PatchWorker.apply` writes the fix.
8. `TestWorker` runs again and both tests genuinely pass.

## Architecture

```
council_chamber/
├── models.py            Seat, Message, CouncilChat -- the shared log.
│                         Posting is inert: nothing auto-responds.
├── seats/
│   └── ai_seat.py        AISeat interface, MockSeat (real, for tests/
│                         demo), RemoteAPISeat (honest placeholder --
│                         needs an injected client to do anything)
├── workers/
│   ├── file_search.py    find_files / search_text / find_symbol
│   ├── test_worker.py    runs a real test command, reports exact failures
│   ├── build_worker.py   runs a real build/start command
│   ├── git_worker.py     status / diff / checkpoint / log
│   └── patch_worker.py   preview_diff (no write) / apply (writes,
│                         rejects paths escaping the project root)
├── orchestrator.py       Council: ask() routes one round to named seats
│                         only; propose_change()/approve_and_apply()/
│                         reject() gate every file write behind an
│                         explicit approval step
└── cli.py                the end-to-end demo above
```

## Design points worth knowing

- **`CouncilChat.post()` never triggers a response.** Only an explicit
  `Council.ask([seat_ids], prompt)` call queries seats, and only the
  seats named in that call — "the system must not allow the AIs to
  generate an uncontrolled endless conversation."
- **A proposed change is never written until `approve_and_apply()` is
  called on that specific `file_path`.** `propose_change()` only posts a
  diff preview into the chat.
- **`PatchWorker` refuses to write outside the project root**
  (`PathEscapesProjectRootError`), even if a proposed `file_path` tries
  to `..`  its way out.
- **Message visibility is per-message, not per-seat-pair.** `visible_to`
  defaults to everyone; a restricted list still always includes the
  sender. There's no context-curation logic yet beyond that — the spec's
  "an AI seat receives only the information relevant to its current
  task" is currently just "everything visible to it," which is honest
  but not yet curated down.

## Known limitations

- **No real provider connections.** ChatGPT/Codex/Gemini/DeepSeek/local
  models are all unconnected in this environment. `RemoteAPISeat` is
  ready to wire up given an API client callable, but none has been
  tested against a real API.
- **No GUI.** Everything here is a library plus one CLI demo. The
  spec's "file tree / code editor / diff viewer / approve and reject
  controls" panel layout doesn't exist yet.
- **No context curation.** Every seat currently sees the full chat
  history visible to it; there's no summarization or relevance-ranking
  to keep long sessions cheap, despite the spec calling for it.
- **No persistent storage.** `CouncilChat` and `Council` are in-memory
  only — closing the process loses the transcript, pinned requirements,
  decisions, and task list the spec describes as belonging to local
  memory.
- **`GitWorker` has no branch/checkpoint-rollback support**, just
  status/diff/commit/log.

## Next five implementation tasks

1. Persist `CouncilChat` (messages, seats, pending changes) to disk —
   JSON or SQLite, matching the "local memory" section of the spec —
   so a session survives a restart.
2. Wire one real `RemoteAPISeat` client (start with whichever provider
   has a key available) and confirm the full demo workflow still holds
   with a genuine API call in place of a `MockSeat`.
3. Context curation: give the orchestrator a policy for what subset of
   the visible transcript actually gets sent to a seat, instead of the
   full visible history every time.
4. A minimal terminal or web UI over the existing `Council`/workers —
   the file tree, diff viewer, and approve/reject controls the spec
   describes — before anything about rooms or multiple projects.
5. Token/resource tracking per seat (`RemoteAPISeat` reporting real
   usage from its client's response, `MockSeat`/local workers reporting
   "usage unavailable" rather than a fabricated number).
