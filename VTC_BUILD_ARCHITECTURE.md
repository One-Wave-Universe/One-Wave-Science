# VTC Build Architecture — Triads, Three Mirror Gates, and 2D Vascular Folding

**Status:** Implementation architecture / physical bench program. Material performance claims remain experimental.

## 1. Core Physical Primitive

The current VTC hardware primitive is a **triad**:

```text
linked mirror element A
          \
           > differential evaluator
          /
linked mirror element -A
```

The two mirror elements are intended to be physically/electromagnetically constrained as one complementary switching mechanism: when one orientation flips, the opposed orientation flips with it. The architecture does **not** require an external processor to detect one flip and command the other.

The third element reads the relation between the two sides around a shared reference.

Ideal differential:

```text
Delta = A - (-A) = 2A
```

Real hardware must measure mirror mismatch, common-mode rejection, independent noise, hysteresis, and a finite zero window. Signal doubling does not automatically imply 2x SNR, 2x switching speed, or half power.

## 2. DC Engagement and AC/Ternary Resolution

The physical decision architecture separates two layers:

```text
DC: EVERYTHING / NOTHING
AC differential: LEFT / STAY / RIGHT
```

- **EVERYTHING** = engage the local operation.
- **NOTHING** = no active assertion; driver may enter high-Z after transients.
- **LEFT / STAY / RIGHT** = `-1 / 0 / +1` differential result around the local reference.

The ternary result is one relational reading, not three independent stored physical objects.

`0` is non-action/hold at the directional layer. It must not be implemented as a third actively powered polarity command.

## 3. Three Triads Make One Cluster

The current architecture has **three physical Mirror Gates**, not six separate physical gates.

```text
3 physical Mirror Gates x 2 orientations/phases = 6 logical pair positions
```

Therefore one basic cluster is:

```text
3 triads x 3 active elements = 9 active elements
```

Conceptual flat arrangement:

```text
        TRIAD A          TRIAD B          TRIAD C
       [A / -A]         [B / -B]         [C / -C]
           |                 |                 |
       evaluator         evaluator         evaluator
           |                 |                 |
=========== continuous shared reference / vascular spine ===========
```

The six logical pair positions remain:

```text
F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6
```

The second three logical positions are the opposite traversal/orientation of the same three physical Mirror-Gate structures, not three additional physical Mirror Gates.

## 4. Recursive 3-of-3 Geometry

The hardware scales by reusing the same relation:

```text
3 elements -> one triad
3 triads   -> one 9-element cluster
3 cluster planes/orientations -> 27-position volumetric structure
```

This produces a Rubik-like `3 x 3 x 3` volume without treating the 27 positions as 27 independent conventional processors.

At higher levels, the resolved outputs of two lower relations can be treated as the opposed inputs of another differential relation. The mechanism is recursively reused rather than replaced by a new gate type.

## 5. 2D Vascular Fabrication First

The preferred construction path is **fabricate flat, then fold**.

The 2D sheet carries continuous vascular paths for:

- shared reference;
- drive/power distribution;
- return;
- differential sense;
- routing/phase paths;
- optional later thermal/fluid channels.

Rigid magnetic cores, switching mechanisms, and components stay away from hinge lines. Fold zones carry only bend-tolerant traces/channels.

```text
flat sheet:
[ TRIAD A ]====flex hinge====[ TRIAD B ]====flex hinge====[ TRIAD C ]
```

Folding changes spatial topology while preserving the already-existing electrical/reference relation. Folding does not create the reference.

## 6. Build Ladder

### VTC-F0 — Single Flat Triad

Bench-scale, oversized, fully probeable.

Measure:

- complementary flip fidelity;
- differential response;
- zero/hold window;
- transition timing;
- hysteresis/retention where applicable;
- write/read energy;
- behavior after driver release.

### VTC-F1 — Three Triads on One Continuous Sheet

Nine active elements and three physical Mirror Gates on one shared reference spine.

Measure:

- propagation skew;
- triad-to-triad routing;
- intentional coupling versus unwanted crosstalk;
- whether the six logical pair orientations can be traversed using three physical gates.

### VTC-F2 — Folded Three-Orientation Cluster

Fold the same vascular sheet into three spatial orientations while keeping the reference and routing paths continuous.

Verify that folding does not materially change the flat-sheet logic behavior.

### VTC-F3 — 27-Position Rubik Volume

Combine three 9-position structures/orientations into a `3 x 3 x 3` volumetric relation.

Only after F0-F2 pass should density, shielding, cooling, or high-count loop targets be treated as engineering specifications.

## 7. Center-Tapped Magnetic Bench Geometry

A center-tapped sense winding is a useful measurement geometry, but the pickup winding measures changing flux:

```text
V_sense = -N dPhi/dt
```

Static remanence does not appear as a persistent DC sense voltage. Use standardized read excitation, transient integration, hysteresis measurements, or appropriate magnetic sensing to infer retained magnetic history.

