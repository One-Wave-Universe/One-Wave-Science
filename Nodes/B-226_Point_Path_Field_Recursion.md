---
node_id: "B-226"
canonical_name: "Point-Path-Field Recursion"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Structural Language Primitive"
claim_gate_detail: "YELLOW (recursive structure and floor/ceiling conditions) / open (cross-scale instantiation — see I-04 classification below)"
metadata_standard: "I-06"
---

# Node B-226: Point-Path-Field Recursion

## Grounding note

Point-Path-Field (PPF) has been used extensively — `UPDATED_40_RECURSIVE_PLANETARY_POINT_PATH_FIELD_ROTATION_MODEL.md` and `UPDATED_41_PLANETARY_SCALE_DISPLACEMENT_MODEL.md` build an entire nine-state planetary architecture on it — but it was never promoted to a canonical node. It existed only as planetary-specific prose, with no general definition, no I-06 metadata, no gate, and critically, no stated reason PPF bottoms out anywhere or why "Point/Path/Field" is the right three-way split rather than an arbitrary one. This node formalizes it as a general, scale-independent structural primitive, and gives the recursion an honest floor and ceiling instead of leaving "how far does it go" unanswered.

Dependencies:
Upstream: A-107 Bounded Motion (supplies the recursion floor, §2), A-111 Recursion (general self-referential update), A-112 Persistent Mode (what a "Point" is), A-115 Unified Compression Field (supplies the recursion ceiling, §3), C-302 Momentum / C-306 Torque / C-307 Angular Momentum (what "Path" is built from), A-105 Restoring Response / D-401 Flux (what "Field" is built from), C-311 Electric-Magnetic Duality (EM generalization, §4), I-04 Scale Recurrence vs. Duplication (governs §5's cross-scale classification)
Downstream: UPDATED_40, UPDATED_41 (planetary instance — should now cite this node as their formal upstream primitive rather than defining PPF ad hoc), C-317 Boundary-Tension Weave (candidate vortex-scale instance), Book 5 Ch1 Galaxies, Book 5 Ch2 Stars (candidate galactic/stellar instances)

## 1. Why this triad, not an arbitrary one

PPF is not three interchangeable labels. Each arm already corresponds to machinery this repository has separately built:

- **Point** — the bounded structure's own internal composition: whether it is a genuine persistent, bounded mode at all. This is exactly A-112 Persistent Mode's subject, tested by A-107's criterion (I₃ > I₁/2, derived in `Internal_Proofs/08_Keplerian_Limit_Derivation.md`'s upstream chain).
- **Path** — its kinematic state: position, velocity, angular momentum, torque. This is exactly C-302/C-306/C-307's subject — the same apparatus `Internal_Proofs/08` §5 used to derive Kepler's laws.
- **Field** — what it generates in, and receives from, its surroundings: the same apparatus A-105 (restoring response) and A-115 (compression field) already use.

A state's PPF decomposition is therefore `(P(X), Pa(X), F(X))` = (does it have genuine internal structure, how is it moving, how does it couple outward) — three independently-motivated questions, not one arbitrary partition dressed up as three.

## 2. Formal recursion and its floor

Define the recursion operator on a bounded state `X`:

```
PPF(X) = ( P(X), Pa(X), F(X) )
```

The recursive claim (already used, never justified, in Updated 40/41) is that `P(X)`, `Pa(X)`, and `F(X)` are themselves bounded states admitting their own PPF decomposition, giving depth-2 nine-fold structure `{PP, PPa, PF, PaP, PaPa, PaF, FP, FPa, FF}`, depth-3 twenty-seven-fold, and so on: `PPF^n(X)` has `3^n` components.

**This cannot recurse forever, and here is a principled place it stops, not previously stated:** applying `PPF` to a candidate sub-state only makes sense if that sub-state is itself a genuine bounded mode — otherwise "its internal structure" is nothing but local Ground/Zero fluctuation, with no persistent Point to decompose further. A-107 already supplies the exact test for this: a candidate solution is bounded motion **iff** `I₃ > I₁/2` (curvature energy exceeds half the gradient energy). Propose, as this node's floor condition:

```
PPF(X) is defined  <=>  X passes A-107's bounded-motion test (I₃ > I₁/2)
```

