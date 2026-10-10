# Audit: Cosmology Scope and Contradictions

**Date:** 2026-10-10
**Branch:** `audit/cosmology-scope-contradictions`
**Scope:** Audit only. No equations are rewritten and no model is replaced in this document.
**Authority order:** A-115 (displacement and compression) → D-601/D-602 (scalar vs. vector) → W2 → E-528 → E-533 → external observational tests.

Labels follow AGENTS.md: **[ESTABLISHED]** standard physics or external data · **[DERIVED]** follows from stated repo equations · **[SIM]** simulation output · **[PROPOSAL]** proposed, not derived · **[OPEN]** unresolved.

---

## 1. Anchor: A-115 as the displacement authority

A-115 (`Nodes/A-115_Unified_Compression_Field.md`) is the current authority for the displacement field. Its primitives:

- Vector displacement `u(x,t)` from Ground/Zero, with scalar compression `χ = −∇·u` **[PROPOSAL, sourced equation]**.
- Energy density `E = (ρ_u/2)|∂_t u|² + (K_χ/2)χ² + (S_u/2)|∇u|² + V_b(u)` **[PROPOSAL]**. The coefficients are stated as uncalibrated.
- Gravity view `Φ = α_g χ`, `g₀ = −α_g ∇χ` **[PROPOSAL]**.

Two gate facts matter for everything downstream:

- A-115 is GREEN overall, but its own `claim_gate_detail` reads **YELLOW for the field decomposition and static-loop equations**. Cosmology claims that depend on the static loop therefore rest on YELLOW content.
- A-115 states that D-413 "does **not** yet derive the A-115 gravity law" and that M_eff is the measured Mass Effect assigned to a bounded source, not an independently defined quantity **[OPEN]**.

---

## 2. W2 audit against the vector formulation

D-601 concludes that the scalar update rule cannot produce E/B structure: "Scalar dies here," with E/B either imposed or requiring a vector field. D-602 (GREEN) generalizes to `ψ⃗` and derives E/B. A-115 uses a vector `u`. W2 (`W2_GRAVITY_FROM_DISPLACEMENT.md`, dated 2026-10-04) is built on scalar ψ. Every scalar assumption that conflicts with the vector formulation:

| # | W2 line | Assumption | Conflict | Class |
|---|---|---|---|---|
| S1 | L13, L4 | `ψ(x,t)` is a scalar; "ψ is the only primitive" | D-601: scalar insufficient for E/B; A-115 uses vector `u` | **Hard conflict** |
| S2 | L35 | `ρᵢ ≡ ∇·ψᵢ = (ψᵢ₊₁ − ψᵢ₋₁)/(2a)` | Divergence of a scalar is undefined. The formula is a 1D central difference, i.e., a gradient. | **Mathematical error** |
| S3 | L22 | `E-field ∝ ∇ψ` (gradient of scalar) | D-601: scalar gradient cannot separate E from B | **Hard conflict** |
| S4 | L51, L68 | `T⁰⁰`, `Tⁱʲ` built from `|∇ψ|²` and `∂ψ/∂xⁱ·∂ψ/∂xʲ` | A-115 energy density has a compression term `(K_χ/2)χ²`; W2 has none | **Structural conflict** |
| S5 | L97–98, L156 | Ricci scalar `Rᵢ = ∇²(∇·ψᵢ)` | Inherits S2. No metric `gᵢⱼ` is defined in the deformed lattice, so this is not the curvature of any metric. | **Mathematical error** |
| S6 | L166 | `… + Λψᵢ` in the Einstein-type equation | A tensor equation reduced to a scalar at each site, with no tensor structure defined | **Structural gap** |
| S7 | L189–191 | Poisson `∇²φ ≈ ρ_matter` with `ρ = ∇·h` | A-115 has `∇²χ = (1/K_eff)∇·J_source` with `χ = −∇·u`. Different source terms and different potentials. | **Conflict with A-115** |
| S8 | L305 | "density waves (∇·ψ) oscillate independently of shear (∇×ψ)" | Curl of a scalar is undefined. D-602 needs a vector field for the transverse mode. | **Hard conflict** |
| S9 | L321–323, L353–358 | Code skeleton uses `np.gradient` on 1D arrays | A 1D scalar cannot represent 3D divergence or curl | **Implementation consequence of S1–S2** |

