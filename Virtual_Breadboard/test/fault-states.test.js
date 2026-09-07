#!/usr/bin/env node
/*
 * Explicit fault-state taxonomy: OPEN, SHORT, FLOATING, OVER-CURRENT,
 * NO REFERENCE, SOLVER FAILED. Per the review this answers: the simulator
 * must never replace an impossible circuit with a nice-looking waveform --
 * every check here builds a REAL fault circuit and asserts the real named
 * state comes back, not just a plausible-looking number.
 *
 * CircuitEngine.diagnose(elements, result) is read-only: it never changes
 * a single solved value, only names what solve() already computed.
 */
const assert = require('assert');
const CircuitEngine = require('../js/circuit.js');
const { Circuit } = CircuitEngine;

let checkCount = 0;
function check(name, condition, note) {
  checkCount++;
  const line = `${condition ? 'PASS' : 'FAIL'} [${name}]${note ? ' -- ' + note : ''}`;
  console.log(line);
  assert.ok(condition, `FAULT-STATE CHECK FAILED: ${name}${note ? ' -- ' + note : ''}`);
}

console.log('=== NO REFERENCE ===');
{
  const c = new Circuit();
  const els = { wires: [], components: [{ id: 'r1', type: 'resistor', value: 1000, a: 'x', b: 'y' }] };
  const res = c.solve(els, 0.001);
  const d = CircuitEngine.diagnose(els, res);
  check('no-battery-no-diffsource-flags-no-reference', d.noReference === true, 'a circuit with no real source anchoring 0V must be named NO REFERENCE');

  const c2 = new Circuit();
  const els2 = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 5, a: 'p', b: 'g' }, { id: 'r1', type: 'resistor', value: 1000, a: 'p', b: 'g' }] };
  const res2 = c2.solve(els2, 0.001);
  const d2 = CircuitEngine.diagnose(els2, res2);
  check('a-real-battery-clears-no-reference', d2.noReference === false, 'a circuit with a real battery must NOT be flagged NO REFERENCE');
}

console.log('\n=== SHORT ===');
{
  const c = new Circuit();
  const els = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 9, a: 'p', b: 'g' }, { id: 'r1', type: 'resistor', value: 0.001, a: 'p', b: 'g' }] };
  const res = c.solve(els, 0.001);
  const d = CircuitEngine.diagnose(els, res);
  check('near-zero-resistance-across-supply-flags-short', d.shorts.length > 0, `a real 1milliohm load across a 9V supply must hit the real current limit and be classified SHORT, got shorts=${JSON.stringify(d.shorts)}`);

  const c2 = new Circuit();
  const els2 = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 9, a: 'p', b: 'g' }, { id: 'r1', type: 'resistor', value: 10000, a: 'p', b: 'g' }] };
  const res2 = c2.solve(els2, 0.001);
  const d2 = CircuitEngine.diagnose(els2, res2);
  check('a-real-load-does-not-falsely-flag-short', d2.shorts.length === 0, 'a normal 10k load must never be misclassified as a short');
}

console.log('\n=== OVER-CURRENT ===');
{
  const c = new Circuit();
  const els = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 5, a: 'p', b: 'g' }, { id: 'r1', type: 'resistor', value: 10, a: 'p', b: 'anode' }, { id: 'led1', type: 'led', a: 'anode', b: 'g', color: 'red' }] };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(els, 0.0001);
  const d = CircuitEngine.diagnose(els, res);
  check('undersized-limiter-flags-overcurrent', d.overCurrent.length > 0, `a 10ohm limiter driving an LED must produce a real overcurrent condition, got overCurrent=${JSON.stringify(d.overCurrent)}`);

  const c2 = new Circuit();
  const els2 = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 5, a: 'p', b: 'g' }, { id: 'r1', type: 'resistor', value: 1000, a: 'p', b: 'anode' }, { id: 'led1', type: 'led', a: 'anode', b: 'g', color: 'red' }] };
  let res2;
  for (let i = 0; i < 5; i++) res2 = c2.solve(els2, 0.0001);
  const d2 = CircuitEngine.diagnose(els2, res2);
  check('a-real-current-limiting-resistor-does-not-falsely-flag-overcurrent', d2.overCurrent.length === 0, 'a properly-sized 1k limiter must never be misclassified as overcurrent');
}

