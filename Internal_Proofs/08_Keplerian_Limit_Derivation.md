# Internal Proof Draft 08: The Keplerian Limit — From A-105/A-106 to Newton's Law and Kepler's Three Laws

**Document status:** DRAFT / INTERNAL
**Authority:** Internal derivation draft only. Current canonical node files override this document wherever they differ. Per `Internal_Proofs/00_PROOF_INDEX.md`, this document does not itself change any node's gate. It supplies the closure math that individual node files then cite, with each node file updated separately and conservatively (I-02: a node advances only within its own gate unless simulation/validation conditions are independently met).

**Purpose.** This closes a specific, repeatedly-flagged gap: nothing in the repository previously derived an inverse-square exterior force law, or Kepler's three laws, from the A-series field primitives. `Book1_Ch12`'s own Yellow Audit lists "Newton's law derivation (inverse square)... remains sketch level" and "Gravitational field Phi_M(r) derivation from update rule not yet complete." `A-115` §7 lists "recover or replace the inverse-square limit" as an unmet Yellow-completion requirement. `C-306`/`C-307` mark their orbital-mechanics math as foundation-level only. `D-413` uses an **imposed**, not derived, curvature well and says so explicitly. `UPDATED_38` through `UPDATED_41` all build multi-body/EM/rotation architecture on top of an abstract force placeholder `F(...)` that every one of those four documents says "must ultimately be derived... rather than fitted" — and none of them derive it. This draft is that missing derivation, done once, honestly, with every assumption stated.

It also finds and flags one real internal inconsistency (§6) rather than papering over it.

**Correction notice (external review, applied in full):** an independent review of this draft found two real mathematical errors, both confirmed and fixed here: (1) §4.1 mixed two different field equations when source-matching, producing the wrong formula for `G_eff` — corrected from `1/(4πα)` to the verified `α/(4πa)`; (2) §4.2 overstated Gauss's-law-derived flux conservation as the full Newtonian shell theorem for any bounded shape, when it is only exact under spherical symmetry — corrected to the honest monopole-equivalence statement. Both corrections are worked in place below with the reasoning shown, not just the fixed conclusion. The Kepler-law derivation in §5 is unaffected by either correction. Where this document is cited elsewhere in the repo as "already-verified," that phrasing should be read as **candidate derived field** until independently checked again — a description this draft failed to live up to once already.

---

## 0. What is assumed vs. what is derived

Stated up front, per repo convention (I-01):

**Already established elsewhere (used, not re-derived here):**
- A-105's linear response law `R_OW = -α∇ψ`.
- A-106's combined energy functional `E[ψ] = ∫[(a/2)(∇ψ)² + V(Δψ) + (b/2)(∇²ψ)²] d³x`, and its requirement `b>0`.
- A-107's rescaling-stability criterion `I₃ > I₁/2`.
- C-306's `τ = r × F` and C-307's `L = I·ω`.

**Newly derived in this draft:**
- The static, source-free, long-range field equation implied by A-105+A-106's own functional (§1).
- Its exact spherically-symmetric solution — a Yukawa correction riding on a `1/r` term, not an assumed `1/r` (§2).
- The far-field reduction to an exact inverse-square response, with `G_eff = α/(4πa)` expressed in terms of *both* A-105's response coefficient `α` and A-106's own source-generation coefficient `a` (§3-4.1, corrected during external review — an earlier version of this draft mixed two different field equations and got this formula wrong; see the correction note in §4.1) — this is what Book1_Ch12 asked for and marked deferred.
- A derived short-range screening length `λ = √(b/a)`, a new falsifiable prediction (§3).
- The *monopole* far-field equivalence for a single extended source, from first principles (§4.2, corrected — an earlier version overstated this as the full shell theorem for any bounded shape; it is exact only under spherical symmetry, see the correction there). Real justification, but weaker than first claimed, for treating one bounded body (e.g. the Sun) as approximately point-like at its own center of mass, which Updated 38-41 do throughout without deriving it.
- Kepler's first, second, and third laws as the two-body limit of the resulting central force (§5).

