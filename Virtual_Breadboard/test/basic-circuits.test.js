#!/usr/bin/env node
/*
 * Basic-circuit reality check: build simple, ordinary circuits and prove
 * the simulator's answer against an INDEPENDENT hand-calculation (real
 * Ohm's law / nodal analysis worked from scratch, never copied from the
 * solver's own output), not just "the trace looks plausible."
 *
 * This file specifically covers two basic, everyday circuits that had NO
 * real hand-calculated regression anywhere in the repo before now:
 *   - a potentiometer used as a voltage divider (unloaded and loaded)
 *   - a Wheatstone bridge (a genuine multi-node/multi-loop network, not
 *     just a single series/parallel chain like every other basic test)
 *
 * Every "expected" value below is computed by an independent nodal-
 * analysis implementation written directly in this file (real Kirchhoff's
 * current law, real Ohm's law, including the battery's own real internal
 * resistance) -- it does not call into js/circuit.js at all. If the
 * simulator's real answer doesn't match, the fix is to the simulator's
 * physics, never to loosen this file's own independent math.
 *
 * Run with: node test/basic-circuits.test.js
 */
const CircuitEngine = require('../js/circuit.js');
const { Circuit } = CircuitEngine;

let checkCount = 0;
function qual(name, expected, actual, tolerance, note) {
  checkCount++;
  const pass = typeof expected === 'boolean' ? expected === actual : Math.abs(actual - expected) <= tolerance;
  const line = `${pass ? 'PASS' : 'FAIL'} [${name}] expected=${expected} actual=${actual}${tolerance != null ? ' tolerance=' + tolerance : ''}${note ? ' -- ' + note : ''}`;
  console.log(line);
  if (!pass) throw new Error('BASIC CIRCUIT REALITY CHECK FAILED: ' + name);
}

// A small, from-scratch Gaussian-elimination nodal solver, used ONLY to
// compute this file's own independent "expected" values -- structurally
// similar to any textbook nodal-analysis method, but written here without
// reference to js/circuit.js's own solveLinear/stamping code.
function independentNodalSolve(A, b) {
  const n = b.length;
  const M = A.map((row, i) => row.concat([b[i]]));
  for (let col = 0; col < n; col++) {
    let piv = col, max = Math.abs(M[col][col]);
    for (let r = col + 1; r < n; r++) if (Math.abs(M[r][col]) > max) { max = Math.abs(M[r][col]); piv = r; }
    if (piv !== col) { const t = M[col]; M[col] = M[piv]; M[piv] = t; }
    const pv = M[col][col];
    for (let r = 0; r < n; r++) {
      if (r === col) continue;
      const f = M[r][col] / pv;
      for (let c = col; c <= n; c++) M[r][c] -= f * M[col][c];
    }
  }
  return Array.from({ length: n }, (_, i) => M[i][n] / M[i][i]);
}

console.log('=== Basic circuit: potentiometer as a voltage divider ===');
{
  // Independent hand-calc: a real battery (with its own real internal
  // resistance) feeding a potentiometer wired end-to-end as a divider.
  // Two unknowns: P (the rail voltage after the battery's own Rint drop)
  // and W (the wiper voltage) -- ground is the reference (0V).
  function expectedPotWiper(totalOhms, pos, loadOhms) {
    const r1 = totalOhms * pos; // rail(+) to wiper
    const r2 = totalOhms * (1 - pos); // wiper to ground
    const Rint = CircuitEngine.BATTERY_RINT;
    const EMF = 9;
    // KCL at P: (P-EMF)/Rint + (P-W)/r1 = 0
    // KCL at W: (W-P)/r1 + W/r2 + (loadOhms ? W/loadOhms : 0) = 0
    const gLoad = loadOhms ? 1 / loadOhms : 0;
    const A = [
      [1 / Rint + 1 / r1, -1 / r1],
      [-1 / r1, 1 / r1 + 1 / r2 + gLoad],
    ];
    const b = [EMF / Rint, 0];
    const [, W] = independentNodalSolve(A, b);
    return W;
  }

  function simPotWiper(totalOhms, pos, loadOhms) {
    const c = new Circuit();
    const components = [
      { id: 'bat1', type: 'battery', value: 9, a: 'p', b: 'g' },
      { id: 'pot1', type: 'potentiometer', value: totalOhms, pos, a: 'p', wiper: 'w', b: 'g' },
    ];
    if (loadOhms) components.push({ id: 'rload', type: 'resistor', value: loadOhms, a: 'w', b: 'g' });
    const res = c.solve({ wires: [], components }, 0.001);
    return res.voltages.get('w');
  }

  [0.25, 0.5, 0.75].forEach((pos) => {
    const expected = expectedPotWiper(10000, pos, null);
    const actual = simPotWiper(10000, pos, null);
    qual(`pot-unloaded-wiper-at-pos-${pos}`, expected, actual, 1e-4,
      `a 10k pot at wiper position ${pos} (unloaded) must match the real linear-taper divider formula, including the battery's own real internal resistance`);
  });

  const expectedLoaded = expectedPotWiper(10000, 0.5, 2500);
  const actualLoaded = simPotWiper(10000, 0.5, 2500);
  qual('pot-loaded-wiper-sags-per-real-thevenin', expectedLoaded, actualLoaded, 1e-4,
    `loading the wiper with a real 2.5k resistor must sag the reading to exactly the real Thevenin-loaded value (${expectedLoaded.toFixed(4)}V), not stay at the ideal unloaded value`);

  const unloadedAtHalf = simPotWiper(10000, 0.5, null);
  qual('pot-loading-genuinely-changes-the-reading', true, Math.abs(actualLoaded - unloadedAtHalf) > 1.5, null,
    `loading the wiper must produce a real, visible sag versus the unloaded reading (unloaded=${unloadedAtHalf.toFixed(3)}V, loaded=${actualLoaded.toFixed(3)}V) -- a passive divider must never silently hold its ideal value under load`);
}

