# Rabbit Hopping and Recursive Scale Translator

Status: working architecture record. This file separates confirmed structure from provisional and experimental claims so later agents do not silently promote guesses into canon.

## Confirmed structural anchors

### 1. Parity anchor and ±1 connector
A hop begins from a chosen parity anchor. If the anchor is even, `anchor - 1` and `anchor + 1` are the neighboring odd positions. If the anchor is odd, the neighboring positions are even.

Examples:

- `4 -> 3 / 5`
- `6 -> 5 / 7`
- `8 -> 7 / 9`

The important rule is:

`anchor + (-1,+1) = mirrored local connection`

This turns a static address into a transition-capable address. The ±1 relation is the connector between opposite parity tracks.

### 2. Shifted anchor form
The explicitly confirmed shifted form is:

`(N + 1) * 2 ± 1`

which expands to:

`2N + 1` and `2N + 3`.

For `N = 1`, the anchor is 4 and the pair is 3 / 5.

Do not confuse this with `N + 1 * 2 ± 1`; parentheses are required because the intended operation is: increment N, then double, then apply ±1.

### 3. Mirrored flip principle
The six-position Android/control structure is:

`Binary -> Ternary -> Quadratic -> Quadratic -> Ternary -> Binary`

The first three positions are the Views/Oversight half. The second three are the Actions/Override half.

The six positions are three mirrored pairs rather than six independent flips:

- Binary <-> Binary
- Ternary <-> Ternary
- Quadratic <-> Quadratic

Therefore the structure has three paired flips across six positions.

### 4. Five lifecycle states remain separate
The lifecycle is:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

These five states describe phase. They are not replacements for, or members of, the six-position mirrored control loop.

### 5. Recursive scale transition: Macro becomes next Micro
The five-scale worker architecture is recursive. A resolved Macro output at one tier can become the Micro input/anchor at the next tier.

The working loop is bidirectional rather than a one-way pipeline:

`Micro -> Small -> Mid -> Large -> Macro -> Large -> Mid -> Small -> Micro`

Confirmed role anchors:

- Micro = Parser
- Mid = Connector
- Large = Explorer
- Macro = Administrator / Void final-say role
- Small remains a bounded local construction role; exact canonical name is still provisional.

### 6. Octave transition principle
Scale changes reuse the same local relationship rather than inventing new geometry at each scale. The working hypothesis is that octave/2x transitions change span or resolution while parity and mirrored-neighbor relationships remain reconstructible.

A high-level resolved anchor can therefore descend through scale into lower-level work, and lower-level consequence can compress upward into a new anchor.

### 7. Reversible receipts
Every scale transition must leave enough evidence to reconstruct how the upper anchor came from lower-level state.

A receipt should minimally preserve:

- source anchor
- source scale/tier
- target scale/tier
- parity/anchor relation used
- hop or transform used
- resulting anchor/state
- reconstruction key or parent reference
- observed consequence when an action occurred

Compression without a reconstruction path is not accepted as drift-safe.

## M4 scale translator: current working model

The fast subconscious/M4 layer is proposed as the scale translator and router. It should translate already-resolved intent between scales rather than re-reasoning the entire decision at every lower tier.

Downward working path:

`Macro decision -> compressed anchor -> scale translation -> lower-tier anchor -> local control/action`

Upward working path:

`local consequence -> receipt -> relational compression -> higher-tier anchor -> next deliberative state`

The translation must remain traceable through reversible receipts.

## Rabbit hopping as memory addressing

Rabbit hopping is being developed as reconstructive addressing rather than a flat lookup table. A stored item can be reached through relational hops generated from anchor, parity, direction, scale, and neighborhood rather than by storing every possible explicit edge.

The intended properties to test are:

1. partial cue can reconstruct a larger stored structure;
2. a larger structure can route back to exact lower-detail evidence;
3. parity/mirror relations reduce arbitrary addressing;
4. octave transitions preserve a reconstructible lineage;
5. failures can be localized to a hop/receipt instead of becoming silent context drift.

## Relational geometry under test

The following remain experimental and must not be treated as mathematically proven merely because they are architecturally useful:

- constellation-style relational memory;
- Circle-of-Fifths/wheel geometry as a routing or weighting structure;
- four-view address families beyond the explicitly verified arithmetic;
- structurally derived weights from adjacency, opposition, recurrence, distance, consequence, and confidence;
- claims that octave compression guarantees freedom from context drift.

These are candidates for falsifiable tests, not completed proofs.

## Candidate multi-view formulas

The conversation explored several related forms, including:

- `2N ± 1`
- `2N + 1 ± 1`
- `2N + 3 ± 1`
- `(N + 1) * 2 ± 1`

Only algebraically equivalent relationships should be merged. Do not automatically extrapolate a regular `+1,+3,+5` family or call it canonical without checking collisions, coverage, mirror symmetry, and whether each view contributes distinct structure.

## Minimum falsification tests

Before promoting this module from working architecture to trusted implementation, test:

1. Generate addresses for a small range such as `N = 1..12`.
2. Verify every claimed ±1 parity relation.
3. Measure duplicate/colliding addresses across candidate views.
4. Verify that a lower-level receipt can reconstruct its upper anchor exactly.
5. Verify that an upper anchor can resolve back to the intended lower path without ambiguous branching.
6. Inject a deliberately wrong hop and confirm the receipt audit catches it.
7. Compare rabbit-hop reconstruction against a flat lookup/vector baseline and a Hopfield-style associative baseline on the same partial-cue task.

## Anti-drift rules for this module

- Preserve exact formulas before summarizing them.
- Same pattern does not mean same system.
- Do not silently rename established roles.
- Do not promote tentative speech/transcription into canonical structure without consistency checking.
- If the same correction method fails three times, switch to a materially different mechanism.
- Explorer may propose new hop families; Macro/Admin may accept or reject them; neither may silently rewrite the source anchor.
- Every accepted compression across scale must retain a reversible receipt.
