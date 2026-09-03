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

> **Authoritative lock:** `RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md`. Rabbit
> Hopping is both an addressing system and a system-communication translator.
> Its three-route grammar, mandatory wrappers, coupled alphabet/vertical
> inversion, and open division boundary supersede older shorthand in this node.

**Dependencies**  
Upstream: A-101 Ground / Zero, A-103 Differential, A-111 Recursion, B-205 Mirror, B-222 Oscillation Center, B-223 Three Moves, G-716 One-Wave Conversion Grammar  
Lateral: E-510 Music Clock / Harmonic Oscillation, G-719 Neural System Functional Analogy Map, G-720 No Control But Self-Control  
Downstream: G-721a Fibonacci reference validation, G-721b Sturmian branch grammar, G-721c episturmian routing, G-721d Arnoux-Rauzy validation, G-721e plastic/Padovan rail grammar, Wave Computer route compilation, Android procedural movement, Goblin embodied-agent simulation

## Purpose

The mirrored alphabet algorithm converts letters and words into ordered, reversible coordinate paths. It is an address/translator grammar. It does not claim that different physical or software systems are identical; it gives them a common relational map that can be tested for translation.

The separation remains mandatory:

\[
\boxed{\text{Hopfield/Boltzmann}=\text{memory relationships}}
\]

\[
\boxed{\text{rabbit-hop map}=\text{identity, nesting, parity, and reversible coordinates}}
\]

\[
\boxed{\text{wheel system}=\text{live oscillating movement geometry}}
\]

\[
\boxed{-1(0)+1=\text{foundational live choice}}
\]

## Alphabet Map

For the forward alphabet:

\[
A=1,\quad B=2,\quad \ldots,\quad Z=26.
\]

For the inverted alphabet:

\[
Z=1,\quad Y=2,\quad \ldots,\quad A=26.
\]

For any forward rank \(N\in\{1,\ldots,26\}\), the inverted rank is

\[
\boxed{N_{inv}=27-N}.
\]

Thus A is 1 forward and 26 inverted; Z is 26 forward and 1 inverted.

These are alphabet ranks used as source addresses. A later generated top
coordinate belongs to that source address; it does not make the letter equal to
the top coordinate.

## N-Only Rabbit-Hop Grammar

The canonical arithmetic is written only in terms of \(N\) and literal offsets. No auxiliary anchor symbols are required.

### 1. Original route and ascending-after ladder

The original `N×2` route stays a separate receipt. The ascending-after route
uses positive `K=1,2,3,...` after doubling:

\[
\boxed{2N,\;2N+1,\;2N+2,\;2N+3,\;2N+4,\;2N+5,\ldots}
\]

In general:

\[
\boxed{R_{after}(N,K)=2N+K},\qquad K\in\{1,2,3,\ldots\}.
\]

### 2. Ascending-before ladder

Move the input first by positive `K`, then double:

\[
\boxed{2N,\;2(N+1),\;2(N+2),\;2(N+3),\;2(N+4),\ldots}
\]

In general:

\[
\boxed{R_{before}(N,K)=2(N+K)},\qquad K\in\{1,2,3,\ldots\}.
\]

These two ladders can reach the same address by different operation orderings. The exact identity is

\[
\boxed{2N+2m=2(N+m)}.
\]

This identity is the canonical "two ways to get to the same thing" relation. A receipt must retain which route was used even when the numerical destination is equal.

### 3. Opposite-parity wrapper

Every selected top address \(X\) is connected to the opposite parity by both
complete packets:

\[
\boxed{N,\;X,\;X-1}
\qquad\text{or}\qquad
\boxed{N,\;X,\;X+1}.
\]

The final wrapper is mandatory. The bare top address is used to calculate the
packet but is not a third wrapper choice.

If \(X\) is even, \(X\pm1\) are odd. If \(X\) is odd, \(X\pm1\) are even.

Applied to the double-first ladder:

\[
\boxed{(2N+m)-1,\;2N+m,\;(2N+m)+1}.
\]

Applied to the shift-first ladder:

\[
\boxed{2(N+m)-1,\;2(N+m),\;2(N+m)+1}.
\]

The wrapper is structural: it lets adjacent nested packets share an address and therefore connect in either direction.

For example, when \(N=1\):

\[
3,4,5
\]

followed by

\[
5,6,7
\]

shares the value 5. Algebraically:

\[
\boxed{2N+1=2(N+1)-1}.
\]

Likewise an odd center can be wrapped by evens:

\[
2,3,4
\]

then

\[
4,5,6
\]

so the parity of the center may alternate while the neighboring wrapper always uses the opposite parity.

## Signed / Mirrored Form

Polarity is independent of alphabet orientation. A complete signed address may be reflected through zero:

\[
\boxed{X\mapsto -X}.
\]

Therefore each rabbit-hop family has positive and negative forms:

\[
\boxed{\pm(2N+m)}
\]

and

\[
\boxed{\pm 2(N+m)}.
\]

The wrapper follows the selected signed center. Sign mirroring changes polarity; it does not by itself invert alphabet rank or reverse traversal order.

## Mirrored, Inverted, and Opposing Operations

Three operations must remain distinguishable:

