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
  `;
  directorPanel.appendChild(statusCard);

  const state = document.getElementById('assistant-live-state');
  const retry = document.getElementById('assistant-live-retry');

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

  async function health(report = false) {
    try {
      const response = await fetch('/api/assistant/health', { cache: 'no-store' });
      const info = await response.json();
      if (!response.ok || !info.ok) throw new Error(info.error || `HTTP ${response.status}`);
      setState(`AI server ready — ${info.backend}${info.model ? ` / ${info.model}` : ''}`);
      if (report) addMessage('AI', 'Connection is ready.');
      return info;
    } catch (error) {
      const message = `AI connection unavailable: ${error.message || error}`;
      setState(message);
      if (report) addMessage('AI', `${message}. The animator still works; only the AI connection is offline.`);
      return null;
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
      setState(`Connected — ${backendLabel}`);
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
    version: '3',
    capabilities: ['director', 'asset', 'provider-neutral', 'local-ready', 'human-ai-cocreative'],
    director(payload) { return call('director', payload); },
    asset(job) { return call('asset', job); },
    metadata: {
      transport: 'local-http',
      storesApiKeys: false,
      role: 'The human and AI are the Dream/Director creative pair. Delegated automatic support may handle small routine pieces, but it does not replace either creator.'
    }
  });

  host.use('live-ai-creative-partner');
  retry.addEventListener('click', () => health(true));

  A.assistantBridge = {
    id: 'live-ai-creative-partner',
    health,
    get backend() { return clone(lastBackend); }
  };

  health();
})();
