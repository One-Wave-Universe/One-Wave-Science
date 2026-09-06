const assert = require('assert');
const fs = require('fs');
const path = require('path');
const CircuitEngine = require('../js/circuit.js');
const { Circuit } = CircuitEngine;

function approx(a, b, eps, msg) {
  assert.ok(Math.abs(a - b) < eps, `${msg}: expected ~${b}, got ${a}`);
}

// Test 1: battery + resistor loop -> Ohm's law with battery internal resistance
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'M', value: 220 },
    ],
  };
  const res = c.solve(els, 1 / 60);
  const expectedI = 5 / (220 + 1); // internal resistance 1 ohm
  approx(res.currents.get('bat1'), expectedI, 1e-4, 'battery current');
  approx(res.currents.get('r1'), expectedI, 1e-4, 'resistor current');
  console.log('Test 1 OK: I =', (res.currents.get('r1') * 1000).toFixed(2), 'mA (Ohm\'s law)');
}

// Test 2: battery + resistor + LED in series -> LED turns on, current limited
{
  const c = new Circuit();
  const els = {
    wires: [{ a: 'P', b: 'N1' }],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'N1', b: 'N2', value: 220 },
      { id: 'led1', type: 'led', a: 'N2', b: 'M', color: 'red' },
    ],
  };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(els, 1 / 60);
  const I = res.currents.get('led1');
  assert.ok(I > 0, 'LED should conduct');
  const expected = (5 - 1.8) / (220 + 12 + 1);
  approx(I, expected, 1e-3, 'LED current');
  assert.ok(res.warnings.length === 0, 'should be no warnings for a safe LED circuit: ' + res.warnings.join('; '));
  console.log('Test 2 OK: LED current =', (I * 1000).toFixed(2), 'mA, LED on =', I > 0);
}

// Test 3: LED wired backwards -> should not conduct
{
  const c = new Circuit();
  const els = {
    wires: [{ a: 'P', b: 'N1' }],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'N1', b: 'N2', value: 220 },
      { id: 'led1', type: 'led', a: 'M', b: 'N2', color: 'red' }, // reversed
    ],
  };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(els, 1 / 60);
  approx(res.currents.get('led1'), 0, 1e-6, 'reversed LED current should be ~0');
  console.log('Test 3 OK: reversed LED current =', res.currents.get('led1'));
}

// Test 4: direct short circuit across battery terminals -> warning + high current
{
  const c = new Circuit();
  const els = {
    wires: [{ a: 'P', b: 'M' }],
    components: [{ id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 }],
  };
  const res = c.solve(els, 1 / 60);
  approx(res.currents.get('bat1'), 5, 1e-3, 'short circuit current (5V/1ohm internal)');
  assert.ok(res.warnings.some((w) => w.includes('Short circuit')), 'should warn about short circuit');
  console.log('Test 4 OK: short-circuit current =', res.currents.get('bat1').toFixed(2), 'A, warned:', res.warnings[0]);
}

// Test 5: too-small resistor with LED -> current-limiting warning
{
  const c = new Circuit();
  const els = {
    wires: [{ a: 'P', b: 'N1' }],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 9 },
      { id: 'r1', type: 'resistor', a: 'N1', b: 'N2', value: 10 },
      { id: 'led1', type: 'led', a: 'N2', b: 'M', color: 'red' },
    ],
  };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(els, 1 / 60);
  assert.ok(res.warnings.some((w) => w.includes('current-limiting')), 'should warn LED current too high: ' + res.warnings.join(';'));
  console.log('Test 5 OK: over-current LED warning fired, I =', (res.currents.get('led1') * 1000).toFixed(0), 'mA');
}

// Test 6: RC charging curve approaches battery voltage over time (real transient physics)
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'N1', value: 1000 },
      { id: 'cap1', type: 'capacitor', a: 'N1', b: 'M', value: 1000e-6 }, // 1000uF, RC=1s
    ],
  };
  const dt = 1 / 60;
  let res;
  let vAtHalfSecond = null;
  for (let step = 0; step < 60 * 5; step++) {
    res = c.solve(els, dt);
    if (step === 30) vAtHalfSecond = res.voltages.get('N1');
  }
  const vFinal = res.voltages.get('N1');
  approx(vFinal, 5, 0.05, 'capacitor should charge close to battery voltage after 5s (5 tau)');
  assert.ok(vAtHalfSecond > 1 && vAtHalfSecond < 3.5, 'capacitor should be partially charged at t=RC/2, got ' + vAtHalfSecond);
  console.log('Test 6 OK: cap voltage at t=0.5s =', vAtHalfSecond.toFixed(2), 'V, at t=5s =', vFinal.toFixed(2), 'V (expect ~5V)');
}

// Test 7: switch open breaks the circuit, closing it reconnects
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'sw1', type: 'switch', a: 'P', b: 'N1', closed: false },
      { id: 'r1', type: 'resistor', a: 'N1', b: 'M', value: 220 },
    ],
  };
  let res = c.solve(els, 1 / 60);
  approx(res.currents.get('r1'), 0, 1e-6, 'open switch -> no current');
  els.components[1].closed = true;
  res = c.solve(els, 1 / 60);
  approx(res.currents.get('r1'), 5 / 221, 1e-3, 'closed switch -> Ohm\'s law current');
  console.log('Test 7 OK: switch open I=0, closed I =', (res.currents.get('r1') * 1000).toFixed(2), 'mA');
}

// Test 8: generic diode conducts forward (Vf=0.7V) and blocks reverse
{
  const c = new Circuit();
  const els = {
    wires: [{ a: 'P', b: 'N1' }],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'N1', b: 'N2', value: 220 },
      { id: 'd1', type: 'diode', a: 'N2', b: 'M' },
    ],
  };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(els, 1 / 60);
  approx(res.currents.get('d1'), (5 - 0.7) / (220 + 5 + 1), 1e-3, 'forward diode current');

  const c2 = new Circuit();
  els.components[2] = { id: 'd1', type: 'diode', a: 'M', b: 'N2' }; // reversed
  for (let i = 0; i < 5; i++) res = c2.solve(els, 1 / 60);
  approx(res.currents.get('d1'), 0, 1e-6, 'reversed diode current should be ~0');
  console.log('Test 8 OK: diode forward =', (res.currents.get('d1') * 1000).toFixed(2), 'mA (reversed), blocks correctly');
}

// Test 9: pushbutton is momentary — closed only while held
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'pb1', type: 'pushbutton', a: 'P', b: 'N1', closed: false },
      { id: 'r1', type: 'resistor', a: 'N1', b: 'M', value: 220 },
    ],
  };
  let res = c.solve(els, 1 / 60);
  approx(res.currents.get('r1'), 0, 1e-6, 'released pushbutton -> no current');
  els.components[1].closed = true;
  res = c.solve(els, 1 / 60);
  approx(res.currents.get('r1'), 5 / 221, 1e-3, 'held pushbutton -> Ohm\'s law current');
  els.components[1].closed = false;
  res = c.solve(els, 1 / 60);
  approx(res.currents.get('r1'), 0, 1e-6, 'released again -> no current');
  console.log('Test 9 OK: pushbutton momentary behavior correct');
}

// Test 10: a Y-split wire is a standalone 4-lead part — each end forks to 2
// holes, joined by a run between the forks — modeled as 3 zero-resistance
// ties (end1A-end1B, end1A-end2A, end2A-end2B). Confirm all 4 holes end up
// as one electrical node, the mechanism app.js's Y-split wire relies on.
{
  const c = new Circuit();
  const els = {
    wires: [{ a: 'A1', b: 'B1' }, { a: 'A1', b: 'A2' }, { a: 'A2', b: 'B2' }],
    components: [
      { id: 'bat1', type: 'battery', a: 'A1', b: 'M', value: 9 },
      { id: 'r1', type: 'resistor', a: 'B2', b: 'M', value: 1000 },
    ],
  };
  const res = c.solve(els, 1 / 60);
  const v = ['A1', 'B1', 'A2', 'B2'].map((id) => res.voltages.get(res.uf.find(id)));
  approx(v[0], v[1], 1e-9, 'Y-split: end1A and end1B should be the same node');
  approx(v[0], v[2], 1e-9, 'Y-split: end1A and end2A should be the same node');
  approx(v[0], v[3], 1e-9, 'Y-split: end1A and end2B should be the same node');
  approx(res.currents.get('r1'), 9 / 1001, 1e-3, 'current flows through the far fork as expected');
  console.log('Test 10 OK: Y-split ties all 4 holes to one node, V =', v[0].toFixed(3), 'V');
}

