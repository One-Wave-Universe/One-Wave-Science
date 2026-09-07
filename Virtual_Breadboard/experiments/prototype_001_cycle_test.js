#!/usr/bin/env node
/*
 * 100+ cycle automated reliability test for PROTOTYPE_001. Not a repeat of
 * the same trial 100 times (this circuit has no cycle-count-dependent wear
 * model to exercise that way) -- instead, each trial is a genuinely
 * different, independent build: real component-tolerance Monte Carlo
 * (js/circuit.js's own COMPONENT_TOLERANCE bands, the same machinery
 * simulate.js's --monteCarlo mode uses) PLUS a randomized write-pulse
 * duration spanning from well under the relay's real switchTau (3ms) up
 * to comfortably over it. That directly tests the real, physical question
 * item #1 of the milestone asked for: does a marginal drive pulse
 * genuinely, sometimes, fail to fully switch the core -- not assumed, not
 * scripted, read back from the real physical contact every time.
 *
 * Run with:
 *   node experiments/prototype_001_cycle_test.js [trials]
 */
const fs = require('fs');
const path = require('path');
const Board = require('../js/board.js');
const AIBuilder = require('../js/ai.js');
const Sim = require('../simulate.js');

const TRIALS = Number(process.argv[2]) > 0 ? Number(process.argv[2]) : 100;
const SEED = 20260906;

const specPath = path.join(__dirname, 'prototype_001.json');
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));

const { ok, errors, parts: validatedParts } = AIBuilder.validateSpec(spec);
if (!ok) { console.error(JSON.stringify({ ok: false, errors })); process.exit(1); }

const layoutKey = spec.layout || '1large';
const layout = Sim.LAYOUT_PRESETS[layoutKey];
const board = Board.build(layout);
board.layoutKey = layoutKey;

const { parts: resolvedParts, errors: holeErrors } = Sim.resolveTerminals(board, validatedParts);
if (holeErrors.length) { console.error(JSON.stringify({ ok: false, errors: holeErrors })); process.exit(1); }

const { names: nodeNameCellIds, errors: nnErrors } = Sim.resolveNodeNames(board, spec.nodeNames);
if (nnErrors.length) { console.error(JSON.stringify({ ok: false, errors: nnErrors })); process.exit(1); }
const measurements = spec.measurements || [];
const snapOpts = { nodeNameCellIds, measurements };

// real logic-level classification thresholds -- the same 100k/contactR
// divider used in the circuit swings close to the full 0V/5V rails, so a
// wide honest margin (not a hair-trigger 2.5V midpoint) separates a real
// "closed" reading from a real "open" one; anything in between is neither,
// and is reported as such rather than rounded to the nearer rail.
const CLOSED_MIN = 4.0;
const OPEN_MAX = 1.0;
function classify(v) {
  if (v == null) return 'unknown';
  if (v >= CLOSED_MIN) return 'closed';
  if (v <= OPEN_MAX) return 'open';
  return 'ambiguous';
}

const rng = Sim.mulberry32(SEED);
const results = [];

