# One-Wave Machine Design Target

**Status:** architectural target; not a claim of completed hardware

**Purpose:** define what the machine/cell architecture is trying to become so later work can be tested against one stable target instead of being reinvented.

---

## 1. Core target

Build a machine from **simple repeatable cells and local control rules** that can combine into larger functional structures while preserving:

- shared reference;
- retained local state;
- local sensing and reflex control;
- Views Up / Actions Down coordination;
- shared recoverable-energy circulation;
- stress escalation before failure;
- adaptive capacity based on repeated need;
- modular growth by adding compatible cells/modules only where useful.

The design goal is not to reproduce biological anatomy part-for-part. It is to copy useful biological control principles with fewer, simpler, measurable machine functions.

---

## 2. Primitive cell target

A useful primitive cell should eventually expose the smallest practical set of functions:

```text
REFERENCE
STATE / MEMORY
INPUT
OUTPUT
LOCAL ENERGY ACCESS
STRESS SENSING
NEIGHBOR CONNECTION
VIEW UP
ACTION DOWN
REINJECTION
```

Not every physical cell must contain every final-system function at full scale. Specialization may emerge from position, connection, retained state, or assigned role.

---

## 3. Need-driven growth / machine hypertrophy

Long-range target:

```text
REPEATED USE
    |
    v
RETAINED DEMAND HISTORY
    |
    v
LOCAL STRESS / LOAD TREND
    |
    v
IS CURRENT CAPACITY ENOUGH?
   / \
 YES  NO
 |     |
HOLD  VIEW UP / REQUEST CAPACITY
       |
       v
ADD / REASSIGN LOCAL CELL OR MODULE
       |
       v
TEST AGAIN UNDER REAL LOAD
       |
       v
STOP GROWING WHEN REQUIRED MARGIN EXISTS
```

The machine analogue of growing muscle is **capacity following demonstrated repeated demand**.

The target is not unlimited growth. The target is:

```text
JUST ENOUGH CAPACITY
+
REQUIRED SAFETY / TRANSIENT MARGIN
-
UNUSED EXCESS HARDWARE
```

A structure should not gain extra modules merely because space or parts are available. Repeated measured need should justify expansion.

---

## 4. Use strengthens; disuse should not force permanent excess

Working architectural principle:

```text
repeated useful path
-> stronger / easier / more available path

persistent local overload
-> request more capacity

capacity repeatedly unused
-> stop allocating new capacity there
-> optionally reassign modular resources if the hardware allows it
```

This separates two kinds of adaptation:

1. **State adaptation:** the same physical path changes its retained state through use.
2. **Structural adaptation:** repeated demand eventually justifies adding or reassigning physical capacity.

Do not confuse the two. Brain Cell V1 is testing state adaptation first. Structural growth comes later.

---

## 5. Growth should be local first

A local unit should solve what it can locally before asking for more structure.

```text
NORMAL LOAD
-> local loop handles it

REPEATED ELEVATED LOAD
-> local retained state records the pattern

PERSISTENT CAPACITY SHORTAGE
-> View Up

HIGHER AUTHORITY
-> decide whether to:
   - add capacity
   - reassign capacity
   - reduce demand
   - route work elsewhere
   - change timing
```

This prevents every temporary spike from causing permanent growth.

---

## 6. Stress is useful information

Machine stress is measured, not guessed.

Candidate signals:

```text
current
voltage deviation
temperature
load / torque
position error
repeated correction count
energy demand
shared-bus pressure
storage state
reinjection saturation
latency / response time
```

Working interpretation:

```text
small transient stress
-> correct locally

repeated manageable stress
-> learn / adapt state

persistent near-capacity stress
-> View Up / request more capacity or less demand

hard safety limit
-> immediate local protection
```

The architecture should respond **before damage**, analogous to biological fatigue/exhaustion signaling that continuing demand is becoming expensive.

---

## 7. Shared energy target

The machine should treat recoverable energy as a system resource.

```text
LOCAL UNIT RETURNS ENERGY
        |
        v
SHARED ENERGY / REINJECTION BUS
   /          |           \
  v           v            v
OTHER LOAD   STORAGE    NEXT DRIVE EVENT
```

