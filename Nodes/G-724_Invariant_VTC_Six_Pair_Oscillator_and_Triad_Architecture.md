---
node_id: "G-724"
canonical_name: "Invariant VTC Six-Pair Oscillator and Triad Architecture"
namespace: "NODE"
gate: "GREEN"
lifecycle: "PROPOSED_BUILD"
classification: "Engineering Architecture / Physical Computing Kernel"
claim_gate_detail: "GREEN (internally consistent architecture) / YELLOW (breadboard proof not yet run)"
metadata_standard: "I-06"
---

# Node G-724: Invariant VTC Six-Pair Oscillator and Triad Architecture

**Dependencies**
Upstream: B-206b Four Views, B-206c Four Actions, B-223 Three Moves, B-224 Two Choices, C-301 Mirror Gate
Lateral: G-716 One-Wave Conversion Grammar, G-722 Android Subconscious Motor Memory Architecture
Downstream: G-725 Processing-Is-Memory Connected-Cube Architecture, Proposed Android Brain Ch1 physical substrate

## Purpose

Define the invariant physical-computing kernel (VTC: the voltage/ternary/choice engine) that the recursive One-Wave decision primitives (Views, Actions, Choices, Moves) instantiate in hardware, and protect that kernel from domain-representation drift.

**Anti-drift rule:** if deleting a domain vocabulary (thermal labels, matter labels, Micro/Small/Mid/Large/Macro, etc.) changes the six-pair oscillator itself, the domain representation has leaked into the kernel. The kernel must survive being described in any domain.

## Canonical six-pair oscillator

\[
F_1/V_6 - V_5/F_2 - F_3/V_4 - V_3/F_4 - F_5/V_2 - V_1/F_6 - F_1/V_6\ \cdots
\]

`/` denotes one simultaneous mirrored relation; `-` denotes return to shared `(0)`, a Mirror-Gate crossover and phase shift (C-301). Six coupled operations expose twelve pair-side positions — they are not twelve unrelated serial instructions. The oscillator originates at \(-(0)+\).

Six process steps: `BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP -> BEGIN`.

## Four Views (state) vs. Four Actions (transformation)

Views describe state (B-206b): **Direction, Phase, Strength, Reference.**

Actions transform/route it (B-206c): **Inward, Outward, Across, Over** —

- Inward: signal/relation enters a local cell or returns toward reference.
- Outward: the local cell expresses its resolved relation.
- Across: opposed/mirrored outputs establish a shared differential.
- Over: the resolved differential crosses the connection boundary into the next stage/cluster/scale.

These two sets are never re-merged: Actions are not "Views," and re-collapsing them re-hides the kernel's actual degrees of freedom.

## Two-layer choice: DC engage vs. AC differential

\[
\text{DC decision: EVERYTHING / NOTHING (engage / do not engage)}
\]
\[
\text{AC differential decision: LEFT / STAY / RIGHT}=-1,\,0,\,+1
\]

DC decides whether the operation participates at all; AC/differential resolves direction only if participating. Zero is the balanced/non-action *result*, not a third actively driven DC command.

Five coarse modulation states remain a separate layer: \(-2,-1,0,+1,+2\) (Floor/Low/Middle/High/Ceiling or any other domain labeling — the labels are representation, the five-state structure is kernel).

## Triad and cluster geometry

\[
1\ \text{triad}=2\ \text{linked/opposed mirror elements}+1\ \text{differential evaluator}=3\ \text{active elements},
\]
\[
3\ \text{triads}=9\text{-element base cluster}=3\ \text{physical Mirror Gates},
\]
\[
3\ \text{physical Mirror Gates}\times2\ \text{orientations/phases}=6\ \text{logical pair positions}.
\]

Do not reinterpret this as six physically separate Mirror-Gate devices — it is three physical gates traversed in two phases. Where practical, opposed elements should be one complementary physical switching mechanism (one flips and its mirror flips simultaneously) rather than a controller issuing two sequential commands.

## Signal flow through one computing cell

\[
\text{IN}\rightarrow\text{DC engage/nothing}\rightarrow\text{OUTWARD local expression}\rightarrow\text{AC differential}(-1/0/+1)\rightarrow\text{ACROSS shared differential}\rightarrow\text{OVER crossover}\rightarrow\text{next differential}.
\]

**Recursive-interface rule:**
\[
\boxed{\text{OUTPUT relation of level }n=\text{INPUT relation expected by level }n{+}1.}
\]
A higher-level cluster must be substitutable for a lower-level relational node without forcing the surrounding architecture to understand its internal implementation. See G-725 for how this rule extends to memory and cube-scale hardware.

## First compute target: balanced-ternary arithmetic

Two operand trits \(A,B\in\{-1,0,+1\}\); a complete one-trit adder handles all nine input combinations and produces sum and carry where required:

\[
+1+(-1)\rightarrow0,\qquad
+1+1=+2=(+1\times3)+(-1\times1),\qquad
-1+(-1)=-2=(-1\times3)+(+1\times1).
\]

One trit carries \(\log_2 3\approx1.585\) bits of information. Recursive ternary addressing does **not** make one trit equal millions of bits — \(n\) ternary decisions address \(3^n\) endpoints; information capacity and addressing reach are kept separate.

## Magnetic differential bench interpretation

A passive pickup winding measures changing flux, \(V=-N\,d\Phi/dt\). Static remanence is not automatically a persistent DC pickup voltage — retention must be measured with an explicit read method. The ideal complementary differential

\[
(A+N)-(-A+N)=2A
\]

gives ideal common-mode cancellation and doubled differential amplitude; it does not by itself prove doubled SNR, doubled speed, or half power.

## Build strategy

\[
\text{breadboard measured primitive}\rightarrow\text{microfabricated triad test structures}\rightarrow\text{repeated triad test die}\rightarrow\text{stacked 3D die/module}\rightarrow\text{six-face packaged cube interface}\rightarrow\text{connected cube lattice.}
\]

Immediate breadboard proof (six-pin mechanically ganged pots, op-amps/comparators, resistors, LED indicators, 5V supply, oscilloscope) must first show: (1) opposed linked response; (2) stable \(-1/0/+1\) differential regions; (3) a resolved differential driving/conditioning the next identical stage; (4) retained state if a magnetic-memory primitive is claimed; (5) the next stage using the same interface without a growing translation layer.

The first custom fabrication run should characterize many primitive geometry/process variants on one test die, not attempt a dense final cube before the primitive is characterized.

## Point / Path / Field (hardware reading)

\[
\text{Point}=\text{local relation/triad behavior},\quad
\text{Path}=\text{neighbor differential/routing},\quad
\text{Field}=\text{coordinated cluster/cube behavior}.
\]

Field, Void, and Routing may be different-scale roles of the same invariant relational mechanism rather than different primitive species (see G-725 for the Field/Void processor-scale split).

## Scope boundary

N-body, Mercury EM, MESSENGER magnetometry, packet compression, and other scientific validation branches (E-533, E-534) exercise this kernel but must not redefine it. A provider-neutral AI-callable video/audio generation goal is a separate product target, independent of the VTC kernel.

## Status

GREEN — the architecture is internally consistent and the dependency direction is locked:
\[
-(0)+\rightarrow\text{six-pair oscillator}\rightarrow\text{Views/Actions/Choices/Moves/Modulation}\rightarrow\text{triad implementation}\rightarrow\text{recursive interface}\rightarrow\text{G-725}.
\]
YELLOW on the physical claim: no breadboard primitive has yet been built or measured against section "Build strategy" above.
