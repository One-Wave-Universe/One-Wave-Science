# Ledger s14 (11 files, all read in full)

## Solver synthesis (no node ID): One-Wave Unified Field: Satellite Validation   (`solvers/ONE_WAVE_UNIFIED_SATELLITE_VALIDATION.md`)
- Gate / lifecycle: Banner L1 "Evidence correction (2026-10-06): The satellite proof claims below are historical hypotheses, not established results." Footer L175 "Framework complete. Validation in progress. Publication ready". The body's "PROVEN" wording is overridden by the L1 correction.
- Upstream: D-409 (twelvefold close-pack lattice, L13, L152), C-319 (magnetic coupling / EM coherence, L62, L78, L90, L127, L141, L148). Downstream / cites: GALAXY_EXTERNAL_VALIDATION.md (L1), satellite_galaxy_validator_clean_systems.py, satellite_galaxy_validator_em_coherence_fixed.py, UNIFIED_SCALE_INVARIANT_GRAMMAR.md (L139-142).
- Core claim: L11 one scalar field ψ with one update rule. L26 "Child orbit = Parent wake geometry". L44 v_total = v_local + v_inherited. L86 "Dark matter = Extended ψ displacement from parent cascade, persisted via EM coherence". L105 gravity = "÷ (division) Pressure gradient (∇·ψ)".
- Equations: L11 ψ_i^{n+1} = ψ_i^n + (1-γ)(ψ_i^n - ψ_i^{n-1}) + β(<ψ_j^n> - ψ_i^n). L44 v_total = v_local + v_inherited. L48 β(r) = β₀ exp(-r/r_decay). L64 β_eff(r) = β₀ e^{-r/r_decay} f_EM(location). L115 E_n = ħ ω_n.
- Point / Path / Field role: Path: the child orbit is inherited from the parent wake (L26, L48). Field: the "gravity wake" is an organized ψ displacement (L24). Point: L33 "Planets sit in stellar wakes -> inherit rotation (tidal lock)", L117 "Electron phase-locks to nuclear wake at precisely ±ℏ/2". The file does not separate Point, Path and Field. Rotation and orbit are both called "inherited" from the wake.
- Magnetism / gravity / rotation link: f_EM (E+B coherence, C-319) multiplies the cascade coupling β (L64). EM coherence "persists" the gravity wake and so supplies the "dark matter" (L86-90). The gravity wake makes galaxies, stars and planets "inherit rotation" (L31-33).
- Open / parked / not-set items: C-319 refinement (χ² ~200-300 against a target of <200, L148-150). D-409 lattice integration (L152). Universality of β₀, r_decay and γ is unproven (L156-161).
- Conflicts:
  - L31-33: rotation is inherited from the gravity wake (planets "inherit rotation (tidal lock)"). This contradicts "Gravity does not start or affect point rotation" and "a thing keeps the point spin it has".
  - L44: v_total = v_local + v_inherited is a plain sum with no parent-to-child transport (R_c^T). This contradicts "Transport first, then add".
  - L64, L86-90: magnetic/EM coherence scales the gravity-wake coupling and makes the "dark matter" gravity. This contradicts "Magnetism does not become gravity". The canonical form is g = -α K_L ∇χ with K_L = I + κ_R R, and it has no f_EM factor.
  - L117: tidal lock is called wake phase-locking. The canonical Bound lattice rule says shared organization, with resistance = mass / organization.
  - L105: gravity as "∇·ψ pressure gradient" is not the canonical g = -α K_L ∇χ form.
  - L54, L56, L169 "PROVEN", "not speculative": these are overridden by the L1 evidence correction.

