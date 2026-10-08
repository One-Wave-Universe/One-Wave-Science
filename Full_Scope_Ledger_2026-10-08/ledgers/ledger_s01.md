# Ledger — slice s01

Files read in full: 2 of 2.
1. `/home/user/One-Wave-Science/.github/PULL_REQUEST_TEMPLATE.md` (29 lines)
2. `/home/user/One-Wave-Science/AI_Readable_Packs/Appendix_A.md` (4387 lines; read lines 1-4388 in three pages). It is a pack of 20 node sources (A+101 .. A-117); each gets its own section below in file order.

Line numbers below are line numbers in the file named in the section heading.

---

## (no node) — One-Wave Update Record / PR template   (`.github/PULL_REQUEST_TEMPLATE.md`)
- Gate / lifecycle: none (process template).
- Upstream: none.   Downstream / cites: none by ID. Asks for "Authoritative node / chapter / math reference" (L5).
- Core claim: Every PR must fill CORE-RULES-PRE (L3-6), MATH-BACKBONE (math preserved/added/superseded, "MATH-REBUILD-REQUIRED items", L8-13), Change, Test/Comparison ("accepted-reference comparisons, tolerances, and pass/fail results", L21), CORE-RULES-POST incl. "YELLOW / OPEN items" and "Drift detected: YES / NO" (L23-29).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

---

## A+101 — ONE FIELD GROUND   (`AI_Readable_Packs/Appendix_A.md` L7-190)
- Gate / lifecycle: GREEN / ACTIVE; ROOT AXIOM (L13-16, L190).
- Upstream: none.   Downstream / cites: A-101 and all A-Series; chain A-101..A-113 (L76-89).
- Core claim: "There is one field." (L37); "All later primitives describe field behavior, not separate entities." (L47).
- Equations: ψ = ψ (L63, L180); ψ₀ = reference condition of ψ (L67).
- Point / Path / Field role: Field = the one field ψ; Point and Path not stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: "How field continuity is represented across scales." (L120); Recursive Validation ❌ (L161).
- Conflicts: none.

## A+102 — POSITIVE DISPLACEMENT EXPRESSION   (Appendix_A.md L194-375)
- Gate / lifecycle: YELLOW / ACTIVE (L200-201).
- Upstream: A-102; reference A-101.   Downstream / cites: A+103 (L213-215).
- Core claim: "Expresses the positive directional component of established displacement." (L363).
- Equations: +Δψ = P+(x) (L234); P+(x)= x if x>0, 0 if x≤0 (L258-260); P+(x)=(x·e+)e+ (L264); |e+|=1 (L249); +Δψ=P+(Δ_ref(ψ,ψ₀)) (L271, L367).
- Point / Path / Field role: none stated (orientation operator only).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: e+ invariance across scales (L308); General Representation ❌, Recursive Validation ❌ (L348-349).
- Conflicts: none.

## A+103 — DIFFERENTIAL EXPRESSION / POSITIVE DIFFERENTIAL   (Appendix_A.md L379-586)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-103.   Downstream / cites: A-104 (L398-399).
- Core claim: "A+103 is the positive expression of an existing Differential relationship." (L572).
- Equations: D+(Δx)=Δx when Δx>0; 0 when Δx≤0 (L423-425, L446-450); D+(Δx)+D−(Δx)=Δx (L520).
- Point / Path / Field role: none stated. Explicitly "Does not define spatial direction, response, or motion." (L478).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: positive-direction invariance across scales (L507); "Growth and instability boundary remains open." (L516); D− not yet defined ("when defined", L518).
- Conflicts: none.