**Explicitly NOT derived here, and not claimed to be:**
- The operator `A` in `R_OW=-A(∇ψ)` in its general (nonlinear) form — this derivation only uses A-105's already-declared linear special case.
- `b`'s value or its relation to `α` (A-106 already lists this open; this draft does not close it, it just gives the ratio `b/a` new physical meaning as `λ²`).
- The equivalence-principle bridge between a body's own source strength and its own response coupling. This is Book1_Ch12's own Prediction #3 ("Equality of gravitational and inertial response is a derivation target, not an assumption") and it stays open. §5 states exactly where this assumption enters and flags it inline rather than silently using it.
- **The finite-wake/multi-body architecture in Updated 38-41.** §4.3 shows that naive linear superposition of several derived fields is the plain "summing independent gravitational wells to infinity" picture Updated 38 explicitly built its finite-wake hypothesis to avoid — not a derivation of that hypothesis, and not evidence for it. That architecture (the assimilation boundary, the overlap weight `W_ij`, the emergent active range `R_active,i(t)`) is untouched by this draft and remains exactly as open as before, with a real, unresolved tension now stated explicitly: whether a finite-range cutoff can coexist at all with the long-range inverse-square limit derived here.
- Anything about the EM-shell terms or rotational coupling in Updated 38-41. Those remain exactly as open as before. This draft only closes the base-case (non-rotating, non-magnetized, single dominant source, two-body) limit that those documents' own `F(...)` placeholder must reduce to.

---

## 1. The static field equation A-105+A-106 already imply

A-105 defines a constitutive relation, not yet a field equation:

```
R_OW = -α∇ψ
```

