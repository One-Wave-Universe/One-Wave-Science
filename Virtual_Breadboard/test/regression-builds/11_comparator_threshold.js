const { Circuit, check } = require('./_lib');

function comparatorOut(vin) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'vref', type: 'battery', value: 2.5, a: 'ref', b: 'gnd' },
    { id: 'vsrc', type: 'diffsource', value: vin, sourceR: 10, a: 'in', b: 'gnd' },
    { id: 'cmp1', type: 'comparator', out1: 'out1', in1m: 'ref', in1p: 'in', gnd: 'gnd', in2p: 'gnd', in2m: 'gnd', out2: 'unused2', vcc: 'vcc' },
  ] };
  let res;
  for (let i = 0; i < 20; i++) res = c.solve(els, 0.0001);
  return res.voltages.get('out1');
}

function run() {
  const below = comparatorOut(2.0);
  const above = comparatorOut(3.0);
  return {
    name: '11_comparator_threshold',
    checks: [
      check('comparator-saturates-low-below-ref', true, below < 0.1, null, `Vin below Vref must saturate OUT1 near ground, got ${below.toFixed(3)}V`),
      check('comparator-saturates-high-above-ref', true, above > 4.9, null, `Vin above Vref must saturate OUT1 near VCC, got ${above.toFixed(3)}V`),
      check('comparator-no-impossible-halfway-output', true, below < 0.1 || below > 4.9, null, 'the output must always be a real saturated rail value, never an idealized in-between analog blend'),
    ],
  };
}

module.exports = { run };
