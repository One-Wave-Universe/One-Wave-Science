# Ledger 06 — slice 06 (27 files, all read in full)

## G-726 — Dual Dream Engine — Programmed 2D Ternary Homeworld   (`Nodes/G-726_Dual_Dream_Engine_2D_Ternary_Homeworld_Mega_City.md`)
- Gate / lifecycle: GREEN / PROPOSED_BUILD; detail "GREEN (role separation) / BROWN (Homeworld implementation)" (L5-8).
- Upstream: none listed by ID (refers to M4/Dream/Mind architecture, L24). Downstream / cites: none by ID.
- Core claim: "The Homeworld Dream Engine is **not an Administrator** ... It is a non-cognitive programmed simulation." (L16-17). "The world has **two spatial dimensions**. `3` refers to its ternary local state" (L19-20). Native gate `3 > 1(0)1 < 6`, six directed neighbors (L57-61).
- Equations: `m in {-1,0,+1}` (L35); `3 > 1(0)1 < 6` (L59).
- Point / Path / Field role: Each hierarchy level uses PPF: Point = site/building/junction/district center; Path = road/rail/utility/route; Field = neighborhood influence, resources, weather, boundary (L80-85). WorldCell2D carries separate `point_state, path_state, field_state` (L49). No rotation content.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: whole Homeworld implementation BROWN; minimum build list L123-133.
- Conflicts: none.

## G-727 — Two Choice, Three Move, and Recursive Point–Path–Field   (`Nodes/G-727_Two_Choice_Three_Move_and_Recursive_PPF.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS ("YELLOW finite logic / proposed dynamics", L14).
- Upstream: B-208, B-216, B-222, B-223, B-224, D-408, D-409, D-410 (L15). Downstream / cites: `six_route_logic.py`, Updated 43, MATH_ATTACK_MAP_UPDATED_43 (L62-65).
- Core claim: YES (1,0) / NO (0,1); Ground (0,0) = no committed choice; (1,1) = conflict; DOWN/HOLD/UP; `2 x 3 = 6` (L19-21). Five commitment amplitudes are not another choice axis (L23-25).
- Equations: Mirror-Gate recurrence `3 > 1(0)1 < 6` 2D, `6 > 1(0)1 < 12` 3D, `12 > 1(0)1 < 24` 4D recurrence (L44-46); `a=a_Gray+delta_a_OW` (L57).
- Point / Path / Field role: "keep three kinematic roles distinct: Point rotation: local/intrinsic orientation; Path rotation: curvature or circulation of the transported center; Field rotation: circulation of the enclosing carrier/boundary." (L29-33). "Any Point, Path, or Field may contain lower-scale Point–Path–Field states. The solver must therefore carry frame transforms and receipts across nesting boundaries instead of replacing all rotations with one angular velocity." (L35-37). Consistent with three-rate rule and transport-first nesting; does not itself state L = I omega.
- Magnetism / gravity / rotation link: Orbital guardrail — Newtonian/relativistic controls retained; corrections must vanish to Gray limit and not degrade conserved quantities (L55-58). No magnetism.
- Open / parked / not-set items: map from route/phase/history to five amplitudes "remains to be derived" (L23-25); count matching "not a derivation" (L49-51).
- Conflicts: none.

## G-728 E1 STAMP — Official E1 split stamp   (`Nodes/G-728_E1_STAMP.md`)
- Gate / lifecycle: artifact, ACTIVE (2026-09-05).
- Upstream: G-728 (parent). Downstream / cites: G-746 (L12, L20).
- Core claim: "GREEN / exact for the assumed scalar PDE: temporal characteristic, ω±(k), under/critical/overdamped boundaries, real-ω k(ω), ℓ_att, analytic v_g." (L14). "YELLOW: lattice-branch identity, Field/Void matrix, coupling, origin of (γ,c_eff,ω0)." (L16). "E5 YELLOW, blocked by matrix-as-physics, open-system energy, independent I0, no-125/no-Hoyle closure." (L18).
- Equations: none beyond symbols.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: E5; origin of γ, c_eff, ω0.
- Conflicts: none.

