# Android Brain Attack Map

Status: working central-brain architecture. Scope is only the Android brain: Field/Dream hemisphere, Void/Administrator hemisphere, and M4 brainstem/router. Peripheral nerves, motors, sensors, and body mechanics remain outside except at the brain input/output boundary.

## Tri-front method

Attack all three fronts simultaneously:

- Strong: try to break the parts that currently look most coherent or implementable.
- Weak: attack undefined variables, timing, authority, and interfaces.
- Middle: attack the handoffs among Field, Void, M4, memory, and consequence.

## 1. Central organization

`Field / Dream <-> M4 <-> Void / Administrator`

These are complementary jobs in one bounded system, not three independent minds.

### Field / Dream

Owns possibility space:

- candidate meanings and actions;
- association and recombination;
- counterfactual simulation;
- movement rehearsal;
- outward expression;
- probabilistic/generative reconstruction.

Field may propose. It does not own committed truth.

### Void / Administrator

Owns continuity and commitment:

- current committed reference;
- exact source/provenance authority;
- permissions and boundaries;
- contradiction/risk checks;
- confirm / defer / deny;
- rollback and receipt integrity;
- incorporation of justified consequence into the next reference.

Void is the receiving/reference/compressive side, not absence.

### M4 / brainstem

Owns fast routing and synchronization:

- salience and attention routing;
- timing and phase;
- scale selection;
- activation/integrity/polarity scoring;
- fast associative recall;
- coordination between Field and Void;
- compression of incoming body state at the brain boundary;
- learned fast responses before slower evaluation completes.

M4 never becomes the final authority or archive.

## 2. Minimum reciprocal loop

```text
Reference Ground
-> M4 routes cue/state
-> Field generates or reconstructs candidates
-> M4 supplies timing/scale/phase/coherence
-> Void confirms, defers, or denies
-> commitment/correction returns through M4
-> Field updates its next candidate field
```

This should execute as overlapping reciprocal state machines, not one giant serial prompt chain.

## 3. Strong-front attacks

### Field

- bounded candidate IDs and expiry;
- alternative-generation benchmark;
- movement rehearsal and counterfactual tests;
- Boltzmann-style reconstruction kept explicitly uncertain.

### Void

- deterministic permission/contradiction checks;
- exact receipt and rollback;
- confirm/defer/deny tests;
- provenance never dropped.

### M4

- fast event routing and latency measurement;
- Hopfield-style partial-cue recall;
- salience queues;
- scheduling and phase synchronization.

### Brain as a whole

- prediction -> action -> consequence -> prediction-error loop;
- ablate Field, Void, and M4 separately and measure characteristic failures.

## 4. Weak-front attacks

The main unresolved brain-build questions are:

1. minimum state vector for Field;
2. minimum commitment packet for Void;
3. exact M4 packet and arbitration law;
4. Reference Ground versus Working Ground semantics;
5. two state-machine transition tables;
6. exact timing ratio between M4 and the hemispheres;
7. what memory is durable versus active versus reconstructed;
8. how uncertainty propagates;
9. final identities of the planned five AI workers.

Do not invent answers merely to complete a diagram.

## 5. Middle-front attacks

### Field <-> Void

- Field cannot self-commit;
- Void cannot regenerate candidates and pretend they came from Field;
- rejection must retain enough context for useful correction;
- Defer must remain distinct from Deny.

### Field <-> M4

- M4 can alter priority/timing without changing candidate meaning;
- fast recall is marked as recall, not new truth;
- stale candidates must be detectable.

### Void <-> M4

- M4 carries authority decisions without owning them;
- fast memory may not silently rewrite the archive;
- override provenance must point back to the Void decision.

### Brain <-> body boundary

Views come up. Actions go down.

The brain map defines packet semantics, not the physical quadratic hardware.

## 6. Brain memory architecture

Keep these jobs separate:

- Constellation = relational memory structure.
- Rabbit hopping = reversible route/scale/navigation through that structure.
- Hopfield-style layer = fast associative completion from partial cues.
- Boltzmann-style layer = probabilistic reconstruction when ambiguity remains.
- Active process memory = recent timing/phase/route/state retained in the live loop.
- Void/Administrator = authority over accepted memory, source, provenance, and incorporation.

### Memory strong front