## Solver README (no node ID): Algorithm Zero Physics Engine & Emergence Encyclopedia   (`solvers/README_ALGORITHM_ZERO.md`)
- Gate / lifecycle: L3 "Validated ✓ All 7 tests passing". L352 "Ready for experimental validation". No node gate.
- Upstream: CLAUDE.md, GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md (L332-334). Downstream / cites: algorithm_zero_physics_engine.py, algorithm_zero_emergence.py, test_algorithm_zero_complete.py, unified_phase_solver.py, three_body_solver.py. No node IDs cited.
- Core claim: L36 six-step cycle BEGIN -> MOVE₁ -> HOLD -> MOVE₂ -> BREAK -> REPEAT, "identical at all scales" (L47). L68 "Parent structures create organized field wakes that child structures inherit". L92 wake "Causes child to phase-lock to parent's frequency".
- Equations: L54 the same ψ update rule (γ=0.05 and β=0.15 by default).
- Point / Path / Field role: Point: L120 "Spin ½: Phase-lock to nuclear wake at ±ℏ/2", L123 "Magnetic moment: Emergent from phase-lock rotation pattern", L325 "Spin Quantization: Wake-induced phase-lock rotation patterns". Path: orbits are "discrete, quantized" through phase-lock (L97). Field: the wake is a "high-pressure compression trail" (L88). The three rates are not separated.
- Magnetism / gravity / rotation link: L132 "Rotation: Top-down gravity wake induces coordinate rotation". L133 "Magnetic fields: Vortex formation from phase-locked structure".
- Open / parked / not-set items: the Future Work list (L343-348). Energy conservation is checked only to ±20% (L220).
- Conflicts:
  - L132: the gravity wake induces rotation. This contradicts "Gravity does not start or affect point rotation".
  - L120, L325: spin is induced by the wake. This contradicts "a thing keeps the point spin it has; it does not start one on its own".
  - L144 "Universe expansion: Overall cascade energy flow". This contradicts "No expansion, no scale factor".
  - L319 claims the three-body problem is "solved" by wakes. This is an unsupported claim, not a canonical-rule conflict.

## Solver README: One-Wave Dispersion Relation Validator (D-600, D-602)   (`solvers/README_DISPERSION_VALIDATOR.md`)
- Gate / lifecycle: L7 "Gate: GREEN", L5 "PRODUCTION READY". The D-600 result is "REVIEW" (L258), with error 0.51 (L138).
- Upstream: D-600, D-601, D-602, D-411 (domain separation, L278), FOUR_INTERACTIONS.md. Downstream / cites: dispersion_validator.py, dispersion_visualizer.py, test_dispersion_validator.py.
- Core claim: L17 the update rule "generates two distinct mode families without external assumption". L39 the vector extension produces "E-like and B-like modes via the sign flip in the Laplacian identity".
- Equations: L23-24 λ² - C(k)λ + (1-γ) = 0, C(k) = 2 - γ + β(cos φ - 1). L43 ψ⃗^{n+1} = ψ⃗^n + (1-γ)(ψ⃗^n - ψ⃗^{n-1}) + β[∇(∇·ψ⃗) - ∇×(∇×ψ⃗)]. L47-48 C_long = 2 - γ - βk², C_trans = 2 - γ + βk². L53 ∇²A = ∇(∇·A) - ∇×(∇×A). L121 stability requires β < 1.
- Point / Path / Field role: Field only. The curl term ∇×(∇×ψ⃗) is labelled "B-like", the transverse mode (L48-56). Point and Path: none stated.
- Magnetism / gravity / rotation link: the B-like mode is the transverse/curl part of the vector field (L55). No link to gravity or rotation is stated.
- Open / parked / not-set items: Maxwell verification (Phase 3). The D-600 error is not yet under 0.01 (L183). The vector field simulator is not yet implemented (L187).
- Conflicts: none against the canonical rules. Internal inconsistency: "Gate: GREEN" (L7) sits beside D-600 "REVIEW" (L258), and "PASS" thresholds are not met.

