#!/usr/bin/env node
/*
 * 10_RECEIPTS -- every test produces a receipt (00_RULES/architecture.md).
 *
 * This script runs the repo's real test sources (test/qualification.test.js,
 * test/primitives.test.js, test/regression-builds/*.js) and writes one
 * receipt file per check in the canonical form:
 *
 *   TEST:
 *   LAYER:
 *   VERSION:
 *   EXPECTED:
 *   ACTUAL:
 *   TOLERANCE:
 *   PASS/FAIL:
 *   DEPENDENCIES:
 *   NOTES:
 *
 * Receipts land in 10_RECEIPTS/current/ (this run) and are copied into
 * 10_RECEIPTS/passing/ or 10_RECEIPTS/failing/ by outcome, so "did anything
 * regress since last time" is a directory diff, not a memory exercise.
 *
 * This intentionally does NOT re-run test/circuit.test.js: that file uses
 * assert.ok()/a custom approx() helper rather than the qual()/check()
 * structured-record pattern the other three suites use, so it has no
 * structured records to export yet. It still runs and must still pass --
 * see package.json's "test" script -- it just isn't emitting receipts here
 * until it's given the same instrumentation, which is real, separate,
 * Layer-09 work and not bundled into this pass.
 *
 * Run with: node 10_RECEIPTS/generate_receipts.js
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.join(__dirname, '..');

function gitVersion() {
  try {
    return execSync('git rev-parse --short HEAD', { cwd: ROOT }).toString().trim();
  } catch (e) {
    return 'unknown';
  }
}
const VERSION = gitVersion();

// Regression builds are each already scoped to one primary layer -- see
// 09_TESTS/MAP.md for the reasoning behind each assignment.
const REGRESSION_BUILD_LAYER = {
  '01_resistor_divider': '03_ELECTRICAL_CORE',
  '02_led_current_limiting': '01_PARTS',
  '03_rc_lowpass_filter': '04_TIME_AND_DYNAMICS',
  '04_rc_highpass_filter': '04_TIME_AND_DYNAMICS',
  '05_lc_ringdown': '04_TIME_AND_DYNAMICS',
  '06_diode_rectifier': '01_PARTS',
  '07_mosfet_lowside_switch': '01_PARTS',
  '08_mosfet_highside_switch': '06_PRIMITIVES',
  '09_halfbridge_deadtime': '06_PRIMITIVES',
  '10_fullbridge_differential_load': '01_PARTS',
  '11_comparator_threshold': '01_PARTS',
  '12_schmitt_hysteresis': '04_TIME_AND_DYNAMICS',
  '13_relaxation_oscillator': '04_TIME_AND_DYNAMICS',
  '14_transformer_turns_ratio': '07_MAGNETICS',
  '15_three_winding_nerve': '07_MAGNETICS',
  '16_battery_led_runtime': '08_POWER',
  '17_balanced_differential_cell': '06_PRIMITIVES',
};

function sanitize(name) {
  return name.replace(/[^a-zA-Z0-9_-]/g, '_');
}

function receiptText(r) {
  return [
    `TEST: ${r.test}`,
    `LAYER: ${r.layer}`,
    `VERSION: ${VERSION}`,
    `EXPECTED: ${r.expected}`,
    `ACTUAL: ${r.actual}`,
    `TOLERANCE: ${r.tolerance != null ? r.tolerance : 'n/a (boolean check)'}`,
    `PASS/FAIL: ${r.pass ? 'PASS' : 'FAIL'}`,
    `DEPENDENCIES: ${r.dependencies}`,
    `NOTES: ${r.note || ''}`,
    '',
  ].join('\n');
}

function collectFromQualification() {
  // no battery here -- unrelated; this just loads the module fresh each run
  delete require.cache[require.resolve('../test/qualification.test.js')];
  const mod = require('../test/qualification.test.js');
  return mod.records.map((rec) => ({
    test: `qualification.test.js :: ${rec.name}`,
    layer: 'multiple (see 09_TESTS/MAP.md — this suite spans the first gate plus fundamental tests across parts/connections/electrical_core/dynamics/power/magnetics)',
    dependencies: 'js/circuit.js, simulate.js',
    ...rec,
  }));
}

function collectFromPrimitives() {
  delete require.cache[require.resolve('../test/primitives.test.js')];
  const mod = require('../test/primitives.test.js');
  return mod.records.map((rec) => ({
    test: `primitives.test.js :: ${rec.name}`,
    layer: '06_PRIMITIVES (built from js/circuit.js parts across multiple lower layers)',
    dependencies: 'js/circuit.js, simulate.js',
    ...rec,
  }));
}

function collectFromRegressionBuilds() {
  const dir = path.join(ROOT, 'test', 'regression-builds');
  const files = fs.readdirSync(dir).filter((f) => /^\d{2}_.*\.js$/.test(f)).sort();
  const out = [];
  files.forEach((f) => {
    const key = f.replace(/\.js$/, '');
    const build = require(path.join(dir, f));
    const { name, checks } = build.run();
    checks.forEach((c) => {
      out.push({
        test: `regression-builds/${f} :: ${c.name}`,
        layer: REGRESSION_BUILD_LAYER[key] || 'unclassified',
        dependencies: 'js/circuit.js, simulate.js',
        expected: c.expected,
        actual: c.actual,
        tolerance: c.tolerance,
        pass: c.pass,
        note: c.note,
      });
    });
    void name;
  });
  return out;
}

function run() {
  const currentDir = path.join(__dirname, 'current');
  const passingDir = path.join(__dirname, 'passing');
  const failingDir = path.join(__dirname, 'failing');
  [currentDir, passingDir, failingDir].forEach((d) => {
    fs.rmSync(d, { recursive: true, force: true });
    fs.mkdirSync(d, { recursive: true });
  });

  let records = [];
  let crashed = null;
  try {
    records = records.concat(collectFromRegressionBuilds());
  } catch (e) {
    crashed = { source: 'regression-builds', error: e.message };
  }
  try {
    records = records.concat(collectFromQualification());
  } catch (e) {
    records.push({
      test: 'qualification.test.js :: (crashed before completing)',
      layer: 'unknown -- see error',
      dependencies: 'js/circuit.js, simulate.js',
      expected: 'suite completes',
      actual: `threw: ${e.message}`,
      tolerance: null,
      pass: false,
      note: 'qualification.test.js throws on its first failing check, so records after the failure point were never generated. Read the thrown check name to find the failing layer.',
    });
  }
  try {
    records = records.concat(collectFromPrimitives());
  } catch (e) {
    records.push({
      test: 'primitives.test.js :: (crashed before completing)',
      layer: 'unknown -- see error',
      dependencies: 'js/circuit.js, simulate.js',
      expected: 'suite completes',
      actual: `threw: ${e.message}`,
      tolerance: null,
      pass: false,
      note: 'primitives.test.js throws on its first failing check.',
    });
  }

  let passCount = 0, failCount = 0;
  records.forEach((r, i) => {
    const fname = `${String(i + 1).padStart(4, '0')}_${sanitize(r.test)}.txt`;
    const text = receiptText(r);
    fs.writeFileSync(path.join(currentDir, fname), text);
    fs.writeFileSync(path.join(r.pass ? passingDir : failingDir, fname), text);
    if (r.pass) passCount++; else failCount++;
  });

  console.log(`Wrote ${records.length} receipts to 10_RECEIPTS/current/ (${passCount} passing, ${failCount} failing)`);
  if (crashed) {
    console.log(`NOTE: ${crashed.source} crashed before producing any records: ${crashed.error}`);
  }
  if (failCount > 0 || crashed) process.exit(1);
}

run();
