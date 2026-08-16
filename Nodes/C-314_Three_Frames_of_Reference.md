---
node_id: "C-314"
canonical_name: "Three Frames of Reference"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Application / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node C-314: Three Frames of Reference

Gap-filling note: this fills a gap explicitly flagged (not built) in
the I-01 H/I/J/K/L resolution addendum — "J-106 Reference Frames...
relates to A-101 Ground/Zero but as a distinct relativistic-frames
treatment, not currently covered." Placed in C-series rather than
inventing a new letter, consistent with I-01 Rule 3.

Dependencies:
Upstream: A-101 Ground / Zero (related but distinct — see below), C-313 Lorentz Invariance Conflict (this node inherits that unresolved tension)
Downstream: none yet (proposed)

Definition:
Three distinct, overlapping coordinate systems, proposed by an
external formalization attempt ("V2"):

1. Medium Frame — the local frame where the surrounding field
   gradient is zero (nabla_Phi = 0). Related to A-101's Ground/Zero
   (psi = psi_0) but NOT identical: A-101's ground condition is about
   a single reference VALUE, while this frame is about a spatial
   region of zero GRADIENT — the same distinction already drawn
   between A-101 and A-105's equilibrium condition (checked earlier
   this session, in the HOLD/BEGIN resolution). Do not merge these
   without the same rigor applied there.

2. Anchor Frame — the comoving rest frame of a stable localized
   structure (a "Logic Anchor" / Persistent Mode, A-112). The frame
   in which the structure's own internal oscillation is purely
   radial.

3. Wave-Signal Frame — the frame propagating at the local phase
   velocity of the field's internal disturbances. Governs
   non-local correlation and interaction transmission.

Mathematics:
No independent mathematics beyond the definitions above. This is a
structural/conceptual framework, not yet formalized into equations
relating the three frames to each other.

