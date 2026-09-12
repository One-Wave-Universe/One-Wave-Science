#!/usr/bin/env node
'use strict';

/*
 * Qualification for SPICE-style analysis helpers.
 * Expected values are analytic circuit equations, not copied solver output.
 */

const CircuitEngine = require('../js/circuit.js');
const { dcSweep, sweepValues } = require('../js/spice-analysis.js');

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`SPICE ANALYSIS QUALIFICATION FAILED: ${name}`);
}
function near(name, actual, expected, tol) {
  check(name, Number.isFinite(actual) && Math.abs(actual - expected) <= tol,
    `expected=${expected} actual=${actual} tolerance=${tol}`);
}

console.log('=== SPICE-style DC sweep qualification ===');

{
  const vals = sweepValues(0, 1, 0.1);
  check('decimal-sweep-hits-stop', vals.length === 11 && vals[vals.length - 1] === 1,
    `points=${vals.length} last=${vals[vals.length - 1]}`);
  const descending = sweepValues(1, -1, -0.5);
  check('descending-sweep', descending.join(',') === '1,0.5,0,-0.5,-1', descending.join(','));
}

{
  // 0..10V source, real battery Rint, two 1k resistors.  Analytic answer:
  // I = Vs / (Rint + R1 + R2), Vmid = I*R2.
  const R1 = 1000;
  const R2 = 1000;
  const total = CircuitEngine.BATTERY_RINT + R1 + R2;
  const elements = {
    wires: [],
    components: [
      { id: 'VIN', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: R1, a: 'vin', b: 'mid' },
      { id: 'R2', type: 'resistor', value: R2, a: 'mid', b: 'gnd' },
    ],
  };
  const sweep = dcSweep(elements, {
    sourceId: 'VIN', start: 0, stop: 10, step: 2,
    probes: [
      { type: 'voltage', node: 'mid' },
      { type: 'current', componentId: 'R1' },
    ],
  });

  check('dc-sweep-row-count', sweep.rows.length === 6, `rows=${sweep.rows.length}`);
  sweep.rows.forEach((row) => {
    const expectedI = row.sourceValue / total;
    const expectedMid = expectedI * R2;
    near(`divider-vmid-at-${row.sourceValue}V`, row.values['V(mid)'], expectedMid, 1e-6);
    near(`divider-current-at-${row.sourceValue}V`, row.values['I(R1)'], expectedI, 1e-9);
    check(`finite-at-${row.sourceValue}V`, row.finite === true);
  });
}

{
  // A diode sweep proves the analysis is exercising the nonlinear solver,
  // not merely scaling a precomputed linear answer.  Below Vf it should be
  // essentially off; above Vf it must conduct and the current must rise.
  const elements = {
    wires: [],
    components: [
      { id: 'VIN', type: 'battery', value: 0, a: 'vin', b: 'gnd' },
      { id: 'R', type: 'resistor', value: 1000, a: 'vin', b: 'd' },
      { id: 'D', type: 'diode', a: 'd', b: 'gnd' },
    ],
  };
  const sweep = dcSweep(elements, {
    sourceId: 'VIN', start: 0, stop: 2, step: 0.25,
    probes: [{ type: 'current', componentId: 'D' }],
  });
  const currents = sweep.rows.map((r) => r.values['I(D)']);
  check('diode-off-below-threshold', Math.abs(currents[1]) < 1e-6, `I@0.25V=${currents[1]}`);
  check('diode-conducts-above-threshold', currents[currents.length - 1] > 5e-4,
    `I@2V=${currents[currents.length - 1]}`);
  check('diode-sweep-is-monotonic', currents.every((v, i) => i === 0 || v >= currents[i - 1] - 1e-12),
    currents.join(','));
}

console.log(`\n=== ALL ${checks} SPICE-ANALYSIS CHECKS PASSED ===`);
