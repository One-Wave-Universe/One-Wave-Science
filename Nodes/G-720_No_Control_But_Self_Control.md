---
node_id: "G-720"
canonical_name: "No Control But Self-Control — Reaction Choice Model"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Application Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node G-720: No Control But Self-Control — Reaction Choice Model

Origin note: “No control but self-control” appeared as a standalone statement early in the project. This node formalizes it as a checkable response rule.

Dependencies:
Upstream: B-203 Expression, B-204 Compression, G-710 Grow The Fuck Up Gate
Downstream: Proposed One-Wave Consciousness Ch2; future response-control simulations

## Definition

A system does not directly control an external stimulus, another agent, or a past event. It controls only the transformation between received input and its own next state.

Automatic reaction:

\[
R_a=gS
\]

where the gain `g` is not constrained by an evaluated internal limit.

Regulated response:

\[
R_c=k(M)S,\qquad 0\le k(M)\le k_{\max}
\]

where `M` is the system's current memory/state evaluation. This is the G-720 application of G-710's unregulated-versus-regulated gain distinction.

The response direction is selected separately through B-203/B-204:

\[
\sigma\in\{-1,+1\}
\]

\[
\Delta\psi=\sigma R
\]

with `σ=-1` for the compressive choice and `σ=+1` for the expressive choice.

## Three-Step Process

1. **Receive** — the stimulus enters the current state.
2. **Hold** — the state is evaluated against memory, limits, and context.
3. **Commit** — the selected bounded transformation writes the next state.

```text
Receive -> Hold -> Commit
```

`Commit` replaces the earlier word `Move`. The earlier wording collided with B-221, where MOVE is the second step and means introduction of a difference. G-720's third step is a state write, so Commit is the correct distinct term.

## State Update

\[
\psi_{n+1}=\psi_n+\sigma_n R_n
\]

Automatic case:

\[
R_n=R_a=gS_n
\]

Regulated case:

\[
R_n=R_c=k(M_n)S_n
\]

The external stimulus `S_n` is not rewritten by this rule. Only the system's own response and resulting state are selected.

## Worked Yellow Example

Use the same stimulus in both cases:

\[
S=4,\qquad k_{\max}=1
\]

Automatic gain:

\[
g=4\Rightarrow R_a=16
\]

Evaluated regulated gain:

\[
k(M)=0.75\Rightarrow R_c=3
\]

For an expressive choice `σ=+1` from `ψ_n=10`:

\[
\psi_{n+1}^{(a)}=10+16=26
\]

\[
\psi_{n+1}^{(c)}=10+3=13
\]

The example demonstrates the intended distinction: the same input can produce a large automatic reaction or a bounded regulated response. It does not yet derive the function `k(M)` from lower-level One-Wave variables.

## Operational Chain

```text
Stimulus
-> Receive
-> Hold / evaluate internal state
-> choose compression or expression
-> bound response gain
-> Commit next state
-> feed result into the next cycle
```

## Yellow Audit

- The collision with B-221's MOVE is resolved.
- The R_a/R_c relationship is explicit and has a worked numerical check.
- `k(M)` remains a constrained function rather than a derived mechanism.
- No dynamic simulation has been run; this node is not Bronze.

## Future Work

Derive or calibrate `k(M)` from G-702 Evaluation, G-703 Modulation, G-709 Regulated-Response Balance, and B-216 control gains. Then run repeated-input simulations comparing automatic overshoot, bounded response, recovery, and failure states.
