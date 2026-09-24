const { Circuit, CircuitEngine, check } = require('../regression-builds/_lib');

// Contrast with the qualification gate's own unclamped flyback test
// (which deliberately has NO snubber, so the disconnected node swings to
// an extreme bounded only by GMIN). Here a real flyback diode sits across
// the coil. Once the coil's real steady-state current is established and
// the source path opens, the diode must clamp the inductive kick to
// approximately -(DIODE_VF + I*DIODE_RON) instead of the huge unclamped
// spike -- the actual reason every real relay/motor/solenoid driver in a
// flashlight-class product carries a flyback diode.
function run() {
  const V = 9, R = 100, L = 0.01;
  const chargeEls = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: V, a: 'vcc', b: 'gnd' },
    { id: 'r1', type: 'resistor', value: R, a: 'vcc', b: 'ind' },
    { id: 'l1', type: 'inductor', value: L, a: 'ind', b: 'gnd' },
  ] };
  const dcr = CircuitEngine.inductorDCR(L);
  const tau = L / (R + dcr);
  const dt = tau / 200;

  const c = new Circuit();
  let res;
  for (let i = 0; i < 4000; i++) res = c.solve(chargeEls, dt); // ~20 tau, well settled
  const iSteady = res.currents.get('l1');

  // UNCLAMPED: source path removed, nothing else in the circuit -- same
  // floating-reference situation as the qualification gate's own test,
  // so read the real difference across the coil's own two terminals.
  const unclampedEls = { wires: [], components: [{ id: 'l1', type: 'inductor', value: L, a: 'ind', b: 'gnd' }] };
  const resUnclamped = c.solve(unclampedEls, dt);
  const vUnclamped = resUnclamped.voltages.get('ind') - resUnclamped.voltages.get('gnd');

  // CLAMPED: a fresh run of the same charge-up, then a real flyback diode
  // (anode=gnd, cathode=ind) takes over instead of an open circuit.
  const c2 = new Circuit();
  let res2;
  for (let i = 0; i < 4000; i++) res2 = c2.solve(chargeEls, dt);
  const clampedEls = { wires: [], components: [
    { id: 'l1', type: 'inductor', value: L, a: 'ind', b: 'gnd' },
    { id: 'd1', type: 'diode', a: 'gnd', b: 'ind' },
  ] };
  const resClamped = c2.solve(clampedEls, dt);
  const vClamped = resClamped.voltages.get('ind') - resClamped.voltages.get('gnd');
  const iThroughDiode = resClamped.currents.get('d1');

  const expectedClampedV = -(CircuitEngine.DIODE_VF + Math.abs(iThroughDiode) * CircuitEngine.DIODE_RON);

  return {
    name: '04_flyback_clamped_coil',
    checks: [
      check('flyback-unclamped-spike-is-huge', true, Math.abs(vUnclamped) > 50, null,
        `with no flyback diode, opening the coil's path produces a real, large, GMIN-bounded spike (${vUnclamped.toFixed(1)}V) -- the same real behavior the qualification gate's own unclamped test establishes`),
      check('flyback-clamped-matches-hand-calc', expectedClampedV, vClamped, 0.05,
        `with a real flyback diode across the coil, V(ind)-V(gnd) must clamp to -(DIODE_VF + I*DIODE_RON) = ${expectedClampedV.toFixed(4)}V using the coil's own real steady-state current (${(iSteady * 1000).toFixed(3)}mA), not the unclamped spike above`),
      check('flyback-clamp-is-orders-of-magnitude-smaller', true, Math.abs(vClamped) < Math.abs(vUnclamped) / 10, null,
        `the real diode must reduce the inductive kick by orders of magnitude (unclamped ${vUnclamped.toFixed(1)}V vs clamped ${vClamped.toFixed(3)}V) -- proving the simulator can tell a protected design from an unprotected one, not just report "some voltage" either way`),
    ],
  };
}

module.exports = { run };