## Solver status: One-Wave Solvers Repair Status 2026-10-05   (`solvers/REPAIR_STATUS_2026_10_05.md`)
- Gate / lifecycle: C-319 hadron mechanism "GREEN (mechanism correctly implemented)" (L70). BROWN items are listed at L290-294. Branch integrate/algorythm-zero-rabbit-circle-unified (L310).
- Upstream: G-749 (Point Rotation, L20, L190, L287, L292), C-319 (L21, L29-71, L182, L188-190, L279), Chapter 12 Gravity (L22, L284), Chapter 13 E-M Duality (L23), Chapter 15 Higgs (L183). Downstream / cites: hadron_mass_predictor.py, dispersion_validator.py, high_energy_validator.py, observational_data_loader.py, galaxy_rotation_validator.py, test_strange_hadrons.py. Data: Sofue 1999, Corbelli & Salucci 2000, Chemin 2009.
- Core claim: L20 "G-749 (Point Rotation): Angular momentum kinematics". L22 "Chapter 12 (Gravity): Gradient response, does not initiate spin". L23 "Chapter 13 (E-M Duality): Magnetism = rotational pressure component". L63 "'Magnetism opens the point' = Magnetic pressure modulates path accessibility K_L". L287 "Angular momentum comes from initial knot structure (G-749)".
- Equations: L55 E_mag = -κ_R × R × pressure × volume_factor, with κ_R = 0.350 GeV. L279 R = λ_B W_B + λ_ω W_ω. L280 K_L = I + κ_R R. L80-92 ω = i ln(λ), corrected from -i ln(λ).
- Point / Path / Field role: Point: G-749 owns angular momentum, which comes from the initial knot structure (L287). The inertia tensor is "declared in G-749, not derived" (L292). Path: K_L "path accessibility" (L280). Field: none separately stated. The file maps "opens the point" onto path accessibility, which mixes the Point and Path roles.
- Magnetism / gravity / rotation link: L284-288 "Why gravity doesn't start spin: Gravity is gradient response ... Passive mechanism, not active initiator ... Magnetic pressure modulates confinement, gravity provides stability". Magnetism is the "rotational pressure component" (L23, L44) and increases binding.
- Open / parked / not-set items: calibration of λ_B, λ_ω and κ_R (L71, L180-181, L291). Inertia tensor derivation (L292). How G-749 connects to C-319 (L190). Separating gravity from magnetic opening (L191). The pressure model fails on real data: RMS 193 km/s (L226), and MW to M31 parameter transfer gives χ² ≈ 1200 (L249-259). LIGO and CERN connectors are not done.
- Conflicts:
  - L63: "Magnetism opens the point" is redefined as path accessibility K_L. Canonically, an opened point means an open magnetic gradient with dL/dt = 0, which is a Point property, not a Path weight.
  - L55, L180: κ_R is assigned 0.350 GeV, and the file says it is to be tuned from hadron masses. This contradicts "kappa_R not set".
  - L60-62: magnetic pressure "increases lattice resistance -> stronger binding". This is not the canonical resistance = mass / organization, and it is not derived.
  - Consistent with the canonical rules: gravity does not start spin (L22, L284-287).

## Solver index: One-Wave Framework Solvers Complete Index   (`solvers/SOLVER_INDEX.md`)
- Gate / lifecycle: L235 "Framework proven across quantum -> atomic -> galactic scales". No node gate. The index has no evidence-correction banner. The banner on ONE_WAVE_UNIFIED_SATELLITE_VALIDATION.md L1 applies to the same satellite claims.
- Upstream: C-319 (L21, L30, L57, L162, L223), D-409 (L118, L163). Downstream / cites: ONE_WAVE_UNIFIED_SATELLITE_VALIDATION.md, MASTER_SOLVER_INDEX.md, cascade_neural_router.py, satellite_galaxy_*.py, atomic_spectra_cascade_resonance.py, galaxy_rotation_c319_magnetic_coupling.py, molecular_geometry_harmonic_resonance.py, exoplanet_resonance_statistics.py, coupling_constants_from_lattice.py.
- Core claim: L30 "Cascade inheritance universal. EM coherence (C-319 magnetic coupling) determines signal preservation." L41 "Electron phase-locks to wake resonances (same as tidal locking)". L98 "Planets inherit orbital geometry from stellar wake". L119 "+ (EM), − (strong), × (weak), ÷ (gravity)". L229 "Unification complete".
- Equations: L14 β(r) = β₀ exp(-r/r_decay). L42 E_n = -13.6/n² eV.
- Point / Path / Field role: Path: orbits and orbital resonances are inherited from the wake (L98-99). Point: none stated directly. Field: none stated.
- Magnetism / gravity / rotation link: EM coherence f_EM (C-319) modulates the galactic cascade signal (L26-30). Gravity comes from "lattice curvature" (L126).
- Open / parked / not-set items: galaxy_rotation_c319_magnetic_coupling.py is in progress (χ² < 200 target). D-409 volumetric effects. Internal inconsistency: the tables call validators "✓ Proven" (L69, L92) while L146-147 and L165-168 call them "to build".
- Conflicts:
  - L30, L57-65: C-319 magnetic coherence is used as the enhancement that bridges the gravity / rotation-curve gap. This contradicts "Magnetism does not become gravity" (the canonical route is K_L path weighting on ∇χ only).
  - L41: tidal locking is treated as wake phase-locking. The canonical Bound lattice rule says shared organization, with resistance = mass / organization.
  - L229 "Unification complete" and the "Proven" labels conflict with the 2026-10-06 evidence correction.

