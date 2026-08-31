# Field / Void / Loop Build Ladder

Status: ACTIVE build-consolidation contract.

This file turns the existing architecture documents into four clear build tracks:

1. Field build
2. Void build
3. Loop programming build
4. Loop hardware build

Every track advances through the same five construction scales:

`Micro -> Small -> Mid -> Large -> Macro`

The runtime loop then returns through scale:

`Macro -> Large -> Mid -> Small -> Micro`

The scale ladder is a construction/delegation rule. It is not the five-state lifecycle, six-route address, or six oscillator gates.

## 1. Shared non-negotiable loop

Current loop-direction contract:

```text
compression / inward route
Micro -> Small -> Mid -> Large -> Macro
                              |
                           MIRROR
                              |
                           RELEASE
                              |
expression / return route
Large -> Mid -> Small -> Micro
                              |
                            PHASE
                              |
                    next compression
```

Expression returns through the same route that compression used, in reverse order. The mirror is the turnaround. Release occurs at that turnaround. Phase is retained before the next compression cycle.

Do not turn compression and expression into unrelated branches.

Do not confuse loop-phase `COMPRESS / EXPRESS` with the identities of Field and Void. Field and Void remain distinct processing roles throughout the loop.

## 2. Shared build rule

Field and Void do **not** get separate incompatible engines.

They share:

- one parser grammar;
- one scale vocabulary;
- one lifecycle vocabulary;
- one receipt format;
- one loop-order validator;
- one exact replay mechanism.

They differ by role, authority, and the packets they are allowed to originate or commit.

This prevents a Field implementation and a Void implementation from drifting into two machines that only share names.

## 3. Field build ladder

Field owns possibility and expression. It may propose, associate, simulate, rehearse, and generate alternatives. It does not commit its own proposal as authority.

### Field Micro

Build:
- parse exact Field input packet;
- retain source/cue, route, phase, scale, and reference;
- create one bounded candidate without changing the source anchor.

Acceptance:
- malformed packet rejected;
- candidate has explicit provenance;
- Field cannot mark its own candidate committed.

### Field Small

Build:
- bounded local candidate constructor;
- alternative candidate IDs and expiry;
- one local associative relation.

Acceptance:
- at least two alternatives can remain distinct;
- no silent merge of conflicting candidates;
- local construction cannot expand its own scope.

### Field Mid

Build:
- M4-facing candidate packet;
- route/scale/phase handoff;
- constellation-neighborhood access without archive authority.

Acceptance:
- M4 may change priority/timing but not candidate meaning;
- route receipt survives handoff;
- stale candidate is detectable.

### Field Large

Build:
- bounded Dream/Field generator;
- counterfactual/simulation path;
- uncertain Boltzmann-style fill remains explicitly generated/uncertain.

Acceptance:
- proposal and remembered fact remain distinguishable;
- generated fill cannot silently enter authoritative memory;
- alternate solutions can be compared without self-approval.

### Field Macro

Build:
- complete Field/Dream hemisphere interface to M4 and Void;
- receives correction/consequence and creates the next candidate field.

Acceptance:
- repeated cycles do not self-commit;
- rejection retains enough context to produce a corrected proposal;
- Field can be ablated and produce a characteristic loss of possibility generation rather than total state corruption.

## 4. Void build ladder

Void owns reference, continuity, comparison, permission, contradiction checks, rollback, and commitment. It does not invent a replacement candidate and pretend Field proposed it.

### Void Micro

Build:
- exact reference/provenance validator;
- deterministic packet/schema checks;
- immutable receipt verification.

Acceptance:
- malformed or provenance-free input rejected;
- source anchor cannot be silently rewritten.

### Void Small

Build:
- explicit `CONFIRM / DEFER / DENY` decision;
- Defer remains different from Deny;
- no decision without a reason/receipt.

Acceptance:
- same input/reference gives deterministic decision where the rule is deterministic;
- Deny and Defer produce different output states.

### Void Mid

Build:
- M4-facing oversight/override packets;
- rollback and receipt-chain checks;
- stale-reference detection.

Acceptance:
- M4 can carry authority but cannot originate it;
- override points back to a Void decision;
- broken receipt chain fails loudly.

### Void Large

Build:
- accepted-memory/reference authority;
- conflict and uncertainty checks on associative/generative rebuilds;
- consequence incorporation rule.

Acceptance:
- uncertain generated content cannot become exact memory without an explicit commit;
- archive and fast recall cannot silently diverge.

### Void Macro

Build:
- Administrator/Void final-say interface;
- final commitment back through M4 to execution;
- next Reference Ground update from justified consequence.

Acceptance:
- Void cannot regenerate Field candidates;
- authority survives the full up/down loop;
- rollback reconstructs why a commitment occurred.

## 5. Loop programming build ladder

### Programming Micro — NOW EXECUTABLE

Owner:
- `One_Wave_Bench/brain/loop_state_machine.py`

Build:
- deterministic line parser;
- Field/Void build profile lock;
- five-state lifecycle validator;
- exact scale-order validator;
- mirror/release/return-path validator;
- append-only SHA-256 digest-chained event receipts;
- deterministic replay/rebuild of active process state and simple key/value process memory.

Current grammar:

```text
PROFILE FIELD|VOID
STATE IDLE|PRIMED|EXECUTING|VECTORING|RESOLVING
COMPRESS MICRO|SMALL|MID|LARGE|MACRO
MIRROR
RELEASE
EXPRESS LARGE|MID|SMALL|MICRO
PHASE
REMEMBER <key> <value...>
FORGET <key>
```

