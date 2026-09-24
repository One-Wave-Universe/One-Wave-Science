const { Circuit, CircuitEngine, check } = require('./_lib');

function run() {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'p', b: 'g' },
    { id: 'r1', type: 'resistor', value: 220, a: 'p', b: 'anode' },
    { id: 'led1', type: 'led', a: 'anode', b: 'g', color: 'red' },
  ] };
  let res;
  for (let i = 0; i < 5; i++) res = c.solve(els, 0.0001);
  const vf = res.voltages.get('anode') - res.voltages.get('g');
  const i = res.currents.get('led1');
  const expectedVf = CircuitEngine.LED_VF.red + i * CircuitEngine.LED_RON;
  return {
    name: '02_led_current_limiting',
    checks: [
      check('led-forward-voltage-real', expectedVf, vf, 0.02, 'a conducting LED shows real Vf plus its own dynamic resistance drop at this current'),
      check('led-current-in-safe-range', true, i > 0.005 && i < 0.02, null, `a 220ohm limiter off a 5V rail must land in a real, safe LED current range, got ${(i * 1000).toFixed(2)}mA`),
    ],
  };
}

module.exports = { run };
