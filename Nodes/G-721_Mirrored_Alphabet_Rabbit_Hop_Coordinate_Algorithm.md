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

The positive coordinate packet is

\[
\boxed{C_{+}(n)=(n,2n,2n+1)}.
\]

The negative mirror is

\[
\boxed{C_{-}(n)=(-n,-2n,-(2n+1))}.
\]

Examples:

\[
C_{+}(A)=(1,2,3),\qquad C_{-}(A)=(-1,-2,-3),
\]

\[
C_{+}(Z)=(26,52,53),\qquad C_{-}(Z)=(-26,-52,-53).
\]

## Coordinate Rails

Each packet preserves three related values:

1. **identity/location rail:** \(n\);
2. **even recursive rail:** \(2n\);
3. **odd recursive rail:** \(2n+1\).

The packet must remain intact even when one recursive branch is selected for a particular hop. Selecting \(2n\) or \(2n+1\) does not erase the unused coordinate.

## Two-Axis Structure

The coordinate system has two distinct axes.

### Direction and location axis

The letter index identifies location in the A-to-Z order. The side of the Mirror Gate determines sign, direction, or mirrored location.

### Recursive/state axis

The relations

\[
n\rightarrow2n,
\qquad
n\rightarrow2n+1
\]

identify the two recursive branches attached to the letter's identity coordinate.

These axes must not be collapsed. A sign change does not alter the letter identity, and a recursive-branch change does not automatically reverse traversal direction.

## Mirror Gate

The Mirror Gate is the shared zero boundary:

\[
\boxed{-\;\;(0)\;\;+}.
\]

Crossing the gate changes side or polarity. It does not delete the coordinate packet.

Two valid layout classes are retained:

### Recursive mirror layout

The same alphabet order is preserved across opposite signs:

```text
-Z ... -A (0) +A ... +Z
```

or numerically:

```text
-26 ... -1 (0) +1 ... +26
```

### Direction/location mirror layout

The alphabet traversal is opposed across the gate:

```text
-A ... -Z (0) +Z ... +A
```

or numerically:

```text
-1 ... -26 (0) +26 ... +1
```

Every generated path must declare which layout it uses.

## Word-to-Path Compilation

For a word with letter indices

\[
\mathbf n=(n_0,n_1,\ldots,n_{m-1}),
\]

and mirror signs

\[
\boldsymbol\sigma=(\sigma_0,\sigma_1,\ldots,\sigma_{m-1}),
\qquad
\sigma_t\in\{-1,+1\},
\]

the full packet path is

\[
\mathbf C_t
=
\sigma_t(n_t,2n_t,2n_t+1).
\]

The packet differential between consecutive letters is

\[
\Delta\mathbf C_t
=
\mathbf C_{t+1}-\mathbf C_t.
\]

This differential is the machine-readable rabbit hop between symbolic addresses.

## Recursive-Branch Trace

When a run commits one recursive branch for letter \(n_t\), record the selected coordinate as

\[
r_t=\sigma_t(2n_t+b_t),
\qquad
b_t\in\{0,1\}.
\]

The branch symbol can be recovered from the signed coordinate without losing mirror information:

\[
\boxed{b_t=|r_t|-2|n_t|}.
\]

A valid packet branch must satisfy

\[
b_t\in\{0,1\}.
\]

Thus:

- \(b_t=0\) selects the even recursive rail \(2n_t\);
- \(b_t=1\) selects the odd recursive rail \(2n_t+1\).

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
2. every packet equals \(\pm(n,2n,2n+1)\);
3. every selected recursive coordinate gives \(b_t\in\{0,1\}\);
4. forward and reverse paths are exact reversals;
5. positive and negative paths are exact sign mirrors;
6. Mirror-Gate zero is never confused with branch symbol zero;
7. branch traces are passed to the declared G-721a through G-721e validator or scheduler without post-hoc reordering;
8. the alphabet, memory, and wheel systems remain separate.

## Failure Conditions

The algorithm fails when:

- a packet value is changed to improve a later ratio;
- a branch symbol is inferred from sign rather than \(2n\) versus \(2n+1\);
- branch zero is treated as the Mirror Gate;
- reversing a path silently complements its branch symbols;
- the coordinate grammar is presented as the live movement mechanism;
- a Fibonacci match is claimed after sorting or deleting inconvenient hops.

## Falsifier

This node must be revised if a compiled implementation cannot preserve packet identity, sign mirror, route reversal, and branch recovery simultaneously without ambiguity.
