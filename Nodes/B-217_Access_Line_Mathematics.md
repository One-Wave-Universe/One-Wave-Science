---
node_id: "B-217"
canonical_name: "Access Line Mathematics"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-217: Access Line Mathematics

Reason:
Definition complete.
Candidate mathematics established.
Validation of the weighting model (Flat vs. Weighted Depth) remains open.

Dependencies:
Upstream: B-213 Access Line, B-214 Recursive Access Growth
Downstream: B-218 Hyperloop Mathematics

Definition:
Access Line Mathematics is the formal mathematical framework governing how
individual Access Lines behave — persistence, merging, reactivation,
strength, and directionality — questions B-213 identifies but does not
resolve. B-214 already gives the growth count (n_AL(k) = k) and a linear
depth approximation (d_k = d_0 + k); this node is the layer beneath both,
addressing the *behavior* of a single Access Line rather than the count
or depth of the whole set.

Access Line Mathematics = formal framework for individual Access Line behavior

Mathematics (partial):
Each Access Line AL_i, for i = 1 to 7, is assumed to carry a state
S_i(t) that is not yet formally defined. Candidate components:

1. Persistence: does S_i decay without use?
   Candidate form (not yet derived): S_i(t) = S_i(0) * exp(-lambda_i * t)
   where lambda_i = 0 would mean pure persistence (B-213's "persistent"
   reading), lambda_i > 0 would mean decay-based.
   Which applies is exactly B-213's open question — not resolved here,
   only given a mathematical shape to be resolved against.

2. Strength through reuse: does S_i grow with repeated use?
   Candidate form (not yet derived): S_i(t+1) = S_i(t) + mu * usage(t)
   where mu is a reinforcement coefficient. Untested.

3. Directionality: is AL_i(A->B) the same object as AL_i(B->A)?
   Not yet formalized in either direction. B-213 leaves this fully open;
   this node does not add new information, only flags it needs a
   formal representation (scalar vs. vector vs. paired-scalar) before
   any of the above equations can be written precisely.

4. Merge/collapse: no candidate form proposed. B-213's question stands
   unaddressed at the mathematical level, not just the conceptual one.

Reconciliation with B-214:
B-214's d_k = d_0 + k treats all k active Access Lines as contributing
equally to depth (one unit of depth per line). This is the Flat Depth
Model. If persistence (item 1 above) turns out to include decay, a
Weighted Depth Model becomes the competing candidate:

Flat Depth Model (B-214's current form):
d_k = d_0 + k

Weighted Depth Model (candidate, not yet derived):
d_k = d_0 + Σ w_i
where w_i = current contribution state of Access Line i (i.e., some
function of S_i(t) from item 1/2 above, not yet specified)

Under the Flat model, access count alone determines depth. Under the
Weighted model, a heavily-reinforced line contributes more than a weak
or decaying one, and count alone is insufficient. These two models are
NOT reconciled here — this node records the fork, it does not resolve it.
B-214 keeps the Flat Model as its stated formula unless and until this
fork is resolved in B-214's favor or the Weighted Model's.

Operational Chain:
Access Line (B-213) + Recursive Access Growth (B-214) => Access Line Mathematics => Hyperloop Mathematics (B-218)

Yellow Audit:
- Persistence vs. decay (lambda_i) not determined — candidate form only
- Reinforcement coefficient mu not derived, not tested
- Directionality representation (scalar/vector/paired) not chosen
- Merge/collapse has no mathematical form proposed at all, not even a candidate
- Fork between Flat Depth Model (B-214's current form) and Weighted Depth
  Model (candidate) is unresolved and may require revising B-214 once
  persistence is known — this node does not pick a side
- Whether each of the 7 Access Lines has a distinct functional role
  (B-213's question) has no mathematical bearing here unless roles imply
  different lambda_i / mu per line — not yet explored

Future Work:
Choose a directionality representation before attempting the persistence
or reinforcement equations, since both depend on it.
Test the decay candidate form (item 1) against any available Access Line
behavior data, if any exists outside this framework.
Revisit B-214's d_k = d_0 + k once persistence is resolved — flag to B-214
if revision is needed rather than silently changing it here.

---
