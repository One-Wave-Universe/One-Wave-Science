#!/usr/bin/env node
'use strict';

const assert = require('assert');
const CE = require('../js/circuit.js');
const { Circuit } = CE;
const Spice = require('../js/spice-analysis.js');

let checks = 0;
function ok(name, condition, detail = '') {
  checks++;
  console.log(`${condition ? 'PASS' : 'FAIL'} [${name}]${detail ? ' -- ' + detail : ''}`);
  assert(condition, `${name}${detail ? ': ' + detail : ''}`);
}

console.log('=== Virtual Breadboard musical-equipment fault qualification ===');

// 1) Broken/open guitar cable. The open conductor must be named OPEN, and
// the amp-side input must fall back through its real 1M input resistor rather
// than magically following the source through a disconnected lead.
{
  const els = { wires: [], components: [
    { id: 'SRC', type: 'battery', value: 1, a: 'tipSource', b: 'shield' },
    { id: 'CABLE_BREAK', type: 'switch', a: 'tipSource', b: 'tipAmp', closed: false },
    { id: 'RIN', type: 'resistor', value: 1e6, a: 'tipAmp', b: 'shield' },
  ] };
  const c = new Circuit();
  const r = c.solve(els, 1e-3);
  const d = CE.diagnose(els, r);
  const vAmp = r.voltages.get(r.uf.find('tipAmp')) || 0;
  const vShield = r.voltages.get(r.uf.find('shield')) || 0;
  ok('broken-guitar-cable-is-named-open', d.openComponents.some((x) => x.id === 'CABLE_BREAK'), JSON.stringify(d.openComponents));
  ok('broken-guitar-cable-does-not-teleport-signal', Math.abs(vAmp - vShield) < 1e-4, `amp-side=${vAmp - vShield}V`);
}

// 2) Completely disconnected cable fragment/shield. A cable physically lying
// on the board but connected to nothing must be named FLOATING, not plotted as
// a plausible zero-volt audio signal.
{
  const els = { wires: [], components: [
    { id: 'SUPPLY', type: 'battery', value: 9, a: 'vcc', b: 'gnd' },
    { id: 'RLOAD', type: 'resistor', value: 10000, a: 'vcc', b: 'gnd' },
    { id: 'BROKEN_CABLE', type: 'resistor', value: 10, a: 'looseTip', b: 'looseShield' },
  ] };
  const r = new Circuit().solve(els, 1e-3);
  const d = CE.diagnose(els, r);
  ok('unplugged-cable-fragment-is-floating', d.floatingNodes.includes('looseTip') && d.floatingNodes.includes('looseShield'), JSON.stringify(d.floatingNodes));
}

// 3) Shorted amplifier/headphone output. A near-zero load directly across a
// 9V source must hit the source's real current limit and be classified SHORT.
{
  const els = { wires: [], components: [
    { id: 'AMP_OUT', type: 'battery', value: 9, a: 'hot', b: 'return' },
    { id: 'SHORTED_JACK', type: 'resistor', value: 0.001, a: 'hot', b: 'return' },
  ] };
  const r = new Circuit().solve(els, 1e-3);
  const d = CE.diagnose(els, r);
  ok('shorted-audio-output-is-named-short', d.shorts.length > 0, JSON.stringify(d.shorts));
}

// 4) DC accidentally delivered to 32-ohm headphones. This circuit is finite
// so it is not a solver fault; instead measure the actual dangerous DC current
// and prove a series output capacitor removes that DC at steady state.
{
  const direct = { wires: [], components: [
    { id: 'DC', type: 'battery', value: 1, a: 'src', b: 'gnd' },
    { id: 'ROUT', type: 'resistor', value: 10, a: 'src', b: 'phones' },
    { id: 'HP', type: 'resistor', value: 32, a: 'phones', b: 'gnd' },
  ] };
  const directOp = Spice.operatingPoint(direct);
  const vHp = directOp.voltages.get('phones') || 0;
  const iHp = Math.abs(vHp / 32);
  ok('dc-coupled-headphones-receive-real-dc-current', iHp > 0.02, `Vhp=${vHp}V Ihp=${iHp}A`);

  const blocked = { wires: [], components: [
    { id: 'DC', type: 'battery', value: 1, a: 'src', b: 'gnd' },
    { id: 'ROUT', type: 'resistor', value: 10, a: 'src', b: 'precap' },
    { id: 'COUT', type: 'capacitor', value: 470e-6, a: 'precap', b: 'phones' },
    { id: 'HP', type: 'resistor', value: 32, a: 'phones', b: 'gnd' },
  ] };
  const blockedOp = Spice.operatingPoint(blocked);
  const blockedV = blockedOp.voltages.get('phones') || 0;
  ok('series-output-cap-blocks-headphone-dc', Math.abs(blockedV) < 2e-5, `Vhp=${blockedV}V`);
}

