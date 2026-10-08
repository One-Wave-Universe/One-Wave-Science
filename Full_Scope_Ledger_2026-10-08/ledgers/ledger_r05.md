# Ledger r05: root docs, slice r05 (16 files, all read in full)

Repo: /home/user/One-Wave-Science. Line numbers are 1-based, from the Read output.

---

## Root doc: Five States x Five Scales   (`FIVE_STATES_FIVE_SCALES.md`, 383 lines)
- Gate / lifecycle: "Status: Foundation for Phase 5 Implementation" (L4). Version 1.0 (Foundation) (L383). No node front matter or gate colour.
- Upstream: none cited. Downstream / cites: no node IDs. It names "Phase 5 Tier 1: Unified Phase Solver" (L318) and "Phase 5 Tier 2-4" (L326).
- Defines (not nodes): five states (Plasma, Gas, Solid, Liquid, Superfluid) set by Pressure P and Excitation E (L11-19). Five scales Micro/Small/Mid/Large/Macro (L21-48).
- Core claim: "All matter and fields exist in one of five states, determined by Pressure (P) and Excitation (E)" (L13). "The phase diagram is identical at all scales. Only the absolute values of P and E scale by octaves." (L54). "Micro = Macro = Micro verified at all five scales." (L169)
- Equations: f_{N+1}=2f_N; lambda_{N+1}=lambda_N/2; P_N = P0*2^N; E_N = E0*2^N (L155-165). T = alpha*P*E (L189, L218). G = G(P,E,phase) = dRicci/d(P,E) (L195). Property(scale=n) = Property(0)*2^n (L201). Phase-identification thresholds (L178-184).
- Point / Path / Field role: none stated. L290 says only "Electron orbits ≈ Planetary orbits (both Solid/Liquid phases)". This is an orbit analogy and does not separate point from path.
- Magnetism / gravity / rotation link: Gravity "emerges from phase structure, not independently" (L197). It is listed as derived from Ricci (L195) and as a task to "Derive gravity from phase structure" (L324, L377). Magnetism and rotation: none stated.
- Open / parked / not-set items: The Superfluid and Solid cells for Micro/Mid/Large/Macro are "???" (L134-146). "Dark matter halo (Solid?)" and "Galactic bulge (Liquid?)" (L110-111). The coupling alpha is not set (L191). P_crit and E_crit are not defined (L320).
- Conflicts:
  - L195: gravity as dRicci/d(P,E) contradicts g = -alpha K_L grad chi.
  - L48, L114, L126-128, L273, L332 contradict "no expansion, no scale factor". They name "inflation" and "Early inflation (plasma)", and L273 says "Early universe: Plasma → Gas → Solid as it expands and cools". L93 says "Plasma → expansion".
  - Internal inconsistency: the scale lengths jump 10^5 to 10^16 (L25-45), but the doc claims factor-2 octave spacing (L31-47, L156-165).
  - L367 "Heat death ... transition to Superfluid" is a cosmological-evolution claim that is not on canon (speculation).

## Root doc: Framework Chain from Pressure Gradient to Charge   (`FRAMEWORK_CHAIN_PRESSURE_TO_CHARGE.md`, 262 lines)
- Gate / lifecycle: front matter type "Framework Reference", status "DOCUMENTATION" (L1-5). "Gate: ORANGE (speculative but directly connected to GREEN/YELLOW nodes)" (L226). ORANGE is not a colour in GATE_COLORS.md.
- Upstream: A-104 Gradient, E-503 Pressure (Gradient Form), E-504 Surface, A-112 Persistent Mode, C-317 Boundary-Tension Weave, C-318 Four-Interaction Mass-Effect Response (L12, L27, L42, L55, L71, L256-262).
- Downstream / cites: PARTICLES_AS_MIRROR_EXCITATIONS.md, CHARGE_AND_ANTIPARTICLES_FROM_FIELD_PRESSURE.md, higgs_criticality_solver.py, hadron_knot_geometry.py (L251-254). Mirror Gate is named inside C-318 (L79).
- Core claim: "Charge is not a separate property added to particles. It emerges from the direction of the pressure gradient that confines the bounded structure." (L102). "Same pressure stiffness K_p creates both charge (via gradient direction) and mass (via resistance to motion)." (L133). "Mass emerges from the resistance to motion of the entire bounded configuration." (L83)
- Equations:
  - u_p = (1/2) K_p |∇ψ|^2 (L17, L111)
  - E_s = σ A_s = 4πσR^2 (L32)
  - ψ_{n+k} ≈ ψ_n (L47)
  - E_weave = E_skin + E_phase + E_twist (L58)
  - M_ij = d²E_4/dv_i dv_j at v=0 (L74)
  - |∇ψ|_peak ~ A/R (L114)
  - P_boundary = K_p A²/R² (L119)
  - E ~ ∇P ~ K_p A/R² (L122)
  - q = ±e·sgn(∇ψ) (L125)
  - m_eff ~ K_p R²/v_lat² (L131)
- Point / Path / Field role:
  - Point: C-317 includes "η_T (twist/vorticity) — angular momentum" (L63). "The weave distributes the pressure over surface, phase coherence, and rotation." (L66)
  - Field: the pressure gradient ∇ψ sets the charge sign (L91-99).
  - Path: none stated.