**Gravity mechanism (C2): resolved in direction, derivation open.** The project owner's definition: the lattice is spacetime, and spacetime curvature is what the lattice is. The rejected claim was not that curvature exists. It was that curvature is an *independent* mechanism separate from the displacement. Per the project owner's direction, and consistent with `UPDATED_64_GRAVITY_IS_THE_WAKE_AND_THE_RELAY.md` (interpretation lock, 2026-10-05) and A-115 §2, gravity is the extended compression wake: the displaced medium a parent creates, which smaller displacements are carried along and trapped in as they move through its paths. W2's curvature mechanism is therefore out of scope for the rewrite. What is not yet derived: the path-capture term (A-115 `Q_capture`; E-09 capture fraction κ), the boundary test for "still distinguishable" (UPDATED_64 states it is not derived and no cutoff radius may be inserted by hand), and recovery of the Newtonian sum as the control **[PROPOSAL / OPEN]**.

**Reach of gravity (C11): finite, and relayed along paths.** Per the project owner's direction, gravity effects do not extend without limit. They persist as the relayed wake follows curved paths, and they end where the slope stops being distinguishable (UPDATED_64). This is not yet consistent with the repo's current finite-wake node. E-532 (YELLOW) defines a finite wake as an isotropic kernel `W(r) = e^{−r/σ}/r`, where gravity-like reach requires large σ, and σ is a free range parameter. That conflicts in two ways. First, the reach is set by a chosen parameter, which UPDATED_64 forbids: "no cutoff radius is to be inserted by hand." Second, the reach is isotropic in r, whereas the owner's direction is path-dependent, following relayed curved paths; C-320's path-weighted restoring response is the existing candidate for path dependence. The audit does not choose a kernel. The derivation has to produce the reach from the distinguishability test along the relay path, and then show whether that reproduces an isotropic kernel in any limit.

**Masking of a parent's reach by descendants (C12): gap, not yet derived.** Per the project owner's direction, a parent's wake has a set range, but every child that sits in it adds its own displacement to the same spacetime curvature. Curvature is the lattice geometry, so the children's contributions add to one geometric response; they do not form a separate curvature term. Summed over the descendants, these contributions hide the parent's effect beyond its nominal range, so the apparent reach of gravity is shorter or more variable than the intrinsic one. This is consistent with UPDATED_64 ("the child adds its displacement and its motion into the shared party") and with `D-415` MATH_GAPS, which lists "independent superposed body fields" as an open problem. It also needs the screening term that `D-401` identifies as missing. Two consequences are testable in principle, and neither is computed here: (i) the measured reach of a lone body should exceed the reach measured inside a populated system, and (ii) the superposition rule must reduce to the Newtonian sum when descendant couplings vanish, as UPDATED_64 requires. The intrinsic range is a free parameter until it is derived from the same relay mechanism as C11 **[PROPOSAL / OPEN]**.

**Status conflict (C6).** W2's Part 10 marks "✓ Einstein equations follow from discrete lattice geometry" and "✓ Schwarzschild emerges." Every item in its implementation checklist is unchecked. W2 carries no I-06 gate metadata. These checkmarks are unsupported by the document's own steps **[OPEN]**.

**Result of the W2 audit:** W2 cannot be salvaged by relabeling. Its primitive (S1), its divergence (S2), and its curvature (S5) all need replacing with vector-field operators. The rewrite should start from `u`, with the energy density in A-115 §1 as the starting point, and should not start from W2's Part 1 stress tensor.

---

## 3. Confronting E-528 and W2: can static transport redshift and a positive Λ coexist?

### Correction to my prior statement

I said earlier that "a static universe with a positive Λ isn't a consistent setup." That was wrong and is withdrawn. The Einstein static solution for pressureless matter requires `Λ = 4πGρ` and `k/a² = Λ`. It exists and is **unstable** under perturbation **[ESTABLISHED]**. A positive Λ therefore does not by itself exclude a static universe. The question is whether the equations and the observations can be satisfied together.

