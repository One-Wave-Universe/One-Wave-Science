---
node_id: "B-221a"
canonical_name: "Six-Step / Six-Gate Mirror-Action Oscillator"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Canonical architecture lock: the six process steps are the six gates; three are Mirror gates and three are Action gates"
metadata_standard: "I-06"
---

# Node B-221a: Six-Step / Six-Gate Mirror-Action Oscillator

## Canonical lock

There is **one six-position primitive** here, not several different six-count systems layered on top of one another:

```text
6 steps = 6 gates = 3 Mirror gates + 3 Action gates
```

The six positions are three consecutive Mirror/Action pairs:

```text
Gate 1  BEGIN = Mirror 1
Gate 2  BUILD = Action 1
Gate 3  HOLD  = Mirror 2
Gate 4  BUILD = Action 2
Gate 5  BREAK = Mirror 3
Gate 6  LOOP  = Action 3
                    |
                    +----> next BEGIN / Mirror 1
```

Do not create a second set of "six oscillator gates" beside the six steps. Do not insert a Mirror Gate between every step. Do not multiply three Mirror gates by two orientations to manufacture a second six-gate count. The steps and gates are the same six positions.

## Pair mapping

The existing Field/Void paired notation remains a view of those same six positions:

```text
Gate 1 / BEGIN / Mirror 1 = F1/V6
Gate 2 / BUILD / Action 1 = V5/F2
Gate 3 / HOLD  / Mirror 2 = F3/V4
Gate 4 / BUILD / Action 2 = V3/F4
Gate 5 / BREAK / Mirror 3 = F5/V2
Gate 6 / LOOP  / Action 3 = V1/F6
```

These are six **coupled pair operations**, not twelve serial instructions.

The Mirror positions read/compare/reflect the opposed relation through the shared reference. The Action positions change/carry the resolved relation forward. Each Action becomes part of what the next Mirror gate reads.

## Six-step recurrence

```text
Mirror 1 / BEGIN
 -> Action 1 / BUILD
 -> Mirror 2 / HOLD
 -> Action 2 / BUILD
 -> Mirror 3 / BREAK
 -> Action 3 / LOOP
 -> Mirror 1 / next BEGIN
```

`BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP` therefore names the behavior of the same six gate positions. G-739 may measure whether a trajectory actually satisfies the expected behavior at a position, but it may not redefine those behaviors as a separate gate set.

## Relationship to the Three Moves and Six Routes

The six-gate oscillator is not the route address space.

Current executable authority in `UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md` defines a separate combinatorial address space:

```text
2 binary choices x 3 ternary moves = 6 route addresses
```

with ternary movement:

```text
DOWN / HOLD / UP = -1 / 0 / +1
```

That route count may label routing possibilities, but it does not add six more physical/logical gates. The primitive gate cycle remains exactly three Mirror gates plus three Action gates.

## Relationship to Views and Actions

Any four-view or four-action vocabulary used by a higher routing layer is a **projection/readout vocabulary**, not the primitive gate count. It must not replace the three Action gates or create extra gates.

The primitive distinction is:

```text
Mirror gate = read / compare / reflect through reference
Action gate = act / carry / change the relation
```

Higher-order views may describe what a Mirror gate sees. Higher-order action labels may describe what an Action gate does. They do not alter `3 Mirror + 3 Action = 6 gates`.

## Relationship to Five-State Self Lifecycle

The five-state self lifecycle is separately defined by `Nodes/G-742_Nonverbal_Loop_Continuity_and_Language_Adapter.md`:

```text
IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING
```

These behavioral lifecycle states are independent of the six gate positions.

## Relationship to Five Commitment/Readout States

Updated 43 owns the current downstream five-state commitment/readout interpretation. Those states are readouts downstream of the gate cycle; they are not additional gates.

Older neutral `-2,-1,0,+1,+2` modulation notation remains compatibility shorthand only.

## Scale boundary

Scale labels such as `Micro / Small / Medium / Large / Macro` are not aliases for lifecycle, commitment, route, or gate state. A scale mapping must be declared by the domain or derivation that uses it.

## Anti-drift audit

A description fails this node if it does any of the following:

- treats the six steps and six gates as separate structures;
- counts six Mirror crossovers in addition to the six steps;
- says three Mirror gates traversed twice *are* the six gates;
- promotes four-view/four-action vocabulary into extra primitive gates;
- turns six route addresses into six additional gates;
- changes the primitive count away from exactly three Mirror gates and three Action gates.

Canonical primitive:

```text
3 Mirror gates + 3 Action gates = 6 gates = 6 steps
```
