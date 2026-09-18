# Memory Rebuild / Constellation Architecture

Status: working architecture. Keep the subsystems distinct; same pattern does not mean same system.

## Primitive idea

Memory is not treated as one stored file that is simply read back. The active processing state, relational structure, and reconstruction route are part of the memory.

Recall flow:

`cue -> constellation neighborhood -> rabbit-hop route -> associative completion -> probabilistic fill -> context/state-machine check -> rebuilt active memory`

## Jobs

### Constellation

The constellation is the relational shape of a memory. A remembered event can be distributed across linked features such as sensory fragments, motion, timing, language, body state, place, and neighboring memories. A partial cue can activate the local neighborhood without requiring a complete stored copy.

Constellation does **not** choose the rabbit-hop coordinate rule and does **not** replace the reconstruction engines.

### Rabbit hopping

Rabbit hopping is the reversible route/coordinate mechanism used to move through the constellation and between scales.

Core local scale anchor:

`N -> 2N`

Wrapped connectors:

`2N-1 <- 2N -> 2N+1`

Parity-aware inverse:

- even `X`: `N = X/2`
- upper odd connector `X = 2N+1`: `N = (X-1)/2`
- lower odd connector `X = 2N-1`: `N = (X+1)/2`

Two upward families are preserved as separate operations:

1. shift then double: `(N+k)*2`, for `k = 1,2,3,...`, each even anchor wrapped by `-1/+1`
2. double then shift: `2N+k`, for `k = 1,2,3,...`, each route preserving its `-/+` or `+/-` orientation

The odd connector carries the up/down side information around an even scale anchor. Across a mirror, connector orientation may invert; do not discard the sign/orientation receipt.

Examples currently stated:

- A (`N=1`): `(1+2)*2 = 6`, connectors `5/7`; next even-up anchor `(1+3)*2 = 8`, connectors `7/9`
- B (`N=2`): `(2+2)*2 = 8`, connectors `7/9`
- C (`N=3`): `(3+2)*2 = 10`, connectors `9/11`

Do not invent a finite stopping value for `k`; test the route grammar and reversibility at each scale.

### Hopfield-style completion

Use associative attractor behavior to settle a partial or noisy cue toward a known stable memory pattern. This is the deterministic/associative completion part of rebuild.

### Boltzmann-style reconstruction

Use probabilistic/generative reconstruction when the cue leaves genuine ambiguity or missing pieces. Generated pieces are proposals, not automatically accepted memory.

### Processing as active memory

The fast recurrent loop carries short-lived history in its current state, timing, phase, and recent route. A memory can therefore exist partly as an active process rather than only as a static record.

Longer-lived memory may retain sparse durable structure such as relationships, weights, anchors, route receipts, and attractor constraints. Recall recreates the richer active state from these pieces.

### Pattern separation

Completion must not force two similar but distinct memories into one attractor. When evidence conflicts with an existing constellation, preserve a separate candidate rather than silently merging it.

### Validation by the two state machines

Reconstruction is not final until the higher state machines compare it with current context and active state. The reconstruction engines propose/rebuild; the state machines decide whether the result is accepted, held as uncertain, or rejected.

The fast loop can continue carrying local procedural state while the slower oversight/override path validates the rebuilt memory.

## Rebuild receipt

Every completed recall should be able to retain a compact receipt containing:

- cue(s) that initiated recall
- constellation neighborhood entered
- rabbit-hop anchors/connectors traversed
- mirror/sign inversions used
- associative completion contribution
- probabilistic fill contribution and confidence/uncertainty
- state-machine validation result

The receipt is for reversibility and debugging; it is not a second full copy of the memory.

## Separation rules

- Constellation = relational memory structure.
- Rabbit hopping = coordinate/navigation/scale reconstruction route.
- Hopfield = associative completion.
- Boltzmann = probabilistic/generative fill.
- Fast loop = active short-term/process memory.
- Two state machines = context/acceptance/oversight and action/override validation.

Do not collapse these jobs into one worker.

## Minimum executable test

1. Store a small constellation with overlapping features across at least two memories.
2. Remove part of one memory.
3. Present a surviving partial cue.
4. Traverse a recorded rabbit-hop neighborhood including at least one `2N +/- 1` connector.
5. Run associative completion.
6. If ambiguity remains, run probabilistic fill and mark the generated portion uncertain.
7. Validate the result against current state.
8. Compare with the original memory and with a no-rabbit-hop/no-constellation baseline.
9. Verify the route can be inverted using the stored parity/sign receipt.

Success means the system reconstructs the intended memory more reliably than the baseline without collapsing a nearby distinct memory into it.
