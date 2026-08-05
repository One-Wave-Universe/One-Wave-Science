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
- **`ChatGPT` and `Codex` in the demo are still `MockSeat` placeholders**
  (canned replies, real implementation of the `AISeat` interface, no
  provider connected). `RemoteAPISeat` is the general honest-placeholder
  pattern: it takes an injected `client` callable and raises
  `SeatNotConfiguredError` rather than fabricating a response if none is
  supplied.
- **One real provider connection exists: `seats/gemini_client.py`.**
  `make_gemini_client()` makes a genuine HTTPS call to
  `generativelanguage.googleapis.com` (stdlib `urllib`, no extra
  dependency) and returns `(reply_text, UsageReport)` with the real
  token counts Google reports. Wire it up with:
  ```python
  from council_chamber.seats.ai_seat import RemoteAPISeat
  from council_chamber.seats.gemini_client import make_gemini_client
  seat = RemoteAPISeat(Seat.create("Gemini", SeatKind.AI), client=make_gemini_client())
  ```
  It reads `GEMINI_API_KEY` from the environment (or pass `api_key=`
  directly) and raises `GeminiNotConfiguredError` if neither is set. A
  real API error (bad key, quota exhausted, ...) raises `GeminiAPIError`
  with Google's own message — it is never caught and turned into a fake
  reply. Verified end to end against the real API: a live key returned a
  real HTTP 429 (`RESOURCE_EXHAUSTED`, free-tier quota limit 0 on that
  key's Google Cloud project) which `GeminiAPIError` surfaced correctly;
  no completion has come back yet because that project's quota is 0
  until its owner enables billing, but the whole request/response/error
  path is proven working over the real network.

## Attaching your own seat (self-service, zero-cost mechanism)

Anyone — a human, or another AI seat that's writing code through
`propose_change`/`approve_and_apply` — can attach a new real provider
without touching `tui.py`, `worker_ant.py`, or any other existing file.
Drop a new file into `council_chamber/seats/` named `<something>_client.py`
following the shape `gemini_client.py` already uses:

```python
# council_chamber/seats/openai_client.py
def make_openai_client(model="gpt-5", api_key=None):
    # read api_key or an env var; raise a clear *NotConfigured* error
    # if neither is set -- never fabricate a reply
    def client(context):
        # make a real API call; raise a clear *APIError* with the
        # provider's own message on failure
        return reply_text, usage_report   # or just reply_text
    return client

from council_chamber.client_registry import register_client
register_client("chatgpt", "ChatGPT", make_openai_client)
```

That's the entire interface — exactly what `RemoteAPISeat(seat,
client=...)` already accepts (a callable returning either a bare string
or `(text, UsageReport)`). `client_registry.discover_and_register_clients()`
imports every `seats/*_client.py` file on startup so the
`register_client(...)` call actually runs, and both `tui.py`'s `open
<key>` and `worker_ant.py`'s session-reload path check this registry
first — using the real client if its factory can configure itself (e.g.
an API key env var is set), and falling back to an honestly-labeled
"not configured" placeholder otherwise, never a fabricated reply.

**This costs nothing by itself.** The registry, the file discovery, and
the fallback are all local file I/O — the only thing that ever costs
money is whichever specific provider a client file actually calls, and
that's opt-in per file. Verified live: a throwaway `zzdemo_client.py`
was dropped in with no edits anywhere else, and `open zzdemo` picked it
up and answered for real on the first try.

## Run the demo

```bash
cd Council_Chamber/python
python3 -m venv .venv
source .venv/bin/activate
pip install pytest

pytest -q
python -m council_chamber.cli
```

## Run the interactive terminal UI

```bash
cd Council_Chamber/python
python3 -m council_chamber.tui [project_dir]   # defaults to the current directory
```

Opens a real `council>` prompt over a real `Council` (ChatGPT and Codex
already open as `MockSeat` placeholders, same honest caveat as the demo)
in a room called `main`, against the given project directory. Type
`help` for the full command list: `rooms`, `room <name>`, `create-room
<name> [dir]`, `branch <parent> <side>`, `files [glob]`, `cat <file>`,
`seats`, `open <chatgpt|codex|claude|gemini|deepseek|grok|local>`,
`ask <seat[,seat...]> <prompt>`, `propose <seat> <file> <content> [--desc
"..."]`, `pending`, `diff <file>`, `approve <file>`, `reject <file>
[reason]`, `usage <seat>`, `usage-summary <seat>`, `transcript`, `save
<path>`, `load <path>`, `quit`. Every command runs against a real
`Council`, `PatchWorker`, and chat log — nothing here is simulated for
display only. `CouncilTUI.execute(line)` is the same entry point the
tests use, so the whole interface is exercised without a real terminal.

- **`open <key>` isn't ChatGPT/Codex-specific.** `SEAT_CATALOG` lists
  every seat kind the spec names — ChatGPT, Codex, Claude, Gemini,
  DeepSeek, Grok, a local model — and any of them can be opened,
  `ask`ed, and used with `propose` the same way. There is nothing in
  `propose_change`/`approve_and_apply` that special-cases which seat
  supplied the code.
- **`save`/`load` persist presence and conversation across restarts.**
  `save <path>` writes the chat, open seats, and any pending
  (unapproved) changes to disk via `storage.py`. `load <path>` restores
  all of that and re-attaches every AI-kind seat as a `MockSeat`
  placeholder automatically, so seats stay usable immediately after a
  reload — swap in a real `RemoteAPISeat` client afterward to reconnect
  a seat for real. Only the transcript, seat identities, and pending
  changes persist; a live provider connection was never serializable to
  begin with, so there's nothing fabricated in what comes back.

### Rooms and side rooms (`rooms.py`)

Every `Council` now lives inside a **room** — a name plus its own chat
and its own project directory. The TUI starts in a room called `main`.

- **`create-room <name> [dir]`** makes a brand new, empty room and
  switches to it. `dir` defaults to `./<name>`.
- **`branch <parent> <side_name>`** makes a **side room**: a real copy
  of the parent room's files, plus a brand new, empty chat (no shared
  transcript, no shared seats with the parent) — a place to try
  something risky. `open`, `propose`/`approve`, and a real `TestWorker`
  run all work inside a side room exactly like anywhere else, against
  its own copy of the files, so nothing there can touch the parent
  room's real code until someone redoes the same
  `propose_change`/`approve_and_apply` against the parent directly —
  there's no automatic merge, just the same gated flow run twice: once
  to validate, once for real.
- **`files [glob]`** and **`cat <file>`** let a seat (or you) see the
  current room's actual code — `cat` refuses to read outside the
  room's own directory, the same `PathEscapesProjectRootError`-style
  guard `PatchWorker` uses for writes.
- **`room <name>`** switches which room subsequent commands (`seats`,
  `ask`, `propose`, `transcript`, ...) operate on; `rooms` lists every
  room with `*` marking the current one.

Verified live end to end: branched a room, had a seat `propose`/`approve`
a real fix to `main.py` inside the side room only, ran a real `pytest`
subprocess against that side room's copy (it passed), then switched
back to the parent room and confirmed its `main.py` was completely
untouched.

## Checking in with an idle seat (worker_ant.py)

```bash
cd Council_Chamber/python
python3 -m council_chamber.worker_ant session.json . Gemini "anything to report?"
```

Loads `session.json`, asks the named seat(s) once, saves the reply back.
Add `--every SECONDS --times N` to repeat the same check-in prompt N
times with a real delay between rounds — the "talk to the AI while it's
idle" pattern:

```bash
python3 -m council_chamber.worker_ant session.json . Gemini "anything to report?" --every 60 --times 20
```

This is still not an autonomous loop: `--times` is a number you choose
explicitly (no infinite default), the prompt is the same one you gave
each round, and it's a plain foreground process you can Ctrl+C anytime.
Every round is still one `Council.ask()` call under the same "only
named seats respond, only when asked" gate as everything else — see the
module docstring for why that's a hard line, not a preference.

To get another AI's own real seat attached (not just Gemini), see
`../ATTACH_A_SEAT.md` — a copy-paste prompt you hand to that AI so it
writes its own `seats/<x>_client.py`, following the exact contract
`client_registry.py` documents.

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
│   ├── ai_seat.py        AISeat interface, MockSeat (real, for tests/
│   │                     demo), RemoteAPISeat (honest placeholder --
│   │                     needs an injected client to do anything)
│   └── gemini_client.py  real Gemini REST client for RemoteAPISeat --
│                         genuine HTTPS calls, real errors, real usage
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
├── client_registry.py    self-service seat registry -- drop in a new
│                         seats/<x>_client.py, no other file changes,
│                         and it's usable via `open <key>`
├── worker_ant.py         one bounded, local, file-driven relay round
│                         over a saved session -- never an autonomous
│                         loop, always one deliberate invocation
├── rooms.py              World/Room: named places, each its own chat +
│                         project dir; branch_room() makes a side room
│                         -- a copy to test in, isolated from the parent
├── tui.py                CouncilTUI: a real command interpreter (rooms/
│                         room/branch/files/cat/seats/open/ask/propose/
│                         diff/approve/reject/usage/transcript/save/load)
│                         plus repl() for interactive use
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
- **No graphical UI.** `tui.py` covers the spec's diff-viewer /
  approve-reject loop as a real terminal command interpreter, but there
  is no file tree, code editor pane, or windowed layout — those would
  need an actual GUI or web frontend.
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
4. ~~A minimal terminal or web UI over the existing `Council`/workers.~~
   **Done (terminal).** See `tui.py`'s `CouncilTUI` and `python -m
   council_chamber.tui`. Still no file tree / code editor pane / windowed
   layout — a graphical or web frontend is a separate, larger step, not
   attempted here.
5. ~~Token/resource tracking per seat.~~ **Done.** See `usage.py` and
   `Council.usage_log`/`usage_for()` — real numbers when a
   `RemoteAPISeat` client reports them, `UsageReport.unavailable()`
   otherwise. Not yet persisted by `storage.py` (a session reload starts
   with an empty usage log) and local workers don't yet post usage into
   the log at all, since none of them do metered work today.
