# Ledger 02 — Slice 02 (27 files, B-216 .. C-312)

All 27 files were read in full (Read, no limit). Line numbers are from the file as read.

## B-216 — Threshold Mathematics   (`Nodes/B-216_Threshold_Mathematics.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Resolution / Formalization Node.
- Upstream: B-207 Threshold State, B-208 Threshold Windows, G-712 Evaluation Mathematics (L15).   Downstream / cites: B-209 Break Condition, B-210 Return, G-713 Modulation Mathematics, G-714 Decision Mathematics (L16-17).
- Core claim: normalized threshold state `Theta_n = [q_n, a_n, p_n]^T` on `Omega = [0,1] x [0,1] x [-1,1]` (L24, L30); proportional restoration is stable for gains in (0,2), "an internal mathematical result, not an experimental calibration" (L94). Activation and polarity are separate axes, so "healthy energy reduction is not the same operation as compression or retreat" (L111-112).
- Equations: `e_n = Theta_n - Theta*_n` (L42); `Theta_(n+1) = Pi_Omega(Theta_n + B u_n + w_n)` (L50); `u_n = -K e_n`, `K = diag(k_q,k_a,k_p)` (L64-65); `e_(n+1) = (I - K)e_n` (L71); `0 < k_j < 2` (L77-79); `|1-k_j| < 1` (L91); `d_n = min(1, sqrt(w_a(a_1-a_2)^2 + w_p(p_1-p_2)^2))` (L126); `q_(n+1) = clip(q_n + eta(1-d_n) - mu d_n - xi O_n, 0, 1)` (L132); `O_n = [a_n - a_danger]_+` (L145); `0 <= q_break < q_return <= 1` (L157); break/return/hold rules (L163-165); reset `N_danger >= N_reset` (L182).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: eta, mu, xi and the mismatch weights need calibration; scale-specific measurement of a, p, q; noise and delayed feedback unresolved; Bronze needs a reproducible simulation (L201-205).
- Conflicts: none.

## B-217 — Access Line Mathematics   (`Nodes/B-217_Access_Line_Mathematics.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Resolution / Formalization Node.
- Upstream: B-213 Access Line, B-214 Recursive Access Growth (L20).   Downstream / cites: B-218 Hyperloop Mathematics (L21).
- Core claim: "formal mathematical framework governing how individual Access Lines behave — persistence, merging, reactivation, strength, and directionality" (L24-26). It records a Flat versus Weighted depth fork and does not choose between them (L74-75).
- Equations (all candidates): `S_i(t) = S_i(0) * exp(-lambda_i * t)` (L39); `S_i(t+1) = S_i(t) + mu * usage(t)` (L46); Flat `d_k = d_0 + k` (L65); Weighted `d_k = d_0 + Σ w_i` (L68).
- Point / Path / Field role: none stated. Directionality (scalar, vector or paired-scalar) is not formalized (L49-53).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: lambda_i, mu, directionality and merge/collapse (no form proposed); the Flat vs Weighted fork is unresolved; per-line roles of the 7 Access Lines (L83-92).
- Conflicts: none.

## B-218 — Hyperloop Mathematics   (`Nodes/B-218_Hyperloop_Mathematics.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Cycle and Relationship Structure.
- Upstream: B-215 Hyperloop, B-217 (L15).   Downstream / cites: Books, applied Hyperloop contexts (L16).
- Core claim: a formal framework for entering, operating in and leaving the Hyperloop. Its internal mathematics are "not yet derived" (L19-21).
- Equations: `n_loop >= 7 => Hyperloop` (L24); `Var[T(n)] < epsilon_H` (L27); `C_correction^(k) = C_0 * alpha^k, 0 < alpha < 1` (L30); `T < T_exit => Hyperloop exits to Paired Loop` (L34); `d_H = d_0 + 7` (L37).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: epsilon_H, alpha and T_exit are not set; whether a shortcut entry exists; whether exit is gradual decay or sudden collapse (L40-44).
- Conflicts: none.

## B-219 — PRESSURE REVERSAL   (`Nodes/B-219_Pressure_Reversal.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Simulation NOT STARTED; Relations PROVISIONAL ONLY (L29-33). Alternate ID PHYS_PRESSURE_REVERSAL (L14). Placement: Appendix B, Interaction Functions.
- Upstream: none formally listed. It relates to the Conversion Grammar `24->12->6->3->1->24` but is "not the same node" (L289-296).   Downstream / cites: Appendix G (later checks), Book One Ch7 (positron and matter/antimatter applications) (L543-560).
- Core claim: "Pressure is not destruction. Pressure is transformation. The gate does not crush. The gate reverses." (L62-65). An entity compressed through `24 -> 12 -> 6 -> 3 -> 1(0)1` may reverse instead of collapsing (L592).
- Equations: pressure factors 1, 2, 4, 8, 16 by layer (L148-153); `R = (entity_state + environmental_factors) / (2 * pressure_at_layer)`; cross if `R > 0.5`, fail if `R <= 0.5` (L192-203, L428-429). The file calls this "a simulation skeleton, not final physics proof" (L205).
- Point / Path / Field role: none stated. Compression is described only as layered pressure.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: all applications are candidates only (eels, frogs, positron, matter/antimatter) (L80-89, L300-318). A relation-hold rule applies until simulation plugins and receipt logs exist (L482-491). The file disallows the words "proves/confirms/solves/locks/establishes" (L505-512).
- Conflicts: none.