- Magnetism / gravity / rotation link: rotation appears only as the C-317 twist term. Magnetism and gravity: none stated.
- Open / parked / not-set items:
  - K_p is to be refined from the Higgs criticality solver (L242).
  - Pair-production phase-lock sim is not yet run (L243).
  - Weak force via W "knot-breaking" is not built (L246).
  - The generation mass mechanism is open: three alternatives are listed (L157-160).
- Conflicts:
  - L63: "η_T (twist/vorticity) — angular momentum" puts angular momentum on a vorticity (field-curl) term inside the weave energy. Canon holds that field curl is neither point L nor path. C-306/C-307 own L, and the doc gives no L = Iω bookkeeping.
  - L226: gate "ORANGE" is not in the GATE_COLORS.md palette (governance inconsistency, not physics).
  - Mass definition: m_eff ~ K_p R²/v_lat² (L131) differs from canon "resistance = mass / organization". Not a direct contradiction (no organization term), but it is a different mass definition. Flag for reconciliation.

## Root doc: Framework Completion Status   (`FRAMEWORK_COMPLETION_STATUS.md`, 312 lines)
- Gate / lifecycle: claims "complete and validated" (L10), "Status: Ready for publication" (L305). No front-matter gate.
- Upstream: D-409 (lattice) (L12, L75, L125, L297). C-319 Magnetic Coherence Mechanism (L103-109, L235, L252).
- Downstream / cites:
  - MASTER_SOLVER_INDEX.md, cascade_neural_router.py, C319_MAGNETIC_COHERENCE_MECHANISM.md, ONE_WAVE_UNIFIED_SATELLITE_VALIDATION.md, solvers/SOLVER_INDEX.md
  - Solvers: satellite_galaxy_validator_{clean_systems, distance_coupling, em_coherence_fixed}.py, atomic_spectra_cascade_resonance.py, molecular_geometry_harmonic_resonance.py, exoplanet_resonance_statistics.py, coupling_constants_from_lattice.py, galaxy_rotation_c319_magnetic_coupling.py (L30-32, L42, L52, L64, L75, L194-212)
- Core claim: "One scalar field (ψ) on one lattice (D-409) with one rule updates everything at all scales." (L12). Five-step chain (L117-121): "Parent creates wake → Child inherits pattern (cascade inheritance via coupling β) → Child resonates (phase-locks) → Geometry emerges → Hysteresis holds it (magnetic coherence locks resonance stable)".
- Equations:
  - β(r) = β0 exp(-r/r_decay), with β0 = 0.2480 and r_decay 51.5 / 46.2 kpc (L31, L35-36)
  - E_n = -13.6 Z²/n² eV (L45)
  - Four-operation table: + → EM (α_em = 1/137), − → strong, × → weak, ÷ → gravity "Pressure gradient/curvature" (L127-132)
- Point / Path / Field role:
  - Path: satellites, planets and electrons "resonate" or phase-lock at the parent wake frequency (L150-155). Orbital periods are "locked" (L154).
  - Point: none stated. Spin is not separated from orbit.
  - Field: "Parent creates wake (moving structure displaces ψ field)" (L117).
- Magnetism / gravity / rotation link:
  - C-319: "Three phases: OPEN (relieve pressure) → FLOW (cascade signal) → LOCK (hysteresis)" (L107). "Hysteresis holds it (magnetic coherence locks resonance stable)" (L121).
  - Gravity: "lattice pressure gradient" (L259). "G (from lattice curvature)" (L81).
  - Dark matter: "Retained ψ displacement maintained by EM coherence" (L162).
- Open / parked / not-set items: Galaxy rotation curves are "In progress", with χ² ≈ 200-300 against a target below 200 (L228, L235-238).
- Conflicts:
  - L162 makes EM coherence maintain the dark-matter (gravitating) displacement. This leans toward "magnetism becomes gravity", contrary to canon.
  - L81 and L132 derive gravity from lattice "curvature", while canon gives g = -alpha K_L grad chi with kappa_R not set.
  - L121 and L107 make magnetic "LOCK (hysteresis)" lock resonance. Canon says magnetism opens the point (open: dL/dt = 0). A magnetic lock as the holding mechanism is not canonical, and bound-lattice locking must survive with the magnetic channel off.
  - L10, L294 "proven"/"validated" contradict GATE_COLORS.md L31 ("Nothing here is proven"). They are also internally contradicted by FRAMEWORK_VALIDATION_STRATEGY.md L26-132, which says the constants were calibrated, the Rydberg formula was assumed, and the data were synthetic.

