---
node_id: "G-721"
canonical_name: "Mirrored Alphabet Rabbit-Hop Coordinate Algorithm"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Symbolic Coordinate System / Route Compiler / Movement Address Grammar"
claim_gate_detail: "BRONZE (coordinate packet and mirror grammar) / YELLOW (embodied-motion implementation)"
metadata_standard: "I-06"
---

# Node G-721: Mirrored Alphabet Rabbit-Hop Coordinate Algorithm

**Dependencies**  
Upstream: A-101 Ground / Zero, A-103 Differential, A-111 Recursion, B-205 Mirror, B-222 Oscillation Center, B-223 Three Moves, G-716 One-Wave Conversion Grammar  
Lateral: E-510 Music Clock / Harmonic Oscillation, G-719 Neural System Functional Analogy Map, G-720 No Control But Self-Control  
Downstream: G-721a Fibonacci reference validation, G-721b Sturmian branch grammar, G-721c episturmian routing, G-721d Arnoux-Rauzy validation, G-721e plastic/Padovan rail grammar, Wave Computer route compilation, Android procedural movement, Goblin embodied-agent simulation

## Purpose

The mirrored alphabet algorithm converts letters and words into ordered coordinate paths for Wave Computer and embodied movement routing. It is the coordinate/address layer of the android rabbit-hopping system. It is not the Hopfield/Boltzmann memory system, the wheel-of-fifths movement system, or the foundational live-choice mechanism.

The separation is mandatory:

\[
\boxed{\text{Hopfield/Boltzmann}=\text{memory relationships}}
\]

\[
\boxed{\text{mirrored alphabet}=\text{identity and symbolic coordinates}}
\]

\[
\boxed{\text{wheel system}=\text{live oscillating movement geometry}}
\]

\[
\boxed{-1(0)+1=\text{foundational live choice}}
\]

Binary or two-symbol route patterns may validate, constrain, or index a compiled path from above. They may not replace foundational choice.

## Alphabet Index

For a letter with index

\[
n\in\{1,2,\ldots,26\},
\]

use

\[
A=1,\quad B=2,\quad \ldots,\quad Z=26.
\]

For identity rank `n`, retain two successive even anchors

\[
E_0=2n,\qquad E_1=2(n+1),
\]

and both odd neighbors of each even anchor:

\[
O_j^\pm=E_j\pm1,\qquad j\in\{0,1\}.
\]

The complete positive coordinate family is

\[
\boxed{
C_+(n)=\{
(n,2n,2n-1),
(n,2n,2n+1),
(n,2(n+1),2(n+1)-1),
(n,2(n+1),2(n+1)+1)
\}.
}
\]

The negative family is its exact sign mirror, `C_-(n)=-C_+(n)`
coordinate by coordinate.

Examples:

\[
C_+(A)=\{(1,2,1),(1,2,3),(1,4,3),(1,4,5)\},
\]

\[
C_+(B)=\{(2,4,3),(2,4,5),(2,6,5),(2,6,7)\},
\]

\[
C_+(Z)=\{(26,52,51),(26,52,53),(26,54,53),(26,54,55)\}.
\]

For A, the negative family begins
`(-1,-2,-1), (-1,-2,-3)` and continues
`(-1,-4,-3), (-1,-4,-5)`.

## Coordinate Rails and Shared Bridge

Each selected hop preserves:

1. **identity/location rail:** \(n\);
2. **even-anchor generation:** current `E0=2n` or next `E1=2(n+1)`;
3. **odd side:** lower `E-1` or upper `E+1`.

The upper odd neighbor of the current anchor equals the lower odd neighbor of
the next anchor:

\[
\boxed{2n+1=2(n+1)-1}.
\]

This repeated value is an intentional shared bridge, not a duplicate to
delete. The odd value alone is therefore insufficient to reconstruct a hop;
the receipt must retain its even anchor and lower/upper side.

## Two-Axis Structure

The coordinate system has two distinct axes.

### Direction and location axis

The letter index identifies location in the A-to-Z order. The side of the Mirror Gate determines sign, direction, or mirrored location.

### Recursive/state axis

The relations

\[
n\rightarrow E_j=2(n+j),
\qquad
E_j\rightarrow E_j\pm1
\]

identify the anchor generation and odd side attached to the identity.

These axes must not be collapsed. A sign change does not alter the letter identity, and a recursive-branch change does not automatically reverse traversal direction.

## Mirror Gate

The Mirror Gate is the shared zero boundary:

\[
\boxed{-\;\;(0)\;\;+}.
\]

Crossing the gate changes side or polarity. It does not delete the coordinate packet.

Two valid alphabet-orientation layouts are retained:

### Forward-outward / reverse-return layout

The same alphabet order is preserved across opposite signs:

```text
A ... Z (0) Z ... A
```

### Inverted-outward / forward-return layout

The alphabet traversal is opposed across the gate:

```text
Z ... A (0) A ... Z
```