console.log('\n=== FLOATING ===');
{
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'vref', type: 'battery', value: 2.5, a: 'ref', b: 'gnd' },
    { id: 'cmp1', type: 'comparator', out1: 'out1', in1m: 'ref', in1p: 'floatpin', gnd: 'gnd', in2p: 'gnd', in2m: 'gnd', out2: 'unused2', vcc: 'vcc' },
  ] };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(els, 0.0001);
  const d = CircuitEngine.diagnose(els, res);
  check('genuinely-dangling-comparator-input-flags-floating', d.floatingNodes.includes('floatpin'), `a comparator input wired to nothing else must be reported FLOATING, got floatingNodes=${JSON.stringify(d.floatingNodes)}`);

  const c2 = new Circuit();
  const els2 = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'vref', type: 'battery', value: 2.5, a: 'ref', b: 'gnd' },
    { id: 'vsrc', type: 'diffsource', value: 1.0, sourceR: 10, a: 'in', b: 'gnd' },
    { id: 'cmp1', type: 'comparator', out1: 'out1', in1m: 'ref', in1p: 'in', gnd: 'gnd', in2p: 'gnd', in2m: 'gnd', out2: 'unused2', vcc: 'vcc' },
  ] };
  let res2;
  for (let i = 0; i < 5; i++) res2 = c2.solve(els2, 0.0001);
  const d2 = CircuitEngine.diagnose(els2, res2);
  check('a-really-connected-input-is-not-flagged-floating', !d2.floatingNodes.includes('in'), 'a comparator input with a real diffsource driving it must never be misclassified as floating');

  // A node genuinely disconnected from the rest of the circuit entirely
  // (not just a high-Z input) must also show up.
  const c3 = new Circuit();
  const els3 = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'p', b: 'g' },
    { id: 'r1', type: 'resistor', value: 1000, a: 'p', b: 'g' },
    { id: 'r2', type: 'resistor', value: 1000, a: 'isolated1', b: 'isolated2' },
  ] };
  const res3 = c3.solve(els3, 0.001);
  const d3 = CircuitEngine.diagnose(els3, res3);
  check('a-whole-unconnected-branch-flags-floating', d3.floatingNodes.includes('isolated1') && d3.floatingNodes.includes('isolated2'), `a resistor wired to nothing else in the circuit must have both its real nodes reported FLOATING, got ${JSON.stringify(d3.floatingNodes)}`);
}

console.log('\n=== OPEN ===');
{
  const c = new Circuit();
  const els = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 5, a: 'p', b: 'g' }, { id: 'sw1', type: 'switch', a: 'p', b: 'x', closed: false }, { id: 'r1', type: 'resistor', value: 1000, a: 'x', b: 'g' }] };
  const res = c.solve(els, 0.001);
  const d = CircuitEngine.diagnose(els, res);
  check('open-switch-is-named-open', d.openComponents.some((o) => o.id === 'sw1'), `an open switch must be reported in openComponents, got ${JSON.stringify(d.openComponents)}`);

  const c2 = new Circuit();
  const els2 = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 5, a: 'p', b: 'g' }, { id: 'sw1', type: 'switch', a: 'p', b: 'x', closed: true }, { id: 'r1', type: 'resistor', value: 1000, a: 'x', b: 'g' }] };
  const res2 = c2.solve(els2, 0.001);
  const d2 = CircuitEngine.diagnose(els2, res2);
  check('closed-switch-is-not-named-open', !d2.openComponents.some((o) => o.id === 'sw1'), 'a real closed switch must never be misclassified as open');

  const c3 = new Circuit();
  const els3 = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' }, { id: 'gsrc', type: 'battery', value: 0, a: 'gate', b: 'gnd' }, { id: 'rdrain', type: 'resistor', value: 1000, a: 'vcc', b: 'drain' }, { id: 'q1', type: 'nmos', value: 1.5, gate: 'gate', drain: 'drain', source: 'gnd' }] };
  const res3 = c3.solve(els3, 0.0001);
  const d3 = CircuitEngine.diagnose(els3, res3);
  check('mosfet-below-threshold-is-named-open', d3.openComponents.some((o) => o.id === 'q1' && o.reason === 'channel off'), `a MOSFET below its threshold voltage must be reported open (channel off), got ${JSON.stringify(d3.openComponents)}`);
}

console.log('\n=== SOLVER FAILED ===');
{
  // A genuinely finite, real circuit must never itself report SOLVER FAILED.
  const c = new Circuit();
  const els = { wires: [], components: [{ id: 'bat1', type: 'battery', value: 9, a: 'p', b: 'g' }, { id: 'r1', type: 'resistor', value: 1000, a: 'p', b: 'g' }] };
  const res = c.solve(els, 0.001);
  const d = CircuitEngine.diagnose(els, res);
  check('a-real-well-posed-circuit-never-flags-solver-failed', d.solverFailed === false, 'an ordinary resistor divider must never be reported as a solver failure');

  // Directly exercise the NaN/Infinity detector itself (the real trigger
  // for this state) without needing to construct a genuinely singular
  // matrix -- diagnose() only reads result.voltages/currents, so a
  // synthetic result proves the detector fires on the real signal it's
  // defined against.
  const fakeResult = { voltages: new Map([['x', NaN]]), currents: new Map(), warnings: [], uf: res.uf, groundRoot: res.groundRoot };
  const dFake = CircuitEngine.diagnose({ components: [] }, fakeResult);
  check('nan-in-solved-state-flags-solver-failed', dFake.solverFailed === true, 'any NaN in the solved voltages/currents must be named SOLVER FAILED, never silently passed through as a real number');
}

console.log(`\n=== ALL ${checkCount} FAULT-STATE CHECKS PASSED ===`);
