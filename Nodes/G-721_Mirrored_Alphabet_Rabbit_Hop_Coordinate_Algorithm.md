---
node_id: "G-721"
canonical_name: "Mirrored Alphabet Rabbit-Hop Coordinate Algorithm"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Symbolic Coordinate System / Route Compiler / Reversible Translator Grammar"
claim_gate_detail: "BRONZE (coordinate packet, parity wrapper, mirror/inversion grammar, reversible arithmetic identities) / YELLOW (cross-domain and embodied implementation)"
metadata_standard: "I-06"
---

# Node G-721: Mirrored Alphabet Rabbit-Hop Coordinate Algorithm

> **Authoritative lock:** `RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md`.
> **Executable arithmetic:** `One_Wave_Bench/brain/rabbit_hop_core.py`.
>
> This node describes the alphabet adapter and its interpretation. If shorthand
> here conflicts with the lock/core, the lock/core wins.

**Dependencies**  
Upstream: A-101 Ground / Zero, A-103 Differential, A-111 Recursion, B-205 Mirror, B-222 Oscillation Center, B-223 Three Moves, G-716 One-Wave Conversion Grammar  
Lateral: E-510 Music Clock / Harmonic Oscillation, G-719 Neural System Functional Analogy Map, G-720 No Control But Self-Control  
Downstream: G-721a Fibonacci reference validation, G-721b Sturmian branch grammar, G-721c episturmian routing, G-721d Arnoux-Rauzy validation, G-721e plastic/Padovan rail grammar, Wave Computer route compilation, Android procedural movement, Goblin embodied-agent simulation

## Purpose

The mirrored alphabet adapter converts letters and words into ordered,
reversible coordinate paths. Rabbit Hopping supplies identity, nesting, parity,
route-of-origin, and reversible coordinates. It does not claim that different
physical or software systems are identical.

Keep these layers separate:

```text
Hopfield / Boltzmann relationships = memory relationship models
Rabbit-Hop map                  = reversible address / translator grammar
wheel system                    = live oscillating movement geometry
-1(0)+1                         = foundational live choice convention
```

## Alphabet map

Forward orientation:

```text
A=1, B=2, ... Z=26
```

Inverted orientation:

```text
Z=1, Y=2, ... A=26
```

For a forward rank `N`:

```text
N_inv = 27 - N
```

A source rank belongs to the letter identity. A generated Rabbit-Hop TOP is an
address produced by that source; it does not replace the source identity.

## Canonical route grammar

The shared numerical core has exactly three current route receipts.

### ORIGINAL

```text
TOP = 2N
K = 0
```

### DOUBLE_THEN_SHIFT

```text
TOP = 2N + K
K ∈ integers
```

The local signed run explicitly includes:

```text
2N-3, 2N-2, 2N-1, 2N, 2N+1, 2N+2, 2N+3
```

and continues in both directions.

### SHIFT_THEN_DOUBLE

```text
TOP = 2(N + K)
K ∈ integers
```

The local signed run explicitly includes:

```text
2(N-3), 2(N-2), 2(N-1), 2N, 2(N+1), 2(N+2), 2(N+3)
```

and continues in both directions.

Historical names `ASCENDING_AFTER` and `ASCENDING_BEFORE` are compatibility
aliases only. They no longer mean positive-only K.

## Mandatory wrapper / connector

Top selection and wrapper selection are distinct operations.

For every selected TOP `X`, both complete packets exist:

```text
N | X | X-1
N | X | X+1
```

The final `-1/+1` is the connector around the already-selected TOP. It must not
be confused with a `K=-1/+1` top shift.

Compact generalized forms:

```text
V_K^s(N) = 2N + K + s
U_K^s(N) = 2(N+K) + s
```

where:

```text
K ∈ integers
s ∈ {-1,+1}
```

The wrapper has opposite parity from its TOP.

## Same destination, different route

Two operation orders can land on the same number:

```text
2N + 2m = 2(N + m)
```

Example:

```text
DOUBLE_THEN_SHIFT K=2
SHIFT_THEN_DOUBLE K=1
```

can reach the same TOP for the same N. The receipt must retain which route and
which K produced it.

Shared numeric destinations are useful handoffs; they do not erase route
history.

## Exact reverse / division reconstruction

For a complete double-then-shift packet:

```text
X = 2N + K + s
N = (X - K - s) / 2
```

For a complete shift-then-double packet:

```text
X = 2(N+K) + s
N = (X - s) / 2 - K
```

The complete route receipt therefore stores at minimum:

- source / alphabet orientation;
- route family;
- signed K;
- wrapper side s;
- polarity;
- traversal direction;
- resulting TOP and wrapper address.

The bounded `1..12 -> 12..24` scale/division rail is separately locked in
`rabbit_hop_scale_rail.py`. Broader claims about division remain open unless
another explicit lock defines them.

## Mirrored, inverted, and opposing remain separate

1. **Mirrored** changes numeric polarity: `X -> -X`.
2. **Inverted** reverses alphabet rank: `N -> 27-N`.
3. **Opposing** reverses declared traversal order.

These operations can compose, but none silently substitutes for another.

Alphabet side-to-side inversion also swaps logical lower/upper wrapper
assignment. Numeric polarity remains independent.

Whole-run Mirror Gate layouts remain:

```text
A-Z(0)Z-A
Z-A(0)A-Z
```

Zero sits between whole alphabet runs. It is not a route wrapper and is not a
letter TOP.

## Point -> Path -> Field interpretation

The grammar may be used as a nested routing map:

```text
Point_N -> Path_N -> Field_N -> next nested address
```

Shared `±1` boundaries can act as handoffs between declared nests. This is a
translator interpretation. A target domain must be tested separately before
claiming that this coordinate grammar faithfully represents its behavior.

## Word-to-path compilation

For each letter at step `t`, first map the letter to a forward or inverted
alphabet source rank `N_t`. Then record:

```text
polarity sigma_t ∈ {-1,+1}
route family
signed K_t
wrapper s_t ∈ {-1,+1}
traversal direction
```

Double then shift:

```text
X_t = sigma_t * (2N_t + K_t + s_t)
```

Shift then double:

```text
X_t = sigma_t * (2(N_t + K_t) + s_t)
```

The hop between consecutive addresses is:

```text
Delta X_t = X_(t+1) - X_t
```

Reversing traversal reverses the route order. It does not silently change
polarity, alphabet orientation, K, or wrapper side.

## Relationship to live choice

The alphabet/Rabbit-Hop translator proposes coordinates/routes; it does not make
foundational live choice.

```text
symbolic cue
-> alphabet coordinate
-> reversible Rabbit-Hop route
-> live -1(0)+1 choice
-> top-down validation / permission
-> committed movement
```

A stored route may schedule or validate movement. It does not force movement if
the live-choice/sensory layer selects Hold.

## Executable adapter

```text
One_Wave_Bench/brain/rabbit_hop_alphabet.py
One_Wave_Bench/brain/test_rabbit_hop_alphabet.py
```

The alphabet adapter imports the shared enums and route arithmetic from:

```text
One_Wave_Bench/brain/rabbit_hop_core.py
One_Wave_Bench/brain/test_rabbit_hop_core.py
```

Music and Circle-of-Fifths use the same core through:

```text
One_Wave_Bench/brain/rabbit_hop_music.py
RABBIT_HOPPING_MUSIC_ADAPTER.md
```

## Validation requirements

A valid implementation must verify:

1. alphabet ranks are in `1..26`;
2. inverted alphabet obeys `N_inv=27-N`;
3. `ORIGINAL` obeys `TOP=2N` and `K=0`;
4. double-then-shift obeys `TOP=2N+K` for signed K;
5. shift-then-double obeys `TOP=2(N+K)` for signed K;
6. explicit `K=-3,-2,-1,0,+1,+2,+3` cases work on both generalized routes;
7. every selected TOP has both `TOP-1` and `TOP+1` complete packets;
8. top shift and wrapper remain separate receipt fields;
9. equal numeric destinations keep different route receipts;
10. positive/negative forms are exact polarity mirrors;
11. mirror, alphabet inversion, and opposing traversal remain distinct;
12. exact inverse reconstruction returns the original source rank;
13. Mirror-Gate zero is not confused with a TOP or wrapper;
14. alphabet, memory, wheel, music, and live-choice layers remain separate.

## Failure conditions

The grammar fails when:

- parentheses are dropped and operation order changes;
- negative K is rejected by a generalized route;
- K and wrapper ±1 are collapsed into one operation;
- equal destinations are treated as identical routes;
- division/rebuild is attempted without route metadata;
- wrapper parity/side is discarded;
- mirroring is silently treated as alphabet inversion;
- reversal silently changes polarity or K;
- route arithmetic is presented as proof of a physical mechanism.

## Falsifier

This node must be revised if the executable implementation cannot
simultaneously preserve source identity, signed route-of-origin, wrapper side,
polarity mirror, alphabet inversion, route reversal, and exact inverse
reconstruction without ambiguity.
