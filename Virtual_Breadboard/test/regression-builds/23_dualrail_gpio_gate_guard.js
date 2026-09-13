'use strict';

const { Circuit, check } = require('./_lib');

function solvePmos(gpioV) {
  const c = new Circuit();
  const elements = { wires: [], components: [
    { id: 'VPLUS', type: 'battery', value: 12, a: 'p', b: 'zero' },
    { id: 'GPIO', type: 'diffsource', value: gpioV, sourceR: 25, a: 'gate', b: 'zero' },
    { id: 'QH', type: 'pmos', model: 'AO3401A', gate: 'gate', drain: 'out', source: 'p' },
    { id: 'LOAD', type: 'resistor', value: 1000, a: 'out', b: 'zero' },
  ] };
  let result;
  for (let i = 0; i < 80; i++) result = c.solve(elements, 0.0001, 25, { mosfetModel: 'continuous', maxIterations: 100 });
  return result;
}

function solveNmos(gpioV) {
  const c = new Circuit();
  const elements = { wires: [], components: [
    { id: 'VMINUS', type: 'battery', value: 12, a: 'zero', b: 'n' },
    { id: 'GPIO', type: 'diffsource', value: gpioV, sourceR: 25, a: 'gate', b: 'zero' },
    { id: 'QL', type: 'nmos', model: '2N7000', gate: 'gate', drain: 'out', source: 'n' },
    { id: 'LOAD', type: 'resistor', value: 1000, a: 'out', b: 'zero' },
  ] };
  let result;
  for (let i = 0; i < 80; i++) result = c.solve(elements, 0.0001, 25, { mosfetModel: 'continuous', maxIterations: 100 });
  return result;
}

function run() {
  const pHigh = solvePmos(5);
  const nLow = solveNmos(0);
  const pOut = pHigh.voltages.get('out') || 0;
  const nOut = nLow.voltages.get('out') || 0;
  const pSrc = pHigh.voltages.get('p') || 0;
  const pGate = pHigh.voltages.get('gate') || 0;
  const nSrc = nLow.voltages.get('n') || 0;
  const nGate = nLow.voltages.get('gate') || 0;
  const pVgs = pGate - pSrc;
  const nVgs = nGate - nSrc;

  return {
    name: '23_dualrail_gpio_gate_guard',
    checks: [
      check('dualrail-pmos-direct-5v-gpio-does-not-turn-off', true, pOut > 10, null,
        `GPIO HIGH=5V gives PMOS Vgs=${pVgs.toFixed(3)}V and OUT=${pOut.toFixed(3)}V; direct BLUE-referenced GPIO is not an OFF command`),
      check('dualrail-nmos-direct-0v-gpio-does-not-turn-off', true, nOut < -10, null,
        `GPIO LOW=0V gives NMOS Vgs=${nVgs.toFixed(3)}V and OUT=${nOut.toFixed(3)}V; direct BLUE-referenced GPIO is not an OFF command`),
      check('dualrail-direct-gpio-cannot-create-stay', true, pOut > 10 && nOut < -10, null,
        'Both supposed OFF commands still drive their rails. CELL_V1 requires gate-to-source bias plus level shifting/isolated drive before Nano control.'),
    ],
  };
}

module.exports = { run };
