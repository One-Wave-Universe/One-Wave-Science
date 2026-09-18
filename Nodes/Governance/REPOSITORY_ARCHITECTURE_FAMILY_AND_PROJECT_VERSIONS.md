# Repository Architecture Family and Project Versions

Date: 2026-08-30

Status: structural organization rule.

## Core rule

The repository contains a recurring architecture family.

Many projects use the same underlying organizational pattern, but they are **different versions / instantiations** of that pattern.

Do not flatten them into one identical machine.

Use this model:

`shared structural pattern -> domain version -> project implementation -> experiment/test`

The pattern recurs. The implementation changes.

---

# 1. Shared structural pattern

The recurring shape is:

`local state -> local event/change -> route -> generate/resolve -> evaluate -> act -> consequence -> new local state`

A second equivalent software-oriented form is:

`Cells -> Nerves -> M4 -> Dream -> Administrator -> Executor -> receipt`

This is the reusable organizational skeleton.

What remains shared across versions:

- bounded local units
- explicit routing
- state carried with context
- fast and slow layers
- view / action separation
- proposal vs commitment separation
- consequence returning as new reference
- receipts/provenance
- recursive composition from smaller units to larger units

What is **not** automatically shared:

- exact state names
- exact number of internal variables
- timing rates
- physical mechanism
- sensor types
- memory representation
- UI representation
- hardware mapping
- project vocabulary

Same pattern does not mean identical implementation.

---

# 2. Version rule

Every project or subsystem must declare its architecture version.

A version declaration should answer:

- what counts as a Cell here?
- what counts as a Nerve/event layer here?
- what performs M4-style routing here?
- what generates candidates here?
- what evaluates candidates here?
- what executes here?
- what is the local state?
- what is the reference/center?
- what travels upward as view/information?
- what travels downward as action/commitment?
- what closes the loop as consequence?

If one of those jobs is absent in a simpler project, mark it absent. Do not invent a fake component just to make the diagram symmetrical.

---

# 3. Control / cognition version

This version uses the architecture most literally.

```text
Cells
 -> Nerves
 -> M4
 -> Dream
 -> Administrator
 -> Executor
 -> body/world consequence
 -> new reference
```

Native concerns:

- fast subconscious reaction
- slower oversight / override
- Field / Void processing
- mirrored view/action relationship
- memory recall and reconstruction
- state / scale routing
- behavioral consequence

This version can use the current shorthand:

`flip, flip, oversight; flip, flip, override`

That timing shorthand belongs to this control-family version unless another version explicitly derives its own equivalent.

---

# 4. Droid / embodied version

Same pattern, different native meaning.

Possible mapping:

- Cells = sensor parsers, motor primitives, local threshold functions
- Nerves = curb-drop, collision, proximity, tilt, wheel-slip, emergency brake handlers
- M4 = body router and timing coordinator
- Dream = candidate movement / path / behavior generator
- Administrator = checks goal, body state, continuity, and consequences
- Executor = wheel, joint, speaker, light, or actuator command layer

Native local state includes body geometry and sensor state.

The droid version is not identical to the abstract cognition version even when it uses the same flow.

---

# 5. VTC / Wave Computer version

Same pattern, computational version.

Possible mapping:

- Cells = deterministic compute primitives / local relational units
- Nerves = local transitions / threshold events / interrupts
- M4 = route, state, scale, phase, and packet coordinator
- Dream = candidate computation paths / alternative reconstructions
- Administrator = validation / acceptance / rejection / coherence checks
- Executor = committed state transition / write / propagation

Native concerns:

- Field / Void relation
- binary / ternary route space
- shared center/reference
- recursive cube or node composition
- local persistent state
- receipts

The VTC version can be implemented in software, electronics, magnetic devices, or another carrier without changing the architecture-family identity.

Carrier != architecture.

---

# 6. Memory-system version

Same structural family, specialized for recall.

```text
partial cue
 -> constellation neighborhood
 -> rabbit-hop route
 -> associative completion
 -> probabilistic candidate fill
 -> higher validation
 -> rebuilt active memory
 -> new active context
```

Mapping:

- Cells = feature / relation units
- Nerves = cue activations / local match events
- M4 = memory route / scale / recall coordinator
- Dream-like function = generative missing-piece proposals
- Administrator-like function = context and consistency validation
- Executor-like function = acceptance into active working state

The memory version uses the same separation of proposal vs commitment, but its output is rebuilt active state rather than a motor action.

---

# 7. Animator / creative-editor version

The animator can use the same organizational pattern, but in a software-creative form.