console.log('\n=== Basic circuit: Wheatstone bridge (multi-node network) ===');
{
  // Independent hand-calc: 3 real unknowns (P after the battery's Rint
  // drop, and the two bridge midpoints A and B) -- a genuinely different
  // topology from every single-loop/simple-divider test elsewhere in this
  // repo, proving the solver handles real multi-node KCL, not just chains.
  function expectedBridge(R1, R2, R3, R4, Rg) {
    const Rint = CircuitEngine.BATTERY_RINT;
    const EMF = 10;
    const A = [
      [1 / Rint + 1 / R1 + 1 / R3, -1 / R1, -1 / R3],
      [-1 / R1, 1 / R1 + 1 / R2 + 1 / Rg, -1 / Rg],
      [-1 / R3, -1 / Rg, 1 / R3 + 1 / R4 + 1 / Rg],
    ];
    const b = [EMF / Rint, 0, 0];
    const [, Va, Vb] = independentNodalSolve(A, b);
    return { Va, Vb, Ig: (Va - Vb) / Rg };
  }

  function simBridge(R1, R2, R3, R4, Rg) {
    const c = new Circuit();
    const els = { wires: [], components: [
      { id: 'bat1', type: 'battery', value: 10, a: 'p', b: 'g' },
      { id: 'r1', type: 'resistor', value: R1, a: 'p', b: 'a' },
      { id: 'r2', type: 'resistor', value: R2, a: 'a', b: 'g' },
      { id: 'r3', type: 'resistor', value: R3, a: 'p', b: 'b' },
      { id: 'r4', type: 'resistor', value: R4, a: 'b', b: 'g' },
      { id: 'rg', type: 'resistor', value: Rg, a: 'a', b: 'b' },
    ] };
    const res = c.solve(els, 0.001);
    return { Va: res.voltages.get('a'), Vb: res.voltages.get('b'), Ig: res.currents.get('rg') };
  }

  // Balanced bridge (R1/R2 == R3/R4): real physics says the bridge current
  // is exactly zero REGARDLESS of the bridge resistor's own value -- a
  // classic, well-known real property, checked at two very different Rg
  // values to prove it's not a coincidence of one particular number.
  [1000, 1e6].forEach((rg) => {
    const expected = expectedBridge(1000, 1000, 1000, 1000, rg);
    const actual = simBridge(1000, 1000, 1000, 1000, rg);
    qual(`bridge-balanced-zero-current-at-rg-${rg}`, 0, actual.Ig, 1e-9,
      `a real balanced bridge (R1/R2 == R3/R4) must show exactly zero bridge current at Rg=${rg}ohm, matching the hand-derived value of ${expected.Ig}`);
    qual(`bridge-balanced-midpoints-equal-at-rg-${rg}`, expected.Va, actual.Va, 1e-4,
      `both bridge midpoints must sit at the same real voltage when balanced`);
  });

  // Unbalanced bridge (a real 10% mismatch on one leg): a genuine,
  // nonzero, independently hand-calculated bridge current and midpoint
  // voltages -- the actual real-world basis for how a bridge sensor
  // (strain gauge, RTD, etc.) reports an unbalance.
  const expectedUnbal = expectedBridge(1000, 1000, 1000, 1100, 1000);
  const actualUnbal = simBridge(1000, 1000, 1000, 1100, 1000);
  qual('bridge-unbalanced-va-matches-hand-calc', expectedUnbal.Va, actualUnbal.Va, 1e-3,
    `a real 10% mismatch on R4 must move midpoint A to exactly the hand-calculated ${expectedUnbal.Va.toFixed(4)}V`);
  qual('bridge-unbalanced-vb-matches-hand-calc', expectedUnbal.Vb, actualUnbal.Vb, 1e-3,
    `and midpoint B to exactly the hand-calculated ${expectedUnbal.Vb.toFixed(4)}V`);
  qual('bridge-unbalanced-current-matches-hand-calc', expectedUnbal.Ig, actualUnbal.Ig, 1e-6,
    `and a real nonzero bridge current of ${(expectedUnbal.Ig * 1000).toFixed(4)}mA must flow between the two midpoints`);
}

console.log(`\n=== ALL ${checkCount} BASIC-CIRCUIT REALITY CHECKS PASSED ===`);
