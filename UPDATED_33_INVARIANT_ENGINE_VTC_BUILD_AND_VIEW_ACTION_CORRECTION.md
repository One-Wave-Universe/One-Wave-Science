# UPDATED 33 — Invariant Engine, VTC Build, and View/Action Correction

**Status:** Current implementation handoff. This update protects the invariant state-machine kernel from domain-representation drift and records the current VTC physical build interpretation.

## 1. Primary Correction: Invariant Engine vs. Representations

The architecture now has a hard boundary:

```text
INVARIANT ENGINE
 -> representation wrappers
 -> physical/domain instantiations
```

### Anti-Drift Rule
> If deleting a domain vocabulary changes the six-pair oscillator, the domain representation has leaked into the kernel.

## 2. Canonical Six-Pair Oscillator

```text
F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6 - F1/V6 ...
```

`/` is one simultaneous mirrored relation. `-` is return to shared `(0)`, Mirror-Gate crossover and phase-shift. Six coupled operations expose twelve pair-side positions; they are not twelve unrelated serial instructions. The engine originates at `-(0)+`.

## 3. Six Process Steps

```text
BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP -> BEGIN
```

## 4. Four Views — measurement/state description

```text
Direction
Phase
Strength
Reference
```

Direction = which way relative to reference. Phase = where in the oscillatory cycle. Strength = amplitude/intensity. Reference = the local zero/baseline giving the others meaning.

## 5. Four Actions — transformation/routing

```text
Inward
Outward
Across
Over
```

For the current hardware interpretation:

- **Inward** = signal/relation enters a local cell or returns toward reference.
- **Outward** = local cell expresses its resolved relation.
- **Across** = opposed/mirrored outputs establish a shared differential.
- **Over** = the resolved differential crosses the connection boundary and becomes input to the next differential stage/cluster/scale.

Earlier material calling Inward/Outward/Across/Over “Views” is superseded.

## 6. DC Choice and AC Ternary Move

The current physical split is deliberately two-layered:

```text
DC decision: EVERYTHING / NOTHING
             engage      do not engage

AC/differential decision: LEFT / STAY / RIGHT
                          -1     0      +1
```

DC decides whether the operation participates. AC/differential behavior resolves direction if participating. Zero is not a third actively driven DC command; it is the balanced/non-action directional result.

## 7. Five-State Modulation

Five coarse states remain separate from the six-step execution cycle:

```text
-2 -1 0 +1 +2
```

Floor/Low/Middle/High/Ceiling, thermal labels, matter labels and Micro/Small/Mid/Large/Macro are domain representations. Seven-band fine thresholding is also separate.

## 8. Three Physical Mirror Gates / Three Triads

Current VTC base cluster:

```text
one triad = two physically linked/opposed mirror elements
          + one differential evaluator
          = three active elements

three triads = nine-element base cluster
             = three physical Mirror Gates

3 physical Mirror Gates x 2 orientations/phases = 6 logical pair positions
```

Where practical, the opposed elements should be one complementary physical switching mechanism: one flips and its mirror flips simultaneously, rather than a processor noticing the first and issuing a second command.

## 9. Signal Flow Through a Computing Cell

Current working interpretation:

```text
signal/relation IN
 -> DC engage/nothing gate
 -> OUTWARD local expression
 -> local AC differential (-1/0/+1)
 -> ACROSS shared differential between mirrored cells
 -> OVER connection/crossover
 -> next differential
```

The two mirror cells each have signal-in and expressed differential-out. Their shared differential is itself a relation. Combined differentials feed the next identical differential interface.

### Recursive-interface rule

```text
OUTPUT relation of level n == INPUT relation expected by level n+1
```

A higher-level cluster must be substitutable for a lower-level relational node without forcing the surrounding architecture to understand its internal implementation.

## 10. Processing Is the Memory

The target architecture is **stateful compute-in-memory**, not conventional `CPU -> RAM -> CPU` traffic.

```text
cell holds physical state
 -> cell receives differential
 -> cell evaluates/changes physical state
 -> new state remains locally available
 -> neighboring differential uses that state
```

Therefore the target primitive combines:

```text
state + memory + transition/logic
```

and a cluster combines:

```text
distributed memory + distributed processing + routing
```

If magnetic remanence/other persistent physical state is used, it must be experimentally demonstrated: write, retain, non-destructively or acceptably read, rewrite, and propagate. Processing-is-memory is an architectural target until that physical behavior is measured.

## 11. Hierarchical Field/Void Processor Split

At large scale, Field and Void may be implemented as two opposed processing regions operating on the same relational interface rather than one centralized processor micromanaging all cells.

```text
             shared reference/state relation
                       (0)
                        |
             +----------+----------+
             |                     |
          FIELD                  VOID
       expression side       compression side
             |                     |
             +------ differential--+
                        |
                     routing
```

Because processing and state are co-located in the cell network, each side's working memory is primarily the persistent local state of its own cells/clusters, not a mandatory separate giant RAM bank.

A higher supervisory controller should be sparse where possible:

```text
0 = local network resolves / no intervention
1 = intervene / trigger / reroute
```

The local network retains the richer `-1/0/+1`, Direction/Phase/Strength/Reference state.

## 12. Scale Up AND Scale Down

The architecture must recurse in both directions.

Upward:

```text
local differential
 -> shared differential
 -> cluster relation
 -> cube relation
 -> cube-cluster relation
```

