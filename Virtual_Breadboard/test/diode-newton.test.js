#!/usr/bin/env node
'use strict';

const CE = require('../js/circuit.js');
const { Circuit, DIODE_IS, DIODE_N, THERMAL_VOLTAGE_25C, BATTERY_RINT } = CE;

let checks = 0;
function check(name, condition, detail) {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  if (!condition) throw new Error(`DIODE NEWTON QUALIFICATION FAILED: ${name}`);
}

function diodeCircuit(sourceV) {
  return {
    wires: [],
    components: [
      { id: 'B1', type: 'battery', value: sourceV, a: 'vin', b: 'gnd' },
      { id: 'D1', type: 'diode', a: 'vin', b: 'gnd' },
    ],
  };
}

function solveNewton(sourceV) {
  const elements = diodeCircuit(sourceV);
  const result = new Circuit().solve(elements, 1e-3, 25, {
    diodeModel: 'newton',
    maxIterations: 80,
  });
  const vin = result.voltages.get(result.uf.find('vin')) || 0;
  const current = result.currents.get('D1') || 0;
  return { elements, result, vin, current };
}

console.log('=== Virtual Breadboard continuous diode / Newton qualification ===');

// Compatibility guard: precision mode is opt-in. Existing breadboard builds
// continue to use the threshold + RON model unless explicitly requested.
{
  const low = new Circuit().solve(diodeCircuit(0.4), 1e-3, 25);
  const high = new Circuit().solve(diodeCircuit(0.8), 1e-3, 25);
  check('simple-model-remains-default', low.solver.diodeModel === 'simple' && high.solver.diodeModel === 'simple');
  check('simple-model-still-off-below-threshold', Math.abs(low.currents.get('D1') || 0) < 1e-15,
    `I=${low.currents.get('D1')}`);
  check('simple-model-still-conducts-above-threshold', (high.currents.get('D1') || 0) > 0,
    `I=${high.currents.get('D1')}`);
}

// Precision model: compare the solved branch current to the independent
// Shockley equation evaluated at the solved terminal voltage, and separately
// verify KCL against the battery's declared 1-ohm internal resistance + GMIN.
const points = [-1.0, 0.2, 0.4, 0.50, 0.51, 0.60, 0.70];
const rows = points.map((sourceV) => {
  const row = solveNewton(sourceV);
  const expectedShockley = DIODE_IS * (Math.exp(Math.max(-5, Math.min(0.8, row.vin)) /
    (DIODE_N * THERMAL_VOLTAGE_25C)) - 1);
  const sourceCurrent = (sourceV - row.vin) / BATTERY_RINT;
  const kclRight = row.current + row.result.solver.gmin * row.vin;
  check(`newton-converges-${sourceV}V`, row.result.solver.converged === true,
    JSON.stringify(row.result.solver));
  check(`newton-mode-reported-${sourceV}V`, row.result.solver.diodeModel === 'newton');
  check(`shockley-current-${sourceV}V`, Math.abs(row.current - expectedShockley) <= Math.max(1e-12, Math.abs(expectedShockley) * 1e-8),
    `Vd=${row.vin} I=${row.current} expected=${expectedShockley}`);
  check(`kcl-closes-${sourceV}V`, Math.abs(sourceCurrent - kclRight) < 2e-7,
    `source=${sourceCurrent} diode+gmin=${kclRight}`);
  return { sourceV, ...row };
});

for (let i = 1; i < rows.length; i++) {
  check(`monotonic-current-${rows[i - 1].sourceV}-to-${rows[i].sourceV}`,
    rows[i].current > rows[i - 1].current,
    `${rows[i - 1].current} -> ${rows[i].current}`);
}

const reverse = rows[0];
check('reverse-current-near-minus-Is', Math.abs(reverse.current + DIODE_IS) < DIODE_IS * 0.02,
  `I=${reverse.current} Is=${DIODE_IS}`);

const p04 = rows.find((r) => r.sourceV === 0.4);
check('subthreshold-current-is-continuous-not-zero', p04.current > 0 && p04.current < 1e-5,
  `I(0.4V)=${p04.current}`);

const p050 = rows.find((r) => r.sourceV === 0.50);
const p051 = rows.find((r) => r.sourceV === 0.51);
const ratio = p051.current / p050.current;
check('no-hard-threshold-jump', ratio > 1 && ratio < 2,
  `I(0.51)/I(0.50)=${ratio}`);

console.log(`\n=== ALL ${checks} DIODE-NEWTON CHECKS PASSED ===`);
