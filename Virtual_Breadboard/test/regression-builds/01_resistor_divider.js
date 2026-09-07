const { Circuit, check } = require('./_lib');

function run() {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 10, a: 'p', b: 'g' },
    { id: 'r1', type: 'resistor', value: 1000, a: 'p', b: 'mid' },
    { id: 'r2', type: 'resistor', value: 1000, a: 'mid', b: 'g' },
  ] };
  const res = c.solve(els, 0.001);
  const mid = res.voltages.get('mid');
  return {
    name: '01_resistor_divider',
    checks: [
      check('divider-midpoint', 5.0, mid, 0.02, 'equal-value divider legs must produce a real half-rail midpoint'),
      check('divider-current-matches-ohms-law', 10 / 2000, res.currents.get('r1'), 1e-5, 'loop current must match I=V/Rtotal'),
    ],
  };
}

module.exports = { run };
