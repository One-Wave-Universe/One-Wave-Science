# Ledger 07 (slice 07, 29 files, all read in full)

## G-749 — C2 Point Rotation and Angular-Momentum Receipt   (`Nodes/G-749_Point_Rotation_and_Angular_Momentum_Receipt.md`)
- Gate / lifecycle: BROWN, ACTIVE_HYPOTHESIS, split-gate (GREEN rigid-frame bookkeeping; YELLOW "not yet physics").
- Upstream: G-748 (hex/bipyramid nest, L57-59). Downstream / cites: G-769 (C3 Path rotation, L63); C8 no-double-count starts here (L38); code `point_rotation.point_L_dot` (L65).
- Core claim: "A Point carries an orthonormal frame R in SO(3)" (L16); "A thing keeps the point spin it already has. It does not start one on its own." (L42); "The stable axes are the greatest and the least inertia. The middle axis fights itself." (L44); "Magnetism opens the point. Closed, it resists... Gravity does not start it, and gravity does not affect point rotation." (L46); "This is not path rotation. The path is the ride." (L48).
- Equations: `\dot R = R[\omega]_\times` (L21); `L = I\omega` (L27), units kg m^2, rad/s, kg m^2/s (L30); `R_child^ground = R_parent^ground R_child^parent` (L35); open magnetic gradient `\dot L = 0`, closed `\dot L = -\gamma L` (L65).
- Point / Path / Field role: Point = frame R, body omega, carries L = I omega. Explicitly "not Path circulation and not Field curl" (L53). Path is the ride (L48), G-769 does not carry L (L63). Six pyramid axes = available frames, not six kernel routes (L54).
- Magnetism / gravity / rotation link: Magnetism opens the point; open gradient lets the turn go (dL/dt=0), closed resists (dL/dt=-gamma L) (L46, L65). Gravity does not start or affect point rotation; "Gravity is an ignored argument" (L65).
- Open / parked / not-set items: I declared, not derived from nest (L52); gamma value not set; no Mass Effect from spin (L55); C3 must rotate Path without writing into R (L59).
- Conflicts: none. (This is a canonical source.)

## G-750 — Body-Rate Transport Mechanics   (`Nodes/G-750_Body_Rate_Transport.md`)
- Gate / lifecycle: BROWN, ACTIVE_HYPOTHESIS, split-gate (GREEN SO(3) kinematics; YELLOW parent/child edge choice).
- Upstream: G-749 (C2), G-748 (hex nest). Downstream / cites: start of C8 (L60).
- Core claim: exact compose rule in child body axes (L44); "Transport first, then add. Adding omega_p+omega_c in mixed axes is illegal." (L53); planar hex is the special case where rates just add, "not the 3D law" (L55).
- Equations: `R_child^ground = R_parent^ground R_child^parent` (L19); `\dot R = R[\omega]_\times` (L25); `\dot R_g = R_g(R_c^T[\omega_p]_\times R_c + [\omega_c]_\times)` (L38); adjoint identity `R^T[v]_\times R = [R^T v]_\times` (L41); boxed `\omega_{g,body} = \omega_c + R_c^T\omega_p` (L44); `\omega_{g,ground} = R_g\omega_{g,body} = R_p\omega_p + R_g\omega_c` (L50).
- Point / Path / Field role: Point rates across nest boundary; "Path circulation is still not this vector" (L61); "L = I omega after transport, in one named frame" (L62).
- Magnetism / gravity / rotation link: rotation only (kinematics); no magnetism/gravity stated.
- Open / parked / not-set items: I still declared (L62); which nest edge is parent/child is modeling choice; hex center as parent of six vertices is convention, not derivation (L66).
- Conflicts: none (canonical source).

## G-751 — Primitive Cell and Brain-Cell Skins versus Biology and Layered Robot Dogs   (`Nodes/G-751_Cell_Brain_Biology_RobotDog_Comparison.md`)
- Gate / lifecycle: YELLOW, ACTIVE; mapping table only; does not change Updated 43/44 kernel (L8).
- Upstream: G-741 (primitive cell), G-744 (void pickup wrapper), G-749/G-750, G-722 (motor memory), G-740, G-742. Downstream / cites: `One_Wave_Bench/brain`, `nested_rotation.py`.
- Core claim: "Three skins share the same six-route address space. None of them is proof of the others." (L14); "`nested_rotation.py` already stores Point/Path/Field phases per carrier. G-749/G-750 now supply the rigid-frame transport law those phases must obey if they are ever treated as rates: omega = omega_c + R_c^T omega_p." (L40).
- Equations: `omega = omega_c + R_c^T omega_p` (L40, quoted from G-750).
- Point / Path / Field role: nested_rotation stores Point/Path/Field phases per carrier (L40); body-rate transport mapped to "neck-on-trunk angular add / adjoint composition" (L54) and "body-rate transport on joints" at mid layer (L74). Update item: point brain `nested_rotation` at G-750 when phases are interpreted as rates (L85).
- Magnetism / gravity / rotation link: rotation via G-750 only; CaMKII latch "not magnetic memory yet" (L50). No gravity.
- Open / parked / not-set items: G-741 P0 rail voltages unmeasured; nonverbal cycle receipt; dog adapter later (L98). Do not update: Mass Effect from damping, 125 GeV into a0 (L93-94).
- Conflicts: none.

## G-752 — Triad Brain from Three Loops   (`Nodes/G-752_Triad_Brain_Three_Loops.md`)
- Gate / lifecycle: YELLOW, ACTIVE.
- Upstream: G-724, G-740, G-742, G-741, G-748, G-750. Downstream / cites: `triad_brain.py`, `jetson_runtime.py`, `install_jetson.sh`. Partly superseded by G-753 (which says G-752 mixed nerve into brain).
- Core claim: brain = DC / AC / Quadratic loops on one address space; Jetson optional (L14-39).
- Equations: none.
- Point / Path / Field role: "Hex/pyramid Points (G-748) sit on the AC ring. Body-rate transport (G-750) is how a child cell reports into the parent DC frame. Quadratic leftover is Path-level steer, not a seventh route." (L43).
- Magnetism / gravity / rotation link: none stated (beyond G-750 transport).
- Open / parked / not-set items: SiC endurance stays G-741 Yellow (L47).
- Conflicts: none against canonical rules.

