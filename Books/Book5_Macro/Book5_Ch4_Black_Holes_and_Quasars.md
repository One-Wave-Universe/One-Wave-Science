# ONE-WAVE FRAMEWORK
## Book 5 — Macro
## Chapter 4: Black Holes, Quasars, and White Energy / Cosmic Mirror Gate

Version: 1.0 (draft)
Date: July 17, 2026
Class: B — Applied Layer
Spine: Gray / 2D / 3D / Mathematics / Predictions / Yellow Audit / Future Work / Closing Thoughts

Dependencies: A-115 Unified Compression Field, C-301 Mirror Gate, C-309 Friction Limit, B-209 Break Condition,
              A-112a Traveling Lattice Rupture, Book 5 Ch3 (Supernovae),
              E-522 Cellular-Stellar Scale Invariance
Status: YELLOW (structure, real math inherited) / YELLOW (cosmological application unverified)

Grounding note: this chapter develops something already real, not new
— C-301 Mirror Gate has listed "Cosmological level: black hole -> white
hole transition" as one of its scale-invariant applications since
before this session's audit began. It was never elaborated into a
chapter. This is that elaboration, not a fresh invention.

---

## Gray — Standard Model Reference

A black hole is a region of spacetime where gravity is so strong that
nothing, including light, can escape once past the event horizon.
Hawking radiation theoretically allows black holes to slowly evaporate
over cosmological timescales. A white hole is a time-reversed
solution to the same general-relativistic equations — nothing can
enter, only exit — but no white hole has ever been observed, and
whether they can exist physically (versus being a mathematical
artifact of the equations) is unresolved.

A quasar is an extremely luminous active galactic nucleus, powered by
matter accreting onto a supermassive black hole — the accretion disk
itself, not the black hole directly, produces the enormous luminosity
and relativistic jets observed.

Standard Model strength: black hole physics (event horizons,
accretion disks, jets) is well-modeled and observationally confirmed
(black hole imaging, gravitational wave detections from mergers).
Standard Model limitation: white holes remain purely theoretical, and
whether any real astrophysical process corresponds to one is
unresolved. Quasar jet mechanics have open questions regarding exact
launching mechanism.

---

## 2D One-Wave Interpretation

In 2D, a black hole is a tear in the lattice — a region where the
Friction Limit (C-309) itself breaks down, not merely a region of
extreme compression.

This is a stronger and more specific claim than "gravity is very
strong here." C-309 establishes light as a mode that always travels
at exactly v_max. If a region of the lattice cannot support
propagation at all — a genuine structural discontinuity, not just an
extreme gradient — light entering that region has nowhere to
propagate to. That is a proposed local failure of the propagation
medium itself. It has no connection to the Mass-Effect mechanism in
C-318, which remains the four-interaction response of a stable recurrence.

A quasar, in this reading, is what a Mirror Gate crossing (C-301)
looks like at this scale: the compressed state on one side of the
tear undergoes the same symplectic rotation already established for
spin-half (C-308) and proposed for the electron/proton system, and
re-expresses on the other side as outward ejection.

---

## 3D One-Wave Interpretation

In 3D: a black hole is a region where the lattice's structural
continuity fails — not simply high beta (coupling) or high gamma
(damping), but a genuine tear, meaning C-309's v_max = sqrt(beta_max)*
Delta_x/Delta_t has no defined value because Delta_x's normal
lattice-step structure doesn't hold there. This is a candidate
definition, not yet distinguished mathematically from "extremely high
compression" — flagged directly in Yellow Audit below.

C-301's real Mirror math, applied here directly:
M(psi_C, psi_E) -> (psi_E, -psi_C), with M^2 = -I, M^4 = I.

The claim: matter/field-state falling into a black hole undergoes
this same Mirror crossing — already established at quantum
(spin-half), atomic (shell transition), and biological (nerve relay)
scale, per C-301's own pre-existing list. A quasar's relativistic jet
is the M^4=I closure completing at cosmological scale: the compressed
state re-expresses as ejection on "the other side" of the crossing,
matching C-301's own literal wording ("black hole -> white hole
transition") rather than inventing new vocabulary for it.

Recycling, connected honestly to Book 5 Ch3's Break Condition
framing: this IS the same "seeding" mechanism as Ch3's supernova
Reset outcome, at a different point in the same family of
mechanisms — B-209's Break Condition describes a paired loop failing
and releasing material; C-301's Mirror Gate describes what happens to
a compressed state AFTER a sufficiently extreme break, specifically
the flip-and-reappear structure. These may be the same underlying
event viewed at two different stages (approach-to-break vs. the
crossing itself) — a real, checkable candidate relationship, not yet
verified term-by-term.

---

## Mathematics

Mirror operator (C-301, real, inherited unmodified):
M = [[0,1],[-1,0]], M^2 = -I, M^4 = I

Friction limit (C-309, real, inherited unmodified):
c = v_max = sqrt(beta_max) * Delta_x / Delta_t