Each active unit uses controlled bidirectional gating to take or return energy.

Design target:

```text
RECOVERABLE ENERGY
-> reinject / redistribute / store

UNAVOIDABLE LOSS
-> measure and minimize

INTENTIONAL DUMPING
-> use only when protection requires it
```

The quiet measurement/reference node remains electrically separate from the high-current shared energy bus unless a later measured circuit proves a safe combined topology.

---

## 8. Biological principles translated into simpler machine functions

```text
BIOLOGICAL PRINCIPLE          MACHINE TARGET
---------------------------------------------------------------
reflex                       fast local control
muscle memory                retained stateful path
fatigue / burn               local stress signal
brain coordination           Views Up / Actions Down
circulation                  shared energy distribution
metabolic allocation         power/storage allocation
growing muscle               repeated-need capacity growth
atrophy / disuse             stop allocating unused capacity
homeostasis                  regulate around shared references
specialization               cells/modules take roles by need/location
```

This table is an architectural analogy, not evidence that the machine already reproduces biological mechanisms.

---

## 9. Minimal-material principle

The long-range machine should aim for **function from organization and reuse**, rather than solving every task by permanently adding dedicated parts.

Priority order:

```text
1. reuse existing state/path
2. reroute existing capacity
3. share energy/resources
4. change timing/control
5. add physical capacity only when repeated measured need remains
```

This is the design meaning of:

```text
NO EXCESS WASTED EXTRA PARTS
```

It does **not** mean removing safety margin, protection, redundancy required for reliability, or components whose losses are physically unavoidable.

---

## 10. Growth must remain bounded

Any future self-expanding architecture needs limits.

A growth decision should require at least:

```text
repeated demand
+
persistent measurable shortage
+
available energy/material/module
+
higher-level authorization or bounded local rule
+
post-growth validation
```

After adding capacity:

```text
add one unit/change
-> test immediately
-> compare with active need
-> measure stress reduction
-> keep only if it solves the shortage
```

Do not recursively add hardware because the previous addition failed. After repeated failure, change the design angle rather than accumulating parts.

---

## 11. Current system hierarchy target

```text
BRAIN CELL
analog processing + retained path state
        |
        v
PATHWAY / LOCAL CLUSTER
neighbor routing and local aggregation
        |
        v
M4 / QUADRATIC
Views Up / Actions Down
        |
        v
ACTION-DOWN STATE
current candidate: spintronic state/command
        |
        v
TERNARY MOTOR UNIT
A / B / C three-winding control
        |
        v
MOTOR / ACTUATOR
        |
        +---- sensor/stress feedback ----> View Up
        |
        +---- recoverable energy --------> shared reinjection bus
```

Repeated need may eventually change **how much capacity exists at a level**, but it must not silently change what the levels mean.

---

## 12. Development order

Do not attempt autonomous growth before proving the primitives.

```text
1. Brain Cell V1: repeated use changes retained analog state.
2. Binary threshold: local vs View-Up escalation.
3. Action Down V1: state/command can drive a separate power gate.
4. One ternary three-winding motor unit.
5. Shared regenerative/reinjection energy bus.
6. Local stress sensing and higher-authority slowdown/redistribution.
7. Two or more cells/modules sharing load and energy.
8. Demonstrate need-driven reassignment using existing capacity.
9. Demonstrate one bounded physical capacity addition triggered by repeated measured need.
10. Test whether added capacity reduces stress enough to justify keeping it.
```

Only after these pass should autonomous structural growth be described as demonstrated.

---

## 13. Success criterion

The long-range target is a machine where:

```text
USE SHAPES STATE
STATE SHAPES NEXT USE
STRESS REQUESTS HELP
HIGHER LEVELS COORDINATE
ENERGY IS RECIRCULATED WHERE PRACTICAL
CAPACITY FOLLOWS REPEATED NEED
GROWTH STOPS WHEN THE NEED IS SATISFIED
```

In plain language:

**Build only what the system repeatedly proves it needs, place that capacity where it is needed, reuse what already exists first, and avoid permanent excess that does no useful work.**
