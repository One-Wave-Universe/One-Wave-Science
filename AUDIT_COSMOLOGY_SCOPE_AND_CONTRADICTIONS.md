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

**Gravity mechanism (C2): resolved in direction, derivation open.** Gravity is not lattice curvature. Per the project owner's direction, and consistent with `UPDATED_64_GRAVITY_IS_THE_WAKE_AND_THE_RELAY.md` (interpretation lock, 2026-10-05) and A-115 §2, gravity is the extended compression wake: the displaced medium a parent creates, which smaller displacements are carried along and trapped in as they move through its paths. W2's curvature mechanism is therefore out of scope for the rewrite. What is not yet derived: the path-capture term (A-115 `Q_capture`; E-09 capture fraction κ), the boundary test for "still distinguishable" (UPDATED_64 states it is not derived and no cutoff radius may be inserted by hand), and recovery of the Newtonian sum as the control **[PROPOSAL / OPEN]**.

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
