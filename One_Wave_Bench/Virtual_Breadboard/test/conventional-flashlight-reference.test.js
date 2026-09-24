#!/usr/bin/env node
/*
 * Conventional flashlight reference/control.
 *
 * IMPORTANT: this is NOT the One-Wave balanced flashlight prototype.
 * It is retained only as a matched-light / matched-energy comparison control.
 *
 * Architecture:
 *   - one positive supply rail
 *   - buffered midpoint only as a measurement reference
 *   - capacitor storage
 *   - binary Schmitt-trigger hysteresis
 *   - PMOS refill gate
 *   - conventional current-limited white LED load
 *
 * The actual One-Wave target is locked in:
 *   One_Wave_Bench/flashlight/BALANCED_FLASHLIGHT_STATE_REINJECTION_LOCK.md
 */
const CircuitEngine = require('../js/circuit.js');
const { Circuit } = CircuitEngine;
const Sim = require('../simulate.js');

let failures = 0;
function check(name, pass, note) {
  console.log(`${pass ? 'PASS' : 'FAIL'} [${name}]${note ? ' -- ' + note : ''}`);
  if (!pass) failures++;
}

const VCC = 5.0;
const CSTORE = 100e-6;
const RCHARGE = 20;
const RLED = 22;
const DT = 10e-6;
const STEPS = 30000;
const SETTLE = 3000;

const circuit = new Circuit();
const elements = {
  wires: [],
  components: [
    { id: 'bat1', type: 'battery', value: VCC, a: 'vcc', b: 'gnd' },
    { id: 'vg1', type: 'vgnd', a: 'vcc', b: 'gnd', out: 'center' },
    { id: 'cstore', type: 'capacitor', value: CSTORE, a: 'store', b: 'gnd', initialV: 3.7 },
    { id: 'rled', type: 'resistor', value: RLED, a: 'store', b: 'led_anode' },
    { id: 'led1', type: 'led', color: 'white', a: 'led_anode', b: 'gnd' },
    { id: 'sg1', type: 'schmitt', in: 'store', out: 'sense_inv', vcc: 'vcc', gnd: 'gnd',
      spec: { vtPlusFrac: 0.80, vtMinusFrac: 0.70 } },
    { id: 'sg2', type: 'schmitt', in: 'sense_inv', out: 'charge_gate', vcc: 'vcc', gnd: 'gnd' },
    { id: 'qcharge', type: 'pmos', value: 1.5, gate: 'charge_gate', drain: 'charge_node', source: 'vcc' },
    { id: 'rcharge', type: 'resistor', value: RCHARGE, a: 'charge_node', b: 'store' },
  ],
};

const capTrace = [];
const ledTrace = [];
const centerErrorTrace = [];
const chargeTrace = [];
let result;
for (let i = 0; i < STEPS; i++) {
  result = circuit.solve(elements, DT);
  const store = result.voltages.get('store');
  const ledI = Math.max(0, result.currents.get('led1') || 0);
  const vcc = result.voltages.get('vcc');
  const gnd = result.voltages.get('gnd');
  const center = result.voltages.get('center');
  const centerIdeal = (vcc + gnd) / 2;
  const chargeI = Math.abs(result.currents.get('qcharge') || 0);
  capTrace.push({ t: i * DT, value: store });
  ledTrace.push(ledI);
  centerErrorTrace.push(Math.abs(center - centerIdeal));
  chargeTrace.push(chargeI);
}

const settledCap = capTrace.slice(SETTLE);
const settledLed = ledTrace.slice(SETTLE);
const settledCenter = centerErrorTrace.slice(SETTLE);
const settledCharge = chargeTrace.slice(SETTLE);

const period = Sim.findPeriod(settledCap, { threshold: 3.75 });
const minStore = Math.min(...settledCap.map((p) => p.value));
const maxStore = Math.max(...settledCap.map((p) => p.value));
const minLed = Math.min(...settledLed);
const avgLed = settledLed.reduce((a, b) => a + b, 0) / settledLed.length;
const maxCenterError = Math.max(...settledCenter);
const chargeOnSamples = settledCharge.filter((i) => i > 1e-3).length;
const chargeOffSamples = settledCharge.filter((i) => i < 1e-5).length;
const avgOpticalW = settledLed.reduce(
  (sum, i) => sum + CircuitEngine.ledLightOutputW(i, 'white'), 0
) / settledLed.length;

console.log('=== Conventional flashlight reference/control ===');
console.log(`storage band measured: ${minStore.toFixed(4)} V .. ${maxStore.toFixed(4)} V`);
console.log(`LED current measured: min ${(minLed * 1000).toFixed(3)} mA, avg ${(avgLed * 1000).toFixed(3)} mA`);
console.log(`modeled average optical output: ${(avgOpticalW * 1000).toFixed(4)} mW`);
console.log(`reinjection crossings: ${period ? period.crossingCount : 0}, period: ${period ? (period.period * 1000).toFixed(3) + ' ms' : 'none'}`);
console.log(`charge gate samples: ON ${chargeOnSamples}, OFF ${chargeOffSamples}`);
console.log(`max center-reference midpoint error: ${(maxCenterError * 1000).toFixed(3)} mV`);

check('storage-does-not-collapse', minStore > 3.20,
  `minimum stored voltage ${minStore.toFixed(4)} V must stay above the white-LED collapse region`);
check('storage-is-bounded-below-source', maxStore < 4.60,
  `maximum stored voltage ${maxStore.toFixed(4)} V must remain below the 5 V source rather than rail-locking`);
check('hysteretic-reinjection-cycles', !!period && period.crossingCount >= 10,
  `control must repeatedly cross the intended storage band; got ${period ? period.crossingCount : 0} crossings`);
check('reinjection-has-real-coast-state', chargeOnSamples > 100 && chargeOffSamples > 100,
  `PMOS charge path must spend measurable time both conducting and disconnected: on=${chargeOnSamples}, off=${chargeOffSamples}`);
check('useful-light-never-drops-out', minLed > 0.003,
  `white LED must remain conducting through the coast interval; minimum ${(minLed * 1000).toFixed(3)} mA`);
check('useful-average-light-is-nontrivial', avgLed > 0.008,
  `average LED current ${(avgLed * 1000).toFixed(3)} mA must remain useful for this indicator-class LED model`);
check('center-reference-remains-a-real-midpoint', maxCenterError < 0.10,
  `buffered CENTER must track the actual source midpoint; worst error ${(maxCenterError * 1000).toFixed(3)} mV`);
check('no-solver-faults', !(result.warnings || []).some((w) => /singular|nan|failed/i.test(String(w))),
  `final solver warnings: ${(result.warnings || []).join('; ') || 'none'}`);

console.log(`\n=== conventional flashlight reference: ${failures} failed ===`);
if (failures) process.exit(1);
