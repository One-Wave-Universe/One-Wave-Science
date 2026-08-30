# Updated 30 — Mirrored Flip Pairs, Memory Rebuild, Worker Architecture, and Animator State

Date: 2026-08-30

Status: working architecture / preservation update. This file records the important decisions and corrections from today without replacing older evidence. Where a relationship is still being tested, it is labeled provisional rather than promoted to a proven physical claim.

## 1. Six apparent positions are three mirrored flip-pairs

Do not model the binary / ternary / quadratic sequence as six independent flips.

The current control-loop interpretation is three mirrored transition pairs across the view/action mirror:

- binary view-side position <-> binary action-side position
- ternary view-side position <-> ternary action-side position
- quadratic view-side position <-> quadratic action-side position

The apparent six positions are therefore three paired transitions seen from two mirrored directions.

A flip is one paired transition across the mirror, not two unrelated events. Do not duplicate the flip count by treating the view and action faces as independent flips.

### Functional direction

Current functional description:

`binary -> ternary -> quadratic` = oversight / view side

`quadratic -> ternary -> binary` = action / execution side

This is a functional mapping, not a claim that the underlying physics has been experimentally established.

### Temporal receipt — provisional but important

Preserve the stated timing relationship for testing:

- old view travels upward
- new view travels upward
- old action travels downward

The point is that the mirrored transition carries state history through the flip instead of replacing everything at once. The exact timing and implementation remain experimental, but the relationship must not be silently flattened into six stateless steps.

## 2. Fast loop and slower oversight / override

Keep the established timing discipline:

`flip, flip, oversight; flip, flip, override`

This expresses a 3:1 local nerve-to-supervisory event relationship and a 6:1 full oversight/override rhythm when the two supervisory events are taken together.

The fast subconscious / nerve loop is intentionally ahead of slower cognition. Local body-protection responses can occur before the higher layer finishes interpreting them.

The higher layer should receive compressed, routed, referenced information rather than raw uncontrolled traffic.

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

## 7. Micro -> Macro recursive coding loop

Preserve the emerging software-construction principle:

Build and validate at the smallest useful scale, then let the same explicit routing / receipt discipline recur upward.

The important part is not copying identical code at every scale. The recurring pattern is:

`local primitive -> event/reaction -> route/synchronize -> generate -> evaluate -> execute -> receipt`

Higher layers should be composed from tested lower-layer behaviors rather than replacing them with a giant opaque controller.

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

Do not reintroduce the discarded Chats-Animator structure as a separate competing architecture; work from the current proven animator path.

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

## 10. Next executable architecture tests

1. Encode one three-flip-pair transition with an explicit receipt showing old view, new view, and old action.
2. Verify the receipt can be inverted without treating the mirror faces as six unrelated events.
3. Implement one tiny Cells -> Nerves -> M4 path with deterministic tests before adding Dream or Administrator.
4. Add one Dream proposal and require Administrator acceptance before Executor action.
5. Run the minimum constellation-memory rebuild test already defined in `ARCHITECTURE_MEMORY_REBUILD_CONSTELLATION.md`.
6. Compare memory rebuild with and without rabbit-hop route receipts.
7. Keep animator regression testing separate: background + character frame playback + Director dialogue must stay runnable while architecture work continues.

## 11. Evidence / claim discipline

This update preserves the architecture as currently understood. It does not convert speculative physical interpretations into established experimental facts.

For repo maintenance:

- preserve old evidence rather than rewriting history
- add corrections explicitly
- keep working hypotheses labeled working / provisional
- promote claims only when there is a reproducible test or external evidence appropriate to the claim
- when two descriptions conflict, keep the newer explicit correction and record what changed
