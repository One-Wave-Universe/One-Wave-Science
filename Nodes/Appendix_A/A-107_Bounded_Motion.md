---
node_id: "A-107"
canonical_name: "BOUNDED MOTION"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Motion Constraint Primitive"
claim_gate_detail: "YELLOW (stability criterion corrected — previous version was insufficient in 3D)"
metadata_standard: "I-06"
---

# Node A-107: BOUNDED MOTION

LAYER: Motion Layer

DEPENDENCIES:
	UPSTREAM: A-105 Restoring Response, A-106 Pressure Response
	DOWNSTREAM: A-110 Oscillation

1. PURPOSE
	FUNCTION:
		Converts pressure response into a motion constraint.

	INPUT:
		A-106 Pressure Response output — now actually used (see §4), not just cited
		as a dependency.

	OUTPUT:
		Bounded Motion condition, with a criterion that is now sufficient, not just
		necessary.

	ROLE:
		Defines whether motion remains confined within an allowed equilibrium boundary.

2. DEFINITION
	CORRECTION (this fix): the previous version of this node listed A-106 as an
	upstream dependency but its Mathematics section never used A-106's output —
	only A-105's V(x)=∫A(s)ds appeared. This was a real gap: the stated bound
	condition, V(x)→∞ as |x|→∞, is a known-insufficient criterion in 3D (Derrick's
	theorem — see A-106 for full derivation). A gradient-plus-potential functional
	with no curvature term generically has no genuine energy minimum under uniform
	rescaling; it collapses or disperses. This node's own dependency list already
	pointed at the fix; it just wasn't wired in.

	Bounded Motion is motion that remains within an allowed equilibrium boundary,
	where "allowed" is now defined by the FULL energy functional, including A-106's
	curvature term, not the potential alone.

	A-105 establishes:
		R_OW = -A(∇ψ)

	A-106 establishes:
		P_OW = (b/2)(∇²ψ)², combined with A-105's term in one functional.

	A-107 defines:
		The actual stability condition on that combined functional.

3. STATE VARIABLES
	x = Displacement.
	A(x) = Response operator (A-105).
	V(x) = Potential function, V(x) = ∫A(s)ds.
	b = Curvature coupling coefficient (A-106).
	I₁ = ∫ (a/2)(∇ψ)² d³x — gradient energy of a candidate solution.
	I₂ = ∫ V(Δψ) d³x — potential energy of the same solution.
	I₃ = ∫ (b/2)(∇²ψ)² d³x — curvature energy of the same solution.
	E_mode = Motion energy.
	E_escape = Escape threshold.

