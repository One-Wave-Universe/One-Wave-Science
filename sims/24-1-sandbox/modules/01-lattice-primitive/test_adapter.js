'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const A = require('./adapter.js');
const K = require('../../../00-lattice-primitive/lattice-kernel.js');
test('adapter exactly matches direct kernel states and measurements', () => {
  const state = A.initialize({parameters: {coupling: 3, damping: .02}, velocity: .2});
  const before = JSON.stringify(state), force = state.sites.map((_, i) => i === 0 ? .3 : 0);
  const direct = K.advance(state.sites, state.parameters, .002, force);
  const adapted = A.step(state, .002, force);
  assert.deepEqual(adapted.state.sites, direct.sites);
  assert.deepEqual(adapted.solver, direct.receipt);
  assert.deepEqual(A.measure(adapted.state), K.measure(direct.sites, state.parameters));
  assert.equal(JSON.stringify(state), before);
});
test('snapshot roundtrip continues the exact state and isolates ownership', () => {
  let state = A.step(A.initialize(), .002).state;
  const snapshot = A.serialize(state), restored = A.restore(JSON.parse(JSON.stringify(snapshot)));
  assert.deepEqual(A.step(restored, .003), A.step(state, .003));
  restored.sites[0].x = 99;
  assert.notEqual(snapshot.state.sites[0].x, 99);
  assert.notEqual(state.sites[0].x, 99);
});
test('geometry is state-driven 37-site 90-edge labeled projection', () => {
  const state = A.initialize(), before = JSON.stringify(state), g = A.geometry(state);
  assert.equal(g.points.length, 37); assert.equal(g.edges.length, 90);
  assert.equal(g.native_dimension, '2D'); assert.match(g.view, /projection/);
  for (const p of g.points) assert.equal(p.displacement, state.sites[p.id].x);
  g.points[0].ground[0] = 999;
  assert.equal(JSON.stringify(state), before);
});
test('zero control remains zero and deterministic receipts reproduce', () => {
  const a = A.run({amplitude: 0}, {steps: 20}), b = A.run({amplitude: 0}, {steps: 20});
  assert.deepEqual(a, b); assert.equal(a.status, 'completed');
  assert.equal(a.measurements.max_absolute_energy_drift, 0);
  assert.ok(a.final.state.sites.every(s => s.x === 0 && s.v === 0));
});
test('pulse receipt records measured values and finite accepted steps', () => {
  const r = A.run({}, {steps: 12, dt: .002});
  assert.equal(r.samples.length, 13); assert.equal(r.solver.length, 12);
  assert.equal(r.configuration.completed_steps, 12);
  assert.equal(r.measurements.final_energy, A.measure(A.restore(r.final)).energy);
  assert.equal(r.checks.finite_accepted_samples, true);
  assert.equal(r.physical_validation, 'unverified');
  assert.match(r.configuration.time_unit, /numerical/);
  assert.match(r.configuration.frequency_unit, /inverse numerical time/);
  assert.deepEqual(r.node_bindings.map(n => n.node_id), ['G-764']);
});
test('run failure preserves last accepted state and reports failure index', () => {
  const config = {parameters: {frequencyHz: 1e12}};
  const r = A.run(config, {steps: 2, dt: 1});
  assert.equal(r.status, 'failed'); assert.equal(r.failure.requested_step, 1);
  assert.equal(r.configuration.completed_steps, 0);
  assert.deepEqual(r.final.state, r.initial.state);
  assert.equal(r.checks.requested_steps_completed, false);
});
test('invalid options, inputs and topology are refused without clamping', () => {
  assert.throws(() => A.initialize({amplitude: NaN}));
  assert.throws(() => A.initialize({parameters: {madeUp: 1}}));
  assert.throws(() => A.run({}, {steps: 10001}));
  assert.throws(() => A.run({}, {dt: 0}));
  assert.throws(() => A.run({}, {steps: -1}));
  const s = A.initialize(), before = JSON.stringify(s);
  assert.throws(() => A.step(s, Infinity));
  assert.throws(() => A.step(s, .001, new Array(37)));
  assert.equal(JSON.stringify(s), before);
  s.sites[0].q += 1; assert.throws(() => A.geometry(s), /Topology/);
});
test('invalid restored state is rejected before JSON can mask nonfinite values', () => {
  const s = A.serialize(A.initialize()); s.state.sites[0].x = NaN;
  assert.throws(() => A.restore(s));
  assert.throws(() => A.restore({id: 'other'}));
});
test('manifest references resolve and source hashes identify source files', () => {
  const m = A.manifest(), hashes = A.references();
  assert.equal(m.adapter.entry_point, 'adapter.js');
  assert.equal(Object.keys(hashes).length, 5);
  for (const h of Object.values(hashes)) assert.match(h, /^[0-9a-f]{64}$/);
  const schema = JSON.parse(fs.readFileSync(path.resolve(__dirname, m.state_schema)));
  const s = A.serialize(A.initialize());
  for (const required of schema.required) assert.ok(Object.hasOwn(s, required));
});
test('missing module implementation prevents a successful run', () => {
  const exists = fs.existsSync;
  try {
    fs.existsSync = p => path.basename(p) === 'adapter.js' ? false : exists(p);
    assert.throws(() => A.run(), /Missing module reference/);
  } finally { fs.existsSync = exists; }
});
test('CLI returns parseable actual receipt without browser or output-file side effects', () => {
  const result = spawnSync(process.execPath, [path.join(__dirname, 'adapter.js')], {encoding: 'utf8'});
  assert.equal(result.status, 0, result.stderr);
  const r = JSON.parse(result.stdout);
  assert.equal(r.status, 'completed'); assert.equal(r.samples.length, 101);
});
test('CLI invalid request returns machine-readable error and nonzero status', () => {
  const result = spawnSync(process.execPath, [path.join(__dirname, 'adapter.js'), '/definitely-missing-lattice-request.json'], {encoding: 'utf8'});
  assert.equal(result.status, 2); assert.equal(JSON.parse(result.stdout).status, 'invalid');
});

test('source changes after import cannot be mislabeled as executed source', () => {
  const read = fs.readFileSync;
  try {
    fs.readFileSync = (p, ...args) => {
      const value = read(p, ...args);
      return String(p).endsWith('lattice-kernel.js') ? Buffer.concat([Buffer.from(value), Buffer.from('\n// changed')]) : value;
    };
    assert.throws(() => A.run({}, {steps: 0}), /Source changed since adapter import/);
  } finally { fs.readFileSync = read; }
});