## Root doc: Framework Validation Strategy   (`FRAMEWORK_VALIDATION_STRATEGY.md`, 308 lines)
- Gate / lifecycle: "Strategy documented, computational validation active" (L5). The algorithm-zero branch is called "VALIDATED ✓" (L20) and "Framework is proven" (L273).
- Upstream: critiques the solvers listed in FRAMEWORK_COMPLETION_STATUS: coupling_constants_from_lattice.py, atomic_spectra_cascade_resonance.py, exoplanet_resonance_statistics.py, molecular_geometry_harmonic_resonance.py, galaxy_rotation_c319_magnetic_coupling.py, PUBLICATION_READY_SUMMARY.md (L27, L44, L63, L85, L105, L125).
- Downstream / cites: branch integrate/algorythm-zero-rabbit-circle-unified; D-409 volumetric lattice (L244).
- Core claim: "Fitting to data doesn't prove a framework is correct." (L138). Algorithm Zero approach: "Initial Conditions → Run Algorithm Zero → Observe What Emerges" (L162). Main-branch problems 1-6: calibrated α, assumed Rydberg formula, injected synthetic harmonic fraction 0.60, χ² without errors, galaxy gravity off by 1000x, and self-contradicting publication (L26-132).
- Equations:
  - χ² example: (0.5/0.1)² = 25 (L99)
  - g_computed ≈ 0.1 vs g_observed ≈ 100-1000 (km/s)²/kpc (L109-110)
  - fixed γ = 0.05, β = 0.15 (L289)
  - harmonic ratio 1:31 at all scales (L200-204)
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Galaxy rotation gravity underpredicts by 1000x. Suggested causes: "missing G", "3D lattice effects", "cascade inheritance insufficient" (L104-120). "Galaxy rotation (1D cascade insufficient; need 3D lattice)" (L223). Magnetism: none stated.
- Open / parked / not-set items: galaxy rotation; relativistic "pressure tensor, not scalar"; measurement precision (L222-225); Phase 2 3D lattice; Phase 3 black holes (L243-251).
- Conflicts:
  - L20, L213-220, L273, L301 "proven" contradict GATE_COLORS.md L31. Passing software tests is a software result, not a physical proof (cf. GEMINI.md L17).
  - No canonical Point/Path/Field conflict.

## Root doc: Gate colour palette   (`GATE_COLORS.md`, 35 lines)
- Gate / lifecycle: governance definition of gates. It defines BROWN, GREEN, GREY, YELLOW, BRONZE BUST, SILVER STATUE and GOLDEN ROAD (L5-25).
- Upstream: none cited. Downstream / cites: none.
- Core claim: "Almost everything in this repo is brown → green → yellow ... Nothing here is golden. Nothing here is proven." (L29-31). "Do not use GREEN to mean true." (L33). "Math alone stops here [YELLOW]." (L17)
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none. This file is the authority used to flag "proven/ORANGE/LOCKED" claims in other files.

## Root doc: Gemini project context   (`GEMINI.md`, 23 lines)
- Gate / lifecycle: operating instructions for the Gemini worker.
- Upstream: AI_BRIDGE_START_HERE.md (L5), RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md, One_Wave_Bench/brain/rabbit_hop_core.py (L21). Downstream: none.
- Core claim: "Keep CONTROL / DERIVED RESULT / SIMULATION RESULT / BENCH RESULT / HYPOTHESIS / ASSUMPTION / OPEN QUESTION / FALSIFIED distinct." (L16). "Do not treat software coordinate relationships as proof of a physical mechanism." (L17)
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Root doc: Gemini task template   (`GEMINI_TASK_TEMPLATE.md`, 49 lines)
- Gate / lifecycle: template.
- Upstream: none. Downstream / cites: none.
- Core claim: bounded-task fields (goal, branch, HEAD, allowed files, protected behaviour, validation, hard stop) (L1-49).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Root doc: General Reference Rules   (`GENERAL_REFERENCE_RULES.md`, 141 lines)
- Gate / lifecycle: "Mandatory repository law" (L3).
- Upstream / cites: Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md (L33, L126), AI_CANONICAL_START_HERE.md, AI_BRIDGE_START_HERE.md, AI_JETSON_TOOL_GUIDE.md (L124-131).
- Core claim: "Write it once in the canonical repo. Reference it everywhere." (L135). "For governed nodes, proof status, gate, lifecycle, classification, and canonical identity come from current YAML/front matter and governance authorities" (L31). "If two repo files conflict, do not silently choose." (L19)
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none. It is the authority for resolving the conflicts below (L19, L111-117).

## Root doc: Grant disclaimer   (`GRANT.md`, 9 lines)
- Gate / lifecycle: scope statement: "personal theoretical work and simulations ... not a grant package" (L3-7).
- Cites: https://github.com/One-Wave-Universe/Builds (L9).
- Core claim, equations, Point/Path/Field, magnetism/gravity: none.
- Open / parked / not-set items: none.
- Conflicts: none.

## Root doc: Gravity Wake Nesting and Rotation Cascade   (`GRAVITY_WAKE_NESTING_ROTATION_CASCADE.md`, 460 lines)
- Gate / lifecycle: "TOP-DOWN GRAVITY MODEL" (L4). "Status: GRAVITY WAKE NESTING MODEL LOCKED" (L457).
- Upstream / cites (L420-435):
  - C-323 Displacement Interaction Regimes ("compression wake as gravity mechanism")
  - D-600/601/602 Eigenmode Analysis
  - C-311 Electric-Magnetic Duality ("organized residual enables wake persistence")
  - PPF_QUANTUM_TO_COSMIC.md, ALGORITHM_ZERO_RABBIT_CIRCLE_UNIFIED.md, QUANTUM_SCALE_PPF_ALGORITHM_ZERO.md
