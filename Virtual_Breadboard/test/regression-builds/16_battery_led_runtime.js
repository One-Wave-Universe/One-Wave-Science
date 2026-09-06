const { Circuit, check } = require('./_lib');

function run() {
  // small capacityAh so the real depletion finishes inside a short test run
  const capacityAh = 0.00005;
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 9, a: 'vcc', b: 'gnd', capacityAh },
    { id: 'r1', type: 'resistor', value: 470, a: 'vcc', b: 'anode' },
    { id: 'led1', type: 'led', a: 'anode', b: 'gnd', color: 'red' },
  ] };
  const dt = 0.005;
  let res, runtimeS = null;
  for (let i = 0; i < 4000; i++) {
    const t = i * dt;
    res = c.solve(els, dt);
    const iLed = res.currents.get('led1');
    if (runtimeS == null && iLed < 0.001) runtimeS = t; // LED effectively dark
  }
  const bs = res.batteryStates.get('bat1');
  return {
    name: '16_battery_led_runtime',
    checks: [
      check('battery-led-runtime-measured', true, runtimeS != null && runtimeS > 0, null, `the LED must genuinely go dark as the battery runs down, runtime=${runtimeS}s`),
      check('battery-soc-low-when-led-dark', true, bs.socFraction < 0.3, null, `state of charge when dark must be genuinely low, got ${(bs.socFraction * 100).toFixed(1)}%`),
      check('battery-energy-consumed-tracked', true, bs.energyConsumedJ > 0, null, 'real cumulative energy consumed must be tracked and positive'),
    ],
  };
}

module.exports = { run };