for (let trial = 0; trial < TRIALS; trial++) {
  const perturbed = Sim.perturbParts(resolvedParts, rng);
  const pulseMs = 1 + rng() * 14; // 1..15ms, straddling switchTau=3ms
  const pulseS = pulseMs / 1000;

  const experimentSpec = {
    stages: [
      // establish a known baseline: both relays commanded Void first
      { name: 'init_void', seconds: 0.03, dt: 0.001, set: [
        { partId: 'in1A', field: 'value', value: 0 }, { partId: 'in2A', field: 'value', value: 5 },
        { partId: 'in1B', field: 'value', value: 0 }, { partId: 'in2B', field: 'value', value: 5 },
      ] },
      // the real test: drive A to Field for exactly pulseMs, nothing else touched
      { name: 'write', seconds: pulseS, dt: 0.0002, set: [
        { partId: 'in1A', field: 'value', value: 5 }, { partId: 'in2A', field: 'value', value: 0 },
      ] },
      // remove drive entirely and hold -- whatever the contact reads now is
      // held by real remanence alone, exactly like the main prototype file
      { name: 'hold', seconds: 0.1, dt: 0.001, set: [
        { partId: 'in1A', field: 'value', value: 0 }, { partId: 'in2A', field: 'value', value: 0 },
      ] },
    ],
    events: [
      { label: 'senseA_closed', node: 'SENSEA', threshold: 2.5, direction: 'rising' },
    ],
    persistence: null,
    traces: [{ label: 'SenseA', node: 'SENSEA', settleBandFrac: 0.02 }],
  };

  let rep;
  try {
    rep = Sim.runExperiment(perturbed, experimentSpec, snapOpts);
  } catch (e) {
    results.push({ trial, pulseMs, outcome: 'solver_error', error: e.message });
    continue;
  }

  const holdStage = rep.stages.find((s) => s.name === 'hold');
  const senseA = holdStage.snapshot.namedVoltages.SENSEA;
  const senseB = holdStage.snapshot.namedVoltages.SENSEB;
  const coreA = holdStage.snapshot.coreStates ? holdStage.snapshot.coreStates.lrA : null;
  const aState = classify(senseA);
  const bState = classify(senseB);

  // B was never commanded to move -- any B state other than "open" is a
  // real cross-talk/wrong-write fault, not just "A didn't switch"
  let outcome;
  if (bState !== 'open') outcome = 'wrong_write'; // B moved when it shouldn't have
  else if (aState === 'closed') outcome = 'success';
  else if (aState === 'open') outcome = 'missed_write'; // pulse too short/weak, genuinely never switched
  else outcome = 'ambiguous'; // partial switch, neither rail -- a real transitioning/fault state

  const closeEvent = rep.events.find((e) => e.label === 'senseA_closed');
  const settledAt = holdStage.traces.SenseA ? Number((holdStage.traces.SenseA.settledAt - holdStage.startT).toFixed(6)) : null;

  results.push({
    trial, pulseMs: Number(pulseMs.toFixed(3)), outcome,
    senseA: Number(senseA.toFixed(4)), senseB: Number(senseB.toFixed(4)), coreA: coreA != null ? Number(coreA.toFixed(4)) : null,
    closeLatencyMs: closeEvent ? Number(((closeEvent.t - (rep.stages[1].startT)) * 1000).toFixed(4)) : null,
    holdSettleMs: settledAt != null ? Number((settledAt * 1000).toFixed(4)) : null,
    warnings: rep.final.warnings,
  });
}

// --- aggregate statistics ---
const counts = {};
results.forEach((r) => { counts[r.outcome] = (counts[r.outcome] || 0) + 1; });

const successRows = results.filter((r) => r.outcome === 'success');
const settleTimes = successRows.map((r) => r.holdSettleMs).filter((v) => v != null);
const closeLatencies = successRows.filter((r) => r.closeLatencyMs != null).map((r) => r.closeLatencyMs);

function stats(arr) {
  if (!arr.length) return null;
  const n = arr.length;
  const mean = arr.reduce((a, b) => a + b, 0) / n;
  const sorted = [...arr].sort((a, b) => a - b);
  return { n, min: sorted[0], max: sorted[n - 1], mean: Number(mean.toFixed(4)), median: sorted[Math.floor(n / 2)] };
}

// bucket outcome by pulse width relative to the real switchTau (3ms) --
// this is the actual disproving/boundary-finding result: does the real
// failure rate rise sharply below switchTau, as real magnetic switching
// physics predicts, or does something else (component tolerance) blur
// that boundary in practice?
const buckets = [
  { label: '<1.5ms (well under switchTau)', test: (p) => p < 1.5 },
  { label: '1.5-3ms (near switchTau)', test: (p) => p >= 1.5 && p < 3 },
  { label: '3-6ms (just over switchTau)', test: (p) => p >= 3 && p < 6 },
  { label: '>=6ms (comfortably over switchTau)', test: (p) => p >= 6 },
];
const bucketStats = buckets.map((b) => {
  const rows = results.filter((r) => b.test(r.pulseMs));
  const succ = rows.filter((r) => r.outcome === 'success').length;
  return { bucket: b.label, n: rows.length, success: succ, missed: rows.filter((r) => r.outcome === 'missed_write').length, ambiguous: rows.filter((r) => r.outcome === 'ambiguous').length, wrong: rows.filter((r) => r.outcome === 'wrong_write').length, successRate: rows.length ? Number((succ / rows.length).toFixed(3)) : null };
});

const warningTrials = results.filter((r) => r.warnings && r.warnings.length);

const report = {
  ok: true,
  trials: TRIALS,
  seed: SEED,
  outcomeCounts: counts,
  successRate: Number((counts.success || 0) / TRIALS).toFixed(3),
  closeLatencyMsStats: stats(closeLatencies),
  holdSettleMsStats: stats(settleTimes),
  byPulseWidth: bucketStats,
  warningTrialCount: warningTrials.length,
  sampleWarnings: warningTrials.slice(0, 5).map((r) => ({ trial: r.trial, pulseMs: r.pulseMs, warnings: r.warnings })),
  wrongWriteTrials: results.filter((r) => r.outcome === 'wrong_write').map((r) => ({ trial: r.trial, pulseMs: r.pulseMs, senseA: r.senseA, senseB: r.senseB })),
};

console.log(JSON.stringify(report, null, 2));
