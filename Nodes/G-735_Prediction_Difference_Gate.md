---
node_id: "G-735"
canonical_name: "Prediction-Difference Gate"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar / Simulation Governance"
claim_gate_detail: "YELLOW (procedural requirement, no physics claim of its own)"
metadata_standard: "I-06"
---

# Node G-735: Prediction-Difference Gate

**Dependencies**
Upstream: G-734 Standard-Mechanics Control Run
Downstream: G-737 No Victory Without Observable Match, all relational-mechanics promotion decisions

## Rule

A relational-mechanics mechanism does not count as new physics unless
its control-run comparison (G-734) shows at least one of:

```text
(a) a measurable departure from the standard-mechanics prediction
    that matches an actual observation the standard model does not
    reproduce as well, or

(b) an equally accurate prediction reached through a genuinely
    simpler derivation (fewer free parameters, fewer imported
    assumptions) than the standard-mechanics path.
```

If a relational run reproduces the standard-mechanics run's numbers
via an equally or more complex derivation, that is a **consistency
check passed**, not a **discovery**. It confirms the reformulation
does not break known mechanics; it does not by itself justify claiming
new physics.

## Why This Gate Is Necessary

Several backlog nodes (C-327, C-330, C-331, C-332) are explicitly
Gray-equivalent restatements of standard mechanics — that is by
design, and is the correct outcome at this stage. G-735 exists to
prevent that equivalence from later being mistaken for, or presented
as, a novel prediction once more of the backlog is developed. A
reformulation earns "new physics" status only by clearing (a) or (b)
above, not by existing.

## Relation to G-734

G-734 supplies the two numbers being compared (Run A vs Run B). G-735
is the decision rule applied to that comparison. Neither is meaningful
without the other: G-734 without G-735 produces numbers with no
promotion criterion; G-735 without G-734 has nothing to gate.

## Failure / Revision Conditions

This node fails if a relational mechanism is promoted past Gray
equivalence (i.e. presented as new physics) without satisfying (a) or
(b) above against an actual control run, or if (b)'s "simpler
derivation" is asserted without an explicit parameter-count or
assumption-count comparison.
