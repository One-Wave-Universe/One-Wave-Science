---
id: G-764
title: Six-Route Commitment Map From the Biased Double-Well Test Bench
status: yellow
tier: executable-math
claim_boundary: closed-form analysis of the specific test-bench equation UPDATED_43 Section 4 already proposed; not a claim that this is the physical carrier
---

# Node G-764: Six-Route Commitment Map From the Biased Double-Well Test Bench

## Purpose

UPDATED_43 Section 3 states the open problem exactly:

> The unresolved derivation is a map `K : (route, prior_state, differential,
> thresholds, phase) -> {-3,-2,0,+2,+3}`. No arbitrary lookup table is
> canonical until this map is derived or calibrated.

Section 4 hands over the tool to derive it with: a damped, driven, biased
double-well oscillator, offered explicitly as "a proposed test bench, not yet
the One-Wave physical law," with required outputs "center residence,
crossing direction, partial/full excursion, hysteresis, return, and phase."

This node solves that test bench in closed form and derives `K` from it —
not a calibrated fit, not an asserted lookup table, but bifurcation and
fixed-point analysis of the exact equation UPDATED_43 already wrote down.
Every threshold below is a critical point of that equation, not a chosen
number.

## 1. The equation, restated

\[
\ddot x+2\zeta\omega_0\dot x+\frac{dV}{dx}=u(t),
\qquad
V(x;h)=\frac{a}{4}x^4-\frac{b}{2}x^2-hx,
\qquad a,b>0.
\]

**Route assignment (new, stated explicitly as a modeling choice, not derived):**
the binary choice sets the sign of the bias, \(h=+h_0\) for YES, \(h=-h_0\)
for NO, \(h=0\) for Ground; the ternary movement is read off the trajectory's
crossing behavior relative to \(x=0\), matching UPDATED_43's own description
of ternary as "a readout of motion around an active center," not an
independent drive parameter. \(u(t)\) is reserved for whatever additional
external drive a given route/context supplies; the results below hold for
\(u(t)=0\) after any transient drive ends, i.e., they characterize where the
system *settles*, which is what a readout needs.

## 2. Fixed points at zero bias (\(h=0\))

\[
\frac{dV}{dx}=ax^3-bx=x(ax^2-b)=0
\quad\Longrightarrow\quad
x=0,\ \ x=\pm x_\pm,\qquad x_\pm\equiv\sqrt{b/a}.
\]

\(x=\pm x_\pm\) are the two committed wells. \(x=0\) is Ground.

## 3. Ground/Hold is a saddle, not a rest state — active, as UPDATED_43 already says

Linearizing about \(x=0\): \(dV/dx\approx-bx\), giving
\(\ddot x+2\zeta\omega_0\dot x-bx=0\), characteristic roots

\[
r_\pm=-\zeta\omega_0\pm\sqrt{\zeta^2\omega_0^2+b}.
\]

Since \(b>0\), the term under the root always exceeds \(\zeta\omega_0\), so
\(r_+>0\) always: **\(x=0\) is an unstable saddle for every choice of
\(\zeta,\omega_0,b>0\).** A system placed at Ground and left undriven does
not stay there — it is repelled toward one well or the other. This is a
derived confirmation, not an assumption, of UPDATED_43's own claim that
"Hold is the active switching/reference region, not absence": residing at
Hold requires nonzero \(u(t)\) actively cancelling the saddle's unstable
mode. Passive rest only exists at the two committed wells.

## 4. The Hold/Partial threshold: the inflection point

\[
\frac{d^2V}{dx^2}=3ax^2-b=0
\quad\Longrightarrow\quad
x^\ast=\sqrt{b/3a}=\frac{x_\pm}{\sqrt3}.
\]

This is where the potential's curvature changes sign — the natural boundary
between the central saddle region and the outer well-dominated region. The
ratio \(x^\ast/x_\pm=1/\sqrt3\) is exact and **independent of \(a,b\)** —
a parameter-free structural constant of this potential family.

## 5. The hysteresis threshold: exact bifurcation field

