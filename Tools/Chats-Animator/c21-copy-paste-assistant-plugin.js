(() => {
  'use strict';

  const A = window.Animator;
  const host = window.OneWaveAssistantPlugins;
  const directorPanel = document.getElementById('director-dialogue');
  if (!A || !host || !directorPanel) throw new Error('C21 requires Animator + assistant plugin host + Director dialogue');

  const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));
  const directorLog = directorPanel.querySelector('#director-log');
  let lastBackend = null;

  const statusCard = document.createElement('section');
  statusCard.id = 'assistant-live-bridge';
  statusCard.style.marginTop = '10px';
  statusCard.innerHTML = `
    <div class="card">
      <strong>Live AI creative partner</strong><br>
      <span id="assistant-live-state">Checking local AI…</span>
      <div style="margin-top:8px"><button id="assistant-live-retry" type="button">Retry AI connection</button></div>
    </div>
    <div id="assistant-key-panel" class="card" hidden style="margin-top:8px">
      <strong>OpenAI connection</strong>
      <div id="assistant-key-status" style="margin:7px 0;color:#b8bdc8">Checking key status…</div>
      <label for="assistant-api-key" style="display:block;font-weight:700;margin-bottom:5px">API key</label>
      <input id="assistant-api-key" type="password" autocomplete="off" spellcheck="false"
             placeholder="Paste key here once"
             style="width:100%;padding:9px;border:1px solid #414551;border-radius:8px;background:#0c0e12;color:#f5f6f8">
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px">
        <button id="assistant-key-show" type="button">Show key</button>
        <button id="assistant-key-save" type="button">Save & Connect</button>
        <button id="assistant-key-close" type="button">Close</button>
      </div>
      <div style="margin-top:7px;color:#8f96a3;font-size:12px">A saved key is identified only by its last 4 characters. The full saved key is never displayed back.</div>
    </div>
  `;
  directorPanel.appendChild(statusCard);

  const state = document.getElementById('assistant-live-state');
  const retry = document.getElementById('assistant-live-retry');
  const keyPanel = document.getElementById('assistant-key-panel');
  const keyStatus = document.getElementById('assistant-key-status');
  const keyInput = document.getElementById('assistant-api-key');
  const keyShow = document.getElementById('assistant-key-show');
  const keySave = document.getElementById('assistant-key-save');
  const keyClose = document.getElementById('assistant-key-close');

  function setState(message) {
    state.textContent = message;
    A.status(message);
  }

  function addMessage(kind, message) {
    if (!directorLog || !String(message || '').trim()) return;
    const row = document.createElement('div');
    row.className = 'director-message';
    row.textContent = `${kind}: ${String(message).trim()}`;
    directorLog.appendChild(row);
    directorLog.scrollTop = directorLog.scrollHeight;
  }

  function describeKey(info) {
    if (info?.connected || info?.key_saved) {
      const suffix = info?.key_suffix ? ` ending in ${info.key_suffix}` : '';
      return `A key is already saved${suffix}. Paste a new one only if you want to replace it.`;
    }
    return 'No API key is saved yet. Paste it once, then click Save & Connect.';
  }

  async function health(report = false) {
    try {
      const response = await fetch('/api/assistant/health', { cache: 'no-store' });
      const info = await response.json();
      if (!response.ok || !info.ok || !info.server) throw new Error(info.error || `HTTP ${response.status}`);

      keyStatus.textContent = describeKey(info);
      if (info.connected) {
        const label = info.model || info.backend || 'AI';
        setState(`AI connected — ${label}`);
        if (report) addMessage('AI', `Connected and ready — ${label}.`);
      } else {
        const detail = info.error ? ` — ${info.error}` : '';
        setState(`Animator server ready; AI model not connected${detail}`);
        if (report) addMessage('AI', `Animator server is ready, but no AI model is connected${detail}.`);
      }
      return info;
    } catch (error) {
      const message = `Animator AI server unavailable: ${error.message || error}`;
      setState(message);
      keyStatus.textContent = message;
      if (report) addMessage('AI', message);
      return null;
    }
  }

  async function openSetup() {
    keyPanel.hidden = false;
    keyInput.value = '';
    keyInput.type = 'password';
    keyShow.textContent = 'Show key';
    await health(false);
    keyInput.focus();
  }

  async function saveAndConnect() {
    const apiKey = keyInput.value.trim();
    if (!apiKey) {
      keyStatus.textContent = 'Paste the API key first. If a key is already saved, you do not need to enter it again.';
      return;
    }
    keySave.disabled = true;
    keyStatus.textContent = 'Validating and saving key…';
    try {
      const response = await fetch('/api/assistant/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ apiKey })
      });
      const body = await response.json();
      if (!response.ok || !body?.ok) throw new Error(body?.error || `HTTP ${response.status}`);
      keyInput.value = '';
      keyInput.type = 'password';
      keyShow.textContent = 'Show key';
      keyStatus.textContent = `Key saved and validated${body.key_suffix ? ` — ending in ${body.key_suffix}` : ''}.`;
      setState(`AI connected — ${body.model || 'OpenAI'}`);
      addMessage('AI', 'Connection configured and ready.');
      await health(false);
    } catch (error) {
      keyStatus.textContent = `Could not connect: ${error.message || error}`;
      setState('AI key setup failed');
    } finally {
      keySave.disabled = false;
    }
  }

  async function call(kind, payload) {
    setState(`AI ${kind === 'director' ? 'thinking with you' : 'creating'}…`);
    try {
      const response = await fetch('/api/assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          apiVersion: 'one-wave-assistant-plugin/v1',
          kind,
          payload: clone(payload)
        })
      });

      let body;
      try {
        body = await response.json();
      } catch (_error) {
        throw new Error(`AI server returned HTTP ${response.status} without JSON`);
      }

      if (!response.ok || !body?.ok) throw new Error(body?.error || `AI server HTTP ${response.status}`);
      const result = body.result || {};
      lastBackend = result._backend || null;
      delete result._backend;
      const backendLabel = lastBackend?.model || lastBackend?.type || 'AI';
      setState(`AI connected — ${backendLabel}`);
      if (kind === 'director') addMessage('AI', result.message || 'Ready.');
      return result;
    } catch (error) {
      const message = `AI could not answer: ${error.message || error}`;
      setState(message);
      addMessage('AI', message);
      return {
        pending: true,
        stage: kind === 'director' ? 'Director' : 'Dream',
        message
      };
    }
  }

  host.register({
    id: 'live-ai-creative-partner',
    name: 'Live AI Creative Partner',
    version: '5',
    capabilities: ['director', 'asset', 'provider-neutral', 'local-ready', 'human-ai-cocreative'],
    director(payload) { return call('director', payload); },
    asset(job) { return call('asset', job); },
    metadata: {
      transport: 'local-http',
      storesApiKeys: true,
      apiKeyStorage: 'local-user-config',
      role: 'The human and AI are the primary creative participants. Dream/Director may delegate small routine jobs to automatic support without replacing either creator.'
    }
  });

  host.use('live-ai-creative-partner');

  retry.addEventListener('click', openSetup);
  keyShow.addEventListener('click', () => {
    const showing = keyInput.type === 'text';
    keyInput.type = showing ? 'password' : 'text';
    keyShow.textContent = showing ? 'Show key' : 'Hide key';
    keyInput.focus();
  });
  keySave.addEventListener('click', saveAndConnect);
  keyClose.addEventListener('click', () => {
    keyInput.value = '';
    keyPanel.hidden = true;
  });
  keyInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') saveAndConnect();
  });

  A.assistantBridge = {
    id: 'live-ai-creative-partner',
    health,
    openSetup,
    get backend() { return clone(lastBackend); }
  };

  health().then((info) => {
    if (info && !info.connected) openSetup();
  });
})();
