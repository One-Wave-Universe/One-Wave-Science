#!/usr/bin/env node
/*
 * Destructive / boundary-finding test suite for the PROTOTYPE_001 write
 * mechanism (item 18 of the hardware-scaling directive). Each section
 * below varies ONE real physical dimension across a wide range while
 * holding everything else at a realistic nominal value, and reports
 * exactly where the real physics stops working -- never compensating for
 * a failure, never forcing a result back into range.
 *
 * This talks to js/circuit.js directly (not the board/JSON pipeline) so
 * each sweep can freely vary things the JSON pipeline has no per-instance
 * knob for yet (a single relay's own coil resistance, injected noise on a
 * command line, etc) -- the SAME real component models/specs used
 * everywhere else in this codebase, just wired up by hand once per sweep.
 *
 * Dimensions actually swept: supply voltage, temperature, component
 * mismatch (unmatched coil resistance between the two relays), command-
 * line noise, and rapid-reversal command cadence (which subsumes the
 * oversight/override-delay-vs-command-rate question -- see that
 * section's own comment for why). Pulse width was already swept
 * end-to-end in prototype_001_cycle_test.js (with real Monte Carlo
 * component tolerance on top) and is not repeated here. "Drive current"
 * is not an independent knob on this architecture -- for a fixed
 * H-bridge RDS(on) and coil resistance, current is set entirely by
 * supply voltage (already its own sweep) and coil resistance (the same
 * axis as the mismatch sweep) -- there is no separate real current-limit
 * component on this signal path to vary, so it is not given its own
 * section (disclosed here, not silently skipped).
 *
 * Real, unforced failure boundaries actually found by running this
 * (verified by hand, then locked in by the values below -- not asserted
 * a priori):
 *   - Supply voltage: clean cliff at the real UVLO threshold (2.7V) --
 *     open below it, fully closed at 3V and every voltage up through
 *     15V (including past the real 10.8V max-rating warning, which
 *     fires but does not by itself stop the write).
 *   - Temperature: a genuinely counter-intuitive result. A marginal
 *     write (5ms, just past nominal switchTau) succeeds all the way
 *     from -20C to 125C, then FAILS at 150C+. Naively "hot cores should
 *     switch easier" (real Hc drift lowers the coercive threshold) --
 *     but real copper-tempco coil-resistance rise (0.393%/C, a physical
 *     constant) reduces the actual drive current faster than Hc drops,
 *     so in this real part's numbers, self-heating HURTS marginal
 *     writes rather than helping them. The simulator was not told this
 *     in advance; it fell out of the two real, independent effects
 *     actually competing.
 *   - Component mismatch: A (nominal coil) and B agree through 60%
 *     coil-resistance mismatch, then genuinely diverge at 80%+ -- a
 *     real demonstration of why "no assumed matched parts" (item 9/14)
 *     matters: M4 issuing the identical command to both relays does
 *     NOT guarantee both relays obey it once real part variation is
 *     large enough.
 *   - Command-line noise: stable through 0.8V RMS injected on the GPIO
 *     lines, genuinely unstable (flips outcome across seeds) at 1.0V+
 *     -- because the H-bridge's real input comparison has a SINGLE
 *     fixed threshold with no hysteresis (unlike the Schmitt gates
 *     built later in the chain), it's a real, physically-grounded
 *     argument for why a logic input feeding real hardware benefits
 *     from Schmitt buffering, not just a made-up number.
 *   - Rapid reversal cadence: two SEPARATE real bandwidth limits, not
 *     one. The relay's own mechanical/magnetic switching keeps up with
 *     command rates down to a 10ms half-cycle, then fails completely at
 *     5ms (a real, sharp mechanical/magnetic ceiling). The override tap
 *     (25k/1uF, ~25ms) degrades much earlier and gradually -- reliable
 *     down to 30ms, then increasingly missing confirmations from 25ms
 *     down to 10ms, well before the relay itself gives out. A real
 *     system's actual command-rate ceiling is set by whichever of these
 *     two independent limits is hit first.
 *
 * Run with:
 *   node experiments/prototype_001_destructive_test.js
 */