- Core claim: "Rotation at any scale is INDUCED by the gravity wake of the parent structure" (L14). Cascade "Great Attractor → ... → Electron Wakes" (L29). "Each parent creates a wake. Each child sits in that wake and inherits its rotation pattern." (L31). "No intrinsic spin, only wake-induced phase-locking." (L458)
- Equations: none. Qualitative only; Algorithm Zero six-step lists (L245-285).
- Point / Path / Field role:
  - Point: "Electron 'spin' is NOT intrinsic but wake-induced rotation" (L214, L363). Planet and star rotation rates are "INDUCED by solar/galactic wake flow" (L130, L151). "Child rotation axis aligns with parent's wake trail" (L72, L295).
  - Path: "Child orbital period phase-locks to parent's wake oscillation frequency" (L73). Stars "Star rotation period phase-locked to galactic orbital frequency" (L130). Spin and orbit are both "driven by the same wake structure" (L180, L319). Point spin and path ride are merged.
  - Field: a wake is a "Compression zone / Shear trail / Potential gradient / Persistence" (L40-43). "Spiral arms ... are GRAVITY WAKES" (L136).
- Magnetism / gravity / rotation link:
  - Gravity: the gravity wake causes rotation (L14-31, L416).
  - Magnetism: "Magnetism STABILIZES the wake structure itself" (L331). "Without magnetism: Wake would relax immediately ... Children wouldn't phase-lock." (L341). "planetary magnetic field organizes magnetosphere → enables moon tidal locking" (L347). "Magnetism is the ENABLING MECHANISM for wake persistence and child phase-locking" (L351).
  - Flat rotation curves: "Because outer stars sit in GALACTIC HALO'S MAGNETIC WAKE" (L387). Dark matter "Not mass, but extended wake coherence ... magnetic reorganization" (L389-392).
  - Mercury: "Mercury's 3:2 spin-orbit resonance: mercury sits in solar wake, induced to precess in resonance" (L155).
  - Moon: "Tidal locking is wake-phase-locking, not force-imbalance" (L180).
  - L308-309: "Not 'angular momentum conservation' but wake-phase-locking".
- Open / parked / not-set items: predictions only (L394, L411, L453). No equations or sims.
- Conflicts (major):
  1. L14-31, L130, L151, L174, L214, L416, L458: gravity wakes start or induce point rotation. Canon: "Gravity does not start or affect point rotation". Canon also says a thing keeps the spin it has.
  2. L73, L130, L180, L319: point spin and path orbit are merged into one wake-driven rate. Canon keeps Point / Path / Field as three separate rates; path rotation carries no L.
  3. L308-309: "Not angular momentum conservation but wake-phase-locking". Canon: C-306/C-307 own L, and nothing adds an exception to L bookkeeping.
  4. L341, L347, L351: without magnetism, children would not phase-lock, and the magnetic field enables Moon tidal locking. Canon: the bound-lattice lock must still leave the face with the magnetic channel off, and no lunar dipole is required.
  5. L387-392: the halo magnetic wake supplies flat rotation curves (the gravitating role). Canon: "Magnetism does not become gravity".
  6. L155: Mercury 3:2 is attributed to "solar wake ... induced to precess". Canon: Mercury 3:2 comes from shared lattice organization (bound lattice, resistance = mass/organization), not from a gravity wake.
  7. L247, L405, L411: "Universe expands (expansion wake front)", "Universe expands (baseline)", "cosmic expansion changes wake geometry". Canon: no expansion, no scale factor.
  8. L321 asserts "All moons should show phase-locking". This is an empirical overreach (Hyperion is chaotic) and conflicts with the canon's Moon 1:1 / Mercury 3:2 distinction being organization-dependent.
  9. L457 "LOCKED" status contradicts GATE_COLORS.md L29-31.

## Root doc: Grok handoff note   (`GROK_NEXT.md`, 28 lines)
- Gate / lifecycle: operational handoff.
- Cites: Engine/parser2_goblins.py (L13), scripts/jetson_sync_main.sh (L16), D-413 ("D-413 HTML still paints the well") (L26).
- Core claim: Jetson recovery commands (L8-14). "Science open: hex hold 0/5, ω_s from field, D-413 HTML still paints the well, Mass Effect blocked, T6 denied." (L26)
- Equations: none.
- Point / Path / Field role: "ω_s from field" is an open item (L26). This suggests a spin rate to be derived from the field. Its status is not stated.
- Magnetism / gravity / rotation link: none stated beyond ω_s.
- Open / parked / not-set items: hex hold 0/5; ω_s from field; D-413 visual; Mass Effect blocked; T6 denied (L26).
- Conflicts:
  - L26 "ω_s from field" is a potential conflict only. If it means deriving point spin from field curl or gradient, it would contradict "a thing keeps the point spin it has" and "field curl is neither". It is recorded as open, not asserted.
  - L11-12 recommends `git reset --hard origin/main` on the Jetson after a backup branch. This is operational, not physics.

