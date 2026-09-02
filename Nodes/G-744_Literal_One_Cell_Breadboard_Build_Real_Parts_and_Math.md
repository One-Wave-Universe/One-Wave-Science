---
node_id: "G-744"
canonical_name: "Literal One-Cell Breadboard Build — Real Parts and Math"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Breadboard / Mixed-Signal / One-Wave Cell Primitive"
claim_gate_detail: "YELLOW until measured on bench"
metadata_standard: "I-06"
---

# Node G-744: Literal One-Cell Breadboard Build — Real Parts and Math

## Purpose

Translate the current One-Wave cell architecture into ordinary low-voltage electronics with explicit components, voltages, thresholds, currents, and pass/fail measurements.

This node is intentionally staged. It does **not** attempt the entire quadratic / reflex / actuator stack at once. Stage 1 proves one millivolt ternary primitive around one shared reference. Only after that passes is it duplicated to three physical triads and linked into the six-position cell.

## Software pre-verification (simulated, not a bench substitute)

`Virtual_Breadboard/` (repo root, merged to `main`) is a real modified-nodal-analysis
circuit simulator — it solves the actual electrical equations rather than
scripting an animation. It implements this node's window-comparator + MOSFET
switch pair as a first-class "Ternary Cell" component (differential input,
hysteresis, mutual exclusion by construction between the pos/neg paths, clean
return to Hold), matching this node's pass conditions in software before
anything touches a bench.

Available launch paths:

- Interactive, in-browser: open `Virtual_Breadboard/index.html` (or
  `docs/index.html` for the hosted copy) and use the "Ternary 3-phase drive"
  preset button, which wires three Ternary Cells to a shared `V0` reference
  and a toroid exactly as this node's Stage 2/3 triads describe.
- Headless, for an automated loop (e.g. a Python driver on other hardware):
  `node Virtual_Breadboard/simulate.js` reads a circuit spec as JSON on
  stdin and returns solved voltages/currents/warnings/ternary states as
  JSON — no browser, no npm install, no dependencies beyond Node itself.
- Regression tests: `node Virtual_Breadboard/test/circuit.test.js` (see its
  Test 16 for the ternary hold/pos/neg + hysteresis/no-chatter proof).
- Full usage docs: `Virtual_Breadboard/README.md`.

This does not advance this node's gate. `claim_gate_detail` stays
"YELLOW until measured on bench" — a correct circuit-equation solve is
evidence the design is electrically sound on paper, not a substitute for the
real-component measurements this node's stages require.

## Locked One-Wave constraints

- one local shared reference `V0` per cell;
- information state is millivolt-scale relative to `V0`;
- local ternary is `-1 / 0 / +1`;
- three physical triads are reused in two traversal orientations for six logical positions;
- MOSFETs are switches, not millivolt comparators;
- View and Action hardware remains separate per G-743;
- three-winding reflex remains separate from quadratic sensing/drive but contributes to Views up and accepts Override down.

## Supply and reference

Bench supply:

```text
+5.000 V USB / bench supply
0 V supply return
```

Recommended local midpoint reference:

```text
U1 = TLE2426 rail splitter
V0 = 0.5 * VS = 2.500 V nominal
```

The TLE2426 is specified for 4 V to 40 V supply and approximately 20 mA source/sink capability. The cell's millivolt information paths must not be used as load-current returns.

Add local bypassing close to U1:

```text
100 nF ceramic from +5 V to supply return
10 uF electrolytic from +5 V to supply return
100 nF ceramic from V0 to supply return only if consistent with the selected TLE2426 package/application guidance
```

Measure `V0` before continuing. Reject the stage if it moves by more than the declared state margin under the tiny signal loads used here.

## State target

Initial state displacement:

```text
Delta = 20 mV

-1 = V0 - 20 mV = 2.480 V
 0 = V0           = 2.500 V
+1 = V0 + 20 mV = 2.520 V
```

This is a starting bench margin, not a universal constant.

## Generate the two threshold references

Use 0.1% or 1% metal-film resistors for the first proof.

### Upper threshold `VHI`

```text
+5 V --- 124 kΩ ---+--- 1.00 kΩ --- V0
                    |
                   VHI
```

Because the node is a divider between +5 V and V0:

```text
VHI = V0 + (5.000 - V0) * 1k / (124k + 1k)

with V0 = 2.500 V:
VHI = 2.500 + 2.500 * (1 / 125)
    = 2.520 V
```