## G-728 — Mathematics Attack Laundry List   (`Nodes/G-728_Mathematics_Attack_Laundry_List.md`)
- Gate / lifecycle: BROWN / ACTIVE_HYPOTHESIS; "Tasks inherit the gate of their evidence" (L15).
- Upstream: Updated 43, G-727, A-114, B-216, C-313, C-318, D-408–D-410, E-523, G-713, G-724–G-727 (L16); authority MATH_ATTACK_MAP_UPDATED_43 (L17). Downstream / cites: G-729, G-730, G-731, G-733, G-734, G-738, G-739, G-769 (C3), B-226 (via G-732).
- Core claim: every checked item needs equations+units, code, raw results, strongest control, failed cases, Brick recommendation (L21-28). "A matching number or visual pattern alone is not a derivation." (L30-31).
- Equations: PPF schema `X_s={P_s,gamma_s,F_s;X_(s-1,1),...,X_(s-1,n)}` (L89); `a_i=a_Gray,i+delta_a_OW,i` (L180).
- Point / Path / Field role: C2 (open) "Point rotation: derive intrinsic/local orientation and its carried angular-momentum receipt" (L90-91). C3 (checked) "Path rotation: kinematic turning is G-769. A closed hexagon turns 2π. The receipt has no L. Not an orbit solution." (L92). C4 (open) "derive Field circulation/curl and its boundary conditions without replacing it with Path rotation" (L93-94). C8 "Nested rotation ledger: prevent intrinsic, orbital, frame, and enclosing-Field rotations from being counted twice" (L101-102). C10 PPF ablation: remove Point, Path, Field rotation one at a time (L105-106). H8 nested orbital PPF: body-internal PPF vs body Path in system Field (L190-191).
- Magnetism / gravity / rotation link: G1-G6 magnetic hardware (LLG cell, DC bias + quadrature AC drive, magnon transport, MTJ/ISHE readout) (L162-171) — device-level, no point-rotation claim. H3 "acceleration is bookkeeping, not a declaration that a fundamental force exists" (L180-181). H10 mechanism ablations include "core rotation" and "EM shell" as candidate orbital mechanisms (L194-195) — listed for test only. I2 galaxy "rotation" = rotation curves (Path).
- Open / parked / not-set items: B4-B6, C1-C2, C4-C10, D1-D8, E1-E7, F1-F7, G1-G6, H1-H13, I1-I7, J1-J6, K1-K5 open per list (overlay updates C1, D1, E1).
- Conflicts: none against canonical rules. Watch: H10 "core rotation" as orbital mechanism (L195) must not imply gravity acting on or from point rotation without derivation; currently only an ablation item. Internal: C3 marked [x] (L92) while `G-728_PROGRESS_OVERLAY.md:26` says "C2–C10 ... remain open" — overlay is stale for C3.

## G-728 PROGRESS OVERLAY — G-728 progress overlay (2026-09-05)   (`Nodes/G-728_PROGRESS_OVERLAY.md`)
- Gate / lifecycle: artifact, ACTIVE.
- Upstream: G-728. Downstream / cites: G-743 (ppf_schema), G-746, G-745, A-114.
- Core claim: C1 PPF schema PARTIAL Yellow; D1 2D hex graph PARTIAL Yellow; E1 SPLIT (GREEN for assumed scalar PDE, YELLOW for lattice identity); "A-114 general-gamma discrete quadratic is exact for that update rule" (L16-21). E5 still YELLOW; "G-745 quarantine stands" (L22).
- Equations: none.
- Point / Path / Field role: "Rotations C2–C4 and plots still open" (L16).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: B4–B6, C2–C10, D2–D8, E2–E4, E6–E7, F–K open (L26).
- Conflicts: internal only — L26 lists C3 as open, but G-728 laundry list L92 marks C3 done (G-769). Overlay predates/ignores G-769 closure.

## G-729 — Mirror Operator for the Three Mirror Gates   (`Nodes/G-729_Mirror_as_Continuous_Phase_with_Six_Route_Projection.md`)
- Gate / lifecycle: YELLOW / ACTIVE; "physical carrier remains unresolved" (L8).
- Upstream: B-205, B-208, B-221a, B-222, C-301, G-727, G-728 (L15). Downstream / cites: `mirror_operator.py` + tests (L108-109).
- Core claim: "There are exactly three primitive Mirror-gate positions in the six-gate cycle: M1 -> A1 -> M2 -> A2 -> M3 -> A3" (L19-22). "Mirror is not a YES/NO swap and does not exchange Field and Void identities." (L27).
- Equations: `z = (x, v/omega)`, `z' = R(delta_phi) z`, preserves `x^2 + (v/omega)^2` (L34-42); half cycle `(x,v/ω)->(-x,-v/ω)` (L44); `M(choice, move) = (choice, -move)` (L53).
- Point / Path / Field role: none stated (phase rotation in oscillator phase space, not spatial rotation).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: phase per physical Mirror gate (L46); drive, damping, asymmetry, thresholds, phase slip (L88).
- Conflicts: none vs canonical. Internal tension: "3 Mirror + 3 Action = 6" primitive gates (L98-102) — G-740:225-233 declares this superseded for CELL_V1 hardware (logical sequence only).

## G-730 — History, Phase, and Hysteresis Commitment Map   (`Nodes/G-730_History_Phase_and_Hysteresis_Commitment_Map.md`)
- Gate / lifecycle: YELLOW / ACTIVE ("control mathematics / semantics comparison open", L14).
- Upstream: B-216, B-222, G-727–G-729 (L15). Downstream / cites: `commitment_map.py`.
- Core claim: five commitment states {-3,-2,0,+2,+3} are "derived readouts, not five primitive choices" (L19-27).
- Equations: `L(Delta_phi)=[1+cos(Delta_phi)]/2` (L37); `q_(n+1)=clip(r*q_n+g*b*m*d*L,-q_max,+q_max)` (L41); thresholds `partial_exit < partial_enter < full_exit < full_enter` (L59-60).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: b*m orientation semantics vs absolute-axis and energy-gradient models (L47-49); parameters are demo defaults (L79-82).
- Conflicts: none. Notational note: symbol `L` (L37, L41) is phase-alignment weight, not angular momentum L = I omega — collision risk only.

