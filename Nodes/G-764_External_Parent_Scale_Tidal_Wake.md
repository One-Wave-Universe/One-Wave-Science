---
node_id: "G-764"
canonical_name: "External Parent-Scale Tidal Wake"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Gravity / Orbital / Nested-Wake Program"
claim_gate_detail: "YELLOW (functional form fixed; no calibrated parent tensor, no falsification test yet)"
metadata_standard: "I-06"
---

# Node G-764: External Parent-Scale Tidal Wake

**Dependencies**
Upstream: `UPDATED_38_FINITE_WAKE_THREE_BODY_PERTURBATION_ARCHITECTURE.md` (its "local wake -> assimilation boundary -> parent reference field" rule), `ONE_WAVE_SCIENCE_ATTACK_MAP.md` section K (Gravity/orbital/nested-wake) and section M (Scale recursion), D-415.
Downstream: `Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/solar_system_control.py` (`external_parent_tidal_acceleration`, the `external_parent_wake` channel in `acceleration_receipt`/`step`), `hybrid_one_wave.py` (this channel is deliberately excluded from `close_internal_channel`).

## Core claim

Structures at each gravitationally nested scale (Great Attractor -> cluster -> galaxy -> star system) impose a curvature/tidal contribution on the scale directly below, treated as a one-way (parent -> child) external field.

This is not a claim that gravity is ever actually one-directional -- Newton's third law (mutual gravitation) holds at every scale, and `solar_system_control.py` already models the Sun/planets/Moon system with full mutual N-body gravity precisely because their mutual backreaction is not negligible. One-way is stated here as a justified *approximation*, valid specifically where the child's mass is negligible relative to the parent's (a star system's gravitational backreaction on its host galaxy is real but has never been measured), the same approximation already implicit in treating the Sun's field as fixed while integrating planetary orbits at even smaller scale.

This node is UPDATED_38's existing finite-wake/assimilation idea, applied one level further out (galaxy-on-solar-system, rather than planet-on-planet), formalized as its own explicit, separately auditable acceleration channel.

## Current mathematics (functional form only)

For a body at position \(r\) relative to a declared center,

\[
a_{\rm parent}(r) = T\,(r - r_{\rm center})
\]

where \(T\) is a general \(3\times3\) linear tidal tensor. This is the standard leading-order (linear/quadrupole) form for an external field sourced by a much larger, unmodeled mass distribution -- the same functional shape used in the real, established galactic-tide literature (Oort–Uraltsev / Heisler & Tremaine) for the Milky Way's effect on the Oort cloud. \(T\) is **not** calibrated to that or any other real parent mass distribution here; only the functional form is fixed.

Implemented in `solar_system_control.external_parent_tidal_acceleration`, defaulting to the zero tensor, so it changes nothing until a specific \(T\) is derived and declared.

## Why this channel is kept separate from the internal candidate law

`hybrid_one_wave.close_internal_channel` explicitly removes net translation and net rotation from any internal-exchange candidate (`one_wave_candidate`), because an internal redistribution among modeled bodies cannot create system momentum or angular momentum from nothing -- its own docstring already states this and requires external forcing to be "a separate boundary channel." This node's channel is exactly that separate boundary channel: an external field's source is not part of the simulated system, so it is allowed to add real net momentum to the modeled system (ordinary \(F=ma\) from an outside force). Routing it through `close_internal_channel` would have been a modeling error, not a stricter check.

## Yellow Audit

- \(T\) is not derived or calibrated from any specific parent mass distribution (Milky Way, Local Group, or otherwise); only its functional form is fixed.
- No falsification test yet exists: no prediction has been made that would distinguish \(T=0\) (the current default) from some specific nonzero \(T\) against held-out orbital- or Oort-cloud-scale data.
- The "one-way is valid because the mass ratio is extreme" justification is stated but not quantified, contrary to Attack Map section K's own requirement to "build Newtonian baseline first, add one candidate term at a time" with an explicit ablation.
- Not yet connected to G-745/C-309's friction-limit/propagation-ceiling discussion. If this parent wake is meant to arise from the same underlying lattice medium as C-309/A-114, that connection is currently undeclared.

## Falsification condition

This channel fails if either:

1. a nonzero \(T\) required to match any real solar-system- or Oort-cloud-scale residual cannot be reconciled with the real, independently known mass and position of any candidate parent structure -- i.e. \(T\) would have to be fit to the residual rather than derived from an independently measured mass distribution; or
2. the same one-way approximation, applied at a scale where the mass ratio is *not* extreme (contradicting its own stated justification), is shown to distort the mutual N-body dynamics already validated by `solar_system_control.py`'s Gray control.

## What does NOT change

This node does not modify the existing mutual N-body Gray control (Sun/planets/Moon) in any way -- that remains full pairwise gravity, unaffected by this channel's default zero tensor. It only formalizes a fourth, separately declared, currently inert channel and gives it a Node so it does not remain undocumented code.

Responsible: Claude (session), 2026-09-12, branch `claude/nice-gauss-sonp6s`.
