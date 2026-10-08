# Ledger 05 — Nodes F-601..F-608, G-701..G-725

All 40 slice files read in full (largest: G-715 636 lines, G-716a 502, G-721a 451, G-716 446). Paths relative to /home/user/One-Wave-Science.

## F-601 — Influence   (`Nodes/F-601_Influence.md`)
- Gate / lifecycle: GREEN / ACTIVE; classification Interaction Operators.
- Upstream: A-112 Persistent Mode. Downstream / cites: F-602..F-608; repair note cites A-112, E-508 (L46-48).
- Core claim: "Influence means a change in one bounded state produces a change in another." (L19); "Influence = nonzero alpha in the state-to-state dependence function." (L33)
- Equations: psi_2 = f(psi_1); alpha = f'(psi_1); delta_psi_2 = alpha * delta_psi_1 (L26-28).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: f and alpha not derived; symmetry alpha_12 vs alpha_21 not specified; local vs nonlocal range not specified (L39-41). F-609 Amplification / F-610 Persistence removed as nonexistent (L48).
- Conflicts: none.

## F-602 — Interaction Differential   (`Nodes/F-602_Interaction_Differential.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: F-601, A-103 Differential. Downstream / cites: F-603, F-604, F-605.
- Core claim: "Interaction Differential measures the imbalance between two interacting states." (L23); specialization of A-103, "Does not redefine A-103" (L18-20).
- Equations: D_psi = psi_1 - psi_2 (L26, L31).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: scalar only, vector differential deferred (L40); whether D_psi is the only relevant differential unresolved (L41).
- Conflicts: none.

## F-603 — Transfer   (`Nodes/F-603_Transfer.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: F-602. Downstream / cites: F-604, F-605, F-608.
- Core claim: "Transfer means reciprocal redistribution of a bounded quantity between states. The total quantity is conserved." (L19-20)
- Equations: Q_total = Q_1 + Q_2 = constant; dQ_1/dt = -dQ_2/dt; DeltaQ_1 + DeltaQ_2 = 0 (L25-29).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (Q not fixed: "amplitude, energy, phase, or other quantity", L39 — angular momentum not named).
- Open / parked / not-set items: transfer law beyond ideal closure; meaning of Q; whether closure holds in lattice; transfer rate (L38-41).
- Conflicts: none against canonical rules. Internal: operational chain L35 still lists "Amplification" as downstream although the L46-48 repair note says F-609 Amplification does not exist.

## F-604 — Resonance   (`Nodes/F-604_Resonance.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: F-603, F-602. Downstream / cites: F-606, F-607; CCD-04.
- Core claim: "Resonance means aligned-choice reinforcement." (L19); firewall: "It does not import quantum superposition ontology." (L39)
- Equations: A_T = A_1 + A_2; A_T > A_1; A_T > A_2 (L28-32).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: why aligned vs opposed resolution occurs deferred to CCD-04 (L41, L47-48); resonance conditions between mode types uncharacterized (L49).
- Conflicts: none against canonical rules. Internal: L44 operational chain still points to "Amplification" despite L54-56 repair note.

## F-605 — Interference   (`Nodes/F-605_Interference.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: F-603, F-602. Downstream / cites: F-606, F-607, F-608; CCD-04.
- Core claim: "Interference means phase-dependent combination that can reinforce, reduce, or cancel." (L19)
- Equations: psi_1 = A cos(omega t); psi_2 = A cos(omega t + phi); psi_T = 2A cos(phi/2) cos(omega t + phi/2); A_eff = 2A |cos(phi/2)| (L25-37).
- Point / Path / Field role: none stated. (omega here is oscillation angular frequency, not point spin.)
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: what sets phi (CCD-04); fixed vs evolving phi; exactness of phi=pi cancellation in lattice (L50-52).
- Conflicts: none.

## F-606 — Reflection   (`Nodes/F-606_Reflection.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: F-604, F-605. Downstream / cites: F-608.
- Core claim: "Reflection is the rejection and return of an incoming state at a boundary." (L19)
- Equations: A_i = A_r + A_t; r = A_r / A_i, 0 <= r <= 1; A_r = r A_i (L26-37).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: what determines r; dependence on frequency/angle/boundary/lattice; relation of r to coupling beta_i (L43-45).
- Conflicts: none.

## F-607 — Transmission   (`Nodes/F-607_Transmission.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: F-606. Downstream / cites: blank (L16).
- Core claim: "Transmission is the acceptance and passage of an incoming state through a boundary." (L19)
- Equations: t = A_t / A_i = 1 - r; r + t = 1; A_t = (1 - r) A_i (L29-35).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: closure exactness in lattice; frequency-dependent transmission (L41-43).
- Conflicts: none against canonical rules. Internal: L38 chain still lists "Amplification / Persistence" despite L48-50 repair note.

## F-608 — Attenuation   (`Nodes/F-608_Attenuation.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: F-603, F-605, F-606. Downstream / cites: blank.
- Core claim: "Attenuation is the progressive weakening of state strength as it propagates or interacts." (L19-20); "Proportional decay is an assumption, not a derived result." (L40)
- Equations: dA/dx = -mu A, mu > 0; A(x) = A_0 exp(-mu x) (L26-29).
- Point / Path / Field role: Path-adjacent only — loss along propagation distance; mu depends on "Lattice resistance gamma", "Coupling strength beta", "Mode frequency" (L34-37). No Point/L statement.
- Magnetism / gravity / rotation link: none stated. Note: same symbol gamma as the canonical closed-gradient damping dL/dt = -gamma L; the file does not link them.
- Open / parked / not-set items: proportional decay unverified; mu not derived from gamma, beta; frequency dependence; non-exponential forms not ruled out (L47-50).
- Conflicts: none. (Relevant to E-528 path loss but does not cite it.)

