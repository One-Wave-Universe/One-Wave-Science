---
node_id: "D-401"
canonical_name: "Flux"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW (partially derived — steady-state harmonic condition confirmed; exponential functional form remains a gap, not a sketch)"
metadata_standard: "I-06"
---

# Node D-401: Flux

Dependencies:
Upstream: A-112 Persistent Mode
Downstream: D-402 Resonant Mode

Definition:
A persistent mode creates a surrounding field.
Flux is the statement that this field threads space and couples to other modes.

Flux = field of a persistent mode threading space and coupling outward

Mathematics (partially derived — real progress from A-109's actual update rule):

Steady-state condition, derived: A-112 Persistent Mode's stability
criterion (‖ψ_{n+k} - ψ_n‖ < ε) means ψᵢⁿ⁺¹ ≈ ψᵢⁿ ≈ ψᵢⁿ⁻¹ at a
persistent mode. Substituting into A-109's real update rule
(ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + βᵢ(⟨ψⱼⁿ⟩-ψᵢⁿ)):

ψᵢ = ψᵢ + (1-γ)(ψᵢ-ψᵢ) + βᵢ(⟨ψⱼ⟩-ψᵢ)
0 = βᵢ(⟨ψⱼ⟩-ψᵢ)

For βᵢ ≠ 0, this requires ⟨ψⱼ⟩ = ψᵢ: a persistent mode satisfies a
discrete harmonic (mean-value) condition. This IS rigorously derived
from real upstream equations, not sketched.

GAP FOUND (new — the original sketch did not derive this and the gap
was not previously flagged): the harmonic condition above does NOT by
itself produce the exponential form Phi(x) ~ A*exp(-|x-x_0|/lambda)
originally sketched. A pure discrete harmonic condition satisfies a
maximum principle; away from a source, a bounded harmonic function on
an infinite lattice tends toward constant, not exponential decay.
Getting the sketched exponential profile requires an additional
"mass" or screening term — most plausibly the residual of the memory
term (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) not being exactly zero, which was assumed away
above. This residual has not been derived or bounded. Until it is,
the exponential form remains an assumption, and the derivation above
only establishes the weaker harmonic condition, not the full sketch.

This is a sketch. The functional form of Phi and the coupling mechanism
are not derived here.

Operational Chain:
Persistent Mode => Flux => Coupling to other modes

Yellow Audit:
- Steady-state harmonic condition (⟨ψⱼ⟩ = ψᵢ) is now rigorously derived
  from A-109's real update rule and A-112's stability criterion — this
  is genuine progress, not sketch
- The exponential functional form Phi(x) ~ exp(-|x-x_0|/lambda) is NOT
  derived from the harmonic condition alone — a real gap, newly found,
  requiring a mass/screening term (candidate source: the residual
  memory term, not yet bounded)
- Coupling length lambda not specified even if the exponential form
  is eventually justified
- Whether flux is conservative, dissipative, or mixed not established
- No longer purely "bookkeeping item, does not block chapter" — the
  harmonic-vs-exponential gap is a real open mathematical question,
  though still not urgent

Future Work:
Bound the residual memory term (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) near a persistent mode
to determine whether it can supply the missing mass/screening term.
Measure coupling length lambda via Wave Reader, once the functional
form question above is resolved (measuring lambda for an unjustified
functional form risks fitting noise to the wrong equation).
Determine whether flux form matches known field profiles.
