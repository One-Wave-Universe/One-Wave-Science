(() => {
  'use strict';
  const A = window.Animator;
  const workspace = document.querySelector('.workspace');
  if (!A?.architecture?.M4 || !workspace) return;

  const panel = document.createElement('section');
  panel.id = 'director-dialogue';
  panel.innerHTML = `
    <div class="director-head">
      <strong>Director dialogue</strong>
      <span id="director-state">Five-scale architecture ready</span>
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
    if (missing.length) {
      addMessage('Dream', `${missing.length} creative gap${missing.length === 1 ? '' : 's'} still need human/AI judgment or a new asset.`);
    }
  }

  async function submit() {
    const text = input.value.trim();
    if (!text) return;
    const item = { text, frame: (A.reel?.activeIndex ?? 0) + 1, time: new Date().toISOString() };
    history.push(item);
    addMessage('You', text);
    input.value = '';
    send.disabled = true;
    state.textContent = 'M4 routing…';

    try {
      const result = await A.architecture.M4.route(text);
      const stage = result?.stage || 'M4';
      const message = result?.message || (result?.ok ? 'Done.' : 'Could not route request.');
      addMessage(stage, message);
      showAutomaticWork(result);
      A.status(message);

      if (result?.pending) state.textContent = `${stage} waiting for assistant`;
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

  A.directorDialogue = { history, submit };
  addMessage('M4', 'Ready. Routine Dream prep and Administrator checks run automatically; human and AI handle the creative choices that remain.');
})();
