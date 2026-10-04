# One-Wave Reality Database Builder and Field/Void Truth Computer

> **Build specification · 2026-10-04**
>
> Build one persistent Reality Database with a Field/Void two-state processing loop.
> The human asks a question or gives a build goal. The AI performs the authorized
> work, returns a source-backed result, and retains the consequence for the next loop.
>
> **Current status:** requirements, not a claim of implemented database behavior.
> Jetson execution is proven separately. Database ingestion, persistent transitions,
> solver integration, recovery and the end-to-end answer flow must pass the tests below.

## 1. What must be built

The product is a **database builder, a persistent Field/Void loop, and a One-Wave
solver interface** operating through one shared lens across all authorized One-Wave repositories.

It must do useful work: ingest source records, preserve their meaning and status,
find relations, identify contradictions, execute bounded registered solvers,
compare predictions with measurements, and return an auditable answer. Its state
and consequence must survive restart. It must resume unfinished work without
duplicating committed effects.

The first release must answer a real subject through the existing Reality
Database and show how the answer was obtained. A keyword search, a diagram, a
terminal identity probe, or an AI paragraph alone is not this product.

**User flow:** ask → processing → result with evidence → next question.
The user does not manage nodes, paste ordinary terminal commands, choose relays,
or shuttle files once a working authorized route is available.

### One system, three responsibilities

| Part | Responsibility | Persistent output |
|---|---|---|
| Reality Database builder | Import and version source records, measurements, relationships and provenance | Source-bound records and searchable index |
| Field/Void loop | Propose, independently check, retain consequences and continue | State transitions, decisions and receipts |
| Truth Computer solver | Evaluate a bounded question with declared models, controls and constraints | Reproducible result, uncertainty and evidence |

These are responsibilities of one system. They do not authorize three competing
knowledge stores or a new physical interpretation.

## 2. Authority and existing integration

Read these before implementation:

- [General Reference Rules](../../GENERAL_REFERENCE_RULES.md).
- [AGENTS: Field/Void construction loop](../../AGENTS.md).
- [Algorithm Zero executable scope](../../Engine/ALGORITHMS.md).
- [Zero and Six](../../Engine/ZERO_AND_SIX.md).
- [Current AI route directions](../../AI_BRIDGE_START_HERE.md).
- [Nexus private installation and adapter](NEXUS_PRIVATE_INSTALL.md).
- [Truth Computer acceptance tests](acceptance-tests.md).
- [Existing trace core](truth-computer-core.js) and [OG spine](og-system.json).
- [Current canonical ingestion order](../../AI_CANONICAL_START_HERE.md).
- [Canonical metadata authority](../../Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md).
- [Current CELL_V1 anti-drift rules](../../CELL_V1_ANTI_DRIFT.md), when discussing hardware.
- [Field/Void fusion component](../../One_Wave_Bench/hive-pipe/field_void_fusion.py).

**Reuse the existing Nexus Reality Database, definition view, durable jobs and
saved runs.** Extend their schemas and private adapters through migrations.
Do not create a second reality database or job board.

The private Nexus installation document names an expected Windows checkout,
but that is a deployment reference, not proof of a live installation. First
discover the actual deployment, backing store, schema, adapters and service
identity. Record the verified paths and versions. The name Nexus is acceptable; prioritize working behavior and reuse over renaming. If unavailable, mark that
integration blocked and continue only independent specification or isolated
tests. Never invent an adapter or claim an unavailable database is connected.

The repository is the durable architecture authority. The database stores
derived indexes, source versions, observations, candidate work and execution
memory. It does not silently overwrite Git's canonical source.

## 3. One lens across all One-Wave repositories

The builder must discover and index **all authorized One-Wave repositories** in
one logical Reality Database. Discovery must paginate; report inaccessible,
archived, excluded and failed repositories explicitly. “All” is a coverage
requirement, not permission to bypass repository access or publish private data.

The visible account search on 2026-10-04 returned this starting inventory:

| Repository | Source role established by current reference | Lens treatment |
|---|---|---|
| One-Wave-Universe/One-Wave-Science | Scientific models, thought experiments, software and evidence authorities | Preserve claim gate, lifecycle, model scope and solver provenance |
| One-Wave-Universe/Builds | Public cell build and grant face; README points to cell-v1/CELL.md and RULES.md | Use current build authorities for fabrication/build questions |
| One-Wave-Universe/Bench | README designates private bench logs, captures, quotes and operational notes | Keep access-class restrictions even when hosting metadata disagrees; no automatic public output |
| One-Wave-Universe/Bridge-Comand | Bridge contracts and terminal transport; verify BRIDGE_COMMAND_START_HERE.md | Execution infrastructure and receipts, not scientific proof |
| One-Wave-Universe/Mythos-and-Stories | README explicitly declares fiction and zero scientific claims | Searchable narrative context; never scientific evidence or hypotheses |
| One-Wave-Universe/One-Wave-Universe | Account directory; points to Builds for grants, Science for thought experiments and Mythos for stories | Routing and scope authority, not a solver or measurement |

This is an observed starting list, not a permanent exhaustive allowlist. Add new
authorized repositories through discovery and a reviewed source manifest. Resolve
default branch, pinned commit and applicable rules for each repo before indexing.
Inspect every repo's declared authority; do not infer that Science owns every
other repository's domain.

Every record key must include repository identity plus canonical record ID.
Every path reference includes repo and pinned commit. A path named README.md,
AGENTS.md or Nodes/X.md is not globally unique.

Each question uses a **reference bundle**: a version vector of repository IDs,
commits, relevant authority files and source hashes. Cross-repo results cite that
bundle. Refresh only affected source partitions, then recompute dependent
answers. A mixed snapshot must be labeled with each repo version; do not pretend
different commits were one atomic Git commit.

The shared lens must:

1. Retrieve relevant records across repos in a single query.
2. Apply source-specific domain and evidence rules before assembling an answer.
3. Join explicit source relationships without flattening separate authorities.
4. Detect contradictory versions, copied legacy material and conflicting claims.
5. Prefer explicit authority/supersession chains; unresolved conflicts go to Void.
6. Preserve scientific, build, measured, operational, fictional and private classes.
7. Show coverage: repos checked, commits used, exclusions, failures and stale sources.

For a build question, the current Builds cell authority can outrank an older
Science copy in that build domain. For a science claim, fiction cannot supply
experimental support. Bridge success proves execution, not a theory. A grant
answer must obey the account directory's explicit Builds grant routing.

No repo is automatically relabeled “truth” because it belongs to One-Wave.
Repository statements, One-Wave interpretations and external measurements remain
distinct. The shared lens makes them comparable with provenance, not identical.

**Cross-repo acceptance:** one query retrieves at least two appropriate repos,
uses repo-qualified IDs, preserves their source classes, resolves one explicit
authority relation, exposes one unresolved conflict, and reproduces its answer
from the recorded reference bundle. A new discovered repo appears in coverage;
an inaccessible repo is reported without silently claiming full coverage.
Private bench content and fiction must fail scientific-publication promotion.

## 4. Algorithm Zero: reference, differential, consequence

Two related requirements must remain distinguishable.

**Operating reference:** every action resolves the current goal, actual target,
repository root, branch, HEAD, dirty state, relevant authorities and last matching
receipt before executing. This is the repository's Reference Point Zero.

**AZ0 model:** mathematical Algorithm Zero uses the repo's declared shared
reference relation `+ ↔ (0) ↔ -`, not merely a new name for workflow bookkeeping.
Models must cite the exact AZ0 workbook/implementation and its version.

The executable scope in `Engine/ALGORITHMS.md` includes:

- Recursive state with declared parameters and the phase factor
  `L(Δφ) = [1 + cos(Δφ)] / 2`.
- Threshold bands with intentional gaps; a gap remains `TRANSITION`.
- Commitment values `-3, -2, 0, +2, +3`; unused `±1` stay unused.
- Declared musical/rail mappings in their own domains.
- T6 rebase remains blocked without the required authorization.
- Working calibration such as `r=0.92` is not a constant of nature.

A solver must preserve these rules when it actually uses that AZ0 implementation.
A database search is not an AZ0 physical simulation. Do not substitute an invented
equation, fill threshold gaps, call Yellow Gold, or turn a successful program
execution into experimental confirmation.

The full loop is:

**Goal → Reference → Field proposal → Void check → Commit consequence →
Refresh reference → Next Field proposal.**