1. **Mirrored** — change sign/polarity: \(X\mapsto-X\).
2. **Inverted** — reverse alphabet rank: \(N\mapsto27-N\).
3. **Opposing** — traverse the declared route in the reverse direction while preserving the same address grammar.

They may be composed, but none is silently substituted for another.

Inverting the alphabet axis also inverts logical up/down: the numeric
`-1/+1` sides assigned to logical lower/upper swap together with the alphabet
orientation.

## Mechanical Division Check / Broader Role Open

The identities below mechanically verify a fully attributed receipt. The
broader role of division is unresolved and must not be described as locked
Rabbit Hopping theory.

For the double-first family

\[
X=2N+m,
\]

recover \(N\) exactly by

\[
\boxed{N=\frac{X-m}{2}}.
\]

For the shift-first family

\[
X=2(N+m),
\]

recover \(N\) exactly by

\[
\boxed{N=\frac{X}{2}-m}.
\]

If a wrapper is present, remove the declared wrapper first. For

\[
X=2(N+m)+s,\qquad s\in\{-1,+1\},
\]

the inverse is

\[
\boxed{N=\frac{X-s}{2}-m}.
\]

For

\[
X=2N+m+s,
\]

the inverse is

\[
\boxed{N=\frac{X-m-s}{2}}.
\]

A reversible receipt therefore stores at minimum:

- alphabet orientation (forward or inverted);
- sign/polarity;
- whether the route was double-first or shift-first;
- integer offset \(m\);
- wrapper side \(s\in\{-1,+1\}\), required on every packet;
- resulting address.

Without those route facts, equal numerical destinations such as \(2N+2m=2(N+m)\) cannot reveal which path produced them.

## Point -> Path -> Field Nesting Interpretation

The arithmetic can be used as a nested routing map:

\[
\boxed{\text{Point}_N\rightarrow\text{Path}_N\rightarrow\text{Field}_N\rightarrow\text{next nested address}}
\]

The shared \(\pm1\) boundary is the handoff between neighboring nests. The next layer changes the reference from \(N\) to \(N+1\) while preserving a reversible connection to the preceding layer.

This is a translator interpretation. Whether a particular target domain (software state, memory, music, motion, physics, or another system) is faithfully represented by this grammar must be tested separately in that domain.

## Word-to-Path Compilation

For a word, first map each letter to its declared forward or inverted alphabet rank \(N_t\). For every step choose and record:

- polarity \(\sigma_t\in\{-1,+1\}\);
- route family: double-first or shift-first;
- integer offset \(m_t\);
- wrapper \(s_t\in\{-1,+1\}\).

Double-first:

\[
\boxed{X_t=\sigma_t(2N_t+m_t+s_t)}.
\]

Shift-first:

\[
\boxed{X_t=\sigma_t(2(N_t+m_t)+s_t)}.
\]

The hop between consecutive addresses is

\[
\boxed{\Delta X_t=X_{t+1}-X_t}.
\]

A route may move forward or backward. Reversal reverses the ordered receipt sequence; it does not silently change sign, alphabet inversion, or wrapper side.

## Relationship to Choice

The alphabet/rabbit-hop translator does not make foundational choice. It supplies a coordinate and candidate route.

The operating order remains:

```text
symbolic cue
-> alphabet coordinate
-> reversible rabbit-hop route
-> live -1(0)+1 choice
-> top-down validation / permission
-> committed movement
```

A stored sequence may schedule or validate a route. It may not force live movement when the choice or sensory layer selects Hold.

## Validation Requirements

A valid implementation of this generalized grammar must verify:

1. alphabet rank is in 1..26;
2. inverted alphabet obeys \(N_{inv}=27-N\);
3. double-first addresses obey \(X=2N+m\);
4. shift-first addresses obey \(X=2(N+m)\);
5. equal-destination cases obey \(2N+2m=2(N+m)\);
6. every packet ends in exactly a \(-1\) or \(+1\) wrapper around its declared
   top address;
7. wrapper parity is opposite the center parity when \(s=\pm1\);
8. adjacent declared nests preserve their shared boundary when one exists;
9. positive and negative forms are exact sign mirrors;
10. mirror, inversion, and opposing traversal remain separately declared;
11. the declared inverse division reconstructs the original \(N\) exactly;
12. receipts preserve route family and offset so equal numerical destinations remain distinguishable;
13. Mirror-Gate zero is never confused with route token zero or a top address;
14. alphabet, memory, wheel, and live-choice systems remain separate layers.

## Failure Conditions

The grammar fails when:

- parentheses are dropped so operation order changes;
- two numerically equal destinations are treated as proof that their routes were identical;
- division is used without first removing the declared offset/wrapper;
- parity wrapper metadata is discarded;
- mirroring is silently treated as alphabet inversion;
- reversal silently changes polarity;
- route arithmetic is presented as already proving a physical mechanism;
- a later ratio is used to alter an earlier packet after the fact.

## Falsifier

This node must be revised if an implementation cannot simultaneously preserve address identity, route-of-origin, sign mirror, alphabet inversion, route reversal, opposite-parity wrapping, and exact division-based reconstruction without ambiguity.