Acceptance:
- same parsed input produces same canonical event;
- invalid lifecycle transition rejected;
- compression must rise Micro->Macro;
- release cannot skip mirror;
- expression must return Large->Mid->Small->Micro;
- Macro is not repeated on the expression leg;
- corrupt or reordered receipt chain rejected;
- replay restores exactly the same process state and memory.

### Programming Small

Build:
- adapters from the shared core into existing `command_memory.py` and other bounded consumers;
- Field and Void packet schemas around the same event core.

Acceptance:
- command-specific vocabulary does not leak into shared parser/FSM;
- Field/Void profile provenance survives adapter round-trip;
- old command-memory tests remain green.

### Programming Mid

Build:
- connect the shared core to `M4DualStateRouter`;
- scheduler receipts for upward Views and downward Actions;
- explicit timing/phase order.

Acceptance:
- Field proposal -> M4 -> Void decision -> M4 -> result is traceable end to end;
- M4 cannot commit;
- stale cycles and mismatched receipt IDs are rejected.

### Programming Large

Build the two memory tiers together without collapsing them:

**Tier A — exact rebuild**
- digest-chained event/archive replay;
- reconstruct exact accepted process state.

**Tier B — associative rebuild**
- constellation neighborhood;
- reversible rabbit-hop route;
- Hopfield-style completion;
- Boltzmann-style fill only when ambiguity remains;
- uncertainty and provenance retained.

Acceptance:
- remove part of a stored memory and rebuild from a partial cue;
- compare against no-constellation/no-rabbit-hop baseline;
- nearby distinct memory does not collapse into the target;
- generated fill is visibly uncertain;
- exact receipt history remains unchanged.

### Programming Macro

Build:
- Reference Ground;
- simulated Views up;
- M4 fast routing/recall;
- Field alternatives;
- Void Confirm/Defer/Deny;
- committed Action down;
- simulated consequence;
- prediction error;
- next reference update;
- complete replay receipt.

Acceptance:
- repeated end-to-end cycles with no role collapse, provenance loss, silent memory rewrite, or expression-path drift.

## 6. Loop hardware build ladder

Hardware must be measured as hardware. Mechanical or magnetic analogies do not count as proof of the full architecture.

### Hardware Micro

Build:
- low-voltage center-referenced differential cell;
- two opposed channels around one measured reference;
- instrument voltage/current/state before adding higher layers.

Acceptance:
- stable reference is measured;
- both opposed channel states and Hold are distinguishable;
- state/transition is reproducible rather than touch/noise dependent.

### Hardware Small

Build:
- one reversible physical closure/opening path;
- compression drives inward through one linkage/path;
- stored tension/release returns through that same mechanical path;
- displacement or angle sensor records the route.

A circular iris-like enclosure is a candidate mechanism, not a required ontology. If magnets actuate it, measure actual displacement/force/hysteresis. Do not infer atomic-lattice compression or expansion merely from pole labels.

Acceptance:
- closure and opening traces are recorded;
- return order is the reverse of compression order;
- release threshold and hysteresis are measurable.

### Hardware Mid

Build:
- couple the center-referenced cell to the candidate AC/ternary or three-winding local controller;
- preserve phase and Hold;
- read Direction / Phase / Strength / Reference upward.

Acceptance:
- six logical routes map to measured states without an arbitrary hidden lookup that invents extra states;
- Hold remains physically distinguishable;
- phase receipt survives a complete cycle.

### Hardware Large

Build:
- paired Field/Void processing regions around shared reference;
- M4-compatible sensor/view packet upward;
- approved action packet downward;
- local state retained long enough to test processing-is-memory behavior.

Acceptance:
- Field/Void physical provenance is not lost;
- one side cannot silently act as both proposal and authority;
- local state can be read before/after a transition.

### Hardware Macro

Build:
- multi-module recursive assembly;
- completed lower module exposed as one bounded node to the next scale;
- consequence returned to the software/brain loop.

Acceptance:
- interface stays the same when scale increases;
- timing and state survive module composition;
- measured hardware receipt can be paired with the software receipt for the same cycle.

## 7. Memory consolidation rule

Do not use associative memory as the exact archive.

```text
EXACT HISTORY
append-only receipts
-> deterministic replay
-> accepted process/reference state

RECONSTRUCTIVE MEMORY
partial cue
-> constellation
-> rabbit-hop route
-> associative completion
-> uncertain generative fill if needed
-> Void/context validation
```

The exact history answers: **what actually happened in this machine?**

The reconstructive tier answers: **what missing relational content can be recovered from a partial cue?**

Keeping them separate gives the rebuild system a ground truth for testing.

## 8. Immediate attack order

1. Keep the Micro parser/FSM/replay core green.
2. Adapt `command_memory.py` to consume the shared core without changing its command behavior.
3. Freeze one Field packet and one Void packet schema.
4. Build the destructive memory-rebuild benchmark from the existing constellation architecture.
5. Only then attach the same event/receipt contract to a measured hardware Micro loop.

Do not jump to Macro while a lower-scale interface is still undefined.

## 9. Evidence required at every scale

Every build must report:

```text
owner
purpose
inputs
outputs
allowed dependencies
forbidden leaks
observable trace
acceptance tests
receipt/evidence
highest-risk dependency
next falsifier
```

Nodes say what a thing means.
Build contracts say what it may do.
Tests say whether the implementation behaves as specified.
Measurements say whether the physical implementation matches the model.
