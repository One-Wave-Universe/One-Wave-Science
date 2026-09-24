#!/usr/bin/env node
'use strict';

const CircuitEngine = require('../js/circuit.js');

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`SOLVER CONVERGENCE QUALIFICATION FAILED: ${name}`);
}

console.log('=== Virtual Breadboard solver convergence qualification ===');

{
  const elements = {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: 5, a: 'vin', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: 1000, a: 'vin', b: 'mid' },
      { id: 'R2', type: 'resistor', value: 1000, a: 'mid', b: 'gnd' },
    ],
  };
  const result = new CircuitEngine.Circuit().solve(elements, 1e-3, 25);
  check('linear-circuit-converges', result.solver && result.solver.converged === true,
    JSON.stringify(result.solver));
  check('linear-circuit-state-stable', result.solver.stateStable === true);
  check('linear-circuit-residual-within-tolerance', result.solver.maxResidual <= result.solver.residualTolerance,
    `residual=${result.solver.maxResidual} tolerance=${result.solver.residualTolerance}`);
  check('linear-circuit-no-solver-failure-warning', !result.warnings.some((w) => /^SOLVER FAILED:/.test(w)),
    result.warnings.join(' | '));
}

{
  // Start the nonlinear diode from its default OFF state, drive it clearly
  // above threshold, and deliberately allow only one fixed-point iteration.
  // The first matrix solve necessarily uses the old OFF guess; the diode state
  // then changes to ON. With no second iteration available, accepting that
  // first answer would be a silent false convergence. The solver must report it.
  const elements = {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: 2, a: 'vin', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: 1000, a: 'vin', b: 'd' },
      { id: 'D1', type: 'diode', a: 'd', b: 'gnd' },
    ],
  };
  const circuit = new CircuitEngine.Circuit();
  const result = circuit.solve(elements, 1e-3, 25, { maxIterations: 1 });
  check('iteration-cap-is-not-silent', result.solver && result.solver.converged === false,
    JSON.stringify(result.solver));
  check('iteration-cap-reports-one-used-iteration', result.solver.iterations === 1 && result.solver.maxIterations === 1,
    JSON.stringify(result.solver));
  check('iteration-cap-identifies-unstable-device-state', result.solver.stateStable === false,
    JSON.stringify(result.solver));
  check('iteration-cap-emits-solver-failed-warning', result.warnings.some((w) => /^SOLVER FAILED: nonlinear solve did not converge/.test(w)),
    result.warnings.join(' | '));
  const diagnosis = CircuitEngine.diagnose(elements, result);
  check('diagnose-names-nonconvergence-as-solver-failure', diagnosis.solverFailed === true,
    JSON.stringify(diagnosis));
}

console.log(`\n=== ALL ${checks} SOLVER-CONVERGENCE CHECKS PASSED ===`);
