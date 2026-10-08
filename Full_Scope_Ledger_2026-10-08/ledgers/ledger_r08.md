# Ledger r08 — root docs (PHASE_5_*, PPF, PRESENTATION, PRIMITIVE)

Repo: /home/user/One-Wave-Science. 12 files, each read in full. None of the 12 files is itself a node; each section lists every node / chapter / doc it cites or defines.

---

## PHASE_5_GRAVITY_HIGGS_SPECTRUM — Phase 5: Gravity, Higgs, and the Complete Particle Spectrum   (`PHASE_5_GRAVITY_HIGGS_SPECTRUM.md`)
- Gate / lifecycle: "Status: Framework Definition (Ready for Implementation)" (L3); target Q1 2027 (L4); all roadmap checkboxes unchecked (L119-133, L271-284, L565-591). Proposal / speculation, not derived.
- Upstream: Phases 1-4 (L5, L11); A-115 "Compression Field" (L29); D-602 dispersion relations (L149-156); W2 blocker (W metric) (L21, L42). Downstream / cites: planned `solvers/gravity_validator.py`, `solvers/higgs_validator.py`, `solvers/weak_validator.py`, `solvers/strong_validator.py`, `solvers/quark_spectrum_solver.py` (L569-581); Manuscripts 2/3 (L589-590, L659-661).
- Core claim: "Gravity: Emerges from compression/rarefaction of the lattice itself (W2 resolved)" (L13); "gravity is lattice deformation itself" (L27); "Compression and rarefaction of the lattice create curvature that acts like gravity" (L40); Higgs "a composite resonance of EM modes at criticality" (L147); W/Z as longitudinal EM modes (L309); strong force from third derivatives (L339-358).
- Equations: ρ_i ∝ ∇·ψ_i; κ_i ∝ ∇²(∇·ψ_i) (L36-37); T^μν = ρ_μν + flow_μν + pressure_μν (L50); G^μν + Λg^μν = (8πG/c⁴) T^μν (L59); ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + β(⟨ψⱼⁿ⟩-ψᵢⁿ) + κ_i·ψ_i (L67); C_long(k) = 2 - γ - βk², C_trans(k) = 2 - γ + βk² (L154-155); ω_long(k→0) ≈ √[(1-γ) - βk²] (L161); m_H² ∝ (1 - β/β_crit) Λ_cutoff² (L179); m_H = √[(β_crit - β)(Λ_cutoff²/2)] (L187); y_f ∝ amplitude / criticality distance (L201); V = λ(H†H)² (L226); m_W/m_Z = cos θ_W, θ_W ≈ arctan(√[1 - β_long/β_trans]) (L320-324); α_s(Q²) = α_s(m_Z)[1 + β_0/(2π) ln(Q²/m_Z²)] (L364); F ~ α_s/r², F ~ σ·r (L461-462).
- Point / Path / Field role: none stated under those names. Field-side: gravity is placed in lattice compression/curvature (a field gradient). No point rotation, spin, L or inertia treatment.
- Magnetism / gravity / rotation link: gravity = lattice compression curvature through Einstein equations (L27-76); "Frame-dragging corrections in rotating black hole geometry" (L94). No magnetism-to-gravity link stated; no point-rotation link.
- Open / parked / not-set items: W2 metric "not yet explicitly derived" (L44); every roadmap item open; β_crit ≈ 0.95, Λ ≈ 350 GeV picked to give 125 GeV (L181-188); risks table (L637-643).
- Conflicts:
  - L13, L27, L40, L57-76: gravity built from lattice compression plus Einstein equations / Ricci curvature. The canonical form is g = -alpha K_L grad chi, which reduces to the A-115 baseline at R=0. A-115 is cited (L29), but as the source of GR-style curvature, not as the K_L baseline.
  - L76, L103-113, L554: the cosmological constant Λ appears as "bare lattice tension", with "Cosmological Acceleration (Dark Energy...)" and w = -1 tests. This conflicts with the no-expansion / no-scale-factor rule. L621 also proposes testing against FLRW spacetime.
  - L92-99: "Schwarzschild Precession (Mercury-like)" is framed as GR frame-dragging. The canon treats Mercury's 3:2 as bound-lattice point-rate locking. This is a mild conflict of framing.