## G-753 — Brain versus 3:1 three-winding nerve   (`Nodes/G-753_Brain_Versus_Three_Winding_Nerve.md`)
- Gate / lifecycle: YELLOW, ACTIVE, yellow-architecture.
- Upstream: G-752 (corrects it), D-411 (planar 3:1 warning, L50). Downstream / cites: none.
- Core claim: brain = Dream (Field/propose), M4 (fast route), Administrator (Void/commit/STOP) (L20-28); nerve = 3:1 three-winding ternary motor around one (0) (L32-38); DC/AC/QC are nerve timing names, not lobes (L54-60).
- Equations: none.
- Point / Path / Field role: none stated (Field = Dream/propose is an architecture label, not kinematic Field).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: do not add a fourth winding; M4 cannot fire a winding (L64).
- Conflicts: none.

## G-754 — Cell to Chip to Cube to Rubik to Two Rubiks   (`Nodes/G-754_Cell_Chip_Cube_Rubik_Two_State_Machines.md`)
- Gate / lifecycle: YELLOW, ACTIVE.
- Upstream: G-748, Updated 34. Downstream / cites: G-756.
- Core claim: scale ladder cell -> chip -> cube -> Rubik -> two Rubiks (L15-19); "The brain is two Rubiks and a midline." (L42).
- Equations: none.
- Point / Path / Field role: none stated (Field Rubik / Void Rubik are architecture seats).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: physical SiC cubes and Rubiks are build targets, not evidence; count matches 2/3/6/8/27 not a derivation (L50).
- Conflicts: none.

## G-755 — Ternary is virtual ground and a choice   (`Nodes/G-755_Ternary_Is_Virtual_Ground_And_Choice.md`)
- Gate / lifecycle: YELLOW, ACTIVE, yellow-lock-candidate.
- Upstream: Updated 43. Downstream / cites: G-756.
- Core claim: "(0) = virtual ground = HOLD", "- = DOWN", "+ = UP"; "That is the entire ternary." (L15-20); "Six routes = those two axes. Stop inventing more axes." (L22).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (space-vector 120/180 tables "how you aim the windings", L26).
- Open / parked / not-set items: none.
- Conflicts: none.

## G-756 — Build contract square-away   (`Nodes/G-756_Build_Contract_Square_Away.md`)
- Gate / lifecycle: YELLOW, ACTIVE; "If a later sentence fights this sheet, this sheet wins until a measured node replaces it." (L14).
- Upstream: G-740, G-739, G-741, G-748, G-749/750, G-753, G-754, G-755, Updated 33, B-206b/c. Downstream / cites: `nested_rotation.py` thresholds.
- Core claim: kernel table (L18-26); two rails every step (L32); loop stacking DC/AC/QC (L36-42); "Point / Path / Field rotation stays three kinematic roles at every scale (G-749/750, C2 done, C3 open)." (L75).
- Equations: none (threshold bands 100-90 ... 15-0, L82).
- Point / Path / Field role: three kinematic roles at every scale (L75); C3 Path rotation listed as unbuilt lock blocker (L117).
- Magnetism / gravity / rotation link: "QC actions down may be carried as spin/magnetic remnant (G-741 Yellow). Not implemented. Not Mass Effect. Not E5." (L109). Sphere/cube/double pyramid "not three extra forces" (L69).
- Open / parked / not-set items: mV P0 cell, mute brain cycle, cube socket, M4 bus timing, C3 Path rotation, SiC endurance (L113-118).
- Conflicts: none against canonical rules. Stale note: L75 "C3 open" and L117 "C3 Path rotation" unbuilt, while G-769 (C3 Path Rotation) now exists with code `path_rotation.py`. Wording "Field rotation" (L75) is looser than canonical "Field curl is neither" but L75 still keeps three separate roles.

## G-757 — Discrete four-interaction energy on the seven-cell   (`Nodes/G-757_Discrete_E4_Seven_Cell.md`)
- Gate / lifecycle: YELLOW, ACTIVE; dimensionless; not C-322 close, not a0, not proton observables (L8).
- Upstream: D-408, G-743, C-322, C-318, `hex_lattice_graph.py`. Downstream / cites: G-757 Hessian receipt, G-758, G-760.
- Core claim: "the first energy that actually lives on D-408 / G-743 geometry" (L14); 14 real coordinates (L26); gate not assigned here (L128).
- Equations: `\psi_i=a_i e^{i\varphi_i}` (L23); `\overline E_4 = E_K+E_E+E_M+E_T+E_\times` (L35-37); `\Gamma = \sum wrap(\varphi_j-\varphi_i)` (L45-47); `E_K = \alpha_K(\Gamma-\Gamma_\star)^2 + \beta_K\sum(a_i-a_j)^2 + \gamma_K a_c\sum(1-cos(\varphi_i-\varphi_c))` (L53-59); `R = (1/6 \sum a_i)/(a_c+\varepsilon)`, `E_E = \alpha_E(R-R_\star)^2 + \delta_E(a_c-1)^2` (L67-70); `C,S`, `\theta = atan2(S,C)`, `E_M = \alpha_M sin^2\theta` (L80-86); `E_T = \alpha_T(R-R_\star-\kappa(\Gamma-\Gamma_\star))^2 + \beta_T\sum(a_i-a_c R_\star)^2` (L94-98); `E_\times = \chi(a_c-1)S` (L106-108); stationarity `\nabla_a E_4 = 0, \nabla_\varphi E_4 = 0` (L118-120).
- Point / Path / Field role: none stated in Point/Path/Field terms. Knot term is phase circulation Gamma around the ring (winding), with "Global phase is a zero mode. Circulation branch is not." (L124). Not labeled as point L or path ride.
- Magnetism / gravity / rotation link: none stated (Mirror E_M is a dipole-angle two-well, not magnetism).
- Open / parked / not-set items: alpha coefficients not from 125 GeV (L132); Gamma_star not baryon number (L133); damping not mass (L134); next calculations list (L139-143).
- Conflicts: none. Note: symbol R here is a shell/core ratio and chi a cross coefficient, distinct from C-319 R tensor and gravity chi.