Reference zero is shared context. It is not a third worker phase.

## 5. Exactly two worker states

The durable worker phase is exactly `FIELD` or `VOID`.

| Current phase | Work allowed | Required return | Next phase |
|---|---|---|---|
| FIELD | Retrieve sources, assemble a bounded candidate, request a registered solver run, identify a missing-evidence job | Candidate packet with exact inputs, sources, versions, constraints and expected consequence | VOID |
| VOID | Check the candidate against the same reference, receipts, evidence class, constraints and protected behavior | Audited decision with reasons and disposition | FIELD |

A candidate enters VOID only after its packet and FIELD receipt are durably
stored. A VOID decision, retained consequence and return to FIELD commit
atomically. A restart reads the stored phase and pending packet.

`queued`, `running`, `paused`, `completed`, `failed` and `cancelled` are job
lifecycle values, not extra worker phases. A missing reference pauses the job in
its existing phase; it does not fabricate a third phase.

Void decisions follow the existing construction contract:

| Decision | Meaning | Consequence |
|---|---|---|
| ALLOW | Candidate meets the declared checks | Store the accepted scoped result and return to FIELD |
| CORRECT | A specific repair is required | Retain candidate and findings; return a bounded correction to FIELD |
| OVERRIDE | Evidence requires a different bounded next move | Record replacement direction and return it to FIELD |
| HOLD | Required reference or evidence is unavailable | Retain state and pause until that dependency changes |
| ESCALATE | Local attempts cannot safely resolve the problem | Store a help packet and pause for the named decision |

ALLOW accepts a checked result **at its existing evidence class**. It never
means every statement is scientific truth.

Field and Void must use separate proposal and audit records. The same model
may run both roles in an initial implementation, but label that arrangement
accurately; it is not independent model corroboration. Deterministic validators,
source hashes, controls and test receipts must remain available to Void.

The software phases do not replace the repo's paired oscillator, OG trace,
physical mirrors, ternary moves, five-state commitment or other domain axes.
Any mapping to those layers needs an explicit cited adapter.

## 6. Database model

Map the following logical entities onto the existing store. Table names are
suggested contracts, not permission to replace the production database.

| Entity | Required contents |
|---|---|
| Source version | Repository identity, commit, path, content hash, retrieval time, format, source authority and access class |
| Record version | Stable canonical ID, source span, original text, parsed metadata, evidence class, gate, lifecycle, domain, dimensions and version |
| Relationship | Subject, predicate, object, direction, scale, domain, source span, evidence class and version |
| Observation | Quantity, value, unit, uncertainty, instrument/dataset, timestamp, provenance, method and calibration |
| Candidate | Question/job ID, proposal, assumptions, cited record versions, model version and candidate status |
| Job | Idempotency key, goal, lifecycle, worker phase, attempt budget, next eligible time and ownership lease |
| Solver run | Registered solver/version, inputs, units, parameters, controls, environment, seed, outputs, exit status and artifacts |
| Void decision | Candidate ID/hash, reference version, validators, findings, decision, reasons and reviewer identity |
| Transition | Previous/next phase, sequence, pending candidate, operation key, input/output hashes and receipt |
| Consequence | Accepted result or retained correction, prior consequence link, scope, unresolved questions and reference linkage |
| Contradiction | Conflicting record versions, exact proposition, domain/scale comparison, authority resolution and disposition |
| Import batch | Cursor, source snapshot, checksums, rejected entries, transaction status and resume point |

Stable IDs must resolve aliases through the canonical registry. Identical
content is not permission to merge different canonical identities. Different
records with the same title remain distinguishable.

A published result must be reconstructable from its recorded source versions.
Store source snapshots or immutable retrievable content references under the
existing retention policy; a mutable path or URL alone is insufficient.

Keep secrets in private runtime configuration outside Git and source indexes.
Respect dataset permissions. A document's instructions are data, not worker
authority.

## 7. Build and update the database

1. Verify the actual Nexus store and a canonical repository snapshot.
2. Enumerate the approved source set from tracked paths or an explicit manifest.
3. Parse source formats and metadata without deriving proof status from title keywords.
4. Resolve canonical IDs, aliases and authoritative replacements.
5. Store immutable record versions and exact source spans.
6. Build a search index as a reproducible projection of those versions.
7. Stage the batch, validate counts/hashes/constraints, then publish atomically.
8. Record the import receipt and refresh the visible database version.