## PHASE_5_HARMONIC_LOCKING_REFOCUS — Phase 5: Harmonic Locking Unification   (`PHASE_5_HARMONIC_LOCKING_REFOCUS.md`)
- Gate / lifecycle: "Status: ✓ REFRAMED → Single Unified Principle" (L4); "REFOCUS COMPLETE" (L229). Narrative reframing. Its results are solver claims, not derivations.
- Upstream: the four Phase 5 solvers (electron g-2, three-body, triple-alpha, gravity) (L11-17). Downstream / cites: manuscript Section 5 rewrite (L162-186). No node IDs cited.
- Core claim: "What is the next stable locking pattern at this boundary?" (L20); "Excitations couple at boundaries. Boundary geometry determines outcome" (L22, L223-225); gravity is "boundary coupling at the lattice cutoff" (L106).
- Equations: G ∝ lattice_coupling / Λ² (L101); ∇²P as curvature (L100); scale ratio 10¹⁹/10² = 10¹⁷ (L102); a_e = 1.1596521818 × 10⁻³, g_SO = 0.5 (L52-53).
- Point / Path / Field role: none stated. "Field geometry changes locally at boundary" (L33) is the only field-side statement.
- Magnetism / gravity / rotation link: magnetic moment a_e "emerges" from the Solid-Liquid boundary (L53). Gravity comes from the pressure Laplacian and lattice metric, and "Einstein equations emerge" (L98-109). No rotation link. The "locking" here is harmonic/boundary locking, not the canonical bound-lattice point-rate locking (no Moon/Mercury).
- Open / parked / not-set items: experimental priorities 1-4 (L193-207).
- Conflicts: L98-109 places gravity in the pressure Laplacian / Ricci / Einstein form rather than g = -alpha K_L grad chi. L59 claims "Predicts Fermilab g-2 exactly (0 ppm)". See the note under QUANTITATIVE_RESULTS: that value is the QED reference passed through unchanged, which is an evidence-gate problem rather than a canonical-rule conflict.

## PHASE_5_IMMEDIATE_PRIORITIES — Phase 5 Immediate Priorities — Next Steps   (`PHASE_5_IMMEDIATE_PRIORITIES.md`)
- Gate / lifecycle: "Status: Ready for implementation" (L3, L246). Plan only.
- Upstream: W2 (L12); Phase 1-4 (L208); "Phase diagram (P, E)", "Five scales × five states" (L211-212); cascade mystery map (L213). Downstream / cites: `solvers/gravity_emergence_validator.py` (L27), `solvers/triple_alpha_solver.py` (L53), `solvers/g_factor_validator.py` (L85), ThreeBodyPressureField (L104).
- Core claim: "W2 Gravity is the keystone—everything depends on it" (L171); "Once gravity emerges from pressure, everything else cascades" (L232).
- Equations: G_μν = (8πG/c⁴)T_μν (L22); ∇²P → Ricci (L18); β=0.8914, γ=0.0966 (L74); α_OW/α_SM ≈ 19.6× (L73).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: gravity from the pressure field P(r) through Ricci / Einstein (L16-30). Galaxy rotation "without dark matter" is listed as a test (L30, L200). No magnetism link, no point-rotation link.
- Open / parked / not-set items: all success-criteria boxes unchecked (L143-165); galaxy-rotation fit deferred (L200).
- Conflicts: L16-24 and L232 put gravity in the pressure Laplacian and Einstein equations, not g = -alpha K_L grad chi. L194: "CMB power spectrum from early-universe phase dynamics" implies a cosmology with an early universe. That is a mild tension with the no-expansion rule (not explicit).

