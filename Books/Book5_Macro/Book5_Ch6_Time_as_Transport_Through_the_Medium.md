# Book 5 — Chapter 6: Time as Transport Through the Medium

Status: YELLOW — One-Wave mechanism hypothesis; relativistic recovery and cosmology validation incomplete.

## The missing cosmology mechanism

One-Wave already had three pieces:

1. a wave equation with finite propagation speed;
2. a lattice dispersion/propagation ceiling;
3. a static redshift transport proposal.

What was missing was the explicit physical connection to time dilation.

This chapter states that connection as a testable hypothesis rather than leaving it implicit.

## Core idea

In the One-Wave interpretation, motion is not motion through empty mathematical space. A persistent pattern changes by propagating through a continuous superfluid-like field, approximated in some nodes by a local lattice.

The medium cannot transmit a change arbitrarily fast.

C-309 and E-509 already contain the propagation ceiling. E-533 asks:

what happens to the pattern's own local evolution as progressively more of the available update is committed to translation through the medium?

The candidate answer is that local evolution decreases as transport approaches the ceiling.

## Velocity-only target

Let

\[
\rho_v=\frac{v^2}{c^2}.
\]

Candidate remaining local-update fraction:

\[
\rho_{\rm local}=1-\rho_v.
\]

If proper-time evolution tracks the square root of that available local capacity,

\[
\frac{d\tau}{dt}
=
\sqrt{1-\frac{v^2}{c^2}},
\]

then

\[
dt
=
\frac{d\tau}{\sqrt{1-v^2/c^2}}.
\]

That reproduces the familiar Lorentz timing factor.

The scientific burden is not writing this equation. The burden is deriving the square-root relation from One-Wave update/dispersion mechanics instead of borrowing the answer.

## The edge-of-wave limit

When

\[
v\to c^-,
\]

the candidate local-update capacity tends to zero:

\[
\rho_{\rm local}\to0.
\]

In the physical language of this framework, that is the wave-edge limit: the pattern is maximally committed to propagation and has no remaining update capacity for internal evolution relative to the external reference.

This gives a mathematical target for the phrase "stuck in place and in time." It is an asymptotic transport limit, not permission for ordinary massive structures to move at c.

## Transport difficulty and gravity/cosmology

Velocity need not be the only contributor.

Define a local medium-difficulty state

\[
\Xi=\Xi(\chi,\nabla\chi,\gamma,\beta,\ldots).
\]

Then the general One-Wave timing problem becomes

\[
\frac{d\tau}{dt}
=
\mathcal T(v,\Xi).
\]

Required limits:

\[
\mathcal T(0,0)=1,
\]

and, if One-Wave truly recovers special-relativistic timing,

\[
\mathcal T(v,0)
=
\sqrt{1-\frac{v^2}{c^2}}.
\]

If increased medium difficulty slows local evolution,

\[
\frac{\partial\mathcal T}{\partial\Xi}<0.
\]

This is where a physical interpretation of gravitational and cosmological timing could enter, but it is not yet derived.

## Redshift must share the same medium law

E-528 proposes

\[
1+z
=
\exp\left[\int\kappa_\gamma d\ell\right].
\]

A viable non-expansion cosmology cannot bolt time dilation on afterward.

It must derive both redshift and transient-duration behavior from one frozen medium description:

\[
\{\chi,\nabla\chi,\gamma,\beta,\ldots\}
\rightarrow
\{\kappa_\gamma,\mathcal T\}
\rightarrow
\{z,\Delta t_{\rm obs}\}.
\]

That is the real test.

## Supernova attack

The immediate cosmology test is therefore not merely "does redshift fit distance?"

It is:

can one frozen One-Wave medium law predict both supernova redshift and observer-frame light-curve duration without inserting the standard (1+z) timing factor by hand?

Pantheon+-type light-curve data should be used only after the timing law is frozen.

## Failure means information

If the exact A-114/C-309/E-509 mechanics cannot generate a Lorentz-compatible timing law, this mechanism fails.

If the same law cannot fit redshift and duration together, the strong shared-medium cosmology fails.

If event-specific tuning is required, the model fails as a universal transport law.

A failed mechanism should be revised or dismissed, not protected by relabeling.

## Canonical chain

Book1 Ch16a wave equation
-> A-114 dispersion
-> C-309 friction/propagation ceiling
-> E-509 local propagation limit
-> E-533 time-transport mechanism
-> E-528 static redshift coupling
-> supernova/cosmology held-out tests

## Next work

1. solve the exact A-114 roots across the stable branch;
2. identify a conserved update budget/norm;
3. derive local-versus-transport allocation from that norm;
4. test whether the square-root timing law emerges;
5. freeze \mathcal T;
6. only then fit supernova timing/redshift data.

## Resistance/change experiment

[E-533 owns the resistance/change interpretation](../../Nodes/E-533_Superfluid_Transport_Time_Dilation.md#resistance-and-change-interpretation--2026-10-04). [The executed propagation control](../../solvers/TIME_RESISTANCE_PROBE.md) measures packet motion, carrier phase and decay from the actual recurrence. All five numerical controls pass across nine cases; the simple damping/carrier-clock identification does not derive universal clock slowing or Lorentz recovery. The next physical test needs a self-held periodic excitation and a measured reversible field-work response.

The [full factor inventory and operational clock-rate definition](../../Nodes/E-533_Superfluid_Transport_Time_Dilation.md#time-clock-rate-and-the-full-response-factors) specifies what the next experiment must retain and measure together. Resistance includes reversible field response; damping alone does not define it. The measured timing ratio compares calibrated internal and reference cycles, while field work and the resulting rate must follow from one shared dynamics.