## B-220 — Scale Layer (Micro/Small/Medium/Large/Macro)   (`Nodes/B-220_Scale_Layer.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Resolution / Formalization Node.
- Upstream: A-101 §8 Recursive Scaling (L20). Bidirectional with E-507 Scale-Invariant Loop (L21-26).   Downstream / cites: B-221 nested recursion; all A-series §8 sections (L27).
- Core claim: B-220 is the shared primitive for the repeated "Preserve [node] meaning across Micro, Small, Medium, Large, Macro" requirement (L30-34). Scale ordering is by containment, `Micro ⊂ Small ⊂ Medium ⊂ Large ⊂ Macro` (L46-47). Scale and phase are orthogonal, so a system state is `(scale, phase)` (L38-41). The transition question reduces to finding γ(s) and β(s) (L67-71).
- Equations: the E-507/A-111 update rule `ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + βᵢ(⟨ψⱼⁿ⟩-ψᵢⁿ)` (L57); an older candidate `S_(n+1) = T(S_n, C_n, R_n)` (L74).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated. A withdrawn Ch15 electroweak/Planck ratio (~10^17) was explicitly retracted (L78-90).
- Open / parked / not-set items: the scaling laws for γ(s) and β(s); whether containment is the right relation (versus ratio, resolution or sampling rate); B-221's nested-cycle dependency; whether to retrofit the A-series §8 sections (L104-131).
- Conflicts: none against the canonical rules. Internal cross-reference drift: L39 names "B-225 Field Cycle", but B-225's current canonical name is "Five-Level Modulation Compatibility Around Reference".

## B-221 — Six Recursive Steps (Master Cycle)   (`Nodes/B-221_Six_Recursive_Steps.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS (L5-8).
- Upstream: A+101, A-101, A-105, A-108, A-110, A-111, C-301 Mirror Gate, D-402, B-220, B-223, B-224 (L15).   Downstream / cites: B-207, B-206b, B-203/B-204, B-222, G-719, all recursive chains (L16).
- Core claim: `Begin -> Move -> Hold -> Build -> Break -> Loop` is the abstract cycle that every recursive chain instantiates (L19-22). HOLD alone does not return to BEGIN; HOLD needs A-108 to do that (L45-55). LOOP's operator G is an open fork between A-111 additive and C-301 rotational (L135-162).
- Equations: `ψ₀` (L32); `Δψ = ψ − ψ₀` (L35); `R_OW = -A(∇ψ)`, linear `R_OW = -α∇ψ` (L39); `Structure = Pattern + Persistence + Feedback` (L68); `Mᵢ = (1-γ)Δψᵢⁿ`, `|Mᵢ| < Rᵢ` gives return, `|Mᵢ| > Rᵢ` gives BREAK (L100-102); `New State = B(previous state, threshold position, crossing magnitude)` with crossing magnitude `|Mᵢ| - Rᵢ` (L131-132); A-111 update rule and `G = ψ_prev + M + C` (L142-145); Mirror `M(ψ_C, ψ_E) → (ψ_E, -ψ_C)`, `M²=-I`, `M⁴=I`, `ψ₀(n+4) = ψ₀(n)` (L148-151).
- Point / Path / Field role: none stated explicitly. LOOP candidate 2 is a rotation operator in state space (4-cycle closure, the same math as C-308 spin-half) (L147-151). It is not tied to physical point rotation.
- Magnetism / gravity / rotation link: L84-87 says C-301 to C-308 are "motion/momentum/spin mechanics", unrelated to feedback/response. Otherwise none stated.
- Open / parked / not-set items: the identity of operator G; the BUILD sum; the term-by-term B-207 correspondence; the 13-to-6 A-series grouping; the nested-recursion claim (pending B-220); the B-201 vs B-222 "Center" naming; Rᵢ is undefined (inherited from A-110) (L108-112, L227-304).
- Conflicts: none against the canonical rules. Internal: B-221's step order `Begin->Move->Hold->Build->Break->Loop` (L22) differs from the GREEN canonical lock in B-221a and C-301, which is `BEGIN->BUILD->HOLD->BUILD->BREAK->LOOP` (B-221a L25-30). B-221 also lists C-301 as only a "candidate" for LOOP's G, while C-301 now defines LOOP as Action 3, not a Mirror gate (C-301 L38).