Every path must separately declare alphabet orientation and coordinate
polarity. Under inverted alphabet orientation,

\[
\boxed{n_{inv}=27-n},
\]

so A has rank 26 and Z has rank 1. Inversion does not imply negative polarity.

## Word-to-Path Compilation

For a word with letter indices

\[
\mathbf n=(n_0,n_1,\ldots,n_{m-1}),
\]

mirror signs, even-anchor generations, and odd sides

\[
\boldsymbol\sigma=(\sigma_0,\sigma_1,\ldots,\sigma_{m-1}),
\qquad
\sigma_t\in\{-1,+1\},
\]

\[
j_t\in\{0,1\},\qquad s_t\in\{-1,+1\},
\]

the full packet path is

\[
\boxed{
\mathbf C_t
=
\sigma_t\left(n_t,2(n_t+j_t),2(n_t+j_t)+s_t\right).
}
\]

The packet differential between consecutive letters is

\[
\Delta\mathbf C_t
=
\mathbf C_{t+1}-\mathbf C_t.
\]

This differential is the machine-readable rabbit hop between symbolic addresses.

## Recursive-Branch Trace

When a run commits one odd side around a declared even anchor, retain the full
triple

\[
(n_t,e_t,o_t)
=
\sigma_t\left(n_t,2(n_t+j_t),2(n_t+j_t)+s_t\right).
\]

Recover anchor generation and binary side token by

\[
\boxed{j_t=\frac{|e_t|}{2}-|n_t|},
\qquad
\boxed{b_t=\frac{|o_t|-|e_t|+1}{2}}.
\]

A valid packet must satisfy

\[
j_t\in\{0,1\},\qquad b_t\in\{0,1\}.
\]

Thus:

- `j=0` selects current even anchor `2n`;
- `j=1` selects next even anchor `2(n+1)`;
- `b=0` selects the lower odd neighbor `e-1`;
- `b=1` selects the upper odd neighbor `e+1`.

The ordered branch trace

\[
\mathbf b=(b_0,b_1,\ldots,b_{m-1})
\]

is available to the declared validator or scheduler family. G-721a is the fixed Fibonacci regression path; G-721b through G-721e test broader branch, route-family, and three-rail grammars.

## Forward, Reverse, and Mirror Rules

The algorithm must preserve all four path views:

1. forward positive path;
2. reverse positive path;
3. forward negative mirror;
4. reverse negative mirror.

Sign mirroring acts on the coordinates:

\[
(n,r)\mapsto(-n,-r).
\]

It does not complement the branch symbol:

\[
b\mapsto b.
\]

Reversing traversal reverses branch order:

\[
(b_0,b_1,\ldots,b_{m-1})
\mapsto
(b_{m-1},\ldots,b_1,b_0).
\]

A complement operation \(0\leftrightarrow1\) is not implied by either sign mirroring or route reversal. It requires a separately declared rule.

## Relationship to Choice

The alphabet algorithm does not make foundational choice. It provides symbolic coordinates and a compiled route candidate.

The operating order is

```text
symbolic cue
-> alphabet coordinate packet
-> candidate recursive branch or route
-> live -1(0)+1 choice
-> top-down validation / permission
-> committed movement
```

A stored Fibonacci word may act as a route template or validation target. It may not force the live system to move when the foundational choice, sensory correction, or safety layer selects Hold.

## Dimensional Declaration

This node is a symbolic coordinate grammar. It is not itself a claim that alphabet coordinates occupy a specific physical dimension.

Any physical implementation must declare:

```text
native dimension
projection dimension
coordinate-to-motion operator
coordination domain
Mirror-Gate implementation
what is omitted by projection
```

The 2D, 3D, and 4D rules of A-117 remain controlling.

## Validation Requirements

A valid implementation must verify:

1. every letter index lies in \(1\ldots26\);
2. every packet equals
   `±(n, 2(n+j), 2(n+j)+s)` for declared `j∈{0,1}`, `s∈{-1,+1}`;
3. every packet recovers legal `j` and `b` values;
4. forward and reverse paths are exact reversals;
5. positive and negative paths are exact sign mirrors;
6. Mirror-Gate zero is never confused with branch symbol zero;
7. branch traces are passed to the declared G-721a through G-721e validator or scheduler without post-hoc reordering;
8. the alphabet, memory, and wheel systems remain separate.

## Failure Conditions

The algorithm fails when:

- a packet value is changed to improve a later ratio;
- a branch symbol is inferred from polarity rather than the odd side of its
  declared even anchor;
- a shared odd bridge is decoded without retaining its anchor generation;
- branch zero is treated as the Mirror Gate;
- reversing a path silently complements its branch symbols;
- the coordinate grammar is presented as the live movement mechanism;
- a Fibonacci match is claimed after sorting or deleting inconvenient hops.

## Falsifier

This node must be revised if a compiled implementation cannot preserve packet identity, sign mirror, route reversal, and branch recovery simultaneously without ambiguity.
