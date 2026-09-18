# Historical Unintegrated Node Draft

This file was removed from the active `Nodes/` namespace in Updated 32 because it has no canonical node ID, uses an alternate template, and contains stale dependency assumptions. Its subject remains covered by Book 1 Chapter 8. No new node ID was invented during the integrity repair.

---

---

Function Node

Function: Neutrino (Weak-Transit Excitation)

Status: 🟡 Yellow

---

Purpose

The existing glossary entry for neutrino (01_Definitions.md #61) describes a diagnostic role — "ghost-like signal, passes through the lattice without affecting it" — without deriving that behavior. Excitation.md locks a Reduction Rule requiring every excitation to reduce to Differential → Flow → Coupling → Stability. This node supplies that reduction.

---

Definition

A neutrino-like excitation is not a separately-postulated object. It is the emitted component of a relaxing localized structure, characterized by a coupling function that is strong at one event (emission) and near-zero everywhere after (transit).

Let a localized structure be:

[
\Delta\psi_L(x,t)
]

Define its boundary as the level set:

[
\Gamma_L(t) = \{x : |\Delta\psi_L(x,t)| > \epsilon\}
]

for a chosen threshold ε. Define the characteristic size:

[
R(t) = \max_{x \in \Gamma_L} |x - x_c|
]

where x_c is the center of the localized excitation (peak or centroid — to be fixed when this node is promoted; the two coincide for symmetric profiles and are not yet distinguished here).

---

Mathematics

Stage 1 — Extraction event

The structure relaxes:

[
\Delta\psi_L \rightarrow \Delta\psi_\nu + \Delta\psi_{remaining}
]

The restoring-response operator (A-105) is nonzero for the emitted component at the moment of release:

[
\mathcal{A}_{emit} = \mathcal{A}_\nabla(\nabla\Delta\psi_\nu) \neq 0
]

because an interaction occurred — this is required for the excitation to carry energy away from the parent structure at all.

Stage 2 — Transit

After emission, the excitation propagates and its boundary expands: R(t) increases. Using the conserved quantity

[
E_\nu = \int |\Delta\psi_\nu|^2\, dV
]

and an expanding front of area A(R) ∝ R^{d-1} (d = spatial dimension of the spreading), conservation gives:

[
\boxed{|\Delta\psi_\nu| \propto R^{-\frac{d-1}{2}}}
]

The gradient then depends on both this amplitude decay and the mode structure (wavenumber k):

[
\nabla\Delta\psi_\nu \sim k\,\Delta\psi_\nu
]

As R → ∞, |Δψ_ν| → 0, so ∇Δψ_ν → 0, and by A-105's already-proven implication (∇ψ = 0 ⇒ F_OW = 0):

[
\boxed{\mathcal{A}_{transit} \to 0}
]

"Passes through without affecting the lattice" is therefore a *consequence* of amplitude dilution, not an assumed property.

---

Open Dependency: Spreading Dimension

The value of d (2 or 3) determines the decay exponent:

[
d=2 \Rightarrow |\Delta\psi_\nu| \propto R^{-1/2}, \qquad d=3 \Rightarrow |\Delta\psi_\nu| \propto R^{-1}
]

This is not resolved here. It depends on whether the emitted excitation spreads through the 2D compressed substrate or the 3D expressed geometry — a question that belongs to the Projection Rule (Appendix G), which does not yet exist as built content (verified directly: `Apendix_G.md` currently contains a duplicate of the Gradient node rather than a Projection Rule node, and Gradient itself lists Appendix G as an unmet dependency). Both cases are stated above rather than one being assumed.

---

Interpretation

Neutrino is not a single-property object. It is a two-stage coupling event: strongly coupled exactly once (extraction), then weakly coupled continuously after (transit), with the transition driven by geometric dilution rather than an intrinsic on/off switch. This matches the physical requirement that emission must do real work (carry energy from a decaying structure) while transit must not.

---

Assumptions

1. ε (the threshold defining Γ_L) is a modeling choice, not yet derived from anything upstream.
2. x_c (peak vs. centroid) is not yet distinguished — immaterial for symmetric profiles, open for asymmetric ones.
3. The conservation law used for E_ν assumes no dissipation between emission and the point of measurement; if 𝒜_transit is only approximately (not exactly) zero, this is an approximation whose error has not been bounded.

---

Candidate Experiment

Objective

Determine the actual spreading dimension d by observing how a released excitation's amplitude falls off with distance from its emission point.

Procedure

1. Construct a localized structure Δψ_L in simulation.
2. Trigger relaxation and identify the emitted component Δψ_ν.
3. Measure |Δψ_ν| as a function of R(t).
4. Fit against R^{-1/2} (d=2) and R^{-1} (d=3); the better fit indicates which geometry governs transit — pending the Projection Rule node existing to make this a formal prediction rather than a post-hoc fit.

---

Dependencies

Core Functions

- A-105 Restoring Response (𝒜_∇, and its proven implication ∇ψ=0 ⇒ F_OW=0)
- A-108 Local Stability (for Δψ_L's own existence as a stable structure prior to relaxation)

Supporting Functions

- Appendix G: Projection Rule — **unmet**. Blocks resolution of d.

Downstream Functions

- Excitation.md's Reduction Rule (this node satisfies it)
- Any future relaxation/emission node for other excitation types, which may reuse this two-stage coupling pattern

---

Yellow Audit Result

The zero-coupling claim from the original glossary entry has been replaced with a derived two-stage mechanism, reusing A-105's already-proven implication rather than asserting transparency as a given. R(t) is grounded in a level-set definition rather than introduced as a free parameter. The decay law comes from a stated conservation principle, not an assumed exponent. The one remaining gap — spreading dimension d — is explicitly left open rather than guessed, and is correctly attributed to a dependency (Projection Rule) rather than treated as this node's own unfinished business.

---

Final Yellow Lock

Neutrino is locked at Yellow: mathematically defined, internally consistent, dependency-honest. It cannot advance to Bronze until either the Projection Rule node resolves d, or a candidate experiment (simulated or real) fixes it empirically.

---
