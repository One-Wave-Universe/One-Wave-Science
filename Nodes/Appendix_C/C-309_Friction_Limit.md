---
node_id: "C-309"
canonical_name: "Friction Limit / Propagation Ceiling"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Propagation Constraint / Damping Formalization"
claim_gate_detail: "YELLOW"
metadata_standard: "I-06"
---

# Node C-309: Friction Limit / Propagation Ceiling

**Dependencies**  
Upstream: A-109 Inertial Memory, A-114 Dispersion Relation, C-303 Kinetic Energy  
Downstream: C-310 Resistance Field, C-318 Four-Interaction Mass-Effect Response, Book 1 Ch7 Photon, E-509 Propagation Limit / Local-Transport Partition

## Purpose

C-309 separates two kinematic quantities:

1. **memory damping**, controlled by A-109's coefficient \(\gamma\); and
2. **maximum propagation speed**, controlled by the real branch of the lattice dispersion relation.

A previous draft misread these propagation constraints as a mechanism for the Mass Effect. That was a false assumption introduced by misunderstanding what C-309 actually describes. It is permanently removed. Neither damping nor propagation status generates inertia.

## Memory Damping

A-109 supplies

\[
M_i=(1-\gamma)\Delta\psi_i^n.
\]

- \(\gamma=0\): complete carry-forward,
- \(\gamma=1\): no carry-forward,
- \(0<\gamma<1\): partial damping.

The scale dependence \(\gamma(s)\) and any useful upper/lower stability bounds remain open.

## Propagation Ceiling

For the current discrete lattice candidate, the maximum supported signal speed is written

\[
c_{\rm lat}=v_{\max}
=\sqrt{\beta_{\max}}\,\frac{\Delta x}{\Delta t}.
\]

This equation constrains travel on the real dispersion branch. It supplies no nonzero rest response and no term in the C-318 Mass-Effect tensor. Whether a mode travels below, at, or near the ceiling cannot be used to infer its Mass Effect.

For the current candidate,

\[
\omega(0)=0,
\]

so the propagation branch remains smooth at \(k=0\). Any nonzero Mass Effect must instead be calculated from the work required to carry and rebuild the complete four-interaction recurrence.

## Operational Separation

```text
C-309: propagation and damping constraints
E-509: local-versus-transport bookkeeping
C-318: four-interaction carried-pattern Mass-Effect response
A-115: unified field and local boundary-resistance view
C-322: 125 GeV Mirror-Gate pressure-work threshold
```

The propagation ceiling can constrain transport predictions after the Mass-Effect mechanism is derived. It is not part of that mechanism's origin.

## Canonical Prohibition

No active One-Wave node, chapter, wiki page, AI-readable pack, simulation, or diagram may derive Mass Effect from:

- propagation speed,
- failure to propagate,
- damping alone,
- localization share,
- a local/transport ratio,
- or the friction limit.

Any future merge that does so fails the canonical audit automatically.

## Yellow Audit

- derive the complete dispersion relation from accepted lattice variables;
- determine whether \(\gamma\) and \(\beta\) are independent or coupled;
- derive any scale dependence \(\gamma(s)\) or \(\beta(s)\);
- identify the parameter regime in which the long-wave signal speed matches measured \(c\);
- verify that transport calculations remain separate from the C-318 response tensor.

## Failure Condition

C-309 fails as a universal propagation constraint if one fixed lattice law cannot support the required signal-speed behavior across the claimed regimes. It does not receive a second role as a mass mechanism if that happens.