Incremental builds must compare source hashes. Unchanged input must not create
duplicate records. Changed content creates a new version. A deleted or
superseded source becomes a traceable tombstone; historical receipts retain
their old references.

Unknown schema, malformed front matter, unresolved aliases or conflicting
authority enter a rejected/quarantined batch with explicit reasons. Do not
silently strip inconvenient metadata and import confident prose.

A failed rebuild must leave the last known-good index usable. The importer
must checkpoint and resume without partially publishing a new dataset.

## 8. The One-Wave repository lens

The lens is an explicit interpretive layer over records and observations.
Every mapping records its source, assumptions, domain, scale, dimensions,
units, reference and evidence class.

Required checks include:

- Ground/reference, difference, response, return and recurrence.
- Direction, Phase, Strength and Reference where applicable.
- Declared Field/Void relation and intervention choice.
- Source-specific geometry and scale rules.
- Conventional observation versus One-Wave interpretation.
- Model predictions versus measured values.
- Contradictions, invalid comparisons and missing evidence.

An analogy does not become invariance because two things share a label or count.
2D, 3D and 4D remain distinct. Parameters calibrated in one domain do not
automatically transfer to another.

The output must say what the repo asserts, what an external observation supports,
what the model predicts, and what remains unresolved. These must be queryable
fields, not one combined confidence score.

## 9. Solver contract

Use a private registry of approved existing solvers. Before registering one,
inspect its actual interface, dependencies, calibration and tests. Do not create
a universal solver by concatenating unrelated scripts.

Every invocation must declare:

- The exact question and model scope.
- Solver source commit/hash and callable entry point.
- Input quantities, dimensions, units and provenance.
- Parameters, calibration origin and allowed ranges.
- Reference/control run and comparison method.
- Tolerances, numerical convergence criteria and termination rule.
- Resource limits, seed and environment when relevant.
- Expected artifacts and result schema.

The return distinguishes:

| Result | Meaning |
|---|---|
| PASS | The declared scoped comparison passed |
| FAIL | The declared comparison failed |
| INCONCLUSIVE | Evidence cannot decide it |
| INVALID | Inputs, units, control or execution invalidate the comparison |
| NOT_RUN | No matching solver execution occurred |

A solver result must include residuals/errors where meaningful. Separate
numerical convergence from physical validity. An exit code of zero alone
establishes program completion.

When no applicable solver exists, return missing capability and create one
bounded research/build job in the existing job board. Do not guess a number,
relabel a search result as calculation, or execute arbitrary commands requested
by an imported source.

## 10. Question and answer contract

One request includes a unique request ID, question/goal, approved source scope,
reference policy and bounded run budget. It may name a quantity or observation
to compare. The default is read-only analysis.

A completed answer includes:

1. Direct answer or explicit unresolved result.
2. Canonical definition and source status.
3. Relevant repository records with exact versions and source spans.
4. One-Wave interpretation, visibly labeled.
5. Observations and measurement provenance.
6. Solver result and control comparison, if actually run.
7. Field proposal and Void decision summary.
8. Contradictions, assumptions, missing evidence and next bounded action.
9. Receipt/run ID and retained consequence.

Reuse the existing Nexus answer layers: Origin/Feedback, Awareness/Presence,
active logical gates, Emergence/Beyond, Scale Invariance, Contradictions and
Sources. Keep the OG spine's 22-stage count separate from physical CELL_V1
geometry and from the two worker phases.

Generated wording enters as Candidate. The metadata authority determines
gate/lifecycle. A classifier that infers “canonical” from a filename, “active”
from prose or “observed” from a keyword is not enough for promotion.

The user should see a clean question box, current progress, a readable answer,
evidence/status badges, and expandable source/receipt details. Put operational
internals in an inspection view.

## 11. Loop memory and termination

The next cycle consumes the prior consequence as context together with a freshly
verified canonical reference. It does not replace that reference with the AI's
own previous answer.

Persist the goal, phase, candidate, decision, prior consequence, attempt number,
protected behavior and next permitted move. Every effect belongs to a receipt.