With bias \(h\), critical points solve \(ax^3-bx-h=0\). Writing this as a
depressed cubic \(x^3-(b/a)x-(h/a)=0\), the discriminant condition for three
real roots (bistable: both wells still exist) versus one real root
(monostable: forced) is

\[
\Delta>0
\iff
\frac{4b^3}{a^3}>\frac{27h^2}{a^2}
\iff
|h|<h_c,
\qquad
h_c\equiv\sqrt{\frac{4b^3}{27a}}=\frac{2}{3\sqrt3}\sqrt{\frac{b^3}{a}}.
\]

For \(|h|<h_c\): both wells coexist. Which one a trajectory ends up in
depends on where it started (or which well it was already in) — genuine
**hysteresis**: sweep \(h\) up through \(+h_c\) then back down through
\(-h_c\) and the system does not retrace the same path; it stays captured in
whichever well it already occupies until forced out at the *far* threshold.
For \(|h|>h_c\): only one well exists — the outcome is forced regardless of
history.

This gives a second, independent way to read "partial" versus "full"
commitment, complementary to Section 4's position-based one: **partial**
commitment is a bias-driven but still-contingent (history-dependent) outcome
(\(|h|<h_c\)); **full** commitment is a forced, history-independent outcome
(\(|h|\ge h_c\)).

## 6. The five-state map \(K\)

Using the position-based thresholds from Sections 2 and 4 (readout position
\(x(T)\) at the declared readout time, after any transient drive has
settled):

\[
K(x(T))=
\begin{cases}
-3 & x(T)\le-x_\pm & \text{full disagree}\\
-2 & -x_\pm<x(T)\le-x^\ast & \text{partial disagree}\\
\phantom{-}0 & -x^\ast<x(T)<x^\ast & \text{unity / Hold reference}\\
+2 & x^\ast\le x(T)<x_\pm & \text{partial agree}\\
+3 & x(T)\ge x_\pm & \text{full agree}
\end{cases}
\]

with \(x^\ast=x_\pm/\sqrt3\) exactly. This is a genuine derivation from the
equation's own critical points — not a chosen lookup table — and it can be
cross-checked against Section 5's independent field-based criterion
(\(|h|\lessgtr h_c\)) for consistency on any given trajectory: agreement
between the two criteria is itself a testable prediction of this node, not
guaranteed by construction (they use different information — one reads the
final position, the other reads whether the well the trajectory is in still
has a partner).

## 7. Capture / return criterion

A trajectory that has crossed \(x^\ast\) toward a well has *not* necessarily
committed — it can still return if damping has not yet removed enough
energy. Using the mechanical energy \(E(t)=\tfrac12\dot x(t)^2+V(x(t);h)\),
a trajectory on the well side of \(x^\ast\) is **captured (no return)** once

\[
E(t)<V(x^\ast;h),
\]

i.e., it no longer has enough energy to climb back over the local barrier at
\(x^\ast\). While \(E(t)\ge V(x^\ast;h)\), the trajectory can still cross
back — this is UPDATED_43's required "return" output, given a precise,
checkable definition directly from the equation of motion rather than a
qualitative description.

**Caveat confirmed by G-765:** this criterion is only valid while \(h\) is
held fixed. If \(h(t)\) itself changes after a trajectory is marked
captured, the barrier \(V(x^\ast;h)\) moves and a previously-captured
trajectory can become uncaptured with no new energy added to it — the field
did work when \(h\) changed, so nothing is violated, but the captured/escaped
read must be re-evaluated at the new \(h\), not carried forward from the old
one. G-765 Section 4 shows this exact transition numerically.

## 8. Phase: post-commitment ringdown frequency

Linearizing about either well, \(V''(x_\pm)=3a(x_\pm)^2-b=3b-b=2b\), giving
a local oscillation (ringdown) frequency

\[
\omega_{\rm well}=\sqrt{2b},
\]

decaying at rate \(\zeta\omega_0\) from the same damping term. This is the
"phase" of residual oscillation once a route has committed to a well — a
derived, well-defined quantity, distinct from the (undamped, unstable)
behavior at Ground in Section 3.