### What the repo says about Λ and about static dynamics

- **W2 §6:** `Λ_bare ≈ β/a²`, identified as lattice tension, with `w = −1 + O(1/a²)` **[PROPOSAL]**.
- **E-528 hard constraint:** "One-Wave contains no expansion of space." Redshift comes from transport friction: `1+z = exp[∫κ_γ dℓ]` **[PROPOSAL]**.
- **A-115 §5:** closed static accounting, with dark energy handled as White Energy circulation and no Λ term **[PROPOSAL]**.

### Mathematical tests for coexistence

These are the tests the audit requires. None has been run yet.

- **T-Λ1 (Einstein static match).** For a static solution, `Λ = 4πGρ_m` must hold with `k/a² = Λ`. W2 requires `β/a² = 4πGρ_m`. If `a` is a lattice-scale length, `Λ` is many orders of magnitude above any observed value, so the static match fails unless `a` is cosmic. The repo must state which length `a` is and derive the constraint. **[OPEN]**
- **T-Λ2 (dark energy has three accounts).** W2 (Λ tension), A-115 §5 (static circulation, no Λ), and E-528 (transport loss) give three different dark-energy accounts. The audit cannot pick one. The test is whether W2's Λ term is an effective term inside the A-115 static budget, or a separate term that double-counts the same energy. **[OPEN]**
- **T-Λ3 (missing dynamics).** A-115 §5 gives an energy *balance* (conservation) for a closed static domain, not a *geometry*. A static cosmology needs an equation for the scale factor or curvature. Neither A-115 nor E-528 supplies one. W2 does, but on the scalar primitive (§2). **[OPEN, missing derivation]**

### Result

- The two models are **not** shown incompatible by any equation in the repo. Their coexistence is undetermined because the geometry equation is missing from the static side (T-Λ3) and the Λ term is undefined (T-Λ1).
- The two models **do** conflict on the dark-energy account (T-Λ2), which must be resolved by derivation, not by preference.

### 3a. Owner definitions: space and time

Owner definitions, recorded as stated and not yet derived:

- **Space** is the lattice.
- **Time** is how hard it is to move through the lattice, i.e., transport resistance.
- **Curvature** is the lattice geometry (§2, C2 and C13).

The repo already has a candidate for this resistance. E-533 defines a local transport-difficulty term `Ξ(χ, ∇χ, γ, β, …) ≥ 0` and a timing factor `𝒯(v, Ξ)`, with `𝒯(0,0) = 1` and `∂𝒯/∂Ξ < 0` **[PROPOSAL]**. E-528 defines a friction `κ_γ` that causes redshift, and E-528 requires that one shared medium state determine both `κ_γ` and `𝒯` **[PROPOSAL]**. The owner's definition identifies these as one quantity: resistance in the lattice. If that holds, a single resistance field would give redshift (through `κ_γ`), time dilation (through `𝒯`), and gravity (through the wake that produces the resistance). That is the strongest version of the shared-law requirement, and it is also the one most exposed to test.

What this definition requires:

- The same resistance must set clock rates in gravitational potentials. That is an established measurement: gravitational redshift (Pound–Rebka, 1960) and GPS clock corrections **[ESTABLISHED]**. Any resistance model must reproduce those rates quantitatively, not only the sign.
- Velocity time dilation must come from resistance. E-533 currently inserts the Lorentz form `d τ/dt = √(1 − v²/c²)` as a target, not a derivation. The square root must follow from the resistance law **[OPEN]**.
- Resistance must not create a second time variable. C-309 requires that the propagation ceiling not be confused with Mass Effect **[PROPOSAL, from E-533]**.
- The C13 question still stands. "Time is resistance" does not say whether the wake and the curvature are the same response. It says the resistance is one scalar candidate for the clock-rate part of that response **[OPEN]**.

### 3b. Owner definition: speed of light as friction limit

