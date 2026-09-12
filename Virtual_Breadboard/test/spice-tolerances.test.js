#!/usr/bin/env node
'use strict';

const { Circuit } = require('../js/circuit.js');

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`SPICE TOLERANCE QUALIFICATION FAILED: ${name}`);
}

function diodeCircuit(v) {
  return {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: v, a: 'vin', b: 'gnd' },
      { id: 'D1', type: 'diode', a: 'vin', b: 'gnd' },
    ],
  };
}

console.log('=== Virtual Breadboard SPICE-style convergence tolerance qualification ===');

// Linear/simple-mode circuits should not be forced through an artificial
// second pass merely because precision nonlinear tolerance tracking exists.
{
  const r = new Circuit().solve(diodeCircuit(0.4), 1e-3, 25, { maxIterations: 1 });
  check('simple-mode-one-pass-preserved', r.solver.converged === true, JSON.stringify(r.solver));
  check('simple-mode-not-precision-gated', r.solver.diodeModel === 'simple');
}

// Precision mode uses SPICE-class defaults unless the caller overrides them.
{
  const r = new Circuit().solve(diodeCircuit(0.7), 1e-3, 25, {
    diodeModel: 'newton', maxIterations: 80,
  });
  check('precision-default-converges', r.solver.converged === true, JSON.stringify(r.solver));
  check('default-reltol', r.solver.reltol === 1e-3, `RELTOL=${r.solver.reltol}`);
  check('default-vntol', r.solver.vntol === 1e-6, `VNTOL=${r.solver.vntol}`);
  check('default-abstol', r.solver.abstol === 1e-12, `ABSTOL=${r.solver.abstol}`);
  check('voltage-delta-converged', r.solver.voltageDeltaConverged === true,
    `dV=${r.solver.maxVoltageDelta} tol=${r.solver.maxVoltageTolerance}`);
  check('current-delta-converged', r.solver.currentDeltaConverged === true,
    `dI=${r.solver.maxCurrentDelta} tol=${r.solver.maxCurrentTolerance}`);
}

// One Newton pass cannot establish delta convergence because there is no
// previous nonlinear iterate to compare against. This is intentional and is
// the exact distinction from the old state-flip-only stopping rule.
{
  const r = new Circuit().solve(diodeCircuit(0.7), 1e-3, 25, {
    diodeModel: 'newton', maxIterations: 1,
  });
  check('one-newton-pass-not-converged', r.solver.converged === false, JSON.stringify(r.solver));
  check('one-pass-voltage-delta-unproven', r.solver.voltageDeltaConverged === false);
  check('one-pass-current-delta-unproven', r.solver.currentDeltaConverged === false);
}

// Loose explicit tolerances should permit the second Newton iterate to count
// as converged even while a much tighter criterion rejects that same budget.
{
  const loose = new Circuit().solve(diodeCircuit(0.7), 1e-3, 25, {
    diodeModel: 'newton', maxIterations: 2,
    reltol: 0, vntol: 10, abstol: 10,
  });
  const tight = new Circuit().solve(diodeCircuit(0.7), 1e-3, 25, {
    diodeModel: 'newton', maxIterations: 2,
    reltol: 0, vntol: 1e-15, abstol: 1e-18,
  });
  check('custom-tolerances-reported', loose.solver.reltol === 0 && loose.solver.vntol === 10 && loose.solver.abstol === 10,
    JSON.stringify(loose.solver));
  check('loose-second-pass-converges', loose.solver.converged === true, JSON.stringify(loose.solver));
  check('tight-same-budget-rejected', tight.solver.converged === false, JSON.stringify(tight.solver));
  check('tight-fails-delta-criterion', !tight.solver.voltageDeltaConverged || !tight.solver.currentDeltaConverged,
    `V=${tight.solver.voltageDeltaConverged} I=${tight.solver.currentDeltaConverged}`);
}

console.log(`\n=== ALL ${checks} SPICE-TOLERANCE CHECKS PASSED ===`);
