const { Circuit, check } = require('./_lib');

// CELL_V1 Station A as it will actually be wired on the bench right now --
// per Virtual_Breadboard/09_TESTS/CELL_ACTUAL_BUILD.md and
// CELL_SCHEMATIC_PRINT.md -- using the manual 10k/10k gate-bias divider
// network (no Nano yet, per the GPIO-safety fix in
// 23_dualrail_gpio_gate_guard.js) and the real AO3401A / 2N7000 model
// cards, not the idealized-battery-gate assumption LOCK.md's older
// cell_v1_stamp2_bridge.py stamp used.
//
// LOCK.md's stamp 2 (10_RECEIPTS/cell_v1_stamp2_bridge.py) says +1 -> +12mA,
// -1 -> -12mA, because it drives each gate with an ideal battery that draws
// no current from BLUE. The real bench build instead makes each ON command
// by adding a second 10k gate-to-BLUE resistor, and that resistor's own
// divider current is drawn from the same BLUE rail I_0 is measured on --
// so the real I_0 is NOT the same number as the ideal stamp. This build
// computes what it actually is, so BUILD_25.md's receipt line isn't
// chasing a number the real circuit was never going to produce.

function stationA(command) {
  // command: 'stay' | 'plus' | 'minus'
  const c = new Circuit();
  const components = [
    { id: 'red', type: 'battery', value: 12, a: 'red', b: 'blue0' },
    { id: 'black', type: 'battery', value: 12, a: 'blue0', b: 'black' }, // black is -12V relative to blue0
    // 1 ohm I_0 shunt at the "home end" of the BLUE trench, exactly as
    // BUILD_25.md step 4 specifies ("1 ohm shunt"), between the trench
    // (BLUE, where the law resistors and station load actually land) and
    // the supply's true common return (blue0).
    { id: 'i0_shunt', type: 'resistor', value: 1, a: 'blue', b: 'blue0' },
    // Law resistors (LOCK.md / CELL_ACTUAL_BUILD.md "col 3: 10k RED-BLUE, 10k BLACK-BLUE").
    { id: 'law_hi', type: 'resistor', value: 10000, a: 'red', b: 'blue' },
    { id: 'law_lo', type: 'resistor', value: 10000, a: 'black', b: 'blue' },
    // Station A devices: AO3401A P-MOS high side, 2N7000 N-MOS low side.
    { id: 'qp', type: 'pmos', model: 'AO3401A', gate: 'pgate_pin', drain: 'pa', source: 'red' },
    { id: 'qn', type: 'nmos', model: '2N7000', gate: 'ngate_pin', drain: 'pa', source: 'black' },
    // 220 ohm series gate resistors (CELL_ACTUAL_BUILD.md: "220 Ω in each
    // gate lead"). No DC current flows into a MOSFET gate in this model,
    // so these are here for the same reason the real build has them
    // (switching-transient protection), not because they change the DC
    // operating point -- this build's checks confirm that assumption.
    { id: 'pgate_series', type: 'resistor', value: 220, a: 'pgate_div', b: 'pgate_pin' },
    { id: 'ngate_series', type: 'resistor', value: 220, a: 'ngate_div', b: 'ngate_pin' },
    // OFF-bias resistors, always present.
    { id: 'pgate_off', type: 'resistor', value: 10000, a: 'pgate_div', b: 'red' },
    { id: 'ngate_off', type: 'resistor', value: 10000, a: 'ngate_div', b: 'black' },
    // 1k load from PA to BLUE.
    { id: 'load', type: 'resistor', value: 1000, a: 'pa', b: 'blue' },
  ];
  // ON-command resistors are only physically present when that phase is
  // being commanded -- exactly the jumper action BUILD_25/CELL_ACTUAL_BUILD
  // describe ("+1 = short P-gate toward BLUE with a jumper").
  if (command === 'plus' || command === 'both') {
    components.push({ id: 'pgate_on', type: 'resistor', value: 10000, a: 'pgate_div', b: 'blue' });
  }
  if (command === 'minus' || command === 'both') {
    components.push({ id: 'ngate_on', type: 'resistor', value: 10000, a: 'ngate_div', b: 'blue' });
  }

  const els = { wires: [], components };
  let res;
  for (let i = 0; i < 50; i++) res = c.solve(els, 0.0001);

  return {
    i0: res.currents.get('i0_shunt') || 0,
    vPA: res.voltages.get('pa'),
    vPgate: res.voltages.get('pgate_pin'),
    vNgate: res.voltages.get('ngate_pin'),
    vBlue: res.voltages.get('blue'),
    redCurrent: res.currents.get('red'),
    warnings: res.warnings || [],
  };
}