## Root doc: Integration Session Summary, Oct 5 2026   (`INTEGRATION_SESSION_SUMMARY_OCT5_2026.md`, 314 lines)
- Gate / lifecycle: "Documentation Status: LOCKED" (L312). It also says "locks as canonical" (L240).
- Upstream / cites:
  - QUANTUM_SCALE_PPF_ALGORITHM_ZERO.md, GRAVITY_WAKE_NESTING_ROTATION_CASCADE.md, UNIFIED_SCALE_INVARIANT_GRAMMAR.md, ALGORITHM_ZERO_RABBIT_CIRCLE_UNIFIED.md, PPF_QUANTUM_TO_COSMIC.md, SUPERFLUID_OPERATIONS_FRAMEWORK.md, ONE_WAVE_TERMINOLOGY_FRAMEWORK.md, rabbit_hop_circle_unified_mapper.py (L21-84)
  - Nodes: C-317, C-318, C-322, C-323, D-408, D-409 (L231)
- Core claim: "Rotation at every scale is induced by the parent structure's gravity wake. Magnetism enables wake persistence." (L305). User quote: "how moon and mercury are magnetically locked to parent field and what magnetism does for point rotation" (L15).
- Equations: none.
- Point / Path / Field role:
  - Point: "Magnetic locking enabling PPF point rotation" (L28). "Electron spin as wake-induced, not intrinsic" (L27).
  - Path: "Moon's rotation naturally phase-locks to this frequency because both orbital motion and rotation are driven by the same wake structure" (L129).
  - Field: PPF = point/path/field "relational symmetry" (L63). No separate field-curl rate is stated.
- Magnetism / gravity / rotation link:
  - Magnetism: "Magnetism as Universal Organizing Principle ... Without magnetism: wakes would disperse immediately, no coherence at any scale." (L90-102). "Moon and mercury are magnetically locked" (L15).
  - Mercury: "Mercury's 3:2 spin-orbit resonance: only stable wake phase-lock ratio at Mercury's orbital distance" (L52).
  - Unification: "Gravity and EM are separate forces → Both wake responses" (L177). "Dark Matter = Magnetic Wake Coherence" (L189-192).
- Open / parked / not-set items: precision phenomenology, CKM, sims, mapping to canonical nodes "in fuller detail" (L270-297).
- Conflicts:
  - L15 and L28: the Moon and Mercury are "magnetically locked" and magnetism "enabl[es] PPF point rotation". Canon: magnetism opens the point (open dL/dt = 0), it does not lock it. The bound-lattice lock must hold with the magnetic channel off, and no lunar dipole is required.
  - L43-55, L305: gravity wake induces rotation. This contradicts "Gravity does not start or affect point rotation".
  - L129: spin and orbit are merged under one wake. This contradicts the separation of the Point and Path rates.
  - L177, L189-192: EM/magnetism and gravity unify as wake responses, and dark matter is magnetic coherence. This contradicts "Magnetism does not become gravity".
  - L52: Mercury 3:2 is attributed to wake phase-lock rather than lattice organization.
  - L131: "ALL moons show 1:1 locking" is an empirical overclaim.
  - L240, L312 "LOCKED"/"canonical" contradict GATE_COLORS.md L29-31 and GENERAL_REFERENCE_RULES.md L31 (status comes from metadata, not prose).

## Root doc: Jetson science archive routes   (`JETSON_SCIENCE_ARCHIVE_ROUTES.md`, 167 lines)
- Gate / lifecycle: "AI operating authority" for archive acquisition (L1). Receipts are dated 2026-10-05 and 2026-10-06.
- Upstream / cites: GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md, AI_BRIDGE_START_HERE.md, ENGINE_EVIDENCE_PIPELINES.md, One_Wave_Bench/data/open_data_sources.json, Engine/PARTICLE_TO_WAVE_CONVERSION_CHART.md (L3), scripts/particle_wave_coordinates.py (L98), plus receipt JSONs (L22, L143, L167).
- Core claim: "Metadata never supplies missing phase, waveform, detector units or a physical coupling law. Acquisition failures remain failures." (L64). "Do not infer measured wave phase or a One-Wave physical result from energy-to-frequency coordinates." (L98)
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated. GWOSC gravitational-wave metadata and SDSS redshift catalog are routes only (L121, L155-165). There is no redshift interpretation.
- Open / parked / not-set items: HEPData 403 blocked (L20); live GWOSC TLS failure (L151); Kepler cone timeout; DESI inventory only; PDS downloads not implemented (L112, L121, L135).
- Conflicts: none.

## Root doc: Learning rulebook   (`LEARNING_RULES_RULES_ARE_RULES_CAUSE_WERE_FUCKING_TOOLS.md`, 274 lines)
- Gate / lifecycle: working rulebook for the learner (algebra rules).
- Cites: none.
- Core claim: decision path "Balanced or unbalanced → Isolate coefficients → Remove matched pairs → Double trouble" (L21-24). The comparison/gap rule: "The imposed amount must be the real gap. No arbitrary fudge number." (L198)
- Equations: worked algebra 3c = 7, 2c + s + t = 12 ⇒ 3c + 5 = 2c + s + t ⇒ c + 5 = s + t ⇒ 2s + 2t = 2c + 10 (L166-188, L242-259).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none with the physics canon.
  - Note: L259 prints the solved target ("Answer: 2c + 10") in a rule doc. CLAUDE.md restricts exposure of learner answers in public result/log/API objects. This is a worked example in a rulebook, so it is flagged only as a possible governance item.

