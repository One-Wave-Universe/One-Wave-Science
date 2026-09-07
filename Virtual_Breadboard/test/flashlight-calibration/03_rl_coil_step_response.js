const { Circuit, CircuitEngine, check } = require('../regression-builds/_lib');

// A real coil (e.g. a boost-driver inductor or a vibration-motor winding)
// stepped from 0 to a real DC voltage. Hand-calculated expectation is the
// full analytic exponential I(t) = (V/Rtotal)*(1 - exp(-t/tau)),
// Rtotal = external R + the coil's own real DCR, tau = L/Rtotal -- checked
// at several points along the curve, not just the final steady state (the
// existing qualification-gate inductor test only checks "near 0 at t~0"
// and "near steady state eventually"; this checks the actual shape).
function run() {
  const V = 5.0, R = 100, L = 0.01;
  const dcr = CircuitEngine.inductorDCR(L);
  const rTotal = R + dcr;
  const tau = L / rTotal;

  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: V, a: 'p', b: 'g' },
    { id: 'r1', type: 'resistor', value: R, a: 'p', b: 'ind' },
    { id: 'l1', type: 'inductor', value: L, a: 'ind', b: 'g' },
  ] };
  const dt = tau / 2000; // fine enough to resolve tau accurately

  const checkPoints = [0.5, 1, 2, 5]; // in units of tau
  const results = [];
  let res, stepsElapsed = 0;
  checkPoints.forEach((mult) => {
    const targetSteps = Math.round((mult * tau) / dt);
    while (stepsElapsed < targetSteps) {
      res = c.solve(els, dt);
      stepsElapsed++;
    }
    const iActual = res.currents.get('l1');
    const iExpected = (V / rTotal) * (1 - Math.exp(-mult));
    results.push({ mult, iActual, iExpected });
  });

  const checks = results.map(({ mult, iActual, iExpected }) =>
    check(`rl-step-response-at-${mult}tau`, iExpected, iActual, iExpected * 0.02 + 1e-6,
      `at t=${mult}*tau, I = (V/Rtotal)*(1-e^-${mult}) = ${(iExpected * 1000).toFixed(4)}mA (Rtotal=${rTotal.toFixed(4)}ohm includes the coil's own real DCR=${dcr.toFixed(4)}ohm, tau=${(tau * 1e6).toFixed(2)}us)`));

  return { name: '03_rl_coil_step_response', checks };
}

module.exports = { run };