## PHASE_5_MANUSCRIPT_NARRATIVE — Phase 5 Manuscript Narrative: Harmonic Locking Unification   (`PHASE_5_MANUSCRIPT_NARRATIVE.md`)
- Gate / lifecycle: "Status: Ready for Section 5 Integration" (L6, L232). Draft manuscript text.
- Upstream: PHASE_5_SOLVER_ATTACK_VECTORS.md (AV-1, AV-2) (L158-172); Phase 4 lattice cutoff (L129). Downstream / cites: PRL submission on Nov 4, 2026 (L228). No node IDs.
- Core claim: "excitations couple at phase boundaries, and boundary geometry determines the outcome" (L12); "The One-Wave lattice itself is spacetime. Pressure field dynamics on the lattice creates effective curvature in particle trajectories" (L120).
- Equations: a = -∇P/m (L65); ∇²P → Ricci tensor (L123-124); M_P ~ 1/a ~ 10¹⁹ GeV, Λ ~ 100-300 GeV, ratio 10¹⁷ (L129-131); a_e values (L47-49).
- Point / Path / Field role: none stated. The three bodies are "pressure extrema in a shared field" (L65), which is field-side.
- Magnetism / gravity / rotation link: anomalous magnetic moment from a boundary "field gradient" (L41, L52). Gravity from the pressure Laplacian and Einstein equations (L119-134). Prediction: "Gravity constant varies with lattice scale" (L190). No rotation link.
- Open / parked / not-set items: figures and supplementary material still owed (L224-233).
- Conflicts: L119-126 gives gravity as Ricci / Einstein from ∇²P, not g = -alpha K_L grad chi. L65 gives a = -∇P/m as the gravitational-type acceleration. In the canon, grad chi plays this role, gated by K_L.

## PHASE_5_QUANTITATIVE_RESULTS — Phase 5: Quantitative Results Summary   (`PHASE_5_QUANTITATIVE_RESULTS.md`)
- Gate / lifecycle: "READY FOR MANUSCRIPT INTEGRATION" (L186). Tables of solver outputs.
- Upstream: Phase 4 dispersion (lattice cutoff) (L102). Downstream / cites: manuscript Section 5 (L3, L188). No node IDs.
- Core claim: the electron g-2 "matches Fermilab 2021 to machine precision without parameter tuning" (L23). However, L12-13 show the One-Wave prediction equals the "QED baseline (reference)", which was "Incorporated into prediction". The match is therefore the input passed through (evidence-gate issue).
- Equations: a_e = a_e_ref × (g_SO / 0.5) (L20); g_eff = -∇P / m (L98); R_μν from ∇²P (L96); G ∝ α_lattice / Λ² (L100); M_P ~ 1/a (L103); rate 10⁻⁴² × 10⁶ = 10⁻³⁶ (L82).
- Point / Path / Field role: none stated. g_SO is described as "Spin-orbit lattice coupling" (L21), but no point/path split is made.
- Magnetism / gravity / rotation link: magnetic moment from phase-boundary coupling (L12-23). Gravity: "Lattice deformation | Pressure field gradient ∇P | Effective metric g_μν" (L95); "Equivalence principle | Inertial mass coupling to field | m_inertial = m_gravitational" (L99).
- Open / parked / not-set items: G only "Parametrized" (L100); falsification table (L153-159).
- Conflicts: L95-100 put gravity in the pressure gradient and Ricci curvature, not g = -alpha K_L grad chi. L99 derives inertial mass from coupling to the gravitational pressure field. The canon has resistance = mass / organization, and gravity does not touch point rotation or inertia.

