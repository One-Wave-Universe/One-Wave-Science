# Rabbit Hopping Address and System-Communication Translator — Locked Core

## Status

- **Locked now:** purpose, packet shape, the complete signed-K route grammar,
  mandatory `TOP-1` / `TOP+1` wrappers, route receipts, alphabet inversion,
  coupled vertical inversion, polarity, and forward/reverse traversal.
- **Locked division rail:** sources `1–12` generate outward; addresses `12–24`
  are read inward by division as defined below.
- **Open:** any broader role of division outside that bounded rail and any claim
  that a target domain is physically equivalent to this arithmetic.
- **Adapter rule:** alphabet, music, neck/fret, memory, movement, and lattice
  adapters may use this grammar, but they must preserve their own domain
  identity and must not erase the Rabbit-Hop route receipt.

## Purpose

Rabbit Hopping is both:

1. an addressing system; and
2. a system-communication translator.

The address packet preserves how an address was produced so it can cross a
system boundary without losing source identity, operation order, signed offset,
wrapper, orientation, polarity, or traversal direction.

## Complete packet

Every complete packet has exactly this semantic shape:

`source identity | generated top address | wrapper address`

The source identity does not become the generated number. For example, normal
`A` carries source rank `1`; a packet `1 | 5 | 4` means that source produced top
address `5` and then selected the lower connector `4`.

### Top offset and wrapper are different operations

This distinction is mandatory.

1. First calculate the **top** using the selected route family and signed `K`.
2. Then attach one of the two mandatory **wrappers** around that top.

Every top has exactly these two complete packets:

- `source | TOP | TOP-1`
- `source | TOP | TOP+1`

There is no bare packet and no zero-wrapper option. An odd top has even
wrappers; an even top has odd wrappers.

A route such as `N×2+1` is therefore **not** the same operation as selecting the
`+1` wrapper around `N×2`. The first `+1` changes the top; the wrapper is a
second operation applied after the top exists.

## Complete signed-K route grammar

Let `N` be the source rank, `K` any integer, and `s` the mandatory connector
side `-1` or `+1`.

| Canonical route receipt | Top-address rule | Complete packet | K domain |
|---|---|---|---|
| `ORIGINAL` | `2N` | `N | 2N | 2N+s` | exactly `0` |
| `DOUBLE_THEN_SHIFT` | `2N+K` | `N | 2N+K | 2N+K+s` | all integers |
| `SHIFT_THEN_DOUBLE` | `2(N+K)` | `N | 2(N+K) | 2(N+K)+s` | all integers |

Historical names `ASCENDING_AFTER` and `ASCENDING_BEFORE` remain executable
aliases for compatibility, but `K` is no longer restricted to ascending
positive values.

The two generalized families are therefore:

`V_K^s(N) = 2N + K + s`

`U_K^s(N) = 2(N + K) + s`

where `K ∈ Z` and `s ∈ {-1,+1}`.

### Explicit local run

Around any source `N`, the double-then-shift tops include:

```text
2N-3
2N-2
2N-1
2N
2N+1
2N+2
2N+3
```

and continue without an artificial endpoint. Every line above separately gets
`TOP-1` and `TOP+1` wrappers.

The shift-then-double tops include:

```text
2(N-3)
2(N-2)
2(N-1)
2N
2(N+1)
2(N+2)
2(N+3)
```

and likewise continue in both directions, with both wrappers around every top.

### Example for normal A (`N=1`)

Double then shift:

| K | Top | Complete packets |
|---:|---:|---|
| -3 | -1 | `1|-1|-2`, `1|-1|0` |
| -2 | 0 | `1|0|-1`, `1|0|1` |
| -1 | 1 | `1|1|0`, `1|1|2` |
| 0 | 2 | `1|2|1`, `1|2|3` |
| +1 | 3 | `1|3|2`, `1|3|4` |
| +2 | 4 | `1|4|3`, `1|4|5` |
| +3 | 5 | `1|5|4`, `1|5|6` |

Shift then double:

| K | Top | Complete packets |
|---:|---:|---|
| -3 | -4 | `1|-4|-5`, `1|-4|-3` |
| -2 | -2 | `1|-2|-3`, `1|-2|-1` |
| -1 | 0 | `1|0|-1`, `1|0|1` |
| 0 | 2 | `1|2|1`, `1|2|3` |
| +1 | 4 | `1|4|3`, `1|4|5` |
| +2 | 6 | `1|6|5`, `1|6|7` |
| +3 | 8 | `1|8|7`, `1|8|9` |

## Same number does not mean same route

Operation order is part of identity.

For example:

`2N + 2 = 2(N + 1)`

The numerical destination may be equal, but one receipt says
`DOUBLE_THEN_SHIFT, K=2` and the other says `SHIFT_THEN_DOUBLE, K=1`.
They must remain distinguishable.

Likewise, intersections caused by wrappers do not erase route history. Shared
addresses are connectors, not permission to collapse the generating paths.

## Wrappers are the connectors

Wrappers connect packets regardless of route family or traversal direction.
Top `4` carries wrappers `3` and `5`; top `5` carries wrappers `4` and `6`.
Those packets can hand off through shared top/wrapper addresses. Tops `4` and
`6` share wrapper `5`.