## A-101 — GROUND / ZERO   (Appendix_A.md L590-880)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A+101.   Downstream / cites: A-102, A-103; cites E-517 Negative Space (L651), B-223 Move, B-224 Choice (L668-669); constraints C-301..C-305 (L789-802) and failure modes F-601..F-605 (L817-835) used as local labels.
- Core claim: "Ground / Zero is the reference state required for measurement." (L625); Void = ψ=ψ₀ "the zero/reference condition within the one field" (L631-632); Void as region = "the set of points currently satisfying ψ=ψ₀" (L647-649); "The void is the absence of defined compression, not the absence of the field itself." (L656-657).
- Equations: x = ψ − ψ₀ (L681, L703, L871); ψ=ψ₀ → x=0; ψ≠ψ₀ → x≠0 (L696-698); same-ground Δx = ψₙ − ψₙ₋₁ (L729).
- Point / Path / Field role: Field reference only (Void = zero compression). Point/Path none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: invariance of ψ₀ across scales; Universal / Local / Nested ground models (L775-786); Geometry Invariance ❌, Long-Term Drift ❌, Recursive Invariance ❌ (L851-853). Operational chain Void→Move→Choice→New State (L668).
- Conflicts: none against canonical rules. Note: local labels C-301..C-305 and F-601..F-605 here are generic constraint/failure tags, not the canonical C-301 Mirror Gate etc. (label collision with canonical C-series IDs; same reuse in A-109 L609-622 and A-110 L816-829).

## A-102 — DISPLACEMENT   (Appendix_A.md L884-1118)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-101.   Downstream / cites: A-103, A-104 (L985-991).
- Core claim: "Displacement is the measurable separation between a current field state and a defined Ground / Zero reference." (L1104).
- Equations: x = Δ_ref(ψ, ψ₀) (L927, L1108); ψ=ψ₀ → x=0; ψ≠ψ₀ → x≠0 (L953-955).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Δ_ref invariance across representations/scales (L1039); Representation Definition ❌, Recursive Validation ❌ (L1088-1089).
- Conflicts: none.

## A-103 — DIFFERENTIAL   (Appendix_A.md L1122-1287)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-101, A-102.   Downstream / cites: A-104.
- Core claim: "Differential compares two already-defined states." (L1273).
- Equations: Δ(A,B)=A−B (L1158, L1276); Δx=x₂−x₁ (L1161).
- Point / Path / Field role: none stated. "Spatial organization belongs to A-104." (L1219).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: scale invariance of comparison (L1226); Cross-scale Validation ❌ (L1259).
- Conflicts: none.

## A-104 — GRADIENT   (Appendix_A.md L1291-1482)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-103.   Downstream / cites: A-105.
- Core claim: "Gradient is the spatial expression of Differential." (L1469); defined on lattice sites i, neighbors N(i) (L1336-1338).
- Equations: Δψᵢⱼ = ψⱼ − ψᵢ (L1326); dᵢⱼ = rⱼ − rᵢ; aᵢⱼ = |rⱼ − rᵢ|; eᵢⱼ = (rⱼ−rᵢ)/|rⱼ−rᵢ| (L1347-1353); ∇ψᵢ ≈ Σⱼ∈N(i)(Δψᵢⱼ/aᵢⱼ)eᵢⱼ (L1359); ∇ψ=(∂ψ/∂x,∂ψ/∂y,∂ψ/∂z) (L1362); uniform ψᵢ=ψⱼ → ∇ψ=0 (L1365).
- Point / Path / Field role: Field — gradient is the Field's spatial structure. Point/Path none stated. "Gradient is confused with curvature" listed as failure (L1437).
- Magnetism / gravity / rotation link: none stated (no curl).
- Open / parked / not-set items: geometry weighting, higher-dimensional representation, scale behavior (L1417-1420); Geometry/Recursive/Experimental validation ❌ (L1453-1455).
- Conflicts: none.

## A-105 — RESTORING RESPONSE   (Appendix_A.md L1486-1717)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-104.   Downstream / cites: A-106, E-501 Flowback (L1520, L1603); terminology note cites A-106, A-107, B-201, B-221, C-305, C-310, Book 1 Ch12, Ch1, Ch2, Ch7 (L1503-1516).
- Core claim: "Restoring Response is the field reaction to gradient imbalance." (L1535). Symbol F_OW renamed R_OW because "Book 1 Ch12 explicitly and repeatedly denies force-carrier mechanisms as fundamental" (L1503-1511).
- Equations: R_OW = −A(∇ψ) (L1532, L1544, L1708); linear R_OW = −α∇ψ (L1547, L1584); ∇ψ=0 → R_OW=0 (L1587).
- Point / Path / Field role: Field response (to gradient). Point/Path none stated.
- Magnetism / gravity / rotation link: none stated directly; the rename references Book 1 Ch12 (Gravity) no-force-carrier stance.
- Open / parked / not-set items: channel extensions Compression/Density, Expression/Phase, Projection "Open" (L1568-1574); operator derivation; scale validation; Experimental validation ❌ (L1691).
- Conflicts: none.