## G-731 — Ground, Center, and Coherent Hold Separation   (`Nodes/G-731_Ground_Center_and_Coherent_Hold_Separation.md`)
- Gate / lifecycle: YELLOW / ACTIVE ("finite classifier / physical thresholds uncalibrated", L14).
- Upstream: B-208, B-216, B-222, G-727–G-730 (L15). Downstream / cites: `ground_hold_classifier.py`.
- Core claim: Logical Ground, center residence, center crossing, movement Hold, turning-point Hold, YES/HOLD vs NO/HOLD, Coherent Hold "are not synonyms" (L19-31). "Logical Ground is outside the six committed routes." (L60). Logical Ground "does not claim that the physical Field or vacuum contains no energy" (L22-23).
- Equations: none (receipt field list L37-49).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: center width, speed width, phase-lock, energy, topology thresholds (L64-67).
- Conflicts: none.

## G-732 — Vortex Trial-Profile Diagnostic Repair   (`Nodes/G-732_Vortex_Trial_Profile_Diagnostic_Repair.md`)
- Gate / lifecycle: YELLOW / ACTIVE ("diagnostics / stationary bound mode open", L14).
- Upstream: A-107, B-226, G-727, G-728 (L15). Downstream / cites: `micro/vortex_diagnostics.py`.
- Core claim: analytic line-vortex dilation integrals; winding via wrapped phase increments; "The dilation minimum is necessary only along one variational direction. It is not proof of a stationary solution or stability" (L32-34). "The linear constant-coefficient equation has no nonzero localized square-integrable harmonic eigenmode on unbounded space." (L34-36).
- Equations: `I1=(5/2)pi^(3/2)sigma`, `I3=(35/4)pi^(3/2)/sigma`; at sigma=2, `lambda*=sqrt(7/8)` (L20-21).
- Point / Path / Field role: none stated explicitly (vortex winding/charge only).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: nonlinear/self-consistent coupling needed before B-226 recursion floor passes (L36-37).
- Conflicts: none.

## G-733 — Noise, Chatter, and False-Commitment Audit   (`Nodes/G-733_Noise_Chatter_and_False_Commitment_Audit.md`)
- Gate / lifecycle: YELLOW / ACTIVE ("deterministic audit / physical noise model open", L14).
- Upstream: B-216, G-730, G-731 (L15). Downstream / cites: `noise_hysteresis_audit.py`, `commitment_map.py`.
- Core claim: hysteresis reduces partial chatter (100% at σ=0.03, 68.52% at σ=0.12; table L30-36) but false full-entry probability at q=0.70 is 1.0 for σ≥0.05 (L46-52). "Hysteresis controls exits and re-entry chatter; it does not by itself validate a threshold excursion." (L55-56). Full commitment needs dwell, k-of-n, filtering, SPRT, or phase-coherent confirmation (L60-66).
- Equations: none (tables).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: B5 delay, correlated noise, quantization, first-passage (L77-78); Gaussian noise not claimed physical (L23-24).
- Conflicts: none.

## G-734 — Asymmetric Center-Origin Oscillator Reference   (`Nodes/G-734_Asymmetric_Center_Origin_Oscillator_Reference.md`)
- Gate / lifecycle: YELLOW / ACTIVE ("dimensionless mechanics / Field derivation open", L14).
- Upstream: B-208, B-216, B-222, G-729–G-733 (L15). Downstream / cites: `dynamics/asymmetric_oscillator.py`; G-735.
- Core claim: exact saddle-node fold; "This is a dimensionless gate-mechanics reference, not the fundamental One-Wave equation and not quark physics." (L46-47).
- Equations: `x_ddot+c*x_dot+a*x^3-b*x-h=u(t)`, `V(x)=a*x^4/4-b*x^2/2-h*x`, `c=2*zeta*omega_ref` (L19-20); `|h_fold|=2*b^(3/2)/(3*sqrt(3*a))` (L24); a=b=1 → 0.384900179 (L28); barrier 1/4 (L42). (Checked: correct.)
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: coefficients require derivation from Field model (L47-49).
- Conflicts: none.

## G-735 — Chapter-Driven Simulator Program   (`Nodes/G-735_Chapter_Driven_Simulator_Program.md`)
- Gate / lifecycle: BROWN / ACTIVE_HYPOTHESIS ("Active implementation authority", L14).
- Upstream: G-728, G-734, all current science chapters (L15). Downstream / cites: `simulators/chapter_registry.py` (23 chapters, Books 1, 2, 5) (L27-30).
- Core claim: route `chapter -> mechanism -> Gray control -> One-Wave extension -> engine -> receipts -> visual scene` (L23). "Micro is the only active implementation scale in this branch." (L54). "Gray/control evolution to remain unchanged when the One-Wave contribution is zero" (L66-67).
- Equations: none.
- Point / Path / Field role: requires "nested PPF receipts" for proton knot simulator (L80-81); no rotation rules.
- Magnetism / gravity / rotation link: Galactic scene "rotation, tidal environment, arms, wake hypotheses" planned (L89); planetary scene "Newton/relativity baseline plus declared One-Wave terms" (L88). No point-rotation/magnetism rule.
- Open / parked / not-set items: stationary-vortex persistence, B-226 floor, noise analysis, proton binding, all higher-scale simulators (L71-75); active freeze at Micro (L79-82).
- Conflicts: none.