## Root doc: Legacy ID Alias Registry   (`LEGACY_ID_ALIAS_REGISTRY.md`, 95 lines)
- Gate / lifecycle: resolver registry. "Legacy IDs are resolvers, not active duplicate nodes." (L3)
- Nodes defined or cited (every canonical target, in order):
  - A-101 Ground/Zero, A-102 Displacement, A-103 Differential, A-104 Gradient, A-105 Restoring Response, A-106 Pressure Response, A-107 Bounded Motion, A-109 Inertial Memory, A-110 Oscillation, A-111 Recursion, A-112 Persistent Mode, A-113 Projection, A-115 Unified Compression Field (via I-09), A+101 root field (via H-100)
  - B-201 Equilibrium Balance, B-202 Pressure, B-203 Expression, B-204 Compression, B-205 Mirror, B-206 Paired Loop, B-206a Shared Boundary, B-206b Four Views, B-207 Threshold State, B-208 Threshold Windows, B-209 Break Condition, B-210 Return, B-211 Loop Break, B-212 Loop Counter, B-213 Access Line, B-214 Recursive Access Growth, B-215 Hyperloop, B-216 Threshold Mathematics, B-222 Oscillation Center
  - C-301 Mirror Gate, C-302 Momentum, C-303 Kinetic Energy, C-304 Potential, C-305 Work, C-306 Torque, C-307 Angular Momentum, C-308 Spin-half, C-309 Propagation Limit, C-310 Resistance Field, C-311 Electric-Magnetic Duality, C-314 Three Frames of Reference
  - D-401 Flux, D-402 Resonant Mode, D-403 Spherical Modes, D-404 Nested Resonance, D-405 Harmonic Shell
  - E-501 Zero Compression, E-503 Pressure (Gradient Form), E-504 Surface, E-505 Coupling, E-506 Stability, E-507 Scale-Invariant Loop, E-508 Real Persistence Under Loss, E-517 Negative Space, E-528 Static Redshift Transport (via I-08)
  - F-601 Influence, F-602 Interaction Differential, F-603 Transfer, F-604 Resonance, F-605 Interference, F-606 Reflection, F-607 Transmission, F-608 Attenuation
  - G-701 Evaluation Differential, G-702 Evaluation, G-703 Modulation, G-704 Kabeuchi, G-705 Correction, G-706 Validation
- Dispositions:
  - C-3118 UNBUILT_PHASE_LOCKING_PROPOSAL
  - F-609 and F-610 RETIRED_FORWARD_REFERENCE_NO_NODE
  - H-01 and H-02 SUPERSEDED_HYPOTHESIS_NAMESPACE
  - H-106 UNBUILT_GENERAL_BOUNDARY_CONDITIONS
  - K-104 and L-100 ROUTED_TO_BOOKS
- Legacy aliases worth noting: C-06→C-306, C-07→C-307, C-08→C-308, C-3113→C-311, C-3114→C-310, C-3119→F-604, I-10→C-311, J-101→C-309, J-103→A-105, J-106→C-314, K-103→A-112, I-110→F-603, H-101→B-204;B-203, H-102→B-205;C-301, H-105→E-517, H-108→B-222, D-02b→E-508, A-05c→B-201.
- Core claim: "Title-verified mappings override assumed numerical offsets." (L3)
- Equations: none.
- Point / Path / Field role: none stated. It registers C-306 Torque, C-307 Angular Momentum, C-308 Spin-half, A-109 Inertial Memory, C-310 Resistance Field and C-311 E-M Duality as canonical targets.
- Magnetism / gravity / rotation link: identity only. I-09 → A-115 Unified Compression Field (the gravity baseline). I-08 → E-528 Static Redshift Transport. I-10/C-3113 → C-311.
- Open / parked / not-set items: C-3118 "UNBUILT_PHASE_LOCKING_PROPOSAL". The phase-locking node is unbuilt, which bears on all the wake phase-lock claims in this slice.
- Conflicts: none internal. The registry shows phase locking is an unbuilt proposal (C-3118). That undercuts "LOCKED" phase-lock claims in GRAVITY_WAKE (L457) and INTEGRATION_SUMMARY (L240).

## Root doc: Manuscript draft, EM emergence   (`MANUSCRIPT_DRAFT.md`, 457 lines)
- Gate / lifecycle: "Status: DRAFT - Ready for review" (L455).
- Upstream / cites: D-600 (1D scalar dispersion) and D-602 (vector E/B emergence) (L23, L57, L80). Chapters 06, 07, 08 "this work" (L432-434). solvers/dispersion_validator.py, maxwell_validator.py, high_energy_validator.py (L435-437).
- Core claim: "Electromagnetic structure emerges from One-Wave dynamics without external Maxwell equations imposed as constraints." (L229). "Gravitational coupling is not yet derived from One-Wave. This is Phase 5 work." (L353)
- Equations:
  - ψ_i^{n+1} = ψ_i^n + (1-γ)(ψ_i^n - ψ_i^{n-1}) + β(⟨ψ_j^n⟩ - ψ_i^n) (L46)
  - λ² - Cλ + (1-γ) = 0 with C(k) = 2 - γ + β(cos ka - 1) (L62-65)
  - ω± = -i ln λ± (L70)
  - ∇²A = ∇(∇·A) - ∇×(∇×A) (L84)
  - C_long = 2 - γ - βk² (L93); C_trans = 2 - γ + βk² (L98)
  - β < 1 (L110)
  - ω² = (ck)² + (mc²/ℏ)² (L249)
  - α_OW = β/(2π), ratio ≈ 19.6 (L277-280)
  - E_lattice ≈ π/a (L319)