## PHASE_5_SESSION_SUMMARY_2026_10_04_CONTINUATION — Phase 5 Session Summary (Oct 4, 2026 continuation)   (`PHASE_5_SESSION_SUMMARY_2026_10_04_CONTINUATION.md`)
- Gate / lifecycle: "Framework complete, First solvers deployed" (L6, L352). Session log.
- Upstream: W2 and W1 "Mirror wells geometry" (L103-104); Phase 4 electron mass (L114). Downstream / cites: `solvers/unified_phase_solver.py` (L14), `solvers/galaxy_rotation_validator.py` (L39), `solvers/three_body_solver.py` (L66), `STANDARD_MODEL_MYSTERIES_CASCADE.md` (L96).
- Core claim: "Gravity is the trunk; all physics branches from pressure structure" (L184); "Dark matter is displacement pressure in the field" (L195); "Dark energy is low-pressure expansion zones ... Explains cosmic acceleration" (L198).
- Equations: a = -∇P; v(r) = √(r·|a(r)|) (L45-46); P(r) = Σ mᵢ exp(-|r-rᵢ|²/σ²); da/dt = -∇P (L72-73); "G = -∇P", "Ricci curvature ∝ ∇²P" (L201-202); χ² values (L51-52).
- Point / Path / Field role: none stated under those names. Tier 3 lists "Electromagnetic ✓ (emerges from rotation)" (L121) without saying which rotation.
- Magnetism / gravity / rotation link: EM "emerges from rotation" (L121, unspecified). Gravity from the pressure gradient (L200-203). Galaxy rotation curves from P(r) fit worse than the flat curve: χ² 1070 vs 170 and 931 vs 112 (L51-53).
- Open / parked / not-set items: W2 still to implement (L267-270); 3-body dynamics "bodies currently diverging" (L87); many Tier items "ready/emerging" (L102-164).
- Conflicts:
  - L198 ("low-pressure expansion zones ... cosmic acceleration") and L161-164 (inflationary predictions, Hubble tension, flatness problem) assume expansion / cosmological acceleration. This conflicts with the no-expansion rule.
  - L200-203 put gravity in the pressure gradient, Ricci and Einstein form, not g = -alpha K_L grad chi.
  - L212-219: "Five scales with 2× frequency ratios" (physical doubling) contradicts PPF_QUANTUM_TO_COSMIC.md L12-13 ("NOT: Physical doubling"). This is internal to the repo.
  - L195: dark matter as "displacement pressure". No canonical rule covers this, so it is listed for audit only.

## PHASE_5_SOLVER_ATTACK_VECTORS — Phase 5 Solvers: Direct Attacks on Standard Model Weaknesses   (`PHASE_5_SOLVER_ATTACK_VECTORS.md`)
- Gate / lifecycle: "Document Status: FINAL" (L214). Publication argument.
- Upstream: PUBLICATION_STRATEGY.md (L5, L216); Phase 1-4 (L180-181). Downstream / cites: manuscript Sections 1-7 (L172-198). It defines AV-1 to AV-5 (Yukawa, Hierarchy, Fine-Tuning, Higgs-safe, QED-safe). No node IDs.
- Core claim: "Gravitational coupling G emerges from lattice metric properties" (L37); "derives three independent coupling constants (electromagnetic, nuclear, gravitational) from single lattice structure" (L43).
- Equations: G_eff ∝ pressure field strength / lattice cutoff (L39); M_P ~ 1/a ~ 10¹⁹ GeV (L59).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: gravitational and EM couplings are "related through common lattice origin" (L40). No point-rotation or magnetism mechanism is given.
- Open / parked / not-set items: Higgs mass deferred to Phase 6 (L127); "Path forward: gravity/Higgs in Phase 6" (L198). Note: GRAVITY_HIGGS_SPECTRUM puts these in Phase 5, so the two documents disagree on phase numbering.
- Conflicts: L37-40 put gravity in the lattice metric / pressure field rather than K_L grad chi. This is mild because no equation is given.

