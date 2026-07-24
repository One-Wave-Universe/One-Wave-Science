---
node_id: "B-225"
canonical_name: "Five-Stage Field Transformation Cycle"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-225: Five-Stage Field Transformation Cycle

Reason:
Two earlier descriptions appeared to conflict:

1. Compress -> Center -> Choose -> Emerge -> Expand
2. Field -> Compression -> Center -> Emergence -> Expansion -> Field

They were not actually two competing five-stage cycles. The conflict came
from mixing the FIELD envelope with the internal operations and, in the
second version, dropping CHOICE from the counted stages.

Canonical resolution:

FIELD_n -> [COMPRESSION -> CENTER -> CHOICE -> EMERGENCE -> EXPANSION] -> FIELD_(n+1)

FIELD is the input/output context that contains the cycle. It is not one of
the five internal transformation stages. CHOICE is the third internal stage
and must not be omitted.

Dependencies:
Upstream: A+101 One Field Ground (Field envelope), A-101 Ground / Zero,
A-102 Positive Displacement, A-103 Differential Expression,
B-204 Compression, B-222 Oscillation Center, B-224 Two Choices,
B-223 Three Moves, B-221 Six Recursive Steps (MOVE), B-203 Expression
Downstream: future field-cycle diagrams, simulations, and scale-specific
instantiations

Definition:
The Five-Stage Field Transformation Cycle describes how an existing field
state is reduced, referenced, directed, displaced, and written back into an
updated field.

The five internal stages are:

1. COMPRESSION
   The current field's active possibilities are reduced toward a coherent
   local reference. This is the B-204 function.

2. CENTER
   The compressed state meets the null/reference/pivot condition. This is
   B-222's oscillation center, not B-201's broader balance relation.

3. CHOICE
   At the center, the system selects a polarity bias through B-224:
   Compression or Expression. Choice is not a field state and is not the
   same thing as movement. It constrains the next allowed movement.

4. EMERGENCE
   A selected displacement appears from the center. This inherits the
   displacement role of A-102/A-103 and B-221's MOVE step. Emergence is the
   field-level appearance of MOVE's displacement, not a second independent
   motion primitive.

5. EXPANSION
   The emerged pattern propagates outward and is written into the larger
   field. This is the field-cycle realization of B-203 Expression.

The result is FIELD_(n+1), the updated environment for the next cycle.

Important distinction:
The selected polarity and the outward write-back direction are different
properties. A compressive choice can still be expressed outward as the
content of the new field. Therefore "Choice = Compression" does not mean
that the write-back stage ceases to be Expansion.

Mathematical formalization:
Let the complete field state at cycle n be Ψ_n.

Compression:
    χ_n = C(Ψ_n)

Center projection:
    ψ_(0,n) = Z(χ_n)

Choice:
    σ_n ∈ {-1,+1}
    σ_n = -1  compression bias
    σ_n = +1  expression bias

Move constraint from B-223:
    m_n ∈ {0, σ_n}

Here m_n = 0 is STAY/HOLD and m_n = σ_n executes the selected bias. STAY is
therefore not a third polarity choice.

Emergence amplitude:
    Δψ_n = a_n m_n,    a_n >= 0
    ψ_(e,n) = ψ_(0,n) + Δψ_n

Expansion / field write-back:
    Ψ_(n+1) = X(Ψ_n, ψ_(e,n))

Compact composition:
    Ψ_(n+1) = X[Ψ_n, E(Q(Z(C(Ψ_n))))]

where C, Z, Q, E, and X are typed operators corresponding to Compression,
Center, Choice, Emergence, and Expansion. This equation formalizes sequence
and role. It does not yet derive the scale-specific physical forms of C, Z,
or X.

12-1(0)-1-12 relationship:
The mnemonic can now be read without confusing positions and operations:

    12_n -> 1 -> 0 -> 1 -> 12_(n+1)

12_n and 12_(n+1) are the field envelope before and after the cycle.
The two 1 positions are compressed and emerged local states. 0 is the center.
CHOICE acts at the center transition but is not itself an additional numeric
position. These numbers remain architectural labels, not derived physical
magnitudes.

Operational Chain:
FIELD_n
  => COMPRESSION
  => CENTER
  => CHOICE
  => EMERGENCE
  => EXPANSION
  => FIELD_(n+1)

Resolution Record:
- RESOLVED: Field is the surrounding input/output context, not one of the
  five internal stages.
- RESOLVED: Choice is the third internal stage and was incorrectly omitted
  from the later naming version.
- RESOLVED: Emergence is the field-level result of displacement/MOVE, not an
  unmatched sixth mechanism.
- RESOLVED: Expansion is the write-back realization of B-203 Expression.
- PRESERVED: both earlier wordings remain in History as the source of the
  reconciliation.

Yellow Audit:
- The sequence and operator types are now formalized.
- The exact physical forms of C, Z, and X remain scale-specific and must be
  supplied by each instantiation.
- The amplitude rule a_n and its limits are not derived here.
- "Exactly two choices" and "exactly three moves" remain inherited open
  closure claims from B-224 and B-223.
- The 12-1(0)-1-12 labels remain mnemonic until derived from a physical model.

Future Work:
1. Define C, Z, and X for one concrete lattice or hardware instantiation.
2. Test whether the typed composition conserves the quantities required by
   that scale.
3. Build the Bronze simulation only after those scale-specific operators are
   defined.
4. Add a cross-scale table under I-04 rather than assuming the same operators
   at every scale.

---