Owner statement, recorded as stated: the speed of light is the friction limit, and a body moving too fast gets stuck in time at the edge of a wave.

Repo mapping:

- **Ceiling.** C-309 defines a propagation ceiling `c_lat = √β_max · Δx/Δt` for the discrete candidate **[PROPOSAL, YELLOW]**. E-509 proves the one-cell-per-step bound `c_L = Δx/Δt` **[GREEN, within the lattice model]**.
- **Stall at the edge.** E-533 "Wave-Edge / Stall Limit" states that as `v → c⁻` the local-update fraction goes to zero and `dτ/dt → 0`. The owner's "stuck in time at the edge" is this mechanism **[PROPOSAL, E-533 YELLOW]**.
- **Identification.** E-533 states that `c_phys = c` requires a derived continuum limit, and that it is "not granted merely by notation" **[OPEN]**.
- **Scope.** C-309 forbids using the ceiling as a Mass-Effect mechanism. A body approaching the ceiling does not acquire its Mass Effect from the ceiling **[PROPOSAL, from C-309]**.

Blockers and tests:

- **C-313 (open, foundational).** The canonical update rule has a first-time-derivative damping term `μψ_t`, which selects a preferred time direction and is not exactly Lorentz invariant. C-313 says an exact Lorentz-invariant replacement must not be adopted until it reproduces the canonical damping. So "the speed of light is the friction limit" cannot be stated as a Lorentz-invariant result until C-313 is resolved **[OPEN, foundational]**.
- **Friction sets passage of time and the speed limit.** Owner statements: friction changes the passage of time, and friction sets the limit. Together these mean friction sets the clock rate (the timing factor `𝒯`) and the speed ceiling `c`. The ceiling therefore depends on `κ_γ`. An earlier draft of this audit said the opposite; that was a misreading of the owner's statement and is withdrawn **[PROPOSAL, owner direction; not yet written as an equation]**.
- **Consequence for the lattice ceiling.** C-309 gives the ceiling as `c_lat = √β_max · Δx/Δt`, a lattice-constant expression, not a friction expression. Identifying the owner's friction with `β_max` and `Δx/Δt` is required and has not been done **[OPEN]**.
- **Consequence for Lorentz invariance.** If the friction, and so `c`, varies with the local compression `χ`, then the measured speed of light would differ in compressed and uncompressed regions. Measured `c` is the same everywhere to high precision **[ESTABLISHED]**. Either the friction is uniform, or clocks and rulers scale with it so that the measured `c` is unchanged. Which one holds has to be derived **[OPEN, central blocker]**.
- **Speed sets friction, friction sets time.** Owner statement: local friction sets the passage of time, and moving faster means more friction, so time slows. This is the transport-commitment mechanism E-533 already names, `ρ_v = v²/c²` with `𝒯 = √(1 − ρ_v)` **[PROPOSAL]**. The owner's version makes the friction depend on speed through the medium: `κ(v, χ, …)`. The square-root form must come out of that friction law; E-533 does not derive it **[OPEN]**.
- **Preferred-frame risk.** If friction depends on speed through the medium, the medium defines a preferred frame, and the time dilation of two clocks in relative motion would be asymmetric, which is not the Lorentz result. Experiments constrain exactly this (for example, the Hafele–Keating flights and Michelson–Morley-type tests) **[ESTABLISHED constraints]**. The friction law must make the medium frame unobservable, or show where it is observable and that no experiment has seen it **[OPEN, central blocker]**.
- **Owner statement on reciprocity (as given): a clock moving faster sees the other clock as slow, and the slower clock sees the other as fast.** This is an asymmetric (non-reciprocal) statement. It is **not** the special-relativistic result, in which each inertial observer sees the other's clock run slow **[ESTABLISHED]**. The asymmetric form implies that "faster" is defined against some reference, i.e., a preferred frame. The owner's model therefore reintroduces the preferred-frame risk stated above, unless the reference is shown to be unobservable. Attribution note: an earlier audit entry recorded a symmetric version as the owner's statement; that attribution was wrong and is withdrawn.
- **Owner statement: the lattice differs only in relation to local displacement.** Recorded as given. This answers the decision above in favor of no absolute frame: the lattice's properties, including friction and so clock rate, depend only on local displacement. Absolute motion through the medium is not a variable. Motion matters only through the displacement it produces locally **[PROPOSAL, owner direction]**.
- **Owner statement: everything is moving; there is no displacement without motion.** Recorded as given. Under this statement, a uniformly moving clock always carries displacement, so the earlier test ("a uniformly moving clock with no displacement would show no dilation") does not arise. The dilation has no zero-displacement case to be compared against **[PROPOSAL, owner direction]**.
- **New contradiction (C14): reference state.** A-101 defines Ground/Zero as the reference state ψ₀ from which displacement is measured, and A-102 defines displacement as separation from it. If everything moves, then either ψ₀ is itself moving, so displacement is measured against a moving reference, or some state is at rest. The repo has to say which. If ψ₀ moves, the definition of displacement needs to be stated relative to what, and whether any absolute reference exists **[OPEN, owner decision required]**.
- **Owner answer: the lattice is zero.** Recorded as given. The reference ψ₀ is the zero state of the lattice, so displacement is departure from zero and motion is a departure from zero. This does not by itself settle C14. "Zero" could be one global state, which would reintroduce an absolute reference, or a local zero at each point, which matches the owner's earlier statement that the lattice differs only in relation to local displacement and avoids a global frame **[PROPOSAL, owner direction; global vs. local open]**. Under a local zero, "everything is moving" must mean each point is displaced relative to its own zero, which the law has to state explicitly **[OPEN]**.
- **Remaining implication to test.** Velocity-based dilation must come from the displacement that motion produces. Whether that displacement is reciprocal for two clocks, or favors one, is still the question for the law **[OPEN]**.
  - The asymmetry in the owner's statement then becomes a question about which clock carries more local displacement, not about a frame. Whether that gives reciprocity or the stated asymmetry is what the law has to decide **[OPEN, owner decision required]**.
  - The law must be written explicitly as a function of local displacement and derived to recover the observed results, including the reciprocal SR result for inertial clocks if the displacement is symmetric **[OPEN]**.
