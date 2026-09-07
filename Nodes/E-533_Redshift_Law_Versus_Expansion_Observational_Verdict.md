---
node_id: "E-533"
canonical_name: "Redshift Law Versus Expansion: Observational Verdict"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cosmology / Redshift / Falsification Audit"
claim_gate_detail: "GREEN (the audit itself: math, external data, and verdict are complete and reproducible) / the audited sub-claim (redshift without any time-dilation-carrying mechanism) is RED per I-02 -- see Verdict"
metadata_standard: "I-06"
---

# Node E-533: Redshift Law Versus Expansion — Observational Verdict

**Dependencies**
Upstream: E-528 Static Redshift Transport, E-529 Low-Coupling Return Mode, E-530 White Energy Recirculation Loop, A-115 Unified Compression Field, Book 5 Ch4 Black Holes and Quasars, I-02 Node Proof and Trust Lifecycle, I-06 Canonical Node Metadata
Downstream: ONE_WAVE_SCIENCE_ATTACK_MAP.md Section L, any future revision of E-528

## Purpose

This node executes the Section L attack from `ONE_WAVE_SCIENCE_ATTACK_MAP.md` verbatim:

> identify a single explicit redshift law; compare against supernova, BAO, CMB,
> time-dilation, and surface-brightness observations; keep observational fit
> separate from mechanism preference; reject or revise any version that cannot
> match the full data set.

It also runs the specific Failure Tests E-528 already listed for itself but that
no downstream node had yet executed: frequency dependence, image blurring,
"redshift-correlated transient-duration behavior without metric time
stretching," and consistency across paths.

This is an audit, not a new mechanism proposal. It changes no upstream field
equation. It reports what the existing E-528/E-529/E-530/A-115 claim, taken at
face value, predicts for five independent outside measurements, and applies
I-02's Gray-to-Red rule honestly: a real, externally-sourced result (not
derived from or fitted to One-Wave) is checked against the model's own stated
prediction. Per I-02, Red is a record of an outcome, not a claim of victory,
and it is scoped to the specific sub-claim the data actually constrains — it
does not reach back and invalidate the rest of the Unified Compression Field
architecture.

## 1. The single explicit redshift law (Attack Map step 1)

E-528 already gives one explicit law. Restated with nothing added:

\[
1+z=\exp\!\left[\int_0^D\kappa_\gamma(\ell)\,d\ell\right],
\qquad
z\approx\kappa_\gamma D \ \text{(for }\kappa_\gamma D\ll1\text{)}.
\]

Photon number is conserved along the ray (\(dN_\gamma/d\ell=0\)); only photon
energy/frequency falls. Space itself does not move, expand, or carry a scale
factor — this is E-528's own Hard Constraint, repeated in Book 5 Ch4 ("No
Hubble parameter, scale factor, or negative-pressure equation belongs in the
One-Wave model") and in A-115 ("One-Wave uses no scale factor and no
expansion of space").

Call this the **static-propagation hypothesis**: redshift is produced
entirely by something happening to the photon in flight through an otherwise
static, non-expanding background, and nothing else about spacetime, clocks,
or emission processes is altered.

Everything below follows from taking that hypothesis exactly as written and
asking what it predicts for measurements that already exist.

## 2. Test 1 — Type Ia supernova light-curve time dilation (decisive)

**What standard (expanding) cosmology predicts.** In an expanding metric, the
proper time between two events at the source (e.g. two points on a supernova's
brightness curve, separated by \(\Delta t_{\rm em}\) in the supernova's own
rest frame) maps to an observed time separation

\[
\Delta t_{\rm obs}=(1+z)\,\Delta t_{\rm em}.
\]

This is the *same* \((1+z)\) that sets the wavelength stretch — both come from
one expansion factor \(a(t)\) evaluated at emission versus observation. The
two numbers are not independent measurements of two different things; they
are forced to be numerically equal by the single underlying mechanism.

**What the static-propagation hypothesis predicts.** In E-528's static
background, two photons emitted \(\Delta t_{\rm em}\) apart travel the same
path length \(D\) at the same propagation behavior as each other (\(\kappa_\gamma\)
is a function of path, not of *when* a given photon entered the path). Nothing
in \(dE_\gamma/d\ell=-\kappa_\gamma E_\gamma\) touches emission-to-emission
timing at all. The predicted observed separation is

\[
\Delta t_{\rm obs}=\Delta t_{\rm em}
\]

— no dilation, regardless of the redshift accumulated over the same path.

**The outside measurement (\(E(x,r)\), not derived from or fitted to
One-Wave).** Type Ia supernova light-curve widths have been measured across
\(z\approx0.1\text{–}0.8\) and shown to stretch with redshift as a power law
\((1+z)^n\) with \(n\) consistent with \(1\) and inconsistent with \(0\) at high
significance:

- Goldhaber et al. 2001 (ApJ 558, 359): \(n=1.03\pm0.07\), using the
  Supernova Cosmology Project sample.