// Test 11: virtual ground / rail splitter — its output node should always
// sit at the midpoint of the two rails it splits, unloaded and loaded, and
// for an asymmetric (single-supply, e.g. 9V) rail pair too.
{
  // Symmetric-looking case: a 5V rail split against 0V ground -> V0 = 2.5V.
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
    ],
  };
  let res = c.solve(els, 1 / 60);
  const vP = res.voltages.get(res.uf.find('P'));
  const vM = res.voltages.get(res.uf.find('M'));
  const vOut = res.voltages.get(res.uf.find('V0'));
  approx(vOut, (vP + vM) / 2, 1e-3, 'unloaded vgnd V0 should be midpoint of 5V rail');

  // Load the V0 output with a resistor back to the minus rail -- midpoint
  // should barely move (small internal resistance, like the battery model).
  const c2 = new Circuit();
  els.components.push({ id: 'r1', type: 'resistor', a: 'V0', b: 'M', value: 10000 });
  res = c2.solve(els, 1 / 60);
  const vOutLoaded = res.voltages.get(res.uf.find('V0'));
  approx(vOutLoaded, 2.5, 0.01, 'loaded vgnd V0 should stay near midpoint (2.5V) with a 10k load');

  // Asymmetric case: a 9V rail split against 0V ground -> V0 = 4.5V.
  const c3 = new Circuit();
  const els3 = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 9 },
      { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
    ],
  };
  res = c3.solve(els3, 1 / 60);
  const vOut9 = res.voltages.get(res.uf.find('V0'));
  approx(vOut9, 4.5, 1e-3, 'vgnd on a 9V rail should read 4.5V midpoint');
  console.log('Test 11 OK: vgnd V0 =', vOut.toFixed(3), 'V (5V rail),', vOut9.toFixed(3), 'V (9V rail), loaded =', vOutLoaded.toFixed(4), 'V');
}

// Test 12: inductor -- backward-Euler companion model should reproduce the
// real L/R current-rise transient of a series battery+resistor+inductor
// loop, the dual of Test 6's RC charging curve.
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'N1', value: 100 },
      { id: 'l1', type: 'inductor', a: 'N1', b: 'M', value: 0.1 },
    ],
  };
  const dt = 1 / 2000;
  let res;
  for (let i = 0; i < 2000; i++) res = c.solve(els, dt); // 1 second
  // steady state: R includes the battery's own internal resistance AND
  // the inductor's own real winding resistance (DCR) -- a real 100mH
  // inductor is never a bare L, so both real series resistances set the
  // actual L/R time constant, not just the resistor the user placed.
  const totalR = 100 + CircuitEngine.BATTERY_RINT + CircuitEngine.inductorDCR(0.1);
  const iSteady = 5 / totalR;
  const tau = 0.1 / totalR;
  const iExpected = iSteady * (1 - Math.exp(-1 / tau));
  approx(res.currents.get('l1'), iExpected, 1e-3, 'inductor current follows the L/R rise curve');
  console.log('Test 12 OK: inductor current after 1s =', (res.currents.get('l1') * 1000).toFixed(2), 'mA (expect ~', (iExpected * 1000).toFixed(2), 'mA)');
}

// Test 13: AC source -- a real time-varying ideal source, evaluated on the
// simulator's own running clock. Step to specific times and check the
// voltage across a resistor load matches the analytic sine.
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'ac1', type: 'acsource', a: 'P', b: 'M', value: 5, freq: 2, phase: 0 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'M', value: 100000 }, // light load, minimal sag
    ],
  };
  const dt = 1 / 4000;
  const stepTo = (target) => {
    const steps = Math.round(target / dt);
    let res;
    for (let i = 0; i < steps; i++) res = c.solve(els, dt);
    return res;
  };
  let res = stepTo(0.125); // quarter period of a 2Hz wave -> peak
  let v = res.voltages.get(res.uf.find('P')) - res.voltages.get(res.uf.find('M'));
  approx(v, 5, 0.05, 'AC source at t=T/4 should be near its positive peak');

  const c2 = new Circuit();
  res = null;
  const steps2 = Math.round(0.25 / dt);
  for (let i = 0; i < steps2; i++) res = c2.solve(els, dt); // half period -> back near zero-crossing
  v = res.voltages.get(res.uf.find('P')) - res.voltages.get(res.uf.find('M'));
  approx(v, 0, 0.05, 'AC source at t=T/2 should be near a zero-crossing');
  console.log('Test 13 OK: AC source tracks a real sine on the sim clock (peak and zero-crossing both landed correctly)');
}

// Test 14: MTJ angle sensor -- a quadrature pair (sin/cos of a rotating
// field) referenced to a shared pin, modeling a real MTJ/TMR angle-sensor
// IC's analog outputs. sin^2+cos^2 should stay ~amplitude^2 (a real
// quadrature identity) and the two channels should be 90 degrees apart.
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'VP', b: 'GND', value: 5 },
      { id: 'vg1', type: 'vgnd', a: 'VP', b: 'GND', out: 'V0' },
      { id: 'mtj1', type: 'mtjsensor', ref: 'V0', sin: 'SIN', cos: 'COS', value: 1, freq: 1, phase: 0 },
      { id: 'rs', type: 'resistor', a: 'SIN', b: 'V0', value: 1000000 },
      { id: 'rc', type: 'resistor', a: 'COS', b: 'V0', value: 1000000 },
    ],
  };
  const dt = 1 / 2000;
  let maxErr = 0;
  let res;
  for (let i = 0; i < 2000; i++) {
    res = c.solve(els, dt);
    const v0 = res.voltages.get(res.uf.find('V0'));
    const vs = res.voltages.get(res.uf.find('SIN')) - v0;
    const vc = res.voltages.get(res.uf.find('COS')) - v0;
    maxErr = Math.max(maxErr, Math.abs(vs * vs + vc * vc - 1));
  }
  if (maxErr > 0.01) throw new Error('MTJ sin^2+cos^2 deviated from the amplitude^2 quadrature identity by ' + maxErr);
  console.log('Test 14 OK: MTJ sin/cos quadrature pair holds sin^2+cos^2 = 1 (max deviation', maxErr.toFixed(5), ')');
}

// Test 15: ferrite toroid -- a single winding should behave exactly like a
// plain inductor (L/R transient), and two windings sharing a core with
// real mutual-inductance coupling should transform an AC drive by
// (approximately, given finite coupling/loading) their turns ratio, the
// way an actual transformer does.
{
  // single winding == plain inductor
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'N1', value: 100 },
      { id: 'tor1', type: 'toroid', coupling: 0, windings: [{ a: 'N1', b: 'M', L: 0.1, R: 0 }] },
    ],
  };
  const dt1 = 1 / 2000;
  let res;
  for (let i = 0; i < 2000; i++) res = c.solve(els, dt1);
  const totalR = 100 + CircuitEngine.BATTERY_RINT;
  const tau = 0.1 / totalR;
  const iExpected = (5 / totalR) * (1 - Math.exp(-1 / tau));
  approx(res.currents.get('tor1'), iExpected, 1e-3, 'single-winding toroid follows the L/R rise curve like a plain inductor');

  // two windings, 1:2 turns ratio, tightly coupled -- secondary should read
  // ~2x the primary at steady state (ideal-transformer limit)
  const c2 = new Circuit();
  const AL = 250e-9;
  const turnsP = 10, turnsS = 20;
  const els2 = {
    wires: [],
    components: [
      { id: 'ac1', type: 'acsource', a: 'P1', b: 'P2', value: 5, freq: 1000, phase: 0 },
      {
        id: 'tor2', type: 'toroid', coupling: 0.995,
        windings: [
          { a: 'P1', b: 'P2', L: AL * turnsP * turnsP, R: 0.01 },
          { a: 'S1', b: 'S2', L: AL * turnsS * turnsS, R: 0.01 },
        ],
      },
      { id: 'rload', type: 'resistor', a: 'S1', b: 'S2', value: 100000 },
    ],
  };
  const dt2 = 1 / 200000;
  const steps = Math.round(20 / 1000 / dt2); // 20 cycles at 1kHz
  let maxVp = 0, maxVs = 0;
  for (let i = 0; i < steps; i++) {
    res = c2.solve(els2, dt2);
    if (i > steps * 0.7) {
      maxVp = Math.max(maxVp, Math.abs(res.voltages.get(res.uf.find('P1')) - res.voltages.get(res.uf.find('P2'))));
      maxVs = Math.max(maxVs, Math.abs(res.voltages.get(res.uf.find('S1')) - res.voltages.get(res.uf.find('S2'))));
    }
  }
  approx(maxVs / maxVp, turnsS / turnsP, 0.1, 'toroid transformer output follows the turns ratio (1:2)');
  console.log('Test 15 OK: toroid single-winding matches a plain inductor, two-winding transformer ratio =', (maxVs / maxVp).toFixed(3), '(expect ~2)');
}

// Test 16 (T-DIV): a 124k/1k divider off a 2.5V mid-rail (5V split by a
// vgnd) must resolve to 2.520V, not snap/round to 2.500V -- proves the
// solver actually carries millivolt-scale asymmetry riding on volts, to
// within 1mV of the exact analytic answer.
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
      { id: 'r1', type: 'resistor', a: 'P', b: 'N', value: 124000 },
      { id: 'r2', type: 'resistor', a: 'N', b: 'V0', value: 1000 },
    ],
  };
  const res = c.solve(els, 1 / 60);
  const vN = res.voltages.get(res.uf.find('N'));
  approx(vN, 2.52, 0.001, 'T-DIV: 124k/1k divider off 2.5V mid-rail must resolve to 2.520V within 1mV');
  console.log('Test 16 OK (T-DIV): divider node =', vN.toFixed(4), 'V (expect 2.5200V)');
}

// Test 17 (T-VGND): Virtual Ground's V0 output must hold the midpoint
// under a real 100k load to a rail, not sag like a plain resistor divider.
{
  const c = new Circuit();
  const elsUnloaded = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
    ],
  };
  const resUnloaded = c.solve(elsUnloaded, 1 / 60);
  const vUnloaded = resUnloaded.voltages.get(resUnloaded.uf.find('V0'));

  const c2 = new Circuit();
  const elsLoaded = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
      { id: 'r1', type: 'resistor', a: 'V0', b: 'M', value: 100000 },
    ],
  };
  const resLoaded = c2.solve(elsLoaded, 1 / 60);
  const vLoaded = resLoaded.voltages.get(resLoaded.uf.find('V0'));
  approx(vLoaded, 2.5, 0.001, 'T-VGND: V0 under a 100k load must stay within 1mV of the unloaded midpoint');
  console.log('Test 17 OK (T-VGND): V0 unloaded =', vUnloaded.toFixed(4), 'V, under 100k load =', vLoaded.toFixed(4), 'V');
}