## G-736 — Standard Model Interpretation Overlay for Micro Simulators   (`Nodes/G-736_Standard_Model_Interpretation_Overlay_for_Micro_Simulators.md`)
- Gate / lifecycle: YELLOW / ACTIVE ("visualization contract / mechanism mapping open", L14).
- Upstream: G-732, G-735, Book 1 Chapters 1–6 and 13–15 (L15). Downstream / cites: `micro/proton_sphere_overlay.html`.
- Core claim: three layers — One-Wave mechanism, Gray interpretation, combined view (L21-27). R/G/B are QCD bookkeeping labels, not literal colors (L38-42).
- Equations: none.
- Point / Path / Field role: Proton overlay displays "internal Point rotation, carried Paths, and enclosing spherical Field phase" (L34) — three roles kept separate. Mechanism layer lists "vortex cores, Paths, enclosing Field" (L21-22).
- Magnetism / gravity / rotation link: none stated; spin is listed among observables a PDE engine must preserve (L49-50).
- Open / parked / not-set items: SU(3) derivation open (L41-42); current motion is "kinematic visualization driven by the validated point-vortex control, not a 3D QCD calculation" (L46-48).
- Conflicts: none.

## G-737 — Synchronized Dual-State Mind — Fast Router and Consequence Feedback   (`Nodes/G-737_Synchronized_Dual_State_Mind_Router_Feedback.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS; "computational architecture; not proof of consciousness or literal neuroanatomy" (L8).
- Upstream: none listed. Downstream / cites: none.
- Core claim: compressive + expressive reciprocal state machines synchronized by fast router and consequence feedback; "Neither ... is permitted to erase the other" (L16-25). Governing rule "Compress without silencing. Express without losing coherence. Route quickly. Correct through consequence." (L55-56).
- Equations: `r_t=R(s_t,m_t,f_{t-1})`; `c_{t+1}=C(c_t,r_t)`, `e_{t+1}=E(e_t,r_t,c_{t+1})`; `a_t=G(c_{t+1},e_{t+1})`, `f_t=o_t-ô_t` (L29-39).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: six required tests (L64-71); failure conditions (L75-77).
- Conflicts: none.

## G-738 — Center Geometry Classification and Receipt   (`Nodes/G-738_Center_Geometry_Classification_and_Receipt.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Brick Yellow (L81).
- Upstream: G-731 (L27-28), closes G-728 B2 (L77). Downstream / cites: `dynamics/center_geometry.py` (via G-728).
- Core claim: five center structures (point residence, finite band, crossing section, limit-cycle section, slow-manifold candidate) (L19-25); "a fast center crossing is therefore never mislabeled Hold" (L53-54); "does not decide that all One-Wave systems share one center type" (L77-78).
- Equations: crossing when `x_i x_{i+1}<0`; `t_× = t_i + (-x_i)/(x_{i+1}-x_i) (t_{i+1}-t_i)` (L45-50; text has LaTeX escape corruption: `\rho`, `\times`, `\frac`, `\le` rendered as broken characters at L38-53).
- Point / Path / Field role: none stated (center of a trajectory coordinate, not Point rotation).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: physical center type simulator-local (L78-79).
- Conflicts: none. Formatting defect L38-53 (escape-sequence corruption).

## G-739 — Six-Gate Mirror-Action Trajectory Extraction   (`Nodes/G-739_Six_Gate_Trajectory_Extraction.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Brick Yellow (L94).
- Upstream: B-221a, C-301 (L45). Downstream / cites: `dynamics/six_gate_extractor.py` (via G-728 B3).
- Core claim: "The six process steps are the six gates" BEGIN=M1, BUILD=A1, HOLD=M2, BUILD=A2, BREAK=M3, LOOP=A3 (L16-25). "Unclassified is an audit result, not a seventh gate." (L76). Gate 6 feeds next Gate 1, not Gate 7 (L90).
- Equations: `dot(E)_i = (E_i - E_(i-1)) / (t_i - t_(i-1))` (L62).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: "does not prove a universal physical mechanism" (L92).
- Conflicts: none vs canonical. Internal tension with G-740:225-233 (see G-729).

