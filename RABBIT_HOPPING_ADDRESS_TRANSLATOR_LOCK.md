# Rabbit Hopping Address and System-Communication Translator — Locked Core

## Canonical status

Rabbit Hopping is a reversible addressing / translation grammar. The numerical
route grammar is label-independent and lives in one shared implementation.
Alphabet, music, guitar-neck, scale, memory, movement, and lattice layers are
**adapters** over that core; they do not get separate arithmetic rules.

Locked now:

- complete `source | TOP | wrapper` packet shape;
- three operation-order route receipts;
- signed integer `K`, including negative, zero, and positive offsets;
- mandatory `TOP-1` and `TOP+1` wrappers around every selected top;
- route-of-origin preservation when two routes reach the same number;
- exact inverse/rebuild arithmetic from a complete receipt;
- polarity and forward/reverse traversal as independent receipt fields;
- alphabet A-Z / Z-A orientation and coupled logical up/down inversion;
- bounded `1..12 -> 12..24` outward/inward scale rail;
- executable music / Circle-of-Fifths and 6-string / 24-fret adapters.

Open unless separately locked:

- a broader physical interpretation of division beyond the declared routing
  uses;
- any claim that two translated domains are physically identical;
- any new route family not explicitly added here with inverse tests.

## One numerical core

Authoritative arithmetic implementation:

```text
One_Wave_Bench/brain/rabbit_hop_core.py
```

All domain adapters import its shared:

```text
RouteFamily
WrapperSide
MirrorPolarity
TraversalDirection
```

Do not copy the formulas into a new domain and let them drift. Add an adapter
that maps the domain's labels/coordinates to this core.

## Complete packet

Every complete packet is:

```text
source identity | generated TOP | wrapper address
```

The source identity does not become the generated number.

The operations occur in this order:

1. identify source rank `N`;
2. calculate a TOP using the declared route family and signed `K`;
3. select exactly one final connector `s`, where `s=-1` or `s=+1`;
4. preserve all route fields so the source can be rebuilt exactly.

**Top offset and wrapper are different operations.**

For example, `2N+1` changes the TOP. That is not the same operation as taking
the `+1` wrapper around TOP `2N`.

Every selected top has exactly two complete connector packets:

```text
N | TOP | TOP-1
N | TOP | TOP+1
```

There is no bare complete packet and no zero-wrapper option.

## Three canonical route receipts

Let `N` be the adapter source rank, `K` any integer, and `s` the final wrapper
side `-1` or `+1`.

| Route | TOP | Complete numeric packet | K domain |
|---|---|---|---|
| `ORIGINAL` | `2N` | `N | 2N | 2N+s` | exactly `0` |
| `DOUBLE_THEN_SHIFT` | `2N+K` | `N | 2N+K | 2N+K+s` | all integers |
| `SHIFT_THEN_DOUBLE` | `2(N+K)` | `N | 2(N+K) | 2(N+K)+s` | all integers |

Historical names are retained only as executable aliases:

```text
ASCENDING_AFTER  == DOUBLE_THEN_SHIFT
ASCENDING_BEFORE == SHIFT_THEN_DOUBLE
```

They no longer imply positive-only `K`.

Equivalent compact forms:

```text
V_K^s(N) = 2N + K + s
U_K^s(N) = 2(N+K) + s
```

where:

```text
K ∈ integers
s ∈ {-1,+1}
```

## Explicit signed local families

The required double-then-shift run includes:

```text
2N-3
2N-2
2N-1
2N
2N+1
2N+2
2N+3
```

and continues in both directions with no artificial endpoint.

The required shift-then-double run includes:

```text
2(N-3)
2(N-2)
2(N-1)
2N
2(N+1)
2(N+2)
2(N+3)
```

and likewise continues in both directions.

**Every line gets both `TOP-1` and `TOP+1` wrappers.**

For `N=1`, double then shift with `K=-3..+3` produces TOPs:

```text
-1, 0, 1, 2, 3, 4, 5
```

For `N=1`, shift then double with `K=-3..+3` produces TOPs:

```text
-4, -2, 0, 2, 4, 6, 8
```

## Equal number does not erase route

Operation order is part of the address receipt.

Example:

```text
2N + 2 = 2(N + 1)
```

These can have the same numerical destination while remaining different
routes:

```text
DOUBLE_THEN_SHIFT, K=2
SHIFT_THEN_DOUBLE, K=1
```

The route family and `K` stay attached to the receipt.

Shared numeric addresses are useful connectors. They are not permission to
collapse route history.

## Exact inverse / rebuild

Remove the declared final wrapper first, then reverse the declared operation
order.

Double then shift:

```text
X = 2N + K + s
N = (X - K - s) / 2
```

Shift then double:

```text
X = 2(N+K) + s
N = (X - s) / 2 - K
```

This is implemented in the shared numerical core and used by the domain
adapters.

