---
node_id: "C-315"
canonical_name: "Wave Reader V1 (Hardware Specification)"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Engineering / Applied Hardware Node"
claim_gate_detail: "YELLOW (first attempt — no prior spec existed anywhere in the repo)"
metadata_standard: "I-06"
---

# Node C-315: Wave Reader V1 (Hardware Specification)

Grounding note: checked directly — no "Wave Reader" specification
exists anywhere in the real repo prior to this node. It is referenced
repeatedly across many Book 1 chapters (Ch4, Ch6, Ch10, Ch13, and
others) as FUTURE hardware ("measure lambda via Wave Reader"), but
never formally specified. This node is the first attempt, not a
formalization of something already established — treat it with the
same caution as any brand-new, unverified claim.

Dependencies:
Upstream: E-503 Pressure (Gradient Form), C-311 Electric-Magnetic Duality
Downstream: Future Android Build Book candidate hardware reference

Definition:
Proposed by an external formalization attempt ("V2"): a sensor that
treats signal and noise as field states rather than as separate
categories, using differential nulling between two mirrored,
out-of-phase emitters.

Hypothesis: if the field is continuous, "noise" is incoherent field
fluctuation, not a separate category from signal. Achieving a
near-perfect phase-null (high Common-Mode Rejection Ratio) would mean
observing the medium in its undisturbed state, not just filtering a
signal.

Proposed testable claim: a stable field source ("Logic Anchor" /
Persistent Mode, A-112) creates a non-linear "distortion tail" that
standard linear theory does not predict. Monitoring the null-point of
two mirrored emitters should show a residual scalar-potential
fluctuation correlating with nearby mass/charge, rather than a clean
zero.

Mathematics:
None derived. This is a hypothesis and a proposed experimental method,
not yet a specified circuit or a quantified prediction. No CMRR value,
no phase-resolution requirement, no specific circuit topology is
defined here — despite being mentioned in the originating proposal,
none of those numbers were actually given a derivation, only named as
required quantities.

Operational Chain:
Two mirrored emitters => Differential null-point => [Standard theory predicts zero] vs [This hypothesis predicts residual field] => Measurement

Yellow Audit:
- No prior grounding existed for this node originally (still true of
  the underlying hypothesis) — but a real circuit topology and
  derived CMRR/phase targets now exist (see Future Work below),
  resolving the "no design at all" gap specifically
- Circuit topology, CMRR target (~120 dB), and phase-resolution target
  (~0.08 degrees) are now specified with real derivations — RESOLVED,
  see Future Work
- The "distortion tail" claim has no connection yet to any of the
  real field equations (A-105, E-503, C-313's energy density) beyond
  general plausibility
- This node inherits C-313's unresolved Lorentz-invariance conflict —
  if the field has a preferred frame, that changes what a "null
  point" measurement would actually be looking for

Future Work:
Specify an actual circuit topology.
Derive a specific CMRR target and phase-resolution requirement rather
than naming them as needed without values.
Connect the "distortion tail" hypothesis to a specific term in E-518's
energy density, if possible, rather than leaving it as a general
plausibility claim.
This node should not be treated as validated hardware until an actual
build exists and the Candidate Experiment framing (same discipline as
I-02's Candidate Experiment) is run for real.

RESOLVED this turn — derived target values and a real topology:

Derived targets (worked calculation, not asserted): to resolve a
hypothetical residual signal at 1e-6 of the emitter amplitude (a
reasonable first target for a "distortion tail" search):
- CMRR needed: ~120 dB. This is demanding but real — high-end
  instrumentation amplifiers (e.g., precision INA-series parts) reach
  100-140 dB CMRR under good conditions. Not exotic, but not trivial.
- Phase-matching needed: better than ~0.08 degrees between the two
  emitters. This is the harder spec — achieving sub-0.1-degree phase
  lock between two independent emitters requires a shared phase
  reference (see topology below), not two free-running oscillators.

Proposed circuit topology (first draft, real, buildable):
1. Single master oscillator, phase-split into two paths via a
   precision 180-degree splitter (not two independent oscillators —
   this is what makes sub-0.1-degree matching achievable at all).
2. Two matched emitter drivers, each fed from one split path.
3. Two matched receive/sense elements, positioned symmetrically,
   feeding a precision differential instrumentation amplifier
   (target CMRR ~120 dB, per above).
4. Amplifier output digitized via a high-resolution ADC (24-bit class,
   to have enough dynamic range below the null point to see the
   target residual).
5. Digital lock-in / synchronous detection referenced to the master
   oscillator, to reject noise outside the expected signal band and
   improve effective sensitivity beyond the raw CMRR figure.

This is a real, standard differential-null measurement architecture
(the same basic approach used in precision null-detection instruments
generally) — nothing about it requires inventing new electronics, only
building a genuinely precise, well-matched version of a known
architecture and pointing it at the specific hypothesis in this node's
Definition section.

Still open: whether a residual at the 1e-6 level (or any level) would
actually appear is the experiment itself, not something this topology
can presuppose. This resolves HOW to look, not WHAT will be found.

---