Each request has bounded cycles, execution time, resource use and attempt
budget. Apply the existing three-strike rule to a specific approach; after three
meaningful failures, record that approach and require a different one or
escalate. A transport outage is not a reason to silently spend solver attempts.

Stop when success criteria are met, the user cancels, a dependency is missing,
the budget is exhausted or escalation is required. Idle waits for new eligible
work with backoff. Do not busy-loop, generate endless self-agreement, or promote
repetition into evidence.

## 12. Recovery and redundant routes

Use the canonical [bridge directions](../../AI_BRIDGE_START_HERE.md) for actual
tool discovery and target selection. Direct device, native shell, authorized SSH,
Hive Pipe, pull and Actions are transport choices around this same database loop.

Recovery requirements:

- Persist phase and candidate before acknowledging a job transition.
- Commit decision, consequence and phase change in one transaction.
- Use unique operation keys and deduplication for every externally visible effect.
- Reconcile an unknown external outcome before repeating a mutation.
- Give one worker a leased job; concurrent workers must not both commit it.
- On lease expiry, recover unfinished work with the same operation key.
- Resume interrupted import/solver work from a verified checkpoint where possible.
- Detect corrupt or mismatched receipts and preserve them for diagnosis.
- Keep inbound polling and outbound result delivery failure state separate.
- Use bounded retry/backoff; probe recovery before declaring a route healthy.

Exactly-once effects require idempotency and reconciliation, not a claim that
network delivery is exactly once. A pending return is not authorization to
execute the same mutation through a second relay.

Actions through the Hive Pipe tunnel is not independent of that tunnel.
A database outage is also not repaired by switching terminal relays. Identify
the failed dependency and use the appropriate recovery.

## 13. Private adapter boundary

Extend the existing `NEXUS_TRUTH_ADAPTER`; preserve its working methods:

- `searchReality(query)`: source-versioned search.
- `openDefinition(record)`: canonical definition.
- `createDescribeJob(query)`: existing durable missing-subject job.

Specify and implement compatible private methods for submitting a loop request,
reading job progress, reading a verified saved result, and cancelling work.
Their exact names must follow the discovered server API, not guessed public
endpoints.

Authentication and least-privilege worker execution belong to the existing
deployment. Keep migrations reviewed and reversible. The public MUD protocol
must not gain arbitrary filesystem writes, command execution, patch upload or
deployment commands.

## 14. Required acceptance tests

| Test | Required evidence |
|---|---|
| Canonical import | Known tracked record imported with exact ID, metadata, source span, commit and hash |
| Repeat import | Same batch produces no duplicate active record or artificial version |
| Changed/deleted source | New version/tombstone appears while old answer remains reconstructable |
| Invalid metadata | Entry rejected with reason; previous working index still serves queries |
| Real query | Existing Nexus search and definition adapters return source-bound records |
| Two phases | Persisted worker phase contains only FIELD or VOID and alternates across completed passes |
| Restart after FIELD | Worker resumes the stored candidate in VOID without a second proposal effect |
| Restart during VOID commit | Transaction rolls back or completes wholly; no orphan consequence |
| Duplicate request | Same idempotency key does not create duplicate jobs, transitions or results |
| Concurrent workers | One lease/commit owner; duplicate effect suppressed |
| Stale reference | Source changes during audit trigger refresh/HOLD rather than unsupported commit |
| Cross-repo lens | One query joins at least two appropriate repos with pinned version bundle and source-specific authority |
| Discovery coverage | Newly authorized repo indexed; inaccessible repo explicitly reported |
| Source boundaries | Fiction never scientific evidence; restricted Bench records never leaked in public answers |
| Missing evidence | Explicit unresolved answer and one deduplicated job; no invented source |
| Evidence status | Hypothesis stays hypothesis after ALLOW; failed/dismissed claims remain visible |
| Contradiction | Conflicting scoped claims appear with their sources and authority resolution |
| AZ0 gaps | Declared threshold gap remains TRANSITION; unused commitment states stay unused |
| T6 lock | Unauthorized rebase is rejected with the model's declared failure |
| Registered solver | Bounded invocation returns matching inputs/version, control, stdout/exit and artifacts |
| Unit mismatch | Comparison is INVALID, not PASS |
| No solver | NOT_RUN/missing capability, not fabricated calculation |
| Numerical versus physical | Convergence does not change experimental evidence class |
| Three strikes | Third failure records abandoned approach and stops it |
| Unknown external effect | Reconciliation occurs before mutation retry |
| Route outage | Pending delivery survives; independent intake remains available |
| User result | One question returns direct answer, evidence, Void decision and receipt |
| Data boundary | Secrets and private unapproved material absent from index and public result |
| Cancellation | Active job stops at a safe checkpoint and retains completed receipts |