## G-740 — Field/Void Ternary and Quadratic Command Routing   (`Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md`)
- Gate / lifecycle: GREEN / ACTIVE_HYPOTHESIS; "Routing contract projected onto three physical bidirectional A/B/C mirrors" (L8).
- Upstream: Algorythm-Zer0 (owns universal primitives, L16-18). Downstream / cites: G-741, G-743 (cites G-740 as authoritative).
- Core claim: "FIELD = active interactions / VOID = unexpressed potential"; shared reference "is not a third polarity" (L22-27). "CELL_V1 uses exactly three physical bidirectional Mirror axes" A±, B±, C± producing six directed edge interfaces (L31-39). M1..A3 is "a logical/receipt sequence only" (L47). "The return is not a reset." (L71). "`HOLD` is active balance, not absence." (L99). Ground outside six-route set (L97).
- Equations: `2 x 3 = 6` route addresses (L92-94).
- Point / Path / Field role: none stated in PPF sense (Field here = Field/Void semantic polarity, not Field curl).
- Magnetism / gravity / rotation link: candidate stateful carriers include "hysteretic magnetic, spintronic/magnetoresistive" (L181) — hardware only.
- Open / parked / not-set items: exact variables, weights, thresholds, biological correspondence (L146); three-way Override fan-out experimental (L208).
- Conflicts: none vs canonical. Internal: L225-233 declares "3 Mirror gates + 3 Action gates = 6 physical gates" superseded for CELL_V1 — tension with G-729:98-102, G-739:33,85 (those say six primitive gates; G-740 scopes to hardware).

## G-741 — Crazy Town — Balanced-Rail Nested-Loop Physical Build Proposition   (`Nodes/G-741_Crazy_Town_Balanced_Rail_Nested_Loop_Build_Proposition.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS; "unbuilt ... no demonstrated computing, actuator, or biological equivalence" (L8).
- Upstream: G-740 (vocabulary). Downstream / cites: G-743, G-744 (later stages).
- Core claim: "This node is an experiment plan, not a claim that the circuit has been built or shown to compute." (L18). Clockwise flat edges `A+ -> B+ -> C+ -> A- -> B- -> C-`; three physical bidirectional mirrors (L25-32). Build stack P0..R1 (L66-78). "DC does not spontaneously become AC" (L122).
- Equations: `b∈{-1,+1}, d∈{-1,0,+1}, 2×3=6` (L50); `v_state = v_signal - V0` (L85); `Q_up=(Direction,Phase,Strength,Reference)` (L184).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "recoverable inductive/magnetic energy is steered back to the controlled DC reservoir" (L102). "If a rotating magnetic field is claimed, the phase relationship producing rotation must be measured rather than inferred from the existence of AC alone." (L126). Motor torque behavior experimental (L146). Engineering-level only; no point-rotation / L claim.
- Open / parked / not-set items: entire build unmeasured; 15-step staged experiment (L267-281); stateful element open (L173).
- Conflicts: none.

## G-742 — Nonverbal Loop Continuity and Reconstructable Language Adapter   (`Nodes/G-742_Nonverbal_Loop_Continuity_and_Language_Adapter.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS; "not evidence for an afterlife or substrate-independent cognition" (L8).
- Upstream: none by ID. Downstream / cites: G-744 artifact (must not replace G-742).
- Core claim: "language unavailable ⇏ self-loop unavailable" (L22). Testimonial reports "used only to generate failure tests" (L25-28). Sensory-dark condition, not sleep/death/Void identity (L69-70).
- Equations: `N_t=(R_t,F_t,V_t,D_t,P_t,S_t,L_t,C_t,I_t)` (L47); `(audio token, N_t, human response, consequence) -> word binding` (L76-78).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: seven required experiments (L97-110).
- Conflicts: none. Notational: `L_t` = lifecycle state (L51), not angular momentum.

## G-743 (artifact) — PPF Schema and 2D Hex Graph Trail   (`Nodes/G-743_PPF_Schema_and_2D_Hex_Graph.md`)
- Gate / lifecycle: artifact ACTIVE; Brick Yellow (L12).
- Upstream: G-728 C1, D1; D-408. Downstream / cites: `ppf_schema.py`, `hex_lattice_graph.py`, tests (5 + 7).
- Core claim: implements `X_s={P_s, gamma_s, F_s; children}` with frames `{ground, local, path}` (L18); hex graph for `3 > 1(0)1 < 6` (L19). Seven-cell edge count 12, Laplacian row sums 0, λ_min=0 (L24-27).
- Equations: schema above; Laplacian receipts.
- Point / Path / Field role: "Schema nesting is not rotation physics." (L31). Next: "C2 Point rotation; C3 Path circulation" (L35).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: C2-C10, D2-D8, Gray-control plots (L14).
- Conflicts: none vs canonical. Internal: duplicate ID G-743 shared with the quadrature-hardware node; L35 lists C3 as next though G-728:92 marks it done (G-769).