## G-757_HESSIAN_RECEIPT — G-757 Hessian receipt (2026-09-06)   (`Nodes/G-757_HESSIAN_RECEIPT.md`)
- Gate / lifecycle: NODE_ARTIFACT of G-757, ACTIVE.
- Upstream: G-757. Downstream / cites: G-760 (uses its singularity result).
- Core claim: at dipole seeds both wells have n_negative = 0, n_soft = 1 (global phase) -> local minima (L28-32); sin^2 theta singular at C=S=0, eigenvalues O(10^9) are coordinate singularity (L36); smooth replacement `E_M = alpha_M S^2` (L38).
- Equations: E = 0.01152; eigenvalue list (L20-27); `E_M = alpha_M S^2`.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: connecting path and saddle Hessian not computed (L44); not C-322, not GeV (L45).
- Conflicts: none.

## G-758 — Nudged elastic band between seven-cell wells   (`Nodes/G-758_Nudged_Elastic_Band.md`)
- Gate / lifecycle: YELLOW, ACTIVE.
- Upstream: G-757, C-322. Downstream / cites: G-759, G-760.
- Core claim: amplitude-only 7-D band, barrier ~0.191 "Not converged... Do not treat 0.191 as Delta E_G." (L38-43).
- Equations: `F_i = -\nabla E(q_i)|_\perp + k(|q_{i+1}-q_i| - |q_i-q_{i-1}|)\hat\tau_i` (L23); `F_climb = -\nabla E|_\perp + (\nabla E\cdot\hat\tau)\hat\tau` (L29); barrier `E(q^\ddagger)-E(q_0)` (L34).
- Point / Path / Field role: "path" here is a configuration-space minimum-energy path, not G-769 Path ride. None stated in PPF terms.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: gauge-fixed 14-D path, improved tangent, saddle Hessian (L45). No GeV, no a0 (L47).
- Conflicts: none.

## G-759 — Mass Effect as four-action carry   (`Nodes/G-759_Mass_Effect_Four_Actions.md`)
- Gate / lifecycle: YELLOW, ACTIVE, yellow-bridge.
- Upstream: C-318 ("C-318 is the law", L14), B-206c, C-322, G-757/758. Downstream / cites: G-761.
- Core claim: "Mass Effect is not a stuff. It is the extra four-interaction work when a hold is moved relative to Ground and must be rebuilt." (L16); "Drag C v is damping. Not mass." (L45); kg not real until W derived (L49-53).
- Equations: `M_ij = d^2 E4 / dv_i dv_j` (L37); `E_MG = E4(q_G) - E4(q_0)` (L40); `m_eff != E_MG / c^2` as cause (L43); `M_jk = sum (D_j Z)^T W (D_k Z)` (L51).
- Point / Path / Field role: none stated in PPF terms. Inertia (mass) = carry cost of moving a hold relative to Ground.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: work metric W (4x4 blocks, crosses on) not derived (L49-53). Over = Mirror-Gate path, not Mass Effect (L29).
- Conflicts: none against canonical rules. (Bears on "resistance = mass / organization": this node defines mass as rebuild work, not as resistance.)

## G-760 — Micro first attack — Mirror term on the seven-cell   (`Nodes/G-760_Micro_First_Attack_Mirror_Term.md`)
- Gate / lifecycle: YELLOW, ACTIVE.
- Upstream: G-735, C-322, G-757 receipt. Downstream / cites: G-761, G-762.
- Core claim: `E_M = alpha S^2` is one valley, NEB flat (L20); with `+ mu(C^2+S^2-m^2)^2` the ring still flattens, barrier ~0 (L22); "Can a Mirror potential that wants a finite dipole survive the weave that wants a round ring?" (L26); "If no coefficient set does that, G-757 does not have two basins and C-322 has no gate on this graph." (L28).
- Equations: `E_M = alpha sin^2 theta`, `E_M = alpha S^2`, `E_M = alpha S^2 + mu (C^2+S^2-m^2)^2` (L18-22).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: attack order 1-5 (coefficient scan mu vs beta_T vs beta_K first; W and Mass Effect step 4; proton observables last) (L32-36).
- Conflicts: none.

## G-761 — Standard Model assumptions versus One-Wave node equations   (`Nodes/G-761_SM_Assumption_Smash.md`)
- Gate / lifecycle: YELLOW, ACTIVE; "measurements kept; ... no claim that OW has replaced SM numerics" (L8).
- Upstream: C-318, C-322, F7, G-735, G-760, E5. Downstream / cites: none.
- Core claim: Mass Effect is carry of four-interaction hold, not Higgs curvature (L24-34); "hbar omega=125 is retired. So is 125 as lattice spacing." (L53); cross term load-bearing (L65); "Until then the SM still wins the spreadsheet." (L103).
- Equations: SM `m = y v`, `V = mu^2 phi^2 + lambda phi^4` (L21, quoted to deny); `\mathcal M_{ij} = \partial_{v_i}\partial_{v_j}\overline E_4|_{v=0}` (L27-31); `E_MG = \overline E_4(q_G)-\overline E_4(q_0) = \int_\Gamma P_ext d\xi \approx 125 GeV` (L42-44); `m_eff != E_MG/c^2` (L48); `R_G = E_MG/(m_eff v_lat^2)` (L100); `2 x 3 = 6` (L88).
- Point / Path / Field role: none stated. Inertia: "If you drop a block of W and the inertia does not change, the mechanism has already failed." (L34).
- Magnetism / gravity / rotation link: "E5 vacuum-integral gravity remains Yellow-blocked. Do not replace the VEV with a new soup." (L77). Light-like branch = traveling mode with M ~ 0 (L83).
- Open / parked / not-set items: gapless + massive hold from one rule open in C-318 (L83); color as derived topological charge open (L71); smash criteria (L97-101).
- Conflicts: none.

## G-762 — Four balanced interactions   (`Nodes/G-762_Four_Balanced_Interactions.md`)
- Gate / lifecycle: YELLOW, ACTIVE.
- Upstream: G-757, G-760, C-318/C-322 (implicit). Downstream / cites: none.
- Core claim: "At a hold, nothing wins." (L14); "Balance means those rows sum to zero at rest. Mass Effect is the cost of moving the whole table. Gate is the cost of the Over column going through." (L37).
- Equations: `\overline E_4 = <E_K+E_E+E_M+E_T+E_\times>` (L17); `\nabla_q \overline E_4(q_0)=0`, `P_ext(\xi=0) = P_K+P_E+P_M+P_T+P_\times = 0` (L21-22); `P_a = dE_a/d\xi` signed (L25).
- Point / Path / Field role: none stated (Knot row "tightens circulation", "winding jump", L31).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: coefficients where all four sit nonzero at q_0 and q_pi (L46).
- Conflicts: none.