## PHASE_5_STATUS — Phase 5: Octave-Scaling Quark Mass Discovery   (`PHASE_5_STATUS.md`)
- Gate / lifecycle: "In Progress (October 4, 2026)" (L4). Final line: "✓ Phase 5 COMPLETE" (L624). The light/heavy quark masses use parameters fitted per flavor (L213-218), which contradicts the "No per-flavor parameter refitting" claim (L458). This is an internal contradiction.
- Upstream / cites: C-318 Mass_Mechanism_Candidate_Resolution, "Absolute-Energy Identifiability" (L47, L52, L164); C-317 Boundary_Tension_Weave (L165); C-322 Mirror_Gate_Higgs_Scale_Resonance (L166); Books/Book1_Micro/Book1_Ch02_The_Proton.md (L53, L167); Nodes/PHASE_5_HEAVY_QUARK_DIAGNOSIS.md (L190); Nodes/PHASE_5_HYPOTHESIS_A_B_TEST_RESULTS.md (L257); Nodes/PHASE_5_COMPREHENSIVE_SOLUTION_ANALYSIS.md (L319); Nodes/PHASE_5_HADRON_EXTENSION_VERIFIED.md (L379). Downstream: solvers/quark_mass_solver.py, proton_mirror_gate_calibration.py, proton_compression_simulator.py, quark_mass_spectrum_optimized.py, hadron_knot_geometry.py, hadron_mass_predictor.py, hadron_calibration.py, tests/energy_component_scaling_analysis.py (L22, L57, L85, L239, L264, L344-346).
- Core claim: "Octave-scaling mechanism (ω ∝ √m_scale) confirmed" (L15); energy-scale freedom W_i → λW_i ⇒ m_eff → λm_eff (L45); 125 GeV Mirror-Gate is "the ONLY independent observable that can fix this freedom" (L148).
- Equations: W_i → λW_i ⇒ m_eff → λm_eff (L45); E_M ∝ ξ²/(1-ξ), ξ_G ≈ 0.75 (L87); λ = 125/128 ≈ 0.976 (L88); R(m) = 0.35 × m_scale^α (L294, L326); κ_T(m) = 1.5 × factor × √m_scale (L284, L295); R_hadron = 0.85 × m_scale^(-0.05) fm (L353); weave parameters σ_T, κ_T, η_T (L364-366).
- Point / Path / Field role: none stated. "Simulated boundary penetration resistance (Mirror-Gate scattering)" (L79) is a resistance term but is not tied to mass/organization.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Mirror-Gate work formula, compression path and E_MG(ξ) curve are YELLOW placeholders (L66-69); strange quark error 83% (L95); Lambda and pion errors (L374-375); flavor differentiation of uud (L127-132); two-tier quark/hadron α (L580-617).
- Conflicts: none against the canonical rules. Internal: "COMPLETE" and "no per-flavor refitting" (L458, L624) against the flavor-dependent α (L213-218) and the calibration to experimental masses (L341).

## PHASE_5_VALIDATION_COMPLETE — Phase 5 Validation: Complete   (`PHASE_5_VALIDATION_COMPLETE.md`)
- Gate / lifecycle: "✓ ALL FOUR KEYSTONE SOLVERS VALIDATED" (L3); "Document Status: FINAL" (L302). No node gate is cited.
- Upstream: none cited by node. Downstream / cites: solvers/electron_g2_solver.py (L25), three_body_solver.py (L56), triple_alpha_solver.py (L98), gravity_emergence_validator.py (L154).
- Core claim: "Gravity Emergence — Lattice cutoff and metric geometry explain curvature and inertia" (L16); "Spacetime curvature is pressure field distortion; Einstein's equations emerge as conservation laws" (L198-199).
- Equations: a_e^OW = a_e_reference × (g_SO/0.5) (L38); P ∝ exp(-|r|²/σ²), a = -∇P/m, equilibrium ∇P = 0 (L70-72); R ∝ exp(-2πη) ≈ 10⁻⁴² (L124); κ ∝ ∇²P (L172); g_eff ∝ ∇P (L177).
- Point / Path / Field role: none stated under those names. Inertia is assigned to field coupling: "Coupling to pressure field creates inertia" (L180).
- Magnetism / gravity / rotation link: magnetic moment from a "spin-orbit coupling strength from phase geometry" (L42). Gravity from the pressure field, which "creates inertia", with m_inertial = m_gravitational (L179-182). Stellar cores in "hydrostatic equilibrium" from emergent gravity (L219).
- Open / parked / not-set items: figures and supplements still owed (L271-279).
- Conflicts:
  - L16 and L179-182: gravity / pressure-field coupling "creates inertia". The canon has inertia I as the point property carrying L = I omega, and resistance = mass / organization (bound lattice). Gravity does not affect point rotation.
  - L167-199: gravity from ∇P / ∇²P and Einstein, not g = -alpha K_L grad chi.
  - L38-49: the g-2 "prediction" is the QED reference scaled by g_SO/0.5 = 1. This is an evidence-gate issue, not a canonical-rule conflict.

