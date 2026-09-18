# Codex Latest Translator Handoff

Read this before changing Rabbit Hopping, alphabet translation, musical-note
translation, Circle of Fifths, guitar-neck mapping, the 12/24 scale rail, or a
new memory/lattice/movement adapter.

## Source of truth order

1. `RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md`
2. `One_Wave_Bench/brain/rabbit_hop_core.py`
3. the relevant domain adapter and its tests
4. `Nodes/G-721_Mirrored_Alphabet_Rabbit_Hop_Coordinate_Algorithm.md`
5. `RABBIT_HOPPING_MUSIC_ADAPTER.md` for music/neck details

If older shorthand conflicts with #1 or #2, the lock/core wins.

## Shared route core

Do not create another copy of the arithmetic.

```text
One_Wave_Bench/brain/rabbit_hop_core.py
```

Canonical routes:

```text
ORIGINAL
TOP = 2N
K = 0

DOUBLE_THEN_SHIFT
TOP = 2N + K
K = any integer

SHIFT_THEN_DOUBLE
TOP = 2(N + K)
K = any integer
```

Every selected TOP separately receives both connector packets:

```text
N | TOP | TOP-1
N | TOP | TOP+1
```

`K` and wrapper `±1` are different receipt fields.

The explicit local family that must remain covered is:

```text
K = -3, -2, -1, 0, +1, +2, +3
```

but +/-3 is not an endpoint. Larger signed values must continue to work.

Exact reverse:

```text
X = 2N + K + s
N = (X-K-s)/2

X = 2(N+K) + s
N = (X-s)/2-K
```

Equal numerical destination does not erase operation order or route receipt.

## Executable adapters

```text
One_Wave_Bench/brain/rabbit_hop_alphabet.py
One_Wave_Bench/brain/test_rabbit_hop_alphabet.py

One_Wave_Bench/brain/rabbit_hop_music.py
One_Wave_Bench/brain/test_rabbit_hop_music.py

One_Wave_Bench/brain/rabbit_hop_neck.py
One_Wave_Bench/brain/test_rabbit_hop_neck.py

One_Wave_Bench/brain/rabbit_hop_scale_rail.py
One_Wave_Bench/brain/test_rabbit_hop_scale_rail.py
```

All of these must use the shared core route types/math.

## Music adapter

Locked implementation includes:

- 12 pitch classes;
- sharp/flat enharmonic aliases;
- chromatic source ranks 1..12;
- forward Circle of Fifths `+7 mod 12`;
- reverse Circle of Fifths `-7 mod 12`;
- every fifth-position can compile to any Rabbit-Hop route;
- One-Wave project spans kept explicitly separate from standard music facts:
  - major `-5(0)+4`
  - minor `-5(0)+3`
  - `FLIP(-a,0,+b) = (-b,0,+a)`.

## Neck adapter

Concrete standard-guitar labeling adapter:

```text
6 E
5 A
4 D
3 G
2 B
1 E
```

Default map is open position through fret 24 inclusive. Every position resolves
to one of the 12 pitch classes and then uses the shared Rabbit-Hop route core.

## Scale / division rail

Keep the narrower historical rail distinct from the generic inverse:

```text
outward source: 1..12
inward address: 12..24
```

Even inward address -> direct `/2` source.
Odd inward address -> both neighboring even TOP sources through wrapper
structure; do not invent half-source addresses.

## Adding a new translator domain

For memory, lattice, movement, or another domain:

1. map domain identity to an explicit source coordinate/rank;
2. call `rabbit_hop_core.py`;
3. preserve route family, signed K, wrapper, polarity, traversal, TOP, and
   wrapper address;
4. provide an inverse mapping when the domain is intended to round-trip;
5. add tests for `K=-3..+3`, at least one larger negative and positive K, both
   wrappers, equal-destination/different-route cases, and reverse recovery;
6. do not silently add a new route family;
7. keep translation evidence separate from physical-theory claims.

## Current implementation layout

```text
Rabbit-Hop core
├── Alphabet: A-Z / Z-A
├── Music: chromatic / enharmonic / Circle of Fifths
├── Neck: 6 strings / 12 pitch classes / 0..24 frets
└── Scale rail: 1..12 outward / 12..24 inward

Next compatible adapters
├── memory / recall
├── lattice addressing / frame routes
└── movement / state-machine routing
```