The recursion terminates at whatever depth a candidate `P`, `Pa`, or `F` component fails that test — below that, there is no further bounded Point to open up, only undifferentiated field. This is a real, checkable stopping condition inherited from already-derived math, not an arbitrary depth limit chosen to make the recursion feel finite.

**What this does not yet tell you:** at which actual physical scale that failure first occurs. That requires evaluating `I₁, I₃` for a real candidate profile at each scale — flagged as open in A-107 itself ("Specific-profile validation ❌") and inherited here unchanged. This node states *where* the floor is defined, not *what scale* it falls at.

## 3. Ceiling

Symmetric question, upward: does `F(X)`'s own Field ever stop having a larger Field to sit inside? I-01 Rule 16 ("no expansion of space in canonical One-Wave math") and A-115 §5's static cosmic energy accounting are both written over a single **closed** domain `Ω`. That closure is the recursion's structural ceiling: there is no "Field within Field" beyond the one static cosmic domain the framework already commits to, by construction — not because derivation ran out, but because the framework's own governance (I-01 Rule 16) forbids treating it as open outward.

**Keep two different senses of "how far up" separate, since conflating them would misstate what's actually established:**
1. **Structural ceiling** (this section): principled, given directly by I-01 Rule 16 + A-115 — the recursion cannot exceed the one closed cosmic domain.
2. **Built-out ceiling** (§5 below): how far the explicit PPF rungs have actually been instantiated and checked. That currently stops at galaxy scale (Book 5 Ch1). Galaxy clusters are not addressed anywhere in this repository yet — an honest gap, not a claim that PPF fails there.

## 4. EM generalization (not planet-specific)

Updated 40 §4 gave planets an "internal EM rotation" channel ad hoc. Generalized: for any bounded state `X` whose Point contains internal current circulation (conducting fluid, charged circulation, plasma — anything C-311 applies to), that circulation and its generated field is itself a full PPF instance, nested inside `P(X)`:

```
P(X) has internal current J(X)  =>  PPF( B_field(X) ) is defined,
  with P(B_field) = the field's own multipole/geometric structure,
  Pa(B_field) = field rotation/precession relative to matter rotation,
  F(B_field) = the field's own external overlap with neighboring bodies' fields
```

using C-311's `E ~ ∇P_c`, `B ~ ∇×P_c` radial/rotational projections as the concrete field this sub-recursion is built from. This is the same structure Updated 40 gave Mercury/Earth/the giant planets specifically, restated as a general rule: **any** vortex, plasma current, or persistent charge circulation gets a nested EM-PPF instance, not just planets — including, in principle, C-317's Vortex Phases (a Vortex Phase with any internal circulation would carry its own nested PPF by this same rule, not previously stated).

## 5. Cross-scale instantiation — classified per I-04, not asserted

This is the part your question actually asks, and it needs I-04's discipline applied explicitly rather than skipped. I-04's evidence ladder requires classifying a cross-scale claim by evidence tier before treating it as anything stronger than what's shown. Current honest tier for "PPF operates identically from vortices to galaxy clusters":

**Tier 4 — Scale Recurrence** ("the same ordered functional architecture appears across scales, roles map consistently, but mechanism/mathematics not yet shown identical. Preserve all instances, build a cross-scale comparison table, do not claim physical identity.")

Not Tier 6 (Candidate Scale Invariance) or Tier 7 (Supported Scale Invariance) — both require the governing mathematics to survive rescaling, which needs `γ(s)`/`β(s)`, the exact quantity B-220, E-507, and E-522 all already flag as the shared unresolved blocker. PPF inherits that same blocker; it does not get a pass just because the P/Pa/F role-mapping looks clean.

**Cross-scale comparison table (roles mapped, mechanism identity NOT claimed):**