## G-743 — Proven Quadrature Rotating-Field Hardware — Views Up / Actions Down   (`Nodes/G-743_Proven_Quadrature_Rotating_Field_Views_Up_Actions_Down.md`)
- Gate / lifecycle: GREEN / PROPOSED_BUILD; "GREEN (external hardware principles) / YELLOW (One-Wave integration mapping)" (L8).
- Upstream: G-740 ("remains authoritative", L203). Downstream / cites: G-744; external refs Analog Devices, Microchip AN1307, Oriental Motor (L331-338).
- Core claim: three-winding = fast ternary reflex; resolver/quadrature sensor = Views UP; two-phase sine/cosine stator = Actions DOWN; "Override never becomes a fourth ternary state." (L367-374). "This node does **not** claim that any established technology proves the full One-Wave architecture." (L39-40).
- Equations: `SINE ~ sin(theta)`, `COSINE ~ cos(theta)` (L51-52); `I_A = I*sin(theta_cmd)`, `I_B = I*cos(theta_cmd)` (L101-102); "3 physical mirrored structures x 2 traversal orientations = 6 logical positions" (L248-250).
- Point / Path / Field role: none stated in PPF sense.
- Magnetism / gravity / rotation link: rotating magnetic field vector produced by quadrature drive; resolver reads rotating magnetic relation (L45-57, L93-106). Engineering electromagnetics only; no L, no point spin, no gravity.
- Open / parked / not-set items: Hold vs counter-action arbitration under Override is a bench question (L192-195); full cross-layer mapping untested (L343-344).
- Conflicts: none. Internal: duplicate node ID G-743.

## G-744 (artifact) — Field-Void Occupancy, Five Lifecycle Verbs, and Loop Pickup   (`Nodes/G-744_Field_Void_Occupancy_and_Loop_Pickup.md`)
- Gate / lifecycle: artifact ACTIVE; Brick "Yellow wrapper" (L12).
- Upstream: Updated 44, Updated 43, G-740, G-742, G-741 ("Must not replace", L13). Downstream / cites: none.
- Core claim: "Matching counts are not evidence that two axes are the same." (L15). Occupancy dictionary field2/void5..void6 (L29-35). "Pickup is not a sixth lifecycle state." (L39). "Harmonic remnant of scale n becomes field choice then void choice of scale n+1. Not a second DC rail on the same cell." (L41).
- Equations: `6 route addresses = 2 x 3` (L22).
- Point / Path / Field role: "`3` may name ternary moves and one Point-Path-Field triad only when both are present." (L37).
- Magnetism / gravity / rotation link: none stated (mentions three-winding motor skin, L43).
- Open / parked / not-set items: depends on G-741 measurements (L43).
- Conflicts: none vs canonical. Internal: protected kernel lists "6 measured oscillator gates" (L23) — tension with G-740:47 (six positions are logical/receipt only for CELL_V1). Duplicate ID G-744.

## G-744 — Literal One-Cell Breadboard Build — Real Parts and Math   (`Nodes/G-744_Literal_One_Cell_Breadboard_Build_Real_Parts_and_Math.md`)
- Gate / lifecycle: YELLOW / PROPOSED_BUILD; "YELLOW until measured on bench" (L8).
- Upstream: G-743 (View/Action separation, L70; later layers L410-412). Downstream / cites: `Virtual_Breadboard/` simulator and tests (L22-55).
- Core claim: Stage 1 one millivolt ternary primitive around shared V0 (L18); MOSFETs are switches, not comparators (L69, L199); three triads x two orientations = six logical positions, "must not be relabeled as six physical gates" (L374). Virtual breadboard "does not advance this node's gate" (L57).
- Equations: `V0 = 0.5*VS = 2.500 V` (L86); `VHI = V0 + (5-V0)*1k/125k = 2.520 V` (L130-134); `VLO = 2.480 V` (L146-148); `I = 2.5V/125kΩ = 20 uA` (L154); `Rth = 124k||1k ≈ 992 Ω` (L251); `Delta_loaded ≈ 19.80 mV` (L257-258); `T=0.1 s`, `tau≈T/6≈16.7 ms`, `RC=15 ms` (L383-398). (Arithmetic checked: correct.)
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "three-triad rotating relation" feeds G-743 resolver (L409-410) — circuit phase circulation only.
- Open / parked / not-set items: all stages unmeasured; oscillator topology determines period (L400).
- Conflicts: none vs canonical. Internal: L195 "Ground is not a third binary choice; it is the active middle ternary region." conflicts with G-731:21-31,60, G-740:97, G-741:60, G-727:20 (Ground = no committed binary choice, outside the six routes; HOLD is the active middle ternary region and is distinct from Ground). Should read "HOLD".

## G-745 — Zone-Edge 125 GeV Lattice-Constant Hypothesis   (`Nodes/G-745_Zone_Edge_125GeV_Lattice_Constant_Hypothesis.md`)
- Gate / lifecycle: YELLOW / ACTIVE_HYPOTHESIS; "not a first-principles derivation of a_0; does not change C-322 or Mass Effect" (L8).
- Upstream: C-322, C-318, Updated 24/26, A-114, G-728 E1–E5/F5 ("Does not override", L15). Downstream / cites: `zone_edge_a0.py`; quarantined by G-746, G-728 overlay.
- Core claim: "C-322 keeps approximately 125 GeV as the measured Mirror-Gate boundary-response work to the first mirrored-basin crossing ... It is not the lattice constant, and it is not Mass Effect by itself." (L20). "Mass Effect still requires all four interactions together. Propagation speed, zone-edge flattening, or group-velocity stall must not be rewritten as mass." (L22). Hoyle/7.654 MeV may not confirm an a0 built from 125 GeV (L71-73).
- Equations: `a_0^(edge) = π ħ c_eff / E_125` under A1–A4 (L28-32); `ħc/E_125 ≈ 1.579e-3 fm` (L51); `a_0(c_eff=c) ≈ 4.96e-18 m` (L58); `c_eff/c ~ 2e-3` (L63-65).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (mass guard only).
- Open / parked / not-set items: A1–A4 assumptions; E1, E3, E4, E5, F5 required for promotion (L77-83).
- Conflicts: none vs canonical. ARITHMETIC ERROR L61-65: a_0 ∝ c_eff, and a_0(c)=4.96e-18 m is ~200x smaller than 1 fm, so forcing a_0~1 fm needs c_eff/c ~ 2×10^2, not 2×10^-3 as written.

