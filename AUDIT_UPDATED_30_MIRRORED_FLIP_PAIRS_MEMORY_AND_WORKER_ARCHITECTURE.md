# Updated 30 — Mirrored Flip Pairs, Memory Rebuild, Worker Architecture, and Animator State

Date: 2026-08-30

Status: **working structural architecture / convergence update — not proof.**

Nothing in this update is being entered as proof of the larger theory. Its importance is structural: several previously separate ideas now fit together more coherently, reduce ambiguity between jobs, and make the next build steps easier to identify. Preserve all of it as working structure to test, refine, connect, or reject through implementation.

## 1. Six apparent positions are three mirrored flip-pairs

Do not model the binary / ternary / quadratic sequence as six independent flips.

The current control-loop interpretation is three mirrored transition pairs across the view/action mirror:

- binary view-side position <-> binary action-side position
- ternary view-side position <-> ternary action-side position
- quadratic view-side position <-> quadratic action-side position

The apparent six positions are therefore three paired transitions seen from two mirrored directions.

A flip is one paired transition across the mirror, not two unrelated events. Do not duplicate the flip count by treating the view and action faces as independent flips.

### Functional direction

Current structural description:

`binary -> ternary -> quadratic` = oversight / view side

`quadratic -> ternary -> binary` = action / execution side

Treat this as a working control-architecture relationship to encode and test.

### Temporal receipt

Preserve the stated timing relationship as part of the working structure:

- old view travels upward
- new view travels upward
- old action travels downward

The point is that the mirrored transition carries state history through the flip instead of replacing everything at once. The exact timing and implementation still have to be built and tested, but the relationship must not be silently flattened into six stateless steps.

## 2. Fast loop and slower oversight / override

Keep the established timing discipline:

`flip, flip, oversight; flip, flip, override`

This expresses a 3:1 local nerve-to-supervisory event relationship and a 6:1 full oversight/override rhythm when the two supervisory events are taken together.

The fast subconscious / nerve loop is intentionally ahead of slower cognition. Local body-protection responses can occur before the higher layer finishes interpreting them.

The higher layer should receive compressed, routed, referenced information rather than raw uncontrolled traffic.

Structurally this now supplies the timing relationship between the fast lower layer and the slower supervisory layer.

## 3. New code-construction organization by job and scale

Today’s proposed programming organization is:

`Cells -> Nerves -> M4 -> Dream -> Administrator -> Executor`

The intention is to stop building one giant worker that parses, reacts, plans, evaluates, routes, and executes everything.

### Cells

Tiny deterministic primitives.

Examples:

- parse one structure
- validate one value
- calculate one quantity
- detect one local pattern
- convert one representation

Cells should be small enough to test independently and compose without hidden state.

### Nerves

Fast event handlers and immediate local reactions.

Examples:

- button / sensor / file / frame events
- collision or curb-drop reaction
- quick local threshold checks
- actuator braking before higher cognition notices

Nerves should not become planners. They react inside bounded local rules.

### M4

Router / timing / synchronization layer.

Jobs:

- route information upward and commands downward
- sequence operations
- synchronize subsystems
- select local state / scale context
- preserve timing receipts
- compress fast activity into information the slower layers actually need

M4 is not the same job as Dream or Administrator.

### Dream

Generator / planner.

Jobs:

- produce candidate plans
- propose edits
- generate alternative actions
- generate assets or motion ideas where appropriate
- explore possibilities without treating proposals as approved truth

### Administrator

Evaluator / supervisor.

Jobs:

- compare proposals against current state and constraints
- check continuity
- approve, reject, hold, or select
- provide oversight / override

Administrator evaluates; it should not swallow every primitive job below it.

### Executor

Actual committed action.

Executor receives an approved action and carries it out. It should not independently reinterpret the entire problem unless a failure receipt forces re-evaluation.

### Why this matters structurally

This worker chain gives the mirrored timing model somewhere concrete to live:

- Cells and Nerves supply fast local state changes.
- M4 preserves order, timing, routing, and compression.
- Dream creates candidate future states.
- Administrator provides the slower view / oversight decision.
- Executor produces the descending committed action.

This does not establish that the architecture is correct. It gives us an executable decomposition that can now be tested one interface at a time.

## 4. Five AI workers, two state machines, fast loop beneath

Project direction preserved today:

- build five distinct AI workers
- coordinate them with two state machines
- keep a faster subconscious loop underneath

Do not invent the final identities of all five workers until they are explicitly assigned. The important architecture decision is separation of jobs plus coordinated state, not arbitrary naming.

The system should integrate:

- the user’s own control algorithm
- rabbit-hop memory / reconstruction routing
- constellation-style relational memory
- Circle-of-Fifths-derived organizational ideas where they are actually useful
- meaningful learned or measured weights rather than arbitrary weighting

Do not collapse the five workers into one omnipotent agent just because a single model can technically perform all five roles.