Candidate black hole condition (new, NOT derived — a proposed
definition requiring further work):
A black hole exists where Delta_x's normal lattice-step definition
fails, making v_max undefined rather than merely very small. This is
different from a Persistent Mode with extremely high compression
(which would still have a defined, if tiny, v_max) — the distinction
between "very strong compression" and "structural failure" has not
been made mathematically precise here.

Candidate quasar condition (new, NOT derived):
Jet luminosity/velocity as a function of the M^4=I closure completing
— no functional form proposed, only the qualitative claim that the
closure produces the ejection.

### Yellow relocation model for a moving tear

A-112a now supplies a minimal conservative model for how a localized
tear could move without leaving an indefinitely growing permanent
fracture. Let `r_i^n` be normalized rupture occupancy at lattice site
`i` and step `n`. For right-moving transport:

```text
r_i^(n+1) = r_i^n - nu(r_i^n-r_(i-1)^n)
nu = v Delta_t / Delta_x
0 <= nu <= 1.
```

Under periodic or zero-flux boundaries:

```text
R_n = sum_i r_i^n
R_(n+1) = R_n.
```

The flux proof is telescoping: what leaves one site enters the next.
Opening and reclosure are the positive and negative parts of the same
state change:

```text
O_i^n = [r_i^(n+1)-r_i^n]_+
C_i^n = [r_i^n-r_i^(n+1)]_+
sum_i O_i^n = sum_i C_i^n.
```

This formalizes "open ahead <-> close behind." It does not yet derive
`nu` from black-hole pressure, gravity, or spacetime observations.

Permanent scar is a separate variable `d_i`, not an automatic result
of rupture transport:

```text
d_i^(n+1) = clip(
  d_i^n + kappa_d[r_i^n-r_damage]_+(1-d_i^n) - lambda_d d_i^n,
  0,1).
```

A normal traveling defect stays below the damage threshold or repairs
behind itself. A propagating fracture is the different regime in which
scar length grows. The mathematical distinction now exists; the claim
that an astrophysical black hole is such a defect remains unverified.

### Event-horizon scaling (candidate, conditional on A-115's own open item)

A-115 section 2 already states the exterior/far-field target this
framework's compression field must hit (not yet derived from the
underlying field equation -- A-115's own "Yellow completion" list still
has "derive chi(r) from sources" as open):

```text
Phi_OW(r) -> -G*M_eff/r,   Phi_OW = alpha_g * chi
```

which gives, in that same exterior regime, `chi(r) -> -G*M_eff/(alpha_g*r)`.

Combining this with this chapter's own tear condition (a tear occurs
where `chi` crosses a critical threshold `chi_crit`, past which C-309's
`v_max` becomes undefined) and solving `|chi(R_tear)| = chi_crit`
(verified symbolically):

```text
R_tear = G*M_eff / (alpha_g * chi_crit)
```

This predicts the tear radius scales **linearly with mass** -- the same
scaling as the real Schwarzschild radius, not a competing prediction.
Matching it exactly to `R_s = 2*G*M/c^2` pins down a specific,
falsifiable calibration target rather than leaving two free constants:

```text
chi_crit = c^2 / (2*alpha_g)
```

If a derived alpha_g does not produce this chi_crit (once chi_crit is
independently derived from whatever makes C-309's v_max undefined),
that is a real quantitative failure of this candidate, not something to
re-tune away.

**Honest limits:** this is conditional on A-115's own not-yet-derived
exterior form, so it shows internal consistency between two already-
written pieces, not a first-principles derivation of event-horizon
scaling from the underlying field equation. It also assumes the
exterior 1/r form extends up to the tear radius itself; A-106's own
Derrick-theorem analysis (used elsewhere this session) shows a bound
field profile is not simply its asymptotic far-field form near the
localized structure, so this boundary assumption needs its own
justification before this candidate can be trusted quantitatively.

### Why only some AGN eject strongly (already implicit in E-530, made explicit)

This does not need a new mechanism -- E-530's own hysteretic threshold
model already answers it, once the connection is stated. The release
state `h` switches on only when `U_C >= U_on` and off when `U_C <=
U_off`. An object whose accretion supply (`P_cap`, `P_nu`) is too low,
or too intermittent, to ever push `U_C` above `U_on` simply stays in
`h=0`: continuous quiet accretion, no strong ejection -- not a
different mechanism from an object that does eject, just a trajectory
that never crosses the same threshold. A high-supply object crosses
`U_on` repeatedly and cycles through release events.

This reuses E-530's existing math rather than proposing new mechanism,
and it lines up with a real, independent observation this framework did
not need to explain away: real AGN jet power is known (Gray) to
correlate with accretion state and black-hole spin (e.g. the
Blandford-Znajek mechanism), so a candidate follow-up is to identify
`P_cap`'s dependence on rotation explicitly, rather than treating it as
a free accretion-rate parameter alone.

**Honest limits:** this explains the qualitative on/off structure, not
a quantitative duty cycle. Mapping `U_on`, `U_off`, `P_cap` to real
observables (accretion rate, spin, AGN population statistics) is
untouched, and E-530's own unaccounted-sink problem (`lambda_C*U_C`,
above) needs fixing before any of these thresholds can be trusted
numerically.