- **One friction, two effects.** E-528 uses `κ_γ` for redshift and E-533 uses `Ξ` for timing. Under the owner's statement these are the same friction. The shared-law requirement becomes: `κ_γ` and `𝒯` must both come from one friction law, so the redshift and the time-stretch in Attack A are two readouts of one quantity **[OPEN, derivation required]**.
- **Open consequence.** E-528 has light changing frequency along its path. If friction slows the local clock, the frequency ratio measured between source and observer must be derived from the clock-rate difference, not from energy loss alone. The two readouts agree only if that derivation holds **[OPEN]**.
- **Established measurement.** The speed of light is measured as the same in all inertial frames, and the Lorentz form of time dilation is confirmed to high precision (for example, in muon lifetimes and atomic clocks) **[ESTABLISHED]**. The friction-limit account must reproduce this invariance, not only the stall at the edge.

---

## 4. Observational attacks

External data is recorded as **[ESTABLISHED]** external evidence, with its source. Where the source is a secondary summary, that is marked.

### Attack A: Supernova time dilation

- **Standard prediction:** observed Type Ia light curves and spectral timescales stretch by `(1+z)`.
- **E-528 prediction:** no stretch. The hard constraint excludes metric time stretching, and E-528's failure list names this test.
- **External data:** Blondin et al. (arXiv:0804.3595) measured apparent aging of 13 Type Ia supernovae over 0.28 ≤ z ≤ 0.62, consistent with `1/(1+z)`. The no-dilation hypothesis is reported as rejected at up to about 6σ for individual supernovae. **[ESTABLISHED, secondary summary; verify against the paper before citing the 6σ figure]**
- **Verdict:** E-528 alone **fails** this attack as written. It survives only if E-533's timing factor `𝒯(v,Ξ)` yields a stretch exponent of 1 using the **same** κ_γ as E-528. E-533 states this shared-law requirement but does not derive it **[OPEN]**.