## G-763 — Scalar differential vector tensor stratum harmonic   (`Nodes/G-763_Scalar_to_Harmonic.md`)
- Gate / lifecycle: YELLOW, ACTIVE, yellow-dictionary.
- Upstream: kernel (2x3). Downstream / cites: none.
- Core claim: six words; "Do not add a seventh word." (L34).
- Equations: none.
- Point / Path / Field role: "vector | the move. DOWN/UP. Path. ternary along a directed edge" (L25); "tensor | carry. M_ij, W_ij" (L26). Point and Field not stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## G-764 — Combined-State Lattice Simulator Foundation   (`Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md`)
- Gate / lifecycle: YELLOW, ACTIVE; physical lattice spacing and nonlinear bound modes open (L8).
- Upstream: Chapter 01 Continuous Lattice, Chapter 05 Simulation Engine, D-408, D-417, E-531, G-728, G-765, G-766, `sims/00_CANONICAL_INGEST_RULE.md` (L22-30). Downstream / cites: `sims/00-lattice-primitive/metadata-anchors.json`.
- Core claim: "The primitive is not a cell and not a particle. It is one local degree of freedom of a numerically discretized continuous medium." (L18); "No physical lattice spacing is assumed." (L48); "A resolved whole may only become a next-scale point after its projection error is measured." (L103).
- Equations (file has stripped-backslash LaTeX): site state `X_i = (q_i, qdot_i, phi_i, x_i, h_i)` (L37); `qddot_i + 2 zeta omega_0 qdot_i + omega_0^2 q_i + lambda q_i^3 = c_L^2 (Delta_h q)_i + d_i(t)` (L55-58); `(Delta_h q)_i = 1/a_num^2 sum_{j in N(i)} (q_j - q_i)` (L64); `Q`, `A_rms`, `V_rms` (L78-84); `C_phi = |1/N sum e^{i phi_i}|` (L90-91); `X_whole = (Q, A_rms, V_rms, C_phi, E, Gamma, Omega)` (L97-98); octave `f_n = 2^n f_0`, `A_n = 2^n A_0`, `r_n = 2^n r_0` only when enabled, kept separate (L140-151).
- Point / Path / Field role: Gamma is a "circulation/vorticity diagnostic" in the combined state (L101); a resolved whole may become a next-scale point (L103). No point L, no path ride stated.
- Magnetism / gravity / rotation link: build order includes "EM LATTICE CONTROL / MAGNETIC REORGANIZATION (G-765)" (L174). No gravity.
- Open / parked / not-set items: lattice spacing, site energy, mass scale not defined by metadata anchors (L119); falsification gates 1-8 (L157-164).
- Conflicts: none. Note: `r_n = 2^n r_0` geometry doubling is a lattice view transform, gated off by default; not a cosmological scale factor. Formatting defect: LaTeX backslashes stripped (e.g. `rac`, `qquad`, `ight` at L64, L78, L91).

## G-765 — EM Lattice Potential and Proton-Displacement Proof   (`Nodes/G-765_EM_Lattice_Potential_and_Proton_Displacement_Proof.md`)
- Gate / lifecycle: YELLOW, ACTIVE_HYPOTHESIS; "no proton-like solution or physical coupling coefficient established" (L8).
- Upstream: C-311, C-319, C-320, G-764, G-766, chapters 01/05, sims ingest rule and anchors (L27-35). Downstream / cites: G-766 run order step 8.
- Core claim: loop "potential -> potential slope / electric field -> lattice displacement -> magnetic rotation -> path reorganization -> next lattice/EM state" (L104-105); "Reorganization changes directional accessibility. It does not, by itself, create energy, charge, scalar compression, gravity, or a proton." (L108-109).
- Equations: extended state `X_i = (q_i, qdot_i, phi_i, x_i, h_i, Phi_i, E_i, B_i, R_i, K_L,i)` (L42-43); `E = -grad Phi - d_t A`, `B = curl A` (L60-63); `f_EM = rho_e E + J x B` (L71); lattice + `g_E D_i(E) + g_B D_i(B, K_L)` (L83-85); C-319 `tau_R d_t R = -R + lambda_B (B⊗B - |B|^2/3 I)`, `K_L = I + kappa_R R` (L94-98); `E_num = E_kin + E_lat + E_EM + E_coupling + E_boundary` (L116-117); `E_EM = ∫(eps_0/2 |E|^2 + 1/(2 mu_0)|B|^2) dV` (L123-126); multi-observable fit `theta* = argmin sum (O_sim - O_meas)^2/sigma^2` (L159-162); `chi = -div u` compression, `omega = curl u` circulation/rotation (L175-182).
- Point / Path / Field role: Field = E, B, Phi layers; magnetic reorganization R changes path accessibility K_L (Path). `omega = curl u` is a Field-level curl of displacement labeled "circulation/rotation" (L181-184) — this is Field curl, not point L.
- Magnetism / gravity / rotation link: magnetism -> "magnetic rotation -> path reorganization" (L104); K_L = I + kappa_R R matches canonical; reorganization does not create gravity (L109). R = 0 run is a required control step (L194). No point-spin statement.
- Open / parked / not-set items: kappa_R, g_E, g_B, D_i projection not set; physical lattice spacing, new EM law, proton solution all open (L220-222).
- Conflicts: none against canonical rules (consistent with "magnetism does not become gravity", K_L form, R=0 baseline control). Wording caution: L181 calls curl u "circulation/rotation"; canonical says Field curl is neither point rotation nor path ride — the node does not claim it carries L, so not a hard conflict.