## A-115 derivation note: Source-Constitutive Connection Derivation   (`solvers/SOURCE_CONSTITUTIVE_DERIVATION.md`)
- Gate / lifecycle: L4 "YELLOW derivation in progress". L342 "requires numerical implementation and independent scale validation before astronomy claims".
- Upstream: A-115 (Unified Compression Field), E-532 (bound/unbound criterion, finite wake), A115_STATIC_SOURCE_DIAGNOSTIC, GALAXY_EXTERNAL_VALIDATION (L6), A-109 (inertia/ρ_u, L42), C-309 (friction/μ_u, L43), A-105 (shear S_u, L45), E-531 (dual-harmonic free field, L97), E-529 (neutrino-like return channel, L251), C-320 (K_L = I + κ_R R, L253-257). Phase 6B is also cited (L33, L246). Downstream / cites: A-115 numerical solve (L310).
- Core claim: L59 "gravity is the gradient of compression, not a separate force". L65-67 "compact radial J_r ... g = 0 exterior ... the source must be non-compact". L255 "If C-320 introduces K_L = I + κ_R R, the mandatory recovery K_L -> I must hold".
- Equations: L30 the ψ update rule. L39 ρ_u ∂²u/∂t² + μ_u ∂u/∂t - K_χ ∇(∇·u) - S_u ∇²u + ∂V_b/∂u = J_source. L53 χ = -∇·u. L57 g₀ = -α_g ∇χ. L63 χ'(r) = J_r/(K_χ + S_u). L76 bound criterion I₃ > I₁/2 and |u| > u_floor. L87 W(r) = e^{-r/σ}/r. L157-159 Φ → -GM_eff/r. L173 J_r ∝ -(K_χ+S_u)/r². L267 J_r = A/(σ²+r²)^{3/2} + A_tail e^{-r/σ}/r. L277 V_b = (k₀/2)|u|². L244 E_total = ∫[ρ_u/2 |∂u/∂t|² + K_χ χ²/2 + S_u |∇u|² + V_b] dV.
- Point / Path / Field role: Field: compression χ and its gradient carry gravity (L53-59). The wake kernel W(r) is the range of the binding influence (L87-93). Path: K_L as magnetic path weighting (L225, L255). Point: none stated.
- Magnetism / gravity / rotation link: L225 "if K_L = I (no magnetic modification), the simpler source law (without magnetic path-weighting) may be insufficient at galaxy scale". L257 "The derived source J_r should work for K_L = I first, before testing magnetic modifications." No rotation link.
- Open / parked / not-set items: A, A_tail, σ, ρ_u, μ_u, K_χ, S_u, k₀ and α_g are not set and must not be fitted to galaxies (L283-292). The form of V_b is a candidate only. The source form is not shown to be unique (L318).
- Conflicts: none. It is consistent with g = -α K_L ∇χ, with K_L → I recovery, and with κ_R not set. Minor note: L141 says "cubic confinement" but gives quadratic and quartic forms.

