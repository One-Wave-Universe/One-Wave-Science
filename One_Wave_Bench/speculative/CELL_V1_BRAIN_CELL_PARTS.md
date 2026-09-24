# CELL_V1 — Analog Brain Cell V1 Parts / BOM

**Companion build:** `One_Wave_Bench/speculative/CELL_V1_BRAIN_CELL_ANALOG_BUILD.md`

This file separates **what the circuit function requires** from **what exact part is already selected**. Do not invent values to make the BOM look finished.

Status key:

```text
LOCKED       = do not change without an explicit architecture revision
BENCH CHOICE = current practical part for the first build
TBD          = function is known, exact part/value must be selected from measurements/datasheet limits
OPTIONAL     = useful for visibility/test, not required for cell operation
LATER        = belongs to a later cell/cluster, not Brain Cell V1
```

---

## 1. First-build BOM

| ID | Qty | Part / function | Status | Role / rule |
|---|---:|---|---|---|
| P1 | 1 | Regulated 5 V supply | LOCKED | First Brain Cell V1 supply |
| U1 | 1 | **TLE2426CLP** 3-terminal rail splitter, or TLE2426 equivalent package | BENCH CHOICE | Creates the 2.5 V center/reference from 5 V |
| S1–S6 | 6 states | Real analog stateful conductance elements | LOCKED FUNCTION / DEVICE TBD | One state position on each hex side in the exact order A+, B+, C+, A-, B-, C- |
| S-source | 1 | **Knowm 1x16 discrete memristor DIP chip or Memristor Discovery device/kit** | PREFERRED PROVEN STARTING SOURCE | Provides real programmable analog conductance devices for the state elements; exact device variant must be identified before choosing drive limits |
| U2 | 1 | **LM339N** 14-pin PDIP quad comparator | BENCH CHOICE | Breadboard-friendly 4-channel threshold block; 3 channels for A/B/C plus one spare/whole-cell channel |
| RPU | as needed | Comparator output pull-up resistor(s) | REQUIRED / VALUE TBD | LM339-family outputs are open collector; calculate from the chosen load and desired current |
| RHYS | as needed | Comparator positive-feedback / hysteresis resistor network | FUNCTION LOCKED / VALUE TBD | Prevents threshold chatter; values come from measured threshold window |
| RLIM | at least 1 per active state path | Memristor/state-element current-limiting resistor(s) or compliance network | REQUIRED / VALUE TBD | Protects the state element; calculate after exact state device and pulse amplitude are selected |
| CDEC | as required | Local decoupling capacitors | REQUIRED / VALUE PER DATASHEET/LAYOUT | Stabilizes IC supply/reference locally |
| CBULK | 1 | Small bulk supply capacitor | BENCH CHOICE / VALUE TBD | Supply transient support; choose after observing 5 V rail |
| LED1 | 1 | LED + its current-limiting resistor | OPTIONAL | Visible binary threshold indicator only; not part of the analog cell state |
| BB1 | 1 | Solderless breadboard or prototype board | BENCH CHOICE | First physical assembly |
| WIRE | as needed | Short jumpers / solid-core hookup wire | REQUIRED | Preserve physical side labeling and test-point access |
| TP | 12+ | Header pins / test loops / labeled probe points | REQUIRED | Repeatable oscilloscope measurements |

---

## 2. Exact side allocation

Do not choose the six state elements and then wire them arbitrarily. Allocate them first and label them physically:

```text
S1 = A+
S2 = B+
S3 = C+
S4 = A-
S5 = B-
S6 = C-
```

Perimeter order:

```text
S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S1
A+ -> B+ -> C+ -> A- -> B- -> C- -> A+
```

Mirror comparisons:

```text
S1 / S4 = A+ / A-
S2 / S5 = B+ / B-
S3 / S6 = C+ / C-
```

Do not physically reorder the six elements just to shorten wires.

---

## 3. Stateful-device choice

For the first genuine analog-memory proof, prefer a **real memristive/stateful conductance device** rather than software emulation.

A practical proven starting family is the Knowm SDC memristor hardware. Knowm documents 16-pin DIP devices, programmable conductance, pulse/read experiments, and differential-pair experiments. Their current documentation also explicitly warns that device current and applied voltage must be limited.

### Hard protection rule

```text
NEVER connect a raw 5 V rail directly across a memristor.
```

The 5 V rail powers the support circuitry. The state device receives a separately limited read/program stimulus appropriate to the exact device variant.

Knowm's published device information lists different limits by device type. Therefore:

```text
CHOOSE EXACT DEVICE
        |
        v
READ ITS LIMITS
        |
        v
CHOOSE PROGRAM/READ VOLTAGE
        |
        v
CALCULATE RLIM / COMPLIANCE
        |
        v
BUILD PART 1
```

Do **not** choose RLIM from habit and then hope the state element survives.

---

## 4. Reference stage — exact first connection

For the 3-terminal TLE2426 package:

```text
5 V supply ------ IN   TLE2426   OUT ------ TP2 = 2.5 V reference
0 V supply ------ COM
```

Check the exact package pinout on the part datasheet before insertion; pin numbering depends on package.

The reference stage is for the low-current analog brain cell. It is not the future motor-current supply.

### Test before adding anything else

```text
TP0 -> 0 V
TP1 -> 5 V
TP2 -> about 2.5 V
```

If TP2 is unstable, stop. Do not compensate elsewhere in the circuit.