Downward:

```text
higher relation
 -> select/condition cube
 -> cluster
 -> triad
 -> local physical state/action
```

Most processing should remain local. Only resolved relations/events need propagate to higher levels.

## 13. Connected Cube Architecture

The long-term machine is a network of **connected cube modules**, not one indefinitely enlarged folded monolith.

The folded/stacked internal structure creates a cube module; cube-to-cube interfaces scale the machine.

Each cube should expose the same relational contract it consumes, including Direction, Phase, Strength and Reference, with physical connections arranged over the six spatial faces (`+X/-X`, `+Y/-Y`, `+Z/-Z`) as engineering permits.

The key abstraction is:

> A complete cube should be externally usable as one larger relational node.

This allows:

```text
one cube
 -> connected cubes
 -> 3 x 3 x 3 = 27-cube block
 -> blocks of blocks
```

without redesigning the logical interface at every scale.

## 14. 3-of-3 / Rubik Geometry

```text
3 elements -> triad
3 triads -> 9-element base cluster
3 cluster planes/orientations -> 27-position 3x3x3 internal volume
```

The 27 positions are not intended as 27 conventional processors. The same relational differential architecture is recursively reused.

## 15. Build Strategy: Breadboard -> Actual Microfabrication

### Immediate proof
Use the available breadboard, six-pin mechanically ganged pots, op-amps/comparators as appropriate, resistors, LEDs as indicators, 5 V supply and oscilloscope.

The six-pin pot is useful because its two sections can physically move together while being wired oppositely, approximating the linked mirror-pair requirement for the bench experiment.

First prove:

1. opposed linked response;
2. stable differential `-1 / 0 / +1` regions;
3. a resolved differential can drive/condition the next identical stage;
4. state can be retained if a magnetic-memory primitive is claimed;
5. the next stage uses the same interface rather than requiring an increasingly complex translation layer.

### Micro version
The actual micro version is **not defined as a PCB miniaturization**. The long-term target is lithographically fabricated mixed-signal/magnetic structures, potentially using thin-film magnetic or magnetoresistive elements, semiconductor differential circuitry, stacked dies/wafer bonding and vertical interconnect (TSV/hybrid bonding or future equivalent).

Conceptual progression:

```text
breadboard measured primitive
 -> thin-film/microfabricated triad test structures
 -> repeated triad test die
 -> stacked 3D die/module
 -> six-face packaged cube interface
 -> connected cube lattice
```

The first custom fabrication should be a test vehicle containing many geometry/process variants of the primitive, not an expensive million-cell final cube before the primitive is characterized.

## 16. Magnetic Differential Bench Interpretation

Known electromagnetic effects are not being re-proven. The experiment asks whether the topology integrates them into a useful relational compute primitive.

A passive pickup winding measures changing flux:

```text
V = -N dPhi/dt
```

Static remanence is not automatically a persistent DC pickup voltage. Retention must be measured with an appropriate read method.

Ideal complementary differential:

```text
(A + N) - (-A + N) = 2A
```

This gives ideal common-mode cancellation and doubled differential signal amplitude. It does not by itself prove doubled SNR, doubled speed or half power.

## 17. First Compute Target

Start with balanced-ternary arithmetic. Two operand trits each take `-1/0/+1`. A complete one-trit adder must handle all nine input combinations and produce both sum and carry where required.

Example:

```text
+1 + (-1) -> 0
```

For overflow:

```text
+1 + +1 = +2 = (+1 x 3) + (-1 x 1)
-1 + -1 = -2 = (-1 x 3) + (+1 x 1)
```

Two triads are a minimum candidate for time-shared arithmetic; three triads provide a clearer dedicated experimental cluster. Hardware determines the minimum.

One trit contains three states and therefore `log2(3) ~= 1.585` bits of information. Recursive ternary addressing does **not** make one trit equal millions of bits; `n` ternary decisions can address `3^n` endpoints. Keep information capacity separate from addressing/control reach.

## 18. Point / Path / Field

```text
Point = local relation/triad behavior
Path  = neighbor differential/routing
Field = coordinated cluster/cube behavior
```

Field, Void and Routing may be different-scale roles of the same invariant relational mechanism rather than different primitive species.

## 19. No Internal Gate 7

One complete system has six internal operations. When two complete six-operation systems establish a shared higher-order relation, the current name is **Namika**. Namika is not an internal seventh gate.

## 20. Display / I-O

A conventional display is sufficient. Translation can expose decimal/binary text while preserving balanced ternary internally. A future native state display may expose the Four Views directly:

```text
Direction
Phase
Strength
Reference
```

## 21. Validation Branches Are Not the Engine

N-body, Mercury EM, MESSENGER magnetometry, packet compression and other scientific tests remain validation branches. They must not redefine the invariant kernel.

## 22. Video Maker Goal

Separate product goal: provider-neutral AI-callable video/audio generation so multiple AI agents can use the repository's video maker as an AI-to-human communication layer. This remains independent of the VTC kernel.

## 23. Canonical Dependency Direction

```text
shared reference -(0)+
 -> invariant six-pair oscillator
 -> Views / Actions / Choices / Moves / Modulation
 -> triad physical implementation
 -> recursive differential interface
 -> processing-is-memory cluster
 -> connected cube module
 -> cube lattice / higher Field-Void split
 -> domain representations and validation branches
```

Do not reverse this dependency direction.