## G-746 — E1 Scalar Dual Problem and Matrix Handoff   (`Nodes/G-746_Damping_Matrix_Dispersion.md`)
- Gate / lifecycle: BROWN / ACTIVE_HYPOTHESIS; "GREEN only for the assumed scalar PDE; YELLOW for lattice identity, matrix physics, and E5" (L8).
- Upstream: A-114, G-728 E1. Downstream / cites: `damping_matrix_dispersion.py`; G-747; G-728_E1_STAMP.
- Core claim: six exact results for the assumed scalar PDE (L59); "Overdamped means ω is imaginary at real k. It is not spatial evanescence." (L42). "Finite γ still implies an undeclared bath." (L76). "No vacuum-mode integral. No c^4 R/(8πG). No G-745 conversion promoted." (L87).
- Equations: `∂t²ψ + γ∂tψ − c_eff²∇²ψ + ω0²ψ = 0` (L17); `ω² + iγω − Ω_k² = 0`, `Ω_k² = c_eff²k² + ω0²` (L25-27); `ω± = −iγ/2 ± sqrt(c_eff²k² + ω0² − γ²/4)` (L33); `k(ω) = ±(1/c_eff) sqrt(ω² + iγω − ω0²)`, `ℓ_att = 1/|Im k|` (L47-49); `v_g = c_eff²k / sqrt(c_eff²k² + ω0² − γ²/4)` (L55-56); `det[−ω²I − iωΓ + D(k)] = 0` (L71). (Checked: roots and v_g correct.)
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: explicitly excludes curvature/gravity term `c^4 R/(8πG)` (L87).
- Open / parked / not-set items: lattice identity, Field/Void matrix, branch coupling, origin of γ, c_eff, ω0 (L63-66); E5 blockers 1-4 (L80-85).
- Conflicts: none.

## G-747 — Two Group-Velocity Zeros   (`Nodes/G-747_Two_Group_Velocity_Zeros.md`)
- Gate / lifecycle: BROWN / ACTIVE_HYPOTHESIS; "split-gate" (L8).
- Upstream: G-746, A-114. Downstream / cites: none.
- Core claim: "Do not treat these as one mechanism." (L14). Continuum has "no Brillouin zone" (L28). Discrete zero "requires a spacing Δx already present in the stencil. It does not derive Δx." (L38).
- Equations: `v_g = c_eff²k/sqrt(...)`, `v_p = sqrt(...)/k`, `v_g v_p = c_eff²` (L20-25); `cos(ωΔt) = 1 + (β/2)(cos(kΔx) − 1)` (L33); small-k speed `c_L sqrt(β/2)` (L36). (Checked: correct.)
- Point / Path / Field role: none stated; "Next: C2 Point rotation" (L49).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: forbidden identifications (L42-45); A-114 v_g at finite γ (L49).
- Conflicts: none.

## G-748 — Nested Hexagon Pyramids and Triangle Cube Hex   (`Nodes/G-748_Nested_Hex_Pyramid_Triangle_Cube.md`)
- Gate / lifecycle: YELLOW / ACTIVE; "combinatorial and Euclidean receipts; not 4D identity; not Mass Effect; not a0" (L8).
- Upstream: D-408, D-410, D-411, G-743 D1, G-746, G-747, Updated 43. Downstream / cites: C2 Point rotation (frames).
- Core claim: "This node keeps the nest in the repo so C2 Point rotation has frames to live on." (L14). Hexagonal bipyramid census; tet midpoint subdivision → 4 tets + 1 octa; octa mid-belt → hexagon; cube/hex sharing "is a projection / section coincidence" (L41).
- Equations: `V=8, E=18, F=12, V−E+F=2` (L30). (Checked: correct.)
- Point / Path / Field role: "C1 schema can store these vertices as Point positions. C2 must assign an orientation to each Point without stealing Path circulation or Field curl." (L52). "Midpoints of one scale are candidate points of the next scale. That is PPF nesting talk, still Yellow until C2–C4 rotations exist." (L50). Consistent with three-rate rule.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: C2–C4 rotations; 24-cell projections parked in D-410/D3 (L57).
- Conflicts: none.

## Slice summary

