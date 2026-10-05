# One-Wave reference apps

**AI builders: start with [the interface implementation guide](INTERFACE_BUILD_GUIDE.md).** Build the specified screens, interactions and persisted behavior; a list of Field/Void steps is not the product.

The target is a clean One-Wave search-and-answer workspace for one identified AI: readable checked answers, exact source inspection, connected follow-ups, a personal journal, bounded correction dialogue, truthful connection/coverage views and restart continuity. The guide specifies layout, visual tokens, components, data contracts and complete user journeys. This README owns launch instructions for the current preview, which implements only part of that target.

## Start

Python 3 standard library on a POSIX host (Linux/macOS); no package installation. The worker lock uses `fcntl.flock`. Run from this directory on the verified host with a local SQLite state file, not a network filesystem. Use existing authorized Git roots; do not move or reset their working trees.

Claude on the laptop uses the already authenticated Claude Code subscription:

```bash
python3 app.py --agent claude --repo /home/scales/.local/share/one-wave-live-executor --port 8765
```

Open `http://127.0.0.1:8765` in that laptop's normal browser. The supplied root is an observed existing runtime checkout, not a claim that its HEAD is current main. The app records its actual HEAD and excludes dirty content.

DeepSeek on the Jetson uses the existing local web relay, not a developer API key:

```bash
python3 app.py --agent deepseek --discover-repos \
  --repo /home/Scales/One-Wave-Science \
  --repo /home/Scales/Builds \
  --repo /home/Scales/Bridge-Comand \
  --repo /home/Scales/Mythos-and-Stories --port 8766
```

Open `http://127.0.0.1:8766` **on the Jetson**, or use an existing authorized SSH forward. This address is not a public phone link. The app does not expose its listener publicly. `--relay` accepts existing loopback services on ports 3000 or 3001. If the existing relay requires its local authentication key, set `DEEPSEEK_WEB_API_KEY_FILE` to that private file; never copy its value into Git or chat.

`--discover-repos` uses the host's existing authenticated `gh` CLI, paginates the actual One-Wave account, resolves missing repositories through pinned GitHub reads, and preserves local-root versions as a visibly mixed snapshot. A failed discovery holds the dependent question rather than claiming full coverage. Without discovery, coverage is configured roots only. Bench is excluded because its declared policy is private even though hosting metadata says public. Fiction is tagged and blocked from scientific answers. A narrative-specific adapter is still required for narrative answers.

## DeepSeek reference and metadata tools

| Tool | Returned evidence |
|---|---|
| `reference_manifest` | Repository IDs, commits, branches, dirty state, domain, exclusions and coverage limits |
| `source_manifest` | Paginated tracked paths for a pinned repository; next offset and total |
| `source_search` | Cross-repo excerpts, source spans, exact content hashes, raw declared front matter, domain and source class |
| `source_read` | Bounded tracked Markdown/JSON/Python/JavaScript reads at the pinned commit |
| `node_spine` | The existing OG reference file; subsequent spans available through source reads |

Tools execute outside model prose. Unknown tools, arbitrary paths, unconfigured repositories, private Bench content and arbitrary terminal commands are denied. DeepSeek can inspect canonical registries and metadata-pipeline source through the pinned source tools. Raw metadata is preserved; this app does not claim it has resolved every alias or authority conflict. Search examines up to 80 matched documents per repo and supplies ten excerpts; the paginated manifest/read tools expose additional tracked sources without pretending the entire account fits in one prompt.

Terminal and code work remain on the existing [bridge routes](../../../AI_BRIDGE_START_HERE.md). This answer app grants no new arbitrary-execution interface. The existing DeepSeek worker and Hive Pipe parser remain responsible for terminal authorization. Solver status is explicitly `NOT_RUN`.

## Enforced loop and memory

Exactly two worker phases, FIELD and VOID, plus six separate cursors: BEGIN, BUILD, HOLD, BUILD, BREAK, LOOP. Each cursor stores a Field artifact and matching Void decision. Fresh references gate advancement. The final output requires matching citations, an ALLOW audit, an exact candidate hash and an unchanged reference. The audit is a separate pass by the same provider, not independent model corroboration or physical verification. Generated results remain candidates.

