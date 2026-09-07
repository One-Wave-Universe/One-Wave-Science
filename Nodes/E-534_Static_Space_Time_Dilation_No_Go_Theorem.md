---
node_id: "E-534"
canonical_name: "Static-Space Time-Dilation No-Go Theorem"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cosmology / Redshift / Structural Constraint"
claim_gate_detail: "GREEN (the flat-lapse cancellation derivation, Section 2) / YELLOW (the varying-c loophole bound, Section 3, uses literature bounds not independently re-derived) / RED (the sub-claim this forecloses: any homogeneous static-space, locally-Lorentz-invariant redshift mechanism reproducing universal (1+z) time dilation)"
metadata_standard: "I-06"
---

# Node E-534: Static-Space Time-Dilation No-Go Theorem

**Dependencies**
Upstream: E-533 Redshift Law Versus Expansion, E-528 Static Redshift Transport, A-115 Unified Compression Field, C-309 Friction Limit, E-509 Propagation Limit
Downstream: any future revision of E-528/A-115 that attempts to satisfy E-533 Section 8; ONE_WAVE_SCIENCE_ATTACK_MAP.md Section L

## Purpose

E-533 Section 8 set a bar: find a mechanism, consistent with One-Wave's own
primitives, that reproduces the observed universal \((1+z)\) time dilation of
distant transients (Type Ia supernova light curves) **without** the spatial
part of the background becoming time-dependent — i.e., without literal
metric expansion.

This node is a serious, good-faith attempt to clear that bar. It does not
succeed. What it produces instead is a derivation of *why* it cannot succeed
for the entire class of homogeneous, isotropic, locally-Lorentz-invariant
static-space models — a structural (no-go) result, not a failed guess. Two
narrow escape routes are identified and each is closed: one by a clean
mathematical triviality, one by an extremely tight independent observational
bound. A third route is named but not developed, because nothing here
motivates it. This keeps Section 8 answerable rather than abandoned: Section
4 states exactly what the theorem does *not* rule out.

## 1. Setup: the most general static-space ansatz

The most general homogeneous, isotropic spacetime with a spatial part that
does **not** depend on time — the literal definition of "static space," and
the weakest possible assumption that still lets a global clock-rate/
propagation-rate effect vary with cosmic time — is

\[
ds^2=-\alpha(t)^2\,dt^2+d\mathbf x^2,
\]

using units with \(c=1\). Here \(\alpha(t)\) is an arbitrary positive
function: a global "lapse." The spatial metric coefficient is exactly \(1\)
for all \(t\) — proper spatial distance between any two fixed comoving points
never changes. This is the most permissive form of "static space, but maybe
clocks or light run at a different rate at different cosmic epochs" that can
be written down. If a mechanism reproducing real time dilation exists within
One-Wave's static-space commitment, it must reduce to something of this form
(or a strictly weaker, less general one) at the level that actually reaches
observers.

**Local clock.** A comoving observer (\(d\mathbf x=0\)) has
\(d\tau=\alpha(t)\,dt\): proper time runs at the global rate \(\alpha(t)\).

**Light propagation, assuming ordinary local Lorentz invariance** (light
moves at the same local proper speed \(c=1\) that clocks are built from — see
Section 3 for what happens if this assumption is dropped): a null ray has
\(ds^2=0\), giving \(dx/dt=\alpha(t)\).

## 2. The cancellation (main result)

Let the source sit at \(x=0\) and the observer at fixed comoving distance
\(x=D\) (unchanging, because the spatial metric is static). A light ray
emitted at global time \(t_e\) arrives at \(t_o\) where

\[
\int_{t_e}^{t_o}\alpha(t)\,dt=D.
\]

Differentiating this relation with respect to \(t_e\) (holding \(D\) fixed)
gives the arrival-time map's slope in *global coordinate time*:

\[
\alpha(t_o)\,\frac{dt_o}{dt_e}=\alpha(t_e)
\quad\Longrightarrow\quad
\frac{dt_o}{dt_e}=\frac{\alpha(t_e)}{\alpha(t_o)}.
\]

