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
├── context.py            ContextPolicy: what subset of a seat's visible
│                         history actually gets sent on each ask() call
│                         -- a recency window plus explicit pinning
├── usage.py              UsageReport + summarize(): per-seat token/price/
│                         request tracking that reports "unavailable"
│                         instead of fabricating a number
├── orchestrator.py       Council: ask() routes one round to named seats
│                         only, recording a UsageReport per reply;
│                         propose_change()/approve_and_apply()/reject()
│                         gate every file write behind an explicit
│                         approval step
├── storage.py            save/load a CouncilChat or a full Council
│                         session (including pending changes) as JSON
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
  sender.
- **`ContextPolicy` curates what a seat actually receives.** By default
  a `Council` sends the seat's full visible history (unchanged prior
  behavior). Passing `Council(chat, patch_worker, context_policy=
  ContextPolicy(max_messages=N))` caps each seat to its N most recent
  visible messages; `context_policy.pin(message_id)` keeps a specific
  message (e.g. a requirement) in every seat's context regardless of
  age. There's no AI-driven relevance ranking or summarization — that
  would itself cost an AI call, contradicting the spec's local-first
  principle — so curation is deliberately just recency + explicit pins.
- **Usage is reported, never invented.** Every `AISeat.respond()` call
  sets `self.last_usage` to a `UsageReport`; `Council.ask()` records one
  per reply in `council.usage_log[seat_id]`, retrievable via
  `council.usage_for(seat_id)` and totaled with `usage.summarize()`.
  `MockSeat` and any `RemoteAPISeat` whose client doesn't return usage
  both report `UsageReport.unavailable()` — every numeric field stays
  `None` rather than defaulting to `0`, so "no data" is never
  indistinguishable from "zero tokens used." A `RemoteAPISeat` client
  that returns `(reply_text, UsageReport(...))` instead of a bare string
  gets its real numbers recorded.

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
- **`GitWorker` has no branch/checkpoint-rollback support**, just
  status/diff/commit/log.
- **No real provider credentials exist in this environment**, so task 2
  below (wiring a real `RemoteAPISeat`) is blocked until an API key for
  some provider is actually supplied — it is not something more code
  here can unblock.

## Next five implementation tasks

1. ~~Persist `CouncilChat` (messages, seats, pending changes) to disk.~~
   **Done.** See `storage.py` — `save_chat`/`load_chat` round-trip a
   bare chat; `save_session`/`load_session` round-trip a full `Council`
   including unapproved pending changes. Live `AISeat` connections
   aren't serializable and are never fabricated on load — the caller
   re-registers whichever seats it wants against the restored seat
   identities, same honest-placeholder pattern as `RemoteAPISeat`.
2. Wire one real `RemoteAPISeat` client (start with whichever provider
   has a key available) and confirm the full demo workflow still holds
   with a genuine API call in place of a `MockSeat`. **Blocked:** no
   provider API key is available in this environment yet.
3. ~~Context curation: give the orchestrator a policy for what subset
   of the visible transcript actually gets sent to a seat.~~ **Done.**
   See `context.py` — `ContextPolicy(max_messages=N)` plus explicit
   `pin()`/`unpin()`, wired into `Council.ask()`.
4. A minimal terminal or web UI over the existing `Council`/workers —
   the file tree, diff viewer, and approve/reject controls the spec
   describes — before anything about rooms or multiple projects.
5. ~~Token/resource tracking per seat.~~ **Done.** See `usage.py` and
   `Council.usage_log`/`usage_for()` — real numbers when a
   `RemoteAPISeat` client reports them, `UsageReport.unavailable()`
   otherwise. Not yet persisted by `storage.py` (a session reload starts
   with an empty usage log) and local workers don't yet post usage into
   the log at all, since none of them do metered work today.
