---
node_id: "A-101"
canonical_name: "GROUND / ZERO"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Foundation Primitive"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node A-101: GROUND / ZERO

LAYER: A-Series Core

DEPENDENCIES:
UPSTREAM: A+101 One Field Ground.
DOWNSTREAM: A-102 Displacement, all downstream nodes requiring a reference condition.

1. PURPOSE
Defines the reference condition from which displacement, difference, and change are measured.

INPUT:
Current field state ψ.
Reference ground state ψ₀.

OUTPUT:
Reference condition.

FUNCTION:
Establishes the baseline from which change is defined.

2. DEFINITION
Ground / Zero is the reference state required for measurement.

Naming note — Void: "Void" has been used informally elsewhere to
describe the reference/zero condition. A+101's root axiom states there
is one field, always present, never absent — so "Void" cannot mean
literal absence-of-field without contradicting that axiom. The only
coherent reading is that Void = ψ = ψ₀, the zero/reference condition
within the one field, which is exactly what this node already defines.

CORRECTION (this fix — resolves a false dichotomy in an earlier
version of this note): an earlier draft of this section additionally
claimed Void "cannot be a spatial region" on the grounds that
Ground/Zero is a value, not a place. That inference does not follow.
ψ=ψ₀ is a condition a point can satisfy; nothing about defining that
condition as a value prevents it from being satisfied across an
extended region. The value (ψ=ψ₀) and its spatial extent (the set of
points where that value holds) are answers to two different questions,
not competing definitions — the value is the criterion, the region is
where the criterion holds. So:

- A-101 remains the criterion: Ground/Zero = the reference value ψ=ψ₀.
  Nothing above changes.
- Void, read as a region, is that same value instantiated across
  space — the set of points currently satisfying ψ=ψ₀ — not a rival
  primitive competing with A-101.
- The internal structure of that region (boundary behavior, cell
  geometry, etc.) is E-517 Negative Space's job, not A-101's. A-101
  still only defines the value; it does not need to, and should not,
  take on spatial/geometric content itself.

Fuller content (added — the void is not passive nothingness):
The void is the absence of defined compression, not the absence of the
field itself. Before a state exists there is possibility. The void
provides: space for displacement, contrast for identity, room for
oscillation, and the boundary between states. Reference point:
0 = undifferentiated potential. From the void, difference appears;
difference creates relationship; relationship creates structure.
This is consistent with, and adds detail to, the ψ=ψ₀ reading above —
it does not replace it. "Void" and "Ground/Zero" remain one concept
under two names, resolved by the same logic used for Mirror/Mirror
Gate and Balance/Balance earlier — checked against the actual root
axiom rather than assumed.

Operational chain (added): Void (this node) => Move (B-223, Up/Stay/Down)
=> Choice (B-224, Compression/Expression bias) => New State => feedback into Void.

ψ and ψ₀ are inherited from A+101 One Field Ground:

ψ = the one field, expressed as the current field state.

ψ₀ = the ground condition of that same field, expressed as the reference ground state.

A-101 does not redefine ψ or ψ₀. It establishes the operational reference role they play in measurement.

Displacement:

x = ψ - ψ₀

A valid displacement requires a defined reference.

RULE:
NO GROUND:
No displacement can be measured.

3. STATE VARIABLES
ψ = current field state (inherited from A+101 One Field Ground).
ψ₀ = reference ground state (inherited from A+101 One Field Ground).
x = displacement from ground.

REFERENCE CONDITION:

ψ = ψ₀ → x = 0

ψ ≠ ψ₀ → x ≠ 0

4. MATHEMATICS
DISPLACEMENT:

x = ψ - ψ₀

ZERO CONDITION:

ψ = ψ₀

THEN:

x = 0

DISPLACEMENT CONDITION:

ψ ≠ ψ₀

THEN:

x ≠ 0

SAME-GROUND DIFFERENTIAL:

For states ψₙ and ψₙ₋₁:

ψ₀,ₙ = ψ₀,ₙ₋₁

Therefore:

Δx = ψₙ - ψₙ₋₁

Reference cancels when ground remains fixed.

5. RELATIONSHIP
CHAIN:
A+101 One Field Ground → A-101 Ground / Zero → A-102 Displacement → A-103 Differential.

ROLE:
A+101 establishes the one field.
Ground establishes the measurement baseline within that field.
Displacement establishes separation from reference.
Differential measures relationships between states.

BOUNDARY:
Ground does not measure change.
Ground establishes the condition from which change is measured.

6. OPERATIONAL RULE
A measurement requires:

1. A current state.
2. A reference state.
3. A defined relationship.

RULE:

ψ - ψ₀ → x

NO GROUND:
No displacement.

7. RECURSIVE POSITION
Ground / Zero is the first measurement primitive, established within the one field asserted by A+101.

FUNCTION:
Provides the reference condition required by all later comparison operations.

BOUNDARY:
Does not define displacement or differential.

8. RECURSIVE SCALING
REQUIREMENT:
Preserve Ground / Zero meaning across Micro, Small, Medium, Large, Macro.

OPEN:
Does the same ψ₀ remain invariant through recursive expansion?

POSSIBLE MODELS:

Universal:
One fixed ψ₀.

Local:
Each region contains ψ₀,ᵢ.

Nested:
Each scale contains a local ground within a larger ground.

9. CONSTRAINTS
C-301:
Ground must be explicitly defined.

C-302:
Ground movement must be separated from system movement.

C-303:
Different representations must preserve reference meaning.

C-304:
Recursive levels must maintain valid zero conditions.

C-305:
Projection behavior must preserve or define transformed ground.

10. DEPENDENCIES
UPSTREAM:
A+101 One Field Ground.

ROLE:
First reference primitive within the one field.

DOWNSTREAM:
A-102 Displacement.
A-103 Differential.
All dependent measurement systems.

11. FAILURE MODES
F-601:
Undefined ground.
No displacement calculation possible.

F-602:
Moving ground.
False change introduced by reference drift.

F-603:
Multiple incompatible grounds.
Comparisons become invalid.

F-604:
Projection distortion.
Different representations create different zero states.

F-605:
Recursive drift.
Ground meaning changes across scales.

12. ADVANCEMENT CRITERIA
ADVANCE WHEN:

1. Stable ground representation is demonstrated.
2. Ground drift can be measured.
3. Differential calculations remain invariant under controlled transformations.
4. Recursive layers preserve reference meaning.
5. Geometry transformations preserve or define ground behavior.

CURRENT:
Definition ✅
Reference Equation ✅
Operational Role ✅
Dependency Foundation ✅
Geometry Invariance ❌
Long-Term Drift Testing ❌
Recursive Invariance ❌

GATE:
GREEN = Defined.
YELLOW = Constrained/Testable.
BRONZE = Validated.
SILVER = Integrated.
GOLD = Confirmed.

13. FINAL DEFINITION / CLOSURE
NODE:
A-101 Ground / Zero.

DEFINITION:
Ground / Zero defines the reference condition against which all displacement and differential measurements are made.

EQUATION:

x = ψ - ψ₀

FUNCTION:
Provides the baseline required for all measurable change.

BOUNDARY:
No Ground → No Displacement.

STATUS:
YELLOW.
