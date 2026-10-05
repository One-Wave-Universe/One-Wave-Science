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

This is an executable isolated answer wrapper. The actual Nexus Reality Database, jobs, saved-run adapter and deployment have not been discovered or connected. Its UI reports that boundary. No schema migration, automatic source promotion, registered physics solver, second-client artifact handoff, unattended service installation or production deployment is claimed. These remain acceptance gates in [the canonical build specification](../REALITY_DATABASE_BUILDER_SPEC.md).

The app does not yet meet the complete database-builder specification. Semantic auditing can still miss unsupported interpretation; candidate labels and source links remain visible. It provides a working single-provider vertical slice rather than a claim of a finished truth engine.

## Verification

```bash
python3 -m unittest discover -s . -v
node --check app.js
```

Tests cover all twelve phase records, retained consequences, duplicate request IDs, checkpoint recovery, ambiguous-call HOLD, citation rejection, source/reference drift, publication races, journal isolation, denied path/tool access, old-database migration and live-worker exclusion. See `WORK_RECORD.md` for actual execution scope and earlier host receipts.