Inherited conflict (from C-313): this node's entire framing assumes
frames related by Lorentz-style covariance are meaningful in the way
V2 intends. If C-313's conflict resolves in favor of a real preferred
lattice frame (Rule (c) in C-313's Future Work), these three frames
would need reinterpreting as approximate/emergent coordinate choices
relative to that preferred frame, not as fully equivalent relativistic
frames.

Yellow Audit:
- Medium Frame vs. A-101 Ground/Zero needs the same explicit
  disambiguation rigor already applied to HOLD/BEGIN — flagged, not
  yet done with full rigor here, only noted as likely distinct
- No mathematics connects the three frames to each other yet
- Fully inherits C-313's unresolved Lorentz-invariance conflict —
  this node's usefulness depends on how that resolves

Future Work:
Formally disambiguate Medium Frame from A-101, the same rigor as the
Void=Ground/Zero and Resistance-vs-A-108 checks earlier this session.
Resolve pending C-313 before treating these three frames as more than
a structural proposal.

---

## Addendum: leading-order math connecting Medium Frame and Anchor Frame

This closes the item above ("no mathematics connects the three frames
to each other yet") for the Medium Frame / Anchor Frame pair
specifically. The Wave-Signal Frame is not addressed here and remains
open.

**Why this matters, concretely:** E-525's measurement addendum (counting
peaks/troughs, or a local finite-difference stencil, to extract omega
and k from field samples) implicitly assumed the sampling apparatus
itself sits still in the Medium Frame. No real Focal Point does — a
Wave Reader (C-315), an orbiting body, or any detector is itself a
bounded structure (A-112 Persistent Mode) with its own Anchor-Frame
motion through the same field the wave is a disturbance of. What such
a device actually measures is contaminated by its own velocity, and
that contamination has a name: Doppler shift.

**Scope of what follows, stated up front:** C-313 leaves this
framework's frame-transformation behavior formally unresolved — no
exact Lorentz covariance is established, and none is assumed here.
What is derived below is the leading-order, non-relativistic (Galilean)
transform between Medium Frame and Anchor Frame, valid to first order
in u/v_phase where u is the detector's own Medium-Frame speed along the
propagation direction. This is not a resolution of C-313; it is the
correct level of rigor to use while C-313 stays open, and — per the
point that prompted this addendum — it is also the physically relevant
level: C-309 sets the propagation ceiling c_lat at or near the speed a
disturbance can move at, and no Persistent Mode this framework
considers (a planet, a spacecraft, a Wave Reader) moves anywhere near
that ceiling. u/v_phase << 1 holds generically for every real detector,
so the second-order (relativistic-scale) corrections this derivation
drops are safely negligible for anything this framework would actually
build or observe with — not merely a convenient simplification.

### Derivation

Medium Frame: a plane wave `psi(x,t) = A*cos(k*x - omega*t + phi)`,
phase velocity `v_phase = omega/k`.

Anchor Frame: a detector holding its own local coordinate fixed while
moving through the Medium Frame at velocity `u` (component along the
propagation direction), i.e. its Medium-Frame trajectory is
`x_A(t) = x_A0 + u*t`. Substituting into the field:

```
psi(x_A(t), t) = A*cos(k*x_A0 + (k*u - omega)*t + phi)
```

The rate of phase change the detector's own clock actually measures —
exactly what E-525's counting method and finite-difference stencil
extract — defines the Anchor-Frame angular frequency:

```
omega' = omega - k*u = omega*(1 - u/v_phase)          (Doppler-omega)
```

For a genuinely simultaneous (same Medium-Frame instant) multi-point
spatial snapshot, Galilean simultaneity is frame-independent, so the
counted wavenumber is unchanged:

```
k' = k
```

(This is a separate claim from the possibly relativistic case C-313
leaves open; if C-313 later resolves toward exact Lorentz covariance
rather than a true preferred frame, this k'=k result would need
revisiting along with everything else in this node.)

Combining, the Anchor-Frame apparent phase velocity is

```
v_phase' = omega'/k' = v_phase - u          (Doppler-v)
```

**Sanity check:** a detector co-moving exactly at the wave's own phase
velocity (`u = v_phase`) measures `omega' = 0` and `v_phase' = 0` — a
frozen pattern, the correct textbook limit (a surfer sitting on a wave
crest sees no oscillation). A detector moving against propagation
measures a higher `omega'` (blueshift); moving with it, a lower one
(redshift) — ordinary Doppler behavior, not new physics.

### Practical consequence

To recover the Medium-Frame `omega, k, v_phase` from a real (moving)
measurement, the detector's own velocity `u` relative to Ground/Zero
(A-101) must be independently known:

```
omega = omega' + k*u,      v_phase = v_phase' + u
```

To leading order in `u/v_phase` (justified above), this is a small,
computable correction, not a fundamental obstruction — but it is a
correction E-525's addendum did not previously carry, and any reading
from a moving Wave Reader (C-315) or from a body's own local field
sample (as used throughout Updated 38-41's `S_local,i(t)`, if that
quantity is ever read as an oscillating rather than quasi-static field)
needs `u` subtracted out before it can be compared against A-114's
Medium-Frame dispersion prediction.

Yellow Audit (addendum-specific):
- Wave-Signal Frame (the third of the three) is not connected to
  either Medium or Anchor Frame here — open.
- This is a Galilean, first-order-in-u/v_phase treatment only; it
  explicitly does not resolve C-313's exact frame-transformation
  question, only supplies the leading-order correction needed for any
  real, non-relativistic measurement device.
- The `k'=k` simultaneity claim assumes a genuinely simultaneous
  Medium-Frame spatial snapshot; a single moving detector building a
  "spatial snapshot" out of sequential position samples over time
  would need a separate, not-yet-derived correction.
- NOT a time-dilation mechanism: `omega' = omega(1-u/v_phase)` is a
  propagation-delay Doppler shift (asymmetric, first-order in u), not
  a change in any internal process's own rate. Book 1 Ch10 explicitly
  flags the risk of conflating this with the still-undissolved
  clock-rate-slowing question — see that chapter's "Motion and
  Gravitational Clock Rates" section for the distinction.

---
