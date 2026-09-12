# Locked Cell Topology: DC, AC, Virtual Ground, and Three Mirrored Gates

## Status

**LOCKED CONCEPTUAL TOPOLOGY** — this document records the current One-Wave cell build contract. It is a design specification and simulation hypothesis. It does not claim that the proposed gravity or lattice interpretation is established physics.

## 1. Rail order and DC start

The cell begins as three parallel rails ordered left to right:

```text
forward DC                                             backward DC
    →                                                       ←

    + rail                 0 rail / virtual ground          - rail
    ─────────────────      ───────────────────────      ─────────────────
```

Invariant:

```text
→  +  |  0  |  -  ←
```

- The positive rail begins at the left side of the controller/source region and carries the forward DC orientation.
- The negative rail begins at the right side of the controller/source region and carries the mirrored backward DC orientation.
- The virtual-ground rail is physically and logically in the middle.
- The center rail is a live reference, not passive earth ground, an output wire, or a Y-junction branch.

## 2. Center interaction

The rails do not merge into a Y. The center is a three-rail interaction/crossing region:

```text
+  ↔  0  ↔  -
```

The outer rail states oscillate bidirectionally with respect to the middle virtual-ground rail. Each swing can cross the center reference, enter mirrored territory, and return. The middle rail is the return/reference path.

The virtual ground carries the resolved center condition back toward the rail-origin/controller region. There is no forward output beyond the center.

```text
controller / rail origins  →  three-rail interaction  →  center event
controller / rail origins  ←  virtual-ground return   ←  center event
```

## 3. Bidirectional double oscillation

The central event is a time-dependent double oscillation around reference zero, not a static comparison:

```text
0 → +1 → 0 → -1 → 0
0 → -1 → 0 → +1 → 0
```

The two mirrored swings may carry different phase, amplitude, persistence, and RC history. The local ternary result is emitted only after the center window resolves.

```text
-1  = negative-side differential persisted through the center window
 0  = counter-oscillation reclosed at virtual ground; hold
+1  = positive-side differential persisted through the center window
```

The ternary receipt is not the whole machine. It is the local resolution of the DC/AC/RC/magnetic loop.

## 4. Three mirrored gate regions

Three bidirectional mirrored gate regions bound and condition the crossing behavior:

```text
→ + DC ──[ G+ ]──[ G0 ]──[ G- ]── - DC ←
← + return ──[ G+ ]──[ G0 ]──[ G- ]── - return →
```

- `G+`: positive-side threshold / compression-expression boundary.
- `G0`: virtual-ground center threshold / hold crossing.
- `G-`: negative-side mirrored threshold / compression-expression boundary.

The gates are not a serial comparator pipeline. They are mirrored threshold bands that participate in a coupled bilateral event. A physical implementation may use bidirectional MOSFET structures, including back-to-back MOSFET arrangements, subject to voltage, current, threshold, and isolation validation.

## 5. DC → AC → RC → rotational hold

```text
DC differential
    → establishes opposed directional bias: → + | 0 | - ←

AC differential
    → oscillates bidirectionally: ↔ + | 0 | - ↔

RC / resistor field
    → provides delay, integration, damping, threshold windows, and anti-chatter history

Three mirrored gates
    → constrain hold, crossing, directional update, modulation, or loop-break

Rotating magnetic / flux hold
    → retains the last resolved directional state as a local memory baseline

Virtual-ground return
    → brings the center receipt back toward the controller and rail origins
```

The selected directional state becomes the relaxed local baseline for the next differential cycle. Balanced virtual ground holds the existing magnetic state without requiring continuous active acceleration.

## 6. Controller loop

The controller is both the rail-origin region and the receiving region for the center return:

```text
controller
  → establishes + / 0 / - rail conditions
  → rails enter the center interaction
  → DC and AC state cross bidirectionally through the center reference
  → center resolves - / 0 / + after its RC window
  → middle virtual-ground rail returns the receipt BACK toward controller
  → controller applies the next bounded mirrored action
```

This is a closed, folded feedback loop. It is not a one-way source → comparator → output chain.

## 7. Axes and roles

| Component | One-Wave role |
|---|---|
| DC dual outer rails | X-axis directional reference and opposed field/void bias |
| AC crossing | Y-axis phase, timing, bidirectional view |
| RC/resistor field | delay, damping, memory window, threshold persistence |
| virtual-ground middle rail | live zero reference and return toward controller |
| rotating magnetic/flux field | Z-axis hold, route memory, and rotational reinjection |
| controller | receives returned center receipt and initiates the next bounded cycle |

## 8. State receipt

Every simulated or physical cell event should emit a receipt:

```json
{
  "dc_left_positive": 0.0,
  "dc_right_negative": 0.0,
  "virtual_ground_middle": 0.0,
  "ac_phase_left": 0.0,
  "ac_phase_right": 0.0,
  "rc_integrated_differential": 0.0,
  "gate_plus": "hold",
  "gate_center": "hold",
  "gate_minus": "hold",
  "ternary_resolution": 0,
  "magnetic_hold_direction": 0,
  "return_target": "controller_rail_origin"
}
```

## 9. Extended route scale

The center remains anchored at `0`. For modulation and loop-breaking, the directional bands can extend symmetrically:

```text
+3, +2, +1 | 0 | -1, -2, -3
```

Each positive route has a mirrored negative route. The extension must not remove the middle virtual-ground rail or convert the topology into a one-way output chain.

## 10. Build and test requirements

Before treating this as hardware behavior, validate it at three levels:

1. **Simulation:** verify that a three-rail model with bidirectional gates produces stable hold, directional update, damping, and return receipts under controlled DC/AC/RC parameters.
2. **Circuit model:** compare an explicit bidirectional MOSFET/RC implementation with SPICE or equivalent circuit analysis; measure threshold, leakage, reverse conduction, switching loss, oscillation stability, and latch-up risk.
3. **Physical prototype:** begin at safe low voltage/current with current limiting, independent measurement of all three rails, and no assumption that an ideal virtual ground remains stable under transient load.

The proposed magnetic-memory and lattice interpretation must be evaluated as a testable hypothesis with measured observables, control cases, and failure criteria.

## 11. Repository binding

This topology is the shared cell contract for:

- `Virtual_Breadboard/` — detailed electrical, magnetic, SPICE-parity, and physical-build work.
- `One_Wave_Bench/` — integration engine, qualification suite, checkers, runs, and schemas.
- `Android_Body/` — sensor/body/action use of the same resolved cell receipts.
- `GRAV-LAB/` — only after an explicit scale-transfer model maps local circulation and retained state into lattice/wake variables.
- `Nodes/` — canonical conceptual primitives, especially ground, displacement, differential, gradient, restoring response, flux, resistance, and finite-wake rules.

## Locked invariant

> The cell starts with opposed DC rails, `→ + | 0 | - ←`. The virtual ground is the middle rail. AC makes the relation bidirectionally oscillate through the center. Three mirrored bidirectional gate regions and the RC/resistor field determine whether the cycle holds, updates direction, modulates, or breaks. The rotating magnetic/flux field retains the resolved route. The center receipt returns on the middle virtual-ground rail BACK toward the controller and the rail origins; it never becomes a forward output beyond the center.
