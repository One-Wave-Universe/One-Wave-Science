#!/usr/bin/env node
/*
 * The 17 permanent regression builds (test/regression-builds/01_*.js
 * through 17_*.js). Each is its own small, real circuit with real
 * expected/actual/tolerance checks -- rerun this file after every major
 * update to js/circuit.js or simulate.js. No eyeballing a waveform and
 * calling it good: every check below prints PASS/FAIL and this script
 * exits nonzero the moment any check fails.
 *
 * Run with: node test/run_regression_builds.js
 */
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'regression-builds');
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

console.log(`\n=== ${files.length} regression builds, ${totalChecks} checks, ${totalFailed} failed ===`);
if (totalFailed > 0) process.exit(1);
