---
node_id: "E-509"
canonical_name: "Propagation Limit / Local-Transport Partition"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "GREEN (one-cell-per-step ceiling) / YELLOW (partition norm)"
metadata_standard: "I-06"
---

# Node E-509: Propagation Limit / Local-Transport Partition

**Dependencies**  
Upstream: A+101 Ground, A-109 Inertial Memory, A-114 Dispersion Relation, core update rule  
Downstream: C-309 Friction Limit / Propagation Ceiling, E-528 Static Redshift Transport

## Definition

The update rule is strictly nearest-neighbor:

\[
\psi_i^{n+1}
=
\psi_i^n
+\gamma F(\psi_i^n,\psi_i^{n-1})
+\beta(\langle\psi_j^n\rangle-\psi_i^n).
\]

A site's next state depends only on itself and its immediate neighbors. A disturbance therefore cannot advance farther than one lattice spacing in one update. This is a structural propagation bound, not a Mass-Effect mechanism.

The update contains two bookkeeping contributions:

- **local update**: \(L_i=\gamma F(\psi_i^n,\psi_i^{n-1})\);
- **neighbor transport**: \(T_i=\beta(\langle\psi_j^n\rangle-\psi_i^n)\).

These labels describe where one update contribution comes from. They do not classify energy as matter, inertia, or rest Mass Effect.

## Mathematics

### Propagation ceiling - GREEN

\[
c_L=\frac{\Delta x}{\Delta t}.
\]

This is the strict one-cell-per-step upper bound. The physical group velocity must be derived from A-114:

\[
v_g(k)=\frac{d\omega}{dk}.
\]

### Local-transport partition - YELLOW

After a conserved update norm \(\|\cdot\|_U\) is derived, define the provisional bookkeeping shares

\[
\ell_i
=
\frac{\|L_i\|_U}{\|L_i\|_U+\|T_i\|_U},
\qquad
\tau_i
=
\frac{\|T_i\|_U}{\|L_i\|_U+\|T_i\|_U},
\qquad
\ell_i+\tau_i=1.
\]

Until that norm is derived, \(\ell_i\) and \(\tau_i\) are placeholders only.

They are bookkeeping shares only. They do not determine group velocity and they do not determine any Mass-Effect quantity. Group velocity comes from the dispersion relation. Mass Effect comes from the second velocity response of the complete four-interaction recurrence.

## Canonical Separation

```text
E-509 -> how a local update is partitioned
A-114 -> dispersion and group velocity
C-309 -> propagation ceiling and damping constraints
C-318 -> Mass Effect from all four interactions together
```

No algebraic conversion from \(\ell/\tau\), \(\tau/\ell\), or either share alone into Mass Effect is permitted.

## Yellow Audit

- derive the local operator \(F\) from the accepted update architecture;
- identify a conserved norm for the complete update;
- calculate \(v_g(k)\) from A-114 rather than from partition shares;
- test whether the partition has any independent predictive use in transport;
- keep every transport quantity mechanically separated from C-318's response tensor.

## Failure Condition

The partition proposal fails if no conserved norm supports it or if it merely repackages the update terms without producing an independent transport prediction. Failure does not authorize reinterpretation as inertia.