## B-221a — Six-Step / Six-Gate Mirror-Action Oscillator   (`Nodes/B-221a_Six_Step_Oscillator_Program.md`)
- Gate / lifecycle: GREEN / ACTIVE. "Canonical architecture lock" (L8).
- Upstream: implied B-221 and C-301. Cites UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md (L72), G-739 (L66), G-742 (L101).   Downstream / cites: G-739 measures the gates but "may not redefine those behaviors" (L66).
- Core claim: `6 steps = 6 gates = 3 Mirror gates + 3 Action gates` (L19). Gate1 BEGIN=M1, Gate2 BUILD=A1, Gate3 HOLD=M2, Gate4 BUILD=A2, Gate5 BREAK=M3, Gate6 LOOP=A3 (L25-30). The Field/Void pairs are F1/V6, V5/F2, F3/V4, V3/F4, F5/V2, V1/F6, as "six coupled pair operations, not twelve serial instructions" (L42-50).
- Equations: route address space `2 binary choices x 3 ternary moves = 6 route addresses`, with `DOWN / HOLD / UP = -1 / 0 / +1` (L75-82). No physics equations.
- Point / Path / Field role: none stated. "Mirror gate = read / compare / reflect through reference; Action gate = act / carry / change the relation" (L93-94).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none. The file gives an anti-drift audit list (L121-128). Scale labels "are not aliases" for lifecycle, commitment, route or gate state (L117).
- Conflicts: none against the canonical rules. Internal: the step list conflicts with B-221 (see above), and the filename "Six_Step_Oscillator_Program" does not match the canonical name.

## B-222 — Oscillation Center   (`Nodes/B-222_Oscillation_Center.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS.
- Upstream: B-203, B-204, B-221, B-208 (45-30 band), B-224 (L15).   Downstream / cites: B-225 "Field Cycle (Center stage)" (L16).
- Core claim: a dynamic switching region between Compression and Expression, explicitly not B-201 Equilibrium Balance (L18-24, L27-31). It is "maximally adaptable — the point of highest information exchange and lowest commitment" (L33-35). 42.5 is a confirmed symmetric pivot of B-208's bands (85↔0, 75↔10) but it is not the midpoint of the 45-30 band, which is 37.5 (L42-63).
- Equations: none asserted ("No independent mathematics is asserted here yet", L38). Only the numerical pivot 42.5.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: whether the Center is a point or a region; whether B-201 and B-222 are the same; whether 42.5 is a Derived Center or an Oscillation Coordinate; formal adoption of the 45-30 band identification (L76-117).
- Conflicts: none against the canonical rules. Internal: B-224 (L53) says Compression/Expression is no longer the fundamental choice, while B-222 still frames the Loop choice as Compression↔Expression and lists B-224 upstream. The downstream "B-225 Field Cycle" is a stale name.

## B-223 — Three Moves — Left, Stay, Right   (`Nodes/B-223_Three_Moves.md`)
- Gate / lifecycle: YELLOW / ACTIVE; "Implementation-canonical signed ternary relation" (L8).
- Upstream: none listed.   Downstream / cites: distinguishes itself from the Four Actions (Inward/Outward/Across/Over) (L51-57).
- Core claim: `-1 = LEFT, 0 = STAY / HOLD / NON-ACTION, +1 = RIGHT` (L19-21). Left and Right are orientation labels and may be renamed, for example to "CCW/Hold/CW" (L24). "The zero state is a real no-assertion/hold result, not a third actively driven polarity" (L36).
- Equations: `Delta < -epsilon -> -1; |Delta| <= epsilon -> 0; Delta > +epsilon -> +1` (L31-33); `Delta = side_A - side_B`; a mirrored pair gives `Delta = 2A` (L64-67).
- Point / Path / Field role: none stated. The CCW/Hold/CW renaming (L24) is a label only, not a rotation claim.
- Magnetism / gravity / rotation link: none stated. "flux" thresholds must be measured per implementation (L72).
- Open / parked / not-set items: physical voltage, phase, flux and mechanical thresholds (L72).
- Conflicts: none.

## B-224 — Two Choices — Everything or Nothing   (`Nodes/B-224_Two_Choices.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: none listed (pairs with B-223).   Downstream / cites: B-223.
- Core claim: `EVERYTHING = engage / assert / open the operation; NOTHING = do not engage / high-Z / non-action` (L19-20). The DC choice decides whether to take part and the AC differential decides direction (L41-42). "0 belongs to the ternary differential layer... must not be implemented by inventing a third powered DC direction" (L47). It corrects the earlier Compression/Expression framing of the two choices (L53).
- Equations: none (a decision tree only, L28-36).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated. "inductive decay, and passive coupling" are validation items for NOTHING (L70).
- Open / parked / not-set items: the electrical realization of NOTHING; physical systems outside compute are only a representation claim (L69-71).
- Conflicts: none.