SQLite stores **per-app runtime conversations, transitions, structured provider returns, corrections and concise journal summaries only**. It is not a second knowledge database or job board. Claude and DeepSeek default to separate files under `~/.local/state/one-wave-answer/`. Same request IDs return the existing record. No hidden chain-of-thought is requested or stored. Missing evidence remains a recorded dependency. Corrections persist and are contextual data, not authority to change evidence.

### Retained checkpoints and explicit recovery

The existing state database is upgraded additively with row versions. Each provider operation retains its stable operation ID, exact structured request/return, input/output hashes, provider identity and timestamps. Candidate and audit checkpoints stay private to the controller; normal history and conversation responses expose only the released answer and safe progress.

An interrupted worker becomes HOLD. A configured local client may explicitly submit the same-origin JSON request `POST /api/resume` with `{"id":"the existing request ID"}`. There is no new browser control in this backend slice. A checkpoint with completed provider returns can resume those saved returns, refresh its reference, finish remaining checks and retain one published consequence. A still-in-flight operation has an unknown outcome and cannot be automatically reissued. A new provider call may occur only for a step that has never been dispatched. Provider identity, source/reference hashes and retained artifacts must still match; otherwise recovery stays on HOLD.

Reference checks run at every phase boundary and before provider dispatch and acceptance. Tracked dirty changes are fingerprinted in addition to the pinned source content. Untracked files remain excluded from source evidence. A process-scoped lock prevents a second app from pausing or duplicating a live worker; row-version checks reject stale writes. Publication binds candidate, audit, reference and stable delivery receipt in one SQLite transaction, with reference checks inside that transaction. This does not lock external Git writers or claim a distributed transaction across Git and SQLite. Completed historical results retain their original reference rather than being silently revalidated.

Recovery tests use deterministic provider fixtures and one deliberately killed local test process. They prove controller behavior, not authenticated Claude/DeepSeek availability, live provider exactly-once execution, deployment or Nexus integration. An adapter call whose return was lost remains ambiguous even if the provider actually completed it.

## Integration boundary and remaining work

The user clarified that no Nexus database exists. The source-qualification core below builds the first explicitly selected shared knowledge store; it does not wait for an existing Nexus database. The answer wrapper and its per-app journals remain separate. No automatic truth promotion, registered physics solver, live model-driven knowledge construction, second-client artifact handoff, unattended service installation or production deployment is claimed. These remain acceptance gates in [the canonical build specification](../REALITY_DATABASE_BUILDER_SPEC.md).

The app does not yet meet the complete database-builder specification. Semantic auditing can still miss unsupported interpretation; candidate labels and source links remain visible. It provides a working single-provider vertical slice rather than a claim of a finished truth engine.

## Verification

```bash
python3 -m unittest discover -s . -v
node --check app.js
```

Tests cover all twelve phase records, retained consequences, duplicate request IDs, checkpoint recovery, ambiguous-call HOLD, citation rejection, source/reference drift, publication races, journal isolation, denied path/tool access, old-database migration and live-worker exclusion. See `WORK_RECORD.md` for actual execution scope and earlier host receipts.


## First shared knowledge store

`knowledge_loop.py` is a runnable CPU reference/differential projection of the current M4 architecture. M4 assembles the goal, current canonical authorities, pinned source, prior accepted record and pending findings into the active world used by both sides. It routes accepted consequence back into the next cycle's memory. It is not a third worker state or a claim about associative neural inference, consciousness, physical simultaneity, or numerical AZ0 dynamics.

The two durable worker phases are exactly `FIELD` and `VOID`; the separately constrained cursor has `BEGIN / BUILD / HOLD / BUILD / BREAK / LOOP`. Each cursor requires a retained Field artifact and specific Void check. `running / paused / completed` are job lifecycle values. `ALLOW / CORRECT / HOLD / ESCALATE` are decisions. None adds a worker phase. Four Views remain Direction/Phase/Strength/Reference; Actions remain Inward/Outward/Across/Over. This source-record slice does not simulate their hardware realization.

