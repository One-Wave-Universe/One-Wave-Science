const { Circuit, check } = require('./_lib');

// The full balanced/differential cell: a buffered CENTER splits a real
// rail into +/CENTER/- with two symmetric resistor arms feeding real
// output nodes -- both a differential measurement primitive AND a
// balanced load, together in one build, exactly as an actual balanced
// differential stage is really built.
function buildCell(loadPlus, loadMinus) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 10, a: 'plus_rail', b: 'minus_rail' },
    { id: 'vg1', type: 'vgnd', a: 'plus_rail', b: 'minus_rail', out: 'center' },
    { id: 'rp1', type: 'resistor', value: 1000, a: 'plus_rail', b: 'plusnode' },
    { id: 'rp2', type: 'resistor', value: 1000, a: 'plusnode', b: 'center' },
    { id: 'rm1', type: 'resistor', value: 1000, a: 'center', b: 'minusnode' },
    { id: 'rm2', type: 'resistor', value: 1000, a: 'minusnode', b: 'minus_rail' },
    { id: 'lp', type: 'resistor', value: loadPlus, a: 'plusnode', b: 'center' },
    { id: 'lm', type: 'resistor', value: loadMinus, a: 'minusnode', b: 'center' },
  ] };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 0.001);
  return {
    center: res.voltages.get('center'),
    plus: res.voltages.get('plusnode') - res.voltages.get('center'),
    minus: res.voltages.get('minusnode') - res.voltages.get('center'),
    iPlusArm: res.currents.get('rp2'),
    iMinusArm: res.currents.get('rm1'),
  };
}

function run() {
  const balanced = buildCell(1e9, 1e9); // no extra load, both sides matched
  const asym = buildCell(200, 1e9); // heavy load on the + side only
  return {
    name: '17_balanced_differential_cell',
    checks: [
      check('balanced-cell-symmetric-unloaded', true, Math.abs(balanced.plus + balanced.minus) < 0.05, null, `balanced +/- relative to CENTER must be equal and opposite: +${balanced.plus.toFixed(4)}V / ${balanced.minus.toFixed(4)}V`),
      check('balanced-cell-matched-arm-currents-equal', true, Math.abs(balanced.iPlusArm - balanced.iMinusArm) < 1e-5, null, 'unloaded, both arms must draw real, equal current'),
      check('balanced-cell-asymmetric-load-disturbs-reading', true, Math.abs(asym.plus - balanced.plus) > 1.0, null, `one-sided loading must visibly disturb the differential reading (moved ${Math.abs(asym.plus - balanced.plus).toFixed(3)}V)`),
      check('balanced-cell-center-stays-stable-buffered', true, Math.abs(asym.center - balanced.center) < 0.05, null, 'the buffered CENTER itself must stay stable even while the loaded arm shows the real disturbance'),
    ],
  };
}

module.exports = { run };
