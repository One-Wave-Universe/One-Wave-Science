(() => {
  'use strict';

  const A = window.Animator;
  const host = window.OneWaveAssistantPlugins;
  const directorPanel = document.getElementById('director-dialogue');
  if (!A || !host || !directorPanel) throw new Error('C21 requires Animator + assistant plugin host + Director dialogue');

  const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));
  let lastBackend = null;

  const statusCard = document.createElement('section');
  statusCard.id = 'assistant-live-bridge';
  statusCard.style.marginTop = '10px';
  statusCard.innerHTML = `
    <div class="card">
      <strong>Live AI creative partner</strong><br>
      <span id="assistant-live-state">Checking local AI…</span>
    </div>
  `;
  directorPanel.appendChild(statusCard);

  const state = document.getElementById('assistant-live-state');

  function setState(message) {
    state.textContent = message;
    A.status(message);
  }

  async function health() {
    try {
      const response = await fetch('/api/assistant/health', { cache: 'no-store' });
      const info = await response.json();
      if (!response.ok || !info.ok) throw new Error(info.error || `HTTP ${response.status}`);
      setState(`AI server ready — ${info.backend}${info.model ? ` / ${info.model}` : ''}`);
      return info;
    } catch (error) {
      setState(`AI server unavailable: ${error.message || error}`);
      return null;
    }
  }

  async function call(kind, payload) {
    setState(`AI ${kind === 'director' ? 'thinking with you' : 'creating'}…`);
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
    return result;
  }

  host.register({
    id: 'live-ai-creative-partner',
    name: 'Live AI Creative Partner',
    version: '2',
    capabilities: ['director', 'asset', 'provider-neutral', 'local-ready', 'human-ai-cocreative'],
    director(payload) { return call('director', payload); },
    asset(job) { return call('asset', job); },
    metadata: {
      transport: 'local-http',
      storesApiKeys: false,
      role: 'The human and AI are the Dream/Director creative pair. This plugin is the AI participant, not a separate software brain.'
    }
  });

  host.use('live-ai-creative-partner');

  A.assistantBridge = {
    id: 'live-ai-creative-partner',
    health,
    get backend() { return clone(lastBackend); }
  };

  health();
})();