// Test 18 (T-NFET-ON): a real N-MOSFET with Vgs=5V (well above its
// threshold) must conduct, with the drain voltage set exactly by the
// RDS(on) divider against its load resistor -- not just "some current".
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'D', value: 1000 },
      { id: 'f1', type: 'nmos', gate: 'P', drain: 'D', source: 'M', value: 1.5 },
    ],
  };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 1 / 60);
  const spec = CircuitEngine.NMOS_PARTS[1.5];
  const vD = res.voltages.get(res.uf.find('D'));
  const vExpected = 5 * spec.rdsOn / (1000 + spec.rdsOn);
  approx(vD, vExpected, 1e-4, 'T-NFET-ON: drain voltage must match I*RDS(on) exactly');
  assert.strictEqual(res.mosfetStates.get('f1').channelOn, true, 'T-NFET-ON: channel must be reported on');
  console.log('Test 18 OK (T-NFET-ON): Vgs=5V conducts, drain =', vD.toFixed(4), 'V (expect', vExpected.toFixed(4), 'V)');
}

// Test 19 (T-NFET-OFF): the same N-MOSFET with Vgs=0 (gate tied to source)
// must block the channel entirely -- current through it comes only from
// whatever the body diode allows, tested separately below.
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'D', value: 1000 },
      // gate tied directly to source -> Vgs=0, the simplest unambiguous off case
      { id: 'f1', type: 'nmos', gate: 'M', drain: 'D', source: 'M', value: 1.5 },
    ],
  };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 1 / 60);
  assert.strictEqual(res.mosfetStates.get('f1').channelOn, false, 'T-NFET-OFF: Vgs=0 must leave the channel off');
  assert.strictEqual(res.mosfetStates.get('f1').bodyDiodeOn, false, 'T-NFET-OFF: reverse-biased body diode must also stay off here (drain above source)');
  approx(res.currents.get('f1'), 0, 1e-6, 'T-NFET-OFF: current through an off FET (no forward-biased diode) must be ~0');
  console.log('Test 19 OK (T-NFET-OFF): Vgs=0 blocks the channel, current =', res.currents.get('f1'));
}

// Test 20 (T-NFET-DIODE): a single off N-MOSFET's body diode conducts
// source->drain past ~0.7V (forward), and blocks drain->source (reverse) --
// the real body-diode direction that makes back-to-back pairs work.
{
  // forward: source pulled above drain -- body diode should conduct
  const cFwd = new Circuit();
  const elsFwd = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'S', b: 'D', value: 5 },
      { id: 'f1', type: 'nmos', gate: 'S', drain: 'D', source: 'S', value: 1.5 },
    ],
  };
  let resFwd;
  for (let i = 0; i < 10; i++) resFwd = cFwd.solve(elsFwd, 1 / 60);
  assert.strictEqual(resFwd.mosfetStates.get('f1').bodyDiodeOn, true, 'T-NFET-DIODE: source above drain must forward-bias the body diode');
  assert.ok(resFwd.currents.get('f1') < 0, 'T-NFET-DIODE: forward body-diode current flows source->drain (negative in the drain->source convention)');

  // reverse: drain pulled above source -- body diode should block
  const cRev = new Circuit();
  const elsRev = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'D', b: 'S', value: 5 },
      { id: 'f1', type: 'nmos', gate: 'S', drain: 'D', source: 'S', value: 1.5 },
    ],
  };
  let resRev;
  for (let i = 0; i < 10; i++) resRev = cRev.solve(elsRev, 1 / 60);
  assert.strictEqual(resRev.mosfetStates.get('f1').bodyDiodeOn, false, 'T-NFET-DIODE: drain above source must reverse-bias (block) the body diode');
  approx(resRev.currents.get('f1'), 0, 1e-6, 'T-NFET-DIODE: reverse-biased body diode must pass ~0 current');
  console.log('Test 20 OK (T-NFET-DIODE): body diode conducts source->drain, blocks drain->source');
}

// Test 21 (T-BB-PAIR): two N-MOSFETs with sources tied together and both
// gates tied to that shared source (definitely off) must block current in
// BOTH directions -- the real bidirectional-switch arrangement (whichever
// way current would try to flow, one of the two body diodes opposes it).
{
  function bbPairCurrent(batteryA, batteryB) {
    const c = new Circuit();
    const els = {
      wires: [{ a: 'G1', b: 'S' }, { a: 'G2', b: 'S' }],
      components: [
        { id: 'bat1', type: 'battery', a: batteryA, b: batteryB, value: 9 },
        { id: 'f1', type: 'nmos', gate: 'G1', drain: 'D1', source: 'S', value: 1.5 },
        { id: 'f2', type: 'nmos', gate: 'G2', drain: 'D2', source: 'S', value: 1.5 },
      ],
    };
    let res;
    for (let i = 0; i < 10; i++) res = c.solve(els, 1 / 60);
    return { res, I: res.currents.get('bat1') };
  }
  const fwd = bbPairCurrent('D1', 'D2');
  const rev = bbPairCurrent('D2', 'D1');
  approx(fwd.I, 0, 1e-6, 'T-BB-PAIR: back-to-back pair must block current in one direction');
  approx(rev.I, 0, 1e-6, 'T-BB-PAIR: back-to-back pair must block current in the other direction too');
  assert.strictEqual(fwd.res.mosfetStates.get('f1').channelOn, false, 'T-BB-PAIR: both channels stay off');
  assert.strictEqual(fwd.res.mosfetStates.get('f2').channelOn, false, 'T-BB-PAIR: both channels stay off');
  console.log('Test 21 OK (T-BB-PAIR): 9V across the pair blocks both directions (I =', fwd.I.toExponential(2), 'A /', rev.I.toExponential(2), 'A)');
}

// Test 22 (T-RC): 150k + 100nF must rise on the real tau = R*C = 15ms
// time constant, checked against the analytic 1-e^(-t/RC) curve at 1 tau
// and 3 tau, not just "eventually gets there".
{
  const c = new Circuit();
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'r1', type: 'resistor', a: 'P', b: 'N', value: 150000 },
      { id: 'cap1', type: 'capacitor', a: 'N', b: 'M', value: 100e-9 },
    ],
  };
  const dt = 1 / 20000;
  const tau = 150000 * 100e-9; // 15ms
  const totalR = 150000 + CircuitEngine.BATTERY_RINT;
  const vFinal = (5 * 150000) / totalR;
  let res;
  let t = 0;
  let v1tau = null;
  let v3tau = null;
  const steps = Math.round((3.5 * tau) / dt);
  for (let i = 0; i < steps; i++) {
    res = c.solve(els, dt);
    t += dt;
    if (v1tau === null && t >= tau) v1tau = res.voltages.get(res.uf.find('N'));
    if (v3tau === null && t >= 3 * tau) v3tau = res.voltages.get(res.uf.find('N'));
  }
  approx(v1tau, vFinal * (1 - Math.exp(-1)), vFinal * 0.02, 'T-RC: voltage at 1 tau must match the analytic RC curve');
  approx(v3tau, vFinal * (1 - Math.exp(-3)), vFinal * 0.02, 'T-RC: voltage at 3 tau must match the analytic RC curve');
  console.log('Test 22 OK (T-RC): 150k+100nF at 1 tau =', v1tau.toFixed(3), 'V, at 3 tau =', v3tau.toFixed(3), 'V (tau =', (tau * 1000).toFixed(1), 'ms)');
}