4. MATHEMATICS
	OLD CRITERION (kept for reference, now marked explicitly insufficient):
		V(x)→∞ as |x|→∞ → bounded motion. [NECESSARY, NOT SUFFICIENT — see below]

	FULL ENERGY FUNCTIONAL (from A-106):
		E[ψ] = ∫ [ (a/2)(∇ψ)² + V(Δψ) + (b/2)(∇²ψ)² ] d³x

	RESCALING TEST (the actual bounded-motion criterion):
	For a candidate solution ψ_λ(x) = ψ(λx), the energy scales as:
		E(λ) = I₁λ⁻¹ + I₂λ⁻³ + I₃λ

	STATIONARITY (dE/dλ = 0 at λ=1):
		I₃ = I₁ + 3I₂

	STABILITY (d²E/dλ² > 0 at λ=1) — derived correctly, replacing an earlier
	miscalculation that had an extra term:
		E'(λ) = -I₁λ⁻² - 3I₂λ⁻⁴ + I₃
		E''(λ) = 2I₁λ⁻³ + 12I₂λ⁻⁵     [note: the I₃λ term is linear, so it
		                                contributes ZERO to E'' — this is the
		                                correction]
		E''(1) = 2I₁ + 12I₂

	Substituting the stationarity condition (I₂ = (I₃−I₁)/3):
		E''(1) = 2I₁ + 4(I₃−I₁) = 4I₃ − 2I₁

	CORRECTED BOUNDED-MOTION CRITERION:
		Bounded Motion = TRUE  ⟺  4I₃ − 2I₁ > 0  ⟺  I₃ > I₁/2

	i.e. the curvature energy of the candidate solution must exceed half its
	gradient energy. This is a real, checkable condition on b (via I₃'s dependence
	on b) for any specific trial profile — not merely "V(x)→∞," which by itself
	guarantees nothing about λ-stability.

	SPECIAL CASE (no potential, V=0 — the pure gradient+curvature competition):
		E(λ) = I₁λ⁻¹ + I₃λ
		This has a genuine global minimum at λ* = √(I₁/I₃) for ANY I₁, I₃ > 0 —
		i.e. the curvature term alone, with no potential at all, is already
		sufficient to produce a stable bounded state. The potential (A-105's V)
		is not required for boundedness once A-106's curvature term is included;
		it may still matter for other properties (depth of the well, multiple
		equilibria), but boundedness itself does not depend on it.

	ENERGY CONDITION (unchanged, still applies once boundedness is established):
		E_mode < E_escape → bounded motion holds even under perturbation.

5. RELATIONSHIP
	CHAIN:
		A-104 Gradient
		→ A-105 Restoring Response
		→ A-106 Pressure Response
		→ A-107 Bounded Motion
		→ A-110 Oscillation

	ROLE:
		A-105 supplies the gradient (collapse-favoring) term.
		A-106 supplies the curvature (dispersal-favoring) term — this is now
		understood as the actual stabilizing mechanism, not a side detail.
		A-107 states the real condition under which the two balance.

	BOUNDARY:
		Does not define Oscillation.

6. OPERATIONAL RULE
	CORRECTED:
		I₃ > I₁/2 → Bounded Motion = TRUE.
		I₃ ≤ I₁/2 → Bounded Motion = FALSE (gradient term dominates; configuration
		disperses under rescaling regardless of what V(x) does at large |x|).

7. RECURSIVE POSITION
	FUNCTION:
		Converts the combined gradient+curvature+potential functional into an
		actual go/no-go stability test.

	BOUNDARY:
		Does not define oscillatory behavior.

8. RECURSIVE SCALING
	REQUIREMENT:
		Preserve bounded behavior across Micro, Small, Medium, Large, Macro.

	OPEN (unchanged):
		Whether I₃ > I₁/2 remains satisfiable at all scales, or whether b's scale
		dependence (still open in A-106) could break this at some scale.

9. CONSTRAINTS
	Bounded Motion requires:
		1. A-106's curvature term to be active (b > 0) — without it, this node's
		   criterion reduces to "always false" per Derrick's theorem.
		2. I₃ > I₁/2 for the specific candidate solution under test.
		3. E_escape threshold defined for the perturbation-stability question,
		   which is separate from the rescaling-stability question above.

	OPEN:
		Escape threshold derivation (unchanged).
		Whether I₃ > I₁/2 can be satisfied for realistic b, or whether it forces
		an unphysically large b — not yet checked against any specific profile.

10. DEPENDENCIES
	UPSTREAM:
		A-105 Restoring Response.
		A-106 Pressure Response — now actually load-bearing, not just listed.

	INPUT:
		I₁, I₂, I₃ computed from a specific trial solution.

	DOWNSTREAM:
		A-110 Oscillation.

11. FAILURE MODES
	Bounded Motion fails when:
		1. b ≤ 0, or I₃ ≤ I₁/2 — genuine dispersal/collapse under rescaling,
		   regardless of V(x)'s large-|x| behavior. [NEW — this failure mode
		   did not exist in the previous version, which had no way to detect it.]
		2. Escape threshold is undefined (unchanged).
		3. Bounded Motion is confused with Oscillation (unchanged).
		4. I₁, I₂, I₃ are computed for the wrong candidate profile (e.g. using a
		   plain Gaussian without checking whether it's actually a solution of the
		   full field equation, not just a convenient trial function).

12. ADVANCEMENT CRITERIA
	ADVANCE WHEN:
		1. Pressure-to-motion relationship is defined. ✅ (this fix — via I₃ > I₁/2)
		2. Escape threshold is derived. ❌ (still open)
		3. A specific candidate profile is checked against I₃ > I₁/2 explicitly.
		   ❌ (open — this needs an actual solved trial function, not just the
		   general criterion)
		4. Oscillation boundary is validated. ❌ (still open, downstream)
		5. Recursive scaling is consistent. ❌ (still open)

	CURRENT:
		Definition ✅
		Dependency Mapping ✅
		Pressure Link ✅ (was ❌ in effect — dependency was listed but unused;
		    now actually wired into the criterion)
		Motion Constraint ✅ (corrected — was previously an insufficient criterion)
		Escape Threshold ❌
		Specific-profile validation ❌
		Experimental Validation ❌

	GATE:
		GREEN = Defined.
		YELLOW = Constrained/Testable.
		BRONZE = Validated.
		SILVER = Integrated.
		GOLD = Confirmed.

13. FINAL DEFINITION / CLOSURE
	NODE:
		A-107 Bounded Motion

	DEFINITION:
		Bounded Motion is the condition where the combined gradient+curvature+
		potential energy functional has a genuine, non-degenerate minimum under
		spatial rescaling — concretely, I₃ > I₁/2 for the candidate solution.

	FUNCTION:
		Converts A-106's pressure/curvature term, together with A-105's gradient
		term, into an actual sufficient stability test — replacing a criterion
		(V(x)→∞) that was necessary but not sufficient in 3D.

	BOUNDARY:
		Defines confinement, not Oscillation. Does not yet check any specific
		trial solution against the criterion — that's the next concrete step,
		not this node's job.

	STATUS:
		YELLOW.
