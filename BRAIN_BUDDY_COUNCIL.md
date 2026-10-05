# Brain Buddy Council

## Identity — do not reinterpret

Brain Buddy is the three-AI loop:

```text
Mark = human operator
ChatGPT = origin / return AI
Gemini = peer AI
DeepSeek = peer AI

ChatGPT -> Council -> Gemini <-> DeepSeek -> ChatGPT
```

The Council script orchestrates Gemini and DeepSeek because ChatGPT is the originating/returning AI outside the local worker process. Do not miscount Mark as an AI and do not misdescribe the Python process as the whole three-AI system.

Canonical implementation is `scripts/brain_buddy_council.py`. The Gemini and DeepSeek wrappers are transports/workers, not competing Brain Buddy versions.

## Modes

### Gemini only

```bash
bash scripts/brain_buddy_council.sh gemini "question"
```

### DeepSeek only

```bash
bash scripts/brain_buddy_council.sh deepseek "question"
```

### Both independently

Runs Gemini and DeepSeek in parallel against the same bounded question.

```bash
bash scripts/brain_buddy_council.sh both "question"
```

Use this when you want two independent reviews before either sees the other answer.

### Gemini then DeepSeek

Gemini answers first. DeepSeek then receives the original question plus Gemini's answer and is instructed to check it against the repo, call out disagreements, and give its own answer.

```bash
bash scripts/brain_buddy_council.sh gemini-deepseek "question"
```

### DeepSeek then Gemini

```bash
bash scripts/brain_buddy_council.sh deepseek-gemini "question"
```

Same handoff in the opposite direction.

### Three-way open discussion

Participants:

- user;
- Gemini;
- DeepSeek.

```bash
bash scripts/brain_buddy_council.sh discussion "question" --rounds 3
```

When run in an interactive terminal, after each Gemini + DeepSeek round the user can:

- type a reply or redirection;
- press Enter and let them continue;
- type `/stop` to end the discussion.

Each model sees the previous discussion turns on its next turn.

The peers are not forced to agree. They are explicitly allowed to preserve disagreements and identify the next test needed to resolve them.

## Interactive menu

Running without arguments opens the menu:

```bash
bash scripts/brain_buddy_council.sh
```

The menu offers:

1. Gemini only
2. DeepSeek only
3. both independently
4. Gemini then DeepSeek
5. DeepSeek then Gemini
6. open three-way discussion

## Reference contract

Every Council task carries the common reference contract:

```text
GENERAL_REFERENCE_RULES.md
    ↓
AI_CANONICAL_START_HERE.md
    ↓
I-06 metadata authority
    ↓
task-specific files
    ↓
worker answer
    ↓
validate
    ↓
return to reference
```

DeepSeek still uses its free web relay + Hive Pipe.

Gemini uses the existing free-web relay through `gemini_web_bridge.py`.

Council itself does not create another repository checkout, source canon, or model credential store.

## Discussion behavior

The discussion transcript is deliberately cumulative.

A worker receives:

- the original user question;
- canonical reference rules;
- prior user turns;
- prior Gemini turns;
- prior DeepSeek turns.

Each new worker turn is asked to address the peer's strongest point rather than merely restating its own answer.

Useful turn endings are:

```text
AGREEMENT: ...
DISAGREEMENT: ...
OPEN QUESTION: ...
```

This makes unresolved claims visible instead of hiding them inside a blended answer.

## Save a discussion receipt

By default Council prints responses but does not create a persistent transcript.

To deliberately save a receipt:

```bash
bash scripts/brain_buddy_council.sh discussion "question" --rounds 2 --save
```

The receipt is written under:

```text
External_Work/brain_buddy/outbox/
```

This is runtime/output evidence, not a second canonical source.

## Examples

Two independent science reviews:

```bash
bash scripts/brain_buddy_council.sh both \
  "Compare the falsifiability of Nodes/E-533_Superfluid_Transport_Time_Dilation.md and Nodes/C-309_Friction_Limit.md."
```

DeepSeek proposes, Gemini checks:

```bash
bash scripts/brain_buddy_council.sh deepseek-gemini \
  "What is the smallest mathematical attack on the time-dilation transport hypothesis?"
```

Open discussion:

```bash
bash scripts/brain_buddy_council.sh discussion \
  "Can the current One-Wave time-dilation transport claim be made quantitatively falsifiable without new experimental data?" \
  --rounds 3
```

## Hard boundaries

Council must not:

- treat either model as canonical authority;
- call agreement proof;
- hide disagreement by averaging answers;
- let one model's answer silently become the other model's reference source;
- bypass the repo-first reference contract;
- merge model edits automatically;
- expose credentials;
- fabricate receipts.

The user remains the controlling participant. The repository remains the reference authority.

## Return safety and automatic reference

Before each worker, Council reads and hashes the canonical entry, this contract,
and the three root reference authorities from the actual checkout. It records
repository, branch, HEAD and tracked working-state hashes, supplies that reference
to the worker, then checks it again on return. A changed reference invalidates the
return for acceptance (`RE_REFERENCE`); it does not erase the answer. This checks
the local checkout, not current remote HEAD or a remote worker's checkout. Those
must be independently verified by the worker before using its tools.

Current transports are `gemini_web_bridge.py` and `deepseek_web_bridge.py`.
This does not switch routes or establish that either free-web relay is currently connected.

One request ID links all turns; `--request-id` can preserve the origin AI's ID.
`--save` writes a unique Markdown transcript and adjacent JSON receipt under the
existing outbox. Receipts include per-turn identity, local source hashes, elapsed
transport time, status and answer hash. The current bridges return plain text, so
provider response IDs are explicitly unavailable: local correlation is not a
provider-signed receipt.

Empty output, error/HOLD text, nonzero exit, missing references and timeouts are
not successful answers. Failed peers are skipped for the rest of that discussion;
the other peer remains usable. `PARTIAL` and `HOLD` return exit 2. `RETURNED` means
nonempty local transport returns, not agreement, grounded correctness or physics
proof. `/stop` prevents subsequent rounds. Round and transport limits remain
resource bounds and never create consensus.

Offline verification: `python3 -m unittest discover -s scripts/tests -p
 'test_brain_buddy_council.py' -v`. This suite mocks providers and is not live
Council activation evidence.

## Optional nested six-step loop

`discussion --loop` uses the same canonical Council and the same Gemini/DeepSeek
transports. Existing modes and ordinary discussion are unchanged. The loop is a
software workflow, not an implementation or validation of physical CELL gates.

Example: `bash scripts/brain_buddy_council.sh discussion "question" --loop --save`

The six public artifact/check positions are Reference, Choice, Move,
View/Action, State/Scale and Reentry. Each position contains a FIELD proposal
(Gemini) and VOID check (DeepSeek); these are two worker phases with a separate
six-step cursor, not twelve states. Move prepares a read-only draft. Council
workers gain no repository mutation permission.

VOID must acknowledge the exact FIELD artifact hash before advancement. Both
peers' final objections remain blocking. An agreed next action is distinct from
an agreed resolution; neither validates scientific claims. Plain prose, missing
IDs, unseen reference citations and mismatched hashes cannot advance this loop.
Structured replies are required only for the opt-in loop.

A bounded missing-evidence question can open a child loop. Its receipt records
parent ID, parent step, depth, reference ID, parent-goal hash and result hash.
The child returns before the parent retries that same step. Changed references
or user redirection invalidate dependent child context, while historical receipts
remain inspectable. Failed children never silently advance their parent.

Confusion or a worker's `reference_required` triggers a fresh local read. Exact
`reference_requests` read additional tracked task files and their full metadata.
Unsafe paths, missing or untracked files, symlinks and oversized reference packs
HOLD rather than being silently guessed or truncated. Default bounds are 32 files,
64 KB per file and 256 KB total. No automatic fetch, checkout switch, new database
or alternate source of truth is created.

Time is carried as elapsed duration, remaining resource budget and age of prior
returns tied to source identity. Current-source material is distinguished from
historical context. This is a software attention/freshness policy, not a numerical
truth score, decay law, physical model or timer-driven consensus.

The shared defaults are 36 provider calls, depth 2 and 1200 seconds; callers can
set `--max-calls`, `--max-depth` and `--budget-seconds`. Every child, retry and
re-reference uses those same bounds. Time exhausted during source reads or a
provider return means `BUDGET_EXHAUSTED`, never agreement. Three rejected attempts
at one step escalate. `/stop` and interrupted workers prevent subsequent calls.
Results appear as they return, before a top-level user redirection prompt.

The outbox receipt preserves the trace; it is not a resumable Nexus job and does
not claim database integration. Live structured Gemini/DeepSeek returns must
still be proven before promoting this optional path as activated. Offline fixtures
are deliberately labeled tests and never stand in for real provider replies.