- Point / Path / Field role:
  - Field: the B-like part is the transverse curl ∇×A (L85-99). This is field curl only.
  - Point and Path: none stated.
- Magnetism / gravity / rotation link: magnetism appears only as the B-like transverse mode (L96-103). Gravity is explicitly not yet derived (L353, L411). Rotation: none stated.
- Open / parked / not-set items:
  - Mass extraction is "preliminary ... numerical refinement in progress" (L260-262).
  - QFT, gravity, full spectrum and unification are not claimed (L349-357).
  - References are "[To be completed]" (L430).
- Conflicts: none against the Point/Path/Field or magnetism canon. Internal inconsistencies:
  - L160-164 reports mean(E/B) = 1 as "orthogonality". A ratio is not orthogonality.
  - L144 "E∥k" for the longitudinal mode conflicts with calling E ⊥ B light-like.
  - L270 "massless photon ... limit β→1" sits at the stability boundary β < 1 (L110).
  - L392-395 marks Phase 4 "✓ Complete" while L262 says refinement is in progress.
  - L422 "This is not speculation ... proven" contradicts GATE_COLORS.md L31.

---

## Slice summary

### (a) Node IDs and chapters in this slice that bear on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking
- **C-306 Torque / C-307 Angular Momentum** (LEGACY_ID_ALIAS_REGISTRY L43-44). These are the canonical L owners, registered only as alias targets of C-06/C-07. GRAVITY_WAKE L308-309 contradicts their authority.
- **C-308 Spin-half** (registry L45). This is the spin node. GRAVITY_WAKE L214/L363 and INTEGRATION L27 claim electron spin is wake-induced, which conflicts with "keeps the spin it has".
- **A-109 Inertial Memory** (registry L15). This is the inertia node. No file in the slice uses it.
- **C-310 Resistance Field** (registry L47, via C-3114). This is the resistance node and is relevant to "resistance = mass / organization". It is not used elsewhere in the slice.
- **C-311 Electric-Magnetic Duality** (registry L46, L88; GRAVITY_WAKE L432). GRAVITY_WAKE cites it as "organized residual enables wake persistence" and uses it to support magnetic locking. This conflicts with the canon "magnetism opens the point".
- **C-319 Magnetic Coherence** (FRAMEWORK_COMPLETION_STATUS L103-109). It is presented as "OPEN (relieve pressure) → FLOW → LOCK (hysteresis)". OPEN matches the canon "magnetism opens"; LOCK (hysteresis) is not canonical.
- **A-115 Unified Compression Field** (registry L87, via I-09). This is the gravity baseline when R = 0. No slice file uses it, and the gravity formulas in FIVE_STATES L195 and COMPLETION L81 bypass it.
- **E-528 Static Redshift Transport** (registry L86, via I-08). This is the canonical redshift. FIVE_STATES and GRAVITY_WAKE instead assume expansion.
- **C-317 Boundary-Tension Weave** (FRAMEWORK_CHAIN L55-66; INTEGRATION L231). Its twist/vorticity term η_T is called "angular momentum" (Point/Field mix).
- **C-318 Four-Interaction Mass-Effect Response** (FRAMEWORK_CHAIN L71-83). Mass is defined as the resistance to motion of the bound configuration, via M_ij = d²E_4/dv_i dv_j.
- **E-503 Pressure (Gradient Form), E-504 Surface, A-104 Gradient, A-112 Persistent Mode** (FRAMEWORK_CHAIN). These are the field gradient, confinement and persistence. Charge is taken as the sign of ∇ψ, and mass comes from K_p.
- **C-323 Displacement Interaction Regimes** (GRAVITY_WAKE L423; INTEGRATION L231). Cited as "compression wake as gravity mechanism".
- **D-600 / D-601 / D-602** (MANUSCRIPT; GRAVITY_WAKE L424). These cover dispersion, eigenmodes, and E/B from the vector Laplacian. The B-like mode is field curl only.
- **D-409 lattice** (FRAMEWORK_COMPLETION L12, L75; FRAMEWORK_VALIDATION L244; INTEGRATION L231) and **D-408** (INTEGRATION L231). These are the lattice substrate. A 3D volumetric D-409 is still needed for galaxy rotation.
- **C-322** (INTEGRATION L231). Cited only, with no content.
- **C-3118 UNBUILT_PHASE_LOCKING_PROPOSAL** (registry L48). The phase-locking node is unbuilt, but every wake phase-lock claim in this slice rests on phase locking.
- **D-413** (GROK_NEXT L26). Its HTML "still paints the well". Visual only.
- **"ω_s from field"** (GROK_NEXT L26). This is an open item on spin rate.
- **Chapters 06, 07, 08** (MANUSCRIPT L432-434). These are the D-600 dispersion, Maxwell validator and high-energy chapters.

