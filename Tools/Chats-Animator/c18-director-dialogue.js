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
      <textarea id="director-input" rows="3" placeholder="Try: duplicate frame, add frame, go to frame 3, hold 4, fps 12, play, stop…"></textarea>
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

  function setRange(id, value) {
    const el = document.getElementById(id);
    if (!el) return false;
    const min = Number(el.min || value);
    const max = Number(el.max || value);
    el.value = String(Math.max(min, Math.min(max, value)));
    el.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
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
      // Provider-neutral hook: a future local brain or remote agent can replace
      // the tiny built-in worker without changing the animator data model.
      if (typeof window.oneWaveDirectorWorker === 'function') {
        const result = await window.oneWaveDirectorWorker({ request: item, animator: A });
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

  A.directorDialogue = { history, submit, runLocal };
  addMessage('Worker', 'Ready. I can control the reel now; the learning-brain bridge plugs into this same box later.');
})();