The exact mapping between the five workers and the six named software jobs above is intentionally left open until the interfaces are tested. Some jobs may be deterministic infrastructure rather than separate AI workers.

## 5. Rabbit hopping — scale and reconstruction route

Today’s rabbit-hop work is already represented in `ARCHITECTURE_RABBIT_HOPPING_SCALE_TRANSLATOR.md` and `AI_Readable_Packs/G-721_Mirrored_Alphabet_Rabbit_Hop.json`.

Preserve the core distinction:

Rabbit hopping is a reversible coordinate / route / scale mechanism. It is not itself the associative memory engine.

Core anchor:

`N -> 2N`

Wrapped connectors:

`2N-1 <- 2N -> 2N+1`

Parity-aware inverse:

- even `X`: `N = X/2`
- upper odd `X = 2N+1`: `N = (X-1)/2`
- lower odd `X = 2N-1`: `N = (X+1)/2`

The odd connector carries side / orientation information. Mirror traversal can invert orientation; preserve a sign/orientation receipt rather than erasing it.

Two route families remain distinct:

- shift then double: `(N+k)*2`
- double then shift: `2N+k`

Do not merge them simply because some values coincide.

Structurally, rabbit hopping now has a clearer possible role: it can provide addressable, reversible traversal information to the memory system without being confused with the memory completion process itself.

## 6. Constellation memory reconstruction

Today’s canonical memory architecture is in `ARCHITECTURE_MEMORY_REBUILD_CONSTELLATION.md`.

Keep the jobs separate:

- Constellation = relational memory structure
- Rabbit hopping = coordinate/navigation/scale reconstruction route
- Hopfield-style process = associative completion from partial/noisy cues
- Boltzmann-style process = probabilistic/generative fill when ambiguity remains
- fast recurrent loop = active process memory / short-lived state history
- two state machines = context validation, acceptance, oversight, and action/override

Recall should be reconstructive, not treated as reading one perfect stored file.

A useful recall receipt can include:

- cue that triggered recall
- constellation neighborhood entered
- rabbit-hop anchors/connectors traversed
- mirror/sign inversions
- associative-completion contribution
- probabilistic-fill contribution and uncertainty
- state-machine validation result

Pattern separation is mandatory: similar memories must not be silently collapsed into one attractor.

### Structural connection to the worker chain

This gives memory a route through the software organization:

`cue -> Cells/Nerves detect -> M4 routes -> constellation neighborhood -> rabbit-hop route -> completion/reconstruction -> Administrator/context check -> accepted state -> Executor if action is required`

Dream can participate when reconstruction genuinely needs candidate generation, but generated material must remain distinguishable from retrieved or strongly reconstructed material.

## 7. Micro -> Macro recursive coding loop

Preserve the emerging software-construction principle:

Build and validate at the smallest useful scale, then let the same explicit routing / receipt discipline recur upward.

The important part is not copying identical code at every scale. The recurring pattern is:

`local primitive -> event/reaction -> route/synchronize -> generate -> evaluate -> execute -> receipt`

Higher layers should be composed from tested lower-layer behaviors rather than replacing them with a giant opaque controller.

This is one of the strongest structural consequences of today’s work: the theory no longer has to be implemented all at once. Each boundary can become a small executable contract.

## 8. Animator / Director work completed or advanced today

The animator lives inside this repository under `Tools/Chats-Animator`; it is a tool project and should remain separate from the state-machine theory even though the same repository currently contains both.

Today’s `main` history includes work that:

- restored / retained the real FPS animator path rather than reopening a discarded alternate shell
- separates server health from AI-model connectivity
- exposes live AI connection failures in Director dialogue
- updates the animator smoke test for live AI dialogue
- uses OpenAI as the Director while retaining local-first image-worker behavior where configured
- adds first-run Director configuration
- wires launcher / Ubuntu installer behavior to the Director configuration
- tests the corrected Director build on `main`

The corrected build state from today supersedes the earlier installer target; the later corrected main commit was `b7853b547989105f3bc96bcd85d98195453f32b2`.

### Animator product requirement remains

The editor is intended to work as a co-creation surface:

- main animation editing / playback window
- built-in dialogue area directly in the program
- user can suggest work in natural language rather than memorize commands
- AI can create or modify background / motion / placement proposals
- user can manually adjust the same project
- motion library is organized per character
- props have their own accessible section
- frame animation remains real still-frame / FPS playback: one PNG file equals one frame, like projector film
- motion assets are created as needed rather than requiring the entire library up front
- completed sequences can be played and inspected, then edited over a specified time range
- the project should keep provider-facing invocation from becoming unnecessarily tied to one AI provider even when one provider is used as the current Director

Do not reintroduce the discarded Chats-Animator structure as a separate competing architecture; work from the **current working animator path**.