### Lower threshold `VLO`

```text
0 V --- 124 kΩ ----+--- 1.00 kΩ --- V0
                    |
                   VLO
```

```text
VLO = V0 - (V0 - 0) * 1k / (124k + 1k)
    = 2.500 - 2.500 * (1 / 125)
    = 2.480 V
```

The reference-divider current is approximately:

```text
I = 2.5 V / 125 kΩ = 20 uA
```

per threshold branch.

## Ternary sensing: real window comparator

Use a dual rail-to-rail comparator:

```text
U2 = TLV3202
supply = +5 V / 0 V
```

The TLV320x family operates from 2.7 V to 5.5 V, has rail-to-rail inputs, about 1 mV typical input offset, and built-in hysteresis around the millivolt range. A 20 mV state margin is therefore deliberately much larger than typical offset/hysteresis.

Comparator A detects the positive state:

```text
U2A + input = VSENSE
U2A - input = VHI
P = HIGH when VSENSE > VHI
```

Comparator B detects the negative state:

```text
U2B + input = VLO
U2B - input = VSENSE
N = HIGH when VSENSE < VLO
```

Truth table:

```text
VSENSE > VHI        -> P=1 N=0 -> +1
VLO <= VSENSE <=VHI -> P=0 N=0 -> HOLD / 0
VSENSE < VLO        -> P=0 N=1 -> -1
P=1 N=1             -> fault / invalid
```

This is a genuine three-region detector. Ground is not a third binary choice; it is the active middle ternary region.

## MOSFET switch stage

Do not feed the ±20 mV signal directly into a MOSFET gate. Ordinary enhancement MOSFET thresholds are measured in volts, not tens of millivolts.

Recommended breadboard-friendly implementation uses SOT-23 devices on breakout adapters:

```text
Q1-Q4 = AO3400A N-channel MOSFET
```

The AO3400A is specified for `RDS(on)` at `VGS = 2.5 V`, making it suitable for a switch whose signal node sits near 2.5 V while its gate is driven between 0 V and 5 V.

Each analog path uses two N-MOSFETs back-to-back, sources tied together, gates tied together. The external path terminals are the two drains. This blocks the intrinsic body diode in both directions when off.

Positive switch:

```text
VPLUS_REF -- drain Q1
              source Q1 -- source Q2
                           drain Q2 -- STATE_OUT
Q1,Q2 gates tied = P
```

Negative switch:

```text
VMINUS_REF -- drain Q3
               source Q3 -- source Q4
                            drain Q4 -- STATE_OUT
Q3,Q4 gates tied = N
```

Add:

```text
100 kΩ from STATE_OUT to V0
```

so `P=0,N=0` produces an electrical Hold near V0 instead of a floating node.

## Generate `VPLUS_REF` and `VMINUS_REF`

For the first proof, the same passive references used for thresholds can be duplicated as separate low-current state-source references. Do not share the exact threshold nodes if switch loading measurably shifts comparator thresholds.

Use a second pair of 124 kΩ / 1 kΩ networks:

```text
VPLUS_REF  = approximately 2.520 V
VMINUS_REF = approximately 2.480 V
```

Their Thevenin resistance is approximately:

```text
Rth = 124k || 1k ~= 992 Ω
```

With the 100 kΩ Hold resistor, the loaded displacement when a state switch closes is approximately:

```text
Delta_loaded = 20 mV * 100k / (100k + 0.992k)
             ~= 19.80 mV
```

which remains close to the intended ±20 mV target.

## Stage-1 breadboard nodes

Do not depend on arbitrary row numbers; label these nodes with jumper-wire colors or tape because breadboard row numbering varies.

Required named nodes:

```text
+5V
GND
V0
VHI
VLO
VPLUS_REF
VMINUS_REF
VSENSE
P
N
STATE_OUT
```

Recommended physical layout:

```text
left side:   supply + TLE2426 + reference dividers
center:      TLV3202 comparator
right side:  Q1-Q4 MOSFET switch pairs + STATE_OUT
```

Keep VHI/VLO/VSENSE wiring short and away from later motor/coil wiring.

## Manual test source

Before connecting another triad, drive `VSENSE` with an adjustable DC source around V0. A 10-turn potentiometer or precision source is preferred. The test source must be able to cross 2.480 V, 2.500 V and 2.520 V slowly enough to observe switching.

