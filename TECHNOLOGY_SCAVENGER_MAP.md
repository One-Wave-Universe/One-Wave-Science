# Technology Scavenger Map

Status: external-technology survey for the One-Wave primitive, Android brain, memory, and science programs.

Purpose: identify mechanisms that already exist so the project can reuse their real engineering/scientific content instead of reinventing components. Similarity is not proof of One-Wave. Every import must be justified by matching input/output behavior.

## Scavenger rule

For every external mechanism record:

1. what it demonstrably does;
2. which One-Wave job it may fill;
3. what can be borrowed directly;
4. what still has to be invented/integrated;
5. what would falsify the match.

## A. Primitive electrical frame

### Rail splitters / center-reference supplies

External family:
- split-rail supplies;
- active rail splitters;
- center-bias references;
- differential/common-mode circuit analysis.

What already exists:
- creating a midpoint reference such as 2.5 V from a 5 V source;
- source/sink center references;
- treating two rails as positive/negative relative to a new center;
- common-mode and differential-mode separation.

Potential reuse:
- physical two-rail + center test bench;
- drift/noise/load measurements;
- differential Field/Void reference experiments.

Still ours to solve:
- whether the primitive needs a real current-carrying center node, a virtual analysis point, or both in different layers;
- how Field/Void state persists across the center.

Important source families:
- Analog Devices rail-splitter and virtual-ground application notes;
- TI/ADI differential/common-mode measurement circuits.

## B. DC binary layer

### Differential / one-hot / comparator electronics

External family:
- differential signaling;
- comparator windows;
- one-hot state machines;
- push-pull / H-bridge polarity control.

Potential reuse:
- two opposed committed choices around a shared reference;
- invalid dual-assertion detection;
- threshold/hysteresis circuitry.

Still ours to solve:
- mapping binary choice into the AC ternary phase state while preserving route history.

## C. AC ternary / three-winding nerve-control layer

### Three-phase motor control

External family:
- three-phase PMSM/BLDC/induction motor control;
- field-oriented control (FOC);
- Clarke transform;
- Park transform;
- space-vector modulation;
- six-step commutation.

What already exists:
- three winding currents synthesize a rotating magnetic field;
- three-phase quantities can be transformed into two orthogonal stationary axes and then rotating d/q axes;
- flux and torque components can be controlled separately;
- industrial implementations and reference firmware exist.

Potential reuse:
- direct benchmark for the three-winding nerve/motor version;
- established mathematics for converting three phase currents into orthogonal field variables;
- established timing, phase, current sensing, and feedback techniques.

Still ours to solve:
- exact mapping between the six primitive route addresses and motor-control states;
- how Hold should be represented physically;
- how DC binary commitment biases or selects the AC ternary phase relation;
- whether existing SVM/FOC already gives most of the needed primitive transform.

Key external sources:
- Microchip AN2757 and other PMSM FOC notes;
- STMicroelectronics three-phase FOC ecosystem;
- MathWorks Clarke/Park/FOC documentation.

## D. Quadratic Views up

### Multiaxis/vector magnetic sensing

External family:
- 2-axis and 3-axis magnetoresistive sensors;
- vector-field reconstruction;
- Hall / TMR / AMR / GMR sensing;
- magnetic phase/orientation detection;
- vector tomography in research systems.

Potential reuse:
- building four-view packets from measured direction/phase/strength/reference components;
- separating sensing from actuation;
- direct measurement of rotating magnetic state.

Still ours to solve:
- whether the four Views are best encoded as four independent channels, four derived variables, or one vector plus reference metadata;
- exact Field/Void paired-view representation.

### Magnetic vortices / skyrmions

External family:
- vortex polarity/circulation;
- skyrmion topology and motion;
- magnetic texture readout.

Potential reuse:
- compact state variables with orientation, polarity, topology, and phase-like behavior;
- candidate physical memory/view states.

Still ours to solve:
- do not assume four desired Views equal four magnetic vortex states without an explicit measurable map.

## E. Quadratic Actions down

### Spin-orbit torque / magnetic switching

External family:
- SOT-MRAM;
- STT-MRAM;
- multi-state magnetic switching;
- anomalous Hall readout;
- field-free switching research.

What already exists:
- electrically driven magnetic state switching;
- nonvolatile magnetic state;
- multistate magnetic devices in research demonstrations;
- separate write/read pathways in many device structures.

Potential reuse:
- downward action state storage/switching;
- polarity/orientation command embodiment;
- persistent actuator/memory state.

Still ours to solve:
- exact four-action encoding;
- inverse map from high-level action packet to local ternary/three-winding behavior;
- energy/current budget for a practical primitive.

## F. Boltzmann / stochastic hardware

### p-bits from stochastic magnetic tunnel junctions