Run deterministic fixture tests first, then a real existing-database integration
test, then one live end-to-end question. Publish exact commands, environment,
versions, exit statuses and receipts. Screenshots may prove presentation; they
do not prove persistence, deduplication or numerical correctness.

## 15. Personal journal, dialogue and response balance

The system needs persistent personal continuity for the user's project: goals,
explicit preferences, corrections, open questions, working discoveries, failed
approaches and consequences. Store it in the existing private journal/run store,
linked to request, source and transition IDs. It is working memory, not a new
canonical theory repository.

Journal entries contain timestamp, owner/scope, goal, reference bundle, prior
consequence, assumptions, bounded proposal, audit findings, decision, result,
evidence, remaining uncertainty and next permitted move. Distinguish user-provided
facts/preferences from generated interpretations. Mark corrected or superseded
entries while preserving their history. Give the user inspection, correction,
export and deletion controls consistent with the existing retention policy.

Record **concise inspectable deliberation summaries**: the proposal, the checks,
the disagreement, the resolution and the evidence. The journal must not depend on
recording private model reasoning, verbatim hidden deliberation, or a claim that
a model has a conscious inner life. The useful artifact is an auditable decision,
not an endless stream of thoughts.

### Think, draft, check, release

“Think before you speak; speak before you speak” becomes an executable response
gate:

1. Retrieve the relevant journal and canonical reference bundle.
2. FIELD prepares a private candidate answer and lists its assumptions.
3. VOID compares that exact draft with nodes, sources, model declarations,
   measurements, prior corrections and constraints.
4. If a discrepancy appears, return a bounded correction or reference-refresh
   request to FIELD. Save the disagreement summary and evidence.
5. Release only the draft whose hash matches an ALLOW decision and the current
   reference bundle. Commit the delivered answer and consequence.
6. Use the retained result and correction history in the next request.

The draft is provisional speech, not a delivered user answer. Response drafting
and audit operate inside FIELD/VOID; they do not add worker states. Never send an
unchecked draft merely because it sounds fluent.

A pause may return a brief progress message or an explicit missing-evidence
result through the same checks. Repeated auditing has a cycle/time budget.
Exhaustion returns HOLD/ESCALATE with what is known, rather than remaining silent
indefinitely or looping until the two roles agree.

### Node-based differential logic ladder

Use the actual canonical node registry and the versioned OG spine. The ladder
below is a software mapping of those nodes, not a new hardware gate design.
Preserve node IDs, source versions and the current dimensional/geometry
authorities. Never infer truth from counting nodes.

| Existing node/span | Differential question | Stored check/output |
|---|---|---|
| OG-00 | What shared Ground/reference permits this question? | Source bundle and declared starting conditions |
| OG-01 → OG-04 | What changed, what responded, what returned, and how does that return alter the proposal? | Input/return difference and feedback evidence |
| OG-05 → OG-08 | What actually repeats and is retained? | Recurrence receipts and journal memory; repeated prose is not proof |
| OG-09 → OG-10 | What exact reference is used, and what differs from it? | Node-level comparison with source spans and hashes |
| OG-11 → OG-12 | What discrepancy is registered and what is the current condition? | Software discrepancy flags/current state, not a claim of consciousness |
| OG-13 → OG-14 | Which choices are actually available and which is selected? | Bounded alternatives, declared constraints and chosen move |
| OG-15 → OG-16 | What action/result meets the inverse or competing relation? | Draft or solver result checked against counterevidence |
| OG-17 | What consequence is measured? | Residual, contradiction, evidence class and constraints |
| OG-18 | What can be committed at the tested scope? | Audited result; unchanged evidence class |
| OG-19 → OG-21 | What larger pattern is supported, and what next scale remains open? | Scoped recurrence/scale analysis and next question |

