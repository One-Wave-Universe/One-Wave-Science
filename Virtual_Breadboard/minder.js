'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { Circuit } = require('./js/circuit.js');

const DEFAULT_AUDIT_INTERVAL_MS = 10 * 60 * 1000;
const SUPPORTED_MODEL_FAMILIES = new Set([
  'mosfet-switch-with-body-diode',
  'dual-push-pull-comparator',
  'rail-splitter',
  'resistor',
  'capacitor',
  'inductor',
  'diode',
  'led',
  'voltage-source',
]);

function finiteNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function safeId(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 100);
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function atomicWriteJson(file, value) {
  ensureDir(path.dirname(file));
  const tmp = `${file}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2) + '\n', 'utf8');
  fs.renameSync(tmp, file);
}

function voltageAt(result, node) {
  if (!result || !result.uf || !result.voltages) return NaN;
  return result.voltages.get(result.uf.find(node));
}

function runRealityCircuits() {
  const checks = [];

  function record(name, pass, detail) {
    checks.push({ name, pass: Boolean(pass), detail });
  }

  // Ordinary electronics first: 5 V across equal 1k resistors must put the
  // midpoint at ~2.5 V. If this breaks, no experimental One-Wave circuit is
  // allowed to claim success on top of it.
  {
    const c = new Circuit();
    const elements = {
      wires: [],
      components: [
        { id: 'bat', type: 'battery', a: 'vcc', b: 'gnd', value: 5 },
        { id: 'r1', type: 'resistor', a: 'vcc', b: 'mid', value: 1000 },
        { id: 'r2', type: 'resistor', a: 'mid', b: 'gnd', value: 1000 },
      ],
    };
    const result = c.solve(elements, 1 / 1000);
    const v = voltageAt(result, 'mid');
    record('ordinary resistor divider', Number.isFinite(v) && Math.abs(v - 2.5) < 0.05, `mid=${v} V; expected about 2.5 V`);
  }

  // TLE2426-class rail splitter sanity check: the model is allowed to be
  // simplified, but its core claim must remain a 1/2-input-span reference.
  {
    const c = new Circuit();
    const elements = {
      wires: [],
      components: [
        { id: 'bat', type: 'battery', a: 'vcc', b: 'gnd', value: 5 },
        { id: 'vg', type: 'vgnd', a: 'vcc', b: 'gnd', out: 'v0' },
        { id: 'load', type: 'resistor', a: 'v0', b: 'gnd', value: 100000 },
      ],
    };
    const result = c.solve(elements, 1 / 1000);
    const v = voltageAt(result, 'v0');
    record('virtual-ground midpoint', Number.isFinite(v) && Math.abs(v - 2.5) < 0.05, `v0=${v} V; expected about 2.5 V under a light load`);
  }

  // RC memory must evolve through time instead of teleporting to the final
  // value. This protects the transient solver the breadboard depends on.
  {
    const c = new Circuit();
    const elements = {
      wires: [],
      components: [
        { id: 'bat', type: 'battery', a: 'vcc', b: 'gnd', value: 5 },
        { id: 'r', type: 'resistor', a: 'vcc', b: 'mid', value: 1000 },
        { id: 'cap', type: 'capacitor', a: 'mid', b: 'gnd', value: 100e-6 },
      ],
    };
    const first = c.solve(elements, 0.001);
    const v1 = voltageAt(first, 'mid');
    let last = first;
    for (let i = 0; i < 250; i++) last = c.solve(elements, 0.001);
    const v2 = voltageAt(last, 'mid');
    record('RC transient evolves', Number.isFinite(v1) && Number.isFinite(v2) && v2 > v1 && v2 < 5.1, `first=${v1} V, later=${v2} V`);
  }

  return checks;
}

function validateCatalog(catalog) {
  const checks = [];
  const parts = catalog && Array.isArray(catalog.parts) ? catalog.parts : [];
  checks.push({ name: 'catalog has parts array', pass: Array.isArray(catalog && catalog.parts), detail: `${parts.length} entries` });

  const ids = new Set();
  for (const part of parts) {
    const errors = [];
    if (!safeId(part.id)) errors.push('missing id');
    if (ids.has(part.id)) errors.push('duplicate id');
    ids.add(part.id);
    if (!part.manufacturer) errors.push('missing manufacturer');
    if (!part.partNumber) errors.push('missing partNumber');
    if (!SUPPORTED_MODEL_FAMILIES.has(part.modelFamily)) errors.push(`unsupported modelFamily ${part.modelFamily}`);
    if (!/^https:\/\//.test(String(part.sourceUrl || ''))) errors.push('missing https primary source');
    if (!part.parameters || typeof part.parameters !== 'object') errors.push('missing parameters');
    else {
      for (const [key, value] of Object.entries(part.parameters)) {
        if (!finiteNumber(value)) errors.push(`parameter ${key} is not a finite number`);
      }
    }
    if (!Array.isArray(part.acceptanceTests) || part.acceptanceTests.length === 0) errors.push('missing acceptance tests');
    checks.push({ name: `catalog:${part.id || 'unnamed'}`, pass: errors.length === 0, detail: errors.length ? errors.join('; ') : 'reality evidence present' });
  }
  return checks;
}

function validateCandidate(candidate) {
  const errors = [];
  const id = safeId(candidate && (candidate.id || candidate.partNumber));
  if (!id) errors.push('id or partNumber is required');
  if (!candidate || !candidate.manufacturer) errors.push('manufacturer is required');
  if (!candidate || !candidate.partNumber) errors.push('partNumber is required');
  if (!candidate || !SUPPORTED_MODEL_FAMILIES.has(candidate.modelFamily)) errors.push('candidate must map to an already-supported physical model family');
  if (!candidate || !/^https:\/\//.test(String(candidate.sourceUrl || ''))) errors.push('an https manufacturer/datasheet source is required');
  if (!candidate || !candidate.parameters || typeof candidate.parameters !== 'object' || Object.keys(candidate.parameters).length === 0) errors.push('bounded electrical parameters are required');
  else {
    for (const [key, value] of Object.entries(candidate.parameters)) {
      if (!finiteNumber(value)) errors.push(`parameter ${key} must be a finite number`);
    }
  }
  if (!candidate || !Array.isArray(candidate.acceptanceTests) || candidate.acceptanceTests.length === 0) errors.push('at least one behavior acceptance test is required');
  return { ok: errors.length === 0, id, errors };
}

class BreadboardMinder {
  constructor(options = {}) {
    this.rootDir = options.rootDir || __dirname;
    this.catalogFile = options.catalogFile || path.join(this.rootDir, 'reality', 'part-catalog.json');
    this.stateDir = options.stateDir || path.join(os.homedir(), '.one-wave-vbb-minder');
    this.intervalMs = Number(options.intervalMs || process.env.VBB_MINDER_INTERVAL_MS || DEFAULT_AUDIT_INTERVAL_MS);
    this.timer = null;
    this.lastReport = null;
    ensureDir(this.stateDir);
  }

  loadCatalog() {
    return JSON.parse(fs.readFileSync(this.catalogFile, 'utf8'));
  }

  auditNow() {
    const startedAt = new Date().toISOString();
    const checks = [];
    try {
      const catalog = this.loadCatalog();
      checks.push(...validateCatalog(catalog));
    } catch (err) {
      checks.push({ name: 'catalog readable', pass: false, detail: err.message });
    }

    try {
      checks.push(...runRealityCircuits());
    } catch (err) {
      checks.push({ name: 'reality circuit suite', pass: false, detail: err.stack || err.message });
    }

    const sourceChecks = [
      ['solver source present', path.join(this.rootDir, 'js', 'circuit.js')],
      ['component palette present', path.join(this.rootDir, 'js', 'components.js')],
      ['compute bridge present', path.join(this.rootDir, 'js', 'compute-bridge.js')],
    ];
    for (const [name, file] of sourceChecks) checks.push({ name, pass: fs.existsSync(file), detail: file });

    const failed = checks.filter((c) => !c.pass);
    const report = {
      schemaVersion: 1,
      startedAt,
      finishedAt: new Date().toISOString(),
      host: os.hostname(),
      platform: process.platform,
      arch: process.arch,
      status: failed.length ? 'FAIL' : 'PASS',
      checks,
      failedCount: failed.length,
      rule: 'A failed ordinary-electronics or evidence check blocks reality-bound promotion. Experimental behavior may still be explored, but it must stay labeled experimental.',
    };
    this.lastReport = report;
    atomicWriteJson(path.join(this.stateDir, 'last-audit.json'), report);
    return report;
  }

  status() {
    if (this.lastReport) return this.lastReport;
    const file = path.join(this.stateDir, 'last-audit.json');
    if (fs.existsSync(file)) {
      try { this.lastReport = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (_) {}
    }
    return this.lastReport || { status: 'NOT_RUN', failedCount: null, checks: [] };
  }

  stageCandidate(candidate) {
    const validation = validateCandidate(candidate);
    if (!validation.ok) return { ok: false, errors: validation.errors };
    const entry = {
      ...candidate,
      id: validation.id,
      status: 'candidate',
      stagedAt: new Date().toISOString(),
      realityRule: 'Candidate only. It is not active until its model behavior is implemented or mapped, tested, and explicitly promoted.',
    };
    const file = path.join(this.stateDir, 'candidates', `${validation.id}.json`);
    atomicWriteJson(file, entry);
    return { ok: true, id: validation.id, file, candidate: entry };
  }

  listCandidates() {
    const dir = path.join(this.stateDir, 'candidates');
    if (!fs.existsSync(dir)) return [];
    return fs.readdirSync(dir)
      .filter((name) => name.endsWith('.json'))
      .sort()
      .map((name) => {
        try { return JSON.parse(fs.readFileSync(path.join(dir, name), 'utf8')); }
        catch (err) { return { id: name, status: 'BROKEN', error: err.message }; }
      });
  }

  start() {
    if (this.timer) return;
    this.auditNow();
    this.timer = setInterval(() => {
      try { this.auditNow(); }
      catch (err) { console.error('[VBB minder] audit failed:', err); }
    }, Math.max(60_000, this.intervalMs));
    if (this.timer.unref) this.timer.unref();
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
    this.timer = null;
  }
}

if (require.main === module) {
  const minder = new BreadboardMinder();
  const report = minder.auditNow();
  console.log(JSON.stringify(report, null, 2));
  if (process.argv.includes('--audit') && report.status !== 'PASS') process.exitCode = 1;
}

module.exports = {
  BreadboardMinder,
  SUPPORTED_MODEL_FAMILIES,
  validateCatalog,
  validateCandidate,
  runRealityCircuits,
};
