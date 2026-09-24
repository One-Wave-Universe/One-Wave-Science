#!/usr/bin/env node
'use strict';

const CircuitEngine = require('../js/circuit.js');
const { operatingPoint, steppedOperatingPoint } = require('../js/spice-analysis.js');

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`SOURCE/GMIN STEPPING QUALIFICATION FAILED: ${name}`);
}

console.log('=== Virtual Breadboard source + GMIN stepping qualification ===');

const nonlinear = {
  wires: [],
  components: [
    { id: 'B1', type: 'battery', value: 2, a: 'vin', b: 'gnd' },
    { id: 'R1', type: 'resistor', value: 1000, a: 'vin', b: 'd' },
    { id: 'D1', type: 'diode', a: 'd', b: 'gnd' },
  ],
};

{
  const direct = operatingPoint(nonlinear, { solverOptions: { maxIterations: 1 } });
  check('direct-one-iteration-op-fails-as-control', direct.solver && direct.solver.converged === false,
    JSON.stringify(direct.solver));
}

{
  const stepped = steppedOperatingPoint(nonlinear, {
    sourceScales: [0, 0.25, 0.5, 0.75, 1],
    gminSteps: [1e-3, 1e-5, 1e-7, 1e-9],
    solverOptions: { maxIterations: 1 },
  });
  check('stepped-one-iteration-op-converges', stepped.solver && stepped.solver.converged === true,
    JSON.stringify(stepped.solver));
  check('final-gmin-is-real-target', stepped.solver.gmin === 1e-9,
    `gmin=${stepped.solver.gmin}`);
  check('final-source-is-full-scale', stepped.analysis.trace[stepped.analysis.trace.length - 1].sourceScale === 1,
    JSON.stringify(stepped.analysis.trace[stepped.analysis.trace.length - 1]));
  check('trace-contains-source-phase', stepped.analysis.trace.some((s) => s.phase === 'source' && s.sourceScale < 1),
    JSON.stringify(stepped.analysis.trace));
  check('trace-contains-gmin-phase', stepped.analysis.trace.some((s) => s.phase === 'gmin' && s.gmin > 1e-9),
    JSON.stringify(stepped.analysis.trace));
  check('final-diode-current-is-forward', (stepped.currents.get('D1') || 0) > 0.0005,
    `I(D1)=${stepped.currents.get('D1')}`);
  check('continuation-method-is-named', stepped.analysis.method === 'source+gmin-stepping',
    JSON.stringify(stepped.analysis));
}

{
  // A linear divider should land at the same physical operating point whether
  // continuation is used or not. Stepping is a convergence aid, not a new
  // circuit model.
  const linear = {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: 10, a: 'vin', b: 'gnd' },
      { id: 'R1', type: 'resistor', value: 1000, a: 'vin', b: 'mid' },
      { id: 'R2', type: 'resistor', value: 1000, a: 'mid', b: 'gnd' },
    ],
  };
  const direct = operatingPoint(linear);
  const stepped = steppedOperatingPoint(linear);
  const delta = Math.abs((direct.voltages.get('mid') || 0) - (stepped.voltages.get('mid') || 0));
  check('stepping-does-not-change-linear-answer', delta < 1e-6,
    `direct=${direct.voltages.get('mid')} stepped=${stepped.voltages.get('mid')} delta=${delta}`);
}

console.log(`\n=== ALL ${checks} SOURCE/GMIN-STEPPING CHECKS PASSED ===`);