## G-701 — Evaluation Differential   (`Nodes/G-701_Evaluation_Differential.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: A-103, B-206 Paired Loop. Downstream / cites: G-702; B-207.
- Core claim: "Differential measures difference. Differential does not determine action." (L28)
- Equations: Delta_n = R_n - I_n (L26, L31).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: scalar vs vector; single differential completeness; link to Threshold T (B-207) (L40-42).
- Conflicts: none.

## G-702 — Evaluation   (`Nodes/G-702_Evaluation.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-701. Downstream / cites: G-703, G-704, B-207, G-708, G-710, G-711, G-712; B-208.
- Core claim: "Evaluation does not act. It assesses." (L23); "Root Rule: Void Evaluates." (L25)
- Equations: E_n = E(Delta_n) (L27); candidate E_n = E(Delta_n, T_n, context) (L33).
- Point / Path / Field role: none stated (Void role assignment only).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: mechanism not derived; noise vs signal; significance threshold; binary vs graded; link to B-208 (L50-55).
- Conflicts: none.

## G-703 — Modulation   (`Nodes/G-703_Modulation.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-702, B-207, B-216, B-206b, B-206c. Downstream / cites: G-705, B-210, B-209, G-708, G-710, G-713; B-225, G-720.
- Core claim: "Modulation converts an evaluation signal into a bounded change of activation, polarity, integrity support, or access state." (L20); "Root Rule: Field Modulates." (L22); control operators (Hold/Increase/Decrease/Redirect/Stabilize/Reject/Admit) are not the canonical Four Actions (L36-58).
- Equations: M_n = M(E_n, Theta_n, Theta*_n, available_control_operators); Theta_n = (q_n,a_n,p_n) (L25, L31); five bands -2 -1 0 +1 +2 (L65).
- Point / Path / Field role: none stated (Field role = modulation, a control label, not field curl).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: scale-specific actuation limits need calibration; concurrency of operators (L78-79).
- Conflicts: none.

## G-704 — Kabeuchi   (`Nodes/G-704_Kabeuchi.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-701, G-702, G-703. Downstream / cites: G-705.
- Core claim: "Kabeuchi is constructive differential review." (L19); "Kabeuchi is not a separate agent." (L26)
- Equations: Delta_n -> E(Delta_n) -> M(E(Delta_n)) (L24); I_{n+1} = I_n + alpha * M_n (L38).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: constructive intent not formalized; distinction from passive reaction not specified (L44-46).
- Conflicts: none.

## G-705 — Correction   (`Nodes/G-705_Correction.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-703, G-704. Downstream / cites: G-706, G-707; A-109, A-111.
- Core claim: "Correction is the application of the modulation signal to update the current state." (L19); update-rule term beta_i(<psi_j> - psi_i) is "the automatic correction term" (L39).
- Equations: I_{n+1} = I_n + alpha * M(E(Delta_n)), 0 < alpha < 1 (L22-24).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: alpha unspecified; fixed vs adaptive; overcorrection instability not analyzed (L46-49).
- Conflicts: none.

## G-706 — Validation   (`Nodes/G-706_Validation.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: G-705, G-701. Downstream / cites: G-707, G-708, G-709, G-711.
- Core claim: "Validation is not absolute proof. It is confirmation through participation." (L21)
- Equations: F_n = 0 => V_n = 0; F_n != 0 => V_n = V(F_n) (L30-33).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: sufficient feedback; binary vs graded; link to B-208 (L39-41).
- Conflicts: none.

## G-707 — Persistence A   (`Nodes/G-707_Persistence_A.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: G-705, G-706. Downstream / cites: G-708, G-709; E-505.
- Core claim: "Persistence A is mathematical convergence of the correction cycle." (L19); "This is purely mathematical. It does not by itself prove successful balance." (L38)
- Equations: lim |I_{n+1} - I_n| -> 0; |I_{n+1} - I_n| = |alpha M_n|; R_n -> I_n => Delta_n -> 0 => E_n -> 0 => M_n -> 0 (L22-36).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: rate; monotonic vs oscillatory; relation to E-505 stability (L45-47).
- Conflicts: none.

## G-708 — Persistence B   (`Nodes/G-708_Persistence_B.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-707, G-702, G-703. Downstream / cites: G-709.
- Core claim: "Convergence alone does not prove balance." (L22); requires convergence + valid evaluation + valid modulation (L34-39).
- Equations: lim |I_{n+1} - I_n| -> 0 => successful balance (L31).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: balance vs stagnation; local vs global detectability (L46-48).
- Conflicts: none.

