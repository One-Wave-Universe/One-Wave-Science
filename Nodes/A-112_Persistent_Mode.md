---
node_id: "A-112"
canonical_name: "Persistent Mode"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Foundation Primitive / Extension"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node A-112: Persistent Mode

Dependencies:
Upstream: A-111
Downstream: A-112a Traveling Lattice Rupture; all object nodes in Books
1-6. Bridge node between foundation language and applied objects.
CORRECTION (verified against the actual Books/ directory): only Book1
(17 chapters), Book2 (1 chapter), and Book5 (5 chapters) currently have
real chapter content. Book3_Medium and Book4_Large exist only as
`00_Scope_and_Status` stub files with zero chapters, and there is no
Book6 directory at all. "All object nodes in Books 1-6" overstates
current coverage; the accurate statement is Books 1, 2, and 5, with 3
and 4 scoped-but-unwritten and 6 not yet started.

Definition:
A Persistent Mode is a recursively stable non-ground-state pattern.
A Persistent Mode is not a particle. It is the field doing something stable.

psi_M != psi_0
Stable Recursion => Persistent Mode

REFINEMENT (checked against A-101 and E-525, genuinely resolves an
earlier tension rather than repeating it): decompose the field as
psi(x,t) = psi_0(x,t) + delta_psi(x,t), where psi_0 is the background/
reference state (matching A-101's real definition: "Ground/Zero is
the reference state required for measurement") and delta_psi is the
excitation — the Persistent Mode itself.

This is NOT the same claim as "particles are measurements," which was
checked and rejected: that claim collapsed the excitation and its
measurement into one thing, contradicting Ch9/E-525's real "no
feedback into psi" principle. This refinement keeps them distinct:
delta_psi is real and evolves under its own recursive dynamics
(the operational stability criterion below), independent of whether
anything measures it. A measurement samples it:
M(t) = integral W(x) * delta_psi(x,t) dx
(directly using E-525's real operator, applied to the excitation
component specifically). The excitation is not "created" by, or
identical to, its measurement — M(t) is a real sampling of a real,
independently-persisting delta_psi.

PRECISION NOTE (checked against E-525's actual text): E-525 defines its
operator over the FULL field, R(t) = integral W(x)*psi(x,t) dx, not
over delta_psi. Since psi = psi_0 + delta_psi, substituting gives
R(t) = integral W(x)*psi_0(x,t) dx + M(t) -- so M(t) equals E-525's R(t)
only if the background term integral W(x)*psi_0 dx vanishes or is
separately subtracted (e.g. by calibrating the detector against Ground
before the excitation arrives). Neither this node nor E-525 states that
assumption. Calling M(t) a direct use of "E-525's real operator" is
therefore imprecise: it is a background-subtracted adaptation of it,
requiring one additional, currently unstated step, not a plain
substitution.

A Persistent Mode is a repeatable excitation pattern that must keep
re-satisfying its own stability criterion. Persistence describes the
recurrence of the structure. It does not, by itself, define inertia or
the Mass Effect; that response belongs to the complete four-interaction
architecture in C-318.

Mathematics:
Operational Stability Criterion (testable now):
||psi_{n+k} - psi_n|| < epsilon

Future Analytical Criterion (deferred, distinct from operational test):
lambda_max < 0
Deferred until recursive dynamics are fully derived.

Four Measurable Quantities Requiring Definition:
1. Stability: operational criterion testable now; analytical criterion deferred
2. Mode type: periodic, quasiperiodic, stationary, localized, traveling, topological — not yet classified
3. Persistence timescale: not yet defined
4. Failure modes: instability, damping, mode coupling, flowback, surface tension, resistance, electrical locking — conditions not yet specified

Every object in Books 1-6 is a Persistent Mode or a collection of interacting Persistent Modes.


Scale-Specific Yellow Child:
- A-112a formalizes one traveling, localized defect as a conservative relocation model.
- It does not promote all proposed object interpretations; it supplies a testable
  mathematical instance of the `traveling` Persistent Mode category.

Operational Chain:
Stable Recursion => Persistent Mode => Excitation => Objects (Books)

Yellow Audit:
- Mode type not yet classified
- Persistence timescale not specified
- Failure conditions not yet formalized
- Bridge to books: all downstream objects depend on this node being resolved
- "Books 1-6" overstated actual coverage (corrected above to 1, 2, 5;
  3/4 are scope-only stubs, 6 does not exist)
- M(t)'s claimed direct use of E-525's operator requires an unstated
  background-subtraction assumption (corrected above); the background
  term's vanishing/subtraction is not derived or justified anywhere yet

Future Work:
Construct recursive update rule. Seed initial mode. Iterate over increasing time.
Measure ||psi_{n+k} - psi_n||. Apply perturbations.
Determine which interaction changes preserve or destroy the mode.