The retained route receipt prevents equal numeric addresses from erasing how
they were reached.

## Alphabet orientation and coupled inversion

The alphabet can be traversed in either orientation:

| Orientation | Rank run | Original-route endpoints |
|---|---|---|
| normal | `A→Z` carries `1→26` | `A` top `2`; `Z` top `52` |
| inverted | `Z→A` carries `1→26` | `Z` top `2`; `A` top `52` |

Whole-run Mirror Gate layouts are `A-Z(0)Z-A` and `Z-A(0)A-Z`. Zero sits
between whole alphabet runs, not inside a letter packet.

Side-to-side alphabet inversion also inverts logical up/down. On the normal
axis, top `2` has logical lower wrapper `1` and upper wrapper `3`. On the
inverted axis, top `2` has logical lower wrapper `3` and upper wrapper `1`.

These receipt fields stay distinct:

- alphabet orientation: normal or inverted;
- route family;
- signed integer `K`;
- wrapper side `s=-1/+1`;
- vertical logical side, coupled to alphabet orientation;
- polarity: positive or negative numeric mirror;
- traversal direction: forward or reverse route order.

Reversing traversal does not silently change polarity, route family, `K`, or
wrapper side.

## Exact inverse / rebuild arithmetic

The full receipt makes both generalized families mechanically reversible.
Remove the declared wrapper first.

For double then shift:

`X = 2N + K + s`

therefore:

`N = (X - K - s) / 2`

For shift then double:

`X = 2(N + K) + s`

therefore:

`N = (X - s) / 2 - K`

This is the translator's exact reconstruction rule. It does not by itself lock
a broader physical interpretation of division.

## Multiplication / division direction

Within the declared scale-routing interpretation:

- `×` projects / expands / sends outward;
- `÷` routes back / locates / rebuilds inward;
- `+K` shifts one signed direction;
- `-K` shifts the opposing signed direction;
- `s=±1` selects the final connector around the chosen top.

A complete example is:

```text
forward: N -> ×2 -> +3 top shift -> +1 wrapper -> X
rebuild: X -> -1 wrapper -> -3 top shift -> ÷2 -> N
```

Changing the order changes the route receipt.

## Locked bounded division rail

The declared bounded rail uses two domains:

- outward source domain: `1–12`;
- inward division-address domain: `12–24`.

For an even address `X` in `12–24`, `X÷2` identifies its source. For an odd
address, division uses the wrapper structure rather than creating a fractional
address: `(X-1)÷2` and `(X+1)÷2` identify the two neighboring connected
sources.

| Outer address | Inward source address(es) |
|---:|---:|
| 12 | 6 |
| 13 | 6, 7 |
| 14 | 7 |
| 15 | 7, 8 |
| 16 | 8 |
| 17 | 8, 9 |
| 18 | 9 |
| 19 | 9, 10 |
| 20 | 10 |
| 21 | 10, 11 |
| 22 | 11 |
| 23 | 11, 12 |
| 24 | 12 |

The larger role of division beyond this bounded scale rail remains open unless
another explicit lock defines it.

## Adapter boundary

The Rabbit-Hop grammar is label-independent. Domain adapters may map labels to
source identities and route receipts, but must not redefine the arithmetic.

Expected adapters include:

```text
Rabbit-Hop core
├── Alphabet
│   ├── A -> Z
│   └── Z -> A
├── Music
│   ├── 12 pitch classes / chromatic order
│   ├── Circle of Fifths traversal
│   ├── major/minor span relationships
│   └── mirrored/inverted traversal
├── Neck / scale
│   ├── 6 strings
│   ├── 12 note classes
│   └── 24-fret / 12-24 division rail
└── Other domains
    ├── memory / recall routing
    ├── movement
    └── lattice addressing
```

Adapters are translators, not proofs that those domains are physically the
same system.

## Executable lock

Reference implementation:

`One_Wave_Bench/brain/rabbit_hop_alphabet.py`

Regression tests:

`One_Wave_Bench/brain/test_rabbit_hop_alphabet.py`

They lock:

- `ORIGINAL = 2N`;
- signed `DOUBLE_THEN_SHIFT = 2N+K` for negative, zero, and positive `K`;
- signed `SHIFT_THEN_DOUBLE = 2(N+K)` for negative, zero, and positive `K`;
- explicit `K=-3,-2,-1,0,+1,+2,+3` local runs;
- both mandatory wrappers around every selected top;
- top-offset and wrapper as separate operations;
- equal numerical destinations retaining different route receipts;
- opposite top/wrapper parity;
- connections within and across route families;
- normal and inverted alphabet endpoints;
- coupled side-to-side and up/down inversion;
- independent polarity and traversal receipts;
- exact mechanical source recovery from a complete receipt.

The historical positive-only `ascending_ladder()` remains as a compatibility
helper; `offset_ladder()` is the canonical signed-K helper.

The bounded division rail remains implemented in:

`One_Wave_Bench/brain/rabbit_hop_scale_rail.py`

with tests in:

`One_Wave_Bench/brain/test_rabbit_hop_scale_rail.py`.