## Solver receipt: Resistance/change timing: executed propagation control   (`solvers/TIME_RESISTANCE_PROBE.md`)
- Gate / lifecycle: L101-102 "Decision: accepted propagation receipt; PARTIAL on the physical timing mechanism". Existing metadata gates are unchanged (L9).
- Upstream: E-533 (interpretation owner, L3, L111), A-114 (recurrence, L4, L8), Book1 Ch16a, C-309, E-509, E-528, Book5 Ch6, AGENTS.md, General Reference Rules (L8-9). PR #193 (native compression candidate, L96, L115). Downstream / cites: time_resistance_probe.py, time_resistance_results.json.
- Core claim: L65-69 "Increasing gamma does not universally slow carrier oscillation ... does not yield the proposed universal slowing mechanism". L84-88 "No closed superfluid energy budget, mass, bound-clock recurrence, Lorentz recovery or shared redshift/timing law is established." L115 PR #193 "excludes stable nontrivial static equilibria for that exact real unconstrained law".
- Equations: L17-18 psi_(n+1) = (2-γ) psi_n - (1-γ) psi_(n-1) + β[(psi_(i+1)+psi_(i-1))/2 - psi_i]. L22 z² - [2-γ+β(cos k-1)]z + (1-γ) = 0. L25-26 ω = -arg z, decay = -log|z|, v_g = dω/dk. L72 c_longwave = sqrt(β/2) = .5.
- Point / Path / Field role: Path: packet transport and group speed (L30-34). L86 says "circulation, weave ... not implemented". Point and Field: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the field-difficulty Xi is not derived (L106). The self-held time-periodic excitation search is the next permitted step (L103-108, L117). No Lorentz law, mass or universal resistance coefficient is established (L119).
- Conflicts: none. It cites E-528 and makes no expansion claim.

## Calibration summary (no node ID): Week 1 Calibration Completion Summary   (`solvers/WEEK_1_COMPLETION_SUMMARY.md`)
- Gate / lifecycle: L259 "Gate: GREEN ✓". Frontmatter status "WEEK 1 COMPLETE" (L4).
- Upstream: none cited as nodes. Downstream / cites: yukawa_matrix_solver.py, hadron_knot_geometry.py, CALIBRATION_ROADMAP.md, LATTICE_VALIDATION_REPORT.md.
- Core claim: L34 "MASS_SCALE_FACTOR converts lattice frequency units to physical mass units". L239 "The mass gap between generations ... isn't emergent from the lattice — it's built into the initial conditions as GENERATION_HIERARCHY". L63 the ratio κ_T/σ_T "directly sets the equilibrium knot size".
- Equations: L93 m = suppression × ω × color_factor × hierarchy_factor × MASS_SCALE_FACTOR × 511.0 MeV, with ω = (1-γ)β. L120 R = base_radius × √(κ_T/σ_T) × vortex_factor. vortex_factor = 1.0 + 0.1(num_vortices - 2). Parameters: MASS_SCALE_FACTOR = 0.0114, GENERATION_HIERARCHY = [1, 207, 3477], σ_T = 0.012 GeV, κ_T = 0.010 GeV, τ_T = 7.54 MeV/fm, and Higgs criticality β = 0.8914, γ = 0.0966.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the 3D lattice extension and hadron binding energies are planned for Week 2.
- Conflicts: none against the canonical rules. Evidence-class concern: the masses are fitted (MASS_SCALE_FACTOR is set from the electron target, and the hierarchy is put in by hand), yet they are labelled "PERFECT" and GREEN.