## B-225 — Five-Level Modulation Compatibility Around Reference   (`Nodes/B-225_Field_Cycle.md`)
- Gate / lifecycle: YELLOW / ACTIVE; legacy compatibility (L8).
- Upstream: cites UPDATED_43 (L32), G-742 (L42), G-739 (L62), UPDATED_44_STATE_AXIS_AUTHORITY_AND_EVOLUTION_RULE.md (L89).   Downstream / cites: none.
- Core claim: legacy `+2..-2` modulation "is not the repository's canonical five-state structure" (L28). The five commitment/readout states (`-3(0)3+ ... +3(0)3-`, `1:1 = unity / ultimate compression / Hold reference`) belong to UPDATED_43 (L35-39). The five-state lifecycle belongs to G-742. Scale is a separate axis (L72).
- Equations: `2 binary choices x 3 ternary moves = 6 routes` (L55); G-739 labels `BEGIN -> BUILD(coherent) -> HOLD -> BUILD(unstable) -> BREAK -> LOOP` (L65).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none new. Representation wrappers must be declared (L76-80).
- Conflicts: none against the canonical rules. Internal: the filename "Field_Cycle" and inbound references (B-220 L39, B-222 L16) do not match the current name.

## B-226 — Research Discovery and Invention Loop   (`Nodes/B-226_Research_Discovery_Invention_Loop.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS.
- Upstream: B-221, A-111, B-220 (L67).   Downstream / cites: research, education, debugging and AI orchestration workflows (L68).
- Core claim: `Primitive -> Relation -> Operation -> Composition -> Test -> Discovery -> next Primitive` (L30). The Complexity-Bottleneck Rule says repeated higher-level patches are "evidence to inspect lower-level assumptions" (L49-53).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the formal mapping to B-221 positions; Discovery promotion criteria; cross-domain validation (L71-73).
- Conflicts: none.

## B-227 — Time-Scale Bottleneck Loop   (`Nodes/B-227_Time_Scale_Bottleneck_Loop.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS.
- Upstream: B-220, B-221, B-226, A-111 (L78).   Downstream / cites: habit, workflow, research and AI diagnosis (L79).
- Core claim: `Second -> Minute -> Hour -> Day -> Week -> Month` diagnostic order, which can also be run downward (L30-34). "Do not assume the visible failure occurs at the scale where its cause lives" (L41).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: mismatch thresholds; translation for very fast or very slow systems; cross-domain testing (L82-84).
- Conflicts: none.

## B-228 — Compression Energy Chains   (`Nodes/B-228_Compression_Energy_Chains.md`)
- Gate / lifecycle: YELLOW / ACTIVE; "Analogy / Scale Bridge — not established biochemistry identity" (L7).
- Upstream: B-203, B-204, B-210, A-105, C-324 (no entanglement) (L14).   Downstream / cites: cell body builds, Book scale chapters, not the Cell-0 netlist (L15).
- Core claim: "ATP is a small reusable packet: ADP + Pi ↔ ATP. The usable kick is the phosphate transfer, not a singularity" (L21). The quasar and climax language is "the same three moves at another scale: load, squeeze, spend. They are not the same object as ATP" (L33). "Micro black hole" means only "a local compression well with a fence" (L35).
- Equations: `ADP + Pi ↔ ATP` (L21); sketch `chain --compress--> well --packet--> ATP --spend--> motion / pump / hold elsewhere` (L40).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: no kcal derivation. Falsifier: an astrophysical hole in a cell, or ATP with no named chemical net (L43).
- Conflicts: none.

## B-229 — One Wave Biology   (`Nodes/B-229_One_Wave_Biology.md`)
- Gate / lifecycle: YELLOW / ACTIVE; reinterpretation, not a replacement textbook.
- Upstream: B-203, B-204, B-210, B-223, B-224, B-228, C-324 (L14).   Downstream / cites: body-scale chapters (L15).
- Core claim: "Life is loops that can change, hold, and spend on named nets. No entanglement." (L19-20). A mapping table pairs membrane with fence/(0) skin, gradient with lean, channel/pump with gate up/down/stay, ATP with small compression packet, and so on (L25-39). "Same six-step shape, different size" (L55).
- Equations: none.
- Point / Path / Field role: none stated. A gradient is "lean, D across a wall" (L28), a biology mapping only.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: falsifier: a biological claim with no named molecule, membrane, current or receipt (L64).
- Conflicts: none. Minor internal note: the scale list "micro/small/cluster/body/macro" (L49-53) relabels B-220's Medium/Large.