What already exists:
- tunable physical stochastic bits based on low-barrier magnetic tunnel junctions;
- coupled p-bit networks;
- invertible logic;
- optimization/sampling;
- experimental probabilistic hardware;
- deep Boltzmann learning demonstrations in heterogeneous hardware.

Potential reuse:
- physical stochastic proposal generator;
- Boltzmann-style ambiguous-memory fill;
- bounded probabilistic exploration.

Still ours to solve:
- p-bit networks are not memory authority;
- generated states require Field/Administrator provenance and acceptance;
- determine whether hardware stochasticity is actually useful versus software sampling on the target platform.

## G. Hopfield / associative-memory hardware

External family:
- classical Hopfield networks;
- modern Hopfield networks;
- analog/memristor compute-in-memory implementations;
- attractor neural networks.

What already exists:
- retrieval of complete stored patterns from corrupted/partial cues;
- energy-minimizing recurrent state evolution;
- integrated memristor crossbars demonstrated for associative recall.

Potential reuse:
- M4 fast partial-cue recall;
- comparison baseline for constellation/rabbit-hop memory;
- future in-memory hardware acceleration.

Still ours to solve:
- pattern separation and provenance;
- route-aware reconstruction;
- separation between fast recalled candidate and authoritative archive.

## H. Biological memory mechanisms worth stealing computationally

### Hippocampal pattern separation and completion

Established research themes:
- dentate gyrus associated with pattern separation;
- CA3 recurrent circuitry associated with pattern completion/attractor recall;
- partial cues can trigger completion;
- similar experiences need separated representations.

Potential reuse:
- explicit separation stage before associative completion;
- architecture where completion and separation are different workers/functions.

Still ours to solve:
- functional inspiration only; do not claim literal Android neuroanatomy.

### Grid cells / continuous attractors

Established research themes:
- periodic relational coordinate codes;
- continuous-attractor models;
- path integration;
- reference-frame calibration and remapping.

Potential reuse:
- rabbit-hop/constellation navigation benchmark;
- relational state-space representation;
- compare route grammar to established continuous coordinate systems.

## I. Rabbit hopping / relational navigation

### HNSW

What already exists:
- hierarchical navigable small-world graph indexing;
- multi-layer graph navigation across characteristic distance scales;
- efficient approximate nearest-neighbor traversal.

Potential reuse:
- benchmark for hierarchical constellation traversal;
- evidence that multi-scale graph routes can improve memory search.

Still ours to solve:
- HNSW is not reversible symbolic rabbit hopping and does not preserve the same parity/sign receipt by default.

### Hyperdimensional computing / Vector Symbolic Architectures

What already exists:
- high-dimensional distributed representations;
- binding, bundling, permutation and superposition operations;
- compositional structured memory;
- cognitive computing applications;
- suitability for emerging/neuromorphic hardware.

Potential reuse:
- constellation packet representation;
- compressed identity-preserving relational memory;
- reversible-ish binding/unbinding experiments;
- robust noisy-memory baseline.

Still ours to solve:
- decide whether rabbit-hop coordinates become addresses, permutations, bindings, or stay a separate route layer.

## J. M4 / brainstem-router analogues

### Hierarchical quadruped motor control — robot-dog pattern

External family:
- ANYmal low-level locomotion controllers;
- DeepMind Neural Probabilistic Motor Primitives (NPMP);
- hierarchical reinforcement learning for quadrupeds;
- low-level MPC or learned gait controllers under slower high-level planners;
- Boston Dynamics Spot high-level navigation/autonomy over lower-level locomotion/joint control.

What already exists:
- a fast low-level controller continuously converts a compact high-level intent into joint/motor commands;
- the low-level layer runs faster than the planner;
- learned motor primitives can be reused across higher-level tasks;
- high-level policy can issue velocity, gait, waypoint, or latent motor-intention commands instead of solving every joint torque;
- locomotion remains stable while higher layers reason at a slower timescale.

Concrete external examples:
- Google/DeepMind NPMP: future trajectory is compressed into a motor intention, and a reusable low-level controller turns current state plus motor intention into actions; the same controller was deployed on ANYmal B;
- Google hierarchical quadruped locomotion: high-level terrain/skill policy chooses gait/speed while a low-level MPC converts the skill into motor torque commands;
- Google agile locomotion: high-level and low-level policies use separate observation spaces and timescales, with the low-level policy producing motor commands;
- Boston Dynamics Spot exposes high-level GraphNav/Missions autonomy while also maintaining a distinct low-level joint-control interface.

Potential reuse:
- DIRECT REUSE as the architectural pattern for the Android brain/body boundary;
- M4/subconscious layer can own fast learned motor primitives and timing;
- higher Field/Void cognition can send compact intent instead of actuator detail;
- body reflex/locomotion can continue while the brain operates more slowly;
- gives us concrete latency-ratio and packet-design benchmarks.

