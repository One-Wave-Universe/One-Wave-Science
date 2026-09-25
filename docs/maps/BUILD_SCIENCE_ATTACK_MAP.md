# Build Science Attack Map

Status: working engineering map. This file organizes the build problem from primitive electronics through control, memory, routing, compute, and project versions. It does not assume the integrated primitive is already solved.

## Tri-front attack method

Every subsystem is attacked from three directions at the same time:

### Strong front
Attack what appears strongest.

Goal: try to break the parts we currently trust most.

Questions:
- does the existing demonstrated technology actually match the job we assigned it?
- what assumptions were imported from analogy rather than measured behavior?
- does it still work under noise, drift, latency, scale change, and interface constraints?
- can a simpler conventional mechanism explain the same result?

### Weak front
Attack the least resolved part.

Goal: expose the current blocker instead of building around it.

Questions:
- what exact interface is missing?
- what variable is undefined?
- what circuit/state transition cannot yet be implemented?
- what measurement would most reduce uncertainty?

### Middle front
Attack the connective tissue.

Goal: find where individually plausible components fail when joined.

Questions:
- do units and timing match?
- does one subsystem output the state the next subsystem actually needs?
- is information lost at the mirror, scale, memory, or action boundary?
- are we silently changing vocabulary while claiming continuity?

No subsystem advances because one front looks good. The three fronts must converge.

## 1. Primitive electrical frame

Current candidate:

- two opposed rails;
- shared virtual/reference center;
- Field and Void relation retained around the center;
- differential behavior measured relative to the center.

Strong attack:
- validate center stability, rail symmetry/asymmetry behavior, noise, and drift using ordinary low-voltage circuit techniques.

Weak attack:
- exact primitive circuit topology is unresolved.

Middle attack:
- determine how center-reference state is handed to binary, ternary, and quadratic stages without hidden re-referencing.

## 2. DC binary layer

Current job:

- opposed two-choice commitment relative to the center;
- Ground/reference is not a third committed binary choice.

Strong attack:
- use known one-hot/two-rail selection mechanisms as benchmarks.

Weak attack:
- determine the smallest reversible/center-referenced hardware implementation that preserves Field/Void identity.

Middle attack:
- specify how DC choice biases or gates the following AC ternary stage.

## 3. AC ternary layer

Current job:

- oriented movement around the center: down / hold / up;
- phase/history matters;
- this is the fast local nerve/control layer.

Existing technology family to study:

- three-phase / three-winding motor control;
- rotating magnetic field generation;
- vector-control transforms and center-referenced torque/flux decomposition.

Strong attack:
- confirm exactly what three-winding motor control demonstrates and what it does not demonstrate about the proposed ternary logic.

Weak attack:
- map six primitive route states onto a physical three-winding control implementation without inventing arbitrary lookup tables.

Middle attack:
- define timing/phase interface from DC binary selection into AC ternary movement and from ternary movement into quadratic view generation.

## 4. Six-route primitive

Current structure:

`2 binary choices x 3 ternary moves = 6 route addresses`

Strong attack:
- deterministic software reference already validates the finite count and illegal states.

Weak attack:
- physical route commitment thresholds, hysteresis, and timing remain unresolved.

Middle attack:
- connect route identity to actual analog/magnetic state while retaining reversible receipts.

## 5. Quadratic views up

Current job:

- four-view state travels upward;
- paired Field/Void views are retained;
- oversight belongs to the upward/view side.

Existing technology families to study:

- rotating magnetic-field / vector-state sensing;
- multiaxis magnetic sensing;
- magnetic phase/orientation state extraction;
- spintronic/magnetic systems that can expose multiple orthogonal state components.

Strong attack:
- identify demonstrated hardware that really supplies four independent or reconstructible view variables.

Weak attack:
- exact four-view physical encoding and readout primitive is unresolved.

Middle attack:
- prove by interface tests that ternary state can be converted into the required four-view packet without losing center, orientation, phase, or Field/Void provenance.

## 6. Quadratic actions down

Current job:

- four-action command travels downward;
- paired Field/Void actions are retained;
- override belongs to the downward/action side.

Existing technology families to study:

- spintronic magnetic switching;
- multi-state magnetic actuation;
- vector magnetic control;
- phase/polarity/circulation control where demonstrated.

Strong attack:
- identify which demonstrated devices genuinely support the action variables we require.

Weak attack:
- exact four-action actuator encoding and inverse mapping to ternary/local motor behavior is unresolved.

Middle attack:
- verify that an upward view packet and downward action packet are true complements without becoming the same signal renamed.

## 7. Mirrored transition timing

Current candidate receipt:

- old view upward;
- new view upward;
- old action downward;
- three mirrored flip-pairs rather than six unrelated flips.

Strong attack:
- test the software/event-state version for deterministic ordering and reversibility.

Weak attack:
- physical timing relationship remains unresolved.

Middle attack:
- specify buffer/latency/phase rules at each transition so old and new state cannot be confused.

## 8. M4 / nerve routing

Current job:

- fast local reactions;
- routing and synchronization;
- compression of body/local information upward;
- commands routed downward;
- slower oversight/override remains behind fast local reaction.

