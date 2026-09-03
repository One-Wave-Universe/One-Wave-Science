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
  // steady state: R includes the battery's own internal resistance too
  const totalR = 100 + CircuitEngine.BATTERY_RINT;
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

// Test 24 (T-NO-MACRO): the new calibration example presets in js/app.js
// must be built from real discrete parts (nmos/pmos), not the legacy
// ternarycell macro -- a static source check since app.js itself needs a
// DOM and can't be required directly from this Node test.
{
  const appSrc = fs.readFileSync(path.join(__dirname, '../js/app.js'), 'utf8');
  const calPresetNames = ['presetCalAParts', 'presetCalBParts', 'presetCalCParts', 'presetCalDParts', 'presetCalEParts', 'presetMemoryCellParts'];
  calPresetNames.forEach((name) => {
    const m = appSrc.match(new RegExp('function ' + name + '\\(\\) \\{([\\s\\S]*?)\\n  \\}'));
    assert.ok(m, 'T-NO-MACRO: could not find ' + name + ' in js/app.js to check');
    assert.ok(!m[1].includes('ternarycell'), 'T-NO-MACRO: ' + name + ' must not reference the legacy ternarycell macro');
  });
  console.log('Test 24 OK (T-NO-MACRO): all', calPresetNames.length, 'calibration presets are built from real discrete parts, no ternarycell macro');
}

console.log('\nAll circuit engine tests passed.');