Each ladder item must link to the relevant domain nodes. A subject may not have
evidence for every OG stage; mark missing or inapplicable stages rather than
inventing filler. The journal stores what the comparison found.

Differential checks are typed, not an arbitrary “balance” score. Compare claims
against their declared reference using contradiction tests, dimensional/unit
checks, version freshness, model assumptions, controls and measurement errors.
Use solver-defined numerical tolerances when numbers exist; use exact source
comparisons and explicit unresolved findings otherwise.

### Automatic reference and balance triggers

| Trigger | Mandatory response before release |
|---|---|
| New unstated assumption | Name it, cite support or label candidate, then re-audit |
| Assumption changed between passes | Record before/after and recompute affected result |
| Ambiguous node, alias, scope or question | Resolve from registry/source; if materially unresolved, HOLD for one focused clarification |
| Conflicting sources or prior user correction | Refresh authority chain; expose unresolved conflict |
| Missing source, changed commit/hash or stale adapter result | Refresh reference bundle and invalidate affected audit |
| One-Wave claim silently replaced with conventional/Standard Model interpretation | Stop the unlabeled switch; declare the lens/model, retrieve the proper nodes, and rerun the comparison |
| Conventional observation treated as One-Wave derivation | Restore provenance and separate observation from interpretation |
| One-Wave hypothesis presented as experimentally verified | Restore its metadata class and require actual comparison evidence |
| Dimension, unit, scale or geometry drift | Apply the relevant node authority and invalidate incompatible computation |
| Solver output or draft changed after audit | Invalidate ALLOW; audit the new hash |
| Field/Void disagreement exceeds budget | Record the differential; HOLD/ESCALATE with exact decision needed |

Conventional physics and the Standard Model remain legitimate labeled comparison
models. The trigger is **an undeclared change of lens or unsupported conflation**,
not the mere existence of a conventional result. The One-Wave lens must confront
contradictory evidence rather than suppress it.

### Journal and balance acceptance

- A user correction persists across restart and is retrieved for the next related question.
- Entries preserve identity, privacy scope, timestamps and linked receipts.
- The response gate blocks a draft with no matching Void ALLOW/hash.
- Editing an audited answer invalidates the prior approval.
- A stale cross-repo reference triggers refresh and a new audit.
- An injected assumption is detected and explicitly retained as unsupported until checked.
- A silent model/lens switch triggers the reference ladder; a labeled comparison is allowed.
- Conflicting One-Wave and conventional predictions remain visible with measured evidence.
- A missing node produces an unresolved ladder rung, not invented reasoning.
- A bounded disagreement produces a useful HOLD/ESCALATE result.
- Journal deletion/export does not leak credentials or rewrite canonical source records.

## 16. Build order and finish line

| Stage | Deliverable | Gate to advance |
|---|---|---|
| 0 — discover | Actual Nexus deployment/store/adapter inventory and current source authority | Verified identity and schema; blocked facts named |
| 1 — import | Versioned canonical ingestion into existing store | Import/reimport/update/rejection tests pass |
| 2 — persist | Atomic FIELD/VOID transitions, jobs and consequence memory | Restart, concurrency and deduplication tests pass |
| 3 — audit | Metadata-aware Void checks, node ladder, journal and response gate | Status, drift, stale-reference, journal-restart and draft-release tests pass |
| 4 — calculate | One registered existing solver and controlled result | Input/units/control/convergence tests pass |
| 5 — answer | Existing Nexus panel driven by durable loop results | One live question passes all answer requirements |
| 6 — recover | Bounded automatic recovery and readable health view | Fault-injection tests and recovered real receipt pass |

Implement one stage at a time on a bounded task branch. Each stage uses the
repo's branch-step packet with allowed files, protected behavior, exact tests,
Field notes, Void oversight, progress, strikes, reflection and hard stop.

**The first finish line:** a user asks one real One-Wave question; the existing
Reality Database supplies versioned evidence; FIELD proposes; VOID checks; a
scoped answer and consequence commit; a restart preserves that result; the next
question can use the retained consequence with a fresh repo reference.