Possible mapping:

- Cells = frame loaders, validators, transforms, timing calculations, asset parsers
- Nerves = UI clicks, file changes, timeline scrubs, playback ticks
- M4 = editor/router that sends work to the correct subsystem
- Dream = generates animation ideas, edits, assets, timing alternatives
- Administrator = checks project constraints, continuity, selected time range, user intent
- Executor = applies approved edit to project state

Native state:

- timeline
- FPS
- frame sequence
- background
- character placement
- motion library
- props
- edit history

Native consequence:

- rendered/playable project state

The animator is therefore a **different version of the recurring architecture**, not literally the same brain/control machine.

Its tests remain ordinary software tests.

---

# 8. Bench / simulator version

The bench version exists to isolate and test pieces of the architecture family.

Mapping:

- Cells = small testable functions
- Nerves = injected events
- M4 = deterministic test router
- Dream = optional candidate generator for tests that require alternatives
- Administrator = assertion / validation layer
- Executor = simulated transition

This version may omit whole layers when testing primitives.

A six-route logic test does not need to instantiate Dream or Administrator unless that test is specifically about those layers.

---

# 9. Mirrored structures are also versions

The binary / ternary / quadratic mirrored relationship should be treated as a reusable structural pattern with domain-specific expressions.

Abstract form:

```text
upward side:   simpler relation -> resolved relation -> richer view
mirror/reference transition
 downward side: richer action -> resolved action -> simpler committed output
```

In the control version this may appear as:

`binary -> ternary -> quadratic` upward

and

`quadratic -> ternary -> binary` downward

Other project versions may use different native payloads while preserving the idea of increasing contextual richness upward and increasing commitment specificity downward.

Do not force the literal words binary/ternary/quadratic onto a project that does not use those data structures.

---

# 10. Recursive scale rule

The architecture can recur at different scales.

A lower-level complete unit can appear as one Cell inside a higher-level version.

Example:

```text
small complete loop
 -> becomes one bounded unit
 -> several bounded units form a routed subsystem
 -> several routed subsystems form a larger project controller
```

This is how the same structural logic can appear repeatedly without every level being identical.

The rule is:

`preserve relationship, change native representation`

At each scale preserve only what still has functional meaning:

- local state
- relation to reference
- route
- proposal/commit distinction
- action/result distinction
- consequence receipt

Do not copy names mechanically across scales.

---

# 11. Project adapters

Each project needs an adapter between the shared architecture family and project-native objects.

Examples:

## Droid adapter

architecture packet -> sensor/motor/body command

## Animator adapter

architecture packet -> timeline/frame/asset edit

## VTC adapter

architecture packet -> relational state transition

## Memory adapter

architecture packet -> cue / constellation / recall operation

Adapters are where project-specific vocabulary belongs.

This prevents project details from corrupting shared architecture while still allowing all projects to use the same structural family.

---

# 12. Common packet, version-specific payload

Use a lightweight shared envelope:

```text
id
source
project/version
tick/time
reference
intent
direction
state summary
payload
confidence/integrity
receipt parent
```

The `payload` is version-specific.

Examples:

- Droid payload: wheel speed, tilt, proximity
- Animator payload: frame range, asset id, transform
- VTC payload: route, phase, local relation
- Memory payload: cue, constellation neighborhood, recall candidate

The envelope is shared; the payload is not.

---

# 13. Architecture registry

Every major subsystem should eventually register itself with:

```text
name
version/domain
shared pattern used
native state
input
output
reference/center
fast path
slow path
proposal owner
decision owner
executor
receipt type
parent architecture version
child units
```

This creates structure without pretending everything is literally one machine.

---

# 14. Next structural build

The next repo work should be structural, not another theory dump.

1. Create an `Architecture/` area for shared patterns and interfaces.
2. Create a `Projects/` registry that identifies each concrete project and its architecture version.
3. Give each project a one-page architecture declaration using the registry fields above.
4. Move no files yet; first build indexes and aliases so nothing breaks.
5. Create the shared packet/schema.
6. Create the first three adapters:
   - Droid
   - VTC
   - Animator
7. Implement a tiny executable path through each version to verify the abstraction actually fits:
   - Droid: sensor event -> route -> motor proposal -> commit -> simulated consequence
   - VTC: local relation -> route -> validation -> committed state -> next reference
   - Animator: edit request -> route -> edit proposal -> approval -> project-state update
8. Compare the three traces and extract only the genuinely shared invariants back into the shared architecture.

That last step is critical: architecture should be strengthened by what survives across versions, not by forcing every project into the same labels.