| Scale | Candidate Point | Candidate Path | Candidate Field | Status |
|---|---|---|---|---|
| Vortex / quark-scale | Vortex Phase, C-317 | phase circulation within the knot | Boundary-Tension Weave | roles plausible; no PPF math run against C-317 yet |
| Particle / atomic | A-112 Persistent Mode | internal recursive cycle (A-111) | A-105 gradient field it projects | roles plausible; native scale of A-105/106/107, best-grounded rung |
| Planetary | UPDATED_40/41's internal rotation state | orbital path (this session's Internal_Proofs/08 §5) | UPDATED_40's moving finite-slope field | only rung with an actual built-out architecture (Updated 40/41) |
| Stellar | Book 5 Ch2's sustained Persistent Mode under compression | stellar motion/orbit within a galaxy | stellar wind / compression field | named in Book 5 Ch2; no PPF structure written for it yet |
| Galactic | galaxy as a bound structure (Book 5 Ch1) | galactic rotation curve (Book 5 Ch1, flagged sketch-only) | compression-ring / dark-matter-view field (Book 5 Ch1) | rotation curve exists as a sketch form only; spiral-arm structure explicitly flagged "not yet attempted" in Book 5 Ch1 — a natural PPF Path/Field target, still open |
| Galaxy cluster | cluster halo, own self-gravity | bulk infall toward Great Attractor/Laniakea basin (real, measured ~600 km/s peculiar velocity) | Great Attractor tidal field | now has real content: `Internal_Proofs/09_Tidal_Torque_Cascade_Mechanism.md` computes the GA→cluster tidal ratio (~10⁻¹·⁷, dynamically real) — still Tier 4, mechanism computed, not simulated |

**What this table licenses and what it does not:** it licenses preserving every row as a real, separately-tracked candidate instance and using the same P/Pa/F questions to organize future work at each scale (including, eventually, galaxy clusters). It does **not** license saying PPF "is" the same mechanism at every scale, or extrapolating the planetary architecture's specific equations upward or downward without redoing the work — that is precisely the jump from Tier 4 to Tier 6/7 that I-04 exists to block, and the exact mistake E-522 was already corrected for making with a different pair of scales.

**Candidate mechanism for how rotation enters the recursion, computed not assumed (`Internal_Proofs/09`):** each level's Path/rotation component is hypothesized to be seeded by tidal torque from its immediately-enclosing level's tidal field acting on its own mass asymmetry, then amplified by angular-momentum conservation if and only if that level subsequently collapses/virializes (the actual physical content of "bounded" in this recursion). Internal_Proofs/09 computes that a direct skip-level reach (e.g. Great Attractor scale directly to planetary spin) is suppressed by roughly 19-26 orders of magnitude, while adjacent-level torques (Attractor→cluster, cluster→galaxy) remain dynamically real. Calling this a "relay" (successive transmission down the hierarchy) is a candidate reading of that computed pattern, not proven by it — flagged explicitly in Internal_Proofs/09 §4 after independent review, and repeated here so this node doesn't restate the stronger, unproven version. This still does not resolve the γ(s)/β(s) blocker below, and is itself order-of-magnitude estimation, not a simulation.

## Yellow Audit

- The floor condition (§2) is a new proposal, checked against A-107's already-derived criterion but not yet evaluated for any real candidate profile at any specific scale — it defines *where* the floor is, not *what scale* it falls at.
- The ceiling condition (§3) is structural (from I-01 Rule 16), not derived from dynamics — a different, weaker kind of "closed" than the floor's dynamical criterion; do not conflate the two.
- §4's EM generalization has not been checked against C-317's Vortex Phases specifically — proposed, not run.
- §5's table is a scaffold for future work, not a result. Every row except Planetary is currently unbuilt math.
- Galaxy clusters: genuinely absent from this repository. Building that rung is future work, not an oversight this node corrects.
- This node inherits, rather than resolves, the shared `γ(s)`/`β(s)` blocker from B-220/E-507. Nothing here makes progress on that; it only states precisely what depends on it.

## Future Work

Evaluate the floor condition (§2) against a real solved A-106/A-107 trial profile at at least one specific scale (the same open item A-107 already lists).
Run §4's EM-PPF generalization against C-317's Vortex Phases as the first concrete micro-scale test.
Attempt Book 5 Ch1's already-flagged "spiral arm structure" as the first real galactic-scale PPF Path/Field derivation, rather than leaving it a named-but-untried extension.
Do not build a galaxy-cluster rung by extrapolation; build it the same way Planetary was built (Updated 40's route), from that scale's own physics.
Prioritize deriving `γ(s)`/`β(s)` (B-220/E-507's shared blocker) over adding further scale rows to §5's table — every row added without it stays stuck at Tier 4.

---
