# Primitive Build Map

Date: 2026-08-30
Status: working integrated architecture

This file assembles the current primitive from the parts already developed across control, memory, routing, scale, and project versions. It is not proof of the complete primitive and it is not yet a final wiring recipe. Its job is to show what the primitive has to contain, what existing technologies can be reused, what data/state must survive each transition, and what integration questions remain.

## 1. Primitive electrical frame

```text
+ rail
  |
Field
  |
shared center / virtual ground
  |
Void
  |
- rail
```

Primitive requirements:

- two opposed rails;
- one shared center reference;
- Field and Void retained as coupled opposites;
- differential state interpreted relative to center;
- center is reference, not a third binary choice.

## 2. DC binary layer

The first active control layer is two-state DC engagement.

```text
DC reference -> one of two opposed committed orientations
```

Logical form:

```text
YES / NO
```

Physical versions may implement this as complementary channels, opposed polarity, rail-side engagement, or another two-way mechanism.

## 3. AC ternary layer

The next layer is oscillatory motion around the same reference:

```text
-1 = one orientation
 0 = active Hold / center
+1 = opposite orientation
```

Binary and ternary combine into:

```text
2 choices x 3 movements = 6 route addresses
```

These are six resolved control possibilities, not six unrelated subsystems.

## 4. Three-winding nerve / motor-control version

A three-winding / three-phase motor-control system is an existing engineering analogue for the ternary nerve layer.

Existing engineering already provides:

- three winding/phase structures;
- rotating stator fields;
- phase/current sensing;
- field-oriented/vector control;
- transformation between three phase currents and orthogonal rotating-frame quantities.

Primitive mapping target:

```text
binary engagement
      +
ternary movement
      ->
three-winding local response
```

The unresolved part is not whether three winding motor control exists. The unresolved part is the smallest mapping that makes the primitive six-route and Hold structure operate through it while preserving Field/Void and the center reference.

## 5. Field and Void

Field and Void persist through the primitive.

Working functional split:

```text
Field = expression / proposal / active differential
Void  = reference / checking / containment / resolution
```

Current ternary domain vocabulary:

```text
Field: Express / Hold / Compress
Void:  Confirm / Defer / Deny
```

Field and Void do not swap identities through the mirror.

## 6. Quadratic Views upward

The upward quadratic layer carries four view quantities:

```text
Direction
Phase
Strength
Reference
```

Direction invariant:

```text
Views UP
```

Existing technology families already demonstrate useful pieces:

- rotating magnetic-field representations;
- vector/phase-resolved motor control;
- multiaxial magnetic sensing;
- spintronic magnetic sensing;
- vector-field reconstruction.

Primitive problem:

Find the minimum device arrangement that carries these four view quantities upward while preserving Field/Void pairing, phase, and the shared center reference.

## 7. Quadratic Actions downward

The mirrored quadratic layer carries four action classes downward:

```text
Inward
Outward
Across
Over
```

Direction invariant:

```text
Actions DOWN
```

Existing spintronic work provides candidate mechanisms such as electrically controlled magnetic switching and multistate magnetic configurations.

Primitive problem:

```text
four action classes
 -> encoded magnetic/spintronic command
 -> local actuator consequence
```

without inventing extra states the architecture does not require.

## 8. Quadratic mirror pair

```text
             HIGHER CONTROLLER
                ^         |
                |         v
          4 Views UP   4 Actions DOWN
                ^         |
                |         v
             Field / Void
                |
         local consequence
                |
                +----> next Views
```

This is one mirrored control relationship, not eight independent machines.

## 9. Three mirrored flip-pairs

Current structural interpretation:

```text
binary    <-> binary
ternary   <-> ternary
quadratic <-> quadratic
```

These are three mirrored transition pairs, not six independent flips.

Current temporal receipt to preserve during testing:

- old view upward;
- new view upward;
- old action downward.

## 10. Fast nerve timing and slower oversight

Current timing rule:

```text
flip
flip
oversight
flip
flip
override
```

Intended hierarchy:

```text
local nerve loop = fastest
M4 routing       = intermediate
higher cognition = slower
```

The body/nerve layer should be able to react locally before higher cognition completes interpretation.

## 11. M4 routing layer