const CircuitEngine = require('../js/circuit.js');
const LR = CircuitEngine.LATCHRELAY_SPEC;
const HB = CircuitEngine.HBRIDGE_SPEC;

// thresholds as a FRACTION of the real supply actually in use, not a
// fixed absolute voltage -- the sense divider's real high level tracks
// VM directly (it's tied straight to the rail), so a fixed 4.0V/1.0V
// classifier would misreport a real, correctly-closed contact as
// "ambiguous" the moment a sweep changes VM away from 5V (caught while
// building the supply-voltage sweep below: a fully-switched core at
// VM=3V read a real 3.0V sense level, correctly "closed" relative to
// its own real supply, but the fixed-5V-assuming classifier called it
// ambiguous).
function classify(v, vm) {
  const supply = vm != null ? vm : 5;
  if (v == null) return 'unknown';
  if (v >= supply * 0.8) return 'closed';
  if (v <= supply * 0.2) return 'open';
  return 'ambiguous';
}

// one relay channel: GPIO command lines -> hbridge -> latchrelay coil ->
// a real VCC/pulldown contact-sense divider, exactly PROTOTYPE_001's own
// per-channel topology, built directly instead of through board holes.
function channelElements(tag, vmVal, coilR, noiseRms) {
  const inA = 'in1' + tag, inB = 'in2' + tag, outA = 'out1' + tag, outB = 'out2' + tag;
  const com = 'com' + tag, no = 'no' + tag;
  return {
    wires: [{ a: com, b: 'vm' }],
    components: [
      { id: 'in1' + tag, type: 'diffsource', value: 0, sourceR: 100, noiseRms: noiseRms || 0, noiseSeed: 'seedA' + tag, a: inA, b: 'gnd' },
      { id: 'in2' + tag, type: 'diffsource', value: 5, sourceR: 100, noiseRms: noiseRms || 0, noiseSeed: 'seedB' + tag, a: inB, b: 'gnd' },
      { id: 'hb' + tag, type: 'hbridge', in1: inA, in2: inB, vm: 'vm', gnd: 'gnd', out1: outA, out2: outB },
      { id: 'lr' + tag, type: 'latchrelay', windings: [{ a: outA, b: outB, N: 1, R: coilR }], contactA: com, contactB: no, hcAmpTurns: LR.hcAmpTurns, phiSat: LR.phiSat, switchTau: LR.switchTau },
      { id: 'pd' + tag, type: 'resistor', value: 100000, a: no, b: 'gnd' },
    ],
  };
}
function merge(...chunks) {
  return { wires: chunks.flatMap((c) => c.wires), components: chunks.flatMap((c) => c.components) };
}
function battery(vmVal) {
  return { wires: [], components: [{ id: 'bat1', type: 'battery', value: vmVal, a: 'vm', b: 'gnd' }] };
}
// mode: 'field' (forward drive, in1=5/in2=0), 'void' (reverse drive,
// in1=0/in2=5), or 'coast' (in1=0/in2=0 -- NO drive at all, genuinely
// different from 'void': a real hold must remove drive entirely, not
// silently re-command the opposite state)
function setCmd(elements, tag, mode) {
  elements.components.forEach((c) => {
    if (c.id === 'in1' + tag) c.value = mode === 'field' ? 5 : 0;
    if (c.id === 'in2' + tag) c.value = mode === 'void' ? 5 : 0;
  });
}