- Blondin et al. 2008 (ApJ 682, 724): tighter sample, same result, \(n=0\)
  (no dilation) excluded at many standard deviations.

This specific test was built for exactly this purpose: it was designed to
distinguish expansion-based redshift from tired-light-style static
propagation, because it is the one clean case where the two hypotheses make
numerically different, non-adjustable predictions for the same measurement
(\(n=1\) vs. \(n=0\)) with no free parameter available to the static model to
close the gap.

**Verdict on this test.** The static-propagation hypothesis, as written in
E-528, predicts \(n=0\). The outside data give \(n\approx1\) and exclude
\(n=0\). This is a direct hit against the hypothesis, not an unmodeled detail
— see Section 6 for why no in-flight photon mechanism can be patched to fix
it without secretly becoming a form of expansion.

## 3. Test 2 — Tolman surface-brightness test

Surface brightness (flux per unit solid angle) of a fixed-size standard
object scales differently under the two hypotheses:

- Expanding-universe prediction (uncorrected): \(\mathrm{SB}\propto(1+z)^{-4}\)
  — one \((1+z)\) from photon energy, one from arrival-rate time dilation, two
  from the angular-diameter-distance relation.
- Static-Euclidean / tired-light prediction: \(\mathrm{SB}\propto(1+z)^{-1}\)
  — only the photon-energy factor; no time-dilation factor (Test 1), and
  angular size falls as ordinary \(1/D\) with no expansion-driven
  angular-diameter turnover.

Lubin & Sandage (2001, AJ 122, 1071/1084/1113), using HST photometry of
brightest cluster ellipticals chosen specifically to minimize galaxy
evolution, measured a surface-brightness decline close to the expanding-universe
range (roughly \((1+z)^{-3}\) to \((1+z)^{-4}\) after evolution correction) and
excluded the static \((1+z)^{-1}\) law at high confidence.

**Verdict on this test.** Same direction as Test 1: the static-propagation
number is excluded by the outside measurement.

## 4. Test 3 — CMB blackbody spectrum and \(T(z)\)

Two separate facts, both already measured, both bear on this:

1. **Spectral shape.** COBE FIRAS measured the CMB to be a blackbody to
   better than \(50\) parts per million (Fixsen 1996; Fixsen 2009 reanalysis).
   A frequency-*independent* \(\kappa_\gamma\) (i.e. \(\kappa_\gamma(\mathbf
   x,\chi,\nabla\chi)\) with no \(\nu\) dependence) is mathematically capable
   of preserving blackbody shape, because uniform fractional photon-energy
   loss is a pure rescaling of the Planck function — the same reason
   expansion preserves it. This much is *not* automatically excluded, but it
   requires committing E-528's \(\kappa_\gamma\) to be exactly
   frequency-independent, which contradicts E-528's own stated general form
   \(\kappa_\gamma(\mathbf x,\nu,\chi,\nabla\chi)\) unless the \(\nu\)
   dependence is fixed to zero by hand. This is listed as one of E-528's own
   open Failure Tests ("frequency dependence or independence") and remains
   unresolved.
2. **Temperature–redshift relation.** \(T(z)=T_0(1+z)\) has been measured
   directly at multiple redshifts via CN/CO rotational-excitation lines in
   quasar absorption spectra and via the Sunyaev–Zel'dovich effect (e.g.
   Noterdaeme et al. 2011, A&A 526, L7, out to \(z\sim2\text{–}3\)), and
   matches the expansion prediction. This measurement is independent of the
   supernova and surface-brightness tests above — it is a different physical
   coupling (molecular excitation by ambient photon bath) at different
   redshifts along different lines of sight, yet it recovers the identical
   \((1+z)\) law. The static-propagation hypothesis has no built-in reason
   for a completely separate physical process (whatever couples the "field"
   to this molecular excitation) to reproduce the same numerical law as the
   photon-energy-loss law of Section 1 — under the static hypothesis these
   would be two unrelated free-parameter fits that happen to agree exactly.

**Verdict on this test.** Not an automatic exclusion like Tests 1–2, but it
adds a second independent requirement (frequency-independent \(\kappa_\gamma\))
that the E-531 dual-harmonic form does not obviously satisfy, plus an
unexplained coincidence (two unrelated channels giving the identical
\((1+z)\) law) that expansion explains for free and the static hypothesis does
not.

## 5. Test 4 — BAO standard ruler across redshift

The baryon acoustic oscillation scale (the sound horizon at recombination,
\(\approx150\) Mpc comoving) has been measured as an apparent angular/redshift
scale from \(z\approx0.1\) (galaxies) out to \(z\approx2.3\) (Lyman-\(\alpha\)
forest in quasar spectra), and is consistent with one expansion history
\(H(z)\) tied to the same sound horizon independently fixed by the CMB
acoustic peaks (Planck Collaboration 2020, A&A 641, A6, and the BOSS/eBOSS BAO
compilation). The static-propagation hypothesis has no mechanism that
produces a standard-ruler apparent size varying with redshift in this specific
non-trivial way (it would need an ad hoc distance-redshift relation
constructed to match, which is curve-fitting the conclusion rather than
predicting it).