## G-709 — Regulated-Response Balance   (`Nodes/G-709_Balance.md`)
- Gate / lifecycle: GREEN / ACTIVE ("Definition is GREEN; promotion to YELLOW depends on upstream audit completion").
- Upstream: G-708, G-706. Downstream / cites: G-710, Books; disambiguated from B-201 Equilibrium Balance ("Do not merge them", L16).
- Core claim: "Balance is regulated response under feedback." (L23)
- Equations: Q_n = k_n F_n, 0 <= k_n <= k_max (L30); balanced: 0 < k_n <= k_max (L42).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: k_n, k_max not derived; fixed vs adaptive; relation to alpha (L51-53); YELLOW promotion blocked on G-702/G-703 audits (L48).
- Conflicts: none.

## G-710 — Grow The Fuck Up Gate   (`Nodes/G-710_Grow_The_Fuck_Up_Gate.md`)
- Gate / lifecycle: GREEN / ACTIVE (definition level).
- Upstream: G-709, G-702, G-703. Downstream / cites: G-711, Books, G-718, G-719, G-720.
- Core claim: "the transition from unregulated reaction to regulated response" (L19).
- Equations: unregulated Q_n = g F_n, g >> k_max; regulated Q_n = k_n F_n, 0 < k_n <= k_max; gate condition g -> k_n (L30-36).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: gradual vs sudden; universality; link to B-208 (L48-50).
- Conflicts: none.

## G-711 — Namika — Inter-System Relation (No Internal Gate 7)   (`Nodes/G-711_Gate_7.md`)
- Gate / lifecycle: YELLOW / ACTIVE; "Implementation-canonical no-7 rule".
- Upstream: none listed. Downstream / cites: none listed.
- Core claim: "A complete internal system contains **six** logical pair operations. There is no seventh internal gate appended after Gate 6." (L16); Namika = relation between two complete six-operation systems (L36-44).
- Equations: sequence F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6 - F1/V6 ... (L29).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Namika mechanics, data packet, physical realization open (L58).
- Conflicts: none against canonical rules. Internal: supersedes old "Gate 7 review" meaning, which is still used by G-716 L21, G-716a L26, G-718 L22-25, G-719 L70-78, G-724 L27/L56-88, G-725 L61 (see summary).

## G-712 — Evaluation Mathematics   (`Nodes/G-712_Evaluation_Mathematics.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Resolution / Formalization Node.
- Upstream: G-702. Downstream / cites: G-713, B-216, G-716; B-208.
- Core claim: candidate significance threshold from ONEWAVE_BRAIN_raw_material_UNVALIDATED.md: "E_n is significant iff E_pattern(Delta_n) / E_noise(Delta_n) > 1" (L29-30); "Dream Generation Test," "Higher Mind" framing NOT adopted (L23-26).
- Equations: E_n = E(Delta_n, T_n, context) (L48); candidate E_n = sigma(w_1 Delta_n + w_2 T_n + w_3 history_n) (L57).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: significance threshold, classification, urgency weighting, context integration; "Candidate form is speculative — not operational" (L67-71). Internal tension: Reason block (L15-18) and audit (L67) still say threshold open while L29-36 supplies a candidate.
- Conflicts: none.

## G-713 — Modulation Mathematics   (`Nodes/G-713_Modulation_Mathematics.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-703, G-712, B-216. Downstream / cites: G-714, G-716; G-720, I-04.
- Core claim: choose r_n = argmin_r J(r), "replaces the earlier undefined `argmax utility` placeholder" (L84-88); "Lowering energy is not a special failure path" (L125-126).
- Equations: Theta_n = [q_n,a_n,p_n]^T; Theta_hat^(r) = Pi_Omega(Theta_n + B u^(r)); J(r) = (Theta_hat-Theta*)^T W (Theta_hat-Theta*) + rho||u||^2 + lambda_D D + lambda_S S; D(Theta) = [a-a_danger]_+^2 + [q_break-q]_+^2; u_n = -(W + rho I)^(-1) W (Theta_n - Theta*) (L24-109); eigenvalues of (W+rho I)^(-1)W in [0,1) (L112).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: W, rho, lambda_D, lambda_S need calibration; I-04 access penalty; Bronze needs trajectory runs (L141-145).
- Conflicts: none.

## G-714 — Decision Mathematics   (`Nodes/G-714_Decision_Mathematics.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-713, B-208, B-209, B-210. Downstream / cites: B-209, B-210, G-716; B-207, B-216, CCD-04.
- Core claim: "formal mathematical framework for Return vs Break selection" (L28); "the Appendix G instantiation of CCD-04" (L56).
- Equations: Decision = f(T_n, E_n, M_n, history_n); f > threshold_return -> Return; f < threshold_break -> Break (L42-46).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: criterion, threshold, deterministic vs probabilistic, CCD-04 link (L52-55).
- Conflicts: none.