The animator is useful as a separate real software testbed for the job-separated coding method, but it must not be used as evidence for the physical/control theory.

## 9. Separation rules from today

Do not collapse these because they sound similar:

- three mirrored flip-pairs != six independent flips
- rabbit route != memory content
- constellation != Hopfield completion
- Hopfield completion != Boltzmann proposal
- fast nerve response != Administrator decision
- M4 routing != Dream planning
- Administrator evaluation != Executor action
- animator Director architecture != physical/control state-machine architecture
- five field lifecycle states != six mirrored positions

The five canonical Field lifecycle states remain:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

Do not invent a sixth lifecycle state from the mirror geometry.

## 10. What today now makes clearer

Today’s value is not that a final answer was reached. It is that the architecture has fewer loose pieces.

The emerging structural stack can now be read as:

`small deterministic state`

`-> fast local reaction`

`-> timed/routed/compressed transport`

`-> memory/context reconstruction when needed`

`-> candidate generation when needed`

`-> slower oversight/selection`

`-> committed action`

`-> receipt carried back into state/memory`

At the same time, the mirrored flip-pair model provides a candidate way to describe how view and action states hand off without pretending they are six unrelated moments.

This narrows the next question from **“How do we build the whole architecture?”** to **“What is the smallest packet that can survive one full round trip through it?”**

## 11. Next build order

The next work should follow dependency order rather than trying to instantiate every layer at once.

### Step A — define the packet

Create one minimal packet that can carry:

- current state
- old view
- new view
- old action
- direction / mirror side
- timestamp or phase
- source
- destination
- confidence / uncertainty where relevant
- route receipt

Do not add more fields until a test requires them.

### Step B — encode one mirrored transition

Implement one three-flip-pair transition using the packet.

The first test is not whether the theory is true. The test is whether the software representation can:

- preserve old/new state distinctly
- move through the mirror without duplicating flips
- retain direction/orientation
- reconstruct what happened from the receipt

### Step C — Cells -> Nerves -> M4 only

Build the smallest executable lower loop:

`Cell detects -> Nerve reacts -> M4 routes -> receipt`

No Dream, Administrator, memory reconstruction, or full AI worker is required yet.

This establishes the fast path first.

### Step D — add oversight

Add Administrator only after the fast path is deterministic.

Test:

`fast event -> compressed M4 report -> Administrator oversight -> no action or override -> receipt`

Then test the second half:

`fast event -> report -> Administrator override -> Executor action -> receipt`

This is where `flip, flip, oversight; flip, flip, override` becomes executable instead of descriptive.

### Step E — add Dream as proposals, not authority

Once oversight works, allow Dream to generate more than one candidate response.

Administrator must be able to choose, reject, or hold all candidates.

Executor only receives the selected committed action.

### Step F — attach reconstructive memory

Only after the live packet loop works, connect:

`constellation -> rabbit-hop route -> associative completion -> probabilistic fill if needed`

Feed the rebuilt result back through Administrator validation before it changes committed state.

### Step G — test recursive scaling

Once one small loop works, instantiate a second level using the same interface discipline.

Do not copy every implementation detail. Reuse the packet/receipt contract and see whether the higher level can treat the lower loop as one bounded unit.

### Step H — then decide the five-worker split

After the interfaces are visible in running code, assign the five AI workers based on actual computational jobs and bottlenecks.

Do not decide the five workers merely to satisfy the number five. The structure should determine which jobs genuinely benefit from separate learned agents and which should remain deterministic code.

## 12. Immediate executable tests

1. Define the minimal transition packet and receipt schema.
2. Encode one three-mirrored-flip transition showing old view, new view, and old action.
3. Reverse the receipt and verify the transition history can be reconstructed.
4. Build one deterministic `Cells -> Nerves -> M4` event path.
5. Add one oversight event without override.
6. Add one override event with Executor action.
7. Add a Dream proposal only after those six tests pass.
8. Run the minimum constellation-memory rebuild test already defined in `ARCHITECTURE_MEMORY_REBUILD_CONSTELLATION.md`.
9. Compare reconstruction with and without rabbit-hop route receipts.
10. Keep animator regression testing separate: background + character frame playback + Director dialogue must stay runnable while architecture work continues.

## 13. Claim discipline for this update

**None of the architecture recorded here is proof.**

The repository should treat it as:

- structural organization
- candidate relationships
- implementation hypotheses
- interface definitions
- test targets
- corrections to earlier structural misunderstandings
- clues about dependency order

A piece becoming more coherent with neighboring pieces is valuable because it tells us what to build next. Coherence alone is not evidence that the larger physical interpretation is correct.

For repo maintenance:

- preserve old material rather than rewriting history
- add corrections explicitly
- keep structural hypotheses available for implementation
- record failures as aggressively as successes
- let executable tests determine which pieces survive
- when two descriptions conflict, keep the newer explicit correction and record what changed