## PPF_QUANTUM_TO_COSMIC — PPF Scale Recursion: Quantum to Cosmic   (`PPF_QUANTUM_TO_COSMIC.md`)
- Gate / lifecycle: "SCALE-INVARIANT GRAMMAR" (L4); "SCALE-INVARIANT FRAMEWORK LOCKED" (L304).
- Upstream / cites: one-wave-framework-principles.md (L22, L295); C-323 Displacement Interaction Regimes (L226, L243, L296); D-411 "Same ratio ≠ same domain" (L297); B-221 Six-Recursive-Steps oscillator / Algorithm Zero (L298); Circle of Fifths (L299); Rabbit Hopping (L300). Downstream: none.
- Core claim: "PPF (Point/Path/Field) rotation is pure relational grammar" (L10); it is NOT "Physical doubling" (L13); POINT ↔ PATH ↔ FIELD → RESOLVE → next-scale POINT (L23).
- Equations: none (relational formula only, L23, L251).
- Point / Path / Field role: this is the only file in the slice that uses the terms directly.
  - Point is a location or center at every scale, not a rate: "Electron nucleus" (L31), Sun (L188), galactic black hole (L215).
  - Path: "Orbital angular momentum, spin quantization" (L32), orbits (L168, L189, L216), circulation and currents (L168).
  - Field: electron cloud (L33); "Gravitational field, magnetic field, weather systems" (L169); "Dark matter halo, magnetic field, gravitational lensing" (L217); CMB / dark energy field (L234).
  - Point rotation, L = I omega, attitude and inertia are never stated.
- Magnetism / gravity / rotation link: Earth's dipole is a "centered field with ±N/S pole wrapper" (L174). The Sun's internal "plasma convection, magnetic dynamo" is described as the same grammar as orbital Kepler cycles (L200-201). Spin-orbit coupling is a "wrapped address" (L38). Galaxy rotation is a "bulge-to-disk transition = PPF boundary" (L226). No mechanism is given.
- Open / parked / not-set items: none listed.
- Conflicts:
  - L32 puts "spin quantization" and "orbital angular momentum" under Path. The canon makes spin a Point rotation (G-749, carries L = I omega) and says Path rotation (G-769) carries no L.
  - L10-13, L279 ("relational grammar", "Not because these systems are physically similar"). The canon treats Point / Path / Field as three separate physical rates. This file defines Point as a location rather than a rotation rate, so every scale entry lacks point rotation. By the canonical rule, that leaves each entry incomplete.
  - L243 ("Hubble flow: expansion velocity field") and L286 ("cosmic expansion") conflict with the no-expansion / E-528 redshift rule.
  - L243 "C-323 Mirror-Gate" conflicts with L296 (C-323 = Displacement Interaction Regimes) and with PHASE_5_STATUS L166 (Mirror-Gate = C-322). The node ID is mislabeled.
  - L169 / L217 list "magnetic field" as a Field item with no statement that magnetism opens the point. This is a mild omission, not a direct contradiction.

## PRESENTATION_ARCHITECTURE — One-Wave Presentation Architecture   (`PRESENTATION_ARCHITECTURE.md`)
- Gate / lifecycle: governance/navigation doc; "A presentation view never replaces the canonical node or its evidence status" (L3).
- Upstream / cites: `Nodes/` (L7); `Wiki_Pages/` (L8); `AI_Readable_Packs/Appendix_A.md`–`Appendix_G.md` (L9); Books 1-5 (L12); I-05 Proposed Build (Android Body & Brain) (L22); `Musical_Universe/` (L44); Master List (L48); `ONE_WAVE_TERMINOLOGY_LEGEND.md` (L52). It defines seven presentation layers (L5-44), the textbook spine "Gray reference -> 2D -> 3D -> Mathematics -> Predictions -> Yellow Audit -> Future Work" (L16), and the One-Wave Times article audit fields (L30-36).
- Core claim: "The Master List is a navigation summary only ... all point to the same canonical nodes and proof statuses" (L48).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Musical Universe format "deliberately undecided" (L44); Consciousness book is an "Active Hypothesis" (L40).
- Conflicts: none.

