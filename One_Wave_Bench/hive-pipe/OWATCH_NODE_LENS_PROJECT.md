# OWATCH NODE LENS — PROJECT GOAL

**Status:** Project definition / build target  
**Scope:** AI reference system, targeted editing system, connected folder logic web  
**Authority:** Must obey `GENERAL_REFERENCE_RULES.md`, `AI_CANONICAL_START_HERE.md`, and current repository metadata/governance rules.

## Main goal

Build OWATCH into a **layered, connected reference-and-editing system for AI**.

The system should let an AI work against a large One-Wave knowledge base without loading, rewriting, or duplicating everything at once. Folders become connected logic nodes. Each node exposes lightweight references and routing information on the outside while keeping most internal content compressed/inactive until the content is actually read.

The result should behave less like a pile of files and more like a **reference neural web**:

- small local nodes;
- explicit connections;
- remembered useful routes;
- bounded targeted edits;
- proposal branches rather than direct uncontrolled mutation;
- higher-authority review/merge;
- learned path preference without allowing path history to become truth.

## Core project law

**Content lives once in the canonical repository.**

OWATCH does not create a second canon.

Indexes, route weights, path memory, caches, extracted layers, compressed views, and edit proposals are navigation/runtime structures around the canonical source.

## 1. Layered content model

A watched document should be addressable from coarse to fine:

```text
folder
  -> file
    -> page / logical page
      -> section
        -> paragraph
          -> sentence
            -> word / exact span
```

The editor must descend only as far as necessary.

Examples:

- word change -> touch only the word/span;
- sentence correction -> touch only the sentence;
- paragraph rewrite -> touch only that paragraph;
- page-level restructuring -> touch only that page/logical page;
- file rewrite -> requires explicit file-level authority.

A narrow request must never silently widen into a broad rewrite.

## 2. Page model

Markdown and source files do not always have physical pages, so OWATCH needs a stable **logical page** concept.

Initial proposal:

- physical page when the source format has pages;
- otherwise a logical page is a bounded section/chunk with stable anchors;
- logical pages receive IDs derived from file identity + structural anchor, not merely current line number;
- line numbers remain supporting evidence but are not the sole identity.

This allows an AI to ask for:

```text
node -> file -> page 3 -> paragraph 2 -> sentence 1
```

without loading the whole file.

## 3. Cold / warm / active content state

Files and nodes should have three runtime states:

### COLD

Not currently being read.

- internal expanded representation is absent;
- only node envelope, references, hashes, routing metadata, and compressed index remain available;
- source file in Git remains canonical.

### WARM

Node has been selected as likely relevant.

- compact summary/index can be expanded;
- page/paragraph map can be read;
- full content still need not be loaded.

### ACTIVE

Specific content is currently being read or edited.

- only necessary layers are expanded;
- exact canonical text is read before proposing change;
- active edit scope is locked.

When the read/edit closes, derived expanded state may be compressed/discarded again.

**Important:** “zipped” means compressed runtime/index representation. Canonical source files should not be constantly rewritten into archive files just to simulate memory.

## 4. Folder node envelope

Each OWATCH folder becomes a graph node with a small outside-facing envelope.

Proposed envelope:

```json
{
  "node_id": "stable-folder-node-id",
  "canonical_path": "Nodes/Example",
  "role": "science | build | bridge | governance | book | mixed",
  "authority_refs": [],
  "outbound_refs": [],
  "inbound_refs": [],
  "concept_tags": [],
  "state": "cold | warm | active",
  "content_hash": "...",
  "route_memory": {},
  "hold": false
}
```

The envelope is for navigation and validation.

It is not a replacement for source content.

## 5. Connected logic web

OWATCH folders should connect through explicit typed edges.

Initial edge types:

- `AUTHORITY_OF`
- `REFERENCES`
- `DEPENDS_ON`
- `SUPPORTS`
- `CONTRADICTS`
- `VALIDATES`
- `IMPLEMENTS`
- `MEASURES`
- `DERIVES_FROM`
- `SUPERSEDES`
- `RELATED_TO`

An AI begins at the current reference node and traverses this graph rather than blindly searching the whole repository.

A reasoning/reference chain therefore becomes inspectable:

```text
question
  -> canonical entry node
  -> authority node
  -> relevant theory/proof node
  -> evidence/metadata node
  -> answer or edit target
```

## 6. Path hysteresis

Useful reference paths should retain memory.

The graph may increase a path score when a route repeatedly produces valid, useful, receipt-backed results.

It may decrease a path score when a route:

- reaches irrelevant content;
- produces HOLD;
- conflicts with authority;
- leads to failed validation;
- repeatedly expands too much irrelevant context.

This is **path hysteresis**, not truth weighting.

A high path score means:

> “This route has historically been useful for this kind of lookup.”

It must never mean:

> “This claim is more true because this route was used often.”

Canonical authority, metadata, evidence, and validation always outrank path score.

## 7. Differential route selection experiment

Explore a differential path system for AI lookup/decision support.

For each candidate next node, calculate separate positive and negative pressures.

Example conceptual form:

```text
positive =
    authority_match
  + semantic_relevance
  + dependency_match
  + prior_success_hysteresis
  + current_scope_match

negative =
    contradiction_risk
  + stale_reference_penalty
  + scope_escape
  + prior_hold_penalty
  + context_cost

lean = positive - negative
```

Then:

- strong positive lean -> traverse candidate;
- near-zero lean -> HOLD / compare alternatives;
- strong negative lean -> reject route;
- disagreement between top routes -> inspect both before action.

This should initially be treated as an **experimental routing heuristic**, not a scientific claim about cognition.

## 8. Proposal-only editing