## A-106 — PRESSURE RESPONSE   (Appendix_A.md L1721-1943)
- Gate / lifecycle: YELLOW / ACTIVE; "curvature relationship now derived" (L1730).
- Upstream: A-105.   Downstream / cites: A-107.
- Core claim: "Pressure Response is the curvature-generated energy term P_OW = (b/2)(∇²ψ)², which combines with A-105's gradient term in a single energy functional to resolve ... Derrick's theorem" (L1925-1928).
- Equations: P_OW := (b/2)(∇²ψ)² (L1760); E[ψ] = ∫[(a/2)(∇ψ)² + V(Δψ) + (b/2)(∇²ψ)²] d³x (L1776, L1816, L1935); scaling λ⁻¹, λ⁻³, λ¹ (L1778); stability I₁+6I₂>0 ⟺ 2I₃>I₁ (L1783-1784); P = R(R_OW) (L1787); ∇²ψ ≈ Σⱼ(ψⱼ−ψᵢ)/a² (L1813).
- Point / Path / Field role: Field (curvature/compression energy term). Point/Path none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: b scale-invariance; b vs A-105 α (L1862-1863, L1900, L1909); b>0 required (L1868); simulation validation not promoted to Bronze (L1910-1911).
- Conflicts: none against canonical rules. Internally consistent with A-107 (I₁+6I₂>0 ≡ 2I₁+12I₂>0; 2I₃>I₁ ≡ 4I₃−2I₁>0).