## A-115 test report: A-115 Galaxy Validation, Derived Source Parameters vs MW Rotation Data   (`solvers/a115_galaxy_validation_report.md`)
- Gate / lifecycle: L5 "Test Status: COMPLETE". The result is negative: "systematic disagreement" (L11).
- Upstream: A-115 static compression field. Data: Sofue 1999, Battaglia 2005, MW DR3+ 2023 (45 points, 5.25 to 27.25 kpc). Downstream / cites: none.
- Core claim: L76 "The amplitude law derivation gives dimensionally compensated exterior response ratios but not the radial structure needed for galaxies". L104-106 "No single amplitude scaling can fix 127 km/s errors".
- Equations: L31 (K_χ + S_u)∇²χ = ∇·J_r. L32 a(r) = -α_g dχ/dr. L33 v_c = √(a r). L41 J_r = -[(1-w)J_core + w J_tail]. Parameters: σ_core = 0.5, σ_tail = 2.0, w = 0.4, layer 12. Result: RMS 44.46 km/s, MAPE 18.19%.
- Point / Path / Field role: Field: compression χ and its gradient (L31-32). Point and Path: none stated. "Rotational inertia / angular momentum" is listed as possible missing physics (L153-154).
- Magnetism / gravity / rotation link: L155 "Magnetic fields (referenced in A-115 but not solved here)". The K_L = I branch is implied.
- Open / parked / not-set items: the 2D disk variant, the physical unit system (K_χ, α_g), the time-dependent wake, and a comparison with MOND and CDM (L188-192).
- Conflicts: none against the canonical rules. Internal issues:
  - L40-42: the sign was flipped so the solver gives "outward acceleration matching galaxy gravity". Galactic gravity is inward, so the sign convention is unclear.
  - L9 "Single free parameter (overall amplitude scale), no parameter fitting" contradicts itself.

## Task packet: Gemini adversarial review, dimensional interaction ladder   (`tasks/gemini/dimensional-interaction-ladder-001.md`)
- Gate / lifecycle: review task only. "do not edit the repository" (L3).
- Upstream: repo cosmology and dimensional files (unspecified). Downstream / cites: none.
- Core claim: L9-11 the sequence 3-1(0)1-6, 6-1(0)1-12, 12-1(0)1-24. L13 "1(0)1 is intended as the invariant interaction/reference structure between dimensional stages". L18 asks whether 3 -> 6 -> 12 -> 24 is "derived ... or currently assumed".
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: whether the 3, 6, 12, 24 ladder is derived is open. The missing lemma is requested (L21).
- Conflicts: none.

## Task packet: Gemini Jetson review, physics-engine-foundation-001   (`tasks/gemini/physics-engine-foundation-001.md`)
- Gate / lifecycle: review mode, "Do not edit files" (L32). "Do not treat One-Wave as proven" (L8).
- Upstream: G-766 (discrete lattice dispersion and octave emergence), D-415 (hexagonal lattice interaction dynamics), D-413 (ground lattice orbital restoring simulation), ENGINE_EVIDENCE_PIPELINES.md, ASSUMPTION_TRANSFORMATION_CONTRACT.md, sims/24-1-sandbox/GOLD_STANDARD.md, sims/00-lattice-primitive/README.md, Engine/README.md, Engine/WAVE_TRANSFORM.md, ../Builds/two-ai-dialogue/ONE_WAVE_LENS.md (L11-20). Downstream / cites: CERN/CMS and GWOSC as held-out adapters (L29).
- Core claim: L7 "One-Wave has no fundamental particles; conventional particle names are observable-layer labels". L27 asks for the first validation job: energy accounting, zero-input control, refinement, anisotropy, and a receipt.
- Equations: none.
- Point / Path / Field role: none stated. D-413 "orbital restoring" is cited by name only.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the authoritative kernel and the missing accounting equations (L25-26).
- Conflicts: none.

## Slice summary

