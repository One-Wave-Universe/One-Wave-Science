'use strict';
// Adapter only: the numerical update and observables remain in the G-764 kernel.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {execFileSync} = require('node:child_process');
let K, KERNEL_LOAD_ERROR;
try { K = require('../../../00-lattice-primitive/lattice-kernel.js'); }
catch (error) { KERNEL_LOAD_ERROR = error; }
const ROOT = path.resolve(__dirname, '../../../..');
const ID = 'lattice-primitive';
const NODE = 'Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md';
const SOURCES = [NODE, 'sims/00-lattice-primitive/lattice-kernel.js',
  'sims/24-1-sandbox/modules/01-lattice-primitive/adapter.js',
  'sims/24-1-sandbox/modules/01-lattice-primitive/manifest.json',
  'sims/00-state-container/state-schema.json'];
const DEFAULTS = {frequencyHz: 1, coupling: 1, damping: 0, nonlinearity: 0};
const LIMITATIONS = ['Numerical software scope only; no physical validity or calibrated lattice spacing.',
  'Spatial/domain convergence, group-velocity calibration and nonlinear confinement are unverified.',
  'Browser visual review is unverified. Height is a displacement projection, not native 3D.',
  'D-412 is the governing standard, not a claim of full compliance.',
  'G-766 dispersion/octave fixture is a separate control, not executed by this adapter.',
  'Hashes identify import-time source files, not bytecode of CommonJS modules preloaded by another caller.',
  'Compression, vorticity field, boundary leakage and physical work balance are unavailable.'];