## G-715 — Stellar Boundary Reversal   (`Nodes/G-715_Stellar_Boundary_Reversal.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Class FUNCTION, alt ID FUNC-SBR-001 (L16-19); "Not a book chapter. Not a book node." (L27-28).
- Upstream: none by ID; references G-716 Bronze grammar (L477-498), "Mirror Gate" (L554). Downstream / cites: future stellar/solar/plasma/boundary nodes (L29).
- Core claim: "the surface is the hold boundary. the corona is the release field." (L47-49); "The corona is hotter than the visible surface because the surface is a compression boundary, and the corona is where boundary tension converts into released wave energy." (L136)
- Equations: T_core > T_cor > T_s (L344); E_c -> E_s -> E_m / E_w -> E_cor (L352); dE_cor/dt = P_release - P_loss (L358); P_release = P_wave + P_reconnection + P_turbulence (L370); P_boundary_release = f(E_s, E_m, E_w, Delta B, Delta P, Delta rho) (L382).
- Point / Path / Field role: Field only — "magnetic loops = tension pathways", "Magnetic paths store twist and tension", "Boundary motion shakes those paths" (L240, L251-252); switchback = "temporary reversal, fold, or kink in the outward magnetic reference" (L278). No Point rotation, no L, no stellar spin statement. "stellar body = pressure knot" (L238).
- Magnetism / gravity / rotation link: magnetism as stored tension/twist released by reconnection or wave dissipation into coronal heat (L251-256, L370). No gravity statement. No point-rotation statement ("twist" is field-line twist, not body spin).
- Open / parked / not-set items: seven Yellow items L551-557 (conversion rule, separation of heating terms, switchback cause/effect, Mirror-Gate-to-switchback math, simulation of T_cor > T_s, density correction, Bronze link). Status YELLOW until simulation (L635).
- Conflicts: none against canonical rules. "solar-wind expansion behavior" (L281) and "release -> escape -> expansion flow" (L472) refer to local solar-wind outflow, not cosmological expansion — not a conflict with "no expansion, no scale factor", but a watch-term. "Mirror Gate" (L554) is ambiguous after G-717 rename (C-301 owns the name).

## G-716 — One-Wave Conversion Grammar   (`Nodes/G-716_One_Wave_Conversion_Grammar.md`)
- Gate / lifecycle: BRONZE / ACTIVE (structural grammar only).
- Upstream: A-117, G-711 Gate 7, G-712, G-713, G-714. Bidirectional/Lateral: D-410; Lateral: Mirror Gate, Paired Exchange, State Changer. Downstream / cites: G-716a, boundary-reversal, biological, stellar, consciousness-conversion nodes.
- Core claim: "the reusable state-change pattern by which a complex field-state compresses through ordered layers, passes through repeated zero-point gates, reaches single-crossing identity, and returns to full-field expression as a changed state." (L27); "Only one entity may occupy the active conversion crossing at a time." (L117); "Bronze does not mean externally proven." (L374)
- Equations: 24 > 1(0)1 < 12 > 1(0)1 < 6 > 1(0)1 < 3 > 1(0)1 < 1 > 1(0)1 < 24 (L41); 24 -> 12 -> 6 -> 3 -> 1 -> 24 (L47); T_n = G(S_n -> S_{n+1}); S_24' != S_24; N_active_gate_entities <= 1 (L321-347); I_n -> R_n -> Delta_n -> E(Delta_n) -> M(E(Delta_n)) -> V_n -> I_{n+1} (L235).
- Point / Path / Field role: none stated in Point/Path/Field rotation sense (layers are conversion layers; "not automatically spatial dimensions", L394).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Yellow items L401-407 (biological, stellar, Sargasso, eel/frog/fish, consciousness, hardware, physical 24/12/6/3/1); Gold reserved for external validation.
- Conflicts: none against canonical rules. Internal: upstream "G-711 Gate 7" (L21) uses superseded name; "Lateral: Mirror Gate" (L23) ambiguous after G-717 rename.

## G-716a — One-Wave Conversion Simulation Rule   (`Nodes/G-716a_One_Wave_Conversion_Simulation_Rule.md`)
- Gate / lifecycle: YELLOW / ACTIVE; "first successful validation may support BRONZE".
- Upstream: A-117, G-716. Bidirectional/Lateral: D-410; Lateral: G-711 Gate 7, G-712, G-713, G-714, State Changer. Downstream / cites: Silver receipts, biological/stellar/consciousness tests; I-02.
- Core claim: "It proves whether the conversion grammar can be executed, logged, checked, and repeated without internal contradiction." (L34); embedded Python v0.1 OneWaveConversionGate (L209-330).
- Equations: layer path [24, 12, 6, 3, 1, 24]; min log length 5 transitions (L189-203).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: L453-459 (layers unmeasured, labels symbolic, logical gate lock, multi-entity rejection, path corruption tests). Internal: Node Sentence L481 calls it "Yellow/Silver-candidate" while L398/L405/L491 say Bronze-promotion candidate.
- Conflicts: none against canonical rules. Note: the code's lock is released in `finally` and the gate is never concurrently entered in the demo, so "multi-entity rejection" is untested (L458 admits this).

## G-717 — Paired Reference Gate   (`Nodes/G-717_Paired_Reference_Gate.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: concept names only (Two References, Shared Middle, Paired Exchange, Pair Response / Commit Condition) — "not real node IDs" (L39-41). Downstream / cites: C-301 Mirror Gate, B-205, C-308 (in naming note L16-24).
- Core claim: "A Paired Reference Gate is valid only when both directions share the same middle." (L110); "No return means no completed Paired Reference Gate." (L121); renamed from "Mirror Gate" in C-301's favor (L16-24).
- Equations: A(0)B / B(0)A; 1(0)-1 / -1(0)1; progression to 5(0)-5 / -5(0)5 (L69-104).
- Point / Path / Field role: none stated ("oscillates about the shared middle", L61 — exchange oscillation, not body rotation). C-301 noted as owning "spin/topology framing" (L22-23).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Pair Response / Commit Condition rule unseparated (L182-184); dependencies to real IDs open.
- Conflicts: none.

