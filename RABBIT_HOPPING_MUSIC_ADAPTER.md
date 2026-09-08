# Rabbit Hopping Music / Circle-of-Fifths Adapter

## Status

This is an executable **domain adapter** over the locked Rabbit-Hop numerical
core. It does not redefine the route grammar and it does not claim that music
and another target domain are physically identical.

## Layering

```text
rabbit_hop_core.py
  signed route arithmetic only
        |
        +-- rabbit_hop_alphabet.py
        |     A-Z / Z-A labels and inversion
        |
        +-- rabbit_hop_music.py
        |     12 pitch classes
        |     sharp / flat aliases
        |     chromatic source ranks 1..12
        |     Circle of Fifths forward / reverse
        |     One-Wave major/minor span convention
        |
        +-- rabbit_hop_neck.py
        |     6 standard guitar strings
        |     12 repeating pitch classes
        |     open through fret 24
        |     every position -> full Rabbit-Hop receipt
        |
        +-- rabbit_hop_scale_rail.py
              bounded 1..12 -> 12..24 outward/inward rail
```

All adapters share the same `RouteFamily`, `WrapperSide`, `MirrorPolarity`, and
`TraversalDirection` definitions from `rabbit_hop_core.py`.

## Rabbit-Hop routes available to every note

For a musical source rank `N`:

```text
ORIGINAL
TOP = 2N

DOUBLE_THEN_SHIFT
TOP = 2N + K

SHIFT_THEN_DOUBLE
TOP = 2(N + K)
```

`K` is any integer. Therefore all of these are directly callable:

```text
2N-3  2N-2  2N-1  2N  2N+1  2N+2  2N+3
```

and:

```text
2(N-3)  2(N-2)  2(N-1)  2N  2(N+1)  2(N+2)  2(N+3)
```

with no artificial stop at +/-3.

Every selected top separately gets exactly two complete connector receipts:

```text
TOP-1
TOP+1
```

The top offset `K` and final connector `s` are never collapsed into one field.

## Exact reverse / division reconstruction

Complete receipt, double then shift:

```text
X = 2N + K + s
N = (X - K - s) / 2
```

Complete receipt, shift then double:

```text
X = 2(N + K) + s
N = (X - s) / 2 - K
```

The music adapter calls the same inverse used by every other domain adapter,
then maps the recovered source rank back to its pitch class.

## Twelve pitch classes

Internal identity is modulo 12. The declared chromatic source-rank adapter is:

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

Enharmonic spellings share pitch-class identity while the display spelling can
be requested as sharps or flats.

## Circle of Fifths

The executable fifth traversal uses pitch-class arithmetic:

```text
forward fifth  = +7 semitones mod 12
reverse fifth  = -7 semitones mod 12
```

Forward from C, sharp display:

```text
C -> G -> D -> A -> E -> B -> F# -> C# -> G# -> D# -> A# -> F -> C
```

Reverse from C, flat display:

```text
C -> F -> Bb -> Eb -> Ab -> Db -> Gb -> B -> E -> A -> D -> G -> C
```

`fifths_rabbit_route()` compiles each pitch-class position directly into the
same complete Rabbit-Hop receipt family. It can therefore use `N*2`,
`N*2+K`, or `(N+K)*2`, including negative and positive K.

## Six strings / 24 frets

`rabbit_hop_neck.py` provides a concrete standard-guitar adapter using normal
string numbering and tuning:

```text
6 E
5 A
4 D
3 G
2 B
1 E
```

The default map covers open position through fret 24 inclusive. Fret 12 returns
the same pitch class one octave up and fret 24 returns it two octaves up. Each
string/fret position resolves to one of the same 12 pitch classes, then calls
`music_wrapper_pair()` so all signed-K routes and both wrappers remain
available.

The neck is a labeling/use adapter. It does not replace the separate locked
numerical `1..12 -> 12..24` scale rail.

## One-Wave span convention

These are retained as **project conventions**, not substituted for standard
music-theory definitions:

```text
major span: -5(0)+4
minor span: -5(0)+3
```

The project FLIP is:

```text
(-a,0,+b) -> (-b,0,+a)
```

Examples:

```text
major  -5(0)+4 -> FLIP -> -4(0)+5
minor  -5(0)+3 -> FLIP -> -3(0)+5
```

On center A these pitch-class coordinates render:

```text
major span -> E, A, C#
minor span -> E, A, C
```

This is a coordinate adapter statement only.

## Executable files

```text
One_Wave_Bench/brain/rabbit_hop_core.py
One_Wave_Bench/brain/test_rabbit_hop_core.py

One_Wave_Bench/brain/rabbit_hop_alphabet.py
One_Wave_Bench/brain/test_rabbit_hop_alphabet.py

One_Wave_Bench/brain/rabbit_hop_music.py
One_Wave_Bench/brain/test_rabbit_hop_music.py

One_Wave_Bench/brain/rabbit_hop_neck.py
One_Wave_Bench/brain/test_rabbit_hop_neck.py

One_Wave_Bench/brain/rabbit_hop_scale_rail.py
One_Wave_Bench/brain/test_rabbit_hop_scale_rail.py
```

## Codex rule

Do not add a separate arithmetic implementation for a new domain. Add a domain
adapter that maps its labels/coordinates to `rabbit_hop_core.py`, preserves the
complete route receipt, and adds round-trip tests.