const clone = value => JSON.parse(JSON.stringify(value));
function finite(value, label) {
  if (!Number.isFinite(value)) throw new RangeError(label + ' must be finite');
  return value;
}
function keys(object, allowed, label) {
  if (!object || typeof object !== 'object' || Array.isArray(object)) throw new TypeError(label + ' must be an object');
  for (const key of Object.keys(object)) if (!allowed.includes(key)) throw new RangeError('Unknown ' + label + ': ' + key);
}
function topology() {
  const sites = [], indices = new Map();
  for (let q = -3; q <= 3; q++) for (let r = Math.max(-3, -q - 3); r <= Math.min(3, -q + 3); r++) {
    indices.set(q + ',' + r, sites.length);
    sites.push({q, r, x: 0, v: 0, phase: 0, n: []});
  }
  const directions = [[1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1], [0, 1]];
  for (const site of sites) site.n = directions.map(([q, r]) => indices.get((site.q + q) + ',' + (site.r + r))).filter(i => i !== undefined);
  return sites;
}
function validateState(state) {
  keys(state, ['sites', 'parameters', 'time', 'steps'], 'state');
  keys(state.parameters, Object.keys(DEFAULTS), 'parameter');
  K.measure(state.sites, state.parameters);
  finite(state.time, 'time');
  if (state.time < 0 || !Number.isSafeInteger(state.steps) || state.steps < 0) throw new RangeError('Invalid time/step count');
  const reference = topology();
  if (state.sites.length !== reference.length) throw new RangeError('Expected 37 sites');
  state.sites.forEach((s, i) => {
    if (s.q !== reference[i].q || s.r !== reference[i].r || JSON.stringify(s.n) !== JSON.stringify(reference[i].n)) throw new RangeError('Topology mismatch');
  });
  return state;
}
function initialize(config = {}) {
  keys(config, ['parameters', 'amplitude', 'velocity'], 'configuration');
  keys(config.parameters || {}, Object.keys(DEFAULTS), 'parameter');
  const parameters = {...DEFAULTS, ...config.parameters}, sites = topology();
  const center = sites.find(s => s.q === 0 && s.r === 0);
  center.x = finite(config.amplitude === undefined ? 1 : config.amplitude, 'amplitude');
  center.v = finite(config.velocity === undefined ? 0 : config.velocity, 'velocity');
  center.phase = Math.atan2(center.v / K.parameters(parameters).w, center.x);
  return validateState({sites, parameters, time: 0, steps: 0});
}
function measure(state) { validateState(state); return K.measure(state.sites, state.parameters); }
function step(state, dt, forces = []) {
  validateState(state); finite(dt, 'dt');
  if (dt <= 0) throw new RangeError('dt must be positive');
  const result = K.advance(state.sites, state.parameters, dt, forces);
  const next = validateState({sites: result.sites, parameters: {...state.parameters}, time: state.time + dt, steps: state.steps + 1});
  if (next.time <= state.time) throw new RangeError('Time does not advance at this precision');
  return {state: next, solver: result.receipt};
}
function geometry(state) {
  validateState(state);
  return {native_dimension: '2D', view: 'displacement-height projection', units: 'numerical',
    points: state.sites.map((s, id) => ({id, ground: [s.q + s.r / 2, Math.sqrt(3) * s.r / 2], displacement: s.x, velocity: s.v})),
    edges: state.sites.flatMap((s, i) => s.n.filter(j => j > i).map(j => [i, j]))};
}
function manifest() { return JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json'), 'utf8')); }
function references() {
  const m = manifest();
  for (const reference of [m.state_schema, m.adapter.existing, m.adapter.entry_point]) {
    if (typeof reference !== 'string' || !fs.existsSync(path.resolve(__dirname, reference))) throw new Error('Missing module reference: ' + reference);
  }
  const node = fs.readFileSync(path.join(ROOT, NODE), 'utf8');
  if (!/^node_id:\s*["']?G-764["']?\s*$/m.test(node)) throw new Error('Canonical node identity mismatch');
  return Object.fromEntries(SOURCES.map(p => [p, crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT, p))).digest('hex')]));
}
function serialize(state) {
  validateState(state);
  return {id: ID, state: clone(state), measurements: Object.entries(measure(state)).map(([name, value]) => ({name, value, unit: 'numerical'})),
    provenance: {source: NODE, version: 'lattice-adapter/v1', seed: null, randomness: 'none'}};
}
function restore(snapshot) {
  if (!snapshot || snapshot.id !== ID || snapshot.provenance?.version !== 'lattice-adapter/v1') throw new RangeError('Unsupported snapshot');
  validateState(snapshot.state);
  return clone(snapshot.state);
}
function run(config = {}, options = {}) {
  keys(options, ['steps', 'dt'], 'run option');
  const count = options.steps === undefined ? 100 : options.steps;
  const dt = options.dt === undefined ? .001 : options.dt;
  if (!Number.isInteger(count) || count < 0 || count > 10000) throw new RangeError('steps must be 0..10000');
  finite(dt, 'dt'); if (dt <= 0) throw new RangeError('dt must be positive');
  if (KERNEL_LOAD_ERROR) throw KERNEL_LOAD_ERROR;
  if (IMPORT_SOURCE_ERROR) throw IMPORT_SOURCE_ERROR;
  const hashes = references();
  if (JSON.stringify(hashes) !== JSON.stringify(IMPORT_SOURCE_HASHES)) throw new Error('Source changed since adapter import; restart before running');
  let state = initialize(config), failure = null;
  const initial = serialize(state), samples = [{time: 0, measurements: measure(state)}], solver = [];
  for (let i = 0; i < count; i++) {
    try { const next = step(state, dt); state = next.state; solver.push(next.solver); samples.push({time: state.time, measurements: measure(state)}); }
    catch (error) { failure = {requested_step: i + 1, name: error.name, message: error.message}; break; }
  }
  let commit = null;
  try { commit = execFileSync('git', ['rev-parse', 'HEAD'], {cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore']}).trim(); } catch (_) { /* File hashes remain authoritative without Git. */ }
  const energies = samples.map(s => s.measurements.energy), energy0 = energies[0];
  return {schema: 'one-wave-lattice-run/v1', module: ID, node_bindings: [{node_id: 'G-764', source: NODE, scope: 'bounded numerical oscillator lattice'}],
    claim_gate: manifest().claim_gate, status: failure ? 'failed' : 'completed', physical_validation: 'unverified',
    provenance: {commit, source_sha256: hashes, commit_is_context_only: true, source_identity: 'import-time source files; rechecked before run'},
    configuration: {parameters: {...state.parameters}, dt, requested_steps: count, completed_steps: state.steps, seed: null, randomness: 'none', drive: 'none', time_unit: 'numerical time; uncalibrated', frequency_unit: 'inverse numerical time; uncalibrated', spacing: 'numerical unit', boundary: 'open radius-3 triangular graph'},
    initial, final: serialize(state), geometry: geometry(state), samples, solver,
    measurements: {initial_energy: energy0, final_energy: energies.at(-1), max_absolute_energy_drift: Math.max(...energies.map(e => Math.abs(e - energy0)))},
    checks: {finite_accepted_samples: samples.every(s => Object.values(s.measurements).every(Number.isFinite)), requested_steps_completed: state.steps === count},
    failure, limitations: [...LIMITATIONS]};
}
let IMPORT_SOURCE_HASHES, IMPORT_SOURCE_ERROR;
try { IMPORT_SOURCE_HASHES = references(); }
catch (error) { IMPORT_SOURCE_ERROR = error; }
module.exports = {manifest, initialize, step, measure, geometry, serialize, restore, references, run};
if (require.main === module) {
  try {
    if (process.argv.length > 3) throw new Error('Usage: node adapter.js [request.json]');
    const request = process.argv[2] ? JSON.parse(fs.readFileSync(process.argv[2], 'utf8')) : {};
    keys(request, ['configuration', 'run'], 'request');
    const receipt = run(request.configuration, request.run);
    process.stdout.write(JSON.stringify(receipt, null, 2) + '\n');
    if (receipt.status !== 'completed') process.exitCode = 1;
  } catch (error) { process.stdout.write(JSON.stringify({schema: 'one-wave-lattice-run/v1', status: 'invalid', error: {name: error.name, message: error.message}}) + '\n'); process.exitCode = 2; }
}