### (a) Nodes bearing on Point / Path / Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice
- G-726: PPF assigned at every Homeworld level (Point=site, Path=route, Field=influence/boundary); separate point/path/field state per cell; 2D six-neighbor lattice.
- G-727: Core statement of three distinct kinematic roles (Point = intrinsic orientation, Path = circulation of transported center, Field = circulation of enclosing carrier); nested PPF requires frame transforms, never one omega. Orbital guardrail a = a_Gray + δa_OW with Gray-limit recovery.
- G-728: C2 Point rotation with "carried angular-momentum receipt" OPEN; C3 Path rotation DONE via G-769 with no L; C4 Field curl OPEN, must not be replaced by Path; C8 nested rotation ledger against double counting; C10 PPF ablation; H-series orbital program (H3 acceleration is bookkeeping, H8 nested orbital PPF, H10 ablations incl. "core rotation" and "EM shell"); G-series magnetic hardware (LLG, magnons); F1-F5 Mass Effect four interactions incl. "Mirror-Gate pressure/resistance".
- G-728 overlay: C2–C4 rotations still open; E1 split; G-745 quarantine.
- G-736: proton overlay displays internal Point rotation, carried Paths, enclosing spherical Field phase separately; spin among observables to preserve.
- G-740/G-741/G-743/G-744(breadboard): magnetic/rotating-field content is engineering only (hysteretic magnetic memory candidates, inductive recovery, quadrature rotating stator vector, resolver); rotation must be measured from phase, not inferred.
- G-743 (artifact): PPF schema `X_s={P_s,γ_s,F_s;children}` with frames ground/local/path; "Schema nesting is not rotation physics."; hex lattice graph D1.
- G-744 (artifact): `3` may name a PPF triad only when present.
- G-745: 125 GeV is Mirror-Gate boundary work, not lattice constant, not Mass Effect; mass needs all four interactions.
- G-746: scalar damped dispersion; explicitly excludes c^4 R/(8πG) gravity term; damping implies undeclared bath.
- G-747: lattice zone-edge v_g = 0 needs given Δx; not mass, not 125 GeV.
- G-748: nested hex/tet/octa frames for C2 Point rotation; Point orientation must not steal Path circulation or Field curl.
- G-732/G-735: vortex winding diagnostics and Micro simulator freeze requiring nested PPF receipts (no rotation law).

### (b) Conflicts found
Against canonical rules: none. No file in the slice states L for Path, gravity acting on point rotation, magnetism becoming gravity, expansion, or an L-bookkeeping exception. Watch item: G-728:194-195 H10 lists "core rotation" as a candidate orbital mechanism (ablation only; must not become gravity–point-rotation coupling).
Internal / factual:
1. G-745:61-65 arithmetic error — needs c_eff/c ~ 2×10^2, not 2×10^-3, to make a_0 ~ 1 fm.
2. G-744_Literal_One_Cell_Breadboard:195 calls Ground "the active middle ternary region"; contradicts G-731:21-31,60, G-740:97, G-741:60, G-727:20 (Ground is outside the six routes; the middle ternary region is HOLD).
3. G-728_PROGRESS_OVERLAY:26 and G-743_PPF_Schema:35 list C3 as open/next; G-728 laundry list:92 marks C3 done (G-769).
4. Gate-count tension: G-729:98-102, G-739:33,85 ("3 Mirror + 3 Action = 6 gates") vs G-740:47,225-233 (superseded for CELL_V1 hardware; logical only) and G-744_Field_Void_Occupancy:23 ("6 measured oscillator gates").
5. Duplicate IDs: G-743 (two different files), G-744 (two different files); G-728 has two artifacts plus the node.
6. Symbol collision: `L` used for phase-alignment weight (G-730:37,41) and lifecycle state (G-742:47,51) — not angular momentum.
7. G-738:38-53 LaTeX escape corruption (broken `\rho`, `\times`, `\frac`, `\le`).

### (c) Cross-references outside the slice relevant to point rotation / magnetism
- G-769 (Path rotation, no L) — cited at G-728:92.
- C2 Point rotation (carried angular-momentum receipt) — cited as next/open by G-728:90, G-743 artifact:35, G-747:49, G-748:14,52 (now owned by G-749 per canonical rules; none of these files reference G-749).
- C-318 four-interaction work metric (Mass Effect) — G-728:16,148; G-745:15.
- C-322 125 GeV Mirror-Gate work — G-745:15,20.
- A-114 discrete Field update / dispersion — G-728, G-745, G-746, G-747.
- D-408, D-410, D-411 lattice/geometry — G-727, G-743 artifact, G-748.
- B-226 recursion floor, A-107 — G-732.
- B-221a, C-301 six-gate canon — G-729, G-739.
- Algorythm-Zer0 — G-740:16.
- Updated 43 / Updated 44 / MATH_ATTACK_MAP_UPDATED_43 — G-727, G-728, G-744 artifact, G-748.
- One_Wave_Bench code: six_route_logic, mirror_operator, commitment_map, ground_hold_classifier, noise_hysteresis_audit, asymmetric_oscillator, center_geometry, six_gate_extractor, vortex_diagnostics, proton_sphere_overlay.html, ppf_schema, hex_lattice_graph, zone_edge_a0, damping_matrix_dispersion, chapter_registry; Virtual_Breadboard/.