This has the same structure as any flux-from-gradient law (Fourier's law of heat conduction, Fick's law of diffusion, Darcy's law) — a vector response proportional to a scalar field's gradient. Reading `R_OW` this way, as a **flux density**, gives a field equation for `ψ` itself via conservation: for a source density `Q(x)` (the rate at which a bounded Persistent Mode, A-112, sources the field),

```
∂ψ/∂t + ∇·R_OW = Q(x)
```

In the static case (`∂ψ/∂t = 0`) with `R_OW = -α∇ψ`:

```
-α∇²ψ = -Q(x)     i.e.     ∇²ψ = Q(x)/α        (Eq. 1, source region)
∇²ψ = 0                                          (Eq. 1', exterior, Q=0)
```

This alone is already Poisson's equation, but it uses only A-105 and throws away A-106's curvature term. A-106 established that the curvature term is not optional — it is what makes bounded states possible at all (A-107, Derrick's theorem). The correct static equation must come from extremizing the **full** A-106 functional, not the truncated one.

Take the functional derivative of `E[ψ] = ∫[(a/2)(∇ψ)² + V(Δψ) + (b/2)(∇²ψ)²] d³x` (standard Euler-Lagrange, two integrations by parts for the biharmonic term):

```
δE/δψ = -a∇²ψ + V'(ψ) + b∇⁴ψ
```

Setting `Δψ ≡ ψ` (A-101 fixes Ground/Zero as the reference, so displacement-from-ground is just `ψ` itself) and requiring the static equilibrium condition `δE/δψ = Q(x)` (source-driven equilibrium; `Q=0` outside the source) gives the **combined static field equation**:

```
-a∇²ψ + b∇⁴ψ + V'(ψ) = Q(x)                     (Eq. 2)
```

**Two assumptions made explicit here, both new (not previously stated in A-105/A-106):**

1. `V'(0) = 0` — Ground/Zero is an extremum of the potential. This is the minimal reading of A-101 (Ground/Zero as *the* reference state) and is not an extra physical assumption beyond what A-101 already asserts.
2. `V''(0) = 0` — no mass term in the linearization around Ground. This one **is** a new, load-bearing, falsifiable assumption, stated here for the first time: **if `V''(0) ≠ 0`, the exterior field is exponentially screened (Yukawa) at all length scales, not just short range, and gravity would not be long-range.** Since Gray (Standard Model comparison) requires the recovered force to be long-range (`R_OW ~ 1/r²` out to Solar-System and larger scales, matching the observed inverse-square law), consistency with the Gray reference **forces** `V''(0)=0` at the level of approximation used here. This is a structural constraint on `V`, not a free choice — it is the price of admission for a long-range gravity limit to exist in this framework at all, and it should be added to A-106/A-107's own open-items list (done in §6).

With both, the linearized exterior static equation is:

```
-a∇²ψ + b∇⁴ψ = 0                                (Eq. 3, exterior, linearized)
```

This is now a concrete, solvable equation using only A-105's and A-106's own already-declared coefficients `a` (A-106's gradient-energy coefficient) and `b` (A-106's curvature coefficient, required `>0` by A-106/A-107).

---

## 2. Exact spherically-symmetric exterior solution

Let `g ≡ ∇²ψ`. Eq. 3 becomes `b∇²g = ag`, i.e.

```
∇²g = κ²g,     κ² ≡ a/b        (κ real, since a,b>0 — a>0 is required for the gradient term to be an energy cost, b>0 is A-106's own stability requirement)
```

For spherically symmetric `g(r)`, write `g=w(r)/r`; then `∇²g = w''(r)/r`, giving `w''=κ²w`, solution `w=Ce^{-κr}` (rejecting the exponentially growing branch — unbounded at infinity, unphysical). So:

```
g(r) = ∇²ψ = C e^{-κr}/r
```

Solve `∇²ψ = g(r)` the same way: let `ψ=v(r)/r`, so `v''(r)=C e^{-κr}`. Integrating twice:

```
v(r) = (C/κ²) e^{-κr} + c₁ r + c₂
ψ(r) = (C/κ²)(e^{-κr}/r) + c₁ + c₂/r          (Eq. 4, general exterior solution, r > R_source)
```

**Boundary condition** (A-101, Ground/Zero at infinity): `ψ→0` as `r→∞` forces `c₁=0` (the only term in Eq. 4 that does not already vanish at infinity). This leaves:

```
ψ(r) = (C/κ²)·e^{-κr}/r + c₂/r,        κ = √(a/b)          (Eq. 5)
```

**This is the exact result**, not a sketch: the exterior field of a bounded Persistent Mode, under A-105+A-106's own field equation, is a **Yukawa-screened correction riding on top of an exact `1/r` term** — not simply an assumed `1/r`. Define the **screening length**

```
λ ≡ 1/κ = √(b/a)
```

so Eq. 5 reads `ψ(r) = (Cλ²/1)·e^{-r/λ}/r + c₂/r`.

---

## 3. The Keplerian (long-range) limit and a new falsifiable prediction

For `r ≫ λ`, the Yukawa term is exponentially suppressed and

```
ψ(r) → c₂/r                                                (Eq. 6, far field)
```

**This is the inverse-square limit that Book1_Ch12 marked "sketch — derivation deferred."** It is now a derived consequence, not an assumption, and it is a genuine limit (`r≫λ`), not an unconditional global statement — which is itself new, testable content:

```
∇ψ(r) = -c₂/r² r̂
R_OW(r) = -α∇ψ = α c₂/r² r̂
```

Writing `c₂ = -k` (k>0 for an attractive/restoring response, matching A-105's sign convention: the response points toward the source) gives

```
R_OW(r) = -(αk)/r² r̂,        r ≫ λ                          (Eq. 7)
```

which is exactly Newton's law `F = -GMm/r² r̂` under the identification `αk ↔ G·M_eff` — closing Book1_Ch12's own stated target ("Derive G from alpha and lattice parameters"). The source-matching integral (§4.1 below) fixes `k` in terms of the total source strength; the correct closed form, worked out there (**not** the version originally stated here, corrected during external review — see §4.1), is

```
G_eff = α/(4πa)                                             (Eq. 8, corrected)
```

**New prediction, not previously in the repo:** for `r ≲ λ = √(b/a)`, Eq. 5's Yukawa term is *not* negligible and the exterior response deviates from pure inverse-square. This is the same structural form as the deviations already searched for experimentally in short-range (sub-millimeter) tests of the inverse-square law, and it gives A-106's previously free coefficient `b` (relative to `a`) a concrete physical meaning it did not have before: `b/a = λ²`, a length scale in principle bounded by existing torsion-balance data. This should be added as a new Prediction/Yellow-Audit item downstream (done in §6) — it is not claimed here to be validated, only derived and made falsifiable.

**Consistency cross-check:** A-106/A-107 already require `b>0` for bounded-motion stability (Derrick's theorem fix). This derivation independently requires `a,b>0` for `κ` to be real (a decaying, non-oscillatory correction rather than an oscillatory/unstable one). The same sign condition is required by both an unrelated stability argument (A-107) and this exterior-field argument — a nontrivial consistency check, not a coincidence that was arranged in advance.

---

## 4. Source matching, the shell theorem, and superposition

### 4.1 Fixing `k` from the source — corrected during external review

**An earlier version of this section made a real error, caught by outside review and confirmed independently before this correction was written: it applied the divergence theorem to Eq. 1 (`∇²ψ=Q/α`) to fix `k`, while the field `ψ` actually being solved throughout §§2-3 is the solution of the *different* equation, Eq. 3 (`-a∇²ψ+b∇⁴ψ=0`, from A-106's full functional). Eq. 1 is a simpler, separate equation obtained from A-105 alone, before A-106's curvature term is added — using it for source-matching after having already solved Eq. 3 silently switched equations mid-derivation and introduced `α` where `a` belongs. Corrected here using Eq. 3 throughout, consistently.**

Define `φ ≡ b∇²ψ - aψ`. For constant `a,b`, `∇²φ = b∇⁴ψ - a∇²ψ`, which is exactly the left side of Eq. 3 with a source: `∇²φ = Q(x)`. So `φ` obeys an ordinary Poisson equation sourced by the *same* `Q` — this is the correct, single, consistent equation to source-match against, built entirely from Eq. 3.

Substitute the already-derived exterior solution (Eq. 5, `ψ=(C/κ²)e^{-κr}/r+c₂/r`, `κ²=a/b`) directly:

```
∇²ψ = C e^{-κr}/r        (= g(r), from §2)
φ = b·g(r) - a·ψ(r) = C e^{-κr}/r·[b - a/κ²] - a·c₂/r
```

Since `a/κ² = a/(a/b) = b`, the bracket `[b-a/κ²]` is **exactly zero** — the Yukawa piece cancels identically, for all `r`, not just far field (verified numerically to 6+ decimal places across a range of `r`). This leaves the exact result

```
φ(r) = -a·c₂/r                                              (exact, all r > R_source)
```

Now source-match `φ` against the ordinary Poisson solution: for `∇²φ=Q(x)` with `Q` compactly supported, `φ(r) → -Q_tot/(4πr)` in the far field (the standard Green's-function/monopole result — subject to the same multipole caveat detailed in §4.2 below). Matching:

```
-a·c₂ = -Q_tot/(4π)     ⟹     c₂ = Q_tot/(4πa)
```

Writing `c₂=-k` as before (§3) gives `k = Q_tot/(4πa)` — **using `a`, not `α`**. `α` re-enters only at the *separate*, already-stated step of converting the sourced field into a physical response via A-105's own constitutive law, `R_OW=-α∇ψ` (§3, Eq. 7). Combining both steps correctly:

```
R_OW(r) = -α∇ψ = -(α k)/r² r̂ = -\frac{α Q_{tot}}{4πa·r^2}\hat r
```

Identifying `Q_tot ≡ M_eff` (the same `M_eff` A-115 §2 uses) gives the corrected closed form:

```
G_eff = α/(4πa)                                             (Eq. 8, corrected)
ψ(r) = -G_eff M_eff · (a/α) / r  =  -\frac{M_eff}{4\pi a}\frac{1}{r},
R_OW(r) = -G_eff M_eff/r^2 \hat r,     r≫λ, r>R_source
```

`a` (how strongly a source generates the field `ψ`) and `α` (how strongly the field's gradient converts into physical response) are genuinely distinct roles, both now visible in `G_eff` rather than one silently substituted for the other. Whether `a` and `α` are themselves related or independent physical constants is not established anywhere in A-105/A-106 and is not assumed here — a new, explicit open item (§7).

### 4.2 Monopole far-field equivalence — corrected from an overstated "shell theorem"

**An earlier version of this section claimed the full Newtonian shell theorem — exact field equivalence to a point source, for *any* bounded shape. That is too strong, and was caught by outside review.** Gauss's law (the divergence-theorem argument used throughout this document) fixes only the *total flux* of `∇ψ` through any enclosing sphere — it does not fix the field's value at each point on that sphere, and does not by itself force the field to look like a point source's field in every direction. The exact Newtonian shell theorem additionally requires **spherical symmetry** of the source; that is a stronger, separate geometric fact, not a consequence of Gauss's law alone.

What Gauss's law alone actually establishes, correctly: the **monopole** term of the exterior field's multipole expansion exactly matches a point source of total `Q_tot`, for *any* bounded source shape. Expanding the exact solution `φ(x)=-\frac{1}{4\pi}\int Q(x')/|x-x'|\,d^3x'` for `|x|` large compared to the source's extent gives

```
φ(x) = -\frac{1}{4\pi}\left[\frac{Q_{tot}}{r} + \frac{\mathbf p\cdot\hat r}{r^2} + O(1/r^3)\right],
\qquad \mathbf p=\int Q(x')\,\mathbf x'\,d^3x'
```

If the origin is placed at the source's own centroid (center of mass/charge), the dipole term `\mathbf p` vanishes identically **by definition of centroid** — a real, exact simplification, not approximate. But the **quadrupole** term (`O(1/r^3)`, depending on the source's actual shape — e.g. how oblate or elongated it is) generically does **not** vanish unless the source is spherically symmetric specifically. This is the same structure real celestial mechanics already uses and needs (Earth's own `J2` oblateness term in real satellite orbit calculations is exactly this quadrupole correction) — not a defect newly introduced here, but a real limit on how strong a claim this derivation supports.

**Corrected statement:** for a bounded, compactly-supported source, the exterior field's monopole component exactly matches a point source of total `Q_tot` at the source's centroid. The full field exactly equals a point source's field, at every exterior point, only under spherical symmetry; for a general shape it is the leading far-field term, with quadrupole-and-higher corrections that fall off faster (`1/r³` and beyond) but do not vanish in general. This is real, useful, honest support — matching how the Sun (very nearly spherical) and, to good approximation, the other major bodies are already treated in real orbital mechanics — for treating `UPDATED_38` through `UPDATED_41`'s bodies as approximately point-like at their centers, not the unconditional exact statement an earlier version of this draft claimed.

### 4.3 Superposition — and a real tension with the finite-wake hypothesis, not a justification of it

Eq. 3 (and Eq. 1) are **linear** in `ψ` in the regime this derivation uses (source-free, `V''(0)=0` linearization). For `N` bounded sources with disjoint supports, `ψ_total = Σᵢψᵢ` solves the same linear equation with `Q = ΣᵢQᵢ`, by direct substitution. Hence

```
R_OW,total(x) = Σᵢ R_OW,i(x) = Σᵢ (-α∇ψᵢ)
```

**This must not be read as validating `UPDATED_38`'s or `UPDATED_40`'s additive architecture, and an earlier version of this section wrongly said it did — flagged and corrected here.** `UPDATED_38`'s own Purpose section states its finite-wake hypothesis explicitly *against* this move: "enforcing the One-Wave finite-wake hypothesis rather than **summing independent gravitational wells to infinity**." That is exactly what §3's far-field solution is: `ψ(r) → c₂/r` has no cutoff, no assimilation boundary, and no distance-dependent weight — it is a plain `1/r` field that individually extends to infinity, for every source, unconditionally. Summing several of them (this section) is the "summing independent gravitational wells to infinity" picture Updated 38 defines itself against, not an alternative to it.

Concretely: nothing derived in §1-§3 produces, or leaves room for, a term like `UPDATED_40`'s overlap weight `W_ij(t)` going to zero at range, or an assimilation boundary `R_i(t)` at all. The only finite length scale this derivation produces (`λ=√(b/a)`, §2-§3) governs a *short*-range correction near the source, not a large-distance cutoff — it is the wrong end of the field for what "finite-wake" is asking for. A real finite-range cutoff, if the framework wants one, has to come from physics this linear derivation does not capture (a nonzero `V''(0)`, e.g., which reintroduces its own problem: a mass term screens the field at **all** ranges, including the ones where the far-field `1/r²` law is required to match observed Solar-System gravity, per §1's own `V''(0)=0` consistency argument). Whether those two requirements — long-range inverse-square out to Solar-System scale, and a finite-wake assimilation boundary at some other scale — can be reconciled at all is a real open question this draft surfaces but does not answer.

What this section actually establishes, stated narrowly: in the strictly linear, disjoint-support, far-field regime, the total field is the naive sum of individual unbounded `1/r` fields. That is a legitimate closed-form result for the ordinary two-body/few-body Newtonian limit used in §5's Kepler derivation (which needs only a single dominant source, not a sum). It is not a derivation of, and should not be cited as support for, Updated 38-41's finite-wake/assimilation-boundary/overlap-weight architecture — if anything it is evidence that architecture requires physics beyond what A-105+A-106's linearized functional supplies.

---

## 5. Kepler's three laws as the two-body limit

Take Eq. 7 as the force law, with the explicit, flagged assumption already stated in §0: that a body's own response coupling scales with its own source strength the same way the source body's does (`k → G_eff·M_eff·m`, `m` the orbiting body's own effective source-strength — this is the equivalence-principle bridge Book1_Ch12 leaves as an open prediction, not re-derived here). Under that stated assumption, the two-body problem reduces to the standard one-body central-force problem with reduced mass `μ`:

```
F(r) = -k'/r² \hat r,     k' = G_eff M_eff μ
```

### 5.1 Kepler's Second Law (equal areas) — from C-306/C-307 directly

C-306 defines `τ = r×F`. For any central force, `F ∥ \hat r`, so `τ = r×F = 0` identically. C-307's own relation `dL/dt=τ` (implicit in `L=I·ω` plus Newton's second law) then gives

```
L = r×p = const                                              (Eq. 9)
```

**This closes C-307's own flagged gap** ("Endpoint derivation from One-Wave field geometry not complete") for exactly this application: the orbital central-force case. It does not close the general, non-central-force case C-307 leaves open — that stays open, narrowly.

Since `L` is a fixed vector and `\mathbf r·L = r·(r×p) = 0` always, the motion is confined to the fixed plane perpendicular to `L` — this is the derivation of "the orbit is planar," also previously unstated. In that plane, using polar coordinates `(r,θ)`,

```
L = m r² (dθ/dt) = const
```

The area swept in time `dt` is `dA = (1/2)r²dθ`, so

```
dA/dt = (1/2)r² dθ/dt = L/(2m) = const                       (Kepler's Second Law)
```

### 5.2 Kepler's First Law (ellipse) — Binet equation

With `u≡1/r`, the standard substitution (from `d²r/dt²` rewritten using `L=mr²\dot θ` to eliminate time) gives the Binet equation

```
d²u/dθ² + u = -\frac{m}{L^2 u^2} F(1/u)
```

For `F(r)=-k'/r²`, i.e. `F(1/u) = -k'u²`:

```
d²u/dθ² + u = mk'/L²
```

a linear ODE with constant forcing. General solution:

```
u(θ) = mk'/L² + Ccos(θ-θ₀)          i.e.          1/r = \frac{mk'}{L^2}\left[1+e\cos(\theta-\theta_0)\right]
```

with `e ≡ CL²/(mk')`. This is the polar equation of a conic section with semi-latus rectum `p=L²/(mk')`. For `0≤e<1` (bound total energy `E<0`) this is an **ellipse**, one focus at the source — **Kepler's First Law**, derived, not assumed, for the first time in this repository's math trail.

### 5.3 Kepler's Third Law (T² ∝ a³)

Integrating the constant areal velocity over one full period `T`: total ellipse area `πab = (L/2m)·T`. Using the standard ellipse identities `b=a\sqrt{1-e^2}` and `p=a(1-e^2)=L^2/(mk')` (so `L=\sqrt{mk'a(1-e^2)}`):

```
T = \frac{2\pi m a b}{L} = \frac{2\pi m a^2\sqrt{1-e^2}}{\sqrt{mk'a(1-e^2)}} = 2\pi\sqrt{\frac{ma^3}{k'}}
```

so

```
T^2 = \frac{4\pi^2 m}{k'}a^3 = \frac{4\pi^2}{G_{eff}M_{eff}}a^3          (Kepler's Third Law)
```

`m` (the orbiting body's own mass/source strength) cancels — this is the same equivalence-principle assumption from §0/§5 surfacing again, now visibly, as the reason the period-radius relation is body-independent. That the assumption is *needed* to get the observed body-independence of Kepler's Third Law, and is not automatically forced by anything derived above it, is exactly the open item Book1_Ch12 already flagged; this draft makes the dependency explicit rather than hiding it inside a cancellation.

---

## 6. One found inconsistency, flagged and resolved

**A-115 §2 defines `Φ_OW = α_g·χ` where `χ=-∇·u`.** If the vector displacement field `u` used in A-115 is the gradient flow of the scalar `ψ` used in A-105/Book1_Ch12 (the natural identification, `u=∇ψ` up to a constant — both represent "displacement of the field away from Ground/Zero"), then `χ = -∇·(∇ψ) = -∇²ψ`. But this derivation shows `∇²ψ=0` throughout the exterior region (Eq. 3's leading order, Eq. 6's regime) — meaning **A-115's own `Φ_OW`, as currently defined, is identically zero everywhere outside the source**, in exactly the region where gravity is observed and where this derivation produces a nonzero, correctly-behaved `1/r` potential and `1/r²` force.

This is a real definitional conflict between A-115 §2 and the ψ-based treatment used in A-105/Book1_Ch12/D-413, not a style difference — one says the exterior potential is a nonzero `1/r` field (Book1_Ch12, this draft), the other defines the exterior potential as something that vanishes in exactly that region (A-115 as currently written). Both cannot be the operative definition of "the gravitational potential."

**Resolution proposed here (recorded, not silently applied):** `Φ_OW` should be identified with `ψ` itself (or a fixed multiple of it), not with `α_g` times its Laplacian. `χ=-∇·u` remains meaningful as the **source density** (playing the role `ρ` plays in `∇²Φ=4πGρ`), satisfying `∇²ψ ∝ χ` inside the source and `∇²ψ≈0` outside it — consistent with Eq. 1/Eq. 3 above and with the ordinary electrostatics/Newtonian-gravity analogy A-115 §2 already invokes. This is flagged as an open correction for A-115's own maintainers to apply; it is applied as a documentation note in A-115 §2 below, without silently rewriting A-115's formal claim status.

---

## 7. Summary of what is now closed vs. what remains open

**Closed by this draft (math-only closure; no gate promoted past what I-02 allows without simulation) — corrected during external review, see §4.1/§4.2 for what changed:**
- Book1_Ch12 Yellow Audit: "Gravitational field Phi_M(r) derivation... not yet complete" — closed, far-field limit (§2-3).
- Book1_Ch12 Yellow Audit: "Newton's law derivation (inverse square)... sketch level" — closed (§3, Eq. 7).
- Book1_Ch12 Future Work: "Derive G from alpha and lattice parameters" — closed, with the corrected form `G_eff=α/(4πa)` (Eq. 8, §4.1) — the originally-stated `1/(4πα)` was wrong, caught by external review, and is not the number to cite.
- A-115 §7: "derive χ(r) from sources, recover or replace the inverse-square limit" — closed, with the χ/ψ conflation flagged and a resolution proposed (§6).
- C-307 Yellow Audit: "Endpoint derivation from field geometry not complete" — closed for the central-force/orbital case specifically (§5.1); general case stays open.
- The monopole far-field equivalence (§4.2, corrected — weaker than the "full shell theorem" an earlier version claimed) — exact for the monopole term and for the vanishing dipole about the centroid; exact for the *complete* field only under spherical symmetry. Real, honest support — not an unconditional proof — for treating the Sun/Jupiter/Earth/etc. as approximately point-like at their centers, the way `UPDATED_38`-`UPDATED_41` already do.
- Kepler's First, Second, and Third Laws — derived as the two-body limit of Eq. 7, closing the actual "explain planetary motion" gap that four architecture documents (Updated 38-41) had built on top of without ever reaching. (Unaffected by the §4.1/§4.2 corrections — the Kepler derivation in §5 uses `G_eff M_eff` symbolically and a single dominant, treated-as-spherical source; it does not depend on the specific numeric formula for `G_eff` or on the general-shape multipole question.)

**Still open (unchanged by this draft, stated so nothing is silently claimed):**
- `A`'s general nonlinear form (A-105).
- `b`'s derivation from a deeper node, though it now has physical meaning as `λ²·a` (A-106).
- **New, from the §4.1 correction: whether `a` (A-106's field-generation coefficient) and `α` (A-105's field-to-response coefficient) are the same constant, related, or genuinely independent is not established anywhere in the source nodes.** `G_eff=α/(4πa)` keeps them as two separate symbols rather than assuming either equality or independence — this is a real, new open question, not a notational nicety.
- **New, from the §4.2 correction: quadrupole-and-higher corrections for non-spherically-symmetric sources.** Real for any body that isn't a sphere (planetary oblateness, tidal bulges); not derived or estimated here.
- The equivalence-principle bridge between source strength and response coupling (used explicitly, not derived, in §5).
- `V''(0)=0` itself is a new assumption, not a derived fact — it is *required* for long-range gravity to exist in this framework, but nothing here derives it from a deeper principle.
- **§4.3's linear superposition of multiple sources' fields is NOT a justification for `UPDATED_38`/`UPDATED_40`'s finite-wake, assimilation-boundary, or overlap-weight architecture — it is the naive "summing independent gravitational wells to infinity" picture Updated 38 explicitly says its finite-wake hypothesis replaces. An earlier version of this draft (and of the cross-reference notes it added to Updated 38/40/42) wrongly presented superposition as supporting that architecture; corrected in §4.3 and in those documents. Whether a genuine finite-range cutoff can coexist with the long-range `1/r²` limit this draft derives is an open, and possibly hard, question — not one this draft answers.**
- Everything specific to Updated 38-41's actual research program: the finite-wake assimilation boundary, EM-shell coupling laws, rotational Point-Path-Field coupling terms, and Mercury's special channel. This draft closes only the single-dominant-source, no-rotation, no-EM two-body limit those documents' placeholder `F(...)` must reduce to — none of the higher-order or multi-body physics in those four documents is touched, and §4.3 above should not be read as touching it either.
- No simulation has been run against this closed-form result. Per I-02, that is required before any node here moves from Yellow to Bronze. This draft is math-only.
