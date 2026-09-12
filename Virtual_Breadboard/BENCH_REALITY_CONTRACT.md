# Virtual Breadboard — Bench Reality Contract

## Status

**AUTHORITATIVE QUALIFICATION BOUNDARY FOR PHYSICAL-BENCH CLAIMS.**

A solver PASS means only that the equations for the supplied model solved and met that test's numeric thresholds. It does **not** automatically mean a breadboard build is physically valid.

A build may be called **BENCH-QUALIFIED** only when it also passes the bench-reality audit and uses the same source, reference, drive, current-limit, and return topology intended for the physical build.

---

## 1. Current CELL_V1 bench authority

For the present dual-rail bench:

```text
+12 V rail
   |
  10 k
   |
   +---------- local / gate experiment
   |
  solid 0 star ---------------- measure I_0 at controller end
   |
  10 k
   |
-12 V rail
```

Physical source architecture:

```text
+12 V  ---- positive supply
  0 V  ---- REAL midpoint / star conductor
-12 V  ---- negative supply
```

This is **not** a TLE2426 / rail-splitter topology.

Do not place `vgnd`, TLE2426, or another synthetic midpoint on top of the true dual-supply 0 V midpoint and call both of them CENTER.

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

The 0 rail itself must remain a low-impedance reference. A pretty midpoint voltage with no real DC 0 path is a failure.

---

## 3. CENTER / 0 spine rules

The 0 spine is a conductor/reference path.

Allowed for measurement:

- a wire;
- a deliberately small known shunt such as 0.1 ohm at the controller end;
- real lead/contact resistance explicitly modeled.

Not allowed in series with the 0 spine:

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

The present F0 bench limit is:

```text
|I_source| <= 20 mA
```

That is an **acceptance limit**, not the engine's historical global source limit.

Any simulation that requires more than the declared bench limit is physically unqualified even if the MNA solver can still produce a voltage solution.

---

## 5. MOSFET gate-drive truth

A MOSFET gate is controlled by **VGS**, not by the gate voltage printed relative to some unrelated ground.

For an N-MOS:

```text
VGS = Vgate - Vsource
```

A Nano GPIO that swings 0..5 V relative to supply 0 can directly command only a device whose source is referenced appropriately to that same 0 V domain.

It cannot directly turn on a 12 V high-side N-MOS after the source rises. The device becomes a source follower / turns back off as VGS collapses. A real high-side N-MOS requires a bootstrapped, isolated, or otherwise source-referenced gate driver.

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

Later motor work uses a separate ESC/proper three-half-bridge driver with its power return bonded to supply 0 at one star point. Motor stall current never returns through a TLE/synthetic midpoint or the cell's delicate I_0 receipt path.

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