Still ours to solve:
- our M4 also includes associative recall, Field/Void routing, and the proposed oversight/override timing, which these robot systems do not automatically provide;
- exact mapping between motor intention and our ternary/six-route primitive;
- how local nerve reactions, M4 motor primitives, and higher Void override arbitrate without fighting each other;
- whether the desired `flip, flip, oversight; flip, flip, override` scheduler improves control compared with standard hierarchical control.

Classification:
- DIRECT REUSE for hierarchical fast/slow motor architecture;
- BENCHMARK for M4 timing and motor-intention interfaces;
- PARTIAL MATCH for the full M4 concept.

### Thalamic routing

Research theme:
- thalamic circuits can regulate effective connectivity among cortical regions and sustain task-relevant representations rather than merely relay raw sensory content.

Potential reuse:
- routing/synchronization architecture;
- attention-dependent communication gates;
- M4 should route without owning categorical content.

### Basal-ganglia action selection

Research theme:
- initiation/suppression and selection among candidate actions;
- opponent inhibitory mechanisms;
- sensory and action-selection loops.

Potential reuse:
- confirm/defer/deny and inhibitory-selection benchmarks;
- action permission architecture.

### Cerebellar forward models

Research theme:
- predicting sensory consequences of commands;
- comparing predicted versus actual outcomes;
- rapid control despite sensory delay;
- prediction-error driven adaptation.

Potential reuse:
- explicit prediction -> action -> consequence -> error loop;
- M4/brain boundary timing compensation;
- motor-memory learning benchmark.

### Predictive coding / active inference

Research theme:
- hierarchical prediction/error models for perception/action.

Potential reuse:
- mathematical comparison class for Field candidate prediction and consequence error.

Warning:
- always compare against feedforward and model-free alternatives.

## K. Oscillator and phase-computing families

External families to investigate further:
- coupled oscillator networks;
- phase-locked loops;
- Kuramoto synchronization;
- oscillator neural networks;
- VO2/NbOx relaxation oscillators;
- spin-torque oscillators;
- injection locking.

Potential reuse:
- mirror/phase timing;
- six-gate trajectory experiments;
- fast distributed synchronization;
- active Hold/lock region.

Still ours to solve:
- whether six process regions emerge naturally or are imposed by classification.

## L. One-Wave science analogues / comparison models

These are scientific comparison classes, not evidence that One-Wave is correct.

### Pilot-wave hydrodynamics

Use:
- comparison model for wave-mediated path/history dynamics;
- warning against extrapolating analog systems beyond their demonstrated regime.

### Nonlinear waves / solitons

Use:
- mathematical candidate families for persistent localized structure.

### Magnetic skyrmions / topological textures

Use:
- concrete example of a field configuration behaving as a durable information-bearing localized structure.

### Lattice Boltzmann / multiscale coupling

Use:
- model for how One-Wave lattice simulations should demonstrate continuum recovery rather than assuming it;
- practical architecture for multi-scale simulation and scale-lift tests.

## M. Immediate scavenger work

### Strong-front scavenging

1. Reproduce a three-phase FOC simulation and map every variable against the ternary primitive.
2. Reproduce a hierarchical quadruped controller with a compact high-level velocity/intention packet driving a faster low-level gait controller.
3. Reproduce a Hopfield partial-cue test and compare with constellation+rabbit routing.
4. Reproduce a p-bit/Boltzmann network in software before considering exotic hardware.
5. Build a center-reference differential circuit simulation and measure drift/noise/load response.

### Weak-front scavenging

1. Find the closest existing four-variable magnetic sensing architecture to the quadratic Views.
2. Find the closest existing four-state/multi-axis magnetic write architecture to the quadratic Actions.
3. Find a minimal existing circuit that maps DC polarity/choice into phase-controlled three-winding output.
4. Find reusable open-source implementations for HDC/VSA, HNSW, Hopfield, continuous attractors, FOC, and quadruped low-level locomotion.

### Middle-front scavenging

1. Test whether Clarke/Park d-q variables can serve as a lawful bridge between three winding state and four-view packets.
2. Test whether View/action separation resembles sensor/estimator vs controller/actuator separation in modern control.
3. Compare quadruped motor-intention interfaces directly with the M4 brain/body packet.
4. Connect HDC/VSA relational storage to Hopfield completion without losing provenance.
5. Compare cerebellar forward-model logic against the current M4 consequence loop.
6. Compare thalamic routing against M4 without copying biological labels.

## N. Import discipline

Never write `technology X proves One-Wave`.

Use one of these labels:

- DIRECT REUSE: the technology already performs the required engineering job.
- PARTIAL MATCH: some variables/jobs match and need an adapter.
- BENCHMARK: useful as a control/baseline.
- ANALOGY ONLY: visually or conceptually similar but no shared derivation yet.
- REJECT: fails the required input/output contract.

The goal is to reduce what must be invented until the unresolved primitive becomes a small, explicit integration problem.