M4 sits between local primitive loops and higher processing.

Jobs:

- collect and compress Views;
- preserve Direction / Phase / Strength / Reference;
- route information upward;
- route committed actions downward;
- maintain timing receipts;
- maintain recent state/history;
- support fast associative recall;
- select state/scale context;
- keep higher cognition on a need-to-know basis.

M4 is not the motor, Dream, Administrator, or long-term archive.

## 12. Memory is part of the primitive architecture

The primitive cannot be treated as stateless switching. Current architecture treats memory as a combination of persistent local state, relational structure, route history, and reconstruction.

Memory jobs remain separated:

```text
Constellation = relational memory structure
Rabbit hopping = reversible navigation / scale route
Hopfield-style process = associative completion
Boltzmann-style process = probabilistic/generative fill
Fast loop = active short-term/process memory
State machines = context validation / acceptance / commitment
```

Recall flow:

```text
cue
 -> constellation neighborhood
 -> rabbit-hop route
 -> associative completion
 -> probabilistic fill if needed
 -> state/context check
 -> rebuilt active memory
```

Generated memory content is proposal until validated.

## 13. Constellation memory

A memory is represented as a relational neighborhood rather than one monolithic stored record.

A constellation may link:

- sensory features;
- motion;
- phase/timing;
- language;
- body state;
- location;
- neighboring memories;
- prior consequences;
- scale context;
- route receipts.

A partial cue should be able to activate the relevant local neighborhood.

Pattern separation is mandatory: similar memories must not be collapsed into one attractor merely because they overlap.

## 14. Rabbit-hop routing

Rabbit hopping is the reversible route/coordinate mechanism used through memory and scale.

Core anchor:

```text
N -> 2N
```

Wrapped connectors:

```text
2N-1 <- 2N -> 2N+1
```

Parity-aware inverse:

```text
even X:          N = X/2
upper odd 2N+1:  N = (X-1)/2
lower odd 2N-1:  N = (X+1)/2
```

Preserve separate route families:

```text
shift then double: (N+k)*2
double then shift: 2N+k
```

Odd connectors retain side/orientation information. Mirror traversal may invert orientation; sign/orientation receipts must survive the transition.

Rabbit hopping is not the memory itself. It is the route used to move through relational structure and across scale.

## 15. Hopfield-style associative rebuild

Hopfield-style completion handles partial/noisy cues by settling toward a known stored relational pattern.

Primitive use:

- recover missing local state;
- restore procedural/motor context;
- provide rapid fast-loop recall;
- avoid asking higher cognition to rebuild every routine action from scratch.

It must not silently overwrite the long-term archive.

## 16. Boltzmann-style generative rebuild

Boltzmann-style reconstruction is used when genuine ambiguity or missing content remains.

Primitive use:

- generate candidate missing structure;
- explore alternative reconstructions;
- assign uncertainty/confidence;
- return proposals for validation.

Probabilistic fill is not automatically accepted as remembered fact.

## 17. Memory receipt

Every meaningful rebuild should be able to retain a compact receipt:

```text
triggering cue
constellation neighborhood
rabbit-hop anchors/connectors
mirror/sign inversions
associative completion contribution
probabilistic fill contribution
uncertainty/confidence
state/context validation result
final consequence
```

The receipt provides reversibility and debugging without duplicating the whole memory.

## 18. Higher processing split

Current higher-level version:

```text
Dream / Field
    -> generates possibilities
Administrator / Void
    -> evaluates / confirms / defers / denies
Executor
    -> commits approved action
```

The primitive family requires separation between proposal, evaluation, and committed execution where higher cognition exists.

## 19. Five-state lifecycle

Lifecycle remains separate from binary, ternary, quadratic, six-route address, and six oscillator steps.

```text
Idle
 -> Primed
 -> Executing
 -> Vectoring
 -> Resolving
```

Lifecycle answers where the self-contained process is in its behavioral cycle.

## 20. Scale recursion

The same structural family can recur at multiple scales without forcing every scale into the same implementation.

Possible instances:

- one electrical primitive;
- one nerve controller;
- one motor group;
- one M4 loop;
- one memory neighborhood;
- one higher cognitive subsystem;
- one complete machine.

Each scale must declare:

- native state;
- native timing;
- inputs;
- outputs;
- carrier/mechanism;
- reference;
- receipts.

A completed lower-scale structure should expose a compact interface so it can act as one node at the next scale.

## 21. Six process / oscillator steps

The recurrent process sequence remains:

```text
Begin -> Build -> Hold -> Build -> Break -> Loop
```

Keep it separate from:

- six binary-by-ternary route addresses;
- five lifecycle states;
- three mirrored flip-pairs.

The six steps describe recurrent stability/process progression, not route count or lifecycle count.

## 22. Full integrated primitive skeleton

```text
                           HIGHER PROCESSING
                     Dream / Administrator
                             Executor
                                ^
                                |
                               M4
                 routing + timing + fast recall
                                ^
                                |
                        4 QUADRATIC VIEWS
                                UP
                                ^
                                |
                          Field / Void
                                |
                         DC BINARY LAYER
                           two choices
                                |
                         AC TERNARY LAYER
                         -1 / 0 / +1
                                |
                     THREE-WINDING NERVE
                        / MOTOR CONTROL
                                |
                           CONSEQUENCE
                                |
                     4 QUADRATIC ACTIONS
                               DOWN
                                |
                          Field / Void
                                |
                           NEW LOCAL STATE
                                |
              +-----------------+------------------+
              |                                    |
        next Views upward                  memory/update path
                                                   |
                                      constellation neighborhood
                                                   |
                                          rabbit-hop route
                                                   |
                                      Hopfield completion
                                                   |
                                      Boltzmann fill if needed
                                                   |
                                       state/context validation
                                                   |
                                         rebuilt active memory
```

Electrical frame around the local primitive:

```text
+ rail
  |
Field
  |
virtual ground / shared center
  |
Void
  |
- rail
```

Cross-cutting state:

```text
binary choice
ternary motion
quadratic View/Action
Field/Void relation
Direction
Phase
Strength
Reference
lifecycle
scale
six-step process position
rabbit-hop route
constellation neighborhood
previous state
memory confidence
consequence receipt
```

## 23. What already exists as mechanisms or developed architecture

### Existing engineering mechanisms to reuse/study

- three-phase / three-winding motor control;
- rotating magnetic-field generation;
- current and phase sensing;
- vector-control transformations;
- multiaxial magnetic sensing;
- spintronic magnetic sensing;
- electrically controlled magnetic switching;
- multistate/four-state magnetic-device research.

### Architecture already developed in this repository

- Field/Void paired processing;
- DC binary + AC ternary six-route logic;
- quadratic Views up / Actions down direction rule;
- M4 fast routing layer;
- five-state lifecycle;
- six process steps;
- three mirrored flip-pair interpretation;
- constellation memory;
- Hopfield-style completion;
- Boltzmann-style reconstruction;
- rabbit-hop scale/route grammar;
- route/sign/orientation receipts;
- recursive scale packaging;
- proposal/evaluation/execution separation.

## 24. What is still unknown

The open problem is the integration bridge.

We still need to determine:

1. exact two-rail / virtual-center circuit;
2. exact binary switching topology;
3. exact DC-binary to AC-ternary transition mechanism;
4. exact six-route-to-three-winding mapping;
5. exact Hold behavior and hysteresis;
6. minimal hardware for four Views upward;
7. minimal hardware for four Actions downward;
8. exact phase/timing relationship among binary, ternary, and quadratic layers;
9. exact 3:1 / 6:1 timing implementation;
10. how local consequence updates lifecycle and six-step process state;
11. how local state is written into/linked with constellation memory;
12. how rabbit-hop receipts are generated from real transitions;
13. what memory must remain local versus higher/archive storage;
14. how one completed primitive packages itself as a node for the next scale.

## 25. Primitive convergence program

Every project/version must now feed this map.

For each version, record:

```text
what structure it uses
what carrier it uses
what behavior works
what fails
what state survives
what timing survives
what receipt survives
what is domain-only
what appears invariant
what this teaches us about the primitive
```

Then revise the primitive by keeping only relationships that survive across versions or are independently necessary for the primitive's function.

The goal is not to force every project into one implementation.
The goal is to use all project versions to make the smallest common primitive progressively clearer.