Do not use a normal single-turn 5 V pot as evidence of exact millivolt thresholds unless the scope measurement confirms the actual crossing voltages.

## Scope test points

Use oscilloscope ground on supply return and measure absolute voltages first, then use math/subtract mode if available to display displacement from V0.

Probe sequentially:

```text
TP0 = V0
TP1 = VHI
TP2 = VLO
TP3 = VSENSE
TP4 = P
TP5 = N
TP6 = STATE_OUT
```

Expected values:

```text
V0   ~= 2.500 V
VHI  ~= 2.520 V
VLO  ~= 2.480 V

STATE_OUT with + selected ~= V0 + 19.8 mV
STATE_OUT with HOLD       ~= V0
STATE_OUT with - selected ~= V0 - 19.8 mV
```

## Pass conditions for one triad

Do not duplicate the circuit until all are true:

1. `VHI > V0 > VLO` and both offsets are close to the intended ±20 mV;
2. `P` and `N` never assert simultaneously in normal operation;
3. the Hold region exists and is repeatable;
4. `STATE_OUT` resolves three distinct levels relative to V0;
5. switching one state does not drag V0 by a significant fraction of 20 mV;
6. state readings remain distinguishable above breadboard noise;
7. opening both switch paths returns `STATE_OUT` to V0 through the 100 kΩ Hold resistor.

## Stage 2: duplicate to three physical triads

After Stage 1 passes, duplicate the entire ternary state block twice:

```text
Triad A
Triad B
Triad C
```

All three use the same cell-level `V0`. Each gets its own `VSENSE`, comparator pair, switch pairs, and state output. The shared V0 is probed while A/B/C switch independently.

Pass condition:

```text
state_A, state_B, state_C are independently distinguishable
while V0 remains stable
```

## Stage 3: six logical positions from three physical triads

Use the three physical states as a circulating three-axis relation. Initial test sequence:

```text
1: A=+  B=0  C=-
2: A=0  B=+  C=-
3: A=-  B=+  C=0
4: A=-  B=0  C=+
5: A=0  B=-  C=+
6: A=+  B=-  C=0
repeat
```

Reverse the sequence to reverse traversal orientation.

This stage is successful only if six repeatable directed positions are measured from the same three physical triads. It must not be relabeled as six physical gates.

## RC timing translation

When the static six-position sequence is proven, introduce timing one change at a time.

For a first slow visible/testable cycle, target roughly 10 Hz:

```text
T = 1/f = 0.1 s
```

A first-order RC time constant may start near one-sixth of the full period:

```text
tau ~= T/6 ~= 16.7 ms
```

Example real values:

```text
R = 150 kΩ
C = 100 nF
RC = 15 ms
```

This is only a starting timing constant. The actual oscillator topology determines the exact period relation, so the measured phase spacing—not the nominal RC product—is authoritative.

## Quadratic and reflex layers after the core passes

Do not attach them before the three-triad/six-position proof.

Then add in order:

```text
three-triad rotating relation
-> G-743 resolver/quadrature Views UP
-> command resolution
-> G-743 two-phase sine/cosine Actions DOWN
-> three-winding ternary reflex controller
-> measured consequence back into Views/reference
```

The three-winding reflex state is included in the upward receipt. A downward Void Deny produces Override to the reflex controller. Override remains separate from the local `-1/0/+1` ternary state.

## Real-world engineering references

- Texas Instruments TLE2426: precision half-supply rail splitter; 4 V to 40 V supply; low-impedance midpoint; source/sink capability suitable for reference service.
- Texas Instruments TLV3201/TLV3202: rail-to-rail comparators; 2.7 V to 5.5 V supply; millivolt-class offset/hysteresis appropriate for a ±20 mV first proof.
- Alpha & Omega AO3400A: N-channel MOSFET with specified `RDS(on)` at `VGS = 2.5 V`, suitable for gate-controlled switching around a 2.5 V signal common-mode when used within ratings.
- G-743 external resolver and two-phase sine/cosine drive references remain authoritative for the later quadratic layers.

## Anti-drift statement

```text
One-Wave architecture defines the relationships.
Conventional electronics defines what can physically sense, switch, oscillate, and drive them.
Millivolt state is information.
Comparator output is gate drive.
MOSFET is a switch.
Shared V0 is the cell reference.
Three physical triads are not six physical gates.
Measured waveforms override labels.
```
