#!/usr/bin/env node
/*
 * The flashlight-adjacent calibration pack (test/flashlight-calibration/
 * 01_*.js through 05_*.js) -- a second, distinct pack from the 17
 * permanent regression builds (test/regression-builds/), built specifically
 * to bracket the real electronics the One-Wave flashlight build will
 * actually use: a real 3.7V single-cell LED rail, a MOSFET switch driving
 * that same LED, a coil's real L/R step response, a flyback-clamped coil,
 * and a reversible H-bridge driving an inductive load. Every check's
 * "expected" value is hand-calculated from a real formula (Ohm's law,
 * Vf+I*Ron, L/R exponential, diode clamp voltage), independent of the
 * solver -- same discipline as run_regression_builds.js.
 *
 * Run with: node test/run_flashlight_calibration.js
 */
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'flashlight-calibration');
const files = fs.readdirSync(dir)
  .filter((f) => /^\d{2}_.*\.js$/.test(f))
  .sort();

let totalChecks = 0;
let totalFailed = 0;
files.forEach((f) => {
  const build = require(path.join(dir, f));
  const { name, checks } = build.run();
  console.log(`\n=== ${name} ===`);
  checks.forEach((c) => {
    totalChecks++;
    const line = `${c.pass ? 'PASS' : 'FAIL'} [${c.name}] expected=${c.expected} actual=${c.actual}${c.tolerance != null ? ' tolerance=' + c.tolerance : ''}${c.note ? ' -- ' + c.note : ''}`;
    console.log(line);
    if (!c.pass) totalFailed++;
  });
});

console.log(`\n=== ${files.length} flashlight-calibration builds, ${totalChecks} checks, ${totalFailed} failed ===`);
if (totalFailed > 0) process.exit(1);