## PRIMITIVE_CONVERGENCE_RULE — Primitive Convergence Rule   (`PRIMITIVE_CONVERGENCE_RULE.md`)
- Gate / lifecycle: "Status: governing architecture rule" (L3).
- Upstream / cites: no node IDs. Versions named: VTC, M4/droid control, memory reconstruction, bench primitive, animator/software workflow (L138). Downstream: architecture receipts and a cross-version invariant table (L138-146).
- Core claim: "A feature becomes a stronger primitive candidate only when it recurs across different versions while preserving the same functional role" (L24); "These are architecture candidates, not proof of a physical primitive" (L43); "Do not treat matching numbers as evidence of identical structures" (L130).
- Equations: none.
- Point / Path / Field role: none stated. The candidate list includes "shared reference / center", "ternary movement / resolution around Hold" and "routing between scales" (L30-41).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: receipts and the invariant table are not yet built (L136-147).
- Conflicts: none. Its rule at L130 is in tension with the numeric-coincidence claims in the PHASE_5 files, for example the hierarchy ratio 10¹⁷ "≈" 10¹⁶ and m_μ = m_e × 207 from octave doubling.

---

## Slice summary

### (a) Nodes / chapters / docs in this slice bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking
- A-115 (cited GRAVITY_HIGGS L29): cited as the "Compression Field" that produces GR-style curvature for gravity. The canon makes A-115 the R=0 baseline of g = -alpha K_L grad chi, so this use departs from the canon.
- D-602 (GRAVITY_HIGGS L149-156): longitudinal/transverse dispersion, used for the Higgs criticality argument. No rotation content.
- W2 (GRAVITY_HIGGS, IMMEDIATE_PRIORITIES, SESSION_SUMMARY): gravity / "W metric" blocker. Every file frames it as Ricci / Einstein from pressure or compression and none shows it derived.
- W1 "Mirror wells geometry" (SESSION_SUMMARY L104): named only.
- C-317 Boundary_Tension_Weave (STATUS L165): confinement for mass; κ_T, σ_T, η_T.
- C-318 Mass_Mechanism_Candidate_Resolution (STATUS L47, L164): mass mechanism, octave scaling, energy-scale freedom W → λW.
- C-322 Mirror_Gate_Higgs_Scale_Resonance (STATUS L166): 125 GeV anchor. "Boundary penetration resistance" (STATUS L79) is the only resistance term in the slice and is not tied to mass/organization.
- Book1_Ch02 The Proton (STATUS L53, L167): three-vortex knot topology for mass.
- C-323 Displacement Interaction Regimes (PPF L226, L243, L296): field boundaries; galaxy-rotation basin crossing. Mislabeled as Mirror-Gate at L243.
- B-221 Six-Recursive-Steps / Algorithm Zero (PPF L298): recursion grammar, with no rotation mechanism.
- D-411 Same ratio ≠ same domain (PPF L297): a guard against number matching.
- one-wave-framework-principles.md (PPF L22, L295): PPF recursion source.
- PPF_QUANTUM_TO_COSMIC (whole file): the only Point/Path/Field treatment in the slice. It places spin and orbital L under Path, defines Point as a location rather than a rate, and puts magnetic field under Field.
- PHASE_5_VALIDATION_COMPLETE and PHASE_5_QUANTITATIVE_RESULTS: inertia and the equivalence principle from pressure-field coupling (VALIDATION L179-182, QUANT L99).
- The PHASE_5 g-2 docs (HARMONIC L53, MANUSCRIPT L41-52, QUANT L12-23, VALIDATION L28-49): magnetic moment from "spin-orbit" boundary coupling g_SO = 0.5, which is the QED reference scaled by 1.
- PHASE_5_HARMONIC_LOCKING_REFOCUS / MANUSCRIPT_NARRATIVE: "harmonic locking" at boundaries. This is not the canonical bound-lattice point-rate locking (no Moon 1:1 or Mercury 3:2).
- PRESENTATION_ARCHITECTURE (I-05, Appendices A-G, Books 1-5, terminology legend) and PRIMITIVE_CONVERGENCE_RULE: governance only. No physics.

