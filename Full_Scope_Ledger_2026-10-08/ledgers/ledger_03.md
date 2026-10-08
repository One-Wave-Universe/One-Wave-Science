# Ledger 03 — Nodes C-313 … D-417 (30 files, all read in full)

## C-313 — Lorentz Invariance vs. Preferred-Frame Conflict   (`Nodes/C-313_Lorentz_Invariance_Conflict.md`)
- Gate / lifecycle: YELLOW / ACTIVE; "Open Conflict Record — Foundational".
- Upstream: A-109 Inertial Memory, A-111 Recursion, C-309 Friction Limit, Book 1 Ch10.   Downstream / cites: C-314, C-315, E-518, all future relativistic reformulations; Chapter 11 damping (L104).
- Core claim: "The first-time-derivative term selects a preferred time direction. It is not exactly Lorentz invariant." (L39). Weak damping gives "an emergent weak-damping approximation, not exact fundamental Lorentz invariance" (L85).
- Equations: psi_i^{n+1}=psi_i^n+(1-gamma)(psi_i^n-psi_i^{n-1})+beta_i(<psi_j^n>-psi_i^n) (L23); psi_tt+mu psi_t-c_eff^2 ∇²psi=0 (L29); mu=gamma/Δt, c_eff²=beta Δx²/(2dΔt²) (L35-36); gamma=muΔt+O(Δt²) (L46); tau_d=1/mu=Δt/gamma (L54); omega=-i mu/2 ± sqrt(c_eff²k²-mu²/4) (L68); epsilon=mu/(c_eff k) (L82).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: frame-transformation behavior of damped medium not derived; no empirical bound on mu, epsilon (L98-99); derive mu(k,s); state whether lattice ground is a physical preferred frame (L103-105); exact D'Alembertian replacement unreconciled (L91).
- Conflicts: none.