(a) Nodes and chapters in the slice that bear on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance or lattice organization:
- G-749 (cited in REPAIR_STATUS L20, L287, L292): point rotation and angular momentum come from the initial knot structure. The inertia tensor is "declared, not derived".
- C-319 (REPAIR_STATUS, SOLVER_INDEX, ONE_WAVE_UNIFIED): magnetic lattice reorganization R = λ_B W_B + λ_ω W_ω and K_L = I + κ_R R. The solver docs misuse it as EM coherence f_EM that scales gravity and cascade coupling, and as hadron binding with κ_R = 0.350 GeV.
- C-320 (SOURCE_CONSTITUTIVE L253-257): K_L = I + κ_R R with mandatory recovery K_L -> I. Consistent with the canonical rules.
- Chapter 12 Gravity (REPAIR_STATUS L22, L284): gravity is a gradient response and does not initiate spin. Consistent.
- Chapter 13 E-M Duality (REPAIR_STATUS L23): "Magnetism = rotational pressure component".
- Chapter 15 Higgs (REPAIR_STATUS L183): cross-check only.
- A-115 (SOURCE_CONSTITUTIVE, a115 report): g₀ = -α_g ∇χ and χ = -∇·u. A compact source gives zero exterior gravity. The derived source fails the MW curve structurally.
- A-109 (inertia ρ_u), A-105 (shear S_u), C-309 (friction μ_u): A-115 coefficients (SOURCE_CONSTITUTIVE L42-45). C-309 is also cited by TIME_RESISTANCE.
- E-532: bound/unbound criterion I₃ > I₁/2 and wake kernel e^{-r/σ}/r, which sets the range of the binding influence.
- E-531 (free-field residual), E-529 (return channel): residual and propagation.
- E-533, A-114, E-509, E-528 (TIME_RESISTANCE): transport, damping and timing. γ is not a universal "resistance" slowing.
- D-409 (twelvefold close-pack lattice) is the lattice organization base for the cascade (ONE_WAVE_UNIFIED L13, SOLVER_INDEX L118).
- D-600 and D-602 (dispersion): the transverse curl mode is "B-like", which is a Field curl term. D-601 and D-411 are cited.
- G-766, D-413, D-415 (physics-engine task): lattice dispersion, orbital restoring and hexagonal dynamics are cited by name only.

(b) Conflicts found:
1. ONE_WAVE_UNIFIED_SATELLITE_VALIDATION.md L31-33: rotation is inherited from the gravity wake. This violates "gravity does not start or affect point rotation" and "a thing keeps its spin".
2. ONE_WAVE_UNIFIED L44: v_total = v_local + v_inherited is a sum without transport. This violates "Transport first, then add".
3. ONE_WAVE_UNIFIED L64, L86-90, and SOLVER_INDEX L30, L57-65: EM/magnetic coherence (C-319) scales gravity and cascade strength and supplies the "dark matter". This violates "Magnetism does not become gravity".
4. ONE_WAVE_UNIFIED L117 and SOLVER_INDEX L41: tidal lock is called wake phase-locking. The canonical bound-lattice rule is shared organization, with resistance = mass / organization.
5. ONE_WAVE_UNIFIED L105: gravity is "∇·ψ pressure gradient" rather than g = -α K_L ∇χ.
6. README_ALGORITHM_ZERO.md L132: the gravity wake induces rotation. L120 and L325: spin is induced by the wake.
7. README_ALGORITHM_ZERO.md L144: "Universe expansion". This violates "no expansion".
8. REPAIR_STATUS_2026_10_05.md L63: "Magnetism opens the point" is redefined as path accessibility K_L, which mixes Point and Path.
9. REPAIR_STATUS L55 and L180: κ_R = 0.350 GeV is set and is to be tuned. This violates "kappa_R not set".
10. REPAIR_STATUS L60-62: magnetic pressure "increases lattice resistance". This is not the canonical resistance = mass / organization.
11. "Proven", "GREEN" and "Unification complete" labels conflict with the 2026-10-06 evidence correction and with the files' own data: SOLVER_INDEX L229 and L235, README_DISPERSION L7 against L258, and WEEK_1 L259 (masses that were fitted).

(c) Cross-references to nodes or files outside the slice that matter for point rotation or magnetism:
- Nodes: G-749, C-319, C-320, A-115, A-109, E-532, E-533, D-409, D-602, D-413.
- Files: Nodes/E-533_Superfluid_Transport_Time_Dilation.md; solvers/GALAXY_EXTERNAL_VALIDATION.md; A115_STATIC_SOURCE_DIAGNOSTIC; FOUR_INTERACTIONS.md; MASTER_SOLVER_INDEX.md; UNIFIED_SCALE_INVARIANT_GRAMMAR.md.
- Code that implements the C-319 coupling: hadron_mass_predictor.py and galaxy_rotation_c319_magnetic_coupling.py.
- Code that implements the f_EM misuse: satellite_galaxy_validator_em_coherence*.py.
- PR #193 (native compression candidate). Book1 Ch16a. Book5 Ch6.