### Attack B: Tolman surface brightness

- **Standard prediction:** surface brightness falls as `(1+z)⁻⁴` in an expanding flat universe **[ESTABLISHED]**. A static flat universe predicts no dimming.
- **E-528 prediction (energy loss only):** under E-528's own statement that mode count is conserved (`dN/dℓ = 0`), with static flat geometry and no time stretch, the photon-energy loss gives exponent −1. **[DERIVED under stated assumptions; this is the audit's calculation and needs confirmation in the repo's formalism]**
- **External data, and the dispute over it:**
  - Lubin & Sandage (2001) report exponents of 2.6 or 3.4 depending on band, against an expected 4. They read this as consistent with expansion. **[ESTABLISHED, contested]**
  - Lerner et al. (2014) and Lerner (2018) remove the expansion-based correction and report consistency with a static universe to z = 5, while noting the galaxy-size evolution model limits the result. **[ESTABLISHED, contested]**
- **Verdict:** the Tolman test does not currently discriminate cleanly. E-528's exponent (−1) is far from the Lubin & Sandage values (2.6–3.4), so if that analysis holds, E-528 alone is disfavored. The audit cannot adopt either dataset without pre-registering which one is used **[OPEN]**.

### Attack C: Redshift–distance relation

- **E-528 prediction:** `1+z = exp[∫κ_γ dℓ]`. For constant κ, `z = e^{κD} − 1`, which is linear in D only at small z (`z ≈ κD`) **[DERIVED from E-528]**.
- **Test:** low-z slope fixes `κ = H₀/c`. The predicted distance–redshift relation at higher z then follows with **no free parameters**, and must be compared to the Hubble diagram.
- **Status:** the luminosity-distance formula implied by E-528 is not derived in the repo. The audit does not compute it, because the photon-number and energy-flux assumptions in E-528 need explicit specification first **[OPEN, next derivation]**.

### Attack D: Energy accounting and blackbody

- **A-115 §5 requirement:** closed static balance, with long-time equalities `⟨Q_γ→χ + Q_W→χ⟩ = ⟨Q_χ→ν + Q_capture⟩`.
- **External data:** the CMB is a near-perfect blackbody (COBE/FIRAS) **[ESTABLISHED]**.
- **Test:** E-528 defines `κ_γ(x, ν, χ, ∇χ)`, which depends on frequency. Frequency-dependent attenuation can distort a blackbody. A frequency-independent κ with conserved occupancy number preserves Planck shape, and the repo must show which case holds **[OPEN]**.
- **Verdict:** unresolved. The energy budget closes by construction in A-115 §5, which does not test the spectrum.

### Attack E: CMB temperature–redshift (not yet sourced)

Expansion predicts `T(z) = T₀(1+z)`. Static transport predicts something else. This test is listed for completeness. It needs a sourced measurement before it can be used **[OPEN, source needed]**.

### Attack F: W2's own predictions (unsourced)

W2 Part 9 gives values (breathing-mode fraction ≈ 0.01; `w ≈ −0.99` to `−1.01`) and states current constraints (breathing mode <10%; `w = −1.00 ± 0.05`). The derivations of these values are not in the document, and the sourcing is unverified **[OPEN, unsourced]**.

---

## 5. Contradictions register

