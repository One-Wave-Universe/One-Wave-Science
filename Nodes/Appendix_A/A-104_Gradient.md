---
node_id: "A-104"
canonical_name: "GRADIENT"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Spatial Organization Primitive"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node A-104: GRADIENT

LAYER: A-Series Core

DEPENDENCIES:
	UPSTREAM: A-103 Differential
	DOWNSTREAM: A-105 Restoring Response

1. PURPOSE
	Converts spatial Differential relationships into directional field structure.
	INPUT:
		Spatial differential between neighboring field states.
	OUTPUT:
		∇ψ
	FUNCTION:
		Defines how field difference changes across space.

2. DEFINITION
	A-103 Differential defines the relationship between defined states.
	A-104 applies Differential across spatial relationships.

	SPATIAL DIFFERENTIAL:
		Δψᵢⱼ = ψⱼ − ψᵢ

	WHERE:
		ψᵢ = Field state at site i.
		ψⱼ = Field state at neighboring site j.

	Gradient converts local field differences into directional spatial change.

3. STATE VARIABLES
	ψ = Field state.
	i = Current lattice site.
	j = Neighboring lattice site.
	N(i) = Neighbor set associated with site i.
	rᵢ = Position of site i.
	rⱼ = Position of site j.
	aᵢⱼ = Distance between sites.
	eᵢⱼ = Unit direction from i to j.
	∇ψ = Gradient.

4. MATHEMATICS
	POSITION DIFFERENCE:
		dᵢⱼ = rⱼ − rᵢ

	DISTANCE:
		aᵢⱼ = |rⱼ − rᵢ|

	DIRECTION:
		eᵢⱼ = (rⱼ − rᵢ)/|rⱼ − rᵢ|

	SPATIAL DIFFERENTIAL:
		Δψᵢⱼ = ψⱼ − ψᵢ

	DISCRETE GRADIENT:
		∇ψᵢ ≈ Σⱼ∈N(i) (Δψᵢⱼ/aᵢⱼ)eᵢⱼ

	CONTINUOUS LIMIT:
		∇ψ = (∂ψ/∂x, ∂ψ/∂y, ∂ψ/∂z)

	UNIFORM FIELD:
		ψᵢ = ψⱼ → ∇ψ = 0

	NON-UNIFORM FIELD:
		ψᵢ ≠ ψⱼ → ∇ψ ≠ 0

5. RELATIONSHIP
	CHAIN:
		A-101 Ground / Zero
		→ A-102 Displacement
		→ A-103 Differential
		→ A-104 Gradient
		→ A-105 Restoring Response

	ROLE:
		A-103 identifies difference.
		A-104 organizes difference across spatial structure.
		A-105 responds to gradient structure.

	BOUNDARY:
		Gradient does not define restoring behavior.

6. OPERATIONAL RULE
	NO SPATIAL DIFFERENCE:
		ψᵢ = ψⱼ → ∇ψ = 0

	SPATIAL DIFFERENCE:
		ψᵢ ≠ ψⱼ → ∇ψ ≠ 0

	Gradient is the directional measurement of spatial change.

7. RECURSIVE POSITION
	FUNCTION:
		Converts local field relationships into spatial organization.

	BOUNDARY:
		Response behavior belongs downstream.

8. RECURSIVE SCALING
	REQUIREMENT:
		Preserve gradient meaning across:
		Micro, Small, Medium, Large, Macro.

	OPEN:
		Verify gradient behavior remains consistent across recursive scales.

9. CONSTRAINTS
	Gradient requires:
		1. Defined spatial relationship.
		2. Stable neighbor mapping.
		3. Valid directional representation.
		4. Consistent geometry.

	OPEN:
		Geometry weighting.
		Higher-dimensional representation.
		Scale behavior.

10. DEPENDENCIES
	UPSTREAM:
		A-103 Differential.

	INPUT:
		Δψᵢⱼ = ψⱼ − ψᵢ

	DOWNSTREAM:
		A-105 Restoring Response.

11. FAILURE MODES
	Gradient fails when:
		1. Neighbor relationship is undefined.
		2. Direction cannot be assigned.
		3. Geometry changes invalidate comparison.
		4. Gradient is confused with curvature.
		5. Recursive scaling loses spatial meaning.

12. ADVANCEMENT CRITERIA
	ADVANCE WHEN:
		1. Discrete gradient calculation is verified.
		2. Geometry dependence is bounded.
		3. Direction representation is validated.
		4. Gradient remains separate from curvature and response.
		5. Recursive scale behavior is tested.

	CURRENT:
		Definition ✅
		Mathematics ✅
		Differential relationship ✅
		Spatial operator defined ✅
		Geometry validation ❌
		Recursive validation ❌
		Experimental validation ❌

	GATE:
		GREEN = Defined.
		YELLOW = Constrained/Testable.
		BRONZE = Validated.
		SILVER = Integrated.
		GOLD = Confirmed.

13. FINAL DEFINITION / CLOSURE
	NODE:
		A-104 Gradient

	DEFINITION:
		Gradient is the spatial expression of Differential.

	EQUATION:
		Δψᵢⱼ → ∇ψᵢ

	FUNCTION:
		Converts field differences between neighboring states into directional spatial structure.

	BOUNDARY:
		Gradient defines spatial organization only.
		Restoring Response is established by A-105.

	STATUS:
		YELLOW.
