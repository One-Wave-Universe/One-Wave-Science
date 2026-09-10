# Breadboard Lab — Free Demo vs Paid Product Contract

Status: product-boundary contract for the human-facing desktop app. One codebase, two entitlements. Do not fork the simulator physics between editions.

## Core rule

The free demo and paid product must use the **same qualified circuit engine, same component models, same fault logic, and same regression suite**.

Edition gating may control UI access, project limits, instruments, export, advanced parts, or add-on workspaces. It must never make the same circuit produce different physics depending on payment status.

## Free Demo

Purpose: let a human install the app, see that it is real, build something useful, change it, and verify measured behavior without needing GitHub, Node, npm, or a terminal.

### Free Demo must include

- one large breadboard workspace;
- editable blank build mode;
- ordinary low-voltage parts sufficient for beginner circuits:
  - jumper wire;
  - resistor;
  - LED;
  - ordinary diode;
  - capacitor;
  - power supply;
  - switch / pushbutton;
  - potentiometer;
  - at least one scope probe / voltage readout;
- live simulation;
- inspector voltage/current readouts;
- warnings for obvious short/fault conditions;
- clear/reset;
- two one-click prebuilt demo builds;
- all free-demo circuit types backed by the same release regression tests as paid.

### Free Demo prebuilt builds

1. **LED Lamp**
   - 5 V supply;
   - current-limiting resistor;
   - LED;
   - ordinary wiring;
   - user can change resistor value and see current/brightness-related electrical behavior change.

2. **RC Charge / Delay**
   - supply;
   - switch;
   - resistor;
   - capacitor;
   - scope probe;
   - user can toggle the switch and watch the real RC transient;
   - user can change R or C and see the time constant change.

The existing short-circuit preset may remain as a safety/fault demonstration, but it is not one of the two primary showcase demos.

### Free Demo limits

Initial release limits should be obvious and non-destructive:

- one board at a time;
- basic component subset only;
- limited scope channels/features;
- no advanced calibration/experimental components;
- no Pedal Lab workspace;
- no Perfboard Amp Lab workspace;
- no batch/export automation;
- local temporary/autosave may be allowed so a crash does not punish the user, but unrestricted project library/export belongs to paid.

Do **not** use artificial solver inaccuracies, fake delays, hidden watermarks over the circuit, or deliberately broken parts as a paywall.

## Paid — Breadboard Lab

Purpose: full human builder product.

Paid unlocks:

- full validated component library;
- all supported board layouts / multi-board workspaces;
- unrestricted project save/reopen;
- project library;
- self-contained circuit export/share;
- full oscilloscope controls and multiple probes;
- differential measurements;
- calibration/reference builds;
- advanced MOSFET, virtual-ground, comparator, inductive/toroid and other qualified components;
- complete fault/diagnostic views;
- BOM/project reporting when implemented;
- AI-assisted build workflow where available, with deterministic validation of resulting circuits;
- future Pedal Lab and Perfboard Amp Lab modules according to license/add-on policy.

## Paid add-ons / editions

The first product family should stay modular:

```text
SiC International
      |
      +-- Breadboard Lab Free Demo
      +-- Breadboard Lab Paid
      +-- Pedal Lab
      +-- Perfboard Amp Lab
```

Pedal Lab and Perfboard Amp Lab reuse the same qualified core. They do not get private alternative physics engines.

## Entitlement implementation

Use one application binary/codebase where practical.

Recommended internal capability model:

```text
edition = free | paid
capabilities = {
  board_count,
  allowed_component_types,
  scope_channels,
  advanced_scope,
  save_projects,
  export_projects,
  calibration_library,
  ai_builder,
  pedal_workspace,
  perfboard_workspace
}
```

UI asks the capability layer whether a feature is available. Circuit-engine code must not read `edition` and must not branch its physics based on entitlement.

## Human acceptance paths

### Free acceptance

```text
install
-> open
-> load LED Lamp demo
-> inspect voltage/current
-> change resistor
-> see result change
-> load RC demo
-> toggle switch
-> observe charge curve
-> make a small blank-board circuit
-> close/reopen app without corruption
```

### Paid acceptance

```text
install
-> activate paid entitlement
-> open blank board
-> build supported ordinary circuit
-> simulate
-> inspect/scope
-> diagnose/adjust
-> save
-> close
-> reopen
-> reload project exactly
-> export/share
-> reopen exported/shared artifact where supported
```

## Release gate

Neither edition ships until:

1. the full supported basic-circuit suite is green;
2. the Electron launch smoke test is green;
3. both demo builds are present in the installed UI and usable without a terminal;
4. the free/paid capability tests prove gating does not change solver output;
5. Linux x64 and Jetson/ARM64 package paths are verified for the intended launch platforms;
6. paid save/reopen/export is exercised end-to-end by a human.

## Pricing

Do not hard-code a price into the simulator source.

Pricing belongs in company/configuration/release metadata so it can change without touching circuit physics. Initial beta pricing should be decided after the installable app survives hands-on human testing and we know which paid features actually carry value.