## C-314 — Three Frames of Reference   (`Nodes/C-314_Three_Frames_of_Reference.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Application / Formalization Node.
- Upstream: A-101 Ground/Zero (related but distinct), C-313.   Downstream / cites: none yet; I-01 addendum gap "J-106 Reference Frames" (L14-18); A-105, A-112.
- Core claim: three frames proposed by external "V2": Medium Frame (∇Phi=0, not identical to A-101's psi=psi_0) (L28-35); Anchor Frame — comoving rest frame of a Persistent Mode where "internal oscillation is purely radial" (L37-40); Wave-Signal Frame at local phase velocity (L42-44).
- Equations: none (L46-49).
- Point / Path / Field role: none stated (Anchor Frame defined with purely radial internal oscillation — no point spin discussed).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Medium Frame vs A-101 disambiguation not done; no math connecting frames; inherits C-313 (L59-71).
- Conflicts: none.

## C-315 — Wave Reader V1 (Hardware Specification)   (`Nodes/C-315_Wave_Reader_V1.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Engineering / Applied Hardware.
- Upstream: E-503 Pressure (Gradient Form), C-311 Electric-Magnetic Duality.   Downstream / cites: future Android Build Book; A-112, A-105, E-518, I-02, C-313; Book1 Ch4/6/10/13.
- Core claim: differential nulling between two mirrored out-of-phase emitters; hypothesis that a Persistent Mode creates a nonlinear "distortion tail" so null shows residual scalar-potential fluctuation correlating with nearby mass/charge (L27-43). Derived targets CMRR ~120 dB, phase match <~0.08° for 1e-6 residual (L84-93); topology: single master oscillator + 180° splitter, matched drivers/sensors, instrumentation amp, 24-bit ADC, digital lock-in (L95-108).
- Equations: none derived (L45-51) beyond the stated numeric targets.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (residual "correlating with nearby mass/charge" L41-42 only).
- Open / parked / not-set items: distortion tail not connected to any field equation (L64-66); inherits C-313; no build exists (L78-80); "This resolves HOW to look, not WHAT will be found" (L119).
- Conflicts: none.

## C-316 — Charge-Sign and Direction Conflation Inside Book 1 Chapter 11   (`Nodes/C-316_Charge_Sign_Convention_Conflict.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Resolved Conflict Record / Formalization Target.
- Upstream: Book1 Ch4, Ch11, C-311, B-203 Expression, B-204 Compression, A-104 Gradient.   Downstream / cites: future repo-wide charge-sign spec.
- Core claim: Ch11's "compression-dominant, inward" electron labels were local errors and corrected; signed boundary-pressure orientation and spatial gradient direction are separate quantities (L32-39).
- Equations: P_q = s_q P_c, s_q ∈ {-1,+1}; G_q = ∇P_q (L44-52); annihilation +P_c + (-P_c) = 0 (L71).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: units/proportionality from P_q, G_q to measured charge underived; C-311 must be audited for same conflation; whole-mode dominance undefined (L82-86).
- Conflicts: none.

## C-317 — Boundary-Tension Weave   (`Nodes/C-317_Boundary_Tension_Weave.md`)
- Gate / lifecycle: GREEN / ACTIVE; detail YELLOW (geometry/energy) / GREEN (full QCD replacement claim).
- Upstream: A-112, A-116, E-503, E-504, E-505, Book1 Ch2.   Downstream / cites: C-318, C-321, C-322, Book1 Ch2/Ch6, D-409, solvers/JOINT_RESPONSE_DERIVATION.md, joint_boundary_response.py.
- Core claim: "continuous 3D surface-and-volume coupling that holds Vortex Phases inside a bounded knot" (L24); gluon -> Tension-Link excitation (L26); Knot Lock: extraction cost does not fall with separation (L123).
- Equations: E_weave=E_skin+E_phase+E_twist (L47); E_skin=sigma_T ∫dA (L53); E_phase=(kappa_T/2)Σ_{a<b}∫|psi_a-psi_b|²dV (L59-64); E_twist=(eta_T/2)Σ_a∫|∇×v_a|²dV (L69-74); r=R_p+eta, eta=Σa_lm Y_lm (L83-90); A_neck≈2πaL, E_neck≈2πa sigma_T L, tau_T≡2πa sigma_T, F_lock=dE_neck/dL=tau_T (L99-121); E_neck≥E_break ⇒ neck break + new knots (L127-131); resolvent H−ω²W−iω(BBᵀ+Γ) (L146).
- Point / Path / Field role: Field — twist/vorticity term ∇×v_a is internal field curl (L69-74). Point / Path: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: sigma_T, kappa_T, eta_T, a unknown; spectrum unmatched; running coupling, reweaving products not derived (L165-169); self-held knot, absolute units not achieved (L187); Bronze requirement (L179).
- Conflicts: none against canonical rules. (Gate GREEN in front matter while claim_gate_detail and audit are YELLOW — internal labeling tension only.)

## C-318 — Four-Interaction Mass-Effect Response   (`Nodes/C-318_Mass_Mechanism_Candidate_Resolution.md`)
- Gate / lifecycle: GREEN / ACTIVE; GREEN (mechanism identity) / YELLOW (profiles, coefficients, spectrum).
- Upstream: A-109, A-112, A-115, C-301, C-311, C-317.   Downstream / cites: Book1 Ch1/2/14/15, C-322, C-309, C-313, Internal_Proofs/Boundary_Coupling_and_Phase5_Audit.md, solvers/joint_boundary_response.py, BULK_EXCITATION_DERIVATION.md, D-409.
- Core claim: "Mass Effect is the resistance produced when the complete four-interaction recurrence must be displaced, carried, and rebuilt relative to Ground." (L177). Four interactions K/E/M/T are one field configuration (L34-41). Propagation-status-as-inertia permanently erased (L22). Mirror-Gate: "The boundary is not forced through" (L274); 125 GeV is not a penetration threshold (L276). Phase-5 quark spectrum/125 GeV claims withdrawn (L353-362).
- Equations: Z=(Z_K,Z_E,Z_M,Z_T) (L45-53); Ē_4=<E_K+E_E+E_M+E_T+E_×> (L60-66); ∇_q Ē_4(q_0)=0, H_0≻0 (L74-85); ||Z_{n+k}-Z_n||<ε (L92); D_t Z_a=∂_t Z_a − Ẋ·∇Z_a (L104-108); Ē_4(v)=Ē_4(0)+½v_i M_ij v_j (L113-119); M_ij=∂²Ē_4/∂v_i∂v_j (L126-132); F≈M_ij a_j (+C_ij v_j drag) (L137-158); m_eff=⅓TrM (L166-170); ΔE_carry, M_jk=ΣΔV (D_jZ_0)ᵀW(D_kZ_0) (L210-231); W 4×4 block (L249-256); [M]=kg (L265-270); E_phys=ε_lat E_dimless, W→λW ⇒ M→λM (L294-312); R_G=E_MG/(m_eff v_lat²) (L333-339).
- Point / Path / Field role: Point — rotations are permitted zero-modes excluded from H_0 (L87); "structural resistance" of knot (L36). Path — translation X(t) carried relative to Ground (L99-108). Field: none stated separately.
- Magnetism / gravity / rotation link: none stated beyond C-311 upstream; drag C_ij must not be absorbed into M (L161).
- Open / parked / not-set items: work metric W and absolute energy scale ε_lat underived — "cannot output kilograms or GeV" (L261, L314); stable native 3D profile, small-velocity differentiation, traveling-light control (L368); bulk excitation is hypothetical closure (L386).
- Conflicts: none against canonical rules. (Mass as carried-pattern resistance relative to Ground; canonical "resistance = mass / organization" is not contradicted but not cited.)

## C-319 — Magnetic Lattice Reorganization   (`Nodes/C-319_Magnetic_Lattice_Reorganization.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS; GREEN (contract) / BROWN (coefficients uncalibrated).
- Upstream: C-311, D-408, D-409, A-104; Lateral C-306, C-307, D-401, E-505.   Downstream / cites: C-320, D-413, D-416; discrete_maxwell_solver_v4.py, faraday_scaling_test.py.
- Core claim: "Magnetism reorganizes the available lattice pathways." (L25). C-306/C-307 remain authority for torque/L (L116). "Magnetism opens the point. Closed, it resists. That is the turn. The magnetic gradient is the opening. It does not invent a pull. Gravity does not turn the point. Path rotation is not this node." (L156-158).
- Equations: R=0 at isotropic Ground (L42); W_B=B⊗B−|B|²I/3, Tr W_B=0 (L50-60); tau_R ∂_t R=−R+λ_B W_B+λ_ω W_ω (L67-71); K_L=I+κ_R R (L81-83); R→0⇒K_L→I (L93-95); R(t)≠R_eq[B(t)] memory (L107); handoff C-311→C-319→C-320→C-306/C-307 (L120-125).
- Point / Path / Field role: Point — magnetism opens the point; closed resists (L156). Path — explicitly "Path rotation is not this node" (L158); paths here are lattice routes, reorganized by R. Field — B as rotational projection; W_ω optional circulation history (L74).
- Magnetism / gravity / rotation link: magnetism reorganizes paths; "No step may be skipped by saying 'magnetism equals gravity' or 'magnetism directly causes torque'" (L127); gravity does not turn the point (L158).
- Open / parked / not-set items: λ_B, λ_ω, τ_R, κ_R uncalibrated (L74); hysteresis test; sign-sensitive effects need extra handed/curl variable (L138); 2D only precursor (L131-133). dL/dt = 0 / −γL equations not written here.
- Conflicts: none.

## C-320 — Magnetic-Compression Path Coupling   (`Nodes/C-320_Magnetic_Compression_Path_Coupling.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS; BROWN (coefficients, fit).
- Upstream: A-104, A-105, A-115, C-306, C-307, C-319, D-409; Lateral C-311, D-401, E-503, E-505.   Downstream / cites: D-413, D-416, Book1 Ch12 Gravity, Ch13 Electricity/Magnetism.
- Core claim: "magnetism does not become gravity; magnetic reorganization changes the lattice through which the compression/restoring bias is expressed." (L266). Sand-through-sieve path-accessibility picture, no literal ether (L211-223).
- Equations: χ=−∇·u (L230); g_0=−α_g∇χ (L236); g_OW=−α_g K_L∇χ, g_i=−α_g K_L,ij ∂_jχ (L252-261); R→0⇒K_L→I⇒g_OW→−α_g∇χ (L270-276); ∇χ=0⇒g_OW=0 (L292-296); τ=∫ r×(ρ_eff g_OW) dV (L305-310).
- Point / Path / Field role: Field — χ, ∇χ compression gradient. Path — K_L path accessibility. Point — torque from off-center path-weighted restoring field handed to C-306/C-307 "-> torque -> rotational/orbital evolution" (L302-323).
- Magnetism / gravity / rotation link: magnetism reorganizes, gravity is A-115 restoring response; off-center g_OW (including baseline g_0 when R=0) produces torque and "rotational/orbital evolution" (L314-323); locking must emerge dynamically (L325). Planetary set Moon/Mercury/Venus/Uranus/Neptune (L345-349).
- Open / parked / not-set items: α_g, κ_R unset; D-413 still uses imposed well (L331); six failure conditions (L357-362).
- Conflicts: L300-323 — a gravity/compression restoring field (g_OW, which reduces to pure g_0 at R=0) generates torque and "rotational/orbital evolution" on an extended body. Canonical rule: "Gravity does not start or affect point rotation." The chain does not separate Point rotation (L = Iω) from Path rotation (orbit), so as written gravity torque feeds spin. Tension also with "magnetic channel off must still leave the face" not stated (it only requires baseline recovery).

## C-321 — Reduced Multi-Center Tension Network   (`Nodes/C-321_Reduced_Multi_Center_Tension_Network.md`)
- Gate / lifecycle: GREEN / ACTIVE; YELLOW (N=3) / GREEN (N>3 & nuclear).
- Upstream: C-317, A-112, A-116, A-117, D-409.   Downstream / cites: future separated-center sims; nuclear bridge only after inter-nucleon law (D-406 cites it).
- Core claim: applies only in slender-neck regime a_i/L_i≪1 (L22-28); N=3 equal tensions meet at 120° (Fermat/Torricelli) (L91); must not be used as carbon-12 binding law (L132).
- Equations: E_i≈τ_iL_i (L37); E(J)=Στ_i|J−q_i|+E_J (L43-46); ∇_J E=Στ_i ê_i+∇_J E_J=0 (L53-58); ê_i·ê_j=−½ (L88); cosθ_ij=(τ_k²−τ_i²−τ_j²)/(2τ_iτ_j) (L96-98); E_Δ, E_Y (L108-123).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: τ_i, neck radii, E_J underived; N>3 open; inter-nucleon law missing (L136-141).
- Conflicts: none.

## C-322 — Mirror-Gate Boundary Coupling and Phase Response   (`Nodes/C-322_Mirror_Gate_Higgs_Scale_Resonance.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS.
- Upstream: A-115, B-205, B-206a, C-301, C-317, C-318.   Downstream / cites: Book1 Ch15, measurement pipeline; solvers/test_mirror_gate_coupling.py; joint_boundary_response.py.
- Core claim: "An incident disturbance cannot be forced through the boundary. It may bounce or reflect, deflect, roll off tangentially, or scatter." (L19). Supersedes forced-crossing threshold interpretation (L21). 125 GeV peak "is not a direct measurement of forcing a proton boundary through a gate" (L53); never stop a scan at 125 GeV and call it prediction (L55).
- Equations: a_out=S a_in, S=exp(−iHτ), H=H† (L32); P_in−P_out=dE_stored/dt+P_diss (L46); S†S⪯I passive (L49).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: absolute normalization, microscopic coupling law, stable 3D profile, collider discriminator open (L66); fixture labels do not implement spatial geometry (L37).
- Conflicts: none against canonical rules (but see C-323, D-414 which contradict this node).

## C-323 — Displacement Interaction Regimes of the Unified Compression Field   (`Nodes/C-323_Four_Forces_as_Displacement_Regimes.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Field Identity / Continuum Interaction Stress.
- Upstream: A-102, A-105, A-106, A-115, C-311, C-318, C-322, E-532; Lateral D-408, D-414, "D-415 Hexagonal Lattice Force Dynamics" (now D-417).   Downstream / cites: hexagonal runs, wake profile, residual spectrum; E-531, Book1 Ch12, Book5 Ch1, D-412.
- Core claim: one displacement field; gravity = local ∇χ response; dark matter = wake of same field; "No second substance. No carrier particles." (L27-33, L171).
- Equations: χ=−∇·u (L46); σ_ij=Kχδ_ij+2μ(ε_ij−⅓θδ_ij)+α∂_iχ∂_jχ+βC_iC_j−γ(∇²χ)δ_ij (L61-72); R_i=∂_jσ_ij, ρü_i=R_i (L80-82); Φ_OW=α_gχ, g_OW=−α_g∇χ (L94-96); g=g_local+g_wake (L106); ρ_DM,eff=−∇·g_wake/(4πG_eff) (L112); E_MG=Ē_4(q_G)−Ē_4(q_0)≈125 GeV "(empirical anchor)" (L121-126); E~∇P_c, B~∇×P_c (L136-138); range~sqrt(γ/K) (L148-150).
- Point / Path / Field role: Field — compression χ, gradient, wake; wake "left by motion and rotation of bound structure" (L109). Point / Path: none stated as separate rates.
- Magnetism / gravity / rotation link: gravity = A-115 ∇χ view (L94-99); magnetism only as B~∇×P_c projection of oriented residual (L133-141). No magnetism→gravity claim.
- Open / parked / not-set items: discretize on D-408; derive g_wake(r) without galaxy fit; close A-115/C-318 bridge (L185-188).
- Conflicts: L117-129 and L166 define Mirror-Gate as "finite work to cross orientation basin" / "the first orientation-basin crossing" with E_MG ≈ 125 GeV as anchor and "large-deformation work across the basin boundary". This contradicts C-322 L19-21 (forced-crossing threshold interpretation superseded; boundary cannot be forced through) and C-318 L274-276 (125 GeV is not an established penetration threshold). Dependency label L18 "C-322 Mirror-Gate 125 GeV Boundary Response" is stale. Also lateral ref "D-415 Hexagonal Lattice Force Dynamics" (L19) is stale (renamed D-417).

## C-324 — No Entanglement — Detector Map   (`Nodes/C-324_No_Entanglement_Detector_Map.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Principle / Measurement Mathematics.
- Upstream: A-110, A-103, B-205, B-223, B-224, C-315.   Downstream / cites: RABBIT-HOPPING build/CELL0, NO_ENTANGLEMENT.md, Book1 No Entanglement chapter.
- Core claim: "There is no entanglement in this science." (L19); "Two sites affect each other only through a net you can point at." (L22).
- Equations: u=A cos(kx−ωt+φ) (L29); s(t*)=sign(u(x_d,t*)) with dead zone T (L35-45); Δx=vΔt (L54-55); sinθ≈(τ_L−τ_R)v/B (L65).
- Point / Path / Field role: Path — "named path" for wave propagation (L21, L27); none on Point/Field rotation.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: physics-vs-lab-QM YELLOW (L78-79).
- Conflicts: none.

## C-325 — Transfluxor Magnetic Solver Triangulation and Reality Gate   (`Nodes/C-325_Transfluxor_Magnetic_Solver_Triangulation.md`)
- Gate / lifecycle: BROWN / ACTIVE_HYPOTHESIS.
- Upstream: C-311, C-319, C-320, D-401; Lateral C-306, C-307, G-749 Point Rotation, G-769 Path Rotation, D-408/D-409.   Downstream / cites: D-413, transfluxor receipts, V1 matrix; chapters/09_Transfluxor_Magnetic_Reorganization_and_Point_Rotation.md; Builds repo validation docs; Chapter 07.
- Core claim: owns the experimental gate; "does not duplicate C-319's reorganization law, C-320's compression coupling, or G-749's point-rotation law" (L16). Three propositions C325-A/B/C (L29-33). Non-conflation: "Magnetic-moment rotation ≠ point-frame rotation ≠ path turning ≠ mechanical motor torque." (L49).
- Equations: none.
- Point / Path / Field role: explicitly separates point-frame rotation, path turning, magnetic-moment rotation and motor torque (L49); LLG vs rigid-body rotation measured separately (L31).
- Magnetism / gravity / rotation link: magnetic precession cannot be inferred to shaft angular velocity without coupling measurement (L31).
- Open / parked / not-set items: TEST DEFINED only, no experiment (L55).
- Conflicts: none.

## D-401 — Flux   (`Nodes/D-401_Flux.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-112.   Downstream / cites: D-402; A-109; Wave Reader (C-315).
- Core claim: "Flux = field of a persistent mode threading space and coupling outward" (L22); persistent mode satisfies discrete harmonic condition <ψ_j>=ψ_i (L34-36); exponential profile NOT derived (L38-49).
- Equations: A-109 update (L29); 0=β_i(<ψ_j>−ψ_i) (L32); Φ(x)~A exp(−|x−x_0|/λ) sketched only (L40).
- Point / Path / Field role: Field — surrounding field of a persistent mode. Point/Path: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: screening term, λ, conservative vs dissipative (L58-70).
- Conflicts: none.

## D-402 — Resonant Mode   (`Nodes/D-402_Resonant_Mode.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: A-111, A-112, D-401.   Downstream / cites: D-403, D-404, D-405, B-221; E-508.
- Core claim: persistent mode returning to itself after k steps (L19-22).
- Equations: ψ_{n+k}=ψ_n (L26); update rule (L35); ||ψ_{n+k}−ψ_n||<ε AND periodic (L41).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: stability under perturbation; loss deferred to E-508 (L47-50). Note L34 attributes update rule to A-111 (C-313/D-401 attribute it to A-109) — attribution inconsistency, not canonical conflict.
- Conflicts: none.

## D-403 — Spherical Modes   (`Nodes/D-403_Spherical_Modes.md`)
- Gate / lifecycle: YELLOW / HELD.
- Upstream: D-402.   Downstream / cites: Books atomic structure; D-405; characteristic_equation_solver.py, discrete_maxwell_solver_v4.py.
- Core claim: 3D bounded resonant mode with angular structure (L19-23).
- Equations: ∇²ψ+k²ψ=0; ψ=R(r)Y_l^m (L27-36).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (m labeled "magnetic quantum number" L36, nomenclature only).
- Open / parked / not-set items: angular numbers, degeneracy not derived; extend to 3D vector ψ (L45-66).
- Conflicts: none.

## D-404 — Nested Resonance   (`Nodes/D-404_Nested_Resonance.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS.
- Upstream: D-402.   Downstream / cites: Books proton/quark; Book1 Ch2.
- Core claim: harmonic generation GREEN; stable nested sub-mode HYPOTHESIS (L38-39).
- Equations: f_n = n f_0 harmonics (L30).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: stability, nonlinearity conditions (L47-50).
- Conflicts: none.

## D-405 — Harmonic Shell   (`Nodes/D-405_Harmonic_Shell.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: D-402, A-110.   Downstream / cites: Books atomic shells; D-407; CCD-01; A-114.
- Core claim: "D-405 currently quantizes geometry. It does not yet quantize energy." (L68).
- Equations: 2πR=nλ (L25); R_n=nλ/2π, ΔR=λ/2π (L34-35); k_n=n/R (L49); k_n=2π/λ independent of n (L56).
- Point / Path / Field role: Path — closed-path standing wave (L20-21); otherwise none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: energy model choice; λ not measured; 0.6594 fm conditional (L105-113).
- Conflicts: none.

## D-406 — Isotope Stability via Outer-Shell Coupling Density   (`Nodes/D-406_Isotope_Stability_Coupling_Density.md`)
- Gate / lifecycle: GREEN / BLOCKED (pending inter-nucleon bridge).
- Upstream: Book1 Ch5, A-108, A-112; conditional C-321.   Downstream / cites: carbon-12 vs 14; C-318, Book1 Ch14.
- Core claim: coupling has a density; stability optimum near N≈Z predicted qualitatively, not derived (L37-54, L96-99).
- Equations: CouplingDensity(i)=Σ_j coupling_strength(i,j)/ExpectedCoupling (L62); decay if < threshold (L65); stable IFF all ≥ threshold (L72).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: coupling_strength, threshold underived; blocked on C-321 bridge (L90-101).
- Conflicts: none.

## D-407 — Harmonic Shell / Two-Shell Neutron Calibration Reanalysis   (`Nodes/D-407_Harmonic_Shell_Calibration_Attempt.md`)
- Gate / lifecycle: YELLOW / ACTIVE (partial resolution).
- Upstream: D-405, A-114, Book1 Ch5.   Downstream / cites: carbon-12/Hoyle (blocked).
- Core claim: σ is a width, not shell spacing (L62-71); nearest adjacent assignment n=7,8; λ*=0.659395 fm conditional (L87-126); D-405 family gives ΔE=0 from dispersion alone (L144-147).
- Equations: Gaussian profiles (L44-45); ΔR_center=0.1078 fm; σ/ΔR=1.9481 (L50-51); n_est=6.800557 (L83); λ_+=0.658029, λ_−=0.660441 fm (L92-93); λ*=2π(7R_+ +8R_−)/(7²+8²)=0.659395 fm (L99-100); k_n=2π/λ (L140).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: adjacency derivation, fit provenance/uncertainty, geometry→energy map (L193-198).
- Conflicts: none.

## D-408 — Sixfold 2D Triangular-Hexagonal Lattice   (`Nodes/D-408_Sixfold_2D_Triangular_Hexagonal_Lattice.md`)
- Gate / lifecycle: GREEN / ACTIVE; YELLOW geometry / GREEN interpretation.
- Upstream: A-101, A-102, A-104, A-117, B-206; Lateral D-411, D-412, E-520, E-524.   Downstream / cites: C-319, D-413, circulation/quark-phase/Wave Computer sims; D-409.
- Core claim: native 2D lattice, 6:1 coordination (L37-41); 3:1 axis-pair ↔ 6:1 directed view (L48); seven-cell cluster (L67); circulation Γ_6 nonzero "is not by itself a quark" (L115); magnetic reorganization changes edge/path weights, not a renderer distortion (L119).
- Equations: a_1=a(1,0), a_2=a(½,√3/2) (L26-28); r_mn (L34); ε_ij strain (L89-91); Γ_6=Σ v_k·Δℓ_k (L109-112); u_i=0, v_i=0 Ground (L147-150).
- Point / Path / Field role: Field — circulation/vorticity proxy on hexagonal rings (L100-115). Path — edges as routes; C-319 path weights (L117-119). Point: none stated.
- Magnetism / gravity / rotation link: first planar control for C-319; any magnetic-gravity planetary claim requires D-409 (L180).
- Open / parked / not-set items: required first simulations (L157-164); non-nearest couplings need declared rules (L141).
- Conflicts: none.

## D-409 — Twelvefold 3D Close-Packed Coordination   (`Nodes/D-409_Twelvefold_3D_Close_Packed_Coordination.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: A-116, A-117, D-408, D-411, D-412, C-317.   Downstream / cites: C-319, C-320, D-416, Vortex-Phase/knot/Mass-Effect sims; BULK_EXCITATION_DERIVATION.md.
- Core claim: native physical layer is 3D, 12:1 (L20-24); P_{3→2}(N_12) ≠ N_12 (L62-65); locked route C-311→C-319→C-320→C-306/C-307→D-416 (L105-111).
- Equations: N_12=(a/√2){(±1,±1,0),(±1,0,±1),(0,±1,±1)} (L32-40); 13 sites (L48); X_i^(3)=(u,v,φ,χ,q,B) (L74-83).
- Point / Path / Field role: q_i "rotational/circulation state" variable (L92) — Point and Field rotation not separated; Path: none separately. Required behaviors include "rotational flow and vorticity" and "rotational perturbation and vorticity retention" (L119, L145).
- Magnetism / gravity / rotation link: required geometry for C-319/C-320; "Neither node may discard out-of-plane routes and then claim a planetary result" (L101); torque/angular accounting via C-306/C-307 (L109).
- Open / parked / not-set items: update law not derived (L95); FCC vs HCP untested (L51); Mirror-Gate response "without forced geometric penetration" (L123).
- Conflicts: none (single q_i lumps rotation/circulation — incompleteness relative to three-rate rule, not a direct contradiction).

## D-410 — Twenty-Fourfold 4D Field/Void Recurrence Shell   (`Nodes/D-410_TwentyFourfold_4D_Field_Void_Recurrence_Shell.md`)
- Gate / lifecycle: YELLOW / ACTIVE; BRONZE architecture / YELLOW physical.
- Upstream: A-111, A-117, B-205, B-206, C-301, D-409; Lateral G-716, G-716a.   Downstream / cites: recurrence sims, Mirror-Gate trajectory analysis, Wave Computer.
- Core claim: 4D layer is ordered evolution of 3D state, not a spatial dimension (L21-39); 24:1 = recurrence/state coordination, not neighbor count (L74-80).
- Equations: X^(4)(n)=(X^(3)_n,φ_n,g_n,d_n,h_n) (L26-28); R_24={F_1..F_12,V_1..V_12} (L52-54); gate 1(0)1 (L107); ε_R(T)=||X(t+T)−M X(t)||/(||X(t)||+ε) (L146-148); G-716 24→12→6→3→1→24 (L166).
- Point / Path / Field role: none stated (d_n directional state only).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: physical spacing/timing of 24 positions Yellow (L66).
- Conflicts: none against canonical rules. Minor: "Mirror-Gate crossing" log language (L21, L112-120) predates C-322's no-forced-crossing rule; D-410's crossing is state-coordination, so only a terminology tension.

## D-411 — Mirrored Axis Pairs and Directed Route Counts   (`Nodes/D-411_Mirrored_Axis_Pairs_and_Directed_Route_Counts.md`)
- Gate / lifecycle: YELLOW / ACTIVE; BRONZE counting.
- Upstream: A-103, A-117, B-205, D-408, D-409, D-410; Lateral G-719, G-720.   Downstream / cites: sim headers, Android routes, ratio audits.
- Core claim: N axis pairs → 2N directed routes → 2N+1 centered states (L30); "same ratio ≠ same domain" (L81).
- Equations: −d (0) +d (L46); c∈{−1,0,+1}, Δq=c d_a (L89-95); count ladder table (L51-56).
- Point / Path / Field role: Path — directed routes counting; center is "hold/reference", not a direction (L33). Point/Field: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: 3D opposite-pair mapping must be declared; 4D row candidate (L60-62).
- Conflicts: none.

## D-412 — Lattice Simulation and State-Driven Visualization Standard   (`Nodes/D-412_Lattice_Simulation_and_State_Driven_Visualization_Standard.md`)
- Gate / lifecycle: YELLOW / ACTIVE; BRONZE standard.
- Upstream: A-102, A-103, A-105, A-117, C-317, D-408–D-411; Lateral I-02, G-706.   Downstream / cites: D-413 and all physical sims.
- Core claim: simulation state → measured fields → visualization; prohibited reversal "desired picture → animation pretending to be evidence" (L24-31). "The Mass Effect is measured after a complete stable recurrence exists. It is not inserted as an initial parameter." (L133).
- Equations: u_i=0, v_i=0, ΔX_i=0 (L45); X_i(t)=(u,v,φ,χ,q,B) (L55).
- Point / Path / Field role: Field — vorticity view, circulation (L76-77); q "circulation/rotation state" (L64) — not split into point/path/field. Point/Path: none stated separately.
- Magnetism / gravity / rotation link: none stated directly; describes D-413 "torque-based axial spin" (L138).
- Open / parked / not-set items: physical implementations pending.
- Conflicts: none directly (inherits D-413 spin description at L138; see D-413).

## D-413 — Ground Lattice Orbital-Restoring Simulation   (`Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-101, A-102, A-103, A-105, A-109, A-115, A-117, C-319, C-320, C-317, D-408, D-411, D-412; Lateral B-202, C-306, C-307, D-409, E-502, E-503, E-506.   Downstream / cites: D-416; 00_MASTER_INDEX.md; runnable dir D-413_.../ (index.html, simulate_d413.py, results/).
- Core claim: runnable 2D Ground lattice with imposed Gaussian well; "turn an off-center fall through a curvature well into orbital motion; generate axial torque when unequal restoring forces act across an asymmetric bounded shell" (L57-58); "Spin is not inserted as an animation command." (L225); current code does not implement C-319/C-320 (L45); well is imposed, not derived gravity (L140).
- Equations: X_i=X_i^0+u_i (L95); F_ij spring+damper (L103-107); F_i,Ground=−k_0u_i−c_0v_i (L113-114); z_G Gaussian (L124-125); z_display=z_force (L135); K_L, g_OW (L149-155); Q=(q,q̇,θ,ω) (L178); f_a=−g_R∇z(q+r_a) (L186); F_Q (L192); τ_Q=(1/N_s)Σ r_a×f_a − c_ω ω (L198-205); I_Q ω̇=τ_Q (L210).
- Point / Path / Field role: Point — axial spin ω with I_Q, generated by restoring-field torque and damped by −c_ω ω (L198-211). Path — orbit of centroid q (L57, L215-223). Field — lattice strain, wake; circulation/vorticity "derived from lattice state" still required (L301). Field curl not implemented.
- Magnetism / gravity / rotation link: gravity-like well torque produces axial spin: "displacement falls across the depression -> restoring force is unequal across the shell -> ... -> torque appears -> orbit and axial spin may emerge" (L216-223); C-306/C-307 authority (L227); magnetic channel OFF must exactly recover baseline (L171).
- Open / parked / not-set items: source-derived χ, C-319/C-320 implementation, 3D translation, work ledger (L289-304).
- Conflicts: (1) L57-58, L213-225, L282 — the gravity/curvature well starts axial (point) spin from rest on an asymmetric shell. Canonical: "Gravity does not start or affect point rotation" and "A thing keeps the point spin it has; it does not start one on its own." (2) L198-205 — point spin is decayed by a generic drag −c_ω ω with no magnetic open/closed distinction; canonical: open magnetic gradient dL/dt = 0, closed dL/dt = −γL. (3) D-412 L138 repeats "torque-based axial spin".

## D-414 — Four-Interaction Shell Simulation (Real Data as Wave Data)   (`Nodes/D-414_Four_Interaction_Shell_Simulation.md`)
- Gate / lifecycle: YELLOW / ACTIVE; illustrative reduced model.
- Upstream: C-318, C-317, C-311, C-301, C-322 "(125 GeV anchor)", A-115.   Downstream / cites: One_Wave_Bench ledger; B-220, B-221, B-222, B-224, A-108; Wiki_Pages/D-414_Wiki_Page.html; assets dir.
- Core claim: renders four C-318 channels driven by real datasets (LIGO, EEG, reactor kinetics, CODATA) as wave inputs; "does not claim to prove gravity, charge, the proton, or Mass Effect" (L69-71).
- Equations: Mirror M²=−I, M⁴=I (4π closure) (L43); otherwise none.
- Point / Path / Field role: Field — toroidal flow (L60); retained wake as dark-matter view (L65). Point/Path: none stated.
- Magnetism / gravity / rotation link: LIGO strain drives Mirror-Gate channel (L52, L62) — analogy only.
- Open / parked / not-set items: geometry and couplings candidate (L69).
- Conflicts: L21, L32, L52 treat 125 GeV / 125.11 GeV Higgs as "mirror-gate boundary scale"/"anchor" and L62 a "crossing ring that flashes when the LIGO strain amplitude passes threshold" — contradicts C-322 L19-21, L53-55 (no forced crossing; 125 GeV not a gate threshold) and C-318 L276. Also L52 "GW150914 (BBH, break-crossing)" same threshold framing.

## D-415 — Nonlocal Three-Excitation One-Field Bench   (`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS.
- Upstream: none listed in header.   Downstream / cites: planetary_visual.html, render_galaxy_video.py, sweep_math_gaps.py, MATH_GAPS.md (in D-415_ dir); Gray multipole control.
- Core claim: one continuous complex Field Ψ instead of three point masses; "measured centers do not source pairwise forces" (L31-34); trace records "separate internal Point, relational Path, and surrounding Field rotations" (L93).
- Equations: Ψ_next=Ψ+(1−γdt)(Ψ−Ψ_prev)+dt²[c²Δ_6Ψ−αΨ−β|Ψ|²Ψ−κ(Ψ−K*Ψ)] (L43-49); q_k=∫r W_k e/∫W_k e (L61).
- Point / Path / Field role: explicitly records Point, Path, Field rotations separately (L93); next target "derive a conserved Point–Path–Field transfer ledger" (L109). Planetary visual described as "Point–Path–Field projection" (L16).
- Magnetism / gravity / rotation link: none stated (galactic arm formation visual only).
- Open / parked / not-set items: potential and kernel candidate; persistent excitations, energy/rotation ledger, 3D geometry (L101-113).
- Conflicts: none.

## D-416 — Planetary Rotation-Magnetic Coupling Test Matrix   (`Nodes/D-416_Planetary_Rotation_Magnetic_Coupling_Test_Matrix.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS; BROWN magnetic-lock prediction.
- Upstream: A-115, C-306, C-307, C-311, C-319, C-320, D-409, D-412, D-413; Lateral D-401, E-505.   Downstream / cites: future 3D planetary sim; NASA references (L45-52).
- Core claim: "One coupling law must face the awkward bodies as well as the convenient ones." (L25); "Locking Is an Output, Not an Input" (L92); Moon model requiring present global dipole fails (L35, L142); Mercury must reach/preserve 3:2 not 1:1 (L36, L143).
- Equations: P=(ω_spin,n_orb,e,θ_spin,θ_B,δ_B/R,B_int,B_ind,χ,∇χ,R,K_L) (L59-75); Δφ_{p:q}=qφ_spin−pφ_orb (L97); Moon 1:1, Mercury 3:2 (L104-105).
- Point / Path / Field role: Point — ω_spin, θ_spin; Path — n_orb, e; Field — χ, ∇χ, R, K_L, B fields. Not framed as the three-rate rule explicitly.
- Magnetism / gravity / rotation link: ablations including baseline gravity/tidal model with C-319/C-320 OFF (L113); magnetism must give measurable residual beyond baseline (L122, L146); no lunar dipole required (L35, L142).
- Open / parked / not-set items: One-Wave lock prediction not derived; coefficients must be frozen before comparison (L126-136).
- Conflicts: none direct. Tension: L113, L146 treat "baseline gravitational/tidal model" as the default spin-locking control, implicitly allowing gravity torque to change spin, whereas the canonical rule says gravity does not start or affect point rotation and locking comes from bound-lattice organization (resistance = mass / organization). The node never states "magnetic channel off must still leave the face" as the expected outcome; it is consistent with but weaker than the canonical bound-lattice rule.

## D-417 — Hexagonal Lattice Interaction Dynamics   (`Nodes/D-417_Hexagonal_Lattice_Interaction_Dynamics.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: D-408, C-323, A-115, E-532, E-531, A-105, D-412; Lateral D-413, D-414, D-415.   Downstream / cites: multi-core wake tests; former file D-415_Hexagonal_Lattice_Force_Dynamics.md (L14).
- Core claim: discretize C-323 stress on D-408 lattice; "No forces. Bond objects are restoring responses." (L34).
- Equations: a_1,a_2 (L41-42); e_a=(cos2πa/6, sin2πa/6) (L48); χ_n=−Σ e_a·(u_{n+a}−u_n) (L56); Δχ (L60); I_1, I_3, bound_n=(I_3>½I_1)∧(|u_n|>u_floor) (L66-72); R_{n,a}=Kχ_n e_a+μ(u_{n+a}−u_n)+α(χ_{n+a}−χ_n)e_a+βC_n(C_n·e_a)[bound_n]−γ(Δχ)_n e_a (L81-91); R_n=ΣR_{n,a}, ρü_n=R_n (L97-104); ((H+1)·2+1)−((H+1)·2−1)=2 (L111).
- Point / Path / Field role: Field — compression, wake "left by motion/rotation of bound structure" (L121). Point/Path: none stated.
- Magnetism / gravity / rotation link: gravity view = down-gradient response of cores (L120); no magnetism.
- Open / parked / not-set items: multi-core validation (L160).
- Conflicts: none.

## Slice summary

### (a) Nodes bearing on Point / Path / Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking
- C-313: damped update → preferred frame; inertial memory (A-109) carry-forward is the base of inertia/damping; no rotation content.
- C-317: Field curl term E_twist = (η_T/2)Σ∫|∇×v_a|² inside knot; Knot Lock non-weakening line tension.
- C-318: mass = Mass-Effect tensor M_ij, resistance to carrying the four-interaction recurrence relative to Ground; drag C_ij kept separate from M; rotation zero-modes excluded from H_0.
- C-319: canonical magnetism→lattice-path reorganization (R, K_L); "Magnetism opens the point. Closed, it resists... Gravity does not turn the point. Path rotation is not this node." (L156-158).
- C-320: g_OW = −α_g K_L ∇χ; R=0 → A-115; ∇χ=0 → g=0; magnetism does not become gravity; torque from off-center g_OW → C-306/C-307; planetary set.
- C-323: gravity = ∇χ view; dark matter = wake of same field (incl. rotation wake); B ~ ∇×P_c.
- C-325: experimental gate; non-conflation magnetic-moment rotation ≠ point-frame rotation ≠ path turning ≠ motor torque; cites G-749 / G-769.
- D-408: planar lattice, Γ_6 circulation (Field), C-319 path weights.
- D-409: 3D lattice required for C-319/C-320 and D-416; q_i lumps rotation/circulation.
- D-412: simulation standard; Mass Effect measured not inserted; vorticity views.
- D-413: orbit (Path) + axial spin ω with I_Q (Point) from well torque; C-319/C-320 not yet in code; magnetic OFF must recover baseline.
- D-414: Field toroidal flow / wake; four-channel illustration.
- D-415: only file in slice that records Point, Path and Field rotations separately and targets a Point–Path–Field transfer ledger.
- D-416: planetary lock matrix; locking is an output; Moon 1:1 without present dipole; Mercury 3:2; Venus, Uranus, Neptune.
- D-417: discrete restoring responses; gravity down-gradient; wake from motion/rotation.
- D-401/D-402/D-403/D-404/D-405/D-406/D-407/D-410/D-411/C-314/C-315/C-316/C-321/C-322/C-324: no Point/Path/Field rotation, magnetism-gravity or locking content (C-322 owns Mirror-Gate no-forced-crossing; D-411 owns route counting).

### (b) Conflicts found
1. D-413 L57-58, L213-225, L282 (and echoed D-412 L138): gravity/curvature-well restoring torque starts axial (point) spin from rest — contradicts "Gravity does not start or affect point rotation" and "a thing does not start point spin on its own".
2. D-413 L198-205: point spin damped by generic −c_ω ω with no magnetic open/closed condition — contradicts open dL/dt = 0 / closed dL/dt = −γL.
3. C-320 L300-323: off-center path-weighted restoring field (reducing to pure gravity g_0 at R=0) → torque → "rotational/orbital evolution" without separating Point rotation from Path rotation — conflicts with gravity not affecting point rotation and the three-rate separation.
4. C-323 L117-129, L166, L18: Mirror-Gate as finite work "across the basin boundary"/"orientation-basin crossing" ≈125 GeV anchor — contradicts C-322 L19-21, L53-55 and C-318 L274-276 (no forced crossing; 125 GeV not a gate threshold). Stale ref "D-415 Hexagonal Lattice Force Dynamics" (C-323 L19).
5. D-414 L21, L32, L52, L62: 125 GeV Higgs as "mirror-gate boundary scale"/anchor; gate "crossing ring" flashing at strain threshold — same contradiction with C-322/C-318.
6. Tension (not hard conflict): D-416 L113, L146 uses a gravitational/tidal baseline as the spin-locking control, implicitly letting gravity torque change spin; canonical rule assigns locking to bound-lattice organization (resistance = mass / organization). D-409 L92 and D-412 L64 lump rotation/circulation into one q variable (three-rate incompleteness). D-410 L112-120 "Mirror-Gate crossing" log terminology predates C-322.

### (c) Cross-references outside the slice that matter for point rotation or magnetism
- G-749 Point Rotation, G-769 Path Rotation (C-325 L16, L24).
- C-306 Torque, C-307 Angular Momentum (C-319, C-320, C-325, D-409, D-413, D-416).
- C-311 Electric-Magnetic Duality (+ Phase 6B: discrete_maxwell_solver_v4.py, faraday_scaling_test.py) (C-319 L166-177).
- A-115 Unified Compression Field; A-109 Inertial Memory; A-105 Restoring Response; A-104 Gradient.
- chapters/09_Transfluxor_Magnetic_Reorganization_and_Point_Rotation.md; Chapter 07 Maxwell-like checks (C-325 L18, L55).
- Builds repo: validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md, REALITY_FIRST_CONTRACT.md (C-325 L19).
- Book1 Ch12 Gravity, Ch13 Electricity/Magnetism (C-320 L194); Book5 Ch1 compression ring (C-323 L109).
- Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/simulate_d413.py, index.html (spin/torque implementation).
- Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/ (Point–Path–Field rotation trace, MATH_GAPS.md, planetary_visual.html).
- solvers/joint_boundary_response.py, JOINT_RESPONSE_DERIVATION.md, BULK_EXCITATION_DERIVATION.md, test_mirror_gate_coupling.py.
- E-505 Coupling, D-401 Flux (lateral to C-319/C-320/D-416); E-531, E-532 (wake / bound flag).
