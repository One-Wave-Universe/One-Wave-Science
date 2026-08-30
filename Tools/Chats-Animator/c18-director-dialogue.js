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
      <span id="director-state">Local suggestion box</span>
    </div>
    <div id="director-log" aria-live="polite"></div>
    <div class="director-entry">
      <textarea id="director-input" rows="3" placeholder="Describe the edit you want: move GR from here to here, change pose, add frames, make this section faster…"></textarea>
      <button id="director-send" type="button">Suggest Edit</button>
    </div>
  `;
  workspace.appendChild(panel);

  const log = panel.querySelector('#director-log');
  const input = panel.querySelector('#director-input');
  const send = panel.querySelector('#director-send');
  const history = [];

  function submit() {
    const text = input.value.trim();
    if (!text) return;
    const item = { text, frame: (A.reel?.activeIndex ?? 0) + 1, time: new Date().toISOString() };
    history.push(item);
    const row = document.createElement('div');
    row.className = 'director-message';
    row.textContent = `Frame ${item.frame}: ${text}`;
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
    input.value = '';
    window.dispatchEvent(new CustomEvent('onewave-director-suggestion', { detail: item }));
    A.status('Director suggestion added');
  }

  send.addEventListener('click', submit);
  input.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') submit();
  });

  A.directorDialogue = { history, submit };
})();