## G-766 — Discrete Lattice Dispersion and Octave-Emergence Proof   (`Nodes/G-766_Discrete_Lattice_Dispersion_and_Octave_Emergence_Proof.md`)
- Gate / lifecycle: YELLOW, ACTIVE_HYPOTHESIS; no physical spacing or octave law established (L8).
- Upstream: G-746, G-745 (quarantined), G-764, chapters 01/05, sims rule/anchors (L24-30). Downstream / cites: G-768 (L196), G-767 (L209-219), G-765 (L173).
- Core claim: "It does not impose an octave ladder as an input" (L18-19); "Overdamping in the temporal problem must not be relabeled as spatial evanescence. Zone-edge flattening must not be relabeled as mass." (L91-92); "Merely drawing the predefined sequence f_n=2^n f_0 is not evidence of emergence." (L118-119); static signed axis "must not be promoted to geometric doubling" (L198).
- Equations: linear control `qddot + 2 zeta omega_0 qdot + omega_0^2 q = c_L^2 (Delta_h q) + d` (L38-39); plane wave (L45); `Lambda_tri(k) = 2/a^2 [cos(k·a1)+cos(k·a2)+cos(k·(a2-a1)) - 3]` (L51-58); `Omega^2 = omega_0^2 - c_L^2 Lambda` (L63-64); `omega_± = -i zeta omega_0 ± sqrt(Omega^2 - zeta^2 omega_0^2)` (L70-72); `v_p`, `v_g = grad_k Re omega` (L84-85); octave residual `r_mn = log2(f_m/f_n) - round(...)` (L100-103); `chi^2(theta)` multi-dataset (L153-158).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: enable G-765 EM forcing and magnetic reorganization only at step 8 (L173). Rotated lattice orientations as controls (L114). No gravity.
- Open / parked / not-set items: tests specified but not run; G-745 quarantined; no physical spacing (L204-207); R3 R2 R1 composition unresolved (L200).
- Conflicts: none. (Consistent with "no expansion, no scale factor": scale transforms kept separate and not promoted.)

## G-767 — Measured Spectrum Lattice Phase Map   (`Nodes/G-767_Measured_Spectrum_Lattice_Phase_Map.md`)
- Gate / lifecycle: YELLOW, ACTIVE_HYPOTHESIS; "no superfluid crystal lattice is established until recurrence survives nulls and held-out data" (L8).
- Upstream: sims ingest rule, sims/01-cern-wave-transform, sims/04-gwosc-strain, G-766 (L86-89). Downstream / cites: G-766 handshake.
- Core claim: "Can independent measured excitation spectra be compressed by a common recursive scale coordinate more strongly than matched null data?" (L16); "'Superfluid crystal lattice' is a One-Wave hypothesis, not an ingest assumption." (L78).
- Equations: `u = log2(x/x0)`, `n = floor(u)`, `phi = u - n` (L25-27); `Q = x/Gamma` (L32); `rho(u) = dN/dlog2(x)` (L38); `rho_n(phi) = A_n F(phi) + epsilon_n(phi)` (L42).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: eight required nulls (L48-55); cross-domain freeze sequence (L59-64).
- Conflicts: none.

## G-768 — Anisotropic Signed-Axis Spectrum and Rotating-Axis Scale Test   (`Nodes/G-768_Anisotropic_Signed_Axis_Spectrum_and_Rotating_Axis_Scale_Test.md`)
- Gate / lifecycle: YELLOW, ACTIVE_HYPOTHESIS; static signed-axis spectrum derived; isotropic 2x not proven (L8).
- Upstream: G-766. Downstream / cites: Rabbit Hop / Z12 grammar (L147-151).
- Core claim: "DISPROVED: one static (J_c=-J) assignment implies isotropic 2x scale recursion." (L105); M-type stripe `psi_nm = A(-1)^{n+m}` (L66, L107); rotational averaging restores isotropy at tensor level but "does not establish d=2" (L126).
- Equations: bond vectors delta_a, delta_b, delta_c (L22-24); `J_a=J_b=+J, J_c=-J` (L29); `D psi_i = sum J_nu (psi_{i+nu}+psi_{i-nu}-2 psi_i)` (L33-34); `Lambda_J(u,v) = 2J[cos(2u) - 2 sin u sin v - 1]` (L39); extrema 0, +J, -8J (L47-49); `E = -sum J_ij psi_i psi_j` (L75); `|Delta psi| = 2|psi_0||sin(theta/2)|` (L83); `sqrt3|psi_0| < H_c < 2|psi_0|` (L87); `D_2 = R_120 D_1 R_120^{-1}`, `D_3 = R_240 D_1 R_240^{-1}`, `D_bar = dI` (L113-123); `R_cycle = R_3 R_2 R_1` (L137).
- Point / Path / Field role: none stated. Rotation here is rotation of a lattice bond-sign assignment (orientation cycling), not point spin.
- Magnetism / gravity / rotation link: "gradient/shear-triggered hysteretic switching" and "transfluxor coupling law" (L79, L89) as candidate selection (magnetic-core hysteresis analogy); no gravity.
- Open / parked / not-set items: hysteretic selection, physical realization, R1/R2/R3 maps, R_cycle = 2I (L157-161).
- Conflicts: none (consistent with "no scale factor" — it refuses to force 2x).

## G-769 — C3 Path Rotation   (`Nodes/G-769_Path_Rotation.md`)
- Gate / lifecycle: BROWN, ACTIVE_HYPOTHESIS; "split-gate: kinematic turning GREEN; not a planetary orbit" (L8).
- Upstream: G-749. Downstream / cites: code `One_Wave_Bench/logic_core/path_rotation.py` (L20).
- Core claim: "The path is the ride. It is not the point." (L14); "A path is a sequence of centers... A closed regular hexagon turns 2pi. A straight ride turns 0." (L16); "The receipt carries turning, corner count, mean edge, and curvature. It does not carry L. The magnetic gradient is not applied. The gravity coefficient on the point is 0." (L18).
- Equations: turn = angle between incoming and outgoing edge; closed hexagon total 2pi (L16) (no formula written).
- Point / Path / Field role: Path = ride, no L; "Point spin stays in G-749" (L22).
- Magnetism / gravity / rotation link: "An open magnetic gradient leaves L unchanged. A closed one resists it. Passing a gravity vector into that rate does not change the rate." (L22). Magnetic gradient not applied to path (L18).
- Open / parked / not-set items: "not an ephemeris. This is not a wake law. The assimilation boundary is still not derived." (L26).
- Conflicts: none (canonical source).

