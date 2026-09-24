const { Circuit, CircuitEngine, check } = require('../regression-builds/_lib');

// The real way a flashlight's electronic switch controls the LED: an
// NMOS low-side switch in series with the same 3.7V/limiter/white-LED
// path as build 01, gated by a separate logic-level drive (e.g. a
// microcontroller GPIO or soft-touch switch IC, not the battery rail
// itself). ON must add the MOSFET's own real RDS(on) into the same
// hand-calculated series loop; OFF must genuinely block, not leak.
function ledCircuit(gateV) {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 3.7, a: 'p', b: 'g' },
    { id: 'r1', type: 'resistor', value: 10, a: 'p', b: 'anode' },
    { id: 'led1', type: 'led', a: 'anode', b: 'cathode', color: 'white' },
    { id: 'gsrc', type: 'battery', value: gateV, a: 'gate', b: 'g' },
    { id: 'q1', type: 'nmos', value: 1.5, gate: 'gate', drain: 'cathode', source: 'g' },
  ] };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 0.0001);
  return res;
}

function run() {
  const on = ledCircuit(5.0); // logic-level gate drive well above the 1.5V Vth
  const off = ledCircuit(0.0);

  const iOn = on.currents.get('led1');
  const iOff = off.currents.get('led1');

  // Same hand calculation as build 01, with the MOSFET's own real
  // RDS(on) (AO3400A-class, 0.03ohm at value:1.5) now in series too.
  const rdsOn = CircuitEngine.NMOS_PARTS[1.5].rdsOn;
  const totalR = 10 + CircuitEngine.LED_RON + CircuitEngine.BATTERY_RINT + rdsOn;
  const iExpectedOn = (3.7 - CircuitEngine.LED_VF.white) / totalR;

  return {
    name: '02_mosfet_switched_led',
    checks: [
      check('mosfet-switched-led-on-current-matches-hand-calc', iExpectedOn, iOn, 1e-5,
        `gate driven above Vth: I = (3.7 - ${CircuitEngine.LED_VF.white}) / (10 + ${CircuitEngine.LED_RON} + ${CircuitEngine.BATTERY_RINT} + ${rdsOn} RDS(on)) = ${(iExpectedOn * 1000).toFixed(3)}mA`),
      check('mosfet-switched-led-off-current-blocks', true, iOff < 1e-6, null,
        `gate held at 0V (below the real 1.5V Vth) must genuinely block the LED path, got ${iOff}A -- a real flashlight switch turning fully off, not dimming`),
      check('mosfet-switched-led-rdson-cost-is-real-but-small', true, iOn < (3.7 - CircuitEngine.LED_VF.white) / (10 + CircuitEngine.LED_RON + CircuitEngine.BATTERY_RINT), null,
        `adding the real switch's own RDS(on) must measurably (even if slightly) reduce current versus build 01's switchless case -- a real, honest series loss, not zero-cost switching`),
    ],
  };
}

module.exports = { run };