// run a real init(void) -> write(pulse, Field) -> hold(no drive) sequence
// on one or two channels sharing the same supply, return final readbacks
function runWrite(elements, { pulseMs, holdMs = 100, ambientC, dtWrite = 0.0002, dtHold = 0.001, tags = ['A'] }) {
  const circuit = new CircuitEngine.Circuit();
  tags.forEach((tag) => setCmd(elements, tag, 'void'));
  for (let i = 0; i < 30; i++) circuit.solve(elements, 0.001, ambientC);
  tags.forEach((tag) => setCmd(elements, tag, 'field'));
  const writeSteps = Math.max(1, Math.round(pulseMs / 1000 / dtWrite));
  let res;
  for (let i = 0; i < writeSteps; i++) res = circuit.solve(elements, dtWrite, ambientC);
  tags.forEach((tag) => setCmd(elements, tag, 'coast'));
  const holdSteps = Math.max(1, Math.round(holdMs / 1000 / dtHold));
  for (let i = 0; i < holdSteps; i++) res = circuit.solve(elements, dtHold, ambientC);
  return res;
}

const report = {};

// ---------------------------------------------------------------------
// 1) Supply voltage: sweep VM from well below UVLO to well above vmMax
// ---------------------------------------------------------------------
{
  const rows = [];
  for (const vm of [1.0, 2.0, 2.5, HB.vmMin, 3.0, 5.0, 9.0, HB.vmMax, 11.0, 13.0, 15.0]) {
    const elements = merge(battery(vm), channelElements('A', vm, LR.coilR, 0));
    const res = runWrite(elements, { pulseMs: 15 });
    const sense = res.voltages.get('noA');
    rows.push({ vm, senseState: classify(sense, vm), coreA: Number(res.coreStates.get('lrA').toFixed(4)), warnings: res.warnings.filter((w) => w.includes('hbA') || w.includes('H-bridge')) });
  }
  report.supplyVoltage = rows;
}

// ---------------------------------------------------------------------
// 2) Temperature: sweep ambientC using a deliberately MARGINAL pulse
// width -- 5ms, just past nominal (25C) switchTau (found by direct
// sweep: 4ms never crosses the armature threshold even at 25C, 5ms just
// does) -- so real Hc drift and real copper-tempco coil-resistance rise
// actually have something to move the outcome across.
// ---------------------------------------------------------------------
{
  const rows = [];
  for (const ambientC of [-20, 0, 25, 50, 75, 100, 125, 150, 175, 200]) {
    const elements = merge(battery(5), channelElements('A', 5, LR.coilR, 0));
    const res = runWrite(elements, { pulseMs: 5, ambientC });
    rows.push({ ambientC, senseState: classify(res.voltages.get('noA')), coreA: Number(res.coreStates.get('lrA').toFixed(4)) });
  }
  report.temperature = rows;
}

// ---------------------------------------------------------------------
// 3) Component mismatch: A's coil stays nominal, B's coil resistance is
// pushed further and further from nominal (no assumed matched parts,
// item 9/14) -- both driven by the IDENTICAL marginal pulse, watching
// for the point where A and B stop agreeing even though M4 issued the
// same command to both
// ---------------------------------------------------------------------
{
  const rows = [];
  for (const mismatchFrac of [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]) {
    const coilRB = LR.coilR * (1 + mismatchFrac);
    const elements = merge(battery(5), channelElements('A', 5, LR.coilR, 0), channelElements('B', 5, coilRB, 0));
    const res = runWrite(elements, { pulseMs: 5, tags: ['A', 'B'] });
    const a = classify(res.voltages.get('noA'));
    const b = classify(res.voltages.get('noB'));
    rows.push({ mismatchFrac, coilRB: Number(coilRB.toFixed(2)), aState: a, bState: b, agree: a === b });
  }
  report.componentMismatch = rows;
}

// ---------------------------------------------------------------------
// 4) Command-line noise: real Gaussian noise added to the GPIO command
// lines -- watch for the hbridge's own input-threshold decision (a real
// comparator-style threshold, not idealized) becoming unstable
// ---------------------------------------------------------------------
{
  const rows = [];
  for (const noiseRms of [0, 0.2, 0.5, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0]) {
    const outcomes = [];
    for (let seed = 0; seed < 8; seed++) {
      const elements = merge(battery(5), channelElements('A', 5, LR.coilR, noiseRms));
      elements.components.forEach((c) => { if (c.noiseSeed) c.noiseSeed = c.noiseSeed + ':' + seed; });
      const res = runWrite(elements, { pulseMs: 15 });
      outcomes.push(classify(res.voltages.get('noA')));
    }
    const distinct = new Set(outcomes);
    rows.push({ noiseRms, outcomes, stable: distinct.size === 1 });
  }
  report.commandNoise = rows;
}

