# One Wave Science — Market Readiness Gate

A product is not ready to sell until every required gate below is either PASS or explicitly waived with a written reason and owner.

## Gate A — Legal company

- [ ] Legal entity formed and active.
- [ ] Initial Statement of Information filed.
- [ ] EIN obtained.
- [ ] Company banking/accounting separated from personal finances.
- [ ] Operating agreement signed.
- [ ] Founder/pre-formation IP assignment completed.
- [ ] Local business-license requirements checked.

## Gate B — Brand/IP

- [ ] Company name cleared for entity use.
- [ ] Company/product names searched for conflicting trademarks.
- [ ] Third-party dependency licenses inventoried.
- [ ] No unlicensed images, fonts, sounds, code, circuit drawings or documentation shipped.
- [ ] Copyright notices/licenses included where required.
- [ ] Trademark filing decision documented.

## Gate C — Product evidence

Every advertised technical claim is labeled internally as one of:
- CONTROL-VALIDATED
- BENCH-VALIDATED
- SIMULATED
- PROPOSED / EXPERIMENTAL

Required:
- [ ] Conventional control suite green.
- [ ] Product-specific regression suite green.
- [ ] No tests weakened merely to make a product claim pass.
- [ ] Known approximations documented.
- [ ] Known unsupported component models documented.
- [ ] Dangerous/invalid circuit states are surfaced rather than hidden.

## Gate D — Desktop app

- [ ] Installer builds successfully for each advertised OS/architecture.
- [ ] App launches from installed package, not only `npm start`.
- [ ] Build a circuit.
- [ ] Power/simulate it.
- [ ] Inspect voltages/currents/faults.
- [ ] Use scope/measurement tools.
- [ ] Save.
- [ ] Quit/reopen.
- [ ] Load and recover same build.
- [ ] Export/share path works.
- [ ] Uninstall/reinstall behavior understood.
- [ ] Crash/error path produces useful report, not silent loss.

## Gate E — Product UX

A new human tester must be able to complete the core workflow without repository knowledge or terminal use.

- [ ] first-run screen explains what the app does;
- [ ] example project opens in one click;
- [ ] common controls are visible;
- [ ] measurements have units;
- [ ] warnings distinguish danger, invalid wiring and model limitations;
- [ ] undo/recovery story documented;
- [ ] help/user guide available inside or beside the app.

## Gate F — Security/privacy

- [ ] No API key bundled in installer or exported circuit.
- [ ] AI/provider integrations are optional.
- [ ] Network behavior documented.
- [ ] Privacy policy matches actual telemetry/data collection.
- [ ] If there is no telemetry, say so accurately.
- [ ] External links and file import paths validated.

## Gate G — Commercial/legal surface

Before accepting payment:
- [ ] Terms of use/license.
- [ ] Privacy policy.
- [ ] Refund/support policy.
- [ ] Warranty/disclaimer language reviewed.
- [ ] Clear statement that simulation does not replace safe physical bench practice.
- [ ] Product-liability/general-liability insurance decision made.
- [ ] Export-control/sanctions/payment-processor requirements checked as applicable.
- [ ] Sales-tax handling determined for physical and digital products sold.

## Gate H — Release operations

- [ ] version number fixed;
- [ ] release notes;
- [ ] installer hashes/artifacts retained;
- [ ] reproducible build source commit recorded;
- [ ] support email/issue path active;
- [ ] rollback/previous release retained;
- [ ] critical bug update path tested.

## Product-specific gates

### Breadboard Lab
- ordinary resistor/network controls;
- RC/RL/diode/LED/MOSFET controls;
- netlist and fault-state controls;
- physical board topology controls;
- human install/build/save/reopen acceptance.

### Pedal Lab
Must add before sale:
- guitar-level source/input impedance fixture;
- audio frequency sweep;
- gain vs frequency;
- clipping waveform/threshold;
- bypass behavior;
- tone-control response;
- supply-current measurement;
- noise/hum model boundaries;
- required transistor/op-amp/diode models for supported pedal circuits;
- known unsupported nonlinear/audio behavior clearly listed.

### Perfboard Amp Lab
Must add before sale:
- perfboard hole/strip/cut/link topology;
- physical layout/connectivity validation;
- amplifier component models required by supported designs;
- quiescent bias/current tests;
- gain and bandwidth;
- clipping/output swing;
- load impedance;
- power dissipation/thermal warnings;
- power-rail/grounding checks;
- oscillation/stability limits documented;
- mains-voltage designs OUT OF SCOPE until a separately reviewed high-voltage safety model exists.

## Hard rule

**Do not market a simulator result as bench proof. Do not market an experimental One-Wave hypothesis as established electronics.**