function run() {
  const stay = stationA('stay');
  const plus = stationA('plus');
  const minus = stationA('minus');
  const both = stationA('both');

  const checks = [];

  checks.push(
    check('station-a-stay-i0-near-zero', true, Math.abs(stay.i0) < 5e-7, null,
      `STAY I_0=${(stay.i0 * 1e6).toFixed(3)}uA (leakage only, no gate-bias draw in STAY)`),

    check('station-a-plus-gate-reaches-on-target', true, Math.abs(plus.vPgate - 6) < 0.05, null,
      `+1 P-gate=${plus.vPgate.toFixed(4)}V (target ~+6V from the 10k/10k divider)`),
    check('station-a-plus-vgs-safely-on', true, (plus.vPgate - 12) < -1.5 - 0.5, null,
      `+1 VGS_P=${(plus.vPgate - 12).toFixed(3)}V vs AO3401A vth=-1.5V`),
    check('station-a-plus-pa-pulled-high', true, plus.vPA > 11.9, null,
      `+1 PA=${plus.vPA.toFixed(4)}V (should sit near +12V through AO3401A's low RDS(on))`),
    check('station-a-plus-i0-includes-gate-bias-draw', 0.0126, plus.i0, 0.0004,
      `+1 real I_0=${(plus.i0 * 1000).toFixed(3)}mA -- NOT the ideal stamp's +12mA: the real gate-bias divider adds ~0.6mA of its own draw from BLUE`),

    check('station-a-minus-gate-reaches-on-target', true, Math.abs(minus.vNgate - (-6)) < 0.05, null,
      `-1 N-gate=${minus.vNgate.toFixed(4)}V (target ~-6V from the 10k/10k divider)`),
    check('station-a-minus-vgs-safely-on', true, (minus.vNgate - (-12)) > 2.1 + 0.5, null,
      `-1 VGS_N=${(minus.vNgate - (-12)).toFixed(3)}V vs 2N7000 vth=2.1V`),
    check('station-a-minus-pa-pulled-low', true, minus.vPA < -11.9, null,
      `-1 PA=${minus.vPA.toFixed(4)}V (should sit near -12V through 2N7000's RDS(on))`),
    check('station-a-minus-i0-includes-gate-bias-draw', -0.0126, minus.i0, 0.0004,
      `-1 real I_0=${(minus.i0 * 1000).toFixed(3)}mA -- NOT the ideal stamp's -12mA, same real gate-bias draw as +1`),

    // Both-ON does NOT show up as a big number on the I_0/BLUE shunt --
    // the rail-to-rail shoot-through path (RED -> qp -> pa -> qn -> BLACK)
    // never touches BLUE at all, so a DMM watching I_0 alone would see
    // almost nothing wrong here. The real, bench-visible signature is a
    // supply current-limit brownout plus every device/resistor in the
    // shoot-through path getting driven past its rating.
    check('station-a-both-on-i0-shunt-does-not-see-the-fault', true, Math.abs(both.i0) < 0.01, null,
      `both-ON I_0=${(both.i0 * 1000).toFixed(3)}mA -- deliberately checking that BLUE/I_0 stays quiet even though the circuit is on fire elsewhere; do not trust I_0 alone to catch a both-ON mistake`),
    check('station-a-both-on-trips-supply-current-limit', true, both.warnings.some((w) => /current-limited/.test(w)), null,
      `${both.warnings.filter((w) => /current-limited/.test(w)).join('; ') || 'no current-limit warning found'}`),
    check('station-a-both-on-exceeds-device-ratings', true, both.warnings.some((w) => /exceeds its .* rating/.test(w)), null,
      `${both.warnings.filter((w) => /exceeds its .* rating/.test(w)).join('; ') || 'no rating-violation warning found'}`),
  );

  return { name: '24_cell_v1_manual_gate_bias_station_a', checks };
}

module.exports = { run };