Strong attack:
- implement ordinary real-time event routing and measure latency budgets.

Weak attack:
- exact compression packet and arbitration rules between fast local response and higher intervention need completion.

Middle attack:
- test `flip, flip, oversight; flip, flip, override` as a scheduler/control policy rather than just a slogan.

## 9. Five lifecycle states

Current lifecycle:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

Strong attack:
- implement as an explicit finite-state machine in software and try to generate invalid transitions.

Weak attack:
- physical observables/thresholds that distinguish each lifecycle state are unresolved.

Middle attack:
- keep lifecycle separate from commitment amplitude, six routes, and six oscillator gates while defining legitimate cross-links.

## 10. Six oscillator/process gates

Current structure:

`Begin -> Build -> Hold -> Build -> Break -> Loop`

Strong attack:
- extract these gates from measured/simulated trajectories using objective classifiers.

Weak attack:
- exact gate boundary definitions are incomplete.

Middle attack:
- connect gate progression to lifecycle and route history without collapsing them into one axis.

## 11. Memory architecture

Current integrated memory pieces:

- constellation relational structure;
- rabbit-hop coordinate/scale/reconstruction route;
- Hopfield-style associative completion;
- Boltzmann-style probabilistic fill;
- active process memory in fast recurrent state;
- receipts preserving cues, routes, sign/orientation, uncertainty, and validation.

Strong attack:
- benchmark Hopfield completion and probabilistic reconstruction independently on small synthetic memories.

Weak attack:
- exact representation shared among constellation nodes, route grammar, active state, and long-term storage is unresolved.

Middle attack:
- measure whether rabbit-hop routing improves reconstruction versus a matched baseline, or merely adds complexity.

## 12. Rabbit hopping and scale translation

Current structure:

- anchor `N -> 2N`;
- wrapped odd connectors `2N-1` and `2N+1`;
- parity-aware inverse;
- route/orientation receipts;
- multiple upward route families preserved separately.

Strong attack:
- mathematical reversibility and ambiguity tests.

Weak attack:
- determine where this coordinate grammar actually improves control/memory rather than only describing it.

Middle attack:
- connect rabbit-hop scale transitions to lifecycle/state packets without confusing numerical scale with behavioral state.

## 13. Dream / Administrator / Executor

Current jobs:

- Dream generates candidates;
- Administrator evaluates/accepts/rejects/holds;
- Executor performs committed action.

Strong attack:
- implement with ordinary software agents/functions and enforce schema boundaries.

Weak attack:
- final division among the planned five AI workers remains open.

Middle attack:
- prevent the generator from silently becoming the authority or the executor from re-planning after commitment.

## 14. Heterogeneous compute

Current candidate allocation:

- CPU: authoritative state, scheduling, receipts;
- GPU: dense Field/tensor/Boltzmann work;
- NPU: bounded fast-loop/Hopfield inference.

Strong attack:
- benchmark parity and latency across devices.

Weak attack:
- actual target workloads and data-transfer costs need measurement.

Middle attack:
- ensure device boundaries do not create new hidden state authorities.

## 15. Recursive cell/cube packaging

Current direction:

- a complete lower-scale unit exposes a relational interface that lets it become one node at the next scale;
- higher scale should preserve identity/history while compressing detail.

Strong attack:
- implement nested software cells with identical envelope schemas.

Weak attack:
- exact physical packaging/topology remains unresolved.

Middle attack:
- test what information must cross a scale boundary for behavior to remain reconstructible.

## 16. Project versions

Each project is a domain version of the structural family, not the universal primitive itself.

Examples:

- electronics bench primitive;
- VTC/Wave Computer;
- droid body/nerve control;
- memory/reconstruction system;
- software/agent architecture;
- animator/editor as a separate software project that may reuse organizational patterns without becoming evidence for physical claims.

Every project must publish:

1. which primitive structures it instantiates;
2. which structures it omits;
3. domain-native variables and timing;
4. adapter mappings;
5. what it teaches us about the primitive;
6. what failed to transfer.

## Immediate build attack order — all three fronts in parallel

### Strong-front queue

1. Benchmark three-winding motor/vector control against the ternary job.
2. Catalog demonstrated multiaxis/spintronic view and action mechanisms against the quadratic jobs.
3. Stress-test six-route software logic, lifecycle FSM, and memory rebuild baselines.

### Weak-front queue

1. Draw the smallest two-rail + center + Field/Void primitive circuit candidate.
2. Define the exact DC-binary -> AC-ternary interface.
3. Define the exact ternary -> quadratic-view and quadratic-action -> ternary interfaces.
4. Freeze packet/state variables and timing receipts.

### Middle-front queue

1. Build a software-in-the-loop end-to-end primitive emulator.
2. Pass one event through binary -> ternary -> views-up -> oversight -> actions-down -> consequence -> new reference.
3. Add lifecycle and six-gate annotations without changing the primitive route.
4. Add memory reconstruction and rabbit-hop receipts.
5. Compare project versions to discover which interfaces survive unchanged.

Completion does not mean every project is finished. Build science is mature when the primitive interfaces are explicit enough that domain implementations can be swapped without changing the underlying state contract.