**This formula is derived at \(h=0\) only.** G-765 found by direct
numerical measurement that a *biased* well's rest point \(x_{\rm well}(h)\)
is not \(x_\pm\) — it is the shifted root of \(ax^3-bx-h=0\) — so its local
curvature is \(V''(x_{\rm well}(h))=3a\,x_{\rm well}(h)^2-b\neq2b\) in
general. Including the standard damped-oscillator correction, the general
ringdown frequency is

\[
\omega_{\rm ring}=\sqrt{V''(x_{\rm well}(h))-(\zeta\omega_0)^2},
\]

which reduces to \(\sqrt{2b}\) exactly at \(h=0\) (where \(x_{\rm
well}(0)=x_\pm\)) and matched a direct numerical measurement to four
significant figures at \(h=-0.3\) in G-765. G-765 Section 5 flags this as
checked numerically at one biased point, not yet proven in closed form for
general \(h\).

## 9. Required-output checklist (UPDATED_43 Section 4)

| Required output | This node's answer |
|---|---|
| Center residence | \(\lvert x(t)\rvert<x^\ast\); Section 3 shows this requires active \(u(t)\), not passive rest |
| Crossing direction | sign of \(\dot x\) at the moment \(\lvert x\rvert\) crosses \(x^\ast\) |
| Partial/full excursion | position criterion, Section 6 (\(x^\ast\) vs \(x_\pm\)); cross-checked by the field criterion, Section 5 (\(h_c\)) |
| Hysteresis | Section 5, exact closed form \(h_c=\sqrt{4b^3/27a}\) |
| Return | Section 7, energy-vs-barrier criterion \(E(t)\lessgtr V(x^\ast;h)\) |
| Phase | Section 8, \(\omega_{\rm ring}=\sqrt{V''(x_{\rm well}(h))-(\zeta\omega_0)^2}\), reducing to \(\sqrt{2b}\) at \(h=0\) |

## What this is not

- Not a claim about the physical carrier (magnonic, MTJ, or otherwise) —
  this stays entirely at the level UPDATED_43 Section 4 set: "a proposed
  test bench, not yet the One-Wave physical law."
- Not a replacement for G-739's trajectory extractor — G-739 measures gates
  from arbitrary declared trajectory data; this node's closed-form
  trajectories are exactly the kind of declared data G-739's extractor
  should be run against as a first validation case, which is proposed as
  the next step, not performed here.
- Not a claim that \(a,b,\zeta,\omega_0,h_0\) have physical values — they
  remain free parameters of the test bench, as UPDATED_43 left them.
- Does not touch the five-state *self lifecycle* (G-742,
  Idle/Primed/Executing/Vectoring/Resolving) or the Field/Void ternaries
  (G-740) — per UPDATED_44, these are separate structures from the
  commitment/readout axis addressed here, and this node does not conflate
  them.

## Failure Conditions

This node fails if: the route-to-\((h,u)\) assignment in Section 1 is shown
to contradict how routes are used elsewhere (it is flagged here as a new
modeling choice, not a derivation, specifically so it can be checked); if
running actual trajectories of this equation through G-739's extractor
produces gate sequences inconsistent with the \(K\)-map's position/field
readout in a way not explained by the different quantities each measures;
or if the discriminant/bifurcation algebra in Section 5 is found to be in
error (it should reproduce the standard cusp-catastrophe threshold for
\(x^3-px-q\); this is a known result, not novel, and is checkable
independently of this repository).

## Recommended Next Step

Run G-739's extractor against numerically integrated trajectories of this
exact equation across a grid of \((h,u(t))\) route assignments and confirm
the gate sequence (Begin/Build/Hold/Build/Break/Loop) it measures lines up
with the crossing/capture events derived here. That is a Yellow-to-Bronze
promotion test this node sets up but does not perform.

**Update:** G-765 performs this test on one concrete trajectory. The gate
order was reproduced, the Loop-crossing time matched exactly, and two real
corrections came out of it — both folded back into Sections 7 and 8 above.
G-765's own Recommended Next Step is to extend the same test across a grid
of \((h_0,\gamma)\) rather than the single program used so far, and to prove
the Section 8 generalization in closed form for general \(h\).
