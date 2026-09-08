const { Circuit, check } = require('./_lib');

// Back-to-back N-channel MOSFETs as one bilateral nerve gate.
// Sources are tied together so the two body diodes oppose one another.
// OFF must block either polarity across LEFT/RIGHT. ON drives both gates
// +5 V relative to their shared source node, so the same physical pair
// conducts in either direction.
//
// The 1k resistor is only the test/load current limiter. It is not the
// One-Wave controller and does not decide the gate state.
function measure(direction, enabled) {
  const c = new Circuit();
  const forward = direction === 'left-to-right';
  const supply = forward ? 'left_supply' : 'right_supply';
  const driven = forward ? 'left' : 'right';
  const returned = forward ? 'right' : 'left';

  const els = { wires: [], components: [
    { id: 'bat1', type: 'battery', value: 5, a: supply, b: 'gnd' },
    { id: 'rlim', type: 'resistor', value: 1000, a: supply, b: driven },
    { id: 'rreturn', type: 'resistor', value: 0.1, a: returned, b: 'gnd' },

    // source-to-source pair: opposed body diodes, one bilateral route
    { id: 'qleft', type: 'nmos', value: 1.5, gate: 'gate', drain: 'left', source: 'common_source' },
    { id: 'qright', type: 'nmos', value: 1.5, gate: 'gate', drain: 'right', source: 'common_source' },

    // Gate drive is referenced to the pair itself: Vgs = 0 V OFF, +5 V ON.
    { id: 'gdrive', type: 'battery', value: enabled ? 5 : 0, a: 'gate', b: 'common_source' },
  ] };

  let res;
  for (let i = 0; i < 30; i++) res = c.solve(els, 0.0001);
  return {
    current: Math.abs(res.currents.get('rlim') || 0),
    warnings: res.warnings || [],
  };
}

function run() {
  const offForward = measure('left-to-right', false);
  const offReverse = measure('right-to-left', false);
  const onForward = measure('left-to-right', true);
  const onReverse = measure('right-to-left', true);

  return {
    name: '18_bidirectional_mosfet_nerve_gate',
    checks: [
      check(
        'bidirectional-gate-off-blocks-left-to-right',
        true,
        offForward.current < 1e-5,
        null,
        `OFF L->R current ${(offForward.current * 1e6).toFixed(3)}uA must remain leakage-scale`,
      ),
      check(
        'bidirectional-gate-off-blocks-right-to-left',
        true,
        offReverse.current < 1e-5,
        null,
        `OFF R->L current ${(offReverse.current * 1e6).toFixed(3)}uA must remain leakage-scale`,
      ),
      check(
        'bidirectional-gate-on-conducts-left-to-right',
        true,
        onForward.current > 0.004,
        null,
        `ON L->R current ${(onForward.current * 1000).toFixed(3)}mA must approach the 5V/1k test load current`,
      ),
      check(
        'bidirectional-gate-on-conducts-right-to-left',
        true,
        onReverse.current > 0.004,
        null,
        `ON R->L current ${(onReverse.current * 1000).toFixed(3)}mA must use the same pair in reverse`,
      ),
      check(
        'bidirectional-gate-on-is-symmetric',
        true,
        Math.abs(onForward.current - onReverse.current) < 5e-5,
        null,
        `forward/reverse ON currents must match: ${(onForward.current * 1000).toFixed(3)}mA vs ${(onReverse.current * 1000).toFixed(3)}mA`,
      ),
    ],
  };
}

module.exports = { run };
