# Ledger 09a — Books: Android, Book2, Book3, Book4, Book5_Macro, Engineer_The_Future Vol1 Ch01-04

All 22 files in slice 09a read in full. For the three Engineer_The_Future HTML files with embedded PNGs (Ch02/Ch03/Ch04), the base64 payload was elided from view. Every other line was read, including the image captions.

---

## Android — Body & Brain   (`Books/Android/Android_Body_and_Brain.html`)
- Gate / lifecycle: "Proposed Architecture Only", "No Consciousness Claim" (L43-46). Active engineering proposal, not validated (L63).
- Upstream / cites: E-526 (energy balance, gradient transport, L88, L98), E-524 (Kuramoto lattice, L91), C-312 (hierarchy, 3:1 fan-in, L98, L194), G-710 (regulated response, L101, L188, L196), E-527 (relaxation cycle, L101), G-719 (audit that removed the "Five/Six Mind" groundings, L175), A-111 (neighbor-average, corrected, L182, L195), B-213 (ruled out as the communication grounding, L182), G-711 (ruled out as the regulation grounding, L188), E-507 (oscillation scales, L197), D-408 / D-411 / D-412 (triangular/hexagonal movement lattice, L198, L206), G-722 (subconscious movement stack, L202), B-221 (six-step transition, L211), Proposed Android Brain Ch3-4, and the Proposed One-Wave Consciousness book (L65, L202). Downstream: none stated.
- Core claim: bio-inspired control architecture. "No module gets unilateral irreversible control" (L69). Commit rule: "promote Working Ground to Reference Ground only when Gate 5 state report matches Gate 6 acceptance" (L145-147). The hierarchy is "distributed rather than dictatorial" (L161).
- Equations: dU/dt = P_in − P_use − P_loss (L88); J = −D·∇μ (L98); Q_n = k_n·F_n (L101, L188); Δψ_i = ⟨ψ_j⟩ − ψ_i (L182).
- Point / Path / Field role: none stated. "Six directed neighbor routes around one center" is geometry for the movement lattice, not rotation (L206).
- Magnetism / gravity / rotation link: none stated.
- Open / parked: the Move→Hold→Transition reduction of B-221's six steps is only partial (L211). A consciousness test definition does not exist (L165). The Kuramoto order parameter settles and does not cycle unless something depletes (L94).
- Conflicts: none.

## Book 2 — Chapter Status Map   (`Books/Book2/00_CHAPTER_STATUS_MAP.md`)
- Gate / lifecycle: Ch01 "ACTIVE / revised"; Ch02-05 "ACTIVE" (L8-12). The markdown is canonical and PDFs are not authorities (L4).
- Upstream / cites: no node IDs. Lists the 5 chapter files and `Books/figures/`.
- Core claim: an 8-point completion gate for every chapter: Gray control, dimensional equation, symbol definitions, figure, separated One-Wave mapping, predictions, Yellow Audit, raw-data links (L16-25).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: Ch2-5 still need data-backed figures (L29).
- Conflicts: none.

## Book 2 Ch01 — The Cell: Boundary, State, and Signal   (`Books/Book2/Book2_Ch01_The_Cell.md`)
- Gate / lifecycle: "GRAY/GREEN reference + YELLOW One-Wave mapping" (L5).
- Upstream / cites: A-104 Gradient, A-108 Local Stability, A-110 Oscillation, A-111 Recursion, A-112 Persistent Mode (L7, L105-109, L123). Figures: `../figures/book2_cell_six_neighbor.svg`, `../figures/book2_surface_volume.svg`.
- Core claim: "A cell is **not** generally hexagonal" (L15). The hexagon is only an "addressing primitive" (L37). A mapping is strengthened only if it beats the control models (L111).
- Equations: P_circle = 2√(πA); A_hex = (3√3/2)s², P_hex = 6s; du_i/dt = F_i(u_i,t) + D Σ_{j∈N(i)}(u_j − u_i); A = 4πr², V = (4/3)πr³, A/V = 3/r; J = −D∇c; ∂c/∂t = D∇²c; J_m = P_m(c_out − c_in); V_m = V_inside − V_outside; q(t) = 1 if u ≥ u_th, else 0 (L19-97).
- Point / Path / Field role: Field only, in the form of concentration gradients and diffusion. No Point or Path content.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: no calibrated One-Wave cellular parameters (L124). Square/hex/disordered graph controls are still to run (L130).
- Conflicts: none.

