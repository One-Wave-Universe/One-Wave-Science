# Ledger slice 01 — A-101 … A-117, B-201 … B-215 (39 files, all read in full)

## A-101 — GROUND / ZERO   (`Nodes/A-101_Ground_Zero.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Foundation Primitive.
- Upstream: A+101 One Field Ground.   Downstream / cites: A-102, A-103, all measurement nodes; cites E-517 Negative Space, B-223 Move, B-224 Choice.
- Core claim: "Ground / Zero is the reference state required for measurement." (L34). Void = ψ=ψ₀ within the one field, not absence of field (L36-41); Void-as-region is the set of points where ψ=ψ₀ (L54-58). "NO GROUND: No displacement can be measured." (L94-96).
- Equations: x = ψ − ψ₀ (L90, L112, L280); ψ=ψ₀ → x=0; ψ≠ψ₀ → x≠0 (L105-107); same-ground differential Δx = ψₙ − ψₙ₋₁ with ψ₀,ₙ = ψ₀,ₙ₋₁ (L134-138).
- Point / Path / Field role: none stated (reference value only; "Ground movement must be separated from system movement", C-302 constraint L201-202).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: ψ₀ invariance across scales (Universal / Local / Nested models, L183-195); geometry invariance, drift testing, recursive invariance ❌ (L260-262).
- Conflicts: none.

## A-102 — DISPLACEMENT   (`Nodes/A-102_Displacement.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Foundation Transition Primitive.
- Upstream: A-101.   Downstream / cites: A-103 (chain to A-104).
- Core claim: "Displacement is the reference-dependent separation between a current field state and Ground / Zero." (L38). "No defined ground reference → No measurable displacement." (L51).
- Equations: x = Δ_ref(ψ, ψ₀) (L42, L75, L223); ψ=ψ₀ → x=0; ψ≠ψ₀ → x≠0.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Δ_ref not defined for active ψ representation (L95, L173, L203); recursive validation ❌.
- Conflicts: none.

## A-103 — DIFFERENTIAL   (`Nodes/A-103_Differential.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Relational Primitive.
- Upstream: A-101, A-102.   Downstream / cites: A-104.
- Core claim: "Differential compares two already-defined states." (L150); "Does not create displacement." (L41).
- Equations: Δ(A,B) = A − B (L35, L52); Δx = x₂ − x₁ (L38, L55).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: scale invariance of comparison (L103); cross-scale validation ❌.
- Conflicts: none.

## A-104 — GRADIENT   (`Nodes/A-104_Gradient.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Spatial Organization Primitive.
- Upstream: A-103.   Downstream / cites: A-105.
- Core claim: "Gradient is the spatial expression of Differential." (L177); "Gradient defines spatial organization only." (L186). Gradient must stay separate from curvature and response (L145, L153).
- Equations: Δψᵢⱼ = ψⱼ − ψᵢ (L34); dᵢⱼ = rⱼ − rᵢ; aᵢⱼ = |rⱼ − rᵢ|; eᵢⱼ = (rⱼ − rᵢ)/|rⱼ − rᵢ| (L55-61); ∇ψᵢ ≈ Σⱼ∈N(i) (Δψᵢⱼ/aᵢⱼ)eᵢⱼ (L67); ∇ψ = (∂ψ/∂x, ∂ψ/∂y, ∂ψ/∂z) (L70); uniform → ∇ψ=0.
- Point / Path / Field role: Field — gradient is the field's directional spatial structure (no curl stated).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: geometry weighting, higher-dimensional representation, scale behaviour (L125-128); geometry/recursive/experimental validation ❌.
- Conflicts: none.

## A-105 — RESTORING RESPONSE   (`Nodes/A-105_Restoring_Response.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Field Response Primitive.
- Upstream: A-104.   Downstream / cites: A-106, E-501 Flowback; terminology note touches A-106, A-107, B-201, B-221, C-305, C-310, Book 1 Ch12.
- Core claim: "Restoring Response is the field reaction to gradient imbalance." (L48). Symbol renamed F_OW → R_OW because Book 1 Ch12 denies force-carriers as fundamental (L16-29). "A does not create the gradient." (L134).
- Equations: R_OW = −A(∇ψ) (L45, L57, L91); linear R_OW = −α∇ψ (L60, L97); ∇ψ=0 → R_OW=0 (L100).
- Point / Path / Field role: Field — first-order gradient-opposing response; nothing on Point or Path.
- Magnetism / gravity / rotation link: none stated directly (it is the restoring leg A-115 builds gravity on).
- Open / parked / not-set items: operator A derivation, channel behaviour (Compression/Density, Expression/Phase, Projection — "Open", L81-87), scale validation; experimental validation ❌.
- Conflicts: none.