// 5) Pedal output accidentally connected to a 10-ohm load instead of a high-Z
// amp input. It should sag hard; the simulator must not preserve the unloaded
// level just because this is an "audio" circuit.
{
  function solveLoad(load) {
    const els = { wires: [], components: [
      { id: 'OUT', type: 'battery', value: 1, a: 'src', b: 'gnd' },
      { id: 'ROUT', type: 'resistor', value: 1000, a: 'src', b: 'jack' },
      { id: 'LOAD', type: 'resistor', value: load, a: 'jack', b: 'gnd' },
    ] };
    const r = new Circuit().solve(els, 1e-3);
    return (r.voltages.get(r.uf.find('jack')) || 0) - (r.voltages.get(r.uf.find('gnd')) || 0);
  }
  const normal = solveLoad(1000000);
  const accidental = solveLoad(10);
  ok('low-z-mispatch-drags-pedal-output', accidental < normal * 0.02, `1M=${normal}V 10ohm=${accidental}V`);
}

// 6) Balanced audio line with one conductor open. The line must report the
// open switch, and a differential load must collapse away from the healthy
// two-leg condition instead of silently treating one wire as still present.
{
  function line(openNegative) {
    const els = { wires: [], components: [
      { id: 'VP', type: 'diffsource', value: 1, sourceR: 100, a: 'pDrive', b: 'gnd' },
      { id: 'VN', type: 'diffsource', value: -1, sourceR: 100, a: 'nDrive', b: 'gnd' },
      { id: 'PWIRE', type: 'switch', a: 'pDrive', b: 'p', closed: true },
      { id: 'NWIRE', type: 'switch', a: 'nDrive', b: 'n', closed: !openNegative },
      { id: 'LOAD', type: 'resistor', value: 10000, a: 'p', b: 'n' },
    ] };
    const r = new Circuit().solve(els, 1e-3);
    const d = CE.diagnose(els, r);
    const diff = (r.voltages.get(r.uf.find('p')) || 0) - (r.voltages.get(r.uf.find('n')) || 0);
    return { diff, d };
  }
  const good = line(false);
  const broken = line(true);
  ok('broken-balanced-leg-is-named-open', broken.d.openComponents.some((x) => x.id === 'NWIRE'), JSON.stringify(broken.d.openComponents));
  ok('broken-balanced-leg-collapses-differential-level', Math.abs(broken.diff) < Math.abs(good.diff) * 0.60, `healthy=${good.diff}V broken=${broken.diff}V`);
}

// 7) Phantom-power-style symmetric feed is self-current-limited by the real
// 6.81k resistors. Shorting one microphone leg is a fault, but it must stay
// in milliamp scale rather than becoming an impossible infinite-current rail.
{
  const els = { wires: [], components: [
    { id: 'V48', type: 'battery', value: 48, a: 'v48', b: 'gnd' },
    { id: 'FEED', type: 'resistor', value: 6810, a: 'v48', b: 'pin2' },
    { id: 'SHORT', type: 'resistor', value: 0.01, a: 'pin2', b: 'gnd' },
  ] };
  const r = new Circuit().solve(els, 1e-3);
  const iFeed = Math.abs(r.currents.get('FEED') || 0);
  ok('phantom-feed-short-stays-resistor-limited', iFeed > 0.005 && iFeed < 0.01, `I=${iFeed}A`);
}

console.log(`\n=== ALL ${checks} MUSICAL-EQUIPMENT FAULT CHECKS PASSED ===`);