## C-301 — Mirror Gate   (`Nodes/C-301_Mirror_Gate.md`)
- Gate / lifecycle: GREEN / ACTIVE; "three Mirror gates occupy three of the six primitive gate positions" (L8).
- Upstream: none listed (pairs with B-221a).   Downstream / cites: C-308 (via C-308's upstream), B-221 LOOP candidate.
- Core claim: "A Mirror Gate is the read/compare/reflect gate of the shared-reference oscillator" (L16). `3 Mirror gates + 3 Action gates = 6 gates = 6 steps` (L27). It gives the same gate mapping and F/V pairs as B-221a (L33-53). "A Mirror gate may involve return toward the shared reference, comparison/crossover, and phase/orientation update" (L58).
- Equations: `M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> M1 ...` (L94). The file has no M²=-I operator. That form appears only in B-221 L148, attributed to C-301.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: a VTC hardware gate "may use ... magnetic coupling, differential sensing" (L74). This is an implementation detail only, with no physics claim.
- Open / parked / not-set items: none.
- Conflicts: none against the canonical rules. Internal: B-221 (L148-149) and C-308 (L19, L49) attribute to C-301 a rotational Mirror operator with 4π closure, but the current C-301 file defines no such operator. That spin-half topology chain is no longer present in its stated source.

## C-302 — Momentum   (`Nodes/C-302_Momentum.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: A-111, A-112 (L15).   Downstream / cites: C-303 (L16).
- Core claim: "Higher k => higher p. p proportional to k" (L21-23).
- Equations: `p ~ hbar * k` ("standard relation, not yet derived from One-Wave geometry alone") (L27).
- Point / Path / Field role: none stated. This is linear momentum only.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: CCD-01. The derivation of S_min = hbar is blocked pending D-405 Harmonic Shell geometry (L31-35).
- Conflicts: none.

## C-303 — Kinetic Energy   (`Nodes/C-303_Kinetic_Energy.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: C-302 (L15).   Downstream / cites: C-304, C-305, C-309 (L16). Cross-references Book 1 Ch14 and A-115 for the Mass-Effect program (L34).
- Core claim: "K proportional to v^2" (L22).
- Equations: `K = (1/2)*m_SM*v^2` (L25); `K_OW = (1/2)*m_eff*v^2`, where m_eff is measured Mass Effect "not yet derived from bounded geometry" (L28).
- Point / Path / Field role: none stated. This is translational only, with no rotational KE term.
- Magnetism / gravity / rotation link: none stated (mass via A-115).
- Open / parked / not-set items: m_eff is not derived (L33).
- Conflicts: none.

## C-304 — Potential   (`Nodes/C-304_Potential.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: A-102, A-105 (L15).   Downstream / cites: C-305 (L16).
- Core claim: "Potential energy is the stored integral of the restoring response" (L32).
- Equations: `V(x) = integral A(s) ds from 0 to x` (L25); `A(x) = alpha*x`, `V(x) = (1/2)*alpha*x^2` (L29-30).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: it inherits A-105's Yellow operator form (L35).
- Conflicts: none.

## C-305 — Work   (`Nodes/C-305_Work.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: C-304, A-105 (L15).   Downstream / cites: C-306, C-307 (L16).
- Core claim: "Force applied over displacement produces work" (L19).
- Equations: `W = integral F(x) dx from x_0 to x_1` (L24); `F = R_OW = -A(nabla_psi)`; `W = integral (-A(nabla_psi)) dx` (L26-27).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: it inherits A-105's Yellow status (L30).
- Conflicts: none.

## C-306 — Torque   (`Nodes/C-306_Torque.md`)
- Gate / lifecycle: GREEN (foundation) / YELLOW (math weak); lifecycle HELD (L5-8).
- Upstream: C-305, A-104 Gradient (L15).   Downstream / cites: C-307, C-320 Magnetic-Compression Path Coupling, D-413 Ground Lattice Orbital-Restoring Simulation, D-416 Planetary Rotation-Magnetic Coupling Test Matrix (L16).
- Core claim: "off-center displacement -> rotational preference -> tau" (L22). "C-306 remains the authority for converting an off-center distributed response into torque; C-320 does not redefine torque" (L33).
- Equations: `tau = r x F` (L25); `tau = r x (-A(nabla_psi))` (L31).
- Point / Path / Field role: owns torque, the agent that changes point rotation. It does not separate point torque from path or orbital torque. r is "the displacement vector from the rotation axis" (L27).
- Magnetism / gravity / rotation link: "For the magnetic/compression bridge, C-320 may supply a distributed path-weighted restoring response" (L33). C-320/D-416 use C-306 "as a mechanics control, not as evidence that magnetic coupling exists" (L38).
- Open / parked / not-set items: full derivation from One-Wave field geometry is deferred; parked for refinement (L36-39).
- Conflicts: possible tension. L33 lets C-320's path-weighted restoring/compression response (the A-115 gravity-side quantity per C-311 L57) supply a torque. Canonical says "Gravity does not start or affect point rotation" and treats magnetism as the point-opening channel. C-306 does not say whether this torque acts on point rotation or only on the path/orbit. This needs clarification and is flagged as a tension, not a confirmed contradiction.

## C-307 — Angular Momentum   (`Nodes/C-307_Angular_Momentum.md`)
- Gate / lifecycle: GREEN (foundation) / YELLOW (endpoint); ACTIVE.
- Upstream: C-306 (L15).   Downstream / cites: C-308, C-320, D-416 (L16).
- Core claim: "Rotation has angular velocity omega. Mass distribution gives rotational inertia I. Angular momentum is their product." (L19-21). "C-320/D-416 add no exception to angular-momentum bookkeeping" (L41). D-416 "treats angular momentum as a control quantity rather than allowing a magnetic-lock story to overwrite mechanics" (L36).
- Equations: `L = I * omega` (L23, L26); `L = integral r x (rho * v) dV` (L29).
- Point / Path / Field role: owns L = I omega (point rotation). It does not split point, path and field. The continuous form ∫ r × (ρ v) dV (L29) counts any circulating field velocity, path circulation included, as L.
- Magnetism / gravity / rotation link: "C-320 may produce a candidate distributed torque through path-weighted restoring response, but any resulting spin/orbit evolution must still obey the angular accounting here" (L36).
- Open / parked / not-set items: endpoint derivation; the formal relation between L and C-308's spin-half topology (L39-40).
- Conflicts: possible tension. The canonical rule (G-769) says Path rotation, the ride, carries no L. C-307 L29 defines L as a volume integral of r × ρv with no exclusion of path or circulation motion, and L36 groups "spin/orbit evolution" under one accounting. Bookkeeping for G-749 versus G-769 is not stated here. L36 (C-320 path-weighted restoring response as a torque source on spin) also carries the same gravity-on-point-rotation tension as C-306 L33. The file adds no L exception, which is consistent.

## C-308 — Spin-half   (`Nodes/C-308_Spin_half.md`)
- Gate / lifecycle: GREEN / ACTIVE; "internal topology chain valid" (L8).
- Upstream: C-301, B-205 Mirror, C-307 (L15).   Downstream / cites: all spin-related object nodes in the Books (L16).
- Core claim: "Spin-half emerges from the 4*pi closure produced by repeated Mirror crossings" (L19). "The state picks up a sign under 2*pi rotation and returns to itself under 4*pi rotation" (L38).
- Equations: `m -> -m` (L25); `(theta, m) -> (theta + 2*pi, -m)`, `psi(theta + 2*pi) = -psi(theta)` (L29-30); `psi(theta + 4*pi) = psi(theta)` (L34). Neutron two-shell model: `R+ = 0.7331 fm`, `R- = 0.8409 fm`, `sigma = 0.210 fm` (L42-44).
- Point / Path / Field role: spin-half topology of the point (sign under 2π). It is not tied to L = I ω (open, per C-307 L40).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: CCD-02 parks the psi_C/psi_E ratio and the kappa+/- stiffness pending E_opp(R) (L52-55).
- Conflicts: none against the canonical rules. Internal: its upstream C-301 no longer contains the Mirror crossing operator `m -> -m` with 4π closure (see C-301). C-301 now defines the Mirror gate as read/compare/reflect in a 6-gate cycle.

## C-309 — Friction Limit / Propagation Ceiling   (`Nodes/C-309_Friction_Limit.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Propagation Constraint / Damping Formalization.
- Upstream: A-109, A-114 Dispersion Relation, C-303 (L15).   Downstream / cites: C-310, C-318 Four-Interaction Mass-Effect Response, Book 1 Ch7, E-509, E-533 (L16). Also cites A-115 and C-322 (L90-91).
- Core claim: it separates memory damping (γ) from the maximum propagation speed. "Neither damping nor propagation status generates inertia" (L25). The Canonical Prohibition bars deriving Mass Effect from propagation speed, damping, localization share, a local/transport ratio or the friction limit (L96-107).
- Equations: `M_i=(1-γ)Δψ_i^n` (L32); `c_lat = v_max = sqrt(β_max) Δx/Δt` (L46-47); `ω(0)=0` (L55); candidate `dτ/dt = T(v,Ξ)`, `T(v,0) ?= sqrt(1-v^2/c^2)` (L68-79). The TeX in L68-79 is corrupted (missing backslashes).
- Point / Path / Field role: none stated directly.
- Magnetism / gravity / rotation link: none stated. Mass Effect comes from "the work required to carry and rebuild the complete four-interaction recurrence" (L58, C-318).
- Open / parked / not-set items: γ(s) and β(s) at nuclear scale; the regime that matches measured c; keeping transport separate from the C-318 tensor (L126-128). Phase 6B validation is claimed for the dispersion relation and γ/β independence (L109-120).
- Conflicts: none against the canonical rules. "resistance = mass / organization" is not contradicted, because C-309 only denies damping and propagation as inertia sources. Formatting defect: L68-79 has broken LaTeX.

## C-310 — Resistance Field   (`Nodes/C-310_Resistance_Field.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Resolution / Formalization Node.
- Upstream: C-309, A-109, A-108 (L24).   Downstream / cites: B-207 Threshold / Break (L25).
- Core claim: "Resistance is the field's tendency to preserve identity against perturbation" (L28-29). It is distinct from Friction (C-309, γ damping) and from Restoring Response (A-105, active force) (L34-41). It does not reduce to A-108, which is binary and local, while Resistance is graded and global (L54-69).
- Equations: A-108's condition `x·A(x)>0` near x=0 (L55-56); placeholder `H(R) = -(R - R_opt)^2 + H_max` (L80), flagged as "NOT derived" (L78-87).
- Point / Path / Field role: none stated in Point/Path/Field terms. Resistance is identity preservation, an inverted-U trade-off.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: R_opt is undefined; the graded form is not derived; the distinction from A-105 is in prose only (L102-119).
- Conflicts: definitional divergence, not a stated contradiction. The canonical bound-lattice rule defines "resistance = mass / organization". C-310 defines Resistance as identity preservation with a parabolic health trade-off (L28-41, L80) and never mentions mass or organization. Two different "resistance" quantities exist and nothing reconciles them.

## C-311 — Electric-Magnetic Duality   (`Nodes/C-311_Electric_Magnetic_Duality.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Phase 6B validation dated 2026-10-03 (L8-10).
- Upstream: B-206b Four Views (pressure cushion), A-104 Gradient (L24).   Downstream / cites: C-319 Magnetic Lattice Reorganization, C-320, Book 1 Ch4, Ch7, Ch9, Ch12 (Gravity), Ch13 (L25).
- Core claim: "Electric and magnetic fields are not two separate fields. They are the radial and rotational projections of ONE pressure field P_c" (L28-30). "C-319 and C-320 are the required bridge for any claim connecting magnetism to lattice organization, gravity/compression, orbital response, or magnetic memory. Do not jump directly from C-311 to 'magnetism equals gravity.'" (L60).
- Equations: `E_vec ~ ∇P_c`, `B_vec ~ ∇×P_c` (L32-33, L44); `P_c = beta * DeltaE / V_c` (L42-43); `|E_vec| = c * |B_vec|` (deferred) (L48). Phase 6B forms: `E ~ ∇(∇·ψ)`, `B ~ ∇×(∇×ψ)`, Faraday `∇×E = -∂B/∂t` (L80-82).
- Point / Path / Field role: the Field. B is the rotational (curl) projection of the single pressure field and E is the radial (gradient) projection. "A moving charge adds the rotational component from its motion" (L35-36). It does not tie field curl to point rotation or L.
- Magnetism / gravity / rotation link: chain `B-206b -> C-311 -> C-319 (rotational magnetic state reorganizes directional lattice paths) -> C-320 (reorganized paths weight A-115 restoring/compression response) -> D-413/D-416` (L54-58). C-319/C-320 "own the magnetism-to-lattice-to-gravity hypothesis; their presence does not validate that hypothesis" (L68-69).
- Open / parked / not-set items: deriving |E| = c|B|; the remaining Maxwell equations (Gauss, Ampere); the C-series vs E-series placement question (L63-74, L90-94).
- Conflicts: none against "magnetism does not become gravity", because L60 forbids that jump. Internal and mathematical issues: P_c is defined as a scalar pressure (L42-43), so `∇×P_c` (L33, L44), the curl of a scalar, is undefined. The Phase 6B forms (L80) use a vector ψ, which differs from the Definition. C-311 is also silent on "Magnetism opens the point (dL/dt=0 open / -gamma L closed)". That is not a contradiction, but the point-coupling of B is absent here.

## C-312 — Hierarchical Sensor-Control Architecture (Android Body)   (`Nodes/C-312_Hierarchical_Sensor_Control_Architecture.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Engineering / Applied Control System Node.
- Upstream: A-109, B-206b (L28).   Downstream / cites: Android_Body book, Books/Proposed_Android_Brain, G-719 (L29). Also cites B-213 Access Line (L79) and Books/Proposed_One_Wave_Consciousness (L22).
- Core claim: a four-level control hierarchy (sensor units, local aggregation, positional chains, central coordinator) that makes "NO verified claim about consciousness" (L14-25, L32-58). 3:1 fan-in repeats at every level (L92-95). The coordinator modulates and does not dictate; overrides are targeted, not broadcast (L107-131).
- Equations: none ("None derived yet", L71). Ratios: 3:1 fan-in, coordinator at half the base frequency.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the hex-L position encoding; command latency; whether 4 levels are needed; the MOSFET circuit link (L86-90, L133-142).
- Conflicts: none against the canonical rules. Internal contradictions: (1) L134-135 Yellow Audit says "Fan-in/fan-out ratios undefined at every level" but L92-95 says 3:1 is confirmed at every level. (2) L100 says the coordinator samples at "HALF the base signaling frequency", but L101-102 says the base completes "three signaling cycles" per oversight cycle, which is a 1/3 ratio.

## Slice summary

### (a) Nodes in this slice that bear on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, or lattice organization/locking
- C-306 Torque: owns `tau = r x F` / `tau = r x (-A(∇ψ))`, the authority for converting an off-center distributed response into torque. It is the mechanics control for C-320/D-413/D-416 and does not separate point torque from path torque.
- C-307 Angular Momentum: owns `L = I omega` and `L = ∫ r x (rho v) dV`. It adds no exception for C-320/D-416. There is no Point/Path split; the L of the continuous form includes circulation.
- C-308 Spin-half: the point spin topology, sign under 2π and identity under 4π, from Mirror crossings. Its relation to L = I omega is not formalized.
- C-311 Electric-Magnetic Duality: the Field. E is the gradient projection and B the curl projection of one pressure field. It routes magnetism to lattice to gravity only through C-319/C-320 and forbids "magnetism equals gravity".
- C-309 Friction Limit: damping and propagation ceiling. It explicitly does not generate inertia or Mass Effect; Mass Effect is routed to C-318/A-115.
- C-310 Resistance Field: resistance as identity preservation (graded, inverted-U placeholder). It is not mass/organization.
- C-303 Kinetic Energy: `K_OW = (1/2) m_eff v^2`. m_eff is not derived and is referred to A-115 and Book 1 Ch14.
- C-302 Momentum: `p ~ hbar k`, linear only. CCD-01 is parked.
- C-304 / C-305 Potential and Work: the stored integral and the work of the restoring response `-A(∇ψ)`. They feed C-306 and C-307.
- C-301 Mirror Gate / B-221a: Mirror is a read/reflect gate position in the 6-gate cycle. Hardware may use magnetic coupling (implementation only).
- B-221 Six Recursive Steps: LOOP candidate 2 is a rotational Mirror operator (M²=-I, 4-cycle closure). This is a state-space rotation, not physical point rotation.
- B-223 Three Moves: the ternary signed move may be relabeled CCW/Hold/CW. This is a label only.
- B-220 Scale Layer: scale containment and γ(s)/β(s) scaling of the lattice update rule. These relate to the lattice but not to locking.

### (b) Conflicts found
1. C-306:L33 and C-307:L36 allow C-320's path-weighted restoring/compression response (the A-115 gravity-side quantity, per C-311:L57) to supply torque on "spin/orbit evolution". This is a tension with "Gravity does not start or affect point rotation" and with "magnetism opens the point". The files do not say whether that torque acts on point rotation or only on path/orbit.
2. C-307:L29 and L36 give one L accounting, `∫ r x (ρ v) dV` covering "spin/orbit", with no separation of Point L (G-749) from Path (G-769). The canonical rule says the path or ride carries no L.
3. C-310:L28-41 and L80 define "Resistance" as identity preservation with a parabolic health function. The canonical rule defines resistance = mass / organization. The two are not reconciled.
4. C-311:L33 and L44 take `∇×P_c` of a scalar P_c (L42-43), which is mathematically undefined. The Phase 6B forms (L80) use a different vector-ψ definition.

Internal (non-canonical) inconsistencies:
- B-221:L22 uses the order Begin/Move/Hold/Build/Break/Loop. B-221a:L25-30 and C-301:L33-38 use BEGIN/BUILD/HOLD/BUILD/BREAK/LOOP.
- B-221:L148 and C-308:L19,L49 attribute a rotational Mirror operator with 4π closure to C-301, but the current C-301 defines no such operator.
- B-220:L39 and B-222:L16 cite "B-225 Field Cycle", but B-225 is now "Five-Level Modulation Compatibility".
- B-222 still frames the choice as Compression↔Expression, while B-224:L53 says this was corrected to Everything/Nothing.
- C-312:L134-135 says ratios are undefined, against L92-95 (3:1 confirmed). C-312:L100 says "half" frequency, against L101-102 (3 cycles per oversight cycle).
- C-309:L68-79 has corrupted LaTeX.

### (c) Cross-references outside this slice that matter for point rotation or magnetism
- C-319 Magnetic Lattice Reorganization (C-311:L25,L56,L60,L68,L93)
- C-320 Magnetic-Compression Path Coupling (C-306:L16,L33,L38; C-307:L16,L36,L41; C-311:L25,L57,L60,L94)
- D-413 Ground Lattice Orbital-Restoring Simulation (C-306:L16; C-311:L58)
- D-416 Planetary Rotation-Magnetic Coupling Test Matrix (C-306:L16,L38; C-307:L16,L36,L41; C-311:L58,L94)
- A-115 Mass Effect / unified field and boundary resistance (C-303:L34; C-309:L90; C-311:L57)
- C-318 Four-Interaction Mass-Effect Response (C-309:L16,L50,L89,L128)
- C-322 125 GeV Mirror-Gate pressure-work threshold (C-309:L91)
- E-533 Superfluid Transport Time Dilation and E-509 Propagation Limit (C-309:L16,L62)
- B-205 Mirror (C-308:L15), the source of the spin-half Mirror crossing
- B-206b Four Views, the pressure cushion P_c (C-311:L24,L42)
- A-104 Gradient (C-306:L15; C-311:L24); A-105 Restoring Response (C-304, C-305, C-306)
- Book 1 Ch12 Gravity and Ch13 Electricity/Magnetism (C-311:L25); Book 1 Ch14 Mass Effect (C-303:L34)
- E-507 Scale-Invariant Loop (B-220:L21)
- D-405 Harmonic Shell (CCD-01, C-302:L33); CCD-02 proton boundary (C-308:L52-55)