**Verdict on this test.** Not addressed by anything in E-528/E-529/E-530.
Open, and structurally hard for a static-Euclidean model for the same reason
as Test 2.

## 6. Why this cannot be patched by a better \(\kappa_\gamma\) (structural argument)

Section 2 is not a calibration problem. Here is why no choice of
\(\kappa_\gamma(\mathbf x,\nu,\chi,\nabla\chi)\), however elaborate, can fix
it while keeping E-528's Hard Constraint:

Redshift (Section 1's law) is something that happens to a photon **after** it
leaves the source, during transit. Time dilation of a light curve (Test 1) is
a statement about the **spacing between emission events at the source**,
as reconstructed from arrival times at the observer. A propagation-only
effect — no matter what it does to a photon's energy between source and
observer — cannot change how far apart two *different* photons' emission
times were, because that spacing was already fixed before either photon
started propagating. Expansion produces the dilation not by acting on photons
in flight but by *stretching the space the later photon still has to cross
while it is in flight*, which is a statement about the metric changing with
time, not about photon energy loss.

To reproduce \(\Delta t_{\rm obs}=(1+z)\Delta t_{\rm em}\) from a static
background, the model would need the effective light-transit time itself —
not just the photon's energy — to depend on *when* the photon was emitted, in
exactly the way a stretching metric would produce. That is precisely what
A-115's own Direct Failure Conditions rule out: *"if redshift requires hidden
expansion terms"* the model fails. A propagation law that reproduces cosmological
time dilation without a metric doing the stretching is not a known
possibility in this analysis, and none of E-528/E-529/E-530/E-531 currently
proposes one.

## 7. Verdict

Per I-02: \(C(x,r)=\text{DirectEquivalent}\) — the static-propagation
hypothesis and standard expansion make numerically different, well-defined
predictions for the same measurement (Test 1), with no shared free parameter.
\(E(x,r)\) is defined (Goldhaber 2001; Blondin 2008; independently, Lubin &
Sandage 2001 for Test 2) and forces the negation of the static-propagation
hypothesis's own stated prediction (\(n=0\)).

**Sub-claim RED per I-02:** *"Redshift produced solely by static in-flight
photon-energy loss, with no other change to emission timing, clocks, or
metric, fully replaces expansion."* This specific sub-claim is excluded by
external data (Tests 1–2) independent of One-Wave's other claims.

**Not RED — explicitly out of scope for this verdict:**
- The Mass Effect / four-interaction architecture (A-115 Sections 1–4).
- The quasar/white-hole identification of White Energy (E-530) as an
  astrophysical ejection phenomenon — nothing here bears on whether that
  identification is correct.
- Whether *some* static-propagation energy-loss channel exists alongside
  expansion as a subdominant effect (untested; not what E-528 currently
  claims, which is full replacement).

The Section L attack map's own standard applies here without modification:
*"reject or revise any version that cannot match the full data set."* This
version does not match the full data set on Tests 1–2 specifically. Tests 3–4
add further unmet requirements rather than independent failures.

## 8. What would actually have to be true for a revised version to survive

**Update: items 1-2 below were attempted in E-534 and found structurally
unsatisfiable for the general static-space case (a no-go theorem, not an
unmet target) — see E-534 for the derivation and the one route it leaves
open (Section 6 there).**

Not a proposal — a specification of the minimum bar, so future work is not
spent on variants that cannot clear it:

1. A mechanism that makes emission-to-emission timing at the source stretch
   by exactly the same factor as the photon energy redshift, for *any*
   emission process (nuclear-decay-powered supernova light curves, orbital/
   accretion variability, particle decay), not tuned per source type.
2. Section 6 shows that requires something that acts like a time-varying
   transit condition, not a per-photon energy loss. If that something is
   added, it must be checked against A-115's explicit failure condition
   ("if redshift requires hidden expansion terms") before being called
   non-expansion — a mechanism that reproduces \((1+z)\) transit-time
   stretching while insisting it is not a form of expansion needs its own
   argument for why not, not an assertion.
3. A frequency-independent \(\kappa_\gamma\) (Test 3) reconciled with E-531's
   dual-harmonic propagation operator, or an explicit statement that E-531
   does not apply to the redshift channel.
4. An explicit BAO-scale prediction (Test 4) derived from the static model's
   own distance relation, checked against the existing measurement, before
   any claim of matching it.

Absent (1)-(2), Tests 1-2 above are not revisable by recalibrating
\(\kappa_\gamma\) — they are excluded by construction, per Section 6.

## Failure Conditions (for this node itself)

This audit fails if: the cited external measurements are shown to be
mischaracterized or their citations invalid; if a static-propagation
mechanism satisfying Section 8's bar already exists elsewhere in the
repository and was missed here; or if I-02's Gray-to-Red criterion is judged
inapplicable to Nodes (as opposed to Book chapters) by a governance node this
audit did not find. Any of these should revise or retract Section 7's Red
assignment, not just soften its wording.