## I-07 — Gate Colors and Metals   (`Nodes/I-07_Gate_Colors.md`)
- Gate / lifecycle: GREEN, ACTIVE, Canon / Language; "The ladder itself is an assumption we are using, not a measurement." (L8).
- Upstream: repo root `GATE_COLORS.md` (L14). Downstream / cites: gate vocabulary used by all nodes.
- Core claim: "Brown seed. Green growth. Grey SM blockage (not invincible). Yellow brick road = math + assumptions. Bronze bust / silver statue from sim + extensive work. Golden road not claimed. Math stops at yellow." (L16).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Golden not claimed.
- Conflicts: none.

## PHASE_5_COMPREHENSIVE_SOLUTION_ANALYSIS — Phase 5 comprehensive hypothesis testing   (`Nodes/PHASE_5_COMPREHENSIVE_SOLUTION_ANALYSIS.md`)
- Gate / lifecycle: NODE_ARTIFACT, parent C-318, ACTIVE_HYPOTHESIS; author "Claude Haiku 4.5", 2026-10-04.
- Upstream: C-318, prior PHASE_5 docs. Downstream / cites: `tests/energy_component_scaling_analysis.py`, `tests/hypothesis_c_flavor_recalibration.py`, `tests/hypothesis_combined_radius_kappa.py`, `solvers/quark_mass_solver.py`, `solvers/proton_compression_simulator.py` (L262-273).
- Core claim: combined A+C "SOLUTION FOUND" with `R(m) = 0.35 × m_scale^(-0.10)`, `κ_T(m) = 1.5 × √m_scale`; heavy 130.6% -> 58.9%, top 297.5% -> 28.6% (L27-33); "The octave-scaling mechanism and four-interaction architecture are SOUND." (L291).
- Equations: `E_total/√m_scale` varies 24x (L45); `E_phase = κ_T × V_knot ≈ constant` (L70); `R(m) = 0.35 m_scale^α`; `κ_T(m) = 1.5 × factor × √m_scale` (L131); `V ∝ R^3 ∝ m_scale^(-0.30)`, `E_K ∝ V^(-1)` (L171-172).
- Point / Path / Field role: none stated in PPF terms. Uses circulation energy E_circ (L58-65) as dominant mass contribution for heavy flavors.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: flavor-specific α (Option 2, L231-238); Hypothesis D QCD extensions (L246-256); 125 GeV anchor re-calibration (L227).
- Conflicts: No direct conflict with the listed canonical rules. In-slice tensions: (1) L171-173 "volume smaller ... Reduces kinetic energy contribution E_K ∝ V^(-1)" is self-contradictory (smaller V with E_K ∝ 1/V raises E_K) and contradicts HEAVY_QUARK_DIAGNOSIS L88 `E_K = ω² × Volume` (E_K ∝ V). (2) Option 2 per-family α (L231-238) is per-observable retuning, which G-765 L165 and G-766 L161-162 / G-761 L101 reject as "not one explanatory mode". (3) Table for α=-0.10 radius-only (L87: 39.0/58.9) differs from A/B file (L50: 41.0/60.4) — numbers reassigned between α rows. (4) "SOLUTION FOUND" while strange/charm/bottom get worse (L140-143) and under I-07 "math stops at yellow".

## PHASE_5_HADRON_EXTENSION_VERIFIED — Phase 5 Hadron Spectrum Extension — Verification by Consequence   (`Nodes/PHASE_5_HADRON_EXTENSION_VERIFIED.md`)
- Gate / lifecycle: frontmatter YELLOW, ACTIVE (L5-8); footer says "Gate: GREEN (nucleons); YELLOW (strangeness, mesons pending)" (L222).
- Upstream: C-317 (confinement, L135), C-318 (carried-pattern resistance, L151), PHASE_5 combined solution. Downstream / cites: `solvers/hadron_mass_predictor.py`, `solvers/hadron_calibration.py`; commits b712c640, d43414d0 (L203-216).
- Core claim: radius law `R = 0.85 fm × m_scale^(-0.05)` "holds uniformly" (L24, L37); nucleons calibrated σ_T=0.010 GeV/fm², κ_T=0.373 GeV, η_T=0.001 GeV; proton 2.6%, neutron 5.4% (L46-57); Lambda 29.9%, pion 196% fail (L91-99); "The mass of such a recurrence is the carried-pattern resistance (C-318): the energy density required to sustain and move this pattern through Ground (the lattice)." (L151).
- Equations: `R(m_scale) = 0.85 fm × m_scale^(-0.05)`, `m_scale = (∏ m_constituent)^(1/n)/m_up` (L24-26); `κ_T(m_scale) = 1.5 × √m_scale` (L67).
- Point / Path / Field role: hadrons as bounded recurrences of displacement field ψ with "three internal Vortex Phases" (L147); pion "2-vortex" (L149). No point L / path ride stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: flavor-dependent α/κ_T, relativistic pair binding for mesons (L194-197).
- Conflicts: (1) Mass as "carried-pattern resistance" (L151) vs canonical "resistance = mass / organization" — this file equates mass with resistance, the canonical rule makes resistance the ratio mass/organization; tension, flag. (2) "superfluid lattice" used as framework fact (L145, L221) vs G-767 L78 "a One-Wave hypothesis, not an ingest assumption". In-slice defects: gate GREEN in footer vs YELLOW frontmatter (L5 vs L222) while I-07 says math stops at yellow; "Verified" radius table (L30-35) is circular (predicted = formula); κ_T table column "Expected: 1.5×√m" lists √m values without the 1.5 (L73-76), and contradicts the calibrated κ_T=0.373 GeV (L48); "proton/neutron masses similar (verified: 938/940 MeV)" (L157) cites experiment, while the model gives 913.5 vs 990.6 MeV with neutron-proton ordering correct but splitting ~77 MeV vs 1.3 MeV measured; R=0.85 fm here vs R=0.35 fm quark knot in other PHASE_5 files (unreconciled).

