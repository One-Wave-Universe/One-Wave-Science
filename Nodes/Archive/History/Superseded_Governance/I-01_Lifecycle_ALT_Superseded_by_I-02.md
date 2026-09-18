---

Function Node

Function: Special Rules I — Node Proof & Trust Lifecycle

---

Purpose

Every node and book chapter in the repository must carry a single, unambiguous claim about how proven it is, separate from what kind of work has been done on it. Special Rules I defines that claim formally — the stage a node/chapter occupies, the order stages must be passed through, and the one conditional transform (Gray → Red) that ties the lifecycle to actual experimental confrontation with the Standard Model rather than internal math alone.

This node also defines what belongs inside any other node's local "Special Rules" section, so that exceptions don't get scattered across Failure Condition, Dependencies, or Future Work by mistake.

---

Definition

Let a node or book chapter be an object x. Define the stage function

\boxed{\sigma(x) \in S}

where S is the ordered set of proof stages

\boxed{S = \{Brown,\ Green,\ Yellow,\ Bronze,\ Silver,\ Gold\}}

with a strict order relation

\boxed{Brown \prec Green \prec Yellow \prec Bronze \prec Silver \prec Gold}

For book chapters specifically, Green is replaced by a parallel state Gray, occupying the same position in the order:

\boxed{Brown \prec Gray \prec Yellow \prec Bronze \prec Silver \prec Gold} \quad \text{(chapters only)}

Gray is not a synonym for Green. Green certifies that the underlying math has room to grow and is ready for work. Gray certifies a documentation discipline: that the chapter has stated its relationship to the Standard Model without omission.

---

Mathematics

Define the Gray comparison as a three-valued function over a chapter x and a Standard Model reference point r:

\boxed{C(x,r) \in \{DirectEquivalent,\ PartialEquivalent,\ NoEquivalent\}}

C must be stated for every chapter; it is never left undefined.

Define E(x,r) as the experimental result confronting the Standard Model at comparison point r (E is undefined until an experiment is actually run — E is not a function of math alone).

Define the Red transform:

\boxed{
\sigma(x) \to Red \iff \sigma(x) = Gray \ \wedge\ E(x,r) \text{ is defined} \ \wedge\ E(x,r) \vDash \neg SM(r)
}

That is: Red is only reachable from Gray, and only when a real, defined experimental result forces the negation of the Standard Model at that specific comparison point. No other stage transforms into Red. Yellow's internal consistency, no matter how clean, does not satisfy the right-hand side of this condition, because Yellow has no defined E term.

Define the NoEquivalent branch explicitly as a choice, not a terminal state:

\boxed{
C(x,r) = NoEquivalent \implies x \in \{Brown,\ Grow(x)\}
}

where Grow(x) denotes building x out into something not derived from or mapped onto the Standard Model at all. NoEquivalent has no forced outcome — the object either stays at its current stage (Brown-equivalent, stuck) or advances under its own terms.

Advancement conditions, stage by stage:

\boxed{Brown \to Green/Gray \iff x \text{ has a template slot and an ID}}

\boxed{Green \to Yellow \iff \text{math for } x \text{ is built and internally tested}}

\boxed{Gray \to Yellow \iff C(x,r) \text{ is stated for every } r, \text{ without omission}}

\boxed{Yellow \to Bronze \iff \text{simulation run} \wedge \text{metadata attached} \wedge \text{first successful validation}}

\boxed{Bronze \to Silver \iff \text{validated in a second, independent application}}

\boxed{Silver \to Gold \iff \text{extraordinary, extensive validation across applications}}

\boxed{Gray \to Red \to Gold \iff \text{as defined above}}

---

Interpretation

The lifecycle has exactly one place where the model touches reality rather than its own internal consistency: the Gray → Red transform. Every other transition (Brown through Silver, and the ceiling at Gold) can in principle be satisfied by work done entirely inside the framework — building, testing, simulating, reusing. Red cannot. Red requires E(x,r) to be defined, which requires an experiment to have actually been run.

This is deliberate, and it is the same discipline already locked elsewhere in the repository: a node is never permitted to assert "the Standard Model fails here" from math alone, no matter how elegant the derivation. It states what the Standard Model says, what the math says as far as it goes, and — only after a real experiment — what happened. Red is a record of an outcome, not a claim of victory.

---

Assumptions

This node assumes:

1. Every node and chapter can be assigned exactly one σ(x) at any given time — stages do not overlap.

2. E(x,r), when defined, is a genuine outside result — not one derived from or fitted to One-Wave itself.

3. The comparison point r is specific enough that C(x,r) and E(x,r) are both well-defined statements, not vague resemblance claims.

Those assumptions should be stated explicitly because a future node may need to challenge whether "exactly one stage at a time" holds once composite objects (a node built from sub-nodes at different stages) enter the repository.

---

Candidate Experiment

Objective

Confirm that the Gray → Red transform, as formalized above, correctly refuses to fire on any currently Gray-tagged chapter that has not yet had a real experiment run against it.

Procedure

1. Enumerate every book chapter currently carrying a Gray tag.
2. For each, check whether E(x,r) is defined for any r.
3. Confirm that σ(x) = Red has not been assigned to any chapter where step 2 returns undefined for all r.
4. Flag any chapter currently marked Red without a defined E(x,r) as a template violation, not a valid stage.

---

Dependencies

Core Functions

None upstream. This node is a Special Rules governance node, not a physical claim, and does not derive from ψ, the lattice, or the update rule.

Supporting Functions

None.

Downstream Functions

Every node's Status field and local Special Rules section, across all series — A through G. Every book chapter's Gray comparison section. Any future audit tooling that reads or assigns σ(x).

---

Green Audit Result

The stage order, the Gray/Green split, and the Red transform are now stated as explicit predicates rather than prose descriptions. The one previously unconfirmed point — whether Gray-turns-Red extends to nodes as well as chapters — is not resolved by this audit and is carried forward rather than assumed.

---

Final Green Lock

Special Rules I is locked at Green: structurally complete, internally consistent, terminology stable, ready for use as the standard other nodes and chapters are checked against. It is not Gold — it has not been "extraordinarily validated" in the sense that term carries elsewhere in the repository, because a rules node doesn't undergo the same kind of experimental confrontation a physics node does. Green is the honest ceiling for this node's own claim about itself.

---

Special Rules (local to this node)

- This node's own σ cannot reach Yellow-Bronze-Silver-Gold the way a physics node does, because it makes no falsifiable claim about ψ. Its ceiling is Green by design, not by an unmet test. This is a boundary exception, not an open failure.
- The Red transform defined above applies to *other* nodes/chapters; it does not apply reflexively to Special Rules I itself, since this node has no Standard Model comparison point r of its own.

---