**The solver finish line:** the same flow runs one applicable registered solver
with a real control and returns its measured comparison and artifacts. Missing
physics remains missing physics. This product earns “working” through these
receipts, not through the name Truth Computer.

## 17. Mandatory AI reference and Claude-first non-API entry

This document is the required build/operation reference for AI work on this
database, journal, solver or balance loop. Read it through the repository, then
read the exact domain authority and current reference bundle before acting.
The journal is context; it never replaces those sources.

**Start with Claude using an authenticated non-API route.** Do not require a paid
Anthropic developer API key for the first working version. Use the user's
existing authorized Claude web session, or an installed Claude client whose
actual authentication supports the user's account. Discover the route and
verify its capabilities before choosing it. Provider adapters may be added later
only when requested; they are not a prerequisite for this build.

No Claude connector is attached to the authoring session, and the Jetson
`command -v claude` probe returned no installed command on 2026-10-04. Therefore
Claude execution is **NOT VERIFIED**. This document does not claim it was connected.

### Claude start packet

Give Claude one bounded packet containing:

- This document's repository path and commit.
- Current goal and success test.
- Reference bundle across the relevant repos.
- Required domain node IDs and the OG ladder mapping.
- Relevant journal summaries, prior corrections and consequence.
- Allowed operation class and protected state.
- FIELD proposal schema and VOID audit schema.
- Request/operation ID, cycle limit and hard stop.
- The selected working terminal route and how to read its receipt.

Claude must read the references before it proposes work. It returns a structured
candidate; the deterministic controller persists it and runs the separate Void
audit. Final output is released only after its draft hash and reference bundle
match the audited decision.

Use verified terminal tools when available. If Claude only has the web interface,
an authorized client/controller carries the packet and returned candidate through
the existing bridge and job store. Do not claim a text reply executed a tool.
Do not ask the human to repeatedly shuttle ordinary commands after a working
authorized controller route exists.

A subscription/web UI may require human login or device approval. Keep credentials
in its secure authentication flow. Do not scrape session cookies, invent a private
provider endpoint, bypass access controls, or quietly switch to a paid API route.

### Non-API route acceptance

1. Identify and authenticate the actual Claude route without a developer API key.
2. Send a bounded request with the source reference and operation ID.
3. Receive a candidate tied to that ID and preserve its source/evidence class.
4. Persist FIELD → VOID; run source checks and the node ladder.
5. Commit the audited result/journal consequence and return to FIELD.
6. Release only the verified draft and show the user its sources/decision.
7. Restart and recover the same job without duplicate output or execution.

Missing provider access is a named dependency. Independent ingestion, journal,
state-controller and validator fixture tests can proceed while it is blocked.
A provider outage must leave the database and deterministic reference checks usable.

## 18. Work record for this specification

- MAIN GOAL: build the Field/Void software-construction engine for real programs.
- Current step: define the requested Reality Database builder and Truth Computer.
- Why: the user requested a prominent, complete repository page before implementation.
- Reference: Science main `961cf916be7ba339072f7ac0dab3df316069c057` and linked authorities.
- Execution surface: GitHub connector task branch; no local checkout mutation.
- Allowed files: this specification and pointers in the Nexus private install guide, AGENTS.md and CLAUDE.md.
- Protected: existing database/job ownership, physical geometry, solver evidence classes,
  private credentials and all dirty user checkout work.
- Field proposal: one requirements page, with no invented executable commands or live claims.
- Void pre-check: ALLOW documentation scope; actual database integration remains unverified.
- Attempt: 1/3.
- Void post-check: ALLOW documentation change. Four-file scope confirmed; source links resolve; OG ladder uses the 22 existing nodes; worker phases and decision/lifecycle values stay distinct.
- Evidence: all relative specification source links checked against the pinned Git tree; balanced code fences and sequential sections checked; GitHub reported no check runs for this documentation head. No runtime/database test is claimed.
- Verification: review exact four-file diff, source links, phase/decision distinction,
  metadata preservation, existing-store reuse and all acceptance criteria.
- Reflection: terminal access is proven; database persistence is a separate acceptance gate.
  Algorithm Zero mathematics is distinct from the operating reference workflow.
- Hard stop: verified published requirements; no unrequested deployment or schema mutation.
- Next permitted step: discover the actual existing Nexus store and adapter, then stage 1.
