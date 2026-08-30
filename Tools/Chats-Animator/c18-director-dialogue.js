(() => {
  'use strict';
  const A = window.Animator;
  const workspace = document.querySelector('.workspace');
  if (!A?.architecture?.M4 || !workspace) return;

  function ensurePluginHost() {
    if (window.OneWaveAssistantPlugins) return window.OneWaveAssistantPlugins;

    const plugins = new Map();
    let activeId = '';
    const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));

    function validatePlugin(plugin) {
      if (!plugin || typeof plugin !== 'object') throw new Error('Assistant plugin must be an object');
      if (!String(plugin.id || '').trim()) throw new Error('Assistant plugin needs an id');
      if (typeof plugin.director !== 'function' && typeof plugin.asset !== 'function') throw new Error('Assistant plugin needs director() and/or asset()');
    }

    const host = {
      apiVersion: 'one-wave-assistant-plugin/v1',
      register(plugin) {
        validatePlugin(plugin);
        const id = String(plugin.id).trim();
        const normalized = {
          id,
          name: String(plugin.name || id),
          version: String(plugin.version || '1'),
          capabilities: Array.isArray(plugin.capabilities) ? [...plugin.capabilities] : [],
          director: typeof plugin.director === 'function' ? plugin.director : null,
          asset: typeof plugin.asset === 'function' ? plugin.asset : null,
          metadata: clone(plugin.metadata || {})
        };
        plugins.set(id, normalized);
        window.dispatchEvent(new CustomEvent('onewave-assistant-plugin-registered', { detail: host.describe(id) }));
        return host.describe(id);
      },
      unregister(id) {
        id = String(id || '');
        const removed = plugins.delete(id);
        if (activeId === id) activeId = '';
        return removed;
      },
      use(id) {
        id = String(id || '');
        if (!plugins.has(id)) throw new Error(`Assistant plugin not registered: ${id}`);
        activeId = id;
        const info = host.describe(id);
        window.dispatchEvent(new CustomEvent('onewave-assistant-plugin-active', { detail: info }));
        A.status(`Assistant plugin active: ${info.name}`);
        return info;
      },
      clear() {
        activeId = '';
        window.dispatchEvent(new CustomEvent('onewave-assistant-plugin-active', { detail: null }));
        A.status('Assistant plugin disconnected');
      },
      get activeId() { return activeId; },
      get active() { return activeId ? plugins.get(activeId) || null : null; },
      list() { return [...plugins.keys()].map((id) => host.describe(id)); },
      describe(id = activeId) {
        const plugin = plugins.get(String(id || ''));
        if (!plugin) return null;
        return { apiVersion: host.apiVersion, id: plugin.id, name: plugin.name, version: plugin.version, capabilities: [...plugin.capabilities], metadata: clone(plugin.metadata) };
      },
      async director(payload) {
        const plugin = host.active;
        if (!plugin?.director) return { pending: true, stage: 'Director', message: 'Director request ready — no assistant plugin is active.' };
        return plugin.director(payload);
      },
      async asset(job) {
        const plugin = host.active;
        if (!plugin?.asset) return { pending: true, stage: 'Dream', job: clone(job), message: 'Asset request ready — active plugin has no asset worker.' };
        return plugin.asset(clone(job));
      }
    };

    // Open event adapter: a desktop host, ChatGPT bridge, or future local AI can
    // consume these events and answer with the matching response id.
    host.register({
      id: 'event-bridge',
      name: 'Open Event Bridge',
      version: '1',
      capabilities: ['director', 'asset', 'provider-neutral', 'local-ready'],
      director(payload) {
        return new Promise((resolve) => {
          const id = `director-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
          const onResponse = (event) => {
            if (event.detail?.id !== id) return;
            window.removeEventListener('onewave-assistant-plugin-response', onResponse);
            resolve(event.detail.result);
          };
          window.addEventListener('onewave-assistant-plugin-response', onResponse);
          window.dispatchEvent(new CustomEvent('onewave-assistant-plugin-request', { detail: { id, kind: 'director', payload: clone(payload), apiVersion: host.apiVersion } }));
        });
      },
      asset(job) {
        return new Promise((resolve) => {
          const id = `asset-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
          const onResponse = (event) => {
            if (event.detail?.id !== id) return;
            window.removeEventListener('onewave-assistant-plugin-response', onResponse);
            resolve(event.detail.result);
          };
          window.addEventListener('onewave-assistant-plugin-response', onResponse);
          window.dispatchEvent(new CustomEvent('onewave-assistant-plugin-request', { detail: { id, kind: 'asset', payload: clone(job), apiVersion: host.apiVersion } }));
        });
      }
    });

    window.OneWaveAssistantPlugins = host;
    window.oneWaveDirectorWorker = (payload) => host.director(payload);
    window.oneWaveAssetWorker = (job) => host.asset(job);
    return host;
  }

  const pluginHost = ensurePluginHost();

  const panel = document.createElement('section');
  panel.id = 'director-dialogue';
  panel.innerHTML = `
    <div class="director-head">
      <strong>Director dialogue</strong>
      <span id="director-state">Open assistant plugin slot ready</span>
    </div>
    <div id="director-log" aria-live="polite"></div>
    <div class="director-entry">
      <textarea id="director-input" rows="3" placeholder="Describe the edit, asset, motion, or timing change you want…"></textarea>
      <button id="director-send" type="button">Do Edit</button>
    </div>
  `;
  workspace.appendChild(panel);

  const log = panel.querySelector('#director-log');
  const input = panel.querySelector('#director-input');
  const send = panel.querySelector('#director-send');
  const state = panel.querySelector('#director-state');
  const history = [];

  function addMessage(kind, text) {
    const row = document.createElement('div');
    row.className = 'director-message';
    row.textContent = `${kind}: ${text}`;
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
  }

  function showAutomaticWork(result) {
    const reused = result?.plan?.automatic?.reusedMotion || [];
    for (const item of reused) {
      const action = item?.need?.action || 'motion';
      const actor = item?.need?.actor ? ` for ${item.need.actor}` : '';
      const name = item?.name || `motion ${item?.index ?? ''}`;
      addMessage('Dream', `Reused ${name}${actor} for ${action}.`);
    }
    if (result?.audit?.ok) {
      const count = Array.isArray(result?.results) ? result.results.length : 0;
      addMessage('Administrator', `Checked ${count} executed step${count === 1 ? '' : 's'} — no executor failures reported.`);
    }
    const missing = Array.isArray(result?.missing) ? result.missing : [];
    if (missing.length) addMessage('Dream', `${missing.length} creative gap${missing.length === 1 ? '' : 's'} still need human/AI judgment or a new asset.`);
  }

  function pluginLabel() {
    const active = pluginHost.describe();
    return active ? active.name : 'no assistant plugin active';
  }

  async function submit() {
    const text = input.value.trim();
    if (!text) return;
    const item = { text, frame: (A.reel?.activeIndex ?? 0) + 1, time: new Date().toISOString() };
    history.push(item);
    addMessage('You', text);
    input.value = '';
    send.disabled = true;
    state.textContent = `M4 routing — ${pluginLabel()}`;

    try {
      const result = await A.architecture.M4.route(text);
      const stage = result?.stage || 'M4';
      const message = result?.message || (result?.ok ? 'Done.' : 'Could not route request.');
      addMessage(stage, message);
      showAutomaticWork(result);
      A.status(message);
      if (result?.pending) state.textContent = `${stage} waiting — ${pluginLabel()}`;
      else if (result?.ok && result?.missing?.length) state.textContent = 'Automatic work done — creative input needed';
      else if (result?.ok) state.textContent = 'Automatic checks passed';
      else state.textContent = `${stage} needs input`;
    } catch (error) {
      console.error(error);
      addMessage('Administrator', `Edit failed: ${error.message || error}`);
      state.textContent = 'Architecture error';
    } finally {
      send.disabled = false;
      input.focus();
    }
  }

  send.addEventListener('click', submit);
  input.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') submit();
  });

  window.addEventListener('onewave-assistant-plugin-active', () => {
    state.textContent = `Assistant slot: ${pluginLabel()}`;
    addMessage('M4', `Assistant plugin changed: ${pluginLabel()}.`);
  });

  A.assistantPlugins = pluginHost;
  A.directorDialogue = { history, submit, plugins: pluginHost };
  addMessage('M4', `Ready. Open plugin API ${pluginHost.apiVersion}; ${pluginHost.list().length} adapter registered. Dream/Admin automation stays inside the animator.`);
})();