## Operator-direction convention

For the declared routing interpretation:

```text
×  project / expand / send outward
÷  route back / locate / rebuild inward
+K shift one signed direction
-K shift the opposing signed direction
±1 select the final connector around the chosen TOP
```

Example:

```text
forward:
N -> ×2 -> +3 TOP shift -> +1 wrapper -> X

rebuild:
X -> -1 wrapper -> -3 TOP shift -> ÷2 -> N
```

Changing operation order changes the route receipt.

## Alphabet adapter

Executable adapter:

```text
One_Wave_Bench/brain/rabbit_hop_alphabet.py
```

Alphabet orientations:

```text
normal:   A -> Z carries source ranks 1 -> 26
inverted: Z -> A carries source ranks 1 -> 26
```

Whole-run Mirror Gate layouts remain:

```text
A-Z(0)Z-A
Z-A(0)A-Z
```

Zero is between whole alphabet runs, not a wrapper and not a letter packet.

Alphabet inversion also inverts logical up/down wrapper assignment while
numeric polarity remains a separate field.

These receipt dimensions remain distinct:

- alphabet orientation;
- route family;
- signed `K`;
- wrapper side;
- polarity;
- traversal direction.

## Music / Circle-of-Fifths adapter

Executable adapter:

```text
One_Wave_Bench/brain/rabbit_hop_music.py
```

The declared chromatic source mapping is 1..12:

```text
1  C
2  C#/Db
3  D
4  D#/Eb
5  E
6  F
7  F#/Gb
8  G
9  G#/Ab
10 A
11 A#/Bb
12 B
```

Enharmonic spellings share pitch-class identity while display spelling can use
sharps or flats.

Circle-of-Fifths traversal is implemented as pitch-class movement:

```text
forward = +7 semitones mod 12
reverse = -7 semitones mod 12
```

Each fifth-position can be compiled through **any** canonical Rabbit-Hop route,
including negative/positive `K` and both wrappers.

Project span conventions remain explicitly separated from standard music facts:

```text
major: -5(0)+4
minor: -5(0)+3
FLIP: (-a,0,+b) -> (-b,0,+a)
```

See:

```text
RABBIT_HOPPING_MUSIC_ADAPTER.md
```

## Six-string / 24-fret neck adapter

Executable adapter:

```text
One_Wave_Bench/brain/rabbit_hop_neck.py
```

Default standard-guitar labels:

```text
6 E
5 A
4 D
3 G
2 B
1 E
```

The default map covers fret `0..24` inclusive. Every string/fret position
resolves to one of the 12 pitch classes, then uses the same Rabbit-Hop core.
The neck is a domain-label adapter and does not replace the numerical scale
rail.

## Locked bounded scale / division rail

Executable adapter:

```text
One_Wave_Bench/brain/rabbit_hop_scale_rail.py
```

Declared domains:

```text
outward source domain: 1..12
inward address domain: 12..24
```

Even inward addresses divide directly:

```text
12 -> 6
14 -> 7
16 -> 8
18 -> 9
20 -> 10
22 -> 11
24 -> 12
```

Odd addresses are shared wrappers and return both neighboring sources:

```text
13 -> 6,7
15 -> 7,8
17 -> 8,9
19 -> 9,10
21 -> 10,11
23 -> 11,12
```

No fractional source address is invented for the odd wrapper positions.

## Executable layout and regression locks

```text
One_Wave_Bench/brain/
├── rabbit_hop_core.py
├── test_rabbit_hop_core.py
├── rabbit_hop_alphabet.py
├── test_rabbit_hop_alphabet.py
├── rabbit_hop_music.py
├── test_rabbit_hop_music.py
├── rabbit_hop_neck.py
├── test_rabbit_hop_neck.py
├── rabbit_hop_scale_rail.py
└── test_rabbit_hop_scale_rail.py
```

Regression requirements include:

- `K=-3,-2,-1,0,+1,+2,+3` on both generalized route families;
- larger signed K values to prove +/-3 is not an endpoint;
- both wrappers around every selected top;
- top offset and wrapper stored separately;
- equal numeric destinations retain distinct route receipts;
- exact reverse reconstruction;
- polarity and traversal independence;
- A-Z / Z-A alphabet round trips;
- enharmonic music identity;
- forward and reverse Circle-of-Fifths traversal;
- all 12 pitch classes on a 6-string open-through-24-fret map;
- bounded 12..24 division-rail reconstruction.

## Adapter rule for Codex

When adding memory, lattice, movement, or another target domain:

1. import `rabbit_hop_core.py`;
2. map the domain label to a source rank / identity;
3. preserve the full route receipt;
4. provide exact reverse reconstruction where applicable;
5. add round-trip tests;
6. do **not** silently create a fourth route family or duplicate the arithmetic.

A translator mapping is a tested coordinate relationship. It is not, by
itself, evidence that two physical systems are the same thing.
