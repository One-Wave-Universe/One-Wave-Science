# ALGORYTHM-ZERO THREE-GATE CORRECTION

This file is a canonical correction note for Algorythm-Zer0. It does not replace the full primitive; it locks the current three-gate body/control interpretation without collapsing separate axes.

## Core counts

```text
3 MIRROR GATES
6 ADDRESS / STEP SIDES
3 MOVES
1 SHARED CENTER / REFERENCE
```

Do not convert six steps into six gates. Do not convert six addresses into six movement states.

## Three moves

```text
SIDE A  <->  CENTER / HOLD  <->  SIDE B
 -1              0                +1
```

The center/reference is active balance. Two opposed oscillations swing away from and back through the same center reference.

## Gate 1 — Binary Field / Void swing

Purpose in the body/hardware mapping:

```text
SENSOR READINGS + POWER / REINJECTION STATE
        ↓
COMPARE TO LOCAL REFERENCE / THRESHOLD
        ↓
BELOW THRESHOLD
= remain local / do not signal upward

ABOVE THRESHOLD
= commit the Field / Void relation and propagate
```

Binary establishes the opposed Field / Void relation and acts as the first significance / engagement filter.

In the hardware simplification, body-energy state may be represented by battery level and present power conditions.

Minimum retained power variables:

```text
battery_level
power_draw
power_reinjection_or_recovery
estimated_remaining_capacity
sustainable_now = yes / no
```

The control question is:

```text
IS CURRENT ENERGY USE SUSTAINABLE
AT THE PRESENT ACTION / POWER LEVEL?
```

## Gate 2 — Ternary Field / Void swing

Purpose in the body/nerve mapping:

```text
MOVE ONE WAY
HOLD / BALANCE
MOVE THE OTHER WAY
```

This is the fast nerve/body reflex layer.

It carries automatic body-state decisions such as:

```text
reflex correction
balance
motor stabilization
automatic movement adjustment
body-state condition
energy expenditure state
feelings / valence mapping
current sense-of-self / continuing body state
```

For the simplified hardware-energy mapping:

```text
SPEND / HOLD / CONSERVE
```

or equivalently, when mapped to signed control:

```text
INCREASE / HOLD / DECREASE
```

These are domain mappings of the same ternary movement primitive; they do not create additional primitive moves.

## Gate 3 — Quadratic Field / Void swing

Quadratic means:

```text
VIEWS UP
ACTIONS DOWN
```

It is the body-state integration gate.

It settles:

```text
current nerve / body state
+ retained body memory
+ automatic decisions already happening
+ significant sensory information
+ present energy sustainability state
+ oversight / override
+ last action state
        ↓
NEW VIEWS UP
LAST / UPDATED ACTIONS DOWN
        ↓
CURRENT BODY MEMORY-ACTION STATE
```

Views Up are not identical to raw sensor readings. Raw sensing can be filtered earlier by the binary threshold gate. Views Up are the settled higher-level representation produced after current body state and oversight/override are reconciled.

Actions Down are not required to be a wholly new command. They can carry, continue, modulate, hold, reduce, or override the current/last action state.

## Body-state / self mapping

In the neural/body domain, the continuing body state can include:

```text
nerve state
sensor consequence
reflex state
energy state
fatigue / reserve mapping
internal condition
last action
retained body memory
oversight / override result
```

The sense-of-self mapping is the continuously retained and updated body/nerve state, not a separate mandatory primitive module.

## Energy simplification

For the prototype, use battery state instead of trying to model stomach, glucose, hormones, liver, fat stores, and other biological energy systems directly.

```text
BATTERY / ENERGY STATE
        ↓
BINARY
enough / significant enough to engage?
        ↓
TERNARY
SPEND / HOLD / CONSERVE
        ↓
QUADRATIC
VIEWS UP / ACTIONS DOWN
        ↓
UPDATED BODY MEMORY-ACTION STATE
        ↺
```

A minimal energy trend model can be implemented as:

```text
energy_change = input_or_recovery + reinjection - usage
```

Interpretation:

```text
energy_change > 0
= reserve building

energy_change ≈ 0
= present use approximately sustainable

energy_change < 0
= reserve depleting
```

Sustainability must also consider remaining battery reserve and required action duration. Instantaneous balance alone is not sufficient.

## Oversight / override fusion

The ternary body/reflex process and the higher oversight/override process are coupled.

```text
FAST BODY / NERVE STATE
        ↕
OVERSIGHT / OVERRIDE
        ↓
QUADRATIC SETTLEMENT
        ↑ VIEWS UP
        ↓ ACTIONS DOWN
        ↓
CURRENT BODY MEMORY-ACTION STATE
```

The resulting state becomes part of the next reference and next control pass.

## Primitive versus domain mapping

Keep these distinctions explicit.

Universal primitive candidates:

```text
shared reference
Field / Void opposition
binary commitment relation
ternary movement around reference
Views Up / Actions Down
retained processing-memory
oversight / override
recursive result-to-reference loop
```

Body / hardware domain mappings:

```text
sensor threshold behavior
power reinjection
battery level
energy sustainability
motor reflex control
nerve/body state
feelings / sense-of-self mapping
specific actuator behavior
```

These mappings implement the primitive. They do not redefine the universal primitive unless separately demonstrated and adopted.

## Anti-drift rules

```text
3 MIRROR GATES != 6 GATES
6 STEPS / SIDES != 6 MOVES
3 MOVES = -1 / 0 / +1
CENTER / REFERENCE IS ACTIVE
BINARY != TERNARY != QUADRATIC
QUADRATIC = VIEWS UP / ACTIONS DOWN
RAW SENSOR READINGS != SETTLED VIEWS UP
BODY ENERGY MAPPING != UNIVERSAL PHYSICAL LAW
BATTERY LEVEL IS THE CURRENT PROTOTYPE ENERGY ABSTRACTION
```