- benchmark pattern completion;
- benchmark pattern separation;
- benchmark probabilistic fill;
- test overlapping memories;
- preserve exact route receipts.

### Memory weak front

- freeze one shared memory packet;
- define durable versus reconstructed content;
- define confidence/uncertainty and separation thresholds.

### Memory middle front

- test whether rabbit-hop routing improves reconstruction versus a matched baseline;
- generated fill cannot masquerade as exact memory;
- M4 fast recall and Void archive cannot diverge silently.

## 7. Existing science/engineering to scavenge for the brain

These are outside technologies to study as candidate parts or constraints, not claims that biology maps exactly onto this architecture:

- hippocampal pattern separation and CA3-style pattern completion;
- continuous attractor/grid-cell navigation for relational/coordinate state;
- Hopfield and modern Hopfield associative memory;
- thalamic control of functional cortical connectivity as a routing analogy;
- basal-ganglia action-selection and inhibitory gating;
- cerebellar forward-model/prediction-error computation;
- predictive-coding and active-inference algorithms, tested against alternatives;
- HDC/VSA distributed relational representation;
- HNSW-style hierarchical graph navigation;
- p-bit/Boltzmann hardware for stochastic candidate generation;
- memristor compute-in-memory for associative reconstruction.

The scavenger rule is: take a mechanism only if its actual input/output job fits. Never import the biological label as proof.

## 8. Views up / Actions down brain boundary

Upward View packet should preserve at least:

- source/provenance;
- Field view;
- Void view;
- reference;
- orientation;
- phase/timing;
- strength/integrity;
- route/lifecycle context when used.

Downward Action packet should preserve at least:

- target;
- Field action;
- Void permission/override state;
- timing/phase;
- strength;
- receipt ID for matching the consequence.

Oversight belongs to the upward Void-view side. Override belongs to the downward Void-action side.

## 9. Consequence loop

```text
prediction
-> committed action
-> observed consequence
-> observed - predicted differential
-> M4 routes discrepancy
-> Field revises possibilities
-> Void revises committed reference if justified
```

Internal agreement is not enough. External consequence must be able to correct both hemispheres.

## 10. Five lifecycle states

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

These describe the behavioral/self process and remain distinct from six route addresses and six oscillator gates.

## 11. Six process gates

`Begin -> Build -> Hold -> Build -> Break -> Loop`

Use these as stability/transition annotations for active loops. Do not use them as lifecycle labels, memory confidence, or action priority.

## 12. Timing target

Current working scheduler relationship:

`flip, flip, oversight; flip, flip, override`

M4 is the faster loop. Hemisphere updates are slower. Consequence integration may be slower again depending on the task.

Measure:

- M4 tick latency;
- Field generation latency;
- Void evaluation latency;
- stale-state rate;
- missed-override and false-override rates;
- synchronization drift.

## 13. Heterogeneous compute candidate

- CPU: authoritative state, exact receipts, permissions, scheduler, committed memory.
- GPU: dense Field generation, simulation, tensor work, Boltzmann batches.
- NPU: bounded M4 fast loop and Hopfield-style inference.

Device assignment is implementation, not ontology. Benchmark transfer overhead and semantic parity before locking it.

## 14. Minimum executable brain before a body

1. Current Reference Ground.
2. Simulated upward View packet.
3. M4 routing plus partial-cue recall.
4. Field creates at least two bounded candidates.
5. Void Confirm/Defer/Deny.
6. One committed simulated Action packet.
7. Simulated consequence.
8. Prediction error.
9. Next reference update.
10. Full receipt across every handoff.

Success means repeated cycles without role collapse, stale-state confusion, provenance loss, or generated material silently becoming authoritative.

## 15. Immediate parallel attack queues

### Strong

- deterministic Void engine;
- bounded Field generator;
- Hopfield benchmark in M4;
- consequence-error loop;
- ablation testing.

### Weak

- packet schemas;
- Ground semantics;
- M4 timing/arbitration;
- two state-machine transition contracts;
- durable/active/reconstructed memory split.

### Middle

- Field -> M4 -> Void -> M4 -> Field conflict tests;
- uncertain-memory provenance tests;
- latency/stale-state tests;
- simulated Views-up/Actions-down with consequence matching;
- compare software workers and hardware allocations without letting either redefine the architecture.