## A-107 — BOUNDED MOTION   (Appendix_A.md L1947-2183)
- Gate / lifecycle: YELLOW / ACTIVE; "stability criterion corrected" (L1956).
- Upstream: A-105, A-106 (also A-108 per A-108's own list).   Downstream / cites: A-110.
- Core claim: "Bounded Motion is the condition where the combined gradient+curvature+potential energy functional has a genuine, non-degenerate minimum under spatial rescaling — concretely, I₃ > I₁/2" (L2168-2170); old V(x)→∞ criterion "NECESSARY, NOT SUFFICIENT" (L2019).
- Equations: E(λ) = I₁λ⁻¹ + I₂λ⁻³ + I₃λ (L2026); stationarity I₃ = I₁ + 3I₂ (L2029); E''(1) = 2I₁ + 12I₂ = 4I₃ − 2I₁ (L2037-2040); criterion I₃ > I₁/2 (L2043); V=0 case λ* = √(I₁/I₃) (L2052); E_mode < E_escape (L2060); I₁,I₂,I₃ definitions (L2011-2013).
- Point / Path / Field role: none stated explicitly ("motion" = confinement of a field profile, not a Path/orbit).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: escape threshold derivation; specific-profile check of I₃>I₁/2; whether realistic b satisfies it; scale behavior (L2109-2112, L2139-2145).
- Conflicts: none.

## A-108 — LOCAL STABILITY   (Appendix_A.md L2187-2466)
- Gate / lifecycle: YELLOW / ACTIVE (frontmatter); closure section has no STATUS line.
- Upstream: A-101, A-105.   Downstream / cites: A-107, C-310 Resistance Field ("checked directly, confirmed distinct from this node, not redundant", L2211, L2401).
- Core claim: "a small displacement from equilibrium produces a restoring response toward the Ground / Zero reference" (L2228).
- Equations: x·A(x)>0 (L2243, L2282); F_restore=−A(x) (L2250, L2270); A(x)=αx, α>0 (L2266); V(x)=½αx² (L2274).
- Point / Path / Field role: none stated. Cites C-310 Resistance Field (resistance) as downstream but gives no content on it.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: nonlinear A(x), scale validation (L2435-2437).
- Conflicts: none against canonical rules. Internal: uses "F_restore" / "Restoring force/response" (L2250, L2261, L2270) after A-105 L1503-1511 says the "Force" symbol was renamed to R_OW everywhere; A-108 was not updated. Closure text truncated: "Does not define global confine.iel" (L2466).

## A-109 — INERTIAL MEMORY   (Appendix_A.md L2470-2703)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-107.   Downstream / cites: A-110, A-111, C-309 Friction Limit ("γ as the friction mechanism"), C-313 Lorentz Invariance Conflict ("γ is the source of the conflict") (L2489).
- Core claim: "Inertial Memory is the field property that carries previous state information into the next recursive update." (L2687); "Field memory represents motion history, not static storage only." (L2617).
- Equations: Δψₙ = ψₙ − ψₙ₋₁ (L2509, L2691); Mₙ=(1−γ)Δψₙ (L2513); ψᵢⁿ⁺¹ = ψᵢⁿ + (1−γ)(ψᵢⁿ−ψᵢⁿ⁻¹) + βᵢ(<ψⱼⁿ>−ψᵢⁿ) (L2539); γ=0 full carry, γ=1 none (L2530-2534).
- Point / Path / Field role: none stated as Point/Path/Field. It is the persistence ("inertial") term of the core update; no L, no I, no ω.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: memory depth beyond two states; γ → operator Γ; coupling range beyond nearest-neighbor (L2613-2622); γ experimentally unconstrained (L2658).
- Conflicts: none against canonical rules. Symbol note: γ here is memory damping / friction (C-309); canonical closed-gradient rule dL/dt = −γ L also uses γ — same letter, different stated role; do not merge without a cited identification.

## A-110 — OSCILLATION   (Appendix_A.md L2707-2895)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-107, A-109.   Downstream / cites: A-111; E-519 Three Fundamental Oscillations; E-524 Kuramoto Lattice Synchronization ("candidate coupling extension, unverified") (L2726).
- Core claim: "Oscillation is repeated ground crossing generated by bounded motion combined with inertial memory." (L2883); "Bounded Motion + Inertial Memory alone does NOT guarantee Oscillation." (L2741).
- Equations: Ψᵢ(t)=Aᵢ(t)e^{jθᵢ(t)} (L2758, L2886); Mᵢ=(1−γ)Δψᵢⁿ (L2764); θᵢⁿ⁺¹=θᵢ+ωᵢ+φᵢ (L2772); |Mᵢ|<Rᵢ no crossing, |Mᵢ|>Rᵢ crossing (L2790-2793).
- Point / Path / Field role: none stated as Point/Path/Field. θᵢ = "Phase / rotational position", ωᵢ = "Natural rotation frequency" (L2750, L2753) — this is phase rotation of a site oscillator, not Point rotation (no L, no I).
- Magnetism / gravity / rotation link: rotation only in the phase sense above; magnetism/gravity none stated.
- Open / parked / not-set items: crossing threshold; Rᵢ derivation; amplitude/phase separation; scale-dependent frequency (L2816-2829).
- Conflicts: none against canonical rules. Terminology risk: "rotation frequency" ωᵢ for phase advance could be misread as Point ω of G-749 (L = I ω); file does not make that claim.

## A-111 — Recursion   (Appendix_A.md L2899-3154)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-109, A-110.   Downstream / cites: A-112; E-520 Recursive Self-Modeling Levels; E-523 Circle Pit Vortex Transition ("real published-physics structural parallel"); G-719 Neural System Functional Analogy Map (L2915-2916).
- Core claim: "Recursion is a closed update cycle where the output of one step becomes the input of the next. Memory alone is not recursion." (L2920); "Oscillation is not required for recursion" (L2948).
- Equations: ψ_{n+1}=f(ψ_n,ψ_{n−1}) (L2923); full update rule (L2935); f^k(ψ)=ψ (L2941); Ψ=(A,f,φ,x,t,m) (L2963); Ψ_{n+1}=F(Ψ_n,Ψ_{n−1},M) (L2978); ψ(t)=A sin(2πft+φ) (L2994); f_b=|f₁−f₂| (L3008); f_n=f₀2^{n/12} (L3016); R=f₂/f₁ (L3024); D_n=‖Ψ_n−Ψ_{n−1}‖ (L3053); S_R=1−|R_n−R_{n−1}|/R_max (L3061); S_total = w_R S_R + w_f S_f + w_φ S_φ + w_A S_A (L3074-3082); phase lock |Δφ|<θ, |Δf|<δ (L3098-3104); selection D_n<ε or S_total>S_threshold, E_total<E_limit (L3114-3126); persistence ‖Ψ_{n+k}−Ψ_n‖<ε (L3141).
- Point / Path / Field role: none stated. "Phase lock" (L3093-3107) is a locking criterion in phase/frequency, not tied to rotation or lattice organization.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: nonlocal effects beyond nearest neighbor (L2946); "Yellow Audit" heading present but empty (L3154).
- Conflicts: none.

## A-112 — Persistent Mode   (Appendix_A.md L3158-3244)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-111.   Downstream / cites: A-112a; all object nodes in Books 1-6; cites A-101, E-525, Ch9 (L3184-3193); C-318 (L3208).
- Core claim: "A Persistent Mode is a recursively stable non-ground-state pattern. A Persistent Mode is not a particle. It is the field doing something stable." (L3178-3179); "Persistence ... does not, by itself, define inertia or the Mass Effect; that response belongs to the complete four-interaction architecture in C-318." (L3205-3208).
- Equations: psi_M != psi_0 (L3181); psi = psi_0 + delta_psi (L3186); M(t) = ∫ W(x) delta_psi(x,t) dx (L3198); ‖psi_{n+k} − psi_n‖ < ε (L3212); lambda_max < 0 (deferred, L3215).
- Point / Path / Field role: none stated. Inertia explicitly deferred to C-318.
- Magnetism / gravity / rotation link: none stated. Failure-mode list includes "resistance, electrical locking" (L3222) with no content.
- Open / parked / not-set items: mode type, persistence timescale, failure conditions all unset (L3219-3222, L3235-3239); analytical criterion deferred (L3215-3216).
- Conflicts: none.

## A-112a — Traveling Lattice Rupture   (Appendix_A.md L3248-3527)
- Gate / lifecycle: YELLOW / ACTIVE; "kinematic Yellow model" (L3278).
- Upstream: A-112, A-102, A-104, A-105, B-203 Expression, B-204 Compression, B-209 Break Condition, E-509 Propagation Limit (L3264-3266).   Downstream / cites: Book 5 Ch4 Black Holes and Quasars; future lattice-defect simulation (L3267-3268).
- Core claim: "A localized rupture can relocate through the lattice without creating an indefinitely lengthening permanent tear, provided rupture content is transported forward while the previous location re-closes." (L3274-3276); "the rupture relocates; it does not accumulate." (L3372).
- Equations: J_(i+1/2)^n = nu_n r_i^n (L3302); r_i^(n+1) = r_i^n − nu_n(r_i^n − r_(i−1)^n) (L3308-3309); nu_n = v_n Δt/Δx (L3315); 0 ≤ nu ≤ 1 (L3333); R_n = Σ r_i^n, R_(n+1)=R_n (L3352, L3366); O_i, C_i, ΣO=ΣC (L3380-3392); x_c, v_n, a_n (L3403-3416); damage d update (L3432-3436); W_n, L_scar (L3464-3470).
- Point / Path / Field role: Path-like — relocation of a defect through the lattice (route/transport), no L, no rotation. Field: rupture occupancy r is a lattice field. Point: none stated.
- Magnetism / gravity / rotation link: none stated. "The physical law that determines nu_n from pressure asymmetry remains open." (L3419).
- Open / parked / not-set items: nu prescribed, not derived; numerical diffusion; no tie to measured black-hole quantities; damage law uncalibrated (L3519-3527).
- Conflicts: none.

## A-113 — Projection   (Appendix_A.md L3531-3691)
- Gate / lifecycle: YELLOW / ACTIVE.
- Upstream: A-101, A-103, A-104.   Downstream / cites: A-117; all 2D interpretations (L3553-3554); CCD-05 (L3657).
- Core claim: "The 2D view is operational, not ontological. It is a tool, not the framework" (L3558); "A slice is one special case of projection." (L3560).
- Equations: ψ_slice(x,y,t)=ψ(x,y,z₀,t) (L3571); ψ_proj=∫ψ dz (L3579); P_2D(G*ψ_3D) ?= G(P_2D*ψ_3D) (L3601); L_P = ‖ψ_3D − ψ̂_3D(P_2D(ψ_3D))‖ (L3623); F_P = 1 − L_P/L_max (L3635); valid when L_P<ε (L3648).
- Point / Path / Field role: none stated. Lost info includes z-gradients and z-curvature (L3592-3594).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: ground invariance under projection (CCD-05) unresolved; information loss incomplete; validity conditions not formalized (L3661-3663). Stray authoring text "The full version for the update" (L3546-3548).
- Conflicts: none.

## A-114 — Dispersion Relation from the Core Update Rule   (Appendix_A.md L3695-3804)
- Gate / lifecycle: YELLOW / ACTIVE ("derived and numerically verified", L3704).
- Upstream: core update rule; E-509 Propagation Limit (c_L = dx/dt) (L3711-3712).   Downstream / cites: D-405 Harmonic Shell, D-407 calibration (L3713-3714); A-112 (L3796).
- Core claim: core update rule gives ω(k) ≈ c_L k √(β/2) for small k, small γ (L3737); for D-405 geometry k_n = 2π/λ independent of n, so no energy ladder from ω(k) alone (L3754-3761).
- Equations: psi_i^n = A z^n e^{ik i dx}, z=e^{−iωdt} (L3724); z² − (2 − γ + C)z + (1 − γ) = 0, C = β(cos(k dx) − 1) (L3730-3731); ω² ≈ −C = β(k dx)²/2 (L3736); ω(k) ≈ c_L k √(β/2) (L3737); numeric check ω=0.0049999844 vs 0.005 (L3739-3741).
- Point / Path / Field role: none stated (ω is a wave frequency, not point spin).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: β unmeasured; small-k/small-γ only; general-γ damped case unsolved; D-405 needs a different shell-energy model; Hoyle-state deferred (L3763-3804).
- Conflicts: none.

## A-115 — Unified Compression Field   (Appendix_A.md L3808-4111)
- Gate / lifecycle: GREEN / ACTIVE; claim gate "YELLOW (field decomposition and static-loop equations) / GREEN (physical identity claims and coefficients)" (L3814-3817).
- Upstream: A-101, A-102, A-104, A-105, A-106, A-109, A-112, A-116, C-309 Friction Limit (L3824).   Downstream / cites: Book 1 Ch12 Gravity, Ch14 Mass Effect, Ch15 Higgs, Book 5 Ch1 Galaxies and Dark Matter, C-301 Mirror Gate, C-322 Mirror-Gate 125 GeV Boundary Response, E-528 Static Redshift Transport, E-529 Low-Coupling Return Mode, E-530 White Energy Recirculation, Book 5 Ch4 (L3825); also C-318 (L3932-3980).
- Core claim: "Gravity, dark-matter behavior, local Mass Effect, and the Mirror-Gate boundary response are measurement views of one displaced, compressed, restoring field." (L3831); "White Energy ... does not mean expansion of space." (L3833); "One-Wave uses no scale factor and no expansion of space. Redshift is handled by E-528" (L4013); "This is circulation and replacement, not expansion." (L4069).
- Equations: χ = −∇·u (L3846); ℰ_OW = (ρ_u/2)|∂_t u|² + (K_χ/2)χ² + (S_u/2)|∇u|² + V_b(u) (L3856-3864); ρ_u∂²_t u + μ_u∂_t u − K_χ∇(∇·u) − S_u∇²u + ∂V_b/∂u = J_source (L3870-3880); Φ_OW = α_g χ, g_OW = −∇Φ_OW = −α_g∇χ (L3890-3892); Φ_OW → −GM_eff/r, |g| → GM_eff/r² (L3898-3900); g_OW = g_local + g_wake (L3910); v_c²/r = |g_local + g_wake| (L3918); ρ_DM,eff = −(1/4πG_eff)∇·g_wake (L3924); Z=(Z_K,Z_E,Z_M,Z_T) (L3934); Ē₄ = ⟨E_K+E_E+E_M+E_T+E_×⟩ (L3943); ℳ_ij = ∂²Ē₄/∂v_i∂v_j (L3957); m_eff = ⅓Tr ℳ (L3968); discrete ℳ_jk (L3975); E_MG = Ē₄(q_G) − Ē₄(q₀) (L3989); E_MG ≈ 125 GeV (L4000); m_eff ≠ E_MG/c² as causal derivation (L4006); five-reservoir transfer equations u_γ, u_χ, u_ν, u_C, u_W (L4018-4038); closed-domain balance (L4046-4050); stationary-transfer equalities (L4056-4066); unified loop (L4073-4084).
- Point / Path / Field role: Field — compression χ, gradient g = −α_g∇χ, wake g_wake ("retained or wake-like compression", L3913). Path — circular motion v_c²/r (L3918) is the orbit/ride. Point — none stated (no spin, no L). Mass Effect = "the resistance produced when the entire coupled recurrence must be carried and rebuilt relative to Ground" (L3982) — translational (velocity Hessian), not rotational inertia.
- Magnetism / gravity / rotation link: gravity = −α_g∇χ (compression gradient). Bronze target includes "gravity/rotation/lensing datasets" (L4100) — rotation curves, not point spin. Magnetism none stated; no K_L / R / κ_R factor (consistent with canonical "R=0 -> A-115 baseline").
- Open / parked / not-set items: coefficients uncalibrated (L3883); W_i work metric "still-unclosed" (L3980); derive χ(r), inverse-square, wake profile, gate path, E-528/E-529 coefficients, E-530 budget (L4090-4096).
- Conflicts: none. Consistent with canonical g = −α K_L∇χ at R=0 baseline, no-expansion, E-528 redshift, E-530 reinjection.

## A-116 — Three-Dimensional Spherical Default   (Appendix_A.md L4115-4212)
- Gate / lifecycle: GREEN / ACTIVE; "YELLOW (minimum-surface geometry) / GREEN (universal application)" (L4124).
- Upstream: A-102, A-104, A-106, A-107, A-112, A-113, E-504 Surface, E-517 Negative Space (L4131).   Downstream / cites: A-117, D-409, Book 1 Ch1 Particle, Ch2 Proton, C-317 Boundary-Tension Weave, C-321 Reduced Multi-Center Tension Network (L4132).
- Core claim: "A physical One-Wave structure is three-dimensional and volumetric unless a node explicitly states ... 2D" (L4136); "The default stable boundary is spherical or sphere-like." (L4138).
- Equations: E_s = σA (L4145); A³ ≥ 36πV² (L4151); A_min = (36πV²)^{1/3}, E_s,min = σ(36πV²)^{1/3} (L4157-4159); r(θ,φ,t) = R₀ + η (L4169); η = Σ a_ℓm Y_ℓm (L4175); Ω_2D = Ω_3D ∩ P; Π: Ω_3D → Ω_2D (L4189-4195).
- Point / Path / Field role: Point-adjacent only — "Rotation, anisotropic coupling, collisions, or internal knot tension may excite ℓ≥2, but deformation must be derived" (L4182); ℓ=1 = "translation of the center" (L4179). No L, no inertia axes stated.
- Magnetism / gravity / rotation link: rotation as a possible deformation driver (L4182); magnetism/gravity none stated.
- Open / parked / not-set items: universal application stays Green until per-structure dynamics derived (L4212); interior stacking (FCC/HCP) not selected (L4208).
- Conflicts: none.

## A-117 — Dimensional Integrity and Projection Declaration   (Appendix_A.md L4216-4384)
- Gate / lifecycle: YELLOW / ACTIVE; "BRONZE (canonical separation rule) / YELLOW (cross-dimensional operators)" (L4225).
- Upstream: A-101, A-102, A-103, A-113, A-116 (L4232).   Downstream / cites: D-408 Sixfold 2D Lattice, D-409 Twelvefold 3D Coordination, D-410 Twenty-Fourfold 4D Recurrence Shell, all simulations, wiki pages (L4233).
- Core claim: "2D≠3D≠4D" and "6:1≠12:1≠24:1" (L4242-4248); 4D "does not mean a second hidden volume" (L4277); 24:1 = "twenty-four coordinated Field/Void or expression/compression positions around one persistent identity/reference through a completed recurrence shell" (L4285); "A matching number does not prove a matching mechanism." (L4289).
- Equations: P_{D→d}: X_D → X_d (L4338); Q(X_D) = Q_d(P X_D) or ε_Q = |Q(X_D) − Q_d(P X_D)| (L4347-4355); 6:1 → 12:1 → 24:1 schematic (L4308-4310).
- Point / Path / Field role: none stated. 2D sims may test "ring circulation" (L4362) — circulation named only as a testable 2D quantity.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: each ratio transition "requires its own geometry or recurrence operator" (L4312); mandatory dimensional declaration (L4316-4331).
- Conflicts: none.

---

## Slice summary

### (a) Nodes bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking
- A+101 — Field: defines the one field ψ.
- A-101 — Field: Void = ψ=ψ₀, "absence of defined compression" (zero-compression reference for χ).
- A-104 — Field: lattice gradient ∇ψ on sites/neighbors N(i); lattice organization (neighbor mapping) required.
- A-105 — Field: response R_OW = −A(∇ψ); renames "Force" because Ch12 Gravity denies force carriers.
- A-106 — Field: curvature/compression energy (b/2)(∇²ψ)² stabilizes against collapse.
- A-107 — bounded confinement criterion I₃ > I₁/2 (not a Path/orbit).
- A-108 — local stability; names C-310 Resistance Field downstream (no content).
- A-109 — "Inertial" memory term (1−γ) in the update; γ tied to C-309 friction and C-313; no L/I/ω.
- A-110 — phase "rotational position" θᵢ and "natural rotation frequency" ωᵢ: phase rotation, not Point rotation; feeds E-524 Kuramoto lattice sync (locking candidate).
- A-111 — phase-lock criterion |Δφ|<θ, |Δf|<δ (locking in phase/frequency only).
- A-112 — inertia / Mass Effect explicitly not defined here, delegated to C-318; lists "resistance, electrical locking" as unspecified failure modes.
- A-112a — Path-like defect relocation through the lattice; nu from "pressure asymmetry" open.
- A-114 — wave ω(k) from lattice update (not point spin).
- A-115 — gravity g = −α_g∇χ (Field gradient); g_wake (Field wake); v_c²/r orbit (Path); Mass Effect = carried-recurrence resistance m_eff = ⅓Tr ℳ (translational inertia, via C-318); no expansion; E-528/E-529/E-530 loop.
- A-116 — rotation may excite ℓ≥2 boundary deformation; ℓ=1 is center translation.
- A-117 — lattice organization: 6:1 (D-408), 12:1 (D-409), 24:1 (D-410) separated; "ring circulation" testable in 2D.
- No node in this slice states Point rotation with L = Iω, inertia axes, magnetism, dL/dt rules, parent/child transport, K_L/κ_R, or bound-lattice spin locking (Moon 1:1, Mercury 3:2).

### (b) Conflicts found
- None against the canonical rules.
- Internal/editorial (not canonical-rule conflicts):
  1. A-108 still uses "F_restore" / "Restoring force/response" (Appendix_A.md L2250, L2261, L2270) after A-105 (L1503-1511) declares all "Force" symbols renamed to R_OW.
  2. A-108 closure truncated "confine.iel" and missing STATUS (L2466).
  3. A-111 "Yellow Audit" heading empty (L3154).
  4. A-113 stray authoring text (L3546-3548).
  5. Label collision: A-101 (L789-835), A-109 (L609-653), A-110 (L816-853) reuse C-301..C-305 and F-601..F-605 as local constraint/failure tags, colliding with canonical C-series IDs (e.g., C-301 Mirror Gate, C-305).
  6. Symbol collision (watch item): γ = memory damping/friction in A-109/A-110/A-114 vs canonical closed-gradient dL/dt = −γL; and ωᵢ "natural rotation frequency" in A-110 (phase) vs G-749 Point ω.

### (c) Cross-references outside this slice that matter for point rotation or magnetism
- C-318 four-interaction architecture (Z_K, Z_E, Z_M, Z_T; mass/inertia owner) — A-112 L3208, A-115 L3932-3982.
- C-310 Resistance Field — A-108 L2211, L2401; A-105 L1505.
- C-309 Friction Limit (γ friction) and C-313 Lorentz Invariance Conflict — A-109 L2489; A-115 L3824.
- C-317 Boundary-Tension Weave, C-321 Reduced Multi-Center Tension Network — A-116 L4132.
- C-322 Mirror-Gate 125 GeV, C-301 Mirror Gate — A-115 L3825.
- E-524 Kuramoto Lattice Synchronization (locking candidate) — A-110 L2726.
- E-523 Circle Pit Vortex Transition — A-111 L2916.
- E-528, E-529, E-530 — A-115 L3825, L4013.
- D-408, D-409, D-410 lattice coordination — A-117 L4233.
- Book 1 Ch12 Gravity, Ch14 Mass Effect, Ch15 Higgs; Book 5 Ch1, Ch4 — A-115 L3825; A-105 L1505.
- B-201, B-221, C-305 (former F_OW users) — A-105 L1504-1505.