| ID | Statement A | Statement B | Type | Resolution path |
|---|---|---|---|---|
| C1 | W2: scalar ψ primitive (S1–S3, S8) | A-115 and D-602: vector `u`/`ψ⃗` | **Hard contradiction** | Adopt vector. W2 must be rewritten. |
| C2 | W2: gravity is curvature of a lattice metric | A-115 §2 and UPDATED_64: gravity is the compression wake and relay | **Resolved in direction; W2 mechanism rejected** | Derive path capture and the "still distinguishable" boundary (§6, item 2). |
| C11 | E-532: finite wake is an isotropic kernel `e^{−r/σ}/r` with free σ | UPDATED_64: reach comes from distinguishability along relayed paths; no hand-inserted cutoff | **Hard contradiction** | Derive reach from the relay path; test whether any limit recovers E-532's kernel. |
| C13 | Owner: spacetime curvature is what the lattice is; wake, curvature, and displacement named separately in the audit | `D-415` translation: Newton/Einstein responses "must not be added again under the names wake, curvature, or displacement" | **Double-count risk; identity open** | Define one response variable. Owner to confirm: is the wake the same object as the curvature, or the cause of it? |
| C14 | Owner: everything is moving; no displacement without motion | A-101/A-102: displacement is measured against a reference ground state ψ₀ | **Owner answer: the lattice is zero. Resolved in direction; global vs. local zero open** | Decide whether zero is one global state or local zero at each point (the local reading matches "differs only in relation to local displacement"). |
| C12 | Intrinsic reach is set; apparent reach is masked by descendants' superposed displacement (owner direction) | D-415 MATH_GAPS: superposed body fields unresolved; D-401: screening term missing | **Gap** | Derive the superposition rule; test lone-body vs. populated-system reach; require Newtonian recovery. |
| C10 | GRAVITY_WAKE_NESTING: rotation cascades top-down from parent wakes | DARK_MATTER_TERMINOLOGY_CORRECTION: "no cascade inheritance" | **Repo-internal conflict** | Decide whether the wake is inherited from parents or only local; cannot both hold. |
| C3 | W2: dark energy is Λ = β/a² | A-115 §5: dark energy is static White Energy circulation, no Λ | **Accounting conflict** | T-Λ2 |
| C4 | E-528: no time stretch | Blondin et al.: time stretch present | **Observational conflict** | E-533 must derive the stretch with the shared κ |
| C5 | W2 energy density: no `χ²` term | A-115 energy density: `(K_χ/2)χ²` | **Structural conflict** | Include the compression term in any rewrite |
| C6 | W2: "✓" marks | W2: all checklist items open; no gate metadata | **Status conflict** | Treat as unproven |
| C7 | D-602: GREEN "verified" | D-602 §"What Remains to Be Verified": quantitative `ω/k = c`, Maxwell equations open | **Gate conflict** | Downgrade or complete the Phase 4 checks |
| C8 | A-115: GREEN | A-115 claim_gate_detail: YELLOW for static-loop equations | **Gate conflict** | Cosmology claims inherit YELLOW |
| C9 | A-115 §2: `M_eff` derived from source | A-115 §2: `M_eff` defined by matching to Newton | **Gap (fit, not prediction)** | Derive χ(r) from the source |

C1 and C2 must be resolved before any cosmology equation is rewritten. C3 and C4 are the physical tests the rewrite must pass.

---

## 6. Missing derivations (ordered)

1. Derive χ(r) from the A-115 sourced equation, with `K_eff` specified (A-115 §7, first Yellow requirement).
2. Derive the wake mechanism from the vector field: the path-capture term, the boundary test for "still distinguishable," and the Newtonian control recovery (C2). The top-down vs. local question (C10) must be settled first, because it fixes whether the wake is inherited.
3. Give the geometry equation for a static domain, including `a` and its relation to Λ (T-Λ1, T-Λ3).
4. Derive the E-528 luminosity-distance relation with explicit photon-number and energy-flux assumptions (Attack C).
5. Derive E-533's timing law `𝒯(v,Ξ)` so that the stretch exponent follows from the same κ_γ (Attack A).
6. Specify the frequency dependence of κ_γ and show the blackbody spectrum is preserved (Attack D).
7. Pre-register the Tolman dataset and analysis before computing (Attack B).

---

## 7. What is not done here

- No equation has been rewritten.
- No model has been chosen.
- No simulation has been run.
- The Blondin 6σ figure and the Lubin & Sandage and Lerner values come from secondary summaries and must be checked against the primary papers before any publication use.
- The E-528 Tolman exponent (−1) is this audit's calculation under stated assumptions, not a repo result.

## 8. Next step

W2 rewrite is gated on C1, C2, and C5 being resolved. The next task is item 1 in §6: derive χ(r) from the A-115 source equation. That derivation is the first place the static and expanding interpretations can be tested against the same equation.
