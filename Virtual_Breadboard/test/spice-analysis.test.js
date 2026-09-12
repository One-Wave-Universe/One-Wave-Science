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
  // 0..10V source, real battery Rint, two 1k resistors. The production
  // solver deliberately stamps GMIN=1e-9 S from every non-ground node to
  // ground so partially-wired breadboards stay numerically solvable. A
  // microvolt-grade qualification must therefore include that declared
  // numerical conductance in the independent nodal equations rather than
  // pretending the solver solves a different matrix.
  //
  // KCL:
  //   vin: (vin-Vs)/Rint + (vin-mid)/R1 + GMIN*vin = 0
  //   mid: (mid-vin)/R1 + mid/R2 + GMIN*mid = 0
  const R1 = 1000;
  const R2 = 1000;
  const Rint = CircuitEngine.BATTERY_RINT;
  const GMIN = 1e-9; // mirrors the explicitly documented/stamped solver floor

  function expectedDivider(Vs) {
    const a11 = 1 / Rint + 1 / R1 + GMIN;
    const a12 = -1 / R1;
    const a21 = -1 / R1;
    const a22 = 1 / R1 + 1 / R2 + GMIN;
    const b1 = Vs / Rint;
    const det = a11 * a22 - a12 * a21;
    const vin = (b1 * a22) / det;
    const mid = (-a21 * b1) / det;
    return { mid, currentR1: (vin - mid) / R1 };
  }

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
    const expected = expectedDivider(row.sourceValue);
    near(`divider-vmid-at-${row.sourceValue}V`, row.values['V(mid)'], expected.mid, 1e-9);
    near(`divider-current-at-${row.sourceValue}V`, row.values['I(R1)'], expected.currentR1, 1e-12);
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