## PHASE_5_HEAVY_QUARK_DIAGNOSIS — Phase 5 Heavy-Quark Mass-Scale Problem Diagnosis   (`Nodes/PHASE_5_HEAVY_QUARK_DIAGNOSIS.md`)
- Gate / lifecycle: NODE_ARTIFACT, parent C-318, ACTIVE_HYPOTHESIS.
- Upstream: C-318, C-322 (125 GeV anchor), `PHASE_5_STATUS.md`, `solvers/proton_compression_simulator.py` (λ = 0.976) (L212-217). Downstream / cites: A/B test results.
- Core claim: "After implementing the 125 GeV Mirror-Gate calibration (λ = 0.976)... heavy quarks (c/b/t) remain dramatically overpredicted by 9× to 1243×" (L20); root cause "mass ∝ m_scale^(3/2) for heavy quarks instead of mass ∝ √m_scale" (L22).
- Equations: `mass = confined_scale_factor × E_total / R² = 0.0015 × √m_scale × E_total / R²` (L64-65); `omega_circulation = omega_up × √m_scale`, `E_K = omega_circulation² × Volume` (L87-89); `weight = 0.6/(1.0 + 0.02(m_scale - 1))` (L149).
- Point / Path / Field role: none stated in PPF terms; "omega_circulation" (circulation rate) squared times volume taken as kinetic energy feeding mass (L87-92). Not tied to L = I omega.
- Magnetism / gravity / rotation link: "Spin-dependent interactions (already accounted via g_SO...)" (L122); "Universal Coupling: Single g_SO = 0.5 ... calibrated from electron g-2" (L185).
- Open / parked / not-set items: Hypotheses A-D (L98-136); weight factor validity (L157).
- Conflicts: (1) Spin-orbit coupling g_SO contributing to quark mass (L122, L185) is in tension with G-749 L55 "no Mass Effect from spin" — flag as possible conflict. (2) In-slice tension with G-761 L48/L53 and G-757 L132: global energy scale is calibrated to 125 GeV (λ = 0.976) for mass prediction; G-761 allows calibrating on 125 only with one fixed E4 and W, which this solver does not have (W not derived per G-759). Internal: L20 says "overpredicted 9× to 1243×" but the table (L32-37) and L39 say heavy quarks are underpredicted (-98%).

## PHASE_5_HYPOTHESIS_A_B_TEST_RESULTS — Phase 5 Hypothesis A & B Test Results   (`Nodes/PHASE_5_HYPOTHESIS_A_B_TEST_RESULTS.md`)
- Gate / lifecycle: NODE_ARTIFACT, parent C-318, ACTIVE_HYPOTHESIS.
- Upstream: PHASE_5_HEAVY_QUARK_DIAGNOSIS, `PHASE_5_STATUS.md`. Downstream / cites: `tests/hypothesis_a_quick_test.py`, `tests/hypothesis_b_weight_factor_analysis.py`, `tests/hypothesis_b_implementation_test.py`, solvers (L255-265).
- Core claim: A rejected as standalone; B rejected, weight is "protective" (L22-35); "confirms the octave-scaling mechanism and four-interaction architecture are sound" (L247-248).
- Equations: `R(m_scale) = 0.35 × m_scale^alpha` (L43); `E_phase_total = E_circ_phase + w(m_scale) × (E_phase + E_shell_phase)` (L133); `m ∝ √m_scale × E_K ∝ m_scale^(3/2)` (L111).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Hypothesis C, D (L182-199); derive flavor mechanism (L228).
- Conflicts: none against canonical list. Internal: L59 "heavier quarks confined to smaller volumes → higher mass" vs COMPREHENSIVE L171-173 (smaller volume reduces E_K); L66 cites α=+0.20 result (1301.9%) absent from its own table; weight function labeled "exponential" (L92) but formula in Diagnosis L149 is hyperbolic; α=-0.10 row (41.0/60.4) differs from COMPREHENSIVE.

## PHASE_5_SESSION_SUMMARY — Phase 5 Session Summary: From Diagnosis to Solution   (`Nodes/PHASE_5_SESSION_SUMMARY.md`)
- Gate / lifecycle: NODE_ARTIFACT, parent C-318, ACTIVE_HYPOTHESIS.
- Upstream: other PHASE_5 docs. Downstream / cites: tests and `PHASE_5_STATUS.md` (L195-211); commit de8aafc0 (L159).
- Core claim: "The heavy-quark problem has been solved in principle." (L264); "The remaining work is implementation and validation—not physics discovery." (L272); α = -0.05 implemented (L153-159).
- Equations: `R(m) = 0.35 × m_scale^α`, `κ_T(m) = 1.5 × factor × √m_scale` (L64); `V ∝ R³ ∝ m_scale^(-0.30)`, E_K "scales as 1/V" (L100-101); `E_total ≈ E_K + κ_T·V` (L115).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: decision α=-0.05 vs -0.10; flavor-specific α; Hypothesis D; hadron extension (L250-258).
- Conflicts: none against canonical list. Internal: baseline numbers L23-24 (u 8.3%, d 18.0%, c 65.6%, b 38.0%) disagree with its table L80-84 (u 20.7%, d 16.1%, c 58.7%, b 35.8%); L65 "while preserving light quarks" vs L87 light 25.5% -> 29.0%; L128 lists bottom 35.8% -> 69.9% under "What We Gain"; same 1/V kinetic-energy contradiction as COMPREHENSIVE; "solved in principle / not physics discovery" (L264, L272) overclaims relative to I-07 and G-761 L103.

## vtc_zero_logic — VTC-0 Breadboard Mapping Verification Notes   (`Nodes/vtc_zero_logic.md`)
- Gate / lifecycle: NODE_ARTIFACT VTC-0-HARDWARE-UI-MAPPING, parent G-740, PROPOSED_BUILD; "UNVERIFIED HARDWARE/UI MAPPING" (L12).
- Upstream: G-740, `CELL_V1_ANTI_DRIFT.md` (geometry authority, L16). Downstream / cites: none.
- Core claim: zero/reference `+ <-> (0) <-> -` (L21); "Three physical bidirectional mirrors produce six directed edge interfaces." (L42); failed mapping must be DISMISSED, not promoted (L52).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: five verification questions (L46-50), including whether split-rail conflicts with virtual-ground CELL_V1.
- Conflicts: none.

## Slice summary