Useful measurements:

```text
left relative to center
right relative to center
common component       = (L + R)/2
differential component = (L - R)/2
integrated sense response -> inferred flux change/history
```

Bench oscilloscope ground clips are commonly tied together and to earth. Do not connect them blindly to a +2.5 V virtual reference. Use a grounding arrangement, isolated supply, or differential measurement method appropriate to the actual scope.

## 8. Reference at Every Step

The reference is not a decorative global ground. Every recursive read is relational:

```text
local mirrored elements
 -> triad reference
 -> cluster reference
 -> folded/field reference
 -> higher-system reference
```

No layer should interpret an absolute state without carrying the local reference that gives the state meaning.

## 9. Point / Path / Field as Scale Representation

Do not hard-code Point/Path/Field into the primitive switching mechanism.

A useful implementation mapping is:

```text
Point = local triad/differential behavior
Path  = neighbor/triad-to-triad coupling and routing
Field = coordinated state of the complete cluster/lattice
```

Each scale may carry Carrier / Breathing / Phase as a representation of its oscillatory behavior.

## 10. First Compute Target

The first computation should be simple balanced-ternary arithmetic, not a full application.

Bench input:

```text
-1 / 0 / +1 operands
```

Bench output:

```text
sum trit
carry trit where required
```

A strong first demonstration is:

```text
+1 + (-1) -> 0
```

where the zero result emerges from the opposed differential relation.

Full one-trit addition must also handle `+2` and `-2` via balanced-ternary carry; ternary does not eliminate carry.

Two triads may be sufficient for a minimum time-shared arithmetic experiment. Three triads provide a clearer dedicated cluster for input/routing/result experiments. The required count must be determined by the physical timing/routing test rather than assumed.

## 11. External Electronics Are Test Harness, Not Core Processor

Oscilloscopes, function generators, MOSFET drivers, ADCs, conventional microcontrollers, Jetson boards, or FPGAs may be used to stimulate, measure, log, or translate the experimental hardware.

They are **not** the intended cognitive/compute core. The VTC architecture must not depend on an external binary processor to enforce every mirror flip or compute every ternary relation.

## 12. Processing Is the Memory

The target VTC does not separate processor and RAM in the conventional sense.

```text
cell physical state = stored state
incoming differential = operation/input
state transition = computation
new retained state = result + memory
```

The same local structure is therefore intended to provide:

```text
memory + processing + routing
```

A cluster is a distributed state machine whose current physical configuration is its working memory. There is no mandatory fetch-compute-writeback loop through a separate main RAM array.

This is an architectural target, not yet a proven magnetic-memory claim. The bench program must demonstrate that the chosen physical element can be written, retain a distinguishable state, be read with acceptable disturbance, be rewritten, and pass its consequence into the next differential stage.

## 13. Four Views and Four Actions at the Hardware Interface

Every scale should expose the same four state views:

```text
Direction
Phase
Strength
Reference
```

and the same four relational actions:

```text
Inward  = receive/return into the local relation
Outward = express the locally resolved state
Across  = form the shared differential with the opposed peer
Over    = cross the connection boundary into the next differential/scale
```

The interface must remain invariant when a single triad is replaced by a cluster or a cluster is replaced by a cube.

## 14. Connected Cube Scaling

The intended machine scales as connected modules, not as one indefinitely enlarged monolith.

```text
triad
 -> 9-element cluster
 -> folded/stacked cube module
 -> face-connected cubes
 -> 3 x 3 x 3 = 27-cube block
 -> blocks of blocks
```

A cube should expose matched relational ports on its six spatial faces where engineering permits:

```text
+X / -X
+Y / -Y
+Z / -Z
shared/local reference
```

The critical recursion test is:

> A complete cube must be externally usable as one larger relational node.

Scaling must work both upward and downward. Local relations combine into cluster/cube relations; higher relations must be able to condition/select lower cubes, clusters and triads without changing the interface contract.

## 15. Field/Void at Processor Scale

At large scale, Field and Void are not intended to become two conventional CPUs with separate external RAM banks. They may be two opposed regions of the same stateful compute-in-memory network.

```text
             shared reference / relation
                       (0)
                        |
             +----------+----------+
             |                     |
          FIELD                  VOID
      expressive region      compressive region
             |                     |
             +------ differential--+
                        |
                     routing
```

Each side's working memory is primarily the persistent state of its own cells/clusters. A sparse higher controller may only need an intervention decision (`0 = leave local resolution alone`, `1 = intervene/trigger/reroute`) while the local network retains the richer `-1/0/+1` state plus Direction/Phase/Strength/Reference.

## 16. Anti-Drift Rule

The material implementation may change while the relational architecture survives.

If ferrite, nanocrystalline material, folded substrate geometry, mechanical linkage, sensing method, thin-film magnetic structures, or stacked-die implementation changes, the invariant six-pair logical timing and relational read architecture should remain independently testable.
