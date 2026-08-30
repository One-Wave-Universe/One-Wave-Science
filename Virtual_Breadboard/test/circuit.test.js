const assert = require('assert');
const { Circuit } = require('../js/circuit.js');

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

// Test 10: a Y-split wire is just two zero-resistance ties sharing an
// endpoint (root->end-B, root->branch) — confirm all 3 holes end up as one
// electrical node, the mechanism app.js's Y-split wire relies on.
{
  const c = new Circuit();
  const els = {
    wires: [{ a: 'A', b: 'B' }, { a: 'A', b: 'C' }],
    components: [
      { id: 'bat1', type: 'battery', a: 'A', b: 'M', value: 9 },
      { id: 'r1', type: 'resistor', a: 'C', b: 'M', value: 1000 },
    ],
  };
  const res = c.solve(els, 1 / 60);
  const vA = res.voltages.get(res.uf.find('A'));
  const vB = res.voltages.get(res.uf.find('B'));
  const vC = res.voltages.get(res.uf.find('C'));
  approx(vA, vB, 1e-9, 'Y-split: end A and end B should be the same node');
  approx(vA, vC, 1e-9, 'Y-split: end A and the branch should be the same node');
  approx(res.currents.get('r1'), 9 / 1001, 1e-3, 'current flows through the branch as expected');
  console.log('Test 10 OK: Y-split ties all 3 holes to one node, V =', vA.toFixed(3), 'V');
}

console.log('\nAll circuit engine tests passed.');