## G-718 — Connection Gates   (`Nodes/G-718_Connection_Gates.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Application / Relational Framework.
- Upstream: G-710, B-224. Downstream / cites: none yet; E-514, G-711, I-05.
- Core claim: seven relational gates (Invitation ... Connection) (L36-44); "no control of another system. Only control of your own state and response." (L46-47); "None derived. ... not derived from the field equations" (L56-59).
- Equations: none (cites Q_n = k_n F_n from G-710, L48).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: no math; Gate 6 ~ G-710 parallel unverified; gate independence untested; no worked example (L62-71).
- Conflicts: none against canonical rules. Internal: L22-25 describes G-711 as "repository self-review", which G-711 now explicitly supersedes (G-711 L18, L52).

## G-719 — Neural System Functional Analogy Map (Hypothesis Layer)   (`Nodes/G-719_Neural_System_Functional_Analogy_Map.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS; "explicitly not anatomical claim".
- Upstream: B-221, G-711, B-213, C-312, B-209, A-111, G-710. Downstream / cites: Books/Proposed_One_Wave_Consciousness, Books/Proposed_Android_Brain; I-05.
- Core claim: functional, not anatomical, comparison (L14-19); re-groundings: Four Mind + Rest + Break = B-221 renamed (L107-124); Five Mind grounded in A-111 neighbor average beta_i(<psi_j> - psi_i) (L128-135); Six Mind grounded in G-710 not G-711 (L137-145).
- Equations: none new; cites B-209 |M_i| > R_i (L114), Q_n = k_n F_n (L141).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: no simulation/prediction/test for any layer (L97-99).
- Conflicts: none against canonical rules. Internal: L70-78 describes G-711 as "a seventh element reviewing six others ... Gate 7 reviews" — superseded by G-711's no-internal-Gate-7 correction.