Ordinary AI workers do not directly finalize edits.

Workflow:

```text
REFERENCE
  -> locate node
  -> descend to exact layer
  -> read canonical target
  -> PROPOSE EDIT
  -> create/update bounded task branch
  -> watcher verifies scope
  -> tests/reference checks
  -> higher authority reviews
  -> MERGE or HOLD
  -> refresh node/index/path memory
```

Proposals must record:

- reference node/path;
- exact target layer;
- old content hash;
- proposed content;
- intention;
- consequence;
- expected affected nodes;
- tests/checks;
- route used to reach the target.

## 9. Higher-authority merge model

Child watcher:

- watches local node;
- verifies exact edit scope;
- detects drift;
- refuses widened/unreferenced changes.

Goblin Folder Holder / higher watcher:

- sees proposals from child nodes;
- evaluates cross-node consequences;
- detects reference conflicts;
- validates branch scope;
- requires checks/receipts;
- is the normal authority allowed to commit/merge the accepted proposal.

Future authority layers may be nested:

```text
word/sentence worker
  -> file watcher
    -> folder watcher
      -> folder holder
        -> project foreman
          -> repository merge authority
```

Each higher layer sees a compressed receipt from lower layers rather than rereading everything by default.

## 10. Logic chaining

A folder node should be able to expose a compact “logic card”:

```text
WHAT I AM
WHAT I AUTHORIZE
WHAT I DEPEND ON
WHAT DEPENDS ON ME
WHAT I SUPPORT
WHAT I CONTRADICT
WHAT EVIDENCE I POINT TO
WHAT PATHS USUALLY REACH ME
WHAT CHANGED LAST
CURRENT HOLD / GATE / LIFECYCLE
```

Multiple logic cards chained together should form a reproducible AI lookup path.

## 11. Lens concept

The connected OWATCH graph may become a reusable **Lens**.

A Lens is a selected subgraph plus routing policy for a particular kind of work.

Examples:

- One-Wave Science Lens
- CELL_V1 Build Lens
- Cosmology Proof Lens
- Bridge/Terminal Lens
- Grant Evidence Lens
- Android Brain Lens

A Lens does not duplicate source content.

It says:

> start here, use these authorities, prefer these edges, expand these layers only when needed.

## 12. Project phases

### Phase 1 — structural addressing

Implement stable:

- file IDs;
- logical page IDs;
- paragraph IDs;
- sentence/span anchors;
- narrow edit target receipts.

**Pass:** a requested sentence can be located and proposed without rewriting the surrounding document.

### Phase 2 — node envelopes

Add:

- stable folder node IDs;
- external reference envelopes;
- inbound/outbound typed edges;
- cold/warm/active state.

**Pass:** an AI can inspect a folder's role/references without expanding its files.

### Phase 3 — proposal branch workflow

Add:

- proposal packets;
- branch creation/update;
- exact-scope diff validation;
- higher watcher approval/HOLD;
- accepted merge receipt.

**Pass:** child AI can propose but cannot self-finalize outside granted authority.

### Phase 4 — path memory

Add:

- route-use receipts;
- success/HOLD/failure signals;
- hysteresis score updates;
- score decay so old paths do not become permanent bias.

**Pass:** repeated useful paths become easier to retrieve while authority remains unchanged.

### Phase 5 — differential router

Implement experimental positive/negative route scoring.

**Pass:** routing choices are inspectable and reproducible from their component scores.

### Phase 6 — Lens API

Expose a bounded interface such as:

```text
lens.reference(query)
lens.route(query)
lens.open(node, layer)
lens.propose_edit(target, change)
lens.validate(proposal)
lens.commit(proposal)   # authority-gated
```

**Pass:** multiple AI clients can use the same Lens without creating their own copies or canon.

## 13. Non-goals

This project must not:

- replace Git as canonical history;
- let route popularity become truth;
- let an AI silently merge its own proposal by default;
- load the whole repository for every question;
- store full duplicate source trees in runtime state;
- use line number alone as durable identity;
- let generated summaries override exact canonical text;
- let compressed/zipped runtime state hide uncommitted edits.

## 14. First build target

The smallest useful vertical slice:

1. choose one OWATCH folder;
2. build its node envelope;
3. index one Markdown file into page -> paragraph -> sentence -> span layers;
4. keep only the envelope/index warm;
5. open one paragraph on demand;
6. propose a one-sentence change on a task branch;
7. child watcher proves only that sentence changed;
8. higher watcher either HOLDs or approves;
9. merge authority records the accepted change;
10. route memory records the successful reference path.

## 15. Experimental question

The first research question for the routing system:

**Can a differential + hysteretic graph router reduce irrelevant repository expansion while preserving or improving reference correctness?**

Compare:

- plain repository search;
- explicit graph traversal;
- graph traversal + hysteresis;
- graph traversal + differential scoring + hysteresis.

Measure:

- number of files opened;
- tokens/context loaded;
- correct authority hit rate;
- wrong-path/HOLD rate;
- edit scope accuracy;
- recovery after references change.

## 16. Project success condition

OWATCH Node Lens succeeds when an AI can enter the repository with a question or edit request and:

- reference the right canonical authority;
- traverse a small inspectable path through connected folder nodes;
- expand only the required content layers;
- make a precisely bounded proposal;
- be prevented from widening scope silently;
- send the proposal upward for independent merge authority;
- learn useful lookup pathways without confusing learned path preference with truth;
- close the content back to compact state;
- leave a reproducible reference/edit/merge receipt.

The target is a **living repository lens**: connected, layered, selective, reference-first, branch-gated, and capable of developing useful path memory while the canonical repository remains the single source of truth.
