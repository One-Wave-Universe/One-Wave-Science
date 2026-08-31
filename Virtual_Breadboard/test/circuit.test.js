const assert = require('assert');
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

console.log('\nAll circuit engine tests passed.');