## Book 2 Ch02 — Membranes, Gradients, and Transport   (`Books/Book2/Book2_Ch02_Membranes_Gradients_and_Transport.md`)
- Gate / lifecycle: GRAY reference / YELLOW comparison (L5).
- Upstream / cites: A-103 Differential, A-104 Gradient, A-108 Local Stability (L6, L78).
- Core claim: any One-Wave cellular model "has to reproduce these ordinary transport limits" (L32). The mapping "should be rejected if it merely renames D, P_m, or g" (L85).
- Equations: J = −D∇c; ∂c/∂t = −∇·J + R; ∂c/∂t = D∇²c + R; J_m = P_m(c_out − c_in); c_i^{n+1} = c_i^n + λΣ(c_j^n − c_i^n) + Δt R_i^n; d/dt∫c dV = −∮J·dA + ∫R dV; E = (RT/zF) ln([ion]_out/[ion]_in); I = g(V_m − E) (L16-72).
- Point / Path / Field role: Field (gradient, flux). Point and Path: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: no transport coefficient derived from One-Wave primitives (L109). The diffusion benchmark with CSV and plots is still to build (L114).
- Conflicts: none.

## Book 2 Ch03 — Energy, Reaction, and Homeostasis   (`Books/Book2/Book2_Ch03_Energy_Reaction_and_Homeostasis.md`)
- Gate / lifecycle: GRAY / YELLOW (L5).
- Upstream / cites: A-105 Restoring Response, A-108 Local Stability, A-111 Recursion (L6, L86).
- Core claim: living systems "maintain **asymmetric, driven steady states**" (L46). "an internal handoff is not external creation" (L58).
- Equations: dc/dt = S v(c,t); d[A]/dt = −k_f[A] + k_r[B] and its pair; τ dx/dt = −(x − x_*) + u(t); dN_i/dt = ΣF_{j→i} − ΣF_{i→k} + P_i − C_i; ΔG = ΔG° + RT ln Q; ẋ = f(x) + bu − k(x − x_*); δẋ ≈ [f'(x_*) − k]δx + bu (L16-80).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: no universal restoring coefficient (L117).
- Conflicts: none. The internal-handoff cancellation (L56-58) is consistent with conserved bookkeeping.

## Book 2 Ch04 — Signals, Thresholds, and Cellular Memory   (`Books/Book2/Book2_Ch04_Signals_Thresholds_and_Memory.md`)
- Gate / lifecycle: GRAY / YELLOW (L5).
- Upstream / cites: A-109 Inertial Memory, A-110 Oscillation, A-111 Recursion, A-112 Persistent Mode (L6, L115-118).
- Core claim: "Threshold, oscillation, recursion, and persistence are distinct mathematical properties" (L149). A ternary abstraction "must not erase graded biological state" (L150).
- Equations: R(L) = R_max L/(K_d + L); Hill R(L) = R_max Lⁿ/(Kⁿ + Lⁿ); τẋ = −x + u(t), y = g(x); ẋ_i = F_i(x_i,u_i) + ΣW_ij H(x_j − x_i); hard threshold; logistic y = 1/(1 + e^{−k(x−θ)}); hysteresis with θ_on and θ_off, Δθ = θ_on − θ_off; x(t) = A(t)cos φ(t), ω(t) = dφ/dt; x_{n+1} = F(x_n, x_{n−1}, u_n; θ) (L17-123).
- Point / Path / Field role: none stated. Here ω is a signal phase rate, not point rotation (L108).
- Magnetism / gravity / rotation link: none stated. "Inertial memory" (A-109) is used only as persistence language for signals.
- Open / parked: the benchmark notebook for synthetic signal classes is still to build (L154).
- Conflicts: none.

## Book 2 Ch05 — Growth, Division, and Scale   (`Books/Book2/Book2_Ch05_Growth_Division_and_Scale.md`)
- Gate / lifecycle: GRAY / YELLOW (L5).
- Upstream / cites: A-107 Bounded Motion, A-108 Local Stability, A-111 Recursion, B-220 scale hierarchy (L6, L122).
- Core claim: B-220 is "an indexing system until an actual transformation law is derived" (L122). "The scale hierarchy is organizational; it is not itself a biological scaling law" (L161).
- Equations: A = 4πr², V = (4/3)πr³; A→4A, V→8V; A/V = 3/r; dM/dt = μM, M = M_0 e^{μt}; dN/dt = rN(1 − N/K); Q_parent = Q_d1 + Q_d2; x_p → (x_d1, x_d2); ε_x = (x − x_*)/x_*; g = (1/M)dM/dt; t_D ~ L²/D; (1/V)dQ/dt ∝ J A/V; L' = sL; A' = s²A, V' = s³V (L16-137).
- Point / Path / Field role: none stated. The chapter mentions "inertial scales" in passing (L172).
- Magnetism / gravity / rotation link: none stated.
- Open / parked: no universal One-Wave transform across scales (L163).
- Conflicts: none. The geometric scale factor s (L127) is a similarity variable, not a cosmological scale factor.

## Book 3 — Medium: Scope and Status   (`Books/Book3_Medium/00_Scope_and_Status.html`)
- Gate / lifecycle: "This book does not yet exist as chapters" (L29).
- Upstream / cites: B-220 (L25, L38), E-507 (L38), E-521 (L39), A-112 and D-404 (L40), and Book 2 Ch6 (L39; no such file is in Books/Book2, whose status map lists only Ch01-05).
- Core claim: physiology "has essentially no grounding nodes yet" (L33). Appendices define and books apply (L46).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: the gamma(s)/beta(s) problem (L38). Nervous system and organ systems have no nodes (L41-42).
- Conflicts: none against the canonical rules. Internal dangling reference: "Book 2 Ch6" (L39) does not exist in the Book2 status map.

## Book 3 — One Wave Biology (simple)   (`Books/Book3_Medium/Book3_OW_Biology_Simple.md`)
- Gate / lifecycle: "Node B-229. Yellow." (L3).
- Upstream / cites: B-229 (self). Mentions the "silicon cell" and "hex cell" without node IDs.
- Core claim: "membranes (fences), chains (food), packets (ATP), gates (channels), and receipts (copy rules)" (L5). "That body is the net. Nothing is paired in the void." (L14). Nerves: "stay until the lean crosses T, then a spike, then return" (L16).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: "Add a molecule only when you can point at it" (L18).
- Conflicts: none.

## Book 4 — Large: Scope and Status   (`Books/Book4_Large/00_Scope_and_Status.html`)
- Gate / lifecycle: "This book does not yet exist as chapters" (L29).
- Upstream / cites: B-220 (L25, L38), G-715 (L33, L39-40), A-112 (L38).
- Core claim: Book 4 is planetary and solar-system scale, and that assignment is "an inference from the size ladder" (L25). It "leans almost entirely on G-715" (L33).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "Magnetic Switchbacks as Mirror Events — G-715 (subfunction)" (L40). Orbital Dynamics: "none — No supporting nodes exist at all" (L42).
- Open / parked: planetary formation and orbital dynamics have no nodes (L41-42).
- Conflicts: **stale and contradicted**. L42 says no nodes exist for orbital dynamics. Books/Book5_Macro/NODE_SUPPLY_No_Expansion.md L11-13 cites D-413 (orbital motion on a source wake) and D-416 (lock: Moon 1:1, Mercury 3:2), and the canonical rules include bound-lattice locking. The scope page predates or ignores these.

## Book 5 Ch1 — Galaxies and the Extended Compression Effect / Dark-Matter Comparison   (`Books/Book5_Macro/Book5_Ch1_Galaxies_and_Dark_Matter.md`)
- Gate / lifecycle: "YELLOW (field equations) / GREEN (galaxy identification and coefficient fit)" (L13). Draft v1.0, Class B (L5-7).
- Upstream / cites: A-115 Unified Compression Field, E-507, A-104, A-105, C-309, Book 1 Ch12 Gravity, Book 1 Ch15 Higgs/Mirror Resonance (L10-12); B-220 (L111, L179); I-09, a dead address replaced by A-115 (L127); C-318, the mass-mechanism removal (L174, L187).
- Core claim: "a galaxy is a large vortex moving through the field" (L40). The Extended Compression Effect is "the field's own displaced response to the galaxy's motion and rotation" (L51-53). "No new particle is required. The ring is a field response, not a substance" (L83).
- Equations: R_ring ~ R_gravity at galactic scale, versus R_ring << R_gravity at micro scale (L70-72, L102-106); R_total = R_gravity + R_ring; R_ring ~ K_p·|∇ψ_ring|²·Area (L97-99); v(r)²/r = R_gravity(r)/m + R_ring(r)/m (L116); v_c(r)²/r = |g_local(r) + g_wake(r)| (L138); ρ_DM,eff = −(1/(4πG_eff)) div(g_wake) (L144).
- Point / Path / Field role:
  - Path: stars "riding inside one larger rotational pattern" (L59-60), and the orbital speed v(r).
  - Field: the wake/compression ring, g_wake (L42-45, L138).
  - Point: none stated. No galaxy L or body spin is separated out, so the Point/Path/Field split is incomplete.
- Magnetism / gravity / rotation link: the extra gravity comes from the field wake of the galaxy's "bulk motion and rotation" (L78-80). "gravity = local directional response of the compression field; dark matter = extended/wake contribution; Higgs-like resistance = local boundary stiffness" (L130-132). No magnetism.
- Open / parked:
  - g_wake(r) is not derived (L147).
  - The micro-to-galactic transition depends on gamma(s)/beta(s) (L108-112, L177-179).
  - The A-115/C-318 shared source mapping is open (L174, L187).
  - Spiral arms and lensing are not attempted (L85-89, L180-181).
- Conflicts:
  - (a) Status says "GREEN (galaxy identification and coefficient fit)" (L13), yet the Yellow Audit says "no fit to actual rotation curve data" (L176). This is an internal gate contradiction.
  - (b) Rotation sources gravity directly. L51-53 and L78-80 attribute a gravity contribution to the galaxy's rotation through a wake, with R_ring ~ R_gravity asserted. The canonical rule is that rotation enters gravity only through K_L = I + κ_R R, with κ_R not set. This chapter effectively asserts a large, unset rotation coupling and does not route it through grad chi / K_L. It also does not separate Point, Path, and Field rotation. Tension, not a formula clash.
  - (c) "Higgs-like resistance = local boundary stiffness" (L132) differs in wording from the canonical "resistance = mass / organization". Flag only.

## Book 5 Ch2 — Stars: Sustained Persistent Modes Under Compression   (`Books/Book5_Macro/Book5_Ch2_Stars.md`)
- Gate / lifecycle: YELLOW / YELLOW (L12).
- Upstream / cites: A-112, A-104, A-105, G-715, C-309 (L10-11, L130); Book 1 Ch7 (photon definition, L81, L121); "Ch8" (L83); B-220 and E-507 (L150).
- Core claim: "a star is a sustained, high-amplitude Persistent Mode (A-112) held in place by its own gradient field" (L37-38). "The star is not 'fighting gravity' — it is a stable recursive pattern" (L65-66). The photosphere is a boundary gate, and the corona is the release zone (L69-74).
- Equations: ||ψ_{n+k} − ψ_n|| < ε (L91); R_OW = −A(∇ψ) (L94); dE_cor/dt = P_release − P_loss, with P_release ≈ P_loss for a stable corona (L99-101); c = v_max (C-309).
- Point / Path / Field role:
  - Field: compression and gradient, and boundary release.
  - Point: none stated. Stellar spin is not addressed.
  - Path: none stated.
- Magnetism / gravity / rotation link: "Stored magnetic/pressure tension converts into outward wave release ABOVE that boundary" (L72-74). Gravity is reframed as a restoring-response balance (L62-66). No rotation.
- Open / parked: fusion has no One-Wave account (L135-136). G-715 is unsimulated (L133). Main-sequence lifetime and the mass-luminosity relation are untreated (L138-139). The link between stellar mass and ε or gamma(s)/beta(s) is open (L148-150).
- Conflicts: none against the canonical rules. Internal: the photon definition is cited as Book 1 Ch7 (L81) and as "Ch8" (L83).

## Book 5 Ch3 — Supernovae: Break Condition at Stellar Scale   (`Books/Book5_Macro/Book5_Ch3_Supernovae.md`)
- Gate / lifecycle: YELLOW / YELLOW. It explicitly does not use standard nucleosynthesis as its mechanism (L12-14).
- Upstream / cites: B-207, B-208, B-209, Book 5 Ch2, A-112, E-522 (L10-11); A-105 (L47, L67); B-213 Access Line (L77, L110); B-220 and E-507 (L142).
- Core claim: a supernova is "a star's Persistent Mode crossing its own Break Condition (B-209)" (L40-41). The B-208 outcomes map onto supernova phenomenology: Separation, Recursive collapse, Access Line, Reset (L69-84).
- Equations: |M_i| > R_i (L62, L103). B-208 bands: 45-30 is Break Risk, 30-15 is Break Condition (L106-108).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated. Core collapse is treated as Persistent Mode failure.
- Open / parked: the Access-Line-as-remnant match is unverified against B-213 (L143-144). Stellar-scale bands depend on gamma(s)/beta(s) (L138-142). No nucleosynthesis account (L145).
- Conflicts: none.

## Book 5 Ch4 — Black Holes, Quasars, and White Energy / Cosmic Mirror Gate   (`Books/Book5_Macro/Book5_Ch4_Black_Holes_and_Quasars.md`)
- Gate / lifecycle: "YELLOW (structure, real math inherited) / YELLOW (cosmological application unverified)" (L13).
- Upstream / cites: A-115, C-301 Mirror Gate, C-309, B-209, A-112a Traveling Lattice Rupture, Book 5 Ch3, E-522 (L10-12); C-318 (L61); C-308 spin-half (L67); E-528 (L84, L92, L245, L265); B-213 (implied by Ch3); E-529 (L257); E-530 (L205, L251, L265).
- Core claim:
  - "a black hole is a tear in the lattice — a region where the Friction Limit (C-309) itself breaks down" (L51-53). The chapter explicitly says this "has no connection to the Mass-Effect mechanism in C-318" (L60-62).
  - "Light does not enter a black hole" (L89), but matter and field energy do (L95-97).
  - A quasar jet is the M⁴ = I closure (L107-111).
  - "One-Wave rejects expansion of space" (L201). "No Hubble parameter, scale factor, or negative-pressure equation belongs in the One-Wave model" (L239).
- Equations:
  - M = [[0,1],[−1,0]], M² = −I, M⁴ = I; M(ψ_C, ψ_E) → (ψ_E, −ψ_C) (L102, L129).
  - c = v_max = √β_max Δx/Δt (L132).
  - r_i^{n+1} = r_i^n − ν(r_i^n − r_{i−1}^n), ν = vΔt/Δx, 0 ≤ ν ≤ 1; R_{n+1} = R_n; O_i^n = [r_i^{n+1} − r_i^n]_+, C_i^n = [r_i^n − r_i^{n+1}]_+, ΣO = ΣC (L155-176).
  - d_i^{n+1} = clip(d_i^n + κ_d[r_i^n − r_damage]_+(1 − d_i^n) − λ_d d_i^n, 0, 1) (L185-187).
  - dU_C/dt = P_cap + P_ν − λ_C U_C − D_Wh U_C; P_W = D_Wh U_C; switching with U_on > U_off (L207-215).
  - dE_W/dt = P_W − P_{W→χ} − Φ_{W,∂Ω}; E_tot = E_γ + E_χ + E_ν + E_C + E_W with dE_tot/dt = 0; ⟨P_W⟩ = ⟨P_cap + P_ν − λ_C U_C⟩ (L219-237).
  - 1 + z = exp(∫κ_γ dℓ); dE_γ/dℓ = −κ_γ E_γ; Q_{γ→χ} = c_L κ_γ u_γ (L248, L255-256).
- Point / Path / Field role:
  - Field: tear, compression reservoir, reinjection.
  - Path: light bends around the hole (L91-92).
  - Point: none stated. The Mirror "symplectic rotation" (L66-67) is a state-space operator, not point spin L. Black-hole spin and accretion-disk L are not addressed.
- Magnetism / gravity / rotation link: lensing is mentioned (L91-92). No magnetism. Rotation appears only as the Mirror operator.
- Open / parked:
  - The black hole vs. extreme compression distinction is not made precise (L139-141).
  - ν is not derived (L178-179).
  - The tired-light coefficient and neutrino deposition are not derived (L271-272).
  - The static balance is unsimulated (L273).
- Conflicts:
  - None against the canonical rules. The chapter is consistent with the no-expansion, E-528 and E-530 rules.
  - Internal gate contradiction: L13 says the cosmological application is "YELLOW … unverified", but L270 says "The quasar/white-hole identification remains Green".

## Book 5 Ch5 — Stellar Nucleosynthesis: Sequential Complexity Through Threshold Crossings   (`Books/Book5_Macro/Book5_Ch5_Stellar_Nucleosynthesis.md`)
- Gate / lifecycle: YELLOW / YELLOW (L12).
- Upstream / cites: Book 1 Ch6 (The Nucleus), Book 5 Ch2, Ch3, B-207, B-208, D-405 (L10-11); "Ch7" binding-energy account (L16, L48, L95, L176); A-112 (L59); B-210 Return (L72); B-209 (L74); E-03/E-503 and E-04/E-505 (L99-100); D-05/D-405 (L101).
- Core claim: nucleosynthesis is a sequence of B-207 threshold crossings that resolve as Returns (B-210). Core collapse is the one Break (B-209). Elements heavier than iron come from the Break's Reset (L70-89). "The star does not break; it steps" (L68).
- Equations: binding peak at iron-56 is the surface/volume minimum (L98-100); 2πR_shell = nλ_nuclear (L101-102); P_core(t) crossing a stage threshold T_n (L106-108, candidate).
- Point / Path / Field role: Field (compression). Point and Path: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: the availability condition for a new harmonic shell is asserted, not derived (L139-141). T_n is not derived (L142-145). No quantitative temperature link (L150-152).
- Conflicts: none against the canonical rules. Internal: the dependency is listed as "Book 1 Ch6 (The Nucleus)" (L10), but the body consistently cites "Ch7" (L16, L48, L95).

## Book 5 Ch6 — Time as Transport Through the Medium   (`Books/Book5_Macro/Book5_Ch6_Time_as_Transport_Through_the_Medium.md`)
- Gate / lifecycle: "YELLOW — One-Wave mechanism hypothesis; relativistic recovery and cosmology validation incomplete" (L3).
- Upstream / cites: C-309, E-509, E-533 (L23); E-528 (L123); A-114 (L157, L168); Book1 Ch16a wave equation (L167); `Nodes/E-533_Superfluid_Transport_Time_Dilation.md` (L186, L188); `solvers/TIME_RESISTANCE_PROBE.md` (L186).
- Core claim: "local evolution decreases as transport approaches the ceiling" (L27). The square-root law must be derived, not borrowed (L61). One frozen medium law must give both z and Δt_obs (L131-141).
- Equations: ρ_v = v²/c²; ρ_local = 1 − ρ_v; dτ/dt = √(1 − v²/c²); dt = dτ/√(1 − v²/c²); Ξ = Ξ(χ, ∇χ, γ, β, …); dτ/dt = 𝒯(v, Ξ), 𝒯(0,0) = 1, 𝒯(v,0) = √(1 − v²/c²), ∂𝒯/∂Ξ < 0; 1 + z = exp[∫κ_γ dℓ]; the map {χ, ∇χ, γ, β} → {κ_γ, 𝒯} → {z, Δt_obs} (L33-141).
- Point / Path / Field role:
  - Path: transport through the medium, v (L19-27).
  - Field: χ and ∇χ medium difficulty (L87-88).
  - Point: none stated. "Internal evolution" is a clock rate, not spin.
- Magnetism / gravity / rotation link: gravitational timing "could enter" through Ξ(χ, ∇χ) but "is not yet derived" (L119). No magnetism or rotation.
- Open / parked:
  - Derive the square root from the A-114 roots and an update-budget norm (L177-182).
  - The E-533 probe passes its five controls, but damping alone does not derive Lorentz slowing (L186).
  - A self-held periodic excitation test is still needed (L186).
- Conflicts: none. The chapter is consistent with no expansion and E-528.

## Book 5 draft — test-ready, not solved   (`Books/Book5_Macro/DRAFT_TEST_READY_NO_EXPANSION.md`)
- Gate / lifecycle: "Gate: BROWN. Not a replacement for Book 5 chapters. No scale factor." (L3).
- Upstream / cites: E-528, A-115, E-530, D-413 (L7-11); data GW150914-v3 and CMS record 24446 (L15); "Chapter 2 radii" (L15).
- Core claim: "Redshift is path loss in a static field" (L7). "E-530 is reinjection, not a negative-pressure fluid. D-413 is orbital restoring. Away-motion is an arc until a sign flip is seen." (L11). "Orbit: the same path must change sign. One-way red fails D-413." (L21).
- Equations: 1 + z = exp ∫κ (L9); κ = ln(1.09)/440 = 1.96e-4 per Mpc (L19); R+/R− = 0.872, λ = 5.284 fm, area = 8.886 fm² (L23).
- Point / Path / Field role:
  - Path: orbital arc, with sign flip (L11, L21).
  - Field: A-115 field.
  - Point: none stated.
- Magnetism / gravity / rotation link: D-413 orbital restoring (L11). "Strain is a Z_M stamp. It does not set a radius." (L25).
- Open / parked: A1-A3 (three phases, 120°, gap on boundary) and B1-B3 (constituents, confinement, gluon-field gap) (L29).
- Conflicts: none.

## Node supply — Book 5, no expansion   (`Books/Book5_Macro/NODE_SUPPLY_No_Expansion.md`)
- Gate / lifecycle: supply note, "Not a replacement for Ch1 or Ch4" (L3).
- Upstream / cites: E-528, E-530, A-115, D-413, D-416 (L3).
- Core claim:
  - "no expansion of space. No scale factor. No Hubble term. Redshift is path loss" (L5).
  - "D-413: orbital motion on a source wake. The current lab well is imposed. It is not derived gravity." (L11).
  - "D-416: lock is an output. Moon 1:1. Mercury 3:2. A lunar dipole is not required. Parent organization sets the rate. Mass is resistance, the delay, not a second clock. A second ratio needs a second stable step." (L13).
- Equations: dE/dl = −κE; 1 + z = exp ∫κ (L7).
- Point / Path / Field role:
  - Point: the rate is locked to the parent, and mass is resistance (L13).
  - Path: orbit on the source wake (L11).
  - Field: the wake (L11).
- Magnetism / gravity / rotation link: no lunar dipole is required for lock (L13). The D-413 well "is not derived gravity" (L11).
- Open / parked: a second ratio needs a second stable step (L13).
- Conflicts: none of substance. It is consistent with the bound-lattice rule (Moon 1:1, Mercury 3:2, no lunar dipole). Wording note: "Mass is resistance" (L13) versus the canonical "resistance = mass / organization". It is compatible if read as mass being the resistance term with parent organization as the divisor, but the short form omits the organization divisor. It also does not state "magnetic channel off must still leave the face".

## Engineer the Future Vol I Ch 1 — The Wave Reader   (`Books/Engineer_The_Future/Vol1/Ch01_The_Wave_Reader.html`)
- Gate / lifecycle: speculative instrumentation. Yellow: "No such residual has been sought yet" (L81).
- Upstream / cites: C-315 (footer, L101); "Logic Anchor" = Persistent Mode (L77); next chapter, Ch II (L98).
- Core claim: a deep differential null may show a "distortion tail … correlating with the nearby mass or charge" (L77).
- Equations: none. Specs: CMRR ~120 dB, phase match < 0.08°, 24-bit ADC (L88-91).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated beyond a residual near "mass or charge" (L77).
- Open / parked: the whole hunt is unrun (L81, L95).
- Conflicts: none.

## Engineer the Future Vol I Ch 2 — The Hierarchical Sensor-Control   (`Books/Engineer_The_Future/Vol1/Ch02_Hierarchical_Sensor_Control.html`)
- Gate / lifecycle: Yellow Audit (L59-62). One embedded PNG (base64 elided), captioned "Signal count compressing 3:1 at each level" (L54).
- Upstream / cites: no node ID in the file. The same architecture is grounded in C-312 by the Android book.
- Core claim: four levels with 3:1 fan-in. The coordinator "samples at half the base signaling frequency" (L41, L50). "The Correction Is Targeted, Not Broadcast" (L56-57).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: no position encoding, latency undefined, level count untested (L61).
- Conflicts: none.

## Engineer the Future Vol I Ch 3 — Pressure Reversal   (`Books/Engineer_The_Future/Vol1/Ch03_Pressure_Reversal.html`)
- Gate / lifecycle: red caveat: "No simulation has been run … candidate relation only, explicitly not locked" (L40-43). One embedded PNG (elided), captioned "no simulation has run yet to produce an actual number" (L50).
- Upstream / cites: an unnamed "source node" (L42). No node ID.
- Core claim: "some gates do not crush what enters them. They reverse it" (L38). The positron is "the pressure of a proton's interior finding release rather than mirror-matter intrusion" (L59).
- Equations: layers 24 → 12 → 6 → 3 → 1(0)1 with pressure 1x, 2x, 4x, 8x, 16x (L47-48); R = (entity_state + environmental_factors)/(2·pressure_at_layer), where R > 0.5 means the entity crosses and R ≤ 0.5 means it breaks (L53-56).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: everything is unsimulated.
- Conflicts: none against the canonical rules. Traceability gap: the source node is not named.

## Engineer the Future Vol I Ch 4 — Stellar Boundary Reversal   (`Books/Engineer_The_Future/Vol1/Ch04_Stellar_Boundary_Reversal.html`)
- Gate / lifecycle: Yellow (L58-61). One embedded PNG (elided): "The real observed reversal (red) against the naive gradient expectation (gray)" (L46).
- Upstream / cites: no node ID in the file. The content is G-715, per Book4 scope and Book5 Ch2.
- Core claim: "the photosphere is a hold boundary, not the end of heat's expression" (L47). Switchbacks are a "mirror operation … the outward field briefly folding to carry its own opposite within it" (L56).
- Equations: none. Chain: interior compression → surface hold → magnetic/wave tension → fold or reconnection → outer plasma release → coronal heating → solar wind (L50-52).
- Point / Path / Field role: Field (magnetic and wave tension, release). Point and Path: none stated.
- Magnetism / gravity / rotation link: stored magnetic tension is released above the boundary, and magnetic switchbacks are mirror events (L47, L56). No rotation or gravity link.
- Open / parked: no simulation shows T_corona > T_surface. The hold→release conversion rule is not derived (L60).
- Conflicts: none.

---

## Slice summary

### (a) Nodes and chapters bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization, or locking
- **D-416** (NODE_SUPPLY_No_Expansion L13): lock is an output. Moon 1:1, Mercury 3:2, no lunar dipole, parent organization sets the rate, mass is resistance (delay). This is the bound-lattice Point-rate rule.
- **D-413** (NODE_SUPPLY L11; DRAFT_TEST_READY L11, L21): orbital motion on a source wake (Path on Field). The lab well is imposed, not derived gravity. An orbit must show a sign flip.
- **A-115** (Book5 Ch1 L10, L125-147; Ch4 L10; DRAFT L11; NODE_SUPPLY L3):
  - gravity = local directional response of the compression field;
  - dark matter = wake;
  - Higgs-like resistance = boundary stiffness.
- **Book5 Ch1 Extended Compression Effect**: gravity contribution from galaxy rotation and motion via the wake (Field). Stars ride a rotational pattern (Path). Point is absent.
- **C-318** (Book5 Ch1 L174; Ch4 L61): mass-mechanism bridge. The transport-to-mass shortcut is removed. The A-115/C-318 mapping to the Mass-Effect tensor and the far-field source amplitude is open.
- **C-309 / E-509** (Ch2, Ch4, Ch6): propagation ceiling c = v_max = √β_max Δx/Δt.
- **E-533** (Ch6): proper-time slowing from transport. Ξ(χ, ∇χ) is the slot for gravitational timing (Path/Field), not derived.
- **E-528 / E-529 / E-530** (Ch4, Ch6, DRAFT, NODE_SUPPLY): static redshift as path loss, Return Mode, reinjection (White Energy). No expansion.
- **C-301 Mirror Gate / C-308 spin-half** (Ch4 L64-68, L101-111): the M operator is a "symplectic rotation" of state, not point L.
- **A-112a** (Ch4 L148-193): conservative traveling-tear transport, with scar variable d_i (lattice organization).
- **G-715** (Book5 Ch2; Book4 scope; ETF Ch4): stellar boundary reversal. Stored magnetic tension is released above the photosphere. Switchbacks are mirror events (magnetism).
- **A-105 / A-112** (Book5 Ch2, Ch3, Ch5): stars as Persistent Modes in restoring balance, "not fighting gravity" (gravity reframed).
- **B-207 / B-208 / B-209 / B-210 / B-213** (Book5 Ch3, Ch5): threshold, break, return, and access-line crossings at stellar scale (organization failure and locking of new configurations).
- **B-220 / E-507 / E-522** (Book5 Ch1-3, Book2 Ch5, Book3/4 scope): scale ladder. The gamma(s)/beta(s) scaling is open and blocks galactic gravity.
- **A-109 Inertial Memory** (Book2 Ch4): "inertial" only in the signal-persistence sense. No mechanical inertia.
- **D-408 / D-411 / D-412** (Android): hex movement lattice geometry. Not rotation.
- **Book 4 scope** (L40, L42): magnetic switchbacks via G-715. It claims no orbital-dynamics nodes.

### (b) All conflicts found
1. **Book4 scope L42** says Orbital Dynamics has "No supporting nodes exist at all". This is stale and contradicted by D-413 and D-416 (NODE_SUPPLY_No_Expansion L11-13) and by the canonical bound-lattice locking rule.
2. **Book5 Ch1 L51-53, L78-80, L104-106**:
   - It attributes a gravity contribution (R_ring ~ R_gravity) to the galaxy's rotation and bulk motion. The canonical rule routes rotation into gravity only through K_L = I + κ_R R, with κ_R not set. The chapter's assertion is not routed through grad chi / K_L.
   - It does not separate Point, Path, and Field rotation (no Point/L term), so the node is incomplete by the three-rate rule.
3. **Book5 Ch1 L13 vs L176**: "GREEN (… coefficient fit)" versus "no fit to actual rotation curve data". Internal gate contradiction.
4. **Book5 Ch4 L13 vs L270**: "YELLOW (cosmological application unverified)" versus "quasar/white-hole identification remains Green". Internal gate contradiction.
5. **Wording only, flagged**:
   - Book5 Ch1 L132 "Higgs-like resistance = local boundary stiffness" and NODE_SUPPLY L13 "Mass is resistance" both differ from the canonical "resistance = mass / organization".
   - NODE_SUPPLY omits "magnetic channel off must still leave the face". It is not contradicted.
6. **Internal reference inconsistencies, not canonical-rule conflicts**:
   - Book5 Ch2 L81 vs L83: photon in Book1 Ch7 vs Ch8.
   - Book5 Ch5 L10 vs L16/L48/L95: Book1 Ch6 vs Ch7 for the nucleus/binding account.
   - Book3 scope L39 cites a nonexistent "Book 2 Ch6".
   - ETF Ch3 cites an unnamed "source node".

No file in the slice contradicts the following: no expansion / E-528 / E-530; C-306/C-307 L bookkeeping (no file touches L); magnetism opening the point; or parent/child transport.

### (c) Cross-references outside the slice that matter for point rotation or magnetism
- D-413, D-416 (lock, Moon 1:1, Mercury 3:2, no lunar dipole, mass as resistance)
- A-115 (compression field, gravity baseline), C-318 (mass mechanism)
- G-715 (stellar boundary reversal, magnetic tension, switchbacks)
- C-301 Mirror Gate, C-308 spin-half (the "symplectic rotation" is not point L)
- A-112a Traveling Lattice Rupture
- E-528, E-529, E-530 (redshift and reinjection loop), E-533 and `Nodes/E-533_Superfluid_Transport_Time_Dilation.md`, `solvers/TIME_RESISTANCE_PROBE.md`
- C-309, E-509, A-114 (propagation ceiling and dispersion)
- Book 1 Ch12 Gravity, Book 1 Ch15 Higgs/Mirror Resonance, Book 1 Ch16a wave equation
- B-220, E-507, E-522 (gamma(s)/beta(s) scale law)
- C-312 (fan-in hierarchy), G-722 (movement stack)
