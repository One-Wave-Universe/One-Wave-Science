const { Circuit, check } = require('./_lib');

function drainV(vgs) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: 'vcc', b: 'gnd' },
    { id: 'gsrc', type: 'battery', value: vgs, a: 'gate', b: 'gnd' },
    { id: 'rdrain', type: 'resistor', value: 1000, a: 'vcc', b: 'drain' },
    { id: 'q1', type: 'nmos', value: 1.5, gate: 'gate', drain: 'drain', source: 'gnd' },
  ] };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 0.0001);
  return res;
}

function run() {
  const off = drainV(0);
  const on = drainV(5);
  const iOn = on.currents.get('q1');
  const vdsOn = on.voltages.get('drain');
  const impliedRon = vdsOn / iOn;
  return {
    name: '07_mosfet_lowside_switch',
    checks: [
      check('nmos-off-below-threshold', true, off.voltages.get('drain') > 4.9, null, 'Vgs below Vth must leave the drain pulled to VCC'),
      check('nmos-on-above-threshold', true, on.voltages.get('drain') < 0.1, null, 'Vgs above Vth must pull the drain near 0V'),
      check('nmos-rdson-matches-real-spec', 0.03, impliedRon, 0.02, `implied RDS(on)=Vds/Id must be near the real AO3400A-class spec, got ${impliedRon.toFixed(4)}ohm`),
    ],
  };
}

module.exports = { run };