// ---------------------------------------------------------------------
// 5) Rapid reversal / command cadence: the SAME fast/oversight/override
// timing chain PROTOTYPE_001 builds (10k/1uF=10ms tap, 25k/1uF=25ms tap),
// commanding alternating Field/Void writes at a shrinking interval --
// this directly answers "does oversight/override delay stay ahead of
// the command rate" (subsuming a separate oversight-delay/override-delay
// sweep: the real question is always relative to how fast commands
// arrive, not the RC values in isolation) and "how fast can this
// mechanism reverse" together.
// ---------------------------------------------------------------------
{
  function withTimingChain(vmVal) {
    const base = merge(battery(vmVal), channelElements('A', vmVal, LR.coilR, 0));
    base.wires.push({ a: 'senseA', b: 'noA' });
    base.components.push(
      { id: 'sgFast', type: 'schmitt', in: 'senseA', out: 'fastOut', vcc: 'vm', gnd: 'gnd' },
      { id: 'rOs', type: 'resistor', value: 10000, a: 'fastOut', b: 'osRC' },
      { id: 'cOs', type: 'capacitor', value: 1e-6, a: 'osRC', b: 'gnd' },
      { id: 'sgOs', type: 'schmitt', in: 'osRC', out: 'osOut', vcc: 'vm', gnd: 'gnd' },
      { id: 'rOv', type: 'resistor', value: 25000, a: 'fastOut', b: 'ovRC' },
      { id: 'cOv', type: 'capacitor', value: 1e-6, a: 'ovRC', b: 'gnd' },
      { id: 'sgOv', type: 'schmitt', in: 'ovRC', out: 'ovOut', vcc: 'vm', gnd: 'gnd' },
    );
    return base;
  }
  const rows = [];
  for (const intervalMs of [200, 100, 60, 40, 30, 25, 20, 15, 10, 5]) {
    const elements = withTimingChain(5);
    const circuit = new CircuitEngine.Circuit();
    const dt = 0.0005;
    const stepsPerHalfCycle = Math.max(1, Math.round(intervalMs / 1000 / dt));
    let res, coreConfirmedCount = 0, overrideConfirmedCount = 0, totalCycles = 6;
    let high = false;
    for (let cyc = 0; cyc < totalCycles; cyc++) {
      high = !high;
      setCmd(elements, 'A', high ? 'field' : 'void');
      for (let i = 0; i < stepsPerHalfCycle; i++) res = circuit.solve(elements, dt);
      // two SEPARATE real bandwidth limits, checked independently rather
      // than conflated into one flag: did the relay's own mechanical/
      // magnetic switching (coreStates) keep up with this command rate at
      // all, and -- even if it did -- did the slow override tap (25k/1uF,
      // itself a real ~25ms time constant) actually finish confirming it
      // by the time the NEXT command arrives. ovOut is a double inversion
      // of the raw sense (same parity as PROTOTYPE_001's OVERRIDE_OUT),
      // so "Field commanded" means ovOut should settle HIGH, "Void" LOW.
      const coreOK = high ? res.coreStates.get('lrA') > 0.8 : res.coreStates.get('lrA') < -0.8;
      const ovV = res.voltages.get('ovOut');
      const overrideOK = high ? ovV >= 4.5 : ovV <= 0.5;
      if (coreOK) coreConfirmedCount++;
      if (overrideOK) overrideConfirmedCount++;
    }
    rows.push({ intervalMs, coreConfirmedCount, overrideConfirmedCount, totalCycles, coreKeepsUp: coreConfirmedCount === totalCycles, overrideKeepsUp: overrideConfirmedCount === totalCycles });
  }
  report.rapidReversalCadence = rows;
}

console.log(JSON.stringify(report, null, 2));
