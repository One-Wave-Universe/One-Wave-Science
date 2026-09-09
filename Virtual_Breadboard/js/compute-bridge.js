(function (root) {
  'use strict';

  if (!root.CircuitEngine || !root.CircuitEngine.Circuit) return;

  const OriginalCircuit = root.CircuitEngine.Circuit;
  const defaults = (root.electronAPI && root.electronAPI.computeDefaults) || {};
  const isJetson = defaults.role === 'jetson';
  const DEFAULT_PORT = Number(defaults.workerPort || 8787);
  const STORAGE_KEY = 'vbbJetsonHost';
  const PROBE_MS = 2500;
  const HEALTH_TIMEOUT_MS = 700;

  function randomSessionId() {
    if (root.crypto && typeof root.crypto.randomUUID === 'function') return root.crypto.randomUUID();
    return `vbb-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  function normalizeHost(value) {
    let host = String(value || '').trim();
    if (!host) return '';
    if (!/^https?:\/\//i.test(host)) host = `http://${host}`;
    host = host.replace(/\/$/, '');
    try {
      const u = new URL(host);
      if (!u.port) u.port = String(DEFAULT_PORT);
      return u.toString().replace(/\/$/, '');
    } catch (_) {
      return '';
    }
  }

  function configuredHost() {
    if (isJetson) return '';
    let stored = '';
    try { stored = root.localStorage.getItem(STORAGE_KEY) || ''; } catch (_) {}
    return normalizeHost(stored || defaults.jetsonHost || '');
  }

  function objectMap(value) {
    return new Map(Object.entries(value || {}));
  }

  function decodeResult(raw) {
    const roots = raw.roots || {};
    return {
      voltages: objectMap(raw.voltages),
      currents: objectMap(raw.currents),
      warnings: Array.isArray(raw.warnings) ? raw.warnings : [],
      mosfetStates: objectMap(raw.mosfetStates),
      coreStates: objectMap(raw.coreStates),
      coreFlux: objectMap(raw.coreFlux),
      comparatorStates: objectMap(raw.comparatorStates),
      latchStates: objectMap(raw.latchStates),
      hbridgeStates: objectMap(raw.hbridgeStates),
      schmittStates: objectMap(raw.schmittStates),
      batteryStates: objectMap(raw.batteryStates),
      uf: { find: (name) => Object.prototype.hasOwnProperty.call(roots, name) ? roots[name] : name },
      groundRoot: raw.groundRoot,
      hasCircuit: Boolean(raw.hasCircuit),
    };
  }

  const computeState = {
    host: configuredHost(),
    ready: false,
    probing: false,
    lastHealth: null,
    statusEl: null,
    lastError: '',
  };

  function setStatus(text, title) {
    if (!computeState.statusEl) return;
    computeState.statusEl.textContent = text;
    computeState.statusEl.title = title || '';
  }

  async function probeRemote() {
    if (!computeState.host || isJetson || computeState.probing) return false;
    computeState.probing = true;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);
    try {
      const res = await fetch(`${computeState.host}/health`, { cache: 'no-store', signal: controller.signal });
      const body = await res.json();
      computeState.ready = Boolean(res.ok && body && body.ok && body.protocol === 1);
      computeState.lastHealth = computeState.ready ? body : null;
      computeState.lastError = computeState.ready ? '' : 'incompatible worker';
    } catch (err) {
      computeState.ready = false;
      computeState.lastHealth = null;
      computeState.lastError = err && err.message ? err.message : 'unreachable';
    } finally {
      clearTimeout(timer);
      computeState.probing = false;
      updateStatus();
    }
    return computeState.ready;
  }

  function updateStatus() {
    if (isJetson) {
      setStatus('Compute: Jetson local', 'This Jetson runs the circuit solver locally and also serves LAN compute to a configured laptop.');
    } else if (!computeState.host) {
      setStatus('Compute: local', 'Click to set the Jetson IP/hostname. The simulator remains fully local until a Jetson is configured.');
    } else if (computeState.ready) {
      const h = computeState.lastHealth || {};
      setStatus(`Compute: Jetson ${h.hostname || ''}`.trim(), `Circuit solves are running on ${computeState.host}. Click to change the Jetson host.`);
    } else {
      setStatus('Compute: local fallback', `Jetson ${computeState.host} is not reachable yet${computeState.lastError ? `: ${computeState.lastError}` : ''}. Local solver is active; click to change host.`);
    }
  }

  function configureHost() {
    if (isJetson) {
      root.alert('This machine is the Jetson compute host. The circuit solver is already running locally here.');
      return;
    }
    const current = computeState.host.replace(/^https?:\/\//, '').replace(/:\d+$/, '');
    const value = root.prompt('Jetson IP or hostname (example: 192.168.4.23). Leave blank to use only this machine:', current);
    if (value === null) return;
    computeState.host = normalizeHost(value);
    computeState.ready = false;
    computeState.lastHealth = null;
    try {
      if (computeState.host) root.localStorage.setItem(STORAGE_KEY, computeState.host);
      else root.localStorage.removeItem(STORAGE_KEY);
    } catch (_) {}
    updateStatus();
    if (computeState.host) probeRemote();
  }

  function installStatusControl() {
    const button = document.createElement('button');
    button.type = 'button';
    button.id = 'vbbComputeStatus';
    button.style.cssText = 'position:fixed;right:12px;bottom:10px;z-index:10000;padding:7px 10px;border-radius:7px;border:1px solid #516174;background:#17202b;color:#dce7f2;font:12px/1.2 system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.25)';
    button.addEventListener('click', configureHost);
    document.body.appendChild(button);
    computeState.statusEl = button;
    updateStatus();
  }

  class DistributedCircuit {
    constructor() {
      this.local = new OriginalCircuit();
      this.sessionId = randomSessionId();
      this.lastRemoteResult = null;
      this.inFlight = false;
      this.pendingDt = 0;
      this.pendingElements = null;
      this.lastLocalResult = null;
    }

    _submitRemote() {
      if (!computeState.ready || !computeState.host || this.inFlight || !this.pendingElements) return;
      const elements = this.pendingElements;
      const dt = Math.min(Math.max(this.pendingDt, 0), 0.25);
      this.pendingElements = null;
      this.pendingDt = 0;
      this.inFlight = true;

      fetch(`${computeState.host}/v1/solve`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ sessionId: this.sessionId, elements, dt }),
        cache: 'no-store',
      })
        .then(async (res) => {
          const body = await res.json();
          if (!res.ok || !body || !body.ok) throw new Error((body && body.error) || `worker HTTP ${res.status}`);
          this.lastRemoteResult = decodeResult(body.result || {});
          computeState.ready = true;
          computeState.lastError = '';
        })
        .catch((err) => {
          computeState.ready = false;
          computeState.lastError = err && err.message ? err.message : 'remote solve failed';
          updateStatus();
        })
        .finally(() => {
          this.inFlight = false;
          if (computeState.ready && this.pendingElements) this._submitRemote();
        });
    }

    solve(elements, dt) {
      if (!computeState.host || isJetson || !computeState.ready) {
        this.lastLocalResult = this.local.solve(elements, dt);
        return this.lastLocalResult;
      }

      this.pendingElements = elements;
      this.pendingDt += Number(dt) || 0;
      this._submitRemote();

      if (this.lastRemoteResult) return this.lastRemoteResult;
      this.lastLocalResult = this.local.solve(elements, dt);
      return this.lastLocalResult;
    }
  }

  root.CircuitEngine.Circuit = DistributedCircuit;
  root.VBBCompute = {
    state: computeState,
    probe: probeRemote,
    configure: configureHost,
    useLocal: () => {
      computeState.host = '';
      computeState.ready = false;
      try { root.localStorage.removeItem(STORAGE_KEY); } catch (_) {}
      updateStatus();
    },
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installStatusControl, { once: true });
  else installStatusControl();

  if (computeState.host) {
    probeRemote();
    setInterval(() => { if (!computeState.ready) probeRemote(); }, PROBE_MS);
  }
})(typeof window !== 'undefined' ? window : this);
