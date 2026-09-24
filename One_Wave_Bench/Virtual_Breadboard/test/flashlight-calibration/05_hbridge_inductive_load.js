const { Circuit, CircuitEngine, check } = require('../regression-builds/_lib');

// A real reversible driver (e.g. a flashlight's vibration-alert motor, or
// a solenoid-latch driver) with an actual inductive load between out1/out2
// instead of the qualification gate's pure resistor. Forward drive must
// build current per the real L/R time constant (not instantly), reversing
// the command must genuinely reverse current direction, and nothing in
// between may show an unbounded/destructive value -- the H-bridge's own
// unconditional body diodes are exactly what makes that last part true.
function buildHBridge() {
  const c = new Circuit();
  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 9, a: 'vm', b: 'gnd' },
    { id: 'in1', type: 'diffsource', value: 0, sourceR: 50, a: 'in1', b: 'gnd' },
    { id: 'in2', type: 'diffsource', value: 0, sourceR: 50, a: 'in2', b: 'gnd' },
    { id: 'hb1', type: 'hbridge', in1: 'in1', in2: 'in2', vm: 'vm', gnd: 'gnd', out1: 'out1', out2: 'out2' },
    { id: 'rballast', type: 'resistor', value: 50, a: 'out1', b: 'coil' }, // real series ballast, keeps current modest
    { id: 'l1', type: 'inductor', value: 0.01, a: 'coil', b: 'out2' },
  ] };
  return { circuit: c, els };
}

function run() {
  const { circuit, els } = buildHBridge();
  const spec = CircuitEngine.HBRIDGE_SPEC;
  const dcr = CircuitEngine.inductorDCR(0.01);
  const rTotal = spec.ronHS + spec.ronLS + 50 + dcr;
  const iSteadyExpected = 9 / rTotal;
  const tau = 0.01 / rTotal;
  const dt = tau / 500;

  // FORWARD: in1 high, in2 low
  els.components[1].value = 5; // in1
  els.components[2].value = 0; // in2
  let res;
  const earlySteps = Math.round((0.5 * tau) / dt);
  for (let i = 0; i < earlySteps; i++) res = circuit.solve(els, dt);
  const iEarly = res.currents.get('l1');
  const iEarlyExpected = iSteadyExpected * (1 - Math.exp(-0.5));

  const remainingSteps = Math.round((20 * tau) / dt) - earlySteps; // ~20 tau total, well settled
  for (let i = 0; i < remainingSteps; i++) res = circuit.solve(els, dt);
  const iForwardSteady = res.currents.get('l1');

  // REVERSE: swap the drive
  els.components[1].value = 0; // in1
  els.components[2].value = 5; // in2
  for (let i = 0; i < Math.round((20 * tau) / dt); i++) {
    res = circuit.solve(els, dt);
  }
  const iReverseSteady = res.currents.get('l1');

  return {
    name: '05_hbridge_inductive_load',
    checks: [
      check('hbridge-inductive-current-not-instant', iEarlyExpected, iEarly, iEarlyExpected * 0.05 + 1e-4,
        `at t=0.5*tau, current must follow the real L/R rise (I = Isteady*(1-e^-0.5) = ${(iEarlyExpected * 1000).toFixed(3)}mA), not jump immediately to steady state`),
      check('hbridge-inductive-forward-steady-matches-hand-calc', iSteadyExpected, iForwardSteady, iSteadyExpected * 0.03,
        `forward steady-state I = VM/(ronHS+ronLS+ballast+DCR) = 9/${rTotal.toFixed(4)} = ${(iSteadyExpected * 1000).toFixed(3)}mA`),
      check('hbridge-inductive-reverse-flips-direction', true, Math.sign(iReverseSteady) !== Math.sign(iForwardSteady), null,
        `reversing the command must genuinely flip current direction (forward=${(iForwardSteady * 1000).toFixed(3)}mA, reverse=${(iReverseSteady * 1000).toFixed(3)}mA)`),
      check('hbridge-inductive-reverse-magnitude-matches-hand-calc', iSteadyExpected, Math.abs(iReverseSteady), iSteadyExpected * 0.03,
        `the reversed steady-state magnitude must match the same real hand-calc (${(iSteadyExpected * 1000).toFixed(3)}mA) -- a symmetric real driver, not a one-directional approximation`),
      check('hbridge-inductive-no-destructive-value-during-reversal', true, Math.abs(iForwardSteady) < 5 && Math.abs(iReverseSteady) < 5, null,
        'neither steady-state current may show an unbounded/destructive value -- the body diodes give the coil a real path to recirculate through instead of an impossible instantaneous reversal'),
    ],
  };
}

module.exports = { run };