// Test 23 (T-MEM): the actual acceptance circuit -- supply, vgnd, two
// N-MOSFETs back-to-back (sources tied, gates driven by a shared control
// signal), a cap, and a leak resistor. Closing the shared gate control
// (SAMPLE) must let "mem" track a real millivolt-scale input; opening it
// (HOLD) must isolate mem so it only relaxes toward V0 on the deliberate
// leak resistor's real RC time constant -- not toward absolute ground, and
// not diverging -- while staying within a few mV of V0 the whole time.
{
  function build(gateV, leakOhms, capFarads) {
    return {
      wires: [],
      components: [
        { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
        { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
        { id: 'r1', type: 'resistor', a: 'P', b: 'IN', value: 124000 },
        { id: 'r2', type: 'resistor', a: 'IN', b: 'V0', value: 1000 },
        { id: 'gatesrc', type: 'battery', a: 'G', b: 'M', value: gateV },
        { id: 'f1', type: 'nmos', gate: 'G', drain: 'IN', source: 'S', value: 1.5 },
        { id: 'f2', type: 'nmos', gate: 'G', drain: 'MEM', source: 'S', value: 1.5 },
        { id: 'cap1', type: 'capacitor', a: 'MEM', b: 'V0', value: capFarads },
        { id: 'leak1', type: 'resistor', a: 'MEM', b: 'V0', value: leakOhms },
      ],
    };
  }
  const leakOhms = 100000;
  const capFarads = 10e-6; // tau = R*C = 1s
  const dt = 1 / 2000;
  const c = new Circuit();

  // SAMPLE: gate high -> both FETs on -> mem must track IN (~V0+20mV)
  let res;
  for (let i = 0; i < 200; i++) res = c.solve(build(5, leakOhms, capFarads), dt);
  const vIn = res.voltages.get(res.uf.find('IN'));
  const vMemSampled = res.voltages.get(res.uf.find('MEM'));
  const vV0Sampled = res.voltages.get(res.uf.find('V0'));
  assert.strictEqual(res.mosfetStates.get('f1').channelOn, true, 'T-MEM: SAMPLE must turn both channels on');
  approx(vMemSampled, vIn, 0.001, 'T-MEM: SAMPLE must let mem track the input within 1mV');
  approx(vMemSampled - vV0Sampled, 0.02, 0.001, 'T-MEM: sampled mem must sit ~20mV above V0');

  // HOLD: gate low -> both FETs off -> mem decays toward V0 (NOT toward 0V,
  // and NOT diverging) on the real tau = leakOhms * capFarads
  const elsHold = build(0, leakOhms, capFarads);
  const tau = leakOhms * capFarads;
  let vAt1Tau = null;
  const steps = Math.round((4 * tau) / dt);
  for (let i = 0; i < steps; i++) {
    res = c.solve(elsHold, dt);
    if (vAt1Tau === null && i * dt >= tau) vAt1Tau = res.voltages.get(res.uf.find('MEM')) - res.voltages.get(res.uf.find('V0'));
  }
  assert.strictEqual(res.mosfetStates.get('f1').channelOn, false, 'T-MEM: HOLD must turn both channels off');
  assert.strictEqual(res.mosfetStates.get('f2').channelOn, false, 'T-MEM: HOLD must turn both channels off');
  // analytic single-pole decay from +20mV toward ~0 (V0): e^-1 ~ 36.8% remains at 1 tau
  approx(vAt1Tau, 0.02 * Math.exp(-1), 0.002, 'T-MEM: mem must decay toward V0 on the real leak*cap tau, not toward absolute ground');
  const vMemFinal = res.voltages.get(res.uf.find('MEM')) - res.voltages.get(res.uf.find('V0'));
  assert.ok(Math.abs(vMemFinal) < 0.005, 'T-MEM: after several tau, mem must settle within a few mV of V0, not diverge past it');
  console.log('Test 23 OK (T-MEM): sampled mem-V0 =', ((vMemSampled - vV0Sampled) * 1000).toFixed(2), 'mV, decays to', (vAt1Tau * 1000).toFixed(2), 'mV at 1 tau, settles to', (vMemFinal * 1000).toFixed(3), 'mV');
}

// Shared small-core parameters for the memory-core tests below -- a real
// winding-resistance figure (turns * mean-turn-length * copper ohms/m for
// standard-gauge wire, the same formula the toroid uses) rather than a
// made-up round number.
const SMALL_CORE = { hcAmpTurns: 2, phiSat: 4e-6, switchTau: 0.002 };
function windingR(turns, meanTurnLen) {
  const ohmsPerMStandardGauge = 0.0531;
  return turns * meanTurnLen * ohmsPerMStandardGauge;
}

// Test 25 (T-CORE-LOCK): a square-loop memory core, driven past its real
// ampere-turns coercive threshold, must lock to +Br; driven the opposite
// way, it must show a real (nonzero, decaying) induced-voltage spike on a
// separate sense winding while flipping to -Br; driven the same way again
// (already saturated there) must show essentially no spike at all.
{
  const N = 20;
  const R = windingR(N, 0.03);
  function build(driveV) {
    return {
      wires: [],
      components: [
        { id: 'bat1', type: 'battery', a: 'P', b: 'GND', value: driveV },
        { id: 'r1', type: 'resistor', a: 'P', b: 'DA', value: 10 },
        {
          id: 'mc1', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau,
          windings: [
            { a: 'DA', b: 'GND', N, R }, // drive winding
            { a: 'SA', b: 'SB', N, R }, // sense winding, unloaded
          ],
        },
      ],
    };
  }
  const dt = 1 / 2000;
  const c = new Circuit();
  let res;
  for (let i = 0; i < 40; i++) res = c.solve(build(2), dt);
  approx(res.coreStates.get('mc1'), 1, 0.01, 'T-CORE-LOCK: write +I must lock the core to +Br');

  let maxSpikeFlip = 0;
  for (let i = 0; i < 80; i++) {
    res = c.solve(build(-2), dt);
    const vSense = res.voltages.get(res.uf.find('SA')) - res.voltages.get(res.uf.find('SB'));
    if (Math.abs(vSense) > Math.abs(maxSpikeFlip)) maxSpikeFlip = vSense;
  }
  approx(res.coreStates.get('mc1'), -1, 0.01, 'T-CORE-LOCK: write -I must flip the core to -Br');
  assert.ok(Math.abs(maxSpikeFlip) > 0.005, 'T-CORE-LOCK: flipping must produce a real sense-winding voltage spike (saw ' + maxSpikeFlip + ')');

  let maxSpikeRepeat = 0;
  for (let i = 0; i < 40; i++) {
    res = c.solve(build(-2), dt);
    const vSense = res.voltages.get(res.uf.find('SA')) - res.voltages.get(res.uf.find('SB'));
    if (Math.abs(vSense) > Math.abs(maxSpikeRepeat)) maxSpikeRepeat = vSense;
  }
  approx(res.coreStates.get('mc1'), -1, 0.001, 'T-CORE-LOCK: writing -I again must leave the core at -Br');
  assert.ok(Math.abs(maxSpikeRepeat) < Math.abs(maxSpikeFlip) / 20, 'T-CORE-LOCK: writing the SAME direction again (already saturated there) must show almost no spike (saw ' + maxSpikeRepeat + ' vs ' + maxSpikeFlip + ' for the real flip)');
  console.log('Test 25 OK (T-CORE-LOCK): lock=+Br, flip spike=', maxSpikeFlip.toFixed(4), 'V, repeat spike=', maxSpikeRepeat.toFixed(6), 'V');
}

// Test 26 (T-CORE-HOLD): a pulse that never crosses the coercive threshold
// must leave remanence completely unchanged -- real "spring back", not a
// small nudge toward zero.
{
  const N = 20;
  const R = windingR(N, 0.03);
  function build(driveV) {
    return {
      wires: [],
      components: [
        { id: 'bat1', type: 'battery', a: 'P', b: 'GND', value: driveV },
        { id: 'r1', type: 'resistor', a: 'P', b: 'DA', value: 10 },
        { id: 'mc1', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau, windings: [{ a: 'DA', b: 'GND', N, R }] },
      ],
    };
  }
  const dt = 1 / 2000;
  const c = new Circuit();
  let res;
  for (let i = 0; i < 40; i++) res = c.solve(build(-2), dt);
  const bBefore = res.coreStates.get('mc1');
  approx(bBefore, -1, 0.01, 'T-CORE-HOLD: setup -- core must start locked at -Br');
  for (let i = 0; i < 30; i++) res = c.solve(build(0.05), dt); // well below Hc
  approx(res.coreStates.get('mc1'), bBefore, 1e-5, 'T-CORE-HOLD: a sub-threshold pulse must leave remanence exactly unchanged');
  console.log('Test 26 OK (T-CORE-HOLD): sub-Hc pulse left B at', res.coreStates.get('mc1').toFixed(6), '(unchanged from', bBefore.toFixed(6), ')');
}

// Test 27 (T-GATE-MEM): a real back-to-back N-MOSFET pair (the same
// bidirectional switch T-BB-PAIR proves) dumps write current through a
// memory-core winding while its gates are driven on, then the gates go off
// -- remanence must survive the gate closing (DC memory, not volatile).
// Now that the MOSFET model includes real gate input capacitance (Ciss),
// the pair's shared source node -- otherwise connected to nothing else --
// would be a genuinely floating node once both channels cut off, exactly
// like a real back-to-back analog-switch IC's internal node: with no real
// DC path, real parasitic Cgs charge from the ON phase has nothing to
// discharge through and the switch can't be relied on to reach a clean
// off state. Any real bench build of this topology needs a defined bias
// path on that node for exactly this reason (a standard real design
// practice for anti-series MOSFET switches) -- sbias is that real, high-
// value (so it doesn't load real signal current) bias resistor.
{
  const N = 20;
  const R = windingR(N, 0.03);
  function build(gateV, leanV) {
    return {
      wires: [],
      components: [
        { id: 'ctrl', type: 'battery', a: 'GATE', b: 'GND', value: gateV },
        { id: 'lean', type: 'battery', a: 'D1', b: 'GND', value: leanV },
        { id: 'f1', type: 'nmos', gate: 'GATE', drain: 'D1', source: 'S', value: 1.5 },
        { id: 'f2', type: 'nmos', gate: 'GATE', drain: 'D2', source: 'S', value: 1.5 },
        { id: 'sbias', type: 'resistor', a: 'S', b: 'GND', value: 1e6 },
        { id: 'mc1', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau, windings: [{ a: 'D2', b: 'GND', N, R }] },
      ],
    };
  }
  const dt = 1 / 2000;
  const c = new Circuit();
  let res;
  for (let i = 0; i < 40; i++) res = c.solve(build(5, 2), dt); // gates ON, dump +2V
  approx(res.coreStates.get('mc1'), 1, 0.01, 'T-GATE-MEM: dumping through the open gate pair must lock the core');
  assert.strictEqual(res.mosfetStates.get('f1').channelOn, true, 'T-GATE-MEM: gates must actually be on during the dump');
  for (let i = 0; i < 20; i++) res = c.solve(build(0, 2), dt); // gates OFF, lean still present
  assert.strictEqual(res.mosfetStates.get('f1').channelOn, false, 'T-GATE-MEM: gates must be off afterward');
  assert.strictEqual(res.mosfetStates.get('f2').channelOn, false, 'T-GATE-MEM: gates must be off afterward');
  approx(res.coreStates.get('mc1'), 1, 0.001, 'T-GATE-MEM: remanence must survive the gate pair opening');
  console.log('Test 27 OK (T-GATE-MEM): locked through the gate pair, survives gates opening, B=', res.coreStates.get('mc1').toFixed(4));
}

// Test 28 (T-TRI-DECIDE): the same cell (one gate pair + one memory core)
// must be able to finish Left, Right, or Hold depending purely on a
// millivolt-scale write lean and whether the gate ever opened -- four
// cases: +lean/open -> Left, -lean/open -> Right, any lean/closed -> Hold
// (never opened), and a lean too weak to cross Hc even with the gate open
// -> Hold. The write lean here (needed to actually push real current
// through a sub-ohm winding) is a few hundred millivolts -- still
// millivolt-scale, distinct from the microvolt/20mV SENSING resolution
// Cal A-E prove, because writing real amp-turns and sensing a comparator
// margin are different jobs with different real current/impedance needs.
{
  const N = 20;
  const R = windingR(N, 0.03);
  function build(leanV, gateOn) {
    return {
      wires: [],
      components: [
        { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
        { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
        { id: 'lean', type: 'battery', a: 'LEAN', b: 'V0', value: leanV },
        { id: 'gatectrl', type: 'battery', a: 'GATE', b: 'M', value: gateOn ? 5 : 0 },
        { id: 'f1', type: 'nmos', gate: 'GATE', drain: 'LEAN', source: 'S', value: 1.5 },
        { id: 'f2', type: 'nmos', gate: 'GATE', drain: 'WRITE', source: 'S', value: 1.5 },
        { id: 'mc1', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau, windings: [{ a: 'WRITE', b: 'V0', N, R }] },
      ],
    };
  }
  const dt = 1 / 2000;
  let res;

  const cLeft = new Circuit();
  for (let i = 0; i < 60; i++) res = cLeft.solve(build(0.2, true), dt);
  approx(res.coreStates.get('mc1'), 1, 0.01, 'T-TRI-DECIDE: +lean with gate open must finish Left (+Br)');

  const cRight = new Circuit();
  for (let i = 0; i < 60; i++) res = cRight.solve(build(-0.2, true), dt);
  approx(res.coreStates.get('mc1'), -1, 0.01, 'T-TRI-DECIDE: -lean with gate open must finish Right (-Br)');

  const cClosed = new Circuit();
  for (let i = 0; i < 40; i++) res = cClosed.solve(build(0.2, false), dt);
  approx(res.coreStates.get('mc1'), 0, 1e-4, 'T-TRI-DECIDE: gate never opened must finish Hold regardless of lean');

  const cWeak = new Circuit();
  for (let i = 0; i < 40; i++) res = cWeak.solve(build(0.005, true), dt);
  approx(res.coreStates.get('mc1'), 0, 1e-4, 'T-TRI-DECIDE: a lean too weak to cross Hc must finish Hold even with the gate open');

  console.log('Test 28 OK (T-TRI-DECIDE): same cell finishes Left/Right/Hold from real lean+gate combinations, all vs V0');
}

// Test 29 (T-GROUP-MEM): three cells, each with its own independent write
// path, all threaded through ONE shared group memory core (extra write
// windings, not a scripted "remember the last decision" mechanism). Only
// the currently-dumping cell contributes real current at any moment, so
// the group core's remanence naturally ends up matching whichever cell
// dumped LAST -- that "last write wins" behavior is not implemented
// anywhere, it falls straight out of real ampere-turns superposition.
{
  const N = 20;
  const R = windingR(N, 0.03);
  function build(activeCell, sign) {
    const comps = [0, 1, 2].map((i) => ({
      id: 'lean' + i, type: 'battery', a: 'W' + i, b: 'GND', value: i === activeCell ? sign * 0.2 : 0,
    }));
    return {
      wires: [],
      components: [
        ...comps,
        {
          id: 'grp', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau,
          windings: [0, 1, 2].map((i) => ({ a: 'W' + i, b: 'GND', N, R })),
        },
      ],
    };
  }
  const dt = 1 / 2000;
  const c = new Circuit();
  let res;
  for (let i = 0; i < 40; i++) res = c.solve(build(0, 1), dt); // cell 0 dumps Pos
  approx(res.coreStates.get('grp'), 1, 0.01, 'T-GROUP-MEM: first dump (cell 0, Pos) must set the group core');
  for (let i = 0; i < 40; i++) res = c.solve(build(1, -1), dt); // cell 1 dumps Neg
  approx(res.coreStates.get('grp'), -1, 0.01, 'T-GROUP-MEM: a later dump (cell 1, Neg) must overwrite the group core');
  for (let i = 0; i < 40; i++) res = c.solve(build(2, 1), dt); // cell 2 dumps Pos -- the LAST dump
  approx(res.coreStates.get('grp'), 1, 0.01, 'T-GROUP-MEM: group remanence must match the LAST cell to dump (cell 2, Pos)');
  for (let i = 0; i < 20; i++) res = c.solve(build(-1, 0), dt); // all quiet
  approx(res.coreStates.get('grp'), 1, 0.001, 'T-GROUP-MEM: with all cells quiet, group remanence must hold (Hold)');
  console.log('Test 29 OK (T-GROUP-MEM): group core remanence tracks the last agreed trit, holds when quiet');
}

// Test 30 (T-TOWARD-AWAY): a center cell's own write current is ALSO
// threaded through one coupling winding on each of two neighbor cores --
// wound the SAME way on one neighbor (toward) and the OPPOSITE way on the
// other (away, terminals swapped -- real winding-polarity/dot-convention
// physics, not a scripted rule). When center locks Left, toward must match
// and away must be mirrored; when center locks Right, both flip.
{
  const N = 20;
  const R = windingR(N, 0.03);
  function build(leanV) {
    return {
      wires: [],
      components: [
        { id: 'lean', type: 'battery', a: 'IN', b: 'GND', value: leanV },
        { id: 'r1', type: 'resistor', a: 'IN', b: 'DRIVE', value: 2 },
        { id: 'mcC', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau, windings: [{ a: 'DRIVE', b: 'GND', N, R: R * 2 }] },
        { id: 'mcL', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau, windings: [{ a: 'DRIVE', b: 'LMID', N, R }] },
        // 'away': terminals swapped relative to the physical current path
        { id: 'mcR', type: 'memorycore', hcAmpTurns: SMALL_CORE.hcAmpTurns, phiSat: SMALL_CORE.phiSat, switchTau: SMALL_CORE.switchTau, windings: [{ a: 'RMID', b: 'LMID', N, R }] },
        { id: 'r2', type: 'resistor', a: 'RMID', b: 'GND', value: 0.001 },
      ],
    };
  }
  const dt = 1 / 2000;
  let res;

  const cLeft = new Circuit();
  for (let i = 0; i < 100; i++) res = cLeft.solve(build(5), dt);
  approx(res.coreStates.get('mcC'), 1, 0.01, 'T-TOWARD-AWAY: center must lock Left');
  approx(res.coreStates.get('mcL'), 1, 0.01, 'T-TOWARD-AWAY: toward neighbor must match center (Left)');
  approx(res.coreStates.get('mcR'), -1, 0.01, 'T-TOWARD-AWAY: away neighbor must mirror center (Left -> away locks Right)');

  const cRight = new Circuit();
  for (let i = 0; i < 100; i++) res = cRight.solve(build(-5), dt);
  approx(res.coreStates.get('mcC'), -1, 0.01, 'T-TOWARD-AWAY: center must lock Right');
  approx(res.coreStates.get('mcL'), -1, 0.01, 'T-TOWARD-AWAY: toward neighbor must match center (Right)');
  approx(res.coreStates.get('mcR'), 1, 0.01, 'T-TOWARD-AWAY: away neighbor must mirror center (Right -> away locks Left)');

  const cHold = new Circuit();
  for (let i = 0; i < 40; i++) res = cHold.solve(build(0.001), dt); // far too weak to cross Hc anywhere
  approx(res.coreStates.get('mcC'), 0, 1e-4, 'T-TOWARD-AWAY: Hold -- center must not lock');
  approx(res.coreStates.get('mcL'), 0, 1e-4, 'T-TOWARD-AWAY: Hold -- neither neighbor is written');
  approx(res.coreStates.get('mcR'), 0, 1e-4, 'T-TOWARD-AWAY: Hold -- neither neighbor is written');

  console.log('Test 30 OK (T-TOWARD-AWAY): toward matches center, away mirrors center, both directions, Hold leaves neighbors untouched');
}

// Test 31 (T-WINDOW-3STATE): a real TLV3202-class dual comparator, wired
// as a window detector (channel 1 active-low for "above the window",
// channel 2 active-high for "below the window", the same topology as the
// Stage 1 Real Millivolt Ternary preset), must distinguish all three of
// -20mV, 0mV, and +20mV relative to V0 by its two real HIGH/LOW outputs
// -- no third output pin, no invented trit value, just two real 2-level
// decisions whose combination happens to carry 3 distinguishable states.
{
  const hcRef = 0.01; // window edges at +/-10mV, so a +/-20mV test signal has real margin over the comparator's own ~2mV offset
  function build(signalV) {
    return {
      wires: [],
      components: [
        { id: 'bat1', type: 'battery', a: 'VCC', b: 'GND', value: 5 },
        { id: 'batX', type: 'battery', a: 'X', b: 'GND', value: 2.5 + hcRef },
        { id: 'batY', type: 'battery', a: 'Y', b: 'GND', value: 2.5 - hcRef },
        { id: 'batSig', type: 'battery', a: 'SIGNAL', b: 'GND', value: 2.5 + signalV },
        {
          id: 'cmp', type: 'comparator',
          in1p: 'X', in1m: 'SIGNAL', out1: 'OUT1', // active-low for "above the window" (Right)
          in2p: 'Y', in2m: 'SIGNAL', out2: 'OUT2', // active-high for "below the window" (Left)
          vcc: 'VCC', gnd: 'GND',
        },
      ],
    };
  }
  const dt = 1 / 2000;
  let res;

  const cRight = new Circuit();
  for (let i = 0; i < 20; i++) res = cRight.solve(build(0.02), dt); // SIGNAL = V0 + 20mV
  assert.strictEqual(res.comparatorStates.get('cmp').out1High, false, 'T-WINDOW-3STATE: +20mV must read OUT1 LOW (above the window)');
  assert.strictEqual(res.comparatorStates.get('cmp').out2High, false, 'T-WINDOW-3STATE: +20mV must read OUT2 LOW');

  const cHold = new Circuit();
  for (let i = 0; i < 20; i++) res = cHold.solve(build(0), dt); // SIGNAL = V0
  assert.strictEqual(res.comparatorStates.get('cmp').out1High, true, 'T-WINDOW-3STATE: 0mV must read OUT1 HIGH (inside the window)');
  assert.strictEqual(res.comparatorStates.get('cmp').out2High, false, 'T-WINDOW-3STATE: 0mV must read OUT2 LOW');

  const cLeft = new Circuit();
  for (let i = 0; i < 20; i++) res = cLeft.solve(build(-0.02), dt); // SIGNAL = V0 - 20mV
  assert.strictEqual(res.comparatorStates.get('cmp').out1High, true, 'T-WINDOW-3STATE: -20mV must read OUT1 HIGH');
  assert.strictEqual(res.comparatorStates.get('cmp').out2High, true, 'T-WINDOW-3STATE: -20mV must read OUT2 HIGH (below the window)');

  console.log('Test 31 OK (T-WINDOW-3STATE): -20mV/0mV/+20mV all give distinct (OUT1,OUT2) combinations');
}

// Test 32 (T-DIFFSCOPE): js/app.js's Differential Scope probe must sample
// V(A) - V(B) from the same live per-frame voltages every other probe
// reads (a real subtraction of two real node voltages, never a separate
// signal) -- checked two ways: a static check that the actual sampling
// code computes exactly that difference for a 2-terminal diffscope probe,
// and a numeric check (via the real solver) that the two nodes it would
// read really do differ by the expected real voltage.
{
  const appSrc = fs.readFileSync(path.join(__dirname, '../js/app.js'), 'utf8');
  assert.ok(/p\.type !== 'scope' && p\.type !== 'diffscope'/.test(appSrc), 'T-DIFFSCOPE: sampleScopeProbes must handle diffscope probes');
  const diffSampleMatch = appSrc.match(/if \(p\.type === 'diffscope'\) \{([\s\S]*?)\}/);
  assert.ok(diffSampleMatch, 'T-DIFFSCOPE: could not find the diffscope sampling branch in sampleScopeProbes');
  assert.ok(/va - vb/.test(diffSampleMatch[1]), 'T-DIFFSCOPE: diffscope must compute va - vb (terminal 0 minus terminal 1), not something else');
  assert.ok(/terminals\[0\]\.cellId/.test(diffSampleMatch[1]) && /terminals\[1\]\.cellId/.test(diffSampleMatch[1]), 'T-DIFFSCOPE: diffscope must read its own two terminals, not e.g. terminal 0 twice');

  // numeric check: the same 2.5V split a diffscope on this preset would show
  const c = new Circuit();
  const dt = 1 / 2000;
  let res;
  for (let i = 0; i < 10; i++) {
    res = c.solve({
      wires: [],
      components: [
        { id: 'bat1', type: 'battery', a: 'P', b: 'GND', value: 5 },
        { id: 'vg1', type: 'vgnd', a: 'P', b: 'GND', out: 'V0' },
      ],
    }, dt);
  }
  const vDiff = res.voltages.get(res.uf.find('P')) - res.voltages.get(res.uf.find('V0'));
  approx(vDiff, 2.5, 0.01, 'T-DIFFSCOPE: V(P) - V(V0) must be a real 2.5V difference for a diffscope to show correctly');
  console.log('Test 32 OK (T-DIFFSCOPE): sampling code computes a real terminals[0]-terminals[1] difference, verified against a real 2.5V split');
}

// Test 33 (T-HOLE-COLLIDE): only one component lead may occupy a
// breadboard hole. simulate.js's resolveTerminals() runs the same
// collision check js/app.js's manual-click and AI-build paths do --
// checked here directly against the real Board geometry, since it's a
// pure function with no DOM.
{
  const Sim = require('../simulate.js');
  const Board = require('../js/board.js');
  const board = Board.build(Sim.LAYOUT_PRESETS['1large']);
  board.layoutKey = '1large';

  // two different parts both claiming the exact same physical hole (e,5) -- must be rejected
  const collidingSpec = [
    { type: 'battery', value: 5, terminals: [{ row: 'e', col: 5 }, { row: 'f', col: 5 }] },
    { type: 'resistor', value: 220, terminals: [{ row: 'e', col: 5 }, { row: 'e', col: 10 }] },
  ];
  const { errors: collideErrors } = Sim.resolveTerminals(board, collidingSpec);
  assert.ok(collideErrors.length > 0, 'T-HOLE-COLLIDE: two parts sharing the exact same physical hole must be rejected');
  assert.ok(/same physical hole/.test(collideErrors[0]), 'T-HOLE-COLLIDE: the rejection must explain it is a hole collision');

  // a DIFFERENT hole on the SAME electrical node (same column, different row) must be accepted
  const okSpec = [
    { type: 'battery', value: 5, terminals: [{ row: 'e', col: 5 }, { row: 'f', col: 5 }] },
    { type: 'resistor', value: 220, terminals: [{ row: 'a', col: 5 }, { row: 'e', col: 10 }] },
  ];
  const { errors: okErrors } = Sim.resolveTerminals(board, okSpec);
  assert.strictEqual(okErrors.length, 0, 'T-HOLE-COLLIDE: a different hole on the same electrical node must NOT be rejected (' + okErrors.join('; ') + ')');

  console.log('Test 33 OK (T-HOLE-COLLIDE): same physical hole rejected, different hole on the same node accepted');
}

// Test 34 (T-BOARD2): a part whose terminal names board 1 (the 2nd
// physical board, 0-indexed) must resolve to a real hole on board 1 and
// stay there through resolution and simulation -- not silently fall back
// to board 0. Checked on the same headless path an external harness uses.
{
  const Sim = require('../simulate.js');
  const Board = require('../js/board.js');
  const board = Board.build(Sim.LAYOUT_PRESETS['2large']);
  board.layoutKey = '2large';

  const spec = [
    { type: 'battery', value: 5, terminals: [{ row: 'e', col: 5, board: 1 }, { row: 'f', col: 5, board: 1 }] },
    { type: 'resistor', value: 1000, terminals: [{ row: 'a', col: 5, board: 1 }, { row: 'e', col: 10, board: 1 }] },
  ];
  const { parts, errors } = Sim.resolveTerminals(board, spec);
  assert.strictEqual(errors.length, 0, 'T-BOARD2: a well-formed board-1 spec must resolve cleanly (' + errors.join('; ') + ')');
  parts.forEach((p) => {
    p.terminals.forEach((t) => {
      assert.ok(t.cellId.startsWith('b1:'), 'T-BOARD2: terminal ' + t.cellId + ' must be on board 1 ("b1:..."), not silently on board 0');
    });
  });

  // and the resulting circuit actually solves on board 1's nodes
  const elements = Sim.toEngineElements(parts);
  const c = new Circuit();
  const res = c.solve(elements, 0.001);
  assert.ok(res.voltages.has(res.uf.find('b1:T5')), 'T-BOARD2: the solved circuit must contain board 1\'s own node');

  console.log('Test 34 OK (T-BOARD2): a board-1 terminal resolves to a real board-1 hole and solves on board-1\'s own node');
}

// Test 35 (T-SUPPLY-CONFLICT): two ideal-ish voltage sources wired
// directly across the same two nodes must be flagged as a conflict --
// not silently accepted as though the resulting midpoint voltage were a
// safe, intended operating point. The solver still reports the real
// physics (a genuine circulating current between them), but the warning
// must name it as a conflicting-supply condition specifically.
{
  const c = new Circuit();
  const res = c.solve({
    wires: [],
    components: [
      { id: 'b1', type: 'battery', a: 'P', b: 'GND', value: 5 },
      { id: 'b2', type: 'battery', a: 'P', b: 'GND', value: 9 },
    ],
  }, 0.001);
  const conflictWarning = res.warnings.find((w) => /Conflicting power supplies/.test(w));
  assert.ok(conflictWarning, 'T-SUPPLY-CONFLICT: two different-valued batteries directly across the same nodes must warn "Conflicting power supplies", got: ' + JSON.stringify(res.warnings));
  approx(res.voltages.get(res.uf.find('P')), 7, 0.1, 'T-SUPPLY-CONFLICT: the real (not silently hidden) result is still the physically correct averaged-by-internal-resistance voltage');

  // two batteries that AGREE (same value, same orientation) must NOT warn -- that's just two supplies in parallel, not a conflict
  const c2 = new Circuit();
  const res2 = c2.solve({
    wires: [],
    components: [
      { id: 'b1', type: 'battery', a: 'P', b: 'GND', value: 5 },
      { id: 'b2', type: 'battery', a: 'P', b: 'GND', value: 5 },
    ],
  }, 0.001);
  assert.ok(!res2.warnings.some((w) => /Conflicting power supplies/.test(w)), 'T-SUPPLY-CONFLICT: two agreeing batteries must not be flagged as conflicting');

  console.log('Test 35 OK (T-SUPPLY-CONFLICT): conflicting supplies explicitly flagged, agreeing supplies are not');
}

// Test 36 (T-CAP-POLARITY): a real electrolytic capacitor (value at/above
// the electrolytic threshold) that ends up reverse-biased beyond a real
// part's reverse-voltage rating must warn -- a ceramic (below the
// threshold) at the same reverse voltage must not, since it has no
// polarity to violate.
{
  function buildReverse(value) {
    return {
      wires: [],
      components: [
        { id: 'bat1', type: 'battery', a: 'HI', b: 'GND', value: 5 },
        // capacitor wired backwards: its "+" lead (a) ties to GND, "-" lead (b) to the +5V node --
        // this reverse-biases it by the full 5V once charged
        { id: 'cap1', type: 'capacitor', a: 'GND', b: 'HI', value },
      ],
    };
  }
  const dt = 0.05;
  const cElectro = new Circuit();
  let res;
  for (let i = 0; i < 20; i++) res = cElectro.solve(buildReverse(10e-6), dt); // 10uF: electrolytic
  assert.ok(res.warnings.some((w) => /reverse-biased/.test(w) && /Electrolytic/.test(w)), 'T-CAP-POLARITY: a reverse-biased electrolytic must warn, got: ' + JSON.stringify(res.warnings));

  const cCeramic = new Circuit();
  for (let i = 0; i < 20; i++) res = cCeramic.solve(buildReverse(100e-9), dt); // 100nF: ceramic, no polarity
  assert.ok(!res.warnings.some((w) => /reverse-biased/.test(w)), 'T-CAP-POLARITY: a non-polarized ceramic at the same reverse voltage must not warn');

  console.log('Test 36 OK (T-CAP-POLARITY): reverse-biased electrolytic warns, reverse-biased ceramic does not');
}

// Test 37 (T-MONTE-CARLO): simulate.js's tolerance/Monte-Carlo mode must
// actually perturb real component values within their real, honest
// manufacturing tolerance (CircuitEngine.COMPONENT_TOLERANCE) -- not just
// report the one perfect nominal case -- and the resulting spread on a
// plain resistor divider must land inside what real +/-5% resistors and a
// real +/-2% supply can actually produce, checked against the analytic
// worst-case bound, not just "some nonzero spread happened".
{
  const Sim = require('../simulate.js');
  const Board = require('../js/board.js');
  const board = Board.build(Sim.LAYOUT_PRESETS['1large']);
  board.layoutKey = '1large';

  // same seed twice must reproduce identically -- a real tolerance run has
  // to be reproducible for a design review, not a new answer every time
  const spec = [
    { type: 'battery', value: 9, terminals: [{ row: 'e', col: 5 }, { row: 'f', col: 5 }] },
    { type: 'resistor', value: 1000, terminals: [{ row: 'c', col: 5 }, { row: 'c', col: 10 }] },
    { type: 'resistor', value: 1000, terminals: [{ row: 'd', col: 10 }, { row: 'h', col: 10 }] },
    { type: 'wire', terminals: [{ row: 'i', col: 5 }, { row: 'i', col: 10 }] },
  ];
  const { parts } = Sim.resolveTerminals(board, spec);
  const sim = { seconds: 0.02, dt: 0.001 };

  const reportA = Sim.runMonteCarlo(parts, sim, { trials: 300, seed: 42, watch: [{ label: 'mid', path: 'voltages.b0:T10' }] });
  const reportB = Sim.runMonteCarlo(parts, sim, { trials: 300, seed: 42, watch: [{ label: 'mid', path: 'voltages.b0:T10' }] });
  assert.deepStrictEqual(reportA.summary.mid, reportB.summary.mid, 'T-MONTE-CARLO: the same seed must reproduce the exact same trial statistics');

  // an even 1k/1k divider off a 9V supply sits at 4.5V nominal; two
  // independent +/-5% resistors plus a +/-2% supply can worst-case push
  // the midpoint roughly +/-(5%+2.5%+2%) ~= +/-9.5% of 4.5V -- real
  // sampled trials must fall well inside that bound and must NOT all be
  // exactly 4.5V (that would mean tolerance isn't actually being applied)
  const { min, max, stdev } = reportA.summary.mid;
  const nominal = 4.5;
  assert.ok(stdev > 0.01, 'T-MONTE-CARLO: trials must show real spread from part tolerance, not all land on the exact nominal value');
  assert.ok(min > nominal * 0.85 && max < nominal * 1.15, 'T-MONTE-CARLO: spread must stay within the real worst-case bound for +/-5% resistors and a +/-2% supply, got min=' + min + ' max=' + max);
  assert.strictEqual(reportA.trials, 300, 'T-MONTE-CARLO: must run exactly the requested trial count');

  console.log('Test 37 OK (T-MONTE-CARLO): 300 seeded trials reproduce identically, midpoint spread', min.toFixed(3), '-', max.toFixed(3), 'V (nominal', nominal, 'V) from real part tolerance');
}

// Test 38 (T-DIFFSOURCE): a real mV differential source (V = V0 + deltaV,
// real source impedance) must hold its commanded deltaV across whatever
// its reference pin is wired to, under a light real load -- exactly the
// same ideal-EMF-plus-series-resistance structure as a battery, just
// referenced to a real node instead of an absolute rail. Its optional
// noise must be real (non-zero spread) and reproducible from the same
// seed, not fresh randomness every run.
{
  const els = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
      { id: 'src1', type: 'diffsource', a: 'LEAN', b: 'V0', value: 0.02, sourceR: 300 },
      { id: 'rload', type: 'resistor', a: 'LEAN', b: 'V0', value: 1e6 },
    ],
  };
  const c = new Circuit();
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 1 / 2000);
  const vLean = res.voltages.get(res.uf.find('LEAN'));
  const vV0 = res.voltages.get(res.uf.find('V0'));
  approx(vLean - vV0, 0.02, 1e-4, 'T-DIFFSOURCE: LEAN must sit deltaV above V0 under a light real load');

  // same seed twice must reproduce the exact same noise sequence
  const elsNoisy = {
    wires: [],
    components: [
      { id: 'bat1', type: 'battery', a: 'P', b: 'M', value: 5 },
      { id: 'vg1', type: 'vgnd', a: 'P', b: 'M', out: 'V0' },
      { id: 'src1', type: 'diffsource', a: 'LEAN', b: 'V0', value: 0.02, sourceR: 300, noiseRms: 0.005, noiseSeed: 7 },
      { id: 'rload', type: 'resistor', a: 'LEAN', b: 'V0', value: 1e6 },
    ],
  };
  function runNoisy() {
    const cc = new Circuit();
    const decisions = [];
    for (let i = 0; i < 20; i++) {
      const r = cc.solve(elsNoisy, 1 / 2000);
      decisions.push(r.voltages.get(r.uf.find('LEAN')) - r.voltages.get(r.uf.find('V0')));
    }
    return decisions;
  }
  const runA = runNoisy();
  const runB = runNoisy();
  assert.deepStrictEqual(runA, runB, 'T-DIFFSOURCE: the same noiseSeed must reproduce the exact same noise sequence');
  const meanA = runA.reduce((a, b) => a + b, 0) / runA.length;
  const varA = runA.reduce((a, b) => a + (b - meanA) ** 2, 0) / runA.length;
  approx(meanA, 0.02, 0.01, 'T-DIFFSOURCE: noisy samples must still average near the commanded deltaV');
  assert.ok(Math.sqrt(varA) > 0.001, 'T-DIFFSOURCE: noiseRms must actually produce real sample-to-sample spread, not a constant value');

  console.log('Test 38 OK (T-DIFFSOURCE): LEAN = V0 + 20mV under load, noise reproducible from its seed with real spread (stdev', Math.sqrt(varA).toFixed(4), 'V)');
}

// Test 39 (T-NAMED-NODES): simulate.js's nodeNames must resolve a real
// declared name to the exact same electrical node as any part wired to
// that hole's bus (a pure label, no new topology), and named measurements
// must report the real solved difference between two such names.
{
  const Sim = require('../simulate.js');
  const Board = require('../js/board.js');
  const AI = require('../js/ai.js');
  const board = Board.build(Sim.LAYOUT_PRESETS['1large']);
  board.layoutKey = '1large';

  const spec = {
    layout: '1large',
    nodeNames: { V0: { row: 'e', col: 20 }, LEAN: { row: 'c', col: 25 } },
    parts: [
      { id: 'bat1', type: 'battery', value: 9, terminals: [{ row: 'e', col: 5 }, { row: 'f', col: 5 }] },
      { id: 'vg1', type: 'vgnd', terminals: [{ row: 'd', col: 5 }, { row: 'g', col: 5 }, { row: 'e', col: 20 }] },
      { id: 'lean1', type: 'diffsource', value: 0.02, sourceR: 300, terminals: [{ row: 'c', col: 25 }, { row: 'a', col: 20 }] },
    ],
    measurements: [{ label: 'Decision', a: 'LEAN', b: 'V0' }],
  };
  const { parts } = Sim.resolveTerminals(board, AI.validateSpec(spec).parts);
  const { names, errors: nameErrors } = Sim.resolveNodeNames(board, spec.nodeNames);
  assert.strictEqual(nameErrors.length, 0, 'T-NAMED-NODES: real hole references must resolve cleanly');

  const elements = Sim.toEngineElements(parts);
  const c = new Circuit();
  let res;
  for (let i = 0; i < 30; i++) res = c.solve(elements, 1 / 2000);
  const snap = Sim.snapshot(res, { nodeNameCellIds: names, measurements: spec.measurements });
  approx(snap.namedVoltages.V0, 4.5, 0.01, 'T-NAMED-NODES: named V0 must read the real solved vgnd midpoint');
  approx(snap.measurements.Decision, 0.02, 0.001, 'T-NAMED-NODES: named measurement Decision must read the real LEAN-V0 difference');

  // an explicit part "id" must be used as-is (not renumbered), so a
  // component-keyed result (currents here) is addressable by that name
  assert.ok('lean1' in snap.currents, 'T-NAMED-NODES: an explicit part id must be preserved as the real component id');

  console.log('Test 39 OK (T-NAMED-NODES): named V0 =', snap.namedVoltages.V0.toFixed(3), 'V, Decision =', (snap.measurements.Decision * 1000).toFixed(2), 'mV');
}

// Test 40 (T-SWEEP): simulate.js's parameter sweep must actually vary the
// declared part field across the declared range and re-solve at each
// point -- checked against the real linear divider response, not just
// "some numbers came back".
{
  const Sim = require('../simulate.js');
  const Board = require('../js/board.js');
  const AI = require('../js/ai.js');
  const board = Board.build(Sim.LAYOUT_PRESETS['1large']);
  board.layoutKey = '1large';
  const spec = {
    layout: '1large',
    nodeNames: { V0: { row: 'e', col: 20 }, LEAN: { row: 'c', col: 25 } },
    parts: [
      { id: 'bat1', type: 'battery', value: 9, terminals: [{ row: 'e', col: 5 }, { row: 'f', col: 5 }] },
      { id: 'vg1', type: 'vgnd', terminals: [{ row: 'd', col: 5 }, { row: 'g', col: 5 }, { row: 'e', col: 20 }] },
      { id: 'lean1', type: 'diffsource', value: 0, sourceR: 300, terminals: [{ row: 'c', col: 25 }, { row: 'a', col: 20 }] },
    ],
    measurements: [{ label: 'Decision', a: 'LEAN', b: 'V0' }],
  };
  const { parts } = Sim.resolveTerminals(board, AI.validateSpec(spec).parts);
  const { names } = Sim.resolveNodeNames(board, spec.nodeNames);
  const snapOpts = { nodeNameCellIds: names, measurements: spec.measurements };
  const report = Sim.runSweep(parts, { seconds: 0.02, dt: 0.001 }, { partId: 'lean1', field: 'value', from: -0.1, to: 0.1, steps: 5 }, snapOpts);
  assert.strictEqual(report.points.length, 5, 'T-SWEEP: must produce exactly the requested number of points');
  const expected = [-0.1, -0.05, 0, 0.05, 0.1];
  report.points.forEach((p, i) => {
    approx(p.value, expected[i], 1e-9, 'T-SWEEP: sweep point ' + i + ' must land on the declared linear value');
    approx(p.measurements.Decision, expected[i], 0.002, 'T-SWEEP: Decision must track the swept deltaV at point ' + i);
  });
  console.log('Test 40 OK (T-SWEEP): 5-point sweep from -100mV to +100mV tracks Decision at every point');
}

// Test 41 (T-EXPERIMENT): simulate.js's staged experiment runner must (a)
// detect a real threshold-crossing event with an interpolated time between
// the two straddling solves, and (b) correctly measure persistence -- a
// real memory-core write followed by a real release, checked with the
// SAME real remanence physics T-CORE-LOCK/T-GATE-MEM already prove, not a
// separate scripted result.
{
  const Sim = require('../simulate.js');
  const Board = require('../js/board.js');
  const AI = require('../js/ai.js');
  const board = Board.build(Sim.LAYOUT_PRESETS['1large']);
  board.layoutKey = '1large';
  const spec = {
    layout: '1large',
    nodeNames: { V0: { row: 'e', col: 20 }, WRITE: { row: 'c', col: 25 } },
    parts: [
      { id: 'bat1', type: 'battery', value: 9, terminals: [{ row: 'e', col: 5 }, { row: 'f', col: 5 }] },
      { id: 'vg1', type: 'vgnd', terminals: [{ row: 'd', col: 5 }, { row: 'g', col: 5 }, { row: 'e', col: 20 }] },
      { id: 'drv1', type: 'diffsource', value: 0, sourceR: 1, terminals: [{ row: 'c', col: 25 }, { row: 'a', col: 20 }] },
      { id: 'mc1', type: 'memorycore', turns: [20], core: 'small', terminals: [{ row: 'd', col: 25 }, { row: 'b', col: 20 }] },
    ],
  };
  const { parts } = Sim.resolveTerminals(board, AI.validateSpec(spec).parts);
  const { names } = Sim.resolveNodeNames(board, spec.nodeNames);
  const snapOpts = { nodeNameCellIds: names, measurements: [] };
  const experiment = {
    stages: [
      { name: 'settle', seconds: 0.01, dt: 0.0005 },
      { name: 'write', seconds: 0.02, dt: 0.0005, set: [{ partId: 'drv1', field: 'value', value: 0.5 }] },
      { name: 'release', seconds: 0.05, dt: 0.0005, set: [{ partId: 'drv1', field: 'value', value: 0 }] },
    ],
    events: [{ label: 'core_lock', core: 'mc1', threshold: 0.9, direction: 'rising' }],
    persistence: { label: 'CoreHold', core: 'mc1', baselineStage: 'write', holdStage: 'release', minDelta: 0.5 },
  };
  const result = Sim.runExperiment(parts, experiment, snapOpts);
  assert.strictEqual(result.errors.length, 0, 'T-EXPERIMENT: a well-formed staged experiment must run without errors');
  approx(result.stages[1].snapshot.coreStates.mc1, 1, 0.001, 'T-EXPERIMENT: the write stage must actually saturate the core (real ampere-turns past Hc)');

  assert.strictEqual(result.events.length, 1, 'T-EXPERIMENT: the core-lock threshold crossing must be detected exactly once');
  const ev = result.events[0];
  assert.strictEqual(ev.stage, 'write', 'T-EXPERIMENT: the crossing must be attributed to the write stage');
  assert.ok(ev.t > 0.01 && ev.t < 0.03, 'T-EXPERIMENT: the interpolated crossing time must fall within the write stage window, got ' + ev.t);
  assert.ok(ev.valueBefore < 0.9 && ev.valueAfter >= 0.9, 'T-EXPERIMENT: the recorded before/after values must straddle the declared threshold');

  assert.strictEqual(result.persistence.baseline, 0, 'T-EXPERIMENT: persistence baseline must be the real pre-write state (demagnetized)');
  assert.ok(result.persistence.distinguishable, 'T-EXPERIMENT: remanence must stay distinguishable from the pre-write baseline throughout release, got minObservedDelta=' + result.persistence.minObservedDelta);
  approx(result.persistence.minObservedDelta, 1, 0.001, 'T-EXPERIMENT: remanence must not meaningfully decay during release (real DC memory, not volatile)');

  console.log('Test 41 OK (T-EXPERIMENT): core-lock event at t=', ev.t.toFixed(6), 's, persistence minObservedDelta=', result.persistence.minObservedDelta.toFixed(4));
}

// Test 42 (T-NO-MACRO): the new calibration example presets in js/app.js
// must be built from real discrete parts (nmos/pmos), not the legacy
// ternarycell macro -- a static source check since app.js itself needs a
// DOM and can't be required directly from this Node test.
{
  const appSrc = fs.readFileSync(path.join(__dirname, '../js/app.js'), 'utf8');
  const calPresetNames = ['presetCalAParts', 'presetCalBParts', 'presetCalCParts', 'presetCalDParts', 'presetCalEParts', 'presetMemoryCellParts', 'presetCalFParts', 'presetCalGParts', 'presetCalHParts', 'presetStage1TernaryParts'];
  calPresetNames.forEach((name) => {
    const m = appSrc.match(new RegExp('function ' + name + '\\(\\) \\{([\\s\\S]*?)\\n  \\}'));
    assert.ok(m, 'T-NO-MACRO: could not find ' + name + ' in js/app.js to check');
    assert.ok(!m[1].includes('ternarycell'), 'T-NO-MACRO: ' + name + ' must not reference the legacy ternarycell macro');
  });
  console.log('Test 42 OK (T-NO-MACRO): all', calPresetNames.length, 'calibration presets are built from real discrete parts, no ternarycell macro');
}

console.log('\nAll circuit engine tests passed.');