---

## 5. Comparator stage — breadboard part

Use **LM339N PDIP-14** for the first breadboard because it provides four comparators in a through-hole package.

Allocation:

```text
Comparator 1 -> A mirror/threshold channel
Comparator 2 -> B mirror/threshold channel
Comparator 3 -> C mirror/threshold channel
Comparator 4 -> whole-cell / reference / experiment channel
```

The LM339 output is open collector. A pull-up is required for a visible/high output state.

Keep the comparator as a **reader of analog state**. It must not become the thing storing the state.

---

## 6. Visual parts placement — first full-cell prototype

This is a functional placement map, not a PCB trace layout:

```text
                              [S1 A+]
                         ________|________
                      /                   \
              [S6 C-]                       [S2 B+]
                 |                             |
                 |         TP2 / 2.5 V         |
                 |          REFERENCE           |
                 |                             |
              [S5 B-]                       [S3 C+]
                      \                   /
                         ________|________
                              [S4 A-]


        5 V ---- [TLE2426] ---- TP2 CENTER
         |
         +------ [LM339N threshold reader]

        A+ / A- ----> comparator channel A
        B+ / B- ----> comparator channel B
        C+ / C- ----> comparator channel C
```

The state-device read/program network is inserted between the stimulus source and the selected S element(s), with current limiting/compliance appropriate to the selected device.

---

## 7. Build parts by stage

### Stage 0 — reference

Required:

```text
P1
U1
CDEC as required
TP0 TP1 TP2
```

Nothing else.

### Stage 1 — one muscle-memory/process axis

Add:

```text
S1 = A+
S4 = A-
RLIM / compliance network
stimulus/read source
TPA+ TPA- TPA_DIFF
oscilloscope
```

Do not add B or C yet.

### Stage 2 — full analog hex

After A passes, add:

```text
S2 = B+
S3 = C+
S5 = B-
S6 = C-
corresponding protection/read wiring
B/C test points
```

### Stage 3 — binary threshold

Add:

```text
U2 LM339N
RPU
RHYS
TP_BIN
optional LED1 + LED resistor
```

### Stage 4 — cell-to-cell output

Add only the smallest buffered/limited View-Up interface required by the next experimental cell or cluster. Do not add M4 or motor power here.

---

## 8. Bench tools

| Tool | Need | Use |
|---|---|---|
| Oscilloscope | REQUIRED | Compare read/program pulses, state response, reference movement, and threshold output |
| Known-good multimeter | STRONGLY RECOMMENDED | Verify supply/reference and passive values; **do not place an unknown high-open-circuit-voltage meter directly across delicate memristor devices** |
| Low-voltage pulse/waveform source | REQUIRED | Controlled state stimulation/programming; must respect device voltage/current limits |
| Current measurement / series sense resistor | REQUIRED | Confirm state-device current stays inside selected limits |
| Current-limited bench supply or protected 5 V source | RECOMMENDED | Prevent wiring mistakes from destroying state devices |
| Printer / build sheet | OPTIONAL | Print the side order and test-point map and leave it beside the breadboard |

---

## 9. Values deliberately NOT guessed yet

These are not missing architecture. They are device-dependent engineering values that must be calculated after the exact state element is selected:

```text
memristor read voltage
memristor program voltage/pulse
pulse width
pulse repetition rate
RLIM / compliance current
comparator threshold resistor values
comparator hysteresis resistor values
supply bulk capacitor
normalization transfer from physical measurement to 0-100 scale
retention/rest test duration
```

Do not promote a convenient simulator value into the physical build without measurement.

---

## 10. Locked 0–100 bands

```text
100-90
85-75
70-60
55-45
40-30
25-15
10-0
```

Preserved gaps:

```text
89-86
74-71
59-56
44-41
29-26
14-11
```

The exact analog quantity mapped into 0–100 must be written into the experiment record. The band boundaries themselves are not to be redone.

---

## 11. What NOT to buy/build for Brain Cell V1 yet

```text
three-winding motor
high-current motor driver
large inductive load
full M4 8+8 flower assembly
multiple duplicated brain cells
large sensor array
microcontroller as cell memory
ADC/DAC loop pretending to be the analog memory
```

Those hide the first question: **does the analog path physically learn/retain enough to alter the next traversal?**

---

## 12. Later BOMs — keep separate

After Brain Cell V1 passes, create separate BOMs for:

1. pathway cell / cell-to-cell routing;
2. local cluster;
3. M4 `2 x 2 x 2 + inverted 2 x 2 x 2` assembly;
4. one local three-winding motor unit;
5. motor cluster coordinating multiple independent motor units.

A motor cluster may coordinate multiple motors, but each independent motor keeps its own local three-winding power stage/current feedback.

---

## 13. Source documents for selected bench parts

- TLE2426 rail splitter, Texas Instruments: https://www.ti.com/product/TLE2426
- LM339 / LM339N quad comparator, Texas Instruments: https://www.ti.com/product/LM339
- Knowm memristors: https://knowm.org/memristors/
- Knowm memristor FAQ: https://knowm.org/memristors/memristor-faq/
- Knowm SDC memristor datasheet: https://knowm.org/downloads/Knowm_Memristors.pdf
- Knowm Memristor Discovery manual: https://knowm.org/downloads/Memristor_Discovery_V0.x.pdf

**Bench rule:** the datasheet for the exact device in hand overrides a generic value in this document.