#!/usr/bin/env node
'use strict';

const CircuitEngine = require('../js/circuit.js');
const { operatingPoint } = require('../js/spice-analysis.js');

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`DC OPERATING POINT QUALIFICATION FAILED: ${name}`);
}
function near(name, actual, expected, tolerance) {
  check(name, Number.isFinite(actual) && Math.abs(actual - expected) <= tolerance,
    `expected=${expected} actual=${actual} tolerance=${tolerance}`);
}

console.log('=== True DC operating point qualification ===');

// Capacitor rule: at DC the capacitor is open, regardless of transient history.
const rc = {
  wires: [],
  components: [
    { id: 'VIN', type: 'battery', value: 5, a: 'vin', b: 'gnd' },
    { id: 'R', type: 'resistor', value: 1000, a: 'vin', b: 'out' },
    { id: 'C', type: 'capacitor', value: 100e-6, a: 'out', b: 'gnd' },
  ],
};

const op1 = operatingPoint(rc);
check('op-identifies-analysis-mode', op1.analysis && op1.analysis.type === 'op');
check('capacitor-is-open-at-dc', op1.currents.get('C') === 0, `I(C)=${op1.currents.get('C')}`);
check('capacitor-removed-from-dc-network',
  !op1.dcElements.components.some((c) => c.id === 'C'));
check('dc-output-rises-to-source-not-transient-initial-condition',
  op1.voltages.get('out') > 4.99, `V(out)=${op1.voltages.get('out')}`);
check('op-converged', op1.solver && op1.solver.converged === true,
  JSON.stringify(op1.solver));

// Create substantial transient history in a completely separate solver, then
// prove .op gives the same answer because it always starts from a fresh state.
const transient = new CircuitEngine.Circuit();
for (let i = 0; i < 200; i++) transient.solve(rc, 0.005);
const opAfterHistory = operatingPoint(rc);
near('op-is-independent-of-prior-transient-capacitor-history',
  opAfterHistory.voltages.get('out'), op1.voltages.get('out'), 1e-12);
near('op-capacitor-current-stays-zero-after-transient-history',
  opAfterHistory.currents.get('C'), 0, 0);

// Inductor rule: DC removes reactance but keeps the solver's declared physical
// winding DCR rather than replacing the coil with an impossible zero-ohm wire.
const L = 10e-3;
const R = 100;
const rl = {
  wires: [],
  components: [
    { id: 'VIN', type: 'battery', value: 5, a: 'vin', b: 'gnd' },
    { id: 'R', type: 'resistor', value: R, a: 'vin', b: 'out' },
    { id: 'L', type: 'inductor', value: L, a: 'out', b: 'gnd' },
  ],
};
const opL = operatingPoint(rl);
const dcr = CircuitEngine.inductorDCR(L);
const dcInductor = opL.dcElements.components.find((c) => c.id === 'L');
check('inductor-becomes-dcr-at-dc', dcInductor && dcInductor.type === 'resistor',
  JSON.stringify(dcInductor));
near('inductor-dcr-value-is-the-existing-physical-model', dcInductor.value, dcr, 1e-15);
const expectedI = 5 / (CircuitEngine.BATTERY_RINT + R + dcr);
near('dc-inductor-current-matches-resistive-loop', opL.currents.get('L'), expectedI, 2e-6);
check('inductor-op-converged', opL.solver && opL.solver.converged === true,
  JSON.stringify(opL.solver));

console.log(`\n=== ALL ${checks} DC OPERATING POINT CHECKS PASSED ===`);
