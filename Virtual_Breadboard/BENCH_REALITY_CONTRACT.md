# Virtual Breadboard — Bench Reality Contract

## Status

**AUTHORITATIVE QUALIFICATION BOUNDARY FOR PHYSICAL-BENCH CLAIMS.**

A solver PASS means only that the equations for the supplied model solved and met that test's numeric thresholds. It does **not** automatically mean a breadboard build is physically valid.

A build may be called **BENCH-QUALIFIED** only when it also passes the bench-reality audit and uses the same source, reference, drive, current-limit, and return topology intended for the physical build.

---

## 1. Current CELL_V1 bench authority

The current CELL_V1 bench is the locked **single 5 V supply + buffered midpoint** build.

```text
5 V protected/current-limited source
        |
   +----+---------------- P
   |
 TLE2426 or equivalent verified midpoint host
   |
   +--------------------- G ~= 2.5 V reference
   |
   +--------------------- N = 0 V supply return
```

The TLE2426 is used as a **low-current signal/reference midpoint**. TI specifies it as a precision half-supply rail splitter with approximately 20 mA typical source/sink capability. It is not the return path for a motor, speaker, or power coil.

Reference:
https://www.ti.com/product/TLE2426

The energy/reinjection reservoir, if used, is a separate DC-link/storage element. `G` is not an energy reservoir.

The retired +/-12 V CELL_V1 bench remains historical only. Do not use it as the current physical authority unless a new measured requirement explicitly reopens it.

---

## 2. Receipt that must work before gates

With equal 10 k arms:

```text
I_0 ~= 0
V(0_bus) ~= V(0_source)
```

Then deliberately change one side, e.g. 10 k -> 6.8 k:

```text
I_0 must become measurably nonzero.
```

Move the mismatch to the opposite arm:

```text
sign(I_0) must reverse.
```

The G reference itself must remain a low-impedance reference. A pretty midpoint voltage with no real DC 0 path is a failure.

---

## 3. CENTER / G spine rules

The G spine is a measured low-current reference path.

Allowed for measurement:

- a wire;
- a deliberately small known shunt such as 0.1 ohm at the controller end;
- real lead/contact resistance explicitly modeled.

Not allowed in series with the G spine:

- capacitor;
- inductor used as the only DC path;
- current source;
- decorative RC network;
- toroid winding standing in for the reference conductor.

A series capacitor can make the far side *look* centered under symmetric loading while the DC reference is actually cut. The bench audit therefore rejects it even if the solved voltage is near zero.

---

## 4. Source-current truth

Every active build must have a source-current receipt.

If resistors, MOSFET channels, LEDs, coils, or other loads are dissipating power, a display showing the supply at `0.00 A` is not an acceptable result unless the solved source current is genuinely below the displayed resolution.

The first reference qualification is deliberately low current. Keep TLE2426 **imbalance current** comfortably below its approximate 20 mA typical source/sink capability; the initial P1/P2 checks use only a few mA. Board supply current is a separate measurement.

This is an acceptance boundary for the midpoint/reference experiment, not a motor-current allowance.

Any simulation that requires more than the declared bench limit is physically unqualified even if the MNA solver can still produce a voltage solution.

---

## 5. MOSFET gate-drive truth

A MOSFET gate is controlled by **VGS**, not by the gate voltage printed relative to some unrelated ground.

For an N-MOS:

```text
VGS = Vgate - Vsource
```

A controller GPIO can directly command only a MOSFET whose required VGS is achieved relative to that MOSFET's actual source. A floating/high-side N-MOS generally requires a source-referenced, bootstrapped, isolated, or dedicated gate driver.

For the present cell work:

- direct Nano drive is allowed only where the common-source node is physically 0-referenced and VGS is proven;
- a floating bilateral pair requires its own real source-referenced / isolated gate drive;
- an ideal floating test battery is a test fixture, not proof that the final controller can drive the pair.

---

## 6. Three logical Mirrors do not license a motor power stage

CELL_V1 and a BLDC inverter are separate machines until a coupling experiment explicitly proves otherwise.

CELL_V1 qualification must not silently include an H-bridge/three-half-bridge motor power stage and then count the result as proof of the cell.

For now:

```text
CELL_V1: G+ / G0 / G- experiments
MOTOR:   disconnected
```

Later motor work uses a separate ESC or proper three-half-bridge driver with its own power return to the real supply return. Motor/coil current never returns through the TLE2426 midpoint or the cell's delicate reference-sense path. Standard three-phase BLDC six-step commutation is the comparison baseline; it normally energizes two phases per 60-degree electrical sector.

Reference:
https://onlinedocs.microchip.com/oxy/GUID-3AFF556D-77AD-488F-9A04-CD7AAB8F7DBC-en-US-1/GUID-A1DD3CA4-D59F-45CF-AA9F-EBBCB9EF37BA.html

---

## 7. Magnetic truth

Toroids, ferrite rings, inductors, or drawn loops are not evidence of magnetic hold.

A magnetic-memory claim requires a drive-off receipt that survives controls for:

- ordinary L/R inductive decay;
- capacitor/RC storage;
- diode/MOSFET reverse recovery;
- sensor offset and drift;
- instrument zero;
- thermal drift;
- remanence of the actual core material.

Until then, magnetic parts are **measurement experiments**, not passed cell functions.

---

## 8. Breadboard parasitics

Physical qualification models at least:

- supply/lead/contact resistance;
- real component tolerance;
- MOSFET model card and VGS reference;
- capacitor ESR/leakage;
- inductor/toroid winding resistance;
- source current budget;
- CENTER/0 shunt resistance where current is measured.

At motor-current scale a solderless breadboard is not an acceptable power bus. Motor-current qualification belongs on a proper driver/module/PCB with appropriate wiring and protection.

---

## 9. PASS language

Use these terms literally:

- **SOLVER PASS** — numerical circuit equations solved.
- **MODEL PASS** — expected behavior occurs in the modeled components.
- **BENCH-REALITY PASS** — supply/reference/drive/current/return constraints also match a plausible physical build.
- **PHYSICAL PASS** — measured on actual hardware.

Never promote one level into the next without the missing receipt.


---

## 10. External reference requirement

This contract is subordinate to G-778 Build Logic, Research, and Reference Validation Standard.

Any new physical claim must identify:
- the real reference mechanism;
- the One-Wave-specific change;
- a control build;
- acceptance/failure criteria;
- a retained measurement receipt.

A MODEL PASS is never promoted to PHYSICAL PASS without actual bench data.
