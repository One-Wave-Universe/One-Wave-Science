(() => {
  'use strict';

  const A = window.Animator;
  const host = window.OneWaveAssistantPlugins;
  const directorPanel = document.getElementById('director-dialogue');
  if (!A || !host || !directorPanel) throw new Error('C21 requires Animator + assistant plugin host + Director dialogue');

  const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));
  let pending = null;
  let lastPacket = null;

  const bridge = document.createElement('section');
  bridge.id = 'assistant-copy-paste-bridge';
  bridge.style.marginTop = '10px';
  bridge.innerHTML = `
    <div class="card">
      <strong>AI Assistant Bridge</strong><br>
      Provider-neutral handoff for ChatGPT, Claude, a local model, or another assistant.
      Send the packet to the assistant, then paste its JSON response below. The normal Administrator and control API still validate and execute the returned work.
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
        <button id="assistant-bridge-copy" type="button">Copy AI Request</button>
        <button id="assistant-bridge-cancel" type="button">Cancel Pending</button>
      </div>
      <textarea id="assistant-bridge-out" readonly style="width:100%;min-height:92px;margin-top:8px;background:#0c0e12;color:#f5f6f8;border:1px solid #414551;border-radius:8px;padding:8px" placeholder="Submit a Director request first; its AI packet will appear here."></textarea>
      <div style="margin-top:8px"><strong>AI response JSON</strong></div>
      <textarea id="assistant-bridge-in" style="width:100%;min-height:110px;margin-top:6px;background:#0c0e12;color:#f5f6f8;border:1px solid #414551;border-radius:8px;padding:8px" placeholder='Paste a plan such as {"steps":[{"operation":"set_fps","args":{"fps":24}}],"missing":[]}'></textarea>
      <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-top:8px">
        <button id="assistant-bridge-apply" type="button">Apply AI Response</button>
        <span id="assistant-bridge-state">Ready</span>
      </div>
    </div>
  `;
  directorPanel.appendChild(bridge);

  const out = document.getElementById('assistant-bridge-out');
  const input = document.getElementById('assistant-bridge-in');
  const state = document.getElementById('assistant-bridge-state');
  const copyButton = document.getElementById('assistant-bridge-copy');
  const applyButton = document.getElementById('assistant-bridge-apply');
  const cancelButton = document.getElementById('assistant-bridge-cancel');

  function setState(message) {
    state.textContent = message;
    A.status(message);
  }

  function makePacket(kind, payload) {
    return {
      apiVersion: 'one-wave-assistant-plugin/v1',
      bridge: 'copy-paste',
      kind,
      instruction: kind === 'director'
        ? 'Return JSON only. Prefer executable steps using only operations listed in payload.context.operations. Shape: {"steps":[{"operation":"...","args":{}}],"missing":[]}. Put unresolved creative needs in missing instead of inventing unsupported operations.'
        : 'Return JSON only. Shape: {"assets":[{"kind":"background|character|prop","name":"...","src":"data:image/...","placement":{}}]}. If you cannot supply an asset, return {"pending":true,"message":"..."}.',
      payload: clone(payload)
    };
  }

  function begin(kind, payload) {
    if (pending) {
      pending.reject(new Error('Assistant bridge request replaced by a newer request'));
      pending = null;
    }

    lastPacket = makePacket(kind, payload);
    out.value = JSON.stringify(lastPacket, null, 2);
    input.value = '';
    setState(`AI ${kind} request ready — copy packet, then paste response.`);

    return new Promise((resolve, reject) => {
      pending = { kind, resolve, reject };
    });
  }

  async function copyPacket() {
    if (!lastPacket) return setState('No AI request packet yet. Submit a Director request first.');
    const text = JSON.stringify(lastPacket, null, 2);
    try {
      await navigator.clipboard.writeText(text);
      setState('AI request copied.');
    } catch (_error) {
      out.focus();
      out.select();
      document.execCommand?.('copy');
      setState('AI request selected/copied where supported.');
    }
  }

  function normalizeResponse(parsed, kind) {
    if (parsed && typeof parsed === 'object' && parsed.result && typeof parsed.result === 'object') parsed = parsed.result;
    if (kind === 'director' && parsed && typeof parsed === 'object' && parsed.plan && typeof parsed.plan === 'object') parsed = parsed.plan;
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('AI response must be a JSON object');
    if (kind === 'director') {
      if (!Array.isArray(parsed.steps)) parsed.steps = [];
      if (!Array.isArray(parsed.missing)) parsed.missing = [];
    }
    return parsed;
  }

  function applyResponse() {
    if (!pending) return setState('No AI request is waiting for a response.');
    try {
      const parsed = normalizeResponse(JSON.parse(input.value), pending.kind);
      const current = pending;
      pending = null;
      current.resolve(parsed);
      setState(`AI ${current.kind} response accepted for normal validation/execution.`);
    } catch (error) {
      setState(`AI response rejected: ${error.message || error}`);
    }
  }

  function cancelPending() {
    if (!pending) return setState('No pending AI request.');
    const current = pending;
    pending = null;
    current.resolve({ pending: true, stage: current.kind === 'director' ? 'Director' : 'Dream', message: 'Assistant request cancelled.' });
    setState('Pending AI request cancelled.');
  }

  host.register({
    id: 'copy-paste-bridge',
    name: 'Universal Copy/Paste AI Bridge',
    version: '1',
    capabilities: ['director', 'asset', 'provider-neutral', 'chatgpt-ready', 'claude-ready', 'local-ready'],
    director(payload) { return begin('director', payload); },
    asset(job) { return begin('asset', job); },
    metadata: {
      transport: 'human-mediated-json',
      storesApiKeys: false,
      note: 'Uses the same validated animator control path for every assistant provider.'
    }
  });

  host.use('copy-paste-bridge');
  copyButton.addEventListener('click', copyPacket);
  applyButton.addEventListener('click', applyResponse);
  cancelButton.addEventListener('click', cancelPending);

  A.assistantBridge = {
    id: 'copy-paste-bridge',
    get pending() { return pending ? pending.kind : null; },
    get lastPacket() { return clone(lastPacket); },
    copyPacket,
    applyResponse,
    cancelPending
  };

  setState('Universal AI bridge active. Director requests can now be handed to ChatGPT, Claude, or another assistant.');
})();
