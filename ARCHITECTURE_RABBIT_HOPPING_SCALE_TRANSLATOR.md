# Rabbit Hopping and Recursive Scale Translator

Status: working architecture record. This file separates the locked arithmetic grammar from domain-level hypotheses so later agents do not collapse route math, memory, movement, or physics into one claim.

## Locked N-based translator grammar

Rabbit hopping uses N as the base address. The grammar has two operation-order families, a parity wrapper, signed mirroring, alphabet inversion, opposing traversal, and exact divide-by-2 reconstruction.

### 1. Double-first family

Double N, then shift:

`2N, 2N+1, 2N+2, 2N+3, 2N+4, ...`

General form:

`R_after(N,m) = 2N + m`

where `m` is an integer offset.

### 2. Shift-first family

Shift N, then double:

`2N, 2(N+1), 2(N+2), 2(N+3), 2(N+4), ...`

General form:

`R_before(N,m) = 2(N+m)`

The two paths can reach the same numerical destination:

`2N + 2m = 2(N+m)`

This is intentionally treated as two routes to one address. A reversible receipt preserves which route produced the address.

### 3. Opposite-parity ±1 wrapper

Any chosen center `X` is wrapped as:

`X-1, X, X+1`

If X is even, its wrapper is odd. If X is odd, its wrapper is even.

Examples:

- `4 -> 3 / 5`
- `6 -> 5 / 7`
- `3 -> 2 / 4`
- `5 -> 4 / 6`

Adjacent nests connect through their shared boundary. For the even-centered sequence:

`3 - 4 - 5`

`5 - 6 - 7`

The shared value follows the identity:

`2N + 1 = 2(N+1) - 1`

The wrapper exists to preserve connection between neighboring nested addresses and allow traversal in either direction.

### 4. Mirrored, inverted, and opposing stay distinct

- Mirrored: change sign/polarity, `X -> -X`.
- Inverted: reverse alphabet rank, `N_inv = 27 - N` for A..Z.
- Opposing: traverse the declared route in reverse order.

These operations may be composed, but they are not synonyms.

### 5. Alphabet map

Forward:

`A=1, B=2, ... Z=26`

Inverted:

`Z=1, Y=2, ... A=26`

Exact inversion:

`N_inv = 27 - N`

### 6. Signed forms

Both route families may be mirrored across zero:

`±(2N+m)`

`±2(N+m)`

Sign does not silently change alphabet orientation or route direction.

### 7. Division is reconstruction

Division by two is the inverse of the doubled route after the declared wrapper/offset is removed.

For:

`X = 2N + m`

recover:

`N = (X-m)/2`

For:

`X = 2(N+m)`

recover:

`N = X/2 - m`

With a wrapper `s` where `s ∈ {-1,+1}`:

`X = 2(N+m) + s`

recover:

`N = (X-s)/2 - m`

and for:

`X = 2N + m + s`

recover:

`N = (X-m-s)/2`

This is the reversible inward path of the outward doubling grammar.

## Point -> Path -> Field nesting

The translator can represent a nested handoff:

`Point_N -> Path_N -> Field_N -> next nested address`

Moving to the next layer changes the reference from `N` to `N+1`. The ±1 wrapper preserves the shared boundary so the old layer and next layer remain connected.

The arithmetic defines a relational map. Whether Point/Path/Field corresponds faithfully to a specific target domain must be tested in that domain.

## Reversible receipts

Every accepted translation must preserve enough information to reconstruct its origin. At minimum record:

- source N;
- forward or inverted alphabet orientation when alphabet mapping is used;
- sign/polarity;
- route family: double-first or shift-first;
- integer offset;
- wrapper side: -1, 0, or +1;
- resulting address;
- traversal direction;
- parent/source reference when nested across scale.

Equal destination does not imply equal path. For example `2N+2m` and `2(N+m)` are numerically equal but retain distinct route receipts.

## Recursive scale transition

The five-scale worker architecture remains bidirectional:

`Micro -> Small -> Mid -> Large -> Macro -> Large -> Mid -> Small -> Micro`

A resolved Macro result may become the next Micro anchor. Lower-level consequence may compress upward only when the reconstruction receipt is retained.

Current role anchors:

- Micro = Parser
- Mid = Connector
- Large = Explorer
- Macro = Administrator / Void final-say role
- Small remains a bounded local construction role; exact canonical name remains provisional.

## M4 scale translator role

M4 routes already-resolved intent and consequences between scales rather than silently re-reasoning the entire decision at every tier.

Downward:

`Macro decision -> compressed address -> scale translation -> lower-tier address -> local action`

Upward:

`local consequence -> receipt -> relational compression -> higher-tier address -> next deliberative state`

## Rabbit hopping as reconstructive addressing

Rabbit hopping is a relational addressing method rather than a flat lookup requirement. A stored item may be reached by reconstructing its route from N, operation order, offset, parity wrapper, polarity, orientation, and traversal direction.

Target properties to test:

1. partial cue reconstructs a larger stored structure;
2. larger structure routes back to exact lower evidence;
3. parity wrapping preserves adjacent nesting;
4. alternate arithmetic paths that meet at the same address remain distinguishable by receipts;
5. divide-by-2 reconstruction returns the original N exactly;
6. failures localize to a hop or receipt rather than becoming silent drift.

## Domain boundary

The translator is intended as a common relational map. Claims that it is universal across every possible system, or that it directly explains physical interactions, remain hypotheses until demonstrated with domain-specific mappings and falsification tests.

The following remain separate from the arithmetic grammar:

- Hopfield/Boltzmann associative memory;
- Circle-of-Fifths/wheel movement geometry;
- embodied motor control;
- physical One-Wave/superfluid interpretations;
- derived weighting schemes.

## Minimum validation tests

1. Generate both route families for `N=1..26` and several offsets.
2. Verify `2N+2m = 2(N+m)` exactly.
3. Verify every ±1 wrapper has opposite parity to its center.
4. Verify adjacent declared nests share the expected wrapper address.
5. Verify positive and negative routes are exact sign mirrors.
6. Verify `N_inv=27-N` maps A<->Z, B<->Y, and so on.
7. Verify all inverse division formulas reconstruct the original N exactly.
8. Verify route receipts distinguish numerically equal destinations reached by different operation orders.
9. Reverse a route and verify the ordered receipt sequence reverses without silently changing sign or inversion.
10. Inject a wrong wrapper, offset, or route-family receipt and verify reconstruction fails visibly.

## Anti-drift rules

- Keep the equations in N unless a downstream implementation requires local variable names.
- Preserve parentheses because operation order is part of the route identity.
- Do not collapse mirrored, inverted, and opposing into one operation.
- Do not collapse equal destination into equal route.
- Do not use division without removing the recorded wrapper/offset in the correct order.
- Do not silently promote translator arithmetic into proof of a physical mechanism.
- Every accepted compression or scale transition must retain a reversible receipt.
