const { Circuit, CircuitEngine, check } = require('../regression-builds/_lib');

// The actual flashlight-scale rail: a single Li-ion cell at 3.7V nominal
// (not the 5V/9V rails used elsewhere in this repo's tests), driving one
// white LED through a real current-limiting resistor. Hand-calculated
// expectation: I = (Vsource - LED_VF.white) / (R + LED_RON), the same
// linear Vf+I*Ron model already established and used throughout
// qualification.test.js -- this is the flashlight-adjacent case of it.
function run() {
  const Vsource = 3.7;
  const R = 10; // ohm limiter
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: Vsource, a: 'p', b: 'g' },
    { id: 'r1', type: 'resistor', value: R, a: 'p', b: 'anode' },
    { id: 'led1', type: 'led', a: 'anode', b: 'g', color: 'white' },
  ] };
  let res;
  for (let i = 0; i < 10; i++) res = c.solve(els, 0.0001);

  const iActual = res.currents.get('led1');
  const vfActual = res.voltages.get('anode') - res.voltages.get('g');

  // The real loop also includes the battery's own internal resistance
  // (BATTERY_RINT) in series -- a hand calculation that forgets it is
  // wrong, not the solver: this is exactly the kind of real series
  // element this calibration pack exists to force into the open.
  const totalR = R + CircuitEngine.LED_RON + CircuitEngine.BATTERY_RINT;
  const iExpected = (Vsource - CircuitEngine.LED_VF.white) / totalR;
  const vfExpected = CircuitEngine.LED_VF.white + iExpected * CircuitEngine.LED_RON;

  return {
    name: '01_white_led_limiter',
    checks: [
      check('white-led-current-matches-hand-calc', iExpected, iActual, 1e-5,
        `at a real 3.7V single-cell rail, I = (3.7 - ${CircuitEngine.LED_VF.white}) / (${R} limiter + ${CircuitEngine.LED_RON} LED_RON + ${CircuitEngine.BATTERY_RINT} battery Rint) = ${(iExpected * 1000).toFixed(2)}mA, hand-calculated independently of the solver`),
      check('white-led-vf-matches-hand-calc', vfExpected, vfActual, 1e-4,
        `real Vf at this operating current = ${vfExpected.toFixed(4)}V (bare Vf plus the LED's own dynamic resistance drop)`),
      check('white-led-headroom-is-thin-not-hidden', true, (Vsource - CircuitEngine.LED_VF.white) < 1.0, null,
        `only ${(Vsource - CircuitEngine.LED_VF.white).toFixed(2)}V of headroom above Vf on a bare-resistor 3.7V rail -- a real, honest flashlight design constraint (this is why real single-cell white-LED flashlights use a boost/constant-current driver, not a bare resistor) that the simulator surfaces rather than hides`),
    ],
  };
}

module.exports = { run };