---



## White Energy: Population-Scale Return

One-Wave rejects expansion of space. The term **White Energy** names the outward-return side of the cosmic circulation: stored compression is released through quasar/white-hole-scale Mirror-Gate events and reinjected into the field.

The "massive ATP ejection" phrase is an architectural analogy. It means stored energy is released to drive the next system state. It does not claim astrophysical objects use cellular chemistry.

The compact reservoir follows E-530:

\[
\frac{dU_C}{dt}=P_{\rm cap}+P_\nu-\lambda_CU_C-D_WhU_C,
\]

\[
P_W=D_WhU_C.
\]

The release state turns on at \(U_{\rm on}\) and off at \(U_{\rm off}<U_{\rm on}\). Recharge, state-dependent discharge, and hysteresis are all required for repeated events.

White Energy remains part of the energy inventory while it travels outward:

\[
\frac{dE_W}{dt}=P_W-P_{W\to\chi}-\Phi_{W,\partial\Omega}.
\]

For a closed accounting domain,

\[
E_{\rm tot}=E_\gamma+E_\chi+E_\nu+E_C+E_W,
\qquad
\frac{dE_{\rm tot}}{dt}=0.
\]

Static long-term balance requires

\[
\langle P_W\rangle
=
\langle P_{\rm cap}+P_\nu-\lambda_CU_C\rangle.
\]

No Hubble parameter, scale factor, or negative-pressure equation belongs in the One-Wave model.

## Redshift and Return Loop

E-528 gives the static propagation law

\[
1+z=\exp\left(\int_0^D\kappa_\gamma d\ell\right).
\]

Energy removed from a Propagating Light Mode enters the compression field. E-529 proposes Low-Coupling Return Modes as one transport channel toward compact reservoirs. E-530 closes the candidate loop:

```text
compression and Mass Effect
-> gravity / extended compression
-> tired-light redshift and field transfer
-> Low-Coupling Return Modes
-> compact reservoir
-> Mirror-Gate threshold
-> White Energy ejection
-> field reinjection
```

## Yellow Audit

- White Energy is a naming and architecture lock, not experimental closure.
- The quasar/white-hole identification remains Green.
- The tired-light coefficient is not derived.
- Neutrino deposition into compact reservoirs is not derived.
- Population-scale static energy balance has not been simulated.
- No expansion variable is permitted in future One-Wave equations.
- UNACCOUNTED SINK (E-530): the compact reservoir's `lambda_C*U_C` decay
  term has no destination anywhere in E-530's stated system -- it does
  not reappear as a source term in any of the other four energy
  channels, and the "closed accounting domain" claim (`dE_tot/dt=0`)
  does not currently hold as written. See E-530's Yellow Audit; this
  must be fixed in the equations before any simulation of this chapter's
  Cosmic Loop is meaningful.
- RESOLVED IN PART: event-horizon scaling now has a candidate --
  combining A-115's own required exterior limit with this chapter's
  tear condition gives `R_tear = G*M_eff/(alpha_g*chi_crit)`, linear in
  mass like the real Schwarzschild radius, with a specific calibration
  target `chi_crit = c^2/(2*alpha_g)` rather than two free constants.
  This is conditional on A-115's exterior form (itself not yet derived
  from the field equation) and on the far-field profile extending to
  the tear radius (not independently justified) -- see "Event-horizon
  scaling" above.
- RESOLVED IN PART: AGN ejection-selectivity is already implicit in
  E-530's existing hysteresis (h switches on only above U_on) rather
  than needing a new mechanism -- see "Why only some AGN eject
  strongly" above. Still open: mapping U_on/U_off/P_cap to real
  accretion-rate and spin observables, and E-530's own unaccounted-sink
  problem needs fixing before these thresholds mean anything numerically.

## Future Work

1. Simulate E-528 through E-530 as one closed energy-conserving system --
   blocked until E-530's lambda_C*U_C sink is given a destination or set
   to zero; see that node's Yellow Audit.
2. Calibrate a static redshift coefficient without image blurring or unexplained heating.
3. Derive Return-Mode production and deposition coefficients.
4. Map compact-reservoir parameters to quasar observations without reverse fitting.
5. Derive chi(r) from A-115's underlying field equation (its own open
   item) so the event-horizon scaling candidate above stops being
   conditional on an unverified exterior form.
6. Derive chi_crit independently (from whatever makes C-309's v_max
   undefined) and check it against c^2/(2*alpha_g) -- a real
   quantitative test this candidate can fail.
7. Map P_cap's dependence on accretion rate and black-hole spin
   explicitly, then compare the predicted eject/no-eject duty cycle
   against real AGN population statistics.