## G-720 — No Control But Self-Control — Reaction Choice Model   (`Nodes/G-720_No_Control_But_Self_Control.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: B-203, B-204, G-710. Downstream / cites: Proposed One-Wave Consciousness Ch2; B-221, G-702, G-703, G-709, B-216.
- Core claim: "A system does not directly control an external stimulus, another agent, or a past event. It controls only the transformation between received input and its own next state." (L22); Receive -> Hold -> Commit; Commit replaces Move to avoid B-221 collision (L59-62).
- Equations: R_a = g S; R_c = k(M) S, 0 <= k(M) <= k_max; sigma in {-1,+1}; Delta psi = sigma R; psi_{n+1} = psi_n + sigma_n R_n; worked example S=4, g=4 -> R_a=16; k=0.75 -> R_c=3; psi 10 -> 26 vs 13 (L26-112).
- Point / Path / Field role: none stated. (Loose analogy only: a system keeps control of its own state, not another's — parallels but does not state the canonical "keeps the point spin it has" rule.)
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: k(M) not derived; no dynamic simulation; not Bronze (L132-133).
- Conflicts: none.

## G-721 — Mirrored Alphabet Rabbit-Hop Coordinate Algorithm   (`Nodes/G-721_Mirrored_Alphabet_Rabbit_Hop_Coordinate_Algorithm.md`)
- Gate / lifecycle: YELLOW / ACTIVE; BRONZE (packet, parity wrapper, mirror/inversion grammar, arithmetic identities) / YELLOW (cross-domain, embodied).
- Upstream: A-101, A-103, A-111, B-205, B-222, B-223, G-716. Lateral: E-510, G-719, G-720. Downstream / cites: G-721a-e, Wave Computer, Android, Goblin; authority RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md and One_Wave_Bench/brain/rabbit_hop_core.py ("the lock/core wins", L14-18); rabbit_hop_alphabet.py, rabbit_hop_music.py, rabbit_hop_scale_rail.py, RABBIT_HOPPING_MUSIC_ADAPTER.md.
- Core claim: alphabet adapter converts letters to "ordered, reversible coordinate paths" and "does not claim that different physical or software systems are identical" (L27-30); mirrored / inverted / opposing remain separate (L191-195).
- Equations: N_inv = 27 - N; TOP = 2N; TOP = 2N + K; TOP = 2(N + K); V_K^s(N) = 2N + K + s; U_K^s(N) = 2(N+K) + s; N = (X - K - s)/2; N = (X - s)/2 - K; X_t = sigma_t (2N_t + K_t + s_t); Delta X_t = X_(t+1) - X_t (L58-251).
- Point / Path / Field role: explicit but declared as translator interpretation only: "Point_N -> Path_N -> Field_N -> next nested address" (L215); "This is a translator interpretation. A target domain must be tested separately" (L219-220). No rotation, L, or curl content.
- Magnetism / gravity / rotation link: none stated ("wheel system = live oscillating movement geometry", L37, is separate layer).
- Open / parked / not-set items: broader division claims open (L186-187); falsifier L329-332; "route arithmetic is presented as proof of a physical mechanism" listed as failure (L325).
- Conflicts: none. The Point/Path/Field naming here is an address-nesting map, not the canonical three-rate Point/Path/Field decomposition; it does not claim the canonical meaning, but readers could conflate them.

## G-721a — Fibonacci Word Hop Validation   (`Nodes/G-721a_Fibonacci_Word_Hop_Validation.md`)
- Gate / lifecycle: YELLOW / ACTIVE; BRONZE (Fibonacci-word math and validator) / YELLOW (route relevance).
- Upstream: G-706, G-712, G-721. Lateral: A-117, G-720. Downstream / cites: G-721b, Wave Computer, Android; Nodes/G-721a_Validation/ (validator.py, csv, json, png, README).
- Core claim: "Fibonacci word = ordered hop validation grammar"; "phi = long-run metric of that grammar" (L33-37); "The golden ratio does not generate the alphabet packet and does not make the live choice." (L40); does not apply phi to lattice / 6:1 / 12:1 / 24:1 (L28).
- Equations: b_t = (|o_t| - |e_t| + 1)/2; W_0 = f_0, W_1 = f_0 f_1, W_k = W_{k-1}W_{k-2}; L_k = F_{k+2}; Z_k = F_{k+1}; O_k = F_k; j_t = |e_t|/2 - |n_t|; epsilon_W(N) = (1/N) sum 1[b_t != w_t]; p(m) = m+1; epsilon_phi ratios (L65-291).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (L359 excludes "proton, quark, Mass-Effect, or Mirror-Gate physics").
- Open / parked / not-set items: factor-complexity test "when tested" (L390); falsifiers L445-451.
- Conflicts: none.

## G-721b — Sturmian Binary Branch Grammar   (`Nodes/G-721b_Sturmian_Binary_Branch_Grammar.md`)
- Gate / lifecycle: YELLOW / ACTIVE; BRONZE (external math) / YELLOW (route and android relevance).
- Upstream: G-721, G-721a. Lateral: G-706, G-720. Downstream / cites: G-721c, G-721d, Android.
- Core claim: generalizes G-721a to the Sturmian family; "live `-1(0)+1` choice still decides movement or hold" (L47); "It does not directly command a joint." (L97)
- Equations: b_t = floor((t+1)alpha + rho) - floor(t alpha + rho); e_t = 2(n_t + j_t), o_t = e_t + (2b_t - 1); p(m) = m+1; frequencies 1/phi^2 vs 1/phi (L26-75).
- Point / Path / Field role: none stated. ("coding by irrational rotations", L58, is symbolic-dynamics rotation, not physical spin.)
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: finite-sample undercounting must be stated (L69).
- Conflicts: none.

## G-721c — Episturmian Multi-Route Directive Grammar   (`Nodes/G-721c_Episturmian_Multi_Route_Directive_Grammar.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-721, G-721b, D-411. Lateral: B-205, G-720. Downstream / cites: G-721d, G-722.
- Core claim: uses episturmian mathematics "as a candidate scheduler for movement-route families, not as a claim about physical lattice construction" (L25); palindromic closure "is not physical proof of the Mirror Gate" (L69).
- Equations: Delta q_t = c_t d_{x_t}, c_t in {-1,0,+1} (L44-50); k route families -> 2k directed routes + 1 center (L60).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: general episturmian complexity not fixed; exact claims need G-721d (L81).
- Conflicts: none.

## G-721d — Arnoux-Rauzy Strict Multi-Route Validation   (`Nodes/G-721d_Arnoux_Rauzy_Strict_Multi_Route_Validation.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: G-721c, G-706. Lateral: D-411. Downstream / cites: ternary triangular-route tests; Nodes/G-721_Sequence_Validation/.
- Core claim: k-letter Arnoux-Rauzy factor complexity p(m) = (k-1)m + 1; ternary p(m) = 2m+1 (L26-32); "Balance is measured, not assumed." (L63); "useful behavior does not grant a mathematical family name by diplomatic immunity" (L73).
- Equations: p(m) = (k-1)m + 1; p(m) = 2m + 1 (L26, L32).
- Point / Path / Field role: none stated. (Mentions torus rotation / Rauzy fractal realization as not automatic, L65 — symbolic, not physical.)
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: finite approximation of infinite recurrence (L49); receipt validates code, "not android movement" (L81).
- Conflicts: none.

## G-721e — Plastic-Padovan Three-Rail Grammar   (`Nodes/G-721e_Plastic_Padovan_Three_Rail_Grammar.md`)
- Gate / lifecycle: YELLOW / ACTIVE; BRONZE (algebraic recurrence) / YELLOW (alphabet and motor relevance).
- Upstream: G-721, G-721b. Lateral: G-723. Downstream / cites: three-rail tests, Android; Nodes/G-721_Sequence_Validation/.
- Core claim: substitution I -> EO, E -> I, O -> E with char. poly x^3 - x - 1, plastic number rho ~ 1.324717957 (Pisot) (L39-65); "This is a proposed mapping, not a theorem of plastic-number dynamics." (L89)
- Equations: I_n = n, E_{n,j} = 2(n+j), O_{n,j,s} = E_{n,j} + s; M_P incidence matrix; L_{m+3} = L_{m+1} + L_m; R(n_t,s_t) piecewise (L25-100). (Matrix checked: columns I,E,O = (0,1,1),(1,0,0),(0,1,0), consistent with substitution.)
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: seed/indexing must be stored (L77); falsifiers L125.
- Conflicts: none.

## G-722 — Android Subconscious Motor Memory Architecture   (`Nodes/G-722_Android_Subconscious_Motor_Memory_Architecture.md`)
- Gate / lifecycle: GREEN / PROPOSED_BUILD; YELLOW (build architecture) / GREEN (role separation).
- Upstream: G-719, G-720, G-721..G-721e, D-411. Lateral: E-510..E-514. Downstream / cites: Pong controller, Goblin agent, android balance/reach/walk sims.
- Core claim: locked role separation Hopfield / Boltzmann / sequence grammar / -1(0)+1 / binary; "No layer may impersonate all the others." (L22-41); "Binary oversight must not become the ordinary source of movement choice." (L101)
- Equations: P(m) proportional to exp(-E(m)/T) (L62); c_i in {-1,0,+1} (L76).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: eight minimum experiments (L120-127); falsifiers L131.
- Conflicts: none.

## G-723 — Pisot-Salem-Mahler Motor Stability Audit   (`Nodes/G-723_Pisot_Salem_Mahler_Motor_Stability_Audit.md`)
- Gate / lifecycle: YELLOW / ACTIVE; classification "Spectral Audit / Expansion-Contraction-Rhythm Measurement".
- Upstream: G-722, G-706. Lateral: G-721d, G-721e. Downstream / cites: G-723a; Nodes/G-723_Spectral_Validation/.
- Core claim: "This node audits structured recurrence matrices and substitution systems. It does not generate foundational movement." (L21); Lehmer's number "not a proven android threshold" (L82).
- Equations: M(P) = |a| prod max(1,|lambda_j|); m(P) = log M(P); lambda_correction < 0, lambda_rhythm ~ 0, lambda_drive > 0 only while commanded and bounded (L58-99).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Salem spectrum "potentially relevant to gait, counter-rotation, alternating pressure, and balance rhythms. It is an analogy and design target" (L45) — motor counter-rotation analogy only, no L/inertia claim.
- Open / parked / not-set items: spectral report requirements (L69-78); Lehmer conjecture open (L82).
- Conflicts: none. "Expansion" here means algebraic root expansion outside the unit circle (L63), not cosmological expansion.

## G-723a — Advanced Mahler and Regulator Computation Hold   (`Nodes/G-723a_Advanced_Mahler_Regulator_Computation_Hold.md`)
- Gate / lifecycle: GREEN / HELD; GRAY external reference.
- Upstream: G-723. Downstream / cites: none until qualifying polynomial.
- Core claim: Deninger, Fuglede-Kadison, Rodriguez-Villegas, elliptic dilogarithm methods "are not part of the active subconscious movement mechanism" (L20); prohibition L50.
- Equations: none (P(x,y)=0 elliptic curve mention, L46).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: four entry conditions (L24-29); release rule (L54).
- Conflicts: none.

## G-724 — M4 Heterogeneous Runtime and Dual Six-Gate Controller   (`Nodes/G-724_M4_Heterogeneous_Runtime_and_Dual_Six_Gate_Controller.md`)
- Gate / lifecycle: GREEN / PROPOSED_BUILD; YELLOW (state architecture) / GREEN (device allocation).
- Upstream: A-101, A-110, A-111, B-203, B-204, B-206, B-208, B-221, B-222, B-223, B-224, C-312, D-411, G-711, G-718, G-719, G-720, G-722; authority UPDATED_42_CENTER_ORIGIN_M4_HETEROGENEOUS_RUNTIME.md.
- Core claim: CPU authoritative / GPU Field-lattice / NPU M4 fast loop (L27-29); "FIELD = FIVE MIND = DREAM ENGINE"; "VOID = SIX MIND = ADMINISTRATOR"; "Void means the reference/receiving/containing/commitment side, not absence." (L36-41); "Mirror is phase rotation and never a Field/Void label swap." (L54)
- Equations: C7 = min(min(S), min(E), L_phi) * P; hysteresis T_open > T_close (L64-71) — "engineering candidate, not derived physical law" (L73).
- Point / Path / Field role: none stated in rotation sense ("Mirror is phase rotation", L54, is a mirror-operation definition, not point spin).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: remains GREEN until executable implementation, schemas, CPU tests (L93-96).
- Conflicts: none against canonical rules. Internal: "Gate-7 commit" (L27), "Dual six-gate and Gate-7 rule" (L56), "Closed-loop Gate-7 integration" (L88) use Gate-7 terminology that G-711 says is not an internal gate; C7 is two six-gate scores coupled, which matches G-711 Namika (inter-system) only if read that way — not stated.

## G-725 — Cross-Domain Build-Hold-Release and Coupled-Mind Grammar   (`Nodes/G-725_Cross_Domain_Build_Hold_Release_and_Coupled_Mind_Grammar.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS; GREEN (grammar) / BROWN (physical scale invariance).
- Upstream: none listed by ID. Downstream / cites: Books/Proposed_One_Wave_Consciousness/Ch05_Two_Hemispheres_M4_Dream_Administrator_and_Cross_Domain_Coupling.md.
- Core claim: shared recursive architecture across hemispheres, human/AI connection, music, physiology, quasars "without claiming that the domains are materially identical" (L16-21); "one mind with complementary functions, not two controlling selves" (L32).
- Equations: N > 1(0)1 < 2N; 2D 3 > 1(0)1 < 6; 3D 6 > 1(0)1 < 12; 4D 12 > 1(0)1 < 24; 1:1 ultimate compression (L36-41); A_(k+1) = Transform_k(A_k) (L54).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (quasar build/release mentioned, L18, gated by "Gray control models", L84).
- Open / parked / not-set items: domain support requires native variables, units, reference, phase, boundary, hysteresis, flow budget, normalization, falsification (L71-73); failure conditions L79-85.
- Conflicts: none against canonical rules. Internal: "retained identity across Gate-7 coupling" (L61) — consistent with G-711 Namika only as inter-system coupling; not cross-referenced.

## Slice summary

(a) Nodes bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking:
- F-608 Attenuation: Path loss dA/dx = -mu A with mu depending on "Lattice resistance gamma" and coupling beta (L34-37); closest node in slice to resistance/path loss (E-528-adjacent but not cited). No L.
- F-603 Transfer: conservation closure Q_1 + Q_2 = const; Q unfixed — could host L bookkeeping but does not name it.
- F-605 Interference: phase-dependent combination; omega is oscillation frequency, not point spin.
- F-606/F-607 Reflection/Transmission: boundary split r + t = 1; r possibly tied to lattice coupling beta_i (open).
- G-705 Correction: identifies update-rule term beta_i(<psi_j> - psi_i) as automatic lattice correction (L39) — lattice organization pulling toward neighbor average.
- G-719: Five Mind grounded in A-111 multi-neighbor average (lattice organization term), L128-135.
- G-715 Stellar Boundary Reversal: Field-only magnetism — magnetic loops store twist/tension, released by reconnection/wave dissipation into coronal heat; switchbacks as magnetic folds. No point rotation, no gravity, no L.
- G-721: uses the words "Point_N -> Path_N -> Field_N" as nested address map (L215), explicitly a translator interpretation, not the canonical three-rate decomposition.
- G-723: Salem spectrum analogy to gait "counter-rotation" (L45); Lyapunov correction/rhythm/drive targets. Analogy only.
- G-724: "Mirror is phase rotation" (L54); GPU assigned Field/lattice computation.
- G-711 Namika / G-724 C7 / G-725 Gate-7 coupling: two complete six-op systems coupled through a shared reference — structural analogue of bound/parent-child coupling, but no rotation or transport math.
- All other slice nodes (F-601, F-602, F-604, G-701..G-704, G-706..G-710, G-712..G-714, G-716, G-716a, G-717, G-718, G-720, G-721a..G-721e, G-722, G-723a) state nothing about Point/Path/Field rotation, magnetism, gravity, inertia, mass, or locking.

(b) Conflicts found:
- Against the canonical rules: none. No file in this slice states L = I omega, point spin initiation, gravity-rotation coupling, magnetism-to-gravity conversion, expansion/scale factor, or exceptions to C-306/C-307 L bookkeeping.
- Watch-terms (not conflicts): G-715 L281 "solar-wind expansion behavior" and L472 "expansion flow" (local outflow, not cosmology); G-723 classification "Expansion-Contraction" (algebraic root moduli); G-721 L215 Point/Path/Field naming as address nesting; F-608 gamma symbol overlaps the canonical damping gamma in dL/dt = -gamma L without linkage.
- Internal (repository) inconsistencies:
  1. G-711 says there is no internal Gate 7 (L16-18, L52), but G-716 L21 and G-716a L26 cite "G-711 Gate 7"; G-718 L22-25 and G-719 L70-78 describe G-711 as Gate-7 repository review; G-724 L27, L56, L88 use "Gate-7 commit/rule/integration"; G-725 L61 "Gate-7 coupling".
  2. F-603 L35, F-604 L44, F-607 L38 still list Amplification/Persistence downstream although their own repair notes say F-609/F-610 do not exist.
  3. G-716 L23 "Lateral: Mirror Gate" and G-715 L554 "Mirror Gate reversal" are ambiguous after G-717 was renamed and C-301 retained the "Mirror Gate" name.
  4. G-716a L481 "Yellow/Silver-candidate" vs L398/L405/L491 "BRONZE-promotion candidate".
  5. G-712 Reason/audit (L15-18, L67) still say significance threshold is open while L29-36 supplies a candidate.

(c) Cross-references outside the slice that matter for point rotation or magnetism:
- C-301 Mirror Gate (spin/topology framing), B-205 Mirror, C-308 Spin-half — cited by G-717 L16-24.
- C-312 Hierarchical Sensor-Control Architecture — G-719, G-724.
- A-111 Recursion / update rule beta_i(<psi_j> - psi_i), A-109 — G-705, G-719 (lattice organization/neighbor pull).
- A-112 Persistent Mode, E-508 Real Persistence Under Loss — F-series repair notes (persistence under loss).
- E-505 stability — G-707.
- D-410 Twenty-Fourfold 4D Recurrence Shell, D-411 Mirrored Axis-Pair Counts, A-117 Dimensional Integrity — G-716, G-716a, G-721c/d, G-722, G-724.
- E-510..E-514 movement geometry / Music Clock (wheel system) — G-721, G-722.
- UPDATED_42_CENTER_ORIGIN_M4_HETEROGENEOUS_RUNTIME.md — G-724 authority file.
- RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md, One_Wave_Bench/brain/rabbit_hop_core.py — G-721 authority.
- No file in this slice cites G-749, G-750, G-769, C-306, C-307, C-311, C-319, C-320, A-115, E-528, or E-530.
