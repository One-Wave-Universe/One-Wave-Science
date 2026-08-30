(() => {
  'use strict';
  const A = window.Animator;
  const workspace = document.querySelector('.workspace');
  if (!A || !workspace) return;

  const panel = document.createElement('section');
  panel.id = 'director-dialogue';
  panel.innerHTML = `
    <div class="director-head">
      <strong>Director dialogue</strong>
      <span id="director-state">Local worker ready</span>
    </div>
    <div id="director-log" aria-live="polite"></div>
    <div class="director-entry">
      <textarea id="director-input" rows="3" placeholder="Try: add prop, load background, save frames 1 to 8 as Walk, create background: alley at night…"></textarea>
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

  function click(id) {
    const el = document.getElementById(id);
    if (!el) return false;
    el.click();
    return true;
  }

  function setInput(id, value) {
    const el = document.getElementById(id);
    if (!el) return false;
    el.value = String(value);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  }

  function setRange(id, value) {
    const el = document.getElementById(id);
    if (!el) return false;
    const min = Number(el.min || value);
    const max = Number(el.max || value);
    el.value = String(Math.max(min, Math.min(max, value)));
    el.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  }

  function acceptAsset(asset) {
    if (!asset?.src) throw new Error('Worker returned an asset without image data');
    const kind = String(asset.kind || 'prop').toLowerCase();
    if (kind === 'background') {
      return A.setBackgroundFromSource(asset.src, asset.name || 'Generated Background.png');
    }
    return A.addAssetFromSource(
      asset.src,
      kind === 'character' ? 'character' : 'prop',
      asset.name || (kind === 'character' ? 'Generated Character.png' : 'Generated Prop.png'),
      asset.placement || {}
    );
  }

  async function requestAsset(kind, prompt, item) {
    const job = {
      type: 'create-asset',
      kind,
      prompt,
      frame: item.frame,
      project: A.snapshot(),
      requestedAt: item.time
    };

    if (typeof window.oneWaveAssetWorker === 'function') {
      state.textContent = 'Creating asset…';
      const result = await window.oneWaveAssetWorker(job);
      const assets = Array.isArray(result?.assets) ? result.assets : (result?.asset ? [result.asset] : []);
      if (!assets.length) throw new Error('Asset worker returned no PNG');
      assets.forEach(acceptAsset);
      return result?.message || `${assets.length} ${kind} asset${assets.length === 1 ? '' : 's'} added.`;
    }

    window.dispatchEvent(new CustomEvent('onewave-asset-request', { detail: job }));
    return `Asset request ready for the external worker: ${kind} — ${prompt}`;
  }

  function captureMotion(start, end, name, tag = '') {
    if (!document.getElementById('c14-capture')) return null;
    setInput('c14-start', start);
    setInput('c14-end', end);
    setInput('c14-seq-name', name);
    if (tag) setInput('c14-tag', tag);
    click('c14-capture');
    return `Saved frames ${start}-${end} to the Motion Library as “${name}”.`;
  }

  function runLocal(text) {
    const t = text.trim().toLowerCase();
    let m;

    if (/^(play|play it|preview)$/.test(t)) {
      A.playback?.play?.();
      return 'Playing the reel.';
    }
    if (/^(stop|stop playback|stop it)$/.test(t)) {
      A.playback?.stop?.();
      return 'Playback stopped.';
    }
    if (/^(duplicate|duplicate frame|copy frame)$/.test(t)) {
      return click('duplicate-frame') ? 'Duplicated the current frame.' : null;
    }
    if (/^(add frame|new frame|add a frame)$/.test(t)) {
      return click('add-frame') ? 'Added a new frame.' : null;
    }
    if (/^(delete frame|remove frame|delete this frame)$/.test(t)) {
      return click('delete-frame') ? 'Deleted the current frame.' : null;
    }
    if (/^(load|add|choose) background(?: png)?$/.test(t)) {
      return click('background-picker') ? 'Choose the background PNG.' : null;
    }
    if (/^(add|load|choose) prop(?: png)?$/.test(t)) {
      return click('prop-picker') ? 'Choose the prop PNG.' : null;
    }
    if (/^(add|load|choose) character(?: png)?$/.test(t)) {
      return click('character-picker') ? 'Choose the character PNG.' : null;
    }
    if ((m = t.match(/(?:save|capture)\s+frames?\s+(\d+)\s+(?:to|through|-)\s*(\d+)\s+(?:as|to)\s+(.+)/))) {
      const start = Number(m[1]);
      const end = Number(m[2]);
      const name = text.trim().match(/(?:as|to)\s+(.+)$/i)?.[1]?.trim() || 'Motion';
      return captureMotion(start, end, name);
    }
    if ((m = t.match(/(?:go to|show|select)?\s*frame\s*(\d+)/))) {
      const n = Number(m[1]);
      if (!A.reel?.frames?.length || n < 1 || n > A.reel.frames.length) {
        return `Frame ${n} does not exist. Reel has ${A.reel?.frames?.length || 0} frame(s).`;
      }
      A.reel.restore(n - 1);
      return `Selected frame ${n}.`;
    }
    if ((m = t.match(/(?:hold|set hold(?: to)?)\s*(\d+)/))) {
      const n = Number(m[1]);
      return setRange('frame-hold', n) ? `Set this frame hold to ${Math.max(1, Math.min(12, n))}x.` : null;
    }
    if ((m = t.match(/(?:fps|set fps(?: to)?)\s*(\d+)/))) {
      const n = Number(m[1]);
      return setRange('fps-control', n) ? `Set playback to ${Math.max(1, Math.min(60, n))} FPS.` : null;
    }
    if (/make (?:this|it) faster/.test(t)) {
      const hold = document.getElementById('frame-hold');
      const next = Math.max(1, Number(hold?.value || 2) - 1);
      return setRange('frame-hold', next) ? `Made this frame faster: ${next}x hold.` : null;
    }
    if (/make (?:this|it) slower/.test(t)) {
      const hold = document.getElementById('frame-hold');
      const next = Math.min(12, Number(hold?.value || 2) + 1);
      return setRange('frame-hold', next) ? `Made this frame slower: ${next}x hold.` : null;
    }
    return null;
  }

  function parseAssetRequest(text) {
    const match = text.match(/^\s*(?:create|make|generate)\s+(?:a\s+|an\s+)?(background|prop|character|motion(?:\s+pose)?)\s*(?::|-)?\s*(.+)$/i);
    if (!match) return null;
    const rawKind = match[1].toLowerCase();
    const kind = rawKind.startsWith('motion') ? 'character' : rawKind;
    return { kind, prompt: match[2].trim(), motionPose: rawKind.startsWith('motion') };
  }

  async function submit() {
    const text = input.value.trim();
    if (!text) return;
    const item = { text, frame: (A.reel?.activeIndex ?? 0) + 1, time: new Date().toISOString() };
    history.push(item);
    addMessage('You', text);
    input.value = '';
    send.disabled = true;
    state.textContent = 'Working…';

    try {
      const assetRequest = parseAssetRequest(text);
      if (assetRequest) {
        const message = await requestAsset(assetRequest.kind, assetRequest.prompt, item);
        addMessage('Worker', message);
        A.status(message);
        state.textContent = typeof window.oneWaveAssetWorker === 'function' ? 'Asset worker connected' : 'Needs asset worker';
        return;
      }

      if (typeof window.oneWaveDirectorWorker === 'function') {
        const result = await window.oneWaveDirectorWorker({ request: item, animator: A });
        const assets = Array.isArray(result?.assets) ? result.assets : (result?.asset ? [result.asset] : []);
        assets.forEach(acceptAsset);
        if (result?.message) addMessage('Worker', result.message);
        state.textContent = 'External worker connected';
        return;
      }

      const result = runLocal(text);
      if (result) {
        addMessage('Worker', result);
        A.status(result);
        state.textContent = 'Local worker ready';
      } else {
        window.dispatchEvent(new CustomEvent('onewave-director-request', { detail: item }));
        addMessage('Worker', 'I do not know that edit yet. The request was exposed to the external-worker bridge.');
        state.textContent = 'Needs brain / bridge';
      }
    } catch (error) {
      console.error(error);
      addMessage('Worker', `Edit failed: ${error.message || error}`);
      state.textContent = 'Worker error';
    } finally {
      send.disabled = false;
      input.focus();
    }
  }

  send.addEventListener('click', submit);
  input.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') submit();
  });

  A.assetWorker = {
    acceptAsset,
    requestAsset,
    complete(assetOrAssets) {
      const assets = Array.isArray(assetOrAssets) ? assetOrAssets : [assetOrAssets];
      return assets.map(acceptAsset);
    }
  };
  A.directorDialogue = { history, submit, runLocal, captureMotion };
  addMessage('Worker', 'Ready. I can control the reel, load/place scene assets, capture motion-library ranges, and accept generated PNGs from the asset-worker bridge.');
})();