### (a) Nodes in this slice bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking
- G-749: canonical Point rotation. R in SO(3), `L = I omega`, point keeps its spin, stable axes greatest/least inertia, magnetism opens the point (open dL/dt=0, closed dL/dt=-gamma L), gravity ignored. I declared; no Mass Effect from spin.
- G-750: canonical parent/child transport `omega_body = omega_c + R_c^T omega_p`; transport first, then add; L in one named frame.
- G-769: canonical Path rotation. Path = ride, carries turning/curvature, no L, magnetic gradient not applied, gravity coefficient 0. Not an ephemeris, not a wake law.
- G-751: maps G-750 onto `nested_rotation.py` Point/Path/Field phases; update item to use G-750 when phases become rates.
- G-752: Points on AC ring; body-rate transport carries a child cell into the parent DC frame; quadratic leftover = Path-level steer.
- G-756: "Point / Path / Field rotation stays three kinematic roles at every scale"; C3 listed as open (stale vs G-769); spin/magnetic remnant for QC actions down is Yellow and "Not Mass Effect. Not E5."
- G-763: vector = the move = Path; tensor = carry `M_ij, W_ij`.
- G-757 / G-757 receipt / G-758 / G-760 / G-762: four-interaction energy on the seven-cell; knot = phase circulation Gamma; Mirror two-well fails against weave (G-760); balance = rows sum to zero at a hold.
- G-759: Mass Effect = four-interaction rebuild work when a hold moves relative to Ground; `M_ij = d^2E4/dv_i dv_j`; damping is not mass; kg requires W.
- G-761: inertia must depend on W blocks; 125 GeV is the gate energy, not mass; E5 gravity Yellow-blocked.
- G-764: lattice simulator; Gamma = circulation/vorticity diagnostic; a whole becomes a next-scale point only after projection error.
- G-765: magnetism -> path reorganization via C-319 `K_L = I + kappa_R R`; R=0 control run; reorganization does not create gravity; `omega = curl u` Field curl labeled circulation/rotation.
- G-766: dispersion; zone-edge flattening must not be called mass; scale transforms separate.
- G-768: static signed-axis does not give isotropic 2x; rotating orientation restores isotropy only at tensor level; hysteretic/transfluxor selection proposed.
- PHASE_5 HEAVY_QUARK_DIAGNOSIS / A_B / COMPREHENSIVE / SESSION_SUMMARY: quark mass from circulation kinetic energy `E_K = omega_circ^2 V` plus constant terms; spin-orbit g_SO; 125 GeV calibration λ=0.976.
- PHASE_5_HADRON_EXTENSION_VERIFIED: mass = "carried-pattern resistance" (C-318) of a bounded recurrence through Ground.

### (b) Conflicts found
Against the canonical rules:
1. `Nodes/PHASE_5_HADRON_EXTENSION_VERIFIED.md:151` — mass defined as "carried-pattern resistance"; canonical has resistance = mass / organization. Tension (mass ≡ resistance vs resistance as a ratio).
2. `Nodes/PHASE_5_HEAVY_QUARK_DIAGNOSIS.md:122,185` — spin-orbit g_SO feeds quark mass; G-749:55 says "no Mass Effect from spin". Possible conflict.
3. `Nodes/G-756_Build_Contract_Square_Away.md:75,117` — C3 Path rotation "open"/unbuilt; stale against G-769 (exists, with `path_rotation.py`). Not a rule conflict, a stale status.
4. `Nodes/G-765_EM_Lattice_Potential_and_Proton_Displacement_Proof.md:181-184` — `curl u` called "circulation/rotation"; canonical says Field curl is neither point rotation nor path. Wording only; no L assigned.
Against other in-slice nodes (G-761/G-765/G-766/G-767/I-07):
5. `PHASE_5_COMPREHENSIVE_SOLUTION_ANALYSIS.md:231-238` — per-family α retuning vs G-765:165, G-766:161-162, G-761:101.
6. `PHASE_5_HEAVY_QUARK_DIAGNOSIS.md:20,39,217` and others — 125 GeV global calibration (λ=0.976) of a mass solver with no derived W, vs G-761:48-53/97-101, G-757:132, G-759:49-53.
7. `PHASE_5_HADRON_EXTENSION_VERIFIED.md:145,221` — "superfluid lattice" assumed vs G-767:78.
8. `PHASE_5_HADRON_EXTENSION_VERIFIED.md:5 vs 222` — YELLOW frontmatter vs GREEN footer; I-07:16 "math stops at yellow".
9. PHASE_5 internal: E_K ∝ V (DIAGNOSIS:88) vs E_K ∝ 1/V (COMPREHENSIVE:172, SESSION_SUMMARY:101) with "smaller volume reduces E_K"; overpredicted vs underpredicted (DIAGNOSIS:20 vs 39); mismatched α-table numbers (A_B:50 vs COMPREHENSIVE:87); baseline numbers mismatch (SESSION_SUMMARY:23-24 vs 80-84); circular radius "verification" and κ_T table missing the 1.5 factor (HADRON:30-35, 73-76).

### (c) Cross-references outside this slice that matter for point rotation or magnetism
- G-748 (hex/bipyramid nest; Points on hex vertices and apices) — G-749:57, G-750:55, G-752:43, G-754:44, G-756:69.
- C-311 (electric/magnetic duality), C-319 (magnetic lattice reorganization, `K_L = I + kappa_R R`), C-320 (magnetic compression-path coupling) — G-765:27-29, 91-99.
- C-318 (mass mechanism), C-322 (Mirror Gate / 125 GeV) — G-757, G-759, G-761, PHASE_5 files.
- G-741 (primitive cell; spin/magnetic remnant Yellow) — G-751, G-756:109.
- E5 (vacuum-integral gravity, Yellow-blocked) — G-761:77, G-756:109.
- Code: `point_rotation.point_L_dot` (G-749:65), `One_Wave_Bench/logic_core/path_rotation.py` (G-769:20), `nested_rotation.py` (G-751:40, G-756:79), `hex_lattice_graph.py` (G-757:28), `solvers/quark_mass_solver.py`, `solvers/proton_compression_simulator.py`, `solvers/hadron_mass_predictor.py`.
- C8 (no double count) begins at G-749/G-750; C9 scale labels (G-756:75).
- G-745 (125 GeV lattice constant, quarantined), G-746 (damping dispersion) — G-766.
- `GATE_COLORS.md` (I-07), `CELL_V1_ANTI_DRIFT.md` (vtc_zero_logic), `PHASE_5_STATUS.md`.