| Cursor | FIELD artifact | VOID acceptance check |
|---|---|---|
| 0 BEGIN | Current active world, source/authority versions and previous consequence | Identity, hash and current-reference equality |
| 1 BUILD | One bounded append-source-record proposal | Exact quote/span/version/metadata/evidence class; explicit source-fidelity-only permission |
| 2 HOLD | Candidate readiness and authorization hash | Matching prior authorization plus fresh reference |
| 3 BUILD | Staged candidate record | Matching readiness and unchanged authorized candidate; no knowledge publication yet |
| 4 BREAK | Candidate/return differential | Deterministic source comparison and retained evidence; no confidence-based promotion |
| 5 LOOP | Retained-consequence packet | Exact audit/candidate/reference binding; append immutable record version, consequence and next FIELD/BEGIN checkpoint in one transaction |

The executable transition table is `knowledge_loop.TRANSITIONS`. FIELD proposal hands to VOID atomically with its artifact. Void CORRECT retains the rejected artifact and an exact source-bound counterproposal, returning to FIELD at the same proposal cursor. A distinct repair attempt must pass authorization again. Three failed attempts ESCALATE. Missing/stale evidence HOLDs at the actual phase/cursor; repeated calls do not consume more attempts or fabricate a result. Start a new immutable goal revision after changed canonical sources. This bounded core has no external model-call ambiguity; the answer wrapper's provider-return recovery remains separate.

### Explicit single-store identity

Choose one shared knowledge path and stable store ID for all wrappers. Both are required; there is no per-agent knowledge default. Store identity, schema version and resolved location are checked before mutation. An app already bound to another path/identity refuses rebinding. An unrelated existing SQLite file is rejected without modifying it. Jobs, Field artifacts, Void audits, source versions, record versions, transitions and accepted consequences live in this one store. Authoritative artifact/audit/source/record/history tables are append-only; changed source commits append versions and retain their predecessor.

Per-provider runtime journals remain separate. Their only shared-store write is configuration binding; accepted knowledge and its checkpoint commit together in the shared store. No transaction across those databases is claimed. After a lost HTTP response or process exit, the stable job ID retrieves the committed consequence directly from the shared store. Reusing an ID with a changed goal or input is rejected.

### Run one source cycle and continue after restart

Use an authorized existing checkout and explicit local POSIX paths. The first slice accepts tracked public Science Markdown spans of 1–60 lines. It reads the mandatory authority paths declared in `AUTHORITIES`; missing authority or source content causes HOLD. No model or solver is invoked.

```bash
python3 knowledge_loop.py --repo /verified/One-Wave-Science   --runtime-state /approved/runtime/claude.sqlite   --knowledge-store /approved/shared/reality.sqlite --store-id one-wave-reality   --id source-first --path Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md   --start-line 1 --end-line 10 --goal 'Retain the current routing source and its declared status'
```

Rerun without `--path` and with the same ID after restart to reconcile/resume retained work. For a new cue, use another ID and the same store path/identity. The second cycle records its prior accepted record; unchanged source versions are reused without duplicate records. JSON output includes the exact phase transitions, audits and accepted receipt. Only a completed receipt may identify a published record.

For the existing local server, add `--knowledge-store PATH --knowledge-store-id ID`. The same-origin JSON endpoint `POST /api/knowledge/build` accepts exactly `{id, request}`, where request has goal, repo, path, start_line and end_line. Read `/api/knowledge/job/ID` for checked trace and `/api/knowledge/record/HASH` for a committed record. Reads before the first build do not create the store. There is no new frontend control in this slice.

### What the first record proves

A record contains repository/path/commit, whole-source content hash, exact source span, declared metadata/gate/lifecycle, evidence class, qualification and uncertainty. `qualification=exact-source-span` and `evidence_class=repository-statement` never mean experimental truth: `proposition_status=NOT_VALIDATED` stays explicit. A wrong quote is challenged/corrected; source status is never changed to make a proposal pass. The Bench and Mythos-and-Stories repositories, arbitrary file paths and untracked content are outside this first builder scope. This is a repository-scope restriction, not a semantic fiction classifier for every document inside Science.

Tests cover non-empty first commit, challenge/correction, preserved failed attempts, restart at every FIELD/VOID cursor, final-transaction fault injection, real process exit/lost handoff, immutable version history, reference drift, same/different-job concurrency, identity/schema mismatch and safe HTTP readback. Fixture execution is not live AI corroboration. Solver integration, general semantic proposition validation and live-provider orchestration are later acceptance gates.