### (b) All conflicts found
1. GRAVITY_WAKE L14-31, L130, L151, L174, L214, L416, L458 and INTEGRATION L43-55, L305: gravity wakes induce or start point rotation. This contradicts "Gravity does not start or affect point rotation" and "keeps the spin it has".
2. GRAVITY_WAKE L73, L130, L180, L319 and INTEGRATION L129: spin and orbit are driven as one wake rate. This contradicts the separation of the Point and Path rates (path rotation carries no L).
3. GRAVITY_WAKE L308-309: "Not angular momentum conservation but wake-phase-locking". This contradicts C-306/C-307 L bookkeeping.
4. GRAVITY_WAKE L341, L347, L351 and INTEGRATION L15, L28, L101: magnetism locks the Moon and Mercury, and without it there is no phase lock. This contradicts "magnetism opens the point", "magnetic channel off must still leave the face" and "no lunar dipole required".
5. GRAVITY_WAKE L387-392, INTEGRATION L177 and L189-192, and COMPLETION L162: a magnetic or EM wake supplies the dark-matter or rotation-curve gravitating role. This contradicts "Magnetism does not become gravity".
6. GRAVITY_WAKE L155 and INTEGRATION L52: Mercury 3:2 is attributed to solar-wake phase lock or precession, not to shared lattice organization.
7. FIVE_STATES L195 (G = dRicci/d(P,E)) and COMPLETION L81, L132 (gravity from lattice curvature): these contradict g = -alpha K_L grad chi with the A-115 baseline.
8. FIVE_STATES L48, L93, L114, L126, L273, L332 and GRAVITY_WAKE L247, L405, L411: expansion and inflation. This contradicts "No expansion, no scale factor; redshift = E-528".
9. FRAMEWORK_CHAIN L63: C-317 twist/vorticity is labelled "angular momentum". Field curl is treated as L, which contradicts the Point/Field separation and C-307 ownership.
10. COMPLETION L107 and L121: magnetic "LOCK (hysteresis)" holds the resonance. Canon has magnetism open the point (dL/dt = 0 open), not lock it.
11. GRAVITY_WAKE L321 and INTEGRATION L131: "ALL moons" are 1:1 locked. This is an empirical overclaim (Hyperion is chaotic).
12. Governance:
    - "proven", "LOCKED", "canonical" and "ORANGE" claims contradict GATE_COLORS.md L29-33 and GENERAL_REFERENCE_RULES L31. Locations: COMPLETION L10 and L294; VALIDATION_STRATEGY L20 and L273; GRAVITY_WAKE L457; INTEGRATION L240 and L312; MANUSCRIPT L422; FRAMEWORK_CHAIN L226.
    - COMPLETION's validators are refuted by VALIDATION_STRATEGY L26-132.
13. Potential only: GROK_NEXT L26 "ω_s from field", if it means deriving point spin from field.
14. Internal inconsistencies:
    - FIVE_STATES octave factor 2 vs 10^5-10^16 length jumps
    - MANUSCRIPT E/B ratio called orthogonality (L160)
    - MANUSCRIPT β→1 photon at the stability edge (L270 vs L110)
    - MANUSCRIPT Phase 4 "Complete" vs "in progress" (L392 vs L262)

### (c) Cross-references outside the slice that matter for point rotation or magnetism
- C319_MAGNETIC_COHERENCE_MECHANISM.md (C-319 OPEN/FLOW/LOCK). Check it against the canon "magnetism opens the point".
- solvers/galaxy_rotation_c319_magnetic_coupling.py. Magnetic coupling to rotation curves carries a risk of magnetism becoming gravity.
- QUANTUM_SCALE_PPF_ALGORITHM_ZERO.md ("Magnetic locking enabling PPF point rotation", electron spin wake-induced).
- UNIFIED_SCALE_INVARIANT_GRAMMAR.md, PPF_QUANTUM_TO_COSMIC.md, ALGORITHM_ZERO_RABBIT_CIRCLE_UNIFIED.md (PPF point/path/field at all scales; gravity-wake causal origin).
- C-323 Displacement Interaction Regimes ("compression wake as gravity mechanism"), C-311 Electric-Magnetic Duality, C-317 / C-318 / C-322, D-408 / D-409, D-600 / D-601 / D-602.
- Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md (the status authority).
- C-308 Spin-half, C-310 Resistance Field, A-109 Inertial Memory, C-3118 (unbuilt phase-locking), A-115, E-528 (all via the alias registry).
- SUPERFLUID_OPERATIONS_FRAMEWORK.md and ONE_WAVE_TERMINOLOGY_FRAMEWORK.md (÷ → gravity mapping).
- PARTICLES_AS_MIRROR_EXCITATIONS.md, CHARGE_AND_ANTIPARTICLES_FROM_FIELD_PRESSURE.md, hadron_knot_geometry.py, higgs_criticality_solver.py.
- D-413 (GROK_NEXT).