### (b) All conflicts found
1. Gravity is placed in Einstein / Ricci curvature from lattice compression or the pressure Laplacian / gradient instead of g = -alpha K_L grad chi:
   - GRAVITY_HIGGS L13, L27, L40, L57-76
   - HARMONIC_LOCKING L98-109
   - IMMEDIATE_PRIORITIES L16-24, L232
   - MANUSCRIPT L65, L119-126
   - QUANTITATIVE L95-100
   - SESSION_SUMMARY L200-203
   - SOLVER_ATTACK L37-40
   - VALIDATION L167-199
2. Expansion / dark energy / cosmological acceleration, against the no-expansion rule (redshift = E-528):
   - GRAVITY_HIGGS L76, L103-113, L554, L621 (FLRW)
   - SESSION_SUMMARY L161-164, L198
   - PPF L243, L286
   - IMMEDIATE_PRIORITIES L194 (implied)
3. Inertia created by gravitational / pressure-field coupling, against inertia I belonging to the point (L = I omega), resistance = mass / organization, and gravity not affecting point rotation: VALIDATION L16, L179-182; QUANTITATIVE L99.
4. Spin and orbital angular momentum placed under Path, against G-749 (spin is Point, carries L) and G-769 (Path carries no L): PPF L32.
5. Point / Path / Field treated as relational grammar and Point as a location, not as three separate rates. No point rotation is stated at any scale, so each PPF entry is incomplete: PPF L10-13, L279.
6. Mercury precession framed as GR frame-dragging instead of the 3:2 bound-lattice point-rate lock: GRAVITY_HIGGS L92-99 (mild).
7. Internal repo conflicts:
   - Octave "2× frequency" physical doubling (SESSION_SUMMARY L212-219) against PPF L13 ("NOT physical doubling").
   - Mirror-Gate labeled C-323 (PPF L243) against C-322 (STATUS L166).
   - Gravity/Higgs placed in Phase 5 (GRAVITY_HIGGS) against Phase 6 (SOLVER_ATTACK L127, L198).
   - STATUS claims "no per-flavor refitting" and "COMPLETE" (L458, L624) against the flavor-dependent α (L213-218).
   - The g-2 "0 ppm" match is the QED reference passed through (QUANT L12-13, VALIDATION L38-41). This is an evidence-gate issue.

### (c) Cross-references outside this slice that matter for point rotation or magnetism
- A-115 (canonical K_L baseline), D-602, C-317, C-318, C-322, C-323, B-221, D-411, I-05.
- one-wave-framework-principles.md (PPF source; should be checked against G-749 / G-769).
- Nodes/PHASE_5_HEAVY_QUARK_DIAGNOSIS.md, Nodes/PHASE_5_HYPOTHESIS_A_B_TEST_RESULTS.md, Nodes/PHASE_5_COMPREHENSIVE_SOLUTION_ANALYSIS.md, Nodes/PHASE_5_HADRON_EXTENSION_VERIFIED.md.
- STANDARD_MODEL_MYSTERIES_CASCADE.md ("Electromagnetic emerges from rotation", per SESSION_SUMMARY L121); PUBLICATION_STRATEGY.md; ONE_WAVE_TERMINOLOGY_LEGEND.md.
- Solvers implementing the gravity-from-pressure and g_SO claims: solvers/gravity_emergence_validator.py, solvers/unified_phase_solver.py (GravityFromPressure), solvers/electron_g2_solver.py (g_SO spin-orbit), solvers/galaxy_rotation_validator.py, solvers/three_body_solver.py.
