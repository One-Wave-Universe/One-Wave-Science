'use strict';

const http = require('http');
const os = require('os');
const { Circuit } = require('./js/circuit.js');

const DEFAULT_PORT = 8787;
const MAX_BODY_BYTES = 8 * 1024 * 1024;
const SESSION_TTL_MS = 30 * 60 * 1000;

function normalizeAddress(address) {
  if (!address) return '';
  return String(address).replace(/^::ffff:/, '');
}

function isPrivatePeer(address) {
  const ip = normalizeAddress(address);
  if (ip === '127.0.0.1' || ip === '::1') return true;
  if (/^10\./.test(ip) || /^192\.168\./.test(ip)) return true;
  const m = ip.match(/^172\.(\d{1,3})\./);
  if (m && Number(m[1]) >= 16 && Number(m[1]) <= 31) return true;
  if (/^(fc|fd)[0-9a-f]{2}:/i.test(ip) || /^fe80:/i.test(ip)) return true;
  return false;
}

function mapObject(value) {
  return value instanceof Map ? Object.fromEntries(value) : {};
}

function serializeResult(result) {
  const roots = {};
  if (result && result.uf && result.uf.parent instanceof Map) {
    for (const name of result.uf.parent.keys()) {
      if (name !== undefined) roots[name] = result.uf.find(name);
    }
  }
  return {
    voltages: mapObject(result && result.voltages),
    currents: mapObject(result && result.currents),
    warnings: Array.isArray(result && result.warnings) ? result.warnings : [],
    mosfetStates: mapObject(result && result.mosfetStates),
    coreStates: mapObject(result && result.coreStates),
    coreFlux: mapObject(result && result.coreFlux),
    comparatorStates: mapObject(result && result.comparatorStates),
    latchStates: mapObject(result && result.latchStates),
    hbridgeStates: mapObject(result && result.hbridgeStates),
    schmittStates: mapObject(result && result.schmittStates),
    batteryStates: mapObject(result && result.batteryStates),
    roots,
    groundRoot: result && result.groundRoot,
    hasCircuit: Boolean(result && result.hasCircuit),
  };
}

function sendJson(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(body),
    'access-control-allow-origin': '*',
    'access-control-allow-methods': 'GET,POST,OPTIONS',
    'access-control-allow-headers': 'content-type',
    'cache-control': 'no-store',
  });
  res.end(body);
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new Error('request too large'));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}'));
      } catch (err) {
        reject(new Error('invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

function createWorkerServer(options = {}) {
  const sessions = new Map();
  const port = Number(options.port == null ? process.env.VBB_WORKER_PORT || DEFAULT_PORT : options.port);
  const bind = options.bind || process.env.VBB_WORKER_BIND || '127.0.0.1';
  const privateOnly = options.privateOnly !== false;

  function getSession(id) {
    const key = String(id || 'default').slice(0, 200);
    let entry = sessions.get(key);
    if (!entry) {
      entry = { circuit: new Circuit(), touchedAt: Date.now() };
      sessions.set(key, entry);
    }
    entry.touchedAt = Date.now();
    return entry;
  }

  function pruneSessions() {
    const cutoff = Date.now() - SESSION_TTL_MS;
    for (const [key, entry] of sessions) {
      if (entry.touchedAt < cutoff) sessions.delete(key);
    }
  }

  const server = http.createServer(async (req, res) => {
    if (req.method === 'OPTIONS') {
      res.writeHead(204, {
        'access-control-allow-origin': '*',
        'access-control-allow-methods': 'GET,POST,OPTIONS',
        'access-control-allow-headers': 'content-type',
      });
      res.end();
      return;
    }

    if (privateOnly && !isPrivatePeer(req.socket.remoteAddress)) {
      sendJson(res, 403, { ok: false, error: 'LAN-only worker: peer is not a private/local address' });
      return;
    }

    if (req.method === 'GET' && req.url === '/health') {
      pruneSessions();
      sendJson(res, 200, {
        ok: true,
        service: 'one-wave-vbb-compute',
        protocol: 1,
        hostname: os.hostname(),
        platform: process.platform,
        arch: process.arch,
        sessions: sessions.size,
      });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/reset') {
      try {
        const body = await readJson(req);
        sessions.delete(String(body.sessionId || 'default').slice(0, 200));
        sendJson(res, 200, { ok: true });
      } catch (err) {
        sendJson(res, 400, { ok: false, error: err.message });
      }
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/solve') {
      try {
        const body = await readJson(req);
        if (!body.elements || !Array.isArray(body.elements.components) || !Array.isArray(body.elements.wires)) {
          sendJson(res, 400, { ok: false, error: 'elements.components and elements.wires are required arrays' });
          return;
        }
        const dt = Number(body.dt);
        if (!Number.isFinite(dt) || dt < 0 || dt > 1) {
          sendJson(res, 400, { ok: false, error: 'dt must be a finite number from 0 to 1 second' });
          return;
        }
        const entry = getSession(body.sessionId);
        const result = entry.circuit.solve(body.elements, dt);
        sendJson(res, 200, { ok: true, result: serializeResult(result) });
      } catch (err) {
        sendJson(res, 500, { ok: false, error: err && err.message ? err.message : String(err) });
      }
      return;
    }

    sendJson(res, 404, { ok: false, error: 'not found' });
  });

  server.vbb = { bind, port, sessions };
  return server;
}

function startStandalone() {
  const port = Number(process.env.VBB_WORKER_PORT || DEFAULT_PORT);
  const bind = process.env.VBB_WORKER_BIND || '0.0.0.0';
  const server = createWorkerServer({ bind, port, privateOnly: true });
  server.listen(port, bind, () => {
    console.log(`[VBB compute] LAN worker listening on http://${bind}:${port}`);
  });
}

if (require.main === module) startStandalone();

module.exports = { DEFAULT_PORT, createWorkerServer, isPrivatePeer, serializeResult };
