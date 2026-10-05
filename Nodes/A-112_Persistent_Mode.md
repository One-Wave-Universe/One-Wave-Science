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
Downstream: A-112a Traveling Lattice Rupture; all object nodes in Books 1-6. Bridge node between foundation language and applied objects.

Definition:
A Persistent Mode is a recursively stable non-ground-state pattern.
A Persistent Mode is the field doing something stable. In One-Wave particle language, measurements identify and classify these field excitations; a separate bead-like object is not inserted into the model.

psi_M != psi_0
Stable Recursion => Persistent Mode

REFINEMENT (checked against A-101 and E-525, genuinely resolves an
earlier tension rather than repeating it): decompose the field as
psi(x,t) = psi_0(x,t) + delta_psi(x,t), where psi_0 is the background/
reference state (matching A-101's real definition: "Ground/Zero is
the reference state required for measurement") and delta_psi is the
excitation — the Persistent Mode itself.

Particle language here means measured signatures and classifications of
field excitations. It includes both the excitation and its measured response,
without making a detector output identical to the full evolving field.
delta_psi evolves under the declared dynamics; a measurement samples it:
M(t) = integral W(x) * delta_psi(x,t) dx
using E-525's sampling operator. The same excitation can produce different
outputs under different detector windows. This operational distinction does
not reject the One-Wave interpretation that particles are measured excitations.
A passive sampler does not create the excitation; a physical coupled detector
requires its own interaction and energy accounting.

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

Future Work:
Construct recursive update rule. Seed initial mode. Iterate over increasing time.
Measure ||psi_{n+k} - psi_n||. Apply perturbations.
Determine which interaction changes preserve or destroy the mode.

## Phase 6B Validation (2026-10-03)

Persistent mode behavior validated on 2D hexagonal lattice:
- Vector field formulation (ψ = (ψ_x, ψ_y)) supports persistent oscillating modes
- Modes persist over 30+ time steps with frequency stability
- Faraday constraint satisfied exactly in continuum limit (error → 0 as domain grows)
- Unified mode interpretation shows E and B are projections of single persistent ψ field
- See: discrete_maxwell_solver_v4.py, faraday_scaling_test.py

## Runnable bulk excitation and measurement experiment (2026-10-04)

The [bulk experiment](../solvers/BULK_EXCITATION_DERIVATION.md) now constructs and evolves a localized excitation on native periodic FCC12 geometry, without an enclosing reflecting wall. Its nonlinear constitutive closure is explicitly hypothetical and separate from the canonical second-order recurrence. At fixed input norm 20, the candidate retains about 98% within radius 2 for 100 model-time units, including finite perturbations; the linear control spreads. Fixed detector windows sample coherent amplitude and intensity from that same state. Ten bulk tests and fifteen existing solver tests pass.

This verifies finite candidate behavior, not a physical particle spectrum. Removing cross/phase coupling still allows single-coordinate localization, so the full four-interaction necessity is not established. Spacing refinement changes energy about 15%; continuum stability, vortex topology, norm selection, real detector coupling and Mass Effect remain open. Full traces, controls and failures are in [the run report](../solvers/bulk_excitation_results.json).