Taken alone, this looks like exactly the dilation factor needed — and it is
the calculation that makes "a slowly changing propagation/clock rate" look
promising at first pass. But \(t\) is a coordinate, not what any clock reads.
What an observer actually measures is the separation between two **proper**
time intervals, \(d\tau_o=\alpha(t_o)\,dt_o\) compared to \(d\tau_e=\alpha(t_e)\,dt_e\):

\[
\frac{d\tau_o}{d\tau_e}
=\frac{\alpha(t_o)\,dt_o}{\alpha(t_e)\,dt_e}
=\frac{\alpha(t_o)}{\alpha(t_e)}\cdot\frac{dt_o}{dt_e}
=\frac{\alpha(t_o)}{\alpha(t_e)}\cdot\frac{\alpha(t_e)}{\alpha(t_o)}
=1.
\]

**The \(\alpha\) factors cancel exactly, for any \(\alpha(t)\).** The observer's
own clock is *also* running at the same time-varying rate at the moment of
reception, and that exactly undoes the apparent stretching in the light's
coordinate transit time. No real, physically measured time dilation survives.

This is not a coincidence particular to this metric — it is the standard fact
that a metric of the form \(-\alpha(t)^2dt^2+d\mathbf x^2\) is related to flat
Minkowski spacetime, \(-d\tau^2+d\mathbf x^2\), by the coordinate change
\(\tau=\int\alpha(t)\,dt\). A pure time-dependent lapse with a genuinely
static (\(t\)-independent) spatial part is a **coordinate artifact**, not new
physics; relabeling the time axis cannot produce an observable effect. The
naive Section-1-style calculation of a redshift-like factor from \(\alpha(t)\)
alone (as in E-528's \(\kappa_\gamma\) picture, or any "the propagation speed
was different in the past" story) is exactly this artifact if nothing else in
the metric changes — which is also why it does not, by itself, predict
genuine time dilation, consistent with the plain assessment in E-533 Section
6, now derived rather than asserted.

**Corollary.** The *only* way to get a spacetime where redshift-linked time
dilation is real (not removable by \(\tau=\int\alpha\,dt\)) is for the
*spatial* metric coefficient to itself depend on \(t\) — i.e. \(ds^2=-dt^2+a(t)^2
d\mathbf x^2\). That is not a variant of a static-space model. That is the
FRW scale factor by another name. Any mechanism landing here has, by
construction, reintroduced literal expansion, whatever it is called.

## 3. Escape route 1 — decouple light from clocks (closed by data, not by math)

Section 2 assumed light's local proper speed equals the same constant that
sets local clock rates (local Lorentz invariance / constancy of the fine
structure constant \(\alpha_{\rm fs}=e^2/4\pi\varepsilon_0\hbar c\) and
related dimensionless couplings). Relaxing that — letting light's *local*
propagation speed genuinely differ from the matter/clock-defining constant,
rather than both moving together — breaks the cancellation in Section 2 and
in principle reopens the door.

This is no longer a coordinate artifact; it is a real physical claim: the
fine-structure constant (or an equivalent dimensionless combination
constraining \(c\) relative to atomic physics) must have been measurably
different at the redshifts probed by the supernova time-dilation data
(\(z\sim0.1\text{--}0.8\)), by an amount of order unity in \(\Delta\alpha_{\rm
fs}/\alpha_{\rm fs}\) (an order-unity effect is what is needed — the required
dilation factor \(1+z\) is itself of order \(1.1\)-\(1.8\) over this range, not
a small correction).

Independent measurements exclude this by many orders of magnitude:

- Quasar absorption-spectrum studies (many-multiplet method) constrain
  \(\Delta\alpha_{\rm fs}/\alpha_{\rm fs}\) to roughly \(10^{-5}\)-\(10^{-6}\)
  across \(z\sim0.5\text{--}3\) (Webb et al. and successors; results are mixed
  on whether a small nonzero drift exists, but all reported values and bounds
  are many orders of magnitude below order-unity).
- The Oklo natural fission reactor bounds local variation even more tightly
  at low redshift/recent cosmic time.

An order-unity variation over exactly the redshift range where the
supernova time-dilation measurement is made would be a dramatic, independent
spectroscopic signature. It is not seen. This route is not merely
undeveloped — it is excluded by data already in hand, at a level that leaves
no room for the effect size actually needed.

## 4. Escape route 2 — break homogeneity/isotropy (named, not developed)

A sufficiently contrived anisotropic or inhomogeneous static structure could
in principle evade the homogeneous-and-isotropic assumption in Section 1.
Nothing here rules this out by construction. But it is not developed in this
node because nothing motivates it independent of wanting to avoid this
theorem, and it inherits its own severe burden: it would need to reproduce
the *same* universal \((1+z)\) law along every line of sight to every
supernova (the measured dilation exponent is consistent with \(n=1\)
regardless of sky position), while not producing any of the large-scale
anisotropies that precision CMB and large-scale-structure isotropy tests
would have already caught. This is listed as logically open and practically
unpromising, not as a live candidate.

## 5. Verdict

Section 8 of E-533 asked for a mechanism satisfying:

1. Reproduces universal \((1+z)\) time dilation for any emission process.
2. Is checked against A-115's "hidden expansion terms" failure condition
   before being called non-expansion.

Section 2 above shows condition 1 and the static-space commitment
(non-time-dependent spatial metric) are jointly unsatisfiable for any
homogeneous, isotropic, locally-Lorentz-invariant model — not as an
unmet engineering target, but as a mathematical identity
(\(\tau=\int\alpha\,dt\) removes the effect for any \(\alpha\)). The one
route that survives the math (Section 3) is closed by existing
fine-structure-constant measurements, independently of this framework.
Route 2 (Section 4) is named as formally open but is not a credible
research direction absent independent motivation.

**Per I-02, applying the same standard used in E-533:** the sub-claim
"a homogeneous, isotropic static-space mechanism, respecting local
Lorentz invariance, can reproduce real universal \((1+z)\) time dilation" is
RED. This is now a structural result (Section 2), not only an
empirical exclusion (E-533's Sections 2-3 remain the empirical
evidence; this node explains *why* no repair of E-528's coefficient
could have closed that gap).

## 6. What this does *not* foreclose

Stated explicitly so Section 8 does not collapse into "give up":

- It does not foreclose the compression-field architecture (A-115
  Sections 1-4: Mass Effect, gravity, Mirror-Gate) or the quasar/white-hole
  identification of White Energy (E-530). None of those claims depend on
  the spatial metric being static.
- It does not foreclose deriving an expansion-like spatial time-dependence
  *from* the compression field's own dynamics, rather than importing it as
  an unexplained external postulate. That is a different, larger research
  question than E-528 currently attempts: whether the field equation in
  A-115 Section 1, together with the White Energy circulation, has a
  homogeneous background solution whose effective spatial scaling behaves
  like \(a(t)\) — i.e., whether One-Wave can explain *why* space behaves as
  though it expands, rather than denying that it does. Section 2's
  corollary is precisely the reason this is the only structurally available
  path left inside the static-space commitment: real time dilation requires
  a time-dependent spatial coefficient, so if One-Wave wants to keep both
  (a) universal \((1+z)\) time dilation and (b) an explanation rooted in its
  own field rather than an imported free scale factor, deriving \(a(t)\)-like
  behavior from \(\chi(\mathbf x,t)\)'s own dynamics is the remaining route —
  not a route around this theorem, but the route it points to.
  **Attempted in E-535**, which reduces A-115's own field equation for a
  homogeneous dilation mode to a driven collective-coordinate oscillator and
  finds a genuine (non-artifact) scale factor is available in principle,
  contingent on reproducing the real expansion history and on revising
  E-528/Book 5 Ch4's current no-expansion rules, neither of which is done
  automatically by that node.
- It does not address BAO or CMB \(T(z)\) (E-533 Sections 4-5 remain open
  on their own terms, independent of this node).

## Failure Conditions (for this node itself)

This node fails if: the metric ansatz in Section 1 is shown not to be the
most general static-space case relevant here (i.e., a materially different
static-space construction escapes the cancellation by a route not
considered); if the fine-structure-constant bounds cited in Section 3 are
outdated, misapplied, or the required effect size is smaller than stated
here; or if local Lorentz invariance is itself an assumption this framework
does not intend to keep, in which case Section 3's exclusion needs
re-examination under whatever replaces it (and should be stated as a
deliberate, explicit departure, not a silent one).