## A-106 — PRESSURE RESPONSE   (`Nodes/A-106_Pressure_Response.md`)
- Gate / lifecycle: YELLOW / ACTIVE; claim detail "curvature relationship now derived".
- Upstream: A-105.   Downstream / cites: A-107.
- Core claim: Pressure Response is the curvature-generated term P_OW = (b/2)(∇²ψ)² that, together with A-105's gradient term, evades Derrick's theorem and allows a stable bounded 3D state (L36-62, L203-206).
- Equations: P_OW := (b/2)(∇²ψ)² (L38); E[ψ] = ∫[(a/2)(∇ψ)² + V(Δψ) + (b/2)(∇²ψ)²] d³x (L54, L94, L213); rescaling λ⁻¹, λ⁻³, λ¹ (L56); stability I₁ + 6I₂ > 0 ⇔ 2I₃ > I₁ (L60-62); P = R(R_OW) (L65); ∇²ψ ≈ Σⱼ(ψⱼ−ψᵢ)/a² (L91).
- Point / Path / Field role: Field — second-order curvature/compression energy; nothing on Point or Path.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: b not derived; b vs α relationship ❌; b scale behaviour (L139-153, L187).
- Conflicts: none with canonical rules. (Internal note: A-106 calls the gradient term "collapse-favoring" L57; A-107 L124 calls A-106's curvature term "dispersal-favoring" — wording of which term pushes which way is not consistent between the two files.)

## A-107 — BOUNDED MOTION   (`Nodes/A-107_Bounded_Motion.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Motion Constraint Primitive.
- Upstream: A-105, A-106.   Downstream / cites: A-110.
- Core claim: Old criterion V(x)→∞ is "NECESSARY, NOT SUFFICIENT" (L71); corrected criterion "Bounded Motion = TRUE ⟺ 4I₃ − 2I₁ > 0 ⟺ I₃ > I₁/2" (L95). With V=0 the curvature term alone gives a minimum at λ* = √(I₁/I₃) (L102-109).
- Equations: E(λ) = I₁λ⁻¹ + I₂λ⁻³ + I₃λ (L78); I₃ = I₁ + 3I₂ (L81); E''(1) = 2I₁ + 12I₂ = 4I₃ − 2I₁ (L89-92); E_mode < E_escape (L112); V(x) = ∫A(s)ds (L61).
- Point / Path / Field role: none stated (confinement of a field configuration; not a Point spin or Path ride).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: escape threshold derivation ❌; no specific trial profile checked ❌; scale dependence of b (L149-151, L161-164).
- Conflicts: none with canonical rules. (Internal: upstream list omits A-108 although A-108 lists A-107 as downstream.)

## A-108 — LOCAL STABILITY   (`Nodes/A-108_Local_Stability.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Stability Evaluation Primitive.
- Upstream: A-101, A-105.   Downstream / cites: A-107, C-310 Resistance Field ("confirmed distinct from this node", L23, L213).
- Core claim: "Local Stability is the condition where a small displacement from equilibrium produces a restoring response toward the Ground / Zero reference." (L40). "Local Stability ≠ Bounded Motion." (L52).
- Equations: x·A(x) > 0 (L55, L94); F_restore = −A(x) (L62, L82); A(x) = αx, α>0 (L78); V(x) = ½αx² (L86).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: nonlinear A(x) ❌; scale validation ❌.
- Conflicts: none with canonical rules. File defects: still uses "F_restore … Restoring force/response" (L62, L73) after A-105's F→R rename; file is truncated — last line reads "Does not define global confine.iel" (L278) and STATUS line is missing.

## A-109 — INERTIAL MEMORY   (`Nodes/A-109_Inertial_Memory.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Recursive State Persistence Primitive.
- Upstream: A-107.   Downstream / cites: A-110, A-111, C-309 Friction Limit (γ as friction), C-313 Lorentz Invariance Conflict (γ is source of conflict).
- Core claim: "Inertial Memory is the persistence of previous state information through recursive change." (L34). "No Memory → No Recursion." (L228).
- Equations: Δψₙ = ψₙ − ψₙ₋₁ (L38); Mₙ = (1−γ)Δψₙ (L42); ψᵢⁿ⁺¹ = ψᵢⁿ + (1−γ)(ψᵢⁿ−ψᵢⁿ⁻¹) + βᵢ(<ψⱼⁿ>−ψᵢⁿ) (L68).
- Point / Path / Field role: none stated. "Inertial" here = temporal carry-forward of the update, not rotational inertia I.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: memory depth >2 states; γ → operator Γ; coupling beyond nearest neighbour (L141-151); experimental γ ❌.
- Conflicts: none. (Naming hazard only: "inertia" in A-109 is not I in L = Iω.)

## A-110 — OSCILLATION   (`Nodes/A-110_Oscillation.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Dynamic Cycle Primitive.
- Upstream: A-107, A-109.   Downstream / cites: A-111, E-519 Three Fundamental Oscillations, E-524 Kuramoto (unverified).
- Core claim: "Oscillation is repeated ground crossing under bounded motion with inertial memory." (L27); bounded motion + memory alone is insufficient (L33).
- Equations: Ψᵢ(t) = Aᵢ(t)e^{jθᵢ(t)} (L50); Mᵢ = (1−γ)Δψᵢⁿ (L56); θᵢⁿ⁺¹ = θᵢ + ωᵢ + φᵢ (L64); |Mᵢ| < Rᵢ → no overshoot; |Mᵢ| > Rᵢ → crossing (L82-85).
- Point / Path / Field role: none stated as Point/Path/Field. θ is labelled "Phase / rotational position" and ω "Natural rotation frequency" (L41, L45) — this is phase rotation of the complex state, not Point rotation and not stated to carry L.
- Magnetism / gravity / rotation link: phase "rotation" only (above); no magnetism/gravity.
- Open / parked / not-set items: crossing condition, Rᵢ derivation ❌; scale-dependent frequency (L121). Phase 6B (2026-10-03) claims oscillation confirmed on 2D hex lattice (L189-195).
- Conflicts: none with canonical rules. (Ambiguity to flag: "rotation" vocabulary for phase could be misread as Point rotation.)

## A-110a — Wave Equation Derivation   (`Nodes/A-110a_Wave_Equation_Derivation.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Foundation Extension.
- Upstream: A-103, A-104, A-105, A-109, A-110; sibling A-114.   Downstream / cites: C-324 No Entanglement Detector Map, C-315 Wave Reader.
- Core claim: restore + inertia ⇒ 1D wave equation; traveling wave "derived, not assumed" (L20, L124). "If there is no path between the two sites, this formula is not licensed." (L119).
- Equations: R_OW = −α ∂ψ/∂x (L35); ∂R_OW/∂x = −α ∂²ψ/∂x² (L41); μ ∂²ψ/∂t² = α ∂²ψ/∂x² (L53); v² = α/μ (L59); ∂²ψ/∂t² = v² ∂²ψ/∂x² (L65); ψ = f(x−vt)+g(x+vt) (L71); ψ = A cos(kx−ωt+φ), ω = vk (L77); lattice ω(k) ≈ c_L k √(β/2) (L93); s = sign_T(ψ(x_d,t*)) (L104); Δx = vΔt (L110); sin θ ≈ v(τ_L−τ_R)/B (L116).
- Point / Path / Field role: Path — propagation needs a "named path" (L107-119). No Point rotation.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: A not proven linear at all scales; nuclear-scale β, γ unmeasured; full 3D deferred; "Cell-0 oscillation may be fight, not this PDE" (L134-138).
- Conflicts: none.

## A-111 — Recursion   (`Nodes/A-111_Recursion.md`)
- Gate / lifecycle: GREEN / ACTIVE ("Five closure criteria verified via a111_closure_validator.py, Oct 5 2026").
- Upstream: A-109, A-110.   Downstream / cites: A-112, E-520, E-523 Circle Pit Vortex, G-719; audit cites A-115, E-505, E-510, A-114, A-114b; future-work list B-221, B-226, C-302, C-313, D-402, D-410, E-516, G-721, G-724, E-524, E-527, E-528, A-117, D-408, E-507.
- Core claim: "Recursion is a closed update cycle where the output of one step becomes the input of the next. Memory alone is not recursion." (L20). "Oscillation is not required for recursion" (L48) — while the operational chain lists Oscillation + Memory + Feedback ⇒ Recursion (L53).
- Equations: ψ_{n+1} = f(ψ_n, ψ_{n−1}) (L23); full update rule (L35); f^k(ψ)=ψ (L41); Ψ = (A,f,φ,x,t,m) (L63); Ψ_{n+1} = F(Ψ_n, Ψ_{n−1}, M) (L78); ψ(t) = A sin(2πft+φ) (L94); f_b = |f₁−f₂| (L108); f_n = f₀2^{n/12} (L116); D_n = ‖Ψ_n − Ψ_{n−1}‖ (L153); S_R = 1 − |R_n−R_{n−1}|/R_max (L161); S_total = w_R S_R + w_f S_f + w_φ S_φ + w_A S_A (L174-183); lock |Δφ|<θ, |Δf|<δ (L198-205); persistence ‖Ψ_{n+k} − Ψ_n‖ < ε (L241).
- Point / Path / Field role: none stated. Cascade simulator: "Child phase-locks to parent wake frequency" (L290) — parent/child phase locking, not rotation transport.
- Magnetism / gravity / rotation link: none stated (E-523 vortex cited only as downstream).
- Open / parked / not-set items: audit marked closed; earlier open items (ε derivation, nonlocal coupling) listed as resolved by validator (L258-266).
- Conflicts: none with canonical rules. (Internal tension: L48 "Oscillation is not required" vs L53 chain that includes Oscillation; audit L274 "Energy conservation validated" vs A-114b Q10 "conserved quadratic … MISSING".)

## A-112 — Persistent Mode   (`Nodes/A-112_Persistent_Mode.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-111.   Downstream / cites: A-112a; all object nodes in Books 1-6; cites A-101, E-525 sampling operator, C-318 four-interaction architecture.
- Core claim: "A Persistent Mode is a recursively stable non-ground-state pattern." (L19). "Persistence … does not, by itself, define inertia or the Mass Effect; that response belongs to the complete four-interaction architecture in C-318." (L44-47). "Every object in Books 1-6 is a Persistent Mode or a collection of interacting Persistent Modes." (L63).
- Equations: psi_M ≠ psi_0 (L22); psi = psi_0 + delta_psi (L27); M(t) = ∫ W(x) delta_psi(x,t) dx (L36); ‖psi_{n+k} − psi_n‖ < ε (L51); deferred λ_max < 0 (L54).
- Point / Path / Field role: none stated. Inertia/mass explicitly deferred to C-318.
- Magnetism / gravity / rotation link: Phase 6B claims "Unified mode interpretation shows E and B are projections of single persistent ψ field" (L91); Faraday constraint satisfied in continuum limit (L90). No rotation/gravity.
- Open / parked / not-set items: mode type, persistence timescale, failure conditions (incl. "resistance, electrical locking") not specified (L57-61, L74-78); bulk FCC12 experiment: continuum stability, vortex topology, norm selection, real detector coupling, Mass Effect open (L98).
- Conflicts: none.

## A-112a — Traveling Lattice Rupture   (`Nodes/A-112a_Traveling_Lattice_Rupture.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Scale-Specific Persistent-Mode Formalization.
- Upstream: A-112, A-102, A-104, A-105, B-203, B-204, B-209, E-509.   Downstream / cites: Book 5 Ch4 Black Holes and Quasars, future defect simulation.
- Core claim: "A localized rupture can relocate through the lattice without creating an indefinitely lengthening permanent tear, provided rupture content is transported forward while the previous location re-closes." (L25-27). "the rupture relocates; it does not accumulate." (L123). Kinematic only; "does not yet derive black-hole motion" (L29-30).
- Equations: J_{i+1/2}^n = ν_n r_i^n (L53); r_i^{n+1} = r_i^n − ν_n(r_i^n − r_{i−1}^n) (L59-60); ν_n = v_nΔt/Δx (L66); 0 ≤ ν ≤ 1 (L84); R_n = Σ r_i^n, R_{n+1}=R_n (L103-118); O_i, C_i, ΣO = ΣC (L131-144); x_c^n = Δx Σ i r_i^n / R_n (L154); v_n, a_n (L160-167); d_i^{n+1} = clip(d + κ_d[r−r_damage]_+(1−d) − λ_d d, 0,1) (L183-187); W_n, L_scar^n (L215-221).
- Point / Path / Field role: Path — relocation/transport of a defect through the lattice (route, not Point spin). No Point rotation, no curl.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: ν prescribed not derived from pressure asymmetry (L170, L270); numerical diffusion; no black-hole data tie; damage law uncalibrated (L268-278).
- Conflicts: none.

## A-113 — Projection   (`Nodes/A-113_Projection.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-101, A-103, A-104.   Downstream / cites: A-117; all 2D interpretations in Books; CCD-05.
- Core claim: "The 2D view is operational, not ontological. It is a tool, not the framework" (L26). Slice is a special case of projection (L28).
- Equations: ψ_slice(x,y,t) = ψ(x,y,z₀,t) (L39); ψ_proj(x,y,t) = ∫ψ(x,y,z,t)dz (L47); P_2D(G*ψ_3D) ?= G(P_2D*ψ_3D) (L69); L_P = ‖ψ_3D − ψ̂_3D(P_2D(ψ_3D))‖ (L91); F_P = 1 − L_P/L_max (L103); valid if L_P < ε (L116).
- Point / Path / Field role: none stated (projection loses z-gradients/curvature, L60-62; commutation fails if six components (E,C,F,B,U,D) are cross-coupled, L72).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: ground invariance under projection (CCD-05) unresolved; info-loss characterisation; fidelity threshold (L125-131, L157).
- Conflicts: none. (Stray editorial text L14-16 "The full version for the update … Below is the full updated version".)

## A-114 — Dispersion Relation from the Core Update Rule   (`Nodes/A-114_Dispersion_Relation.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: core update rule, E-509 Propagation Limit (c_L = dx/dt).   Downstream / cites: D-405 Harmonic Shell, D-407 calibration.
- Core claim: ω(k) derived from the update rule; "frequency is no longer an arbitrary symbol" (L48-51). D-405 shell mapping resolves negatively: k_n = 2π/λ independent of n (L58-65).
- Equations: ψ_i^n = A z^n e^{ikiΔx}, z = e^{−iωΔt} (L28); C = β(cos(kΔx)−1) (L35); z² − (2−γ+C)z + (1−γ) = 0 (L34); ω² ≈ −C = β(kΔx)²/2 ⇒ ω ≈ c_L k √(β/2) (L40-41); numeric check ω = 0.0049999844 for β=0.5, k=0.01 (L43-45).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Phase 6B claims "Frequency matching: ω_E(k) = ω_B(k) for all k (unified mode)" (L93); open "c*|B| = |E| relation" (L107). No rotation/gravity.
- Open / parked / not-set items: β, γ physical meaning; nuclear-scale β; non-perturbative regime; D-405 shell energy needs a different model (L67-87, L105-109).
- Conflicts: none with canonical rules. (Internal: L83-87 says general-γ "not solved here" while Phase 6B L94 says it is solved/tested.)

## A-114a — Exact Dispersion Roots   (`Nodes/A-114a_Exact_Dispersion_Roots.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-114.   Downstream / cites: A-110a, C-324.
- Core claim: exact roots of the A-114 characteristic quadratic; "Falsifier: a claimed ω that is not arg(z)/Δt for a root of this quadratic on a named lattice." (L61).
- Equations: z² − Sz + P = 0, S = 2−γ+C, P = 1−γ, C = β(cosθ−1), θ = kΔx (L19-23); z_± = [S ± √(S²−4P)]/2 (L29); Δ = γ² + 2(2−γ)C + C² (L35); γ=0: Δ = C(C+4), z_± = 1 + C/2 ± √(C(C+4))/2 (L41-44); ωΔt = −arg(z) (L52).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none beyond Phase 6B claims (L63-75).
- Conflicts: none.

## A-114b — Dispersion Trail — Next Ten Questions   (`Nodes/A-114b_Dispersion_Trail.md`)
- Gate / lifecycle: YELLOW / ACTIVE; Trail / Compare-to-Repo.
- Upstream: A-114 → A-114a → A-110a → C-324.   Downstream / cites: A-112, C-324, NO_ENTANGLEMENT.md, HEX-SPLIT, RABBIT-HOPPING/build/CELL0.md, PHASE_6B_COMPLETION_STATUS.md.
- Core claim: ten scored questions; "|z|=1 is the linear version of persist" (L60); Cell-0 does NOT obey this ω(k) (L71-72).
- Equations: |z₊z₋| = |P| = |1−γ| (L21); ω = −ln(z)/iΔt (L28); v_p ≈ v_g ≈ c_L √(β/2) (L36); γ=0 stability 0<β≤2 (1D) (L42); C_hex = β((1/6)Σe^{ik·e} − 1) (L48); k = 2πm/N (L52).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Q1 general-γ unit circle, Q3 exact v_g, Q4 hex β bound, Q8 forced-site term, Q10 conserved quadratic (L120-125). File has corrupted characters at L21-24 ("|z| \neq 1" rendered as "|z| \neq" line break "eq").
- Conflicts: none.

## A-115 — Unified Compression Field   (`Nodes/A-115_Unified_Compression_Field.md`)
- Gate / lifecycle: frontmatter gate GREEN / ACTIVE; claim detail "YELLOW (field decomposition and static-loop equations) / GREEN (physical identity claims and coefficients)".
- Upstream: A-101, A-102, A-104, A-105, A-106, A-109, A-112, A-116, C-309.   Downstream / cites: Book 1 Ch12 Gravity, C-320, D-413, D-416 Planetary Rotation-Magnetic Coupling Test Matrix, Book 1 Ch14 Mass Effect, Ch15 Higgs, Book 5 Ch1, C-301, C-322, E-528, E-529, E-530, Book 5 Ch4; route via C-311, C-319, C-320, C-318, D-409.
- Core claim: "Gravity, dark-matter behavior, local Mass Effect, and the Mirror-Gate boundary response are measurement views of one displaced, compressed, restoring field." (L22). White Energy "does not mean expansion of space" (L24). D-413 "imposes its curvature depression … does not yet derive the A-115 gravity law" (L41). "A nonzero magnetic field is not allowed to create A-115 gravity by itself when grad(chi)=0." (L117). Mass Effect = "the resistance produced when the entire coupled recurrence must be carried and rebuilt relative to Ground" (L208).
- Equations: χ = −∇·u (L54); ℰ_OW = (ρ_u/2)|∂_t u|² + (K_χ/2)χ² + (S_u/2)|∇u|² + V_b(u) (L63-72); ρ_u∂²_t u + μ_u∂_t u − K_χ∇(∇·u) − S_u∇²u + ∂V_b/∂u = J_source (L77-88); Φ_OW = α_gχ, g₀ = −α_g∇χ (L98-100); g_OW = −α_g K_L ∇χ (L106); K_L → I ⇒ g_OW → g₀ (L111-114); Φ_OW → −GM_eff/r (L122); g₀ = g_local + g_wake (L134); v_c²/r = |g_local + g_wake| (L142); ρ_DM,eff = −(1/4πG_eff)∇·g_wake (L148); Z = (Z_K,Z_E,Z_M,Z_T) (L161); Ē₄ = ⟨E_K+E_E+E_M+E_T+E_×⟩ (L169-171); 𝓜_ij = ∂²Ē₄/∂v_i∂v_j (L183-188); m_eff = ⅓Tr𝓜 (L194); 𝓜_jk = Σ_i ΔV (D_j Z_{0,i})ᵀ W_i (D_k Z_{0,i}) (L200-203); D(ω) = H − ω²W − iω(BBᵀ+Γ), S(ω) = I + 2iωBᵀD(ω)⁻¹B (L214); five-channel static energy accounting u_γ,u_χ,u_ν,u_C,u_W (L225-246) and closed-domain balance (L253-273).
- Point / Path / Field role: Field — compression χ and its gradient are the gravity view. Path — circular-orbit v_c²/r (L142) is a ride readout. No Point rotation / L stated.
- Magnetism / gravity / rotation link: canonical route A-115 → C-311 magnetic rotational view → C-319 lattice reorganisation → C-320 path-weighted response → D-413 → D-416 (L32-39); C-320 is the only node allowed the magnetic path-weighting extension (L103); magnetism cannot create gravity when ∇χ = 0 (L117, L320); C-319/C-320 "is not permission to rewrite the cosmic accounting loop" (L293). Bronze requires a fixed law to reproduce "gravity/rotation/lensing datasets" (L310).
- Open / parked / not-set items: χ(r) from sources; inverse-square recovery; wake profile; four-interaction work metric W_i "still-unclosed" (L206); E-528 coefficient; E-529 coefficients; E-530 budget; C-319/C-320 calibration without breaking K_L → I (L299-306). The K_L = I + κ_R R form and κ_R are not written here (deferred to C-319/C-320).
- Conflicts: none — consistent with g = −α K_L ∇χ, K_L→I baseline, ∇χ=0 → no gravity, no expansion, E-528 redshift, E-530 reinjection. (Gate label oddity: frontmatter GREEN but claim detail says field equations YELLOW.)

## A-116 — Three-Dimensional Spherical Default   (`Nodes/A-116_Three_Dimensional_Spherical_Default.md`)
- Gate / lifecycle: GREEN / ACTIVE; claim detail "YELLOW (minimum-surface geometry) / GREEN (universal application)".
- Upstream: A-102, A-104, A-106, A-107, A-112, A-113, E-504 Surface, E-517.   Downstream / cites: A-117, D-409, Book 1 Ch1, Ch2, C-317 Boundary-Tension Weave, C-321.
- Core claim: "A physical One-Wave structure is three-dimensional and volumetric unless a node explicitly states … 2D" (L20); default stable boundary spherical (L22).
- Equations: E_s = σA (L29); A³ ≥ 36πV² (L35); A_min = (36πV²)^{1/3}, E_s,min = σ(36πV²)^{1/3} (L41-43); r(θ,φ,t) = R₀ + η (L53); η = Σ a_ℓm(t)Y_ℓm (L59); ℓ=0 breathing, ℓ=1 translation, ℓ≥2 shape (L62-64).
- Point / Path / Field role: Point (shape only) — "Rotation, anisotropic coupling, collisions, or internal knot tension may excite ℓ≥2, but deformation must be derived" (L66). No L, no rate.
- Magnetism / gravity / rotation link: rotation may deform the envelope (L66); nothing else.
- Open / parked / not-set items: application to protons, shells, stars, galaxies remains Green (L96).
- Conflicts: none.

## A-117 — Dimensional Integrity and Projection Declaration   (`Nodes/A-117_Dimensional_Integrity_and_Projection_Declaration.md`)
- Gate / lifecycle: YELLOW / ACTIVE; claim detail "BRONZE (canonical separation rule) / YELLOW (cross-dimensional operators)".
- Upstream: A-101, A-102, A-103, A-113, A-116.   Downstream / cites: D-408, D-409, D-410, all physical simulations and wiki pages.
- Core claim: "2D ≠ 3D ≠ 4D" and "6:1 ≠ 12:1 ≠ 24:1" (L25, L31); layers "may not be silently collapsed into one mechanism" (L34). 4D = ordered recurrence of a 3D state, not a hidden fourth volume (L60). Mandatory dimensional declaration (L99-114).
- Equations: P_{D→d}: X_D → X_d (L121); Q(X_D) = Q_d(P X_D) or ε_Q = |Q(X_D) − Q_d(P X_D)| (L130-139).
- Point / Path / Field role: none stated ("ring circulation" is a permitted 2D test, L145 — a Path readout only).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: each ratio transition needs its own operator (L95); failure conditions L153-157.
- Conflicts: none. (Duplicate sentence L72/L74.)

## B-201 — Equilibrium Balance   (`Nodes/B-201_Balance.md`)
- Gate / lifecycle: GREEN / ACTIVE ("GREEN (Yellow Audit Open)").
- Upstream: primitives E, I, R (Resistance), L (Electrical Locking) "defined in Books".   Downstream / cites: B-202, B-206, Restoring Response; distinct from G-709.
- Core claim: "Balance defines the scalar measure of equilibrium between driving and opposing contributions." (L24); "does not define Pressure, Force, or Response" (L26).
- Equations: B = (k_E E + k_I I) − (k_R R + k_L L), all k > 0 (L34-35); B=0 equilibrium, B>0 driving, B<0 restoring (L38-40).
- Point / Path / Field role: none stated. Resistance R appears as an opposing scalar contribution (L31).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: coefficients unknown; nonlinear forms; temporal evolution; physical meaning of E, I, R, L deferred to Books (L49-52).
- Conflicts: none.

## B-202 — Pressure   (`Nodes/B-202_Pressure.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: B-201.   Downstream / cites: Force Density, Local Stability, Bounded Motion (A-107), B-206; E-503 Pressure (Gradient Form) is a specialisation of A-104, not of B-202; E-502 cross-ref.
- Core claim: "Pressure defines the local state generated by imbalance … Pressure is not itself a force … a field quantity, not a surface quantity." (L22-24).
- Equations: P = f(B) (L26); B=0, f(0)=0 → P=0 (L31).
- Point / Path / Field role: Field (scalar pressure state); none on Point/Path.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: constitutive f unspecified; direction/motion via spatial variation not specified (L42-43).
- Conflicts: none. (Still uses "Force Density" in the chain L39, after A-105's force→response rename.)

## B-203 — Expression   (`Nodes/B-203_Expression.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: A-102, A-110.   Downstream / cites: B-204, B-206, B-205, B-206a, B-206b, B-225, G-720; Appendix A Proof A-05b.
- Core claim: "Expression is the outward phase of a one-wave oscillation cycle. The half-cycle in which one system is the transmitter." (L19-20).
- Equations: ψ_i^{n+1} > ψ_i^n (L26); E(ψ) = ψ + β∇ψ (L31-32); P = −c²∇²ψ (L39).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: phase boundary Expression/Compression; amplitude-to-information relation (L45-46).
- Conflicts: none.

## B-204 — Compression   (`Nodes/B-204_Compression.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: A-102, A-110.   Downstream / cites: B-203, B-206, B-205, B-206a, B-206b, B-225, G-720.
- Core claim: "Compression is the inward phase of a one-wave oscillation cycle. The half-cycle in which one system is the receiver." (L19-20). "One system's Expression is another system's Compression input." (L28).
- Equations: ψ_i^{n+1} < ψ_i^n (L26); C(ψ) = ψ − α∇ψ (L32-33), matched to R_OW = −A∇ψ (L37).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: phase boundary; compression depth; threshold link (L45-47).
- Conflicts: none.

## B-205 — Mirror   (`Nodes/B-205_Mirror.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: B-203, B-204.   Downstream / cites: C-301 Mirror Gate, B-206a, B-206b; C-308 Spin-half.
- Core claim: "Mirror is the flip operation between Expression and Compression states." (L19); Mirror Gate C-301 is the location (L21).
- Equations: M(ψ_C, ψ_E) → (ψ_E, −ψ_C) (L25); M = [[0,1],[−1,0]], M² = −I, M⁴ = I ⇒ 4π closure (L29-41); "follows from SU(2) structure of the S3 fiber" (L43).
- Point / Path / Field role: none stated as Point/Path/Field. M is a "symplectic rotation" in (ψ_C, ψ_E) state space (L28) — not a spatial Point rotation and not stated to carry L.
- Magnetism / gravity / rotation link: state-space rotation and spin-half cross-ref (C-308) only.
- Open / parked / not-set items: whether Mirror is forced by geometry or a boundary rule (CCD-03); S3 fiber derivation from update rule (L50-51).
- Conflicts: none with canonical rules. (Flag: "rotation"/"spin-half" vocabulary here is internal-state rotation; must not be read as Point spin.)

## B-206 — Paired Loop   (`Nodes/B-206_Paired_Loop.md`)
- Gate / lifecycle: GREEN / ACTIVE; "GREEN (definition) / YELLOW (threshold dynamics)".
- Upstream: B-201, B-202, B-203, B-204.   Downstream / cites: B-206a, B-206b, B-207, B-215.
- Core claim: "A Paired Loop is a reciprocal exchange between two systems that alternate between Expression and Compression while maintaining a shared state." (L19-20). "Only the participants change. The loop structure remains invariant." (L33).
- Equations: none (loop Express → Compress → Threshold → Return or Break, L30).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: return-vs-break threshold, drift, synchronisation of loops (L50-53).
- Conflicts: none.

## B-206a — Shared Boundary   (`Nodes/B-206a_Shared_Boundary.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: B-203, B-204, B-205, B-206.   Downstream / cites: B-206b, C-301, C-308 Spin-half, "E-503 Surface".
- Core claim: "A Shared Boundary is the common reference interface between paired regions … the shared zero-reference where paired exchange is evaluated." (L20-26); operational form of (0,0) (L33).
- Equations: r = R; ψ_B = ψ(R,θ,t); B = ψ_in(R) − ψ_out(R); E_B = ½k_B B²; E_s = σA_s; hold E_B ≤ E_s; release E_B > E_s; ΔE_B = E_B − E_s; Λ_B = ΔE_B/E_s (L37-75).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (relation to spin-half inversion open, L112).
- Open / parked / not-set items: k_B derivation; surface-tension function; general surfaces; spin-half relation; experiment (L109-113).
- Conflicts: none with canonical rules. (ID mismatch: downstream "E-503 Surface" (L16) while B-202 L18 names E-503 "Pressure (Gradient Form)" and A-116 L15 names "E-504 Surface".)

## B-206b — Four Views — Direction, Phase, Strength, Reference   (`Nodes/B-206b_Four_Views.md`)
- Gate / lifecycle: YELLOW / ACTIVE; descriptive readout vocabulary.
- Upstream: (not listed in frontmatter; cycle M1→A1→M2→A2→M3→A3).   Downstream / cites: B-206c.
- Core claim: four Views "are readout dimensions/modes … not four Mirror gates" (L24); canonical primitive "3 Mirror + 3 Action = 6 gates = 6 steps" (L91).
- Equations: none (ViewState packet L36-41).
- Point / Path / Field role: none stated ("Phase — including handedness/orientation", L29).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: sensors/coordinates implementation-specific; relation to 1D-4D representations (L97-98).
- Conflicts: none.

## B-206c — Four Action Modes — Inward, Outward, Across, Over   (`Nodes/B-206c_Four_Actions.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: (not listed; references B-206b).   Downstream / cites: none listed.
- Core claim: Inward/Outward/Across/Over "are four action modes … not four primitive Action gates" (L22). "Over — carry the resolved relation into a changed orientation, path, cell, or recursive scale" (L33).
- Equations: none.
- Point / Path / Field role: none stated (Over mentions "orientation, path" as vocabulary only).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: mode selection and physical realisation implementation-specific (L104-105).
- Conflicts: none.

## B-207 — Threshold State   (`Nodes/B-207_Threshold.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: B-206, B-206b, B-201.   Downstream / cites: B-208, B-209, B-210, B-216, G-702, G-703; I-04.
- Core claim: scalar T∈[0,100] replaced by state vector "Θ_n = (q_n, a_n, p_n)" (L39); integrity, activation, polarity independent (L50-54).
- Equations: Θ_n = (q_n,a_n,p_n), q∈[0,1], a∈[0,1], p∈[−1,1] (L39-46); Ω = [0,1]×[0,1]×[−1,1], projection Π_Ω (L73-76).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: physical mapping of a, p, q; bands provisional; update law in B-216; calibration (L100-104).
- Conflicts: none.

## B-208 — Threshold Windows   (`Nodes/B-208_Threshold_Windows.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: B-207.   Downstream / cites: B-209, B-210, B-216, G-703, G-714.
- Core claim: "Low activation does not imply break. High activation does not imply connection." (L50-51); break determined by integrity (L116).
- Equations: A = 100a; Q = 100q; activation bands table (L35-42); 85/2 = 42.5 illustration (L93); reset: A ≥ A_danger for N_danger steps AND q falling or < q_safe (L106-107).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: A_danger, q_break, q_safe, N_danger uncalibrated; pivot widths; cross-scale recurrence (L120-125).
- Conflicts: none.

## B-209 — Break Condition   (`Nodes/B-209_Break_Condition.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: B-207, B-208, B-216, G-703, G-714.   Downstream / cites: B-210, B-211, B-213, G-719.
- Core claim: "Break is determined by integrity q, not by activation a." (L26).
- Equations: q_n ≤ q_break ⇒ Break candidate (L29); hysteresis q_break < q_return (L40).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: calibration of q_break/q_return; outcome selection (G-714); allowed time below q_break (L63-65).
- Conflicts: none.

## B-210 — Return   (`Nodes/B-210_Return.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: B-207, B-208, B-216, G-702, G-703, G-714.   Downstream / cites: B-206, B-212.
- Core claim: "Return is successful restoration of loop integrity after evaluation and modulation." (L22).
- Equations: q_{n+1} ≥ q_return AND q_{n+1} ≥ q_n AND danger not increasing (L31-33); [a_{n+1} − a_danger]_+ ≤ [a_n − a_danger]_+ (L39).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: energy/time cost; seven-return Hyperloop claim unvalidated; noisy-trajectory simulation (L57-59).
- Conflicts: none.

## B-211 — Loop Break   (`Nodes/B-211_Loop_Break.md`)
- Gate / lifecycle: GREEN / ACTIVE; "GREEN (definition) / YELLOW (formation dynamics)".
- Upstream: B-209.   Downstream / cites: B-213, B-212, B-215.
- Core claim: "A Loop Break is a Break Condition event that preserves a future access pathway rather than producing complete separation." (L19-20).
- Equations: n_AL = n_LB (L28); n_LB = 7 ⇒ Hyperloop entry (L30).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Loop Break vs separation; degradation; max count (L38-40).
- Conflicts: none with canonical rules. (Internal: B-211 puts Hyperloop entry at 7 Loop Breaks; B-212 counts Returns + Loop Breaks; B-215 L35 shows Return^7.)

## B-212 — Loop Counter   (`Nodes/B-212_Loop_Counter.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: B-210, B-211.   Downstream / cites: B-215, B-214.
- Core claim: "n_loop = count of successful Returns and Loop Breaks" (L22); "n_loop ≥ 7 ⇒ Hyperloop entry" (L28).
- Equations: n_loop += 1 on Return or Loop Break (L25-26).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: fixed vs coupling-dependent 7; reset behaviour; partial loops (L37-39).
- Conflicts: none (see B-211 counting note).

## B-213 — Access Line   (`Nodes/B-213_Access_Line.md`)
- Gate / lifecycle: GREEN / ACTIVE.
- Upstream: B-211.   Downstream / cites: B-214, B-215, B-217, G-719.
- Core claim: "An Access Line is a persistent recursive pathway established when a Paired Loop undergoes a Loop Break that preserves future exchange." (L19-20). "Access Lines are pathways, not participants." (L21).
- Equations: n_AL = n_LB; n_AL_max = 7; AL_1…AL_7 (L28-30).
- Point / Path / Field role: none stated (pathway is relational, not a physical ride).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: eight open questions on formation, persistence, merging, roles, selection, reactivation, strengthening, directionality (L41-48).
- Conflicts: none.

## B-214 — Recursive Access Growth   (`Nodes/B-214_Recursive_Access_Growth.md`)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: B-213, B-212.   Downstream / cites: B-215, B-217, B-218.
- Core claim: "Recursive Access Growth is the process by which successive Loop Breaks expand the available communication structure between a coupled pair." (L19-20).
- Equations: n_AL(k) = k; d_k = d_0 + k; k=7 ⇒ Hyperloop (L29-31).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: linear depth approximation; d_0; saturation; meaning of levels (L39-42).
- Conflicts: none.

## B-215 — Hyperloop   (`Nodes/B-215_Hyperloop.md`)
- Gate / lifecycle: GREEN / ACTIVE; "GREEN (concept) / YELLOW (threshold conditions and mathematics)".
- Upstream: B-212, B-213, B-214.   Downstream / cites: B-218.
- Core claim: "The Hyperloop is not a new interaction. It is a higher operating regime of the same Paired Loop." (L21-22).
- Equations: n_loop ≥ 7 ⇒ Hyperloop (L32); C_correction^Hyperloop < C_correction^PairedLoop; σ_Hyperloop < σ_PairedLoop (L38-39).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: fixed 7; C_correction; return definition; decay; Access Line roles; measurable signature (L49-54).
- Conflicts: none.

## Slice summary

### (a) Nodes in this slice bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking
- A-104 Gradient — defines ∇ψ, the Field gradient used by every restoring/gravity view; no curl defined.
- A-105 Restoring Response — R_OW = −A(∇ψ); the Field restoring leg A-115 builds gravity on; renames "force" to "response".
- A-106 Pressure Response — curvature energy (b/2)(∇²ψ)²; Field compression term that permits bounded 3D states.
- A-107 Bounded Motion — I₃ > I₁/2 confinement criterion for field configurations; not Point or Path rotation.
- A-108 Local Stability — x·A(x) > 0; points to C-310 Resistance Field as a distinct downstream node.
- A-109 Inertial Memory — temporal carry-forward (1−γ); "inertia" here is update memory, not rotational inertia I; feeds C-309 friction and C-313.
- A-110 Oscillation — phase θ called "rotational position", ω "natural rotation frequency": phase rotation only, no L.
- A-110a Wave Equation — traveling wave needs a named path (Path); μ "inertia density" in the 1D wave equation.
- A-111 Recursion — cascade child phase-locks to parent wake frequency (parent/child locking in phase, not rotation transport).
- A-112 Persistent Mode — defers inertia and Mass Effect to C-318; says E and B are projections of one ψ field (Phase 6B).
- A-112a Traveling Lattice Rupture — Path-type relocation of a lattice defect; conserved rupture content.
- A-114 Dispersion — ω_E(k) = ω_B(k) unified-mode claim; c|B| = |E| open.
- A-115 Unified Compression Field — gravity g₀ = −α_g∇χ; g_OW = −α_g K_L∇χ; K_L → I baseline; magnetism cannot make gravity when ∇χ = 0; Mass Effect = resistance of carrying the recurrence; circular-orbit v_c²/r; no expansion; E-528/E-529/E-530; magnetism route C-311 → C-319 → C-320 → D-413 → D-416.
- A-116 Spherical Default — rotation may excite ℓ ≥ 2 deformation of the 3D envelope; D-409 coordination.
- A-117 Dimensional Integrity — 6:1 / 12:1 / 24:1 lattice coordination layers must stay separate.
- B-201 Equilibrium Balance — Resistance R and Electrical Locking L are opposing scalar primitives (defined in Books).
- B-202 Pressure — field-quantity pressure P = f(B).
- B-205 Mirror — symplectic state-space rotation, M⁴ = I, 4π closure, spin-half C-308; not spatial Point spin.
- B-206a Shared Boundary — boundary energy vs surface hold (σA_s); spin-half relation open.

### (b) Conflicts found
No file in this slice contradicts the canonical Point/Path/Field, L-bookkeeping, magnetism-opens-the-point, gravity-from-∇χ, parent/child transport, bound-lattice, or no-expansion rules. A-115 matches the canonical gravity/magnetism separation; it does not write K_L = I + κ_R R or say κ_R is unset, and leaves that to C-319/C-320.
Non-canonical issues to flag:
1. A-108 L278: file truncated ("Does not define global confine.iel"), STATUS missing; A-108 L62/L73 still uses "F_restore … force" after A-105's F_OW → R_OW rename (A-105 L16-29). B-202 L39 still says "Force Density".
2. A-106 L57 vs A-107 L124: they describe the gradient and curvature terms' collapse/dispersal roles differently.
3. A-107 upstream omits A-108, but A-108 L22 lists A-107 as downstream.
4. A-111 L48 "Oscillation is not required for recursion" vs L53 chain that includes Oscillation; A-111 L274 "Energy conservation validated" vs A-114b Q10 "conserved quadratic MISSING".
5. A-114 L83-87 says general-γ is "not solved here", but Phase 6B L94 says it was solved and tested.
6. E-503 ID mismatch: B-206a L16 says "E-503 Surface", B-202 L18 says "E-503 Pressure (Gradient Form)", and A-116 L15 says "E-504 Surface".
7. Hyperloop counting: B-211 L30 counts 7 Loop Breaks, B-212 L22 counts Returns + Loop Breaks, and B-215 L35 counts Return^7.
8. Vocabulary hazard, not a contradiction: A-110 L41/L45 ("rotational position", "rotation frequency") and B-205 L28 ("symplectic rotation", spin-half) use rotation words for phase or state-space rotation, which could be confused with G-749 Point rotation. A-109 "inertial" means memory, not I.
9. A-115 frontmatter says gate GREEN while claim_gate_detail says the field equations are YELLOW. A-114b L21-24 has corrupted characters. A-113 L14-16 has stray editorial text. A-117 repeats a sentence at L72 and L74.

### (c) Cross-references outside this slice relevant to point rotation or magnetism
- C-311 magnetic rotational view, C-319 magnetic lattice reorganization (K_L), C-320 Magnetic-Compression Path Coupling — A-115 L32-39, L103-117, L293, L324.
- D-413 Ground Lattice Orbital-Restoring Simulation; D-416 Planetary Rotation-Magnetic Coupling Test Matrix — A-115 L16, L28-41, L313.
- C-318 four-interaction architecture (inertia / Mass Effect, work metric W) — A-112 L44-47; A-115 L158-216.
- C-310 Resistance Field — A-108 L23, L213.
- C-309 Friction Limit (γ), C-313 Lorentz Invariance Conflict — A-109 L18; A-115 L15, L335.
- C-308 Spin-half — B-205 L44, B-206a L16.
- C-301 Mirror Gate, C-322 125 GeV boundary response — A-115 L16, L214; B-205.
- E-528 Static Redshift Transport, E-529 Low-Coupling Return Mode, E-530 White Energy Recirculation — A-115 L16, L220, L303-305.
- E-523 Circle Pit Vortex Transition, E-524 Kuramoto Lattice Synchronization — A-111 L16, L371-379; A-110 L18.
- D-409 Twelvefold 3D Coordination, D-408 Sixfold 2D Lattice, D-410 24:1 shell — A-116, A-117.
- C-317 Boundary-Tension Weave, C-321 — A-116 L16.
- Book 1 Ch12 Gravity, Ch14 Mass Effect — A-115 L16; A-105 L16-29.
- Solvers: discrete_maxwell_solver_v4.py, faraday_scaling_test.py (E/B unified-mode claims, A-112 L87-92, A-114 L89-97); solvers/joint_boundary_response.py (A-115 L343-349).
