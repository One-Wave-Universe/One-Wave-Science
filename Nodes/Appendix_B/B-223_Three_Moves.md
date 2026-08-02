---
node_id: "B-223"
canonical_name: "Three Moves (Up / Stay / Down)"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Directional Motion System"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-223: Three Moves (Up / Stay / Down)

Reason:
Correction notice: an earlier version of this node incorrectly defined
the three moves as {Expression, Compression, Mirror}. That was wrong —
Mirror (B-205) is a separate flip mechanism, not one of the three moves.
The correct structure, below, is a three-valued directional vector.

Dependencies:
Upstream: A-101 Ground / Zero (Void — the reference field the moves act relative to)
Downstream: B-224 Two Choices (the bias applied to a move), B-221 Six Recursive Steps (Hold step corresponds to Stay)

Definition:
The Three Moves describe HOW a state changes — the three fundamental
transitions available to any state, given as a signed vector:

UP (+): Expansion, increase, expression. Moves away from the current
  compressed state. More possibility, more degrees of freedom, greater
  external relationship. Field Action: Expression (B-203).
  Questions: "What can this become?" / "What new relationship can form?"

STAY (0): Maintenance, balance, coherence. Preserves the current
  relationship while monitoring change — stability without freezing.
  Field Action: Hold. NO DEDICATED NODE EXISTS FOR THIS YET — "Hold"
  currently only appears as a step inside B-221's six-step cycle, not
  as its own standalone primitive the way B-203/B-204 are. This is a
  real gap, not yet filled.
  Questions: "Is this state still coherent?" / "Does this pattern need adjustment?"

DOWN (-): Compression, return, integration. Moves toward simpler or
  more concentrated states. Reduction, storage, restoration.
  Field Action: Compression (B-204).
  Questions: "What can be conserved?" / "What returns to the center?"

Three Move Cycle: UP -> Expansion, STAY -> Stabilization, DOWN -> Integration.

This node describes the MOVE layer specifically — the vector itself
(+/0/-). It does NOT describe why a move goes up or down; that bias is
B-224 Two Choices, a separate layer. See Mathematics below for how the
two layers relate.

Mathematics:
Move (this node) and Choice (B-224) are related but distinct:
- Move is a 3-valued vector: {+, 0, -} = {UP, STAY, DOWN}
- Choice is a 2-valued bias: {Compression, Expression}
- UP's Field Action IS Expression, and DOWN's Field Action IS
  Compression — meaning for nonzero moves, Move and Choice are tightly
  coupled (a + move IS an Expression choice manifesting; a - move IS a
  Compression choice manifesting).
- STAY (0) is the case where no directional choice is currently
  manifesting as motion — not the same as "no choice exists," more
  like a choice held in reserve or in equilibrium.
This coupling is stated here as observation, not derived. Whether Move
and Choice are truly two independent layers, or Move is simply Choice's
visible output with an added "no active choice" state, is unresolved.

Operational Chain:
Void (A-101) => Move (this node, Up/Stay/Down) => Choice (B-224, Compression/Expression bias) => New State => feedback into Void

Yellow Audit:
- No dedicated node exists for STAY/Hold as a standalone primitive —
  flagged above, not filled here
- Whether Move and Choice are genuinely two layers or one layer counted
  twice is unresolved (see Mathematics)
- The closure claim ("exactly three moves, no fourth") is asserted by
  the source material's own framing, not derived from anything upstream
- Relationship to B-221's six-step cycle beyond the Stay<->Hold
  correspondence is not mapped — where do UP and DOWN fit against
  Begin/Move/Build/Break/Loop specifically?

Future Work:
Determine whether STAY/Hold should become its own dedicated node
(matching B-203/B-204's status) or remain only a step inside B-221.
Resolve the Move-vs-Choice layering question in Mathematics above.
Map UP and DOWN against B-221's six steps term by term.

---
