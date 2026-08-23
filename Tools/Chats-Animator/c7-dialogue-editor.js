(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.voiceLab) throw new Error('C7 requires C6 Voice Lab');
  const aside = document.querySelector('aside');
  const $ = (id) => document.getElementById(id);
  if (!aside) return;

  const state = {
    duckDb: 9,
    attackMs: 80,
    releaseMs: 300
  };

  function ensureClip(clip) {
    if (!Number.isFinite(Number(clip.trimStart))) clip.trimStart = 0;
    if (!Number.isFinite(Number(clip.trimEnd))) clip.trimEnd = 0;
    if (!Number.isFinite(Number(clip.fadeIn))) clip.fadeIn = 0.02;
    if (!Number.isFinite(Number(clip.fadeOut))) clip.fadeOut = 0.04;
    if (!Number.isFinite(Number(clip.gainDb))) clip.gainDb = 0;
    return clip;
  }

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C7 Dialogue Editor</strong><br>
    Non-destructive speech finishing after Voice Lab: trim, fades, clip gain, and music duck settings stay editable with the project.
    <div class="control"><label><span>Music duck</span><span id="c7-duck-v">9 dB</span></label><input id="c7-duck" type="range" min="0" max="24" step="1" value="9"></div>
    <div class="control"><label><span>Duck attack</span><span id="c7-attack-v">80 ms</span></label><input id="c7-attack" type="range" min="10" max="500" step="10" value="80"></div>
    <div class="control"><label><span>Duck release</span><span id="c7-release-v">300 ms</span></label><input id="c7-release" type="range" min="50" max="1500" step="50" value="300"></div>
    <button id="c7-refresh" type="button">Refresh Dialogue Clips</button>
    <div id="c7-clips" style="margin-top:8px"></div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function bindRange(id, out, key, suffix) {
    $(id)?.addEventListener('input', (e) => {
      state[key] = Number(e.target.value);
      if ($(out)) $(out).textContent = `${e.target.value}${suffix}`;
    });
  }
  bindRange('c7-duck', 'c7-duck-v', 'duckDb', ' dB');
  bindRange('c7-attack', 'c7-attack-v', 'attackMs', ' ms');
  bindRange('c7-release', 'c7-release-v', 'releaseMs', ' ms');

  function render() {
    const box = $('c7-clips');
    box.innerHTML = '';
    const clips = A.voiceLab.state.clips || [];
    if (!clips.length) {
      box.textContent = 'No dialogue clips yet.';
      return;
    }
    clips.slice().sort((a,b) => Number(a.start) - Number(b.start)).forEach((clip) => {
      ensureClip(clip);
      const row = document.createElement('div');
      row.className = 'card';
      row.innerHTML = `
        <strong>${clip.name}</strong><br>
        <label>Start <input data-k="start" type="number" min="0" step="0.01" value="${clip.start}" style="width:72px"> s</label><br>
        <label>Trim in <input data-k="trimStart" type="number" min="0" step="0.01" value="${clip.trimStart}" style="width:72px"> s</label><br>
        <label>Trim out <input data-k="trimEnd" type="number" min="0" step="0.01" value="${clip.trimEnd}" style="width:72px"> s</label><br>
        <label>Fade in <input data-k="fadeIn" type="number" min="0" step="0.01" value="${clip.fadeIn}" style="width:72px"> s</label><br>
        <label>Fade out <input data-k="fadeOut" type="number" min="0" step="0.01" value="${clip.fadeOut}" style="width:72px"> s</label><br>
        <label>Clip gain <input data-k="gainDb" type="number" min="-36" max="18" step="1" value="${clip.gainDb}" style="width:72px"> dB</label>
      `;
      row.querySelectorAll('input[data-k]').forEach((input) => {
        input.addEventListener('change', (e) => {
          const key = e.target.dataset.k;
          let value = Number(e.target.value) || 0;
          if (['start','trimStart','trimEnd','fadeIn','fadeOut'].includes(key)) value = Math.max(0, value);
          if (key === 'gainDb') value = Math.max(-36, Math.min(18, value));
          clip[key] = value;
          A.status(`Dialogue ${key} updated`);
        });
      });
      box.appendChild(row);
    });
  }

  $('c7-refresh')?.addEventListener('click', render);

  function serialize() {
    return { ...state };
  }

  function loadState(next) {
    if (!next) return;
    if (Number.isFinite(Number(next.duckDb))) state.duckDb = Number(next.duckDb);
    if (Number.isFinite(Number(next.attackMs))) state.attackMs = Number(next.attackMs);
    if (Number.isFinite(Number(next.releaseMs))) state.releaseMs = Number(next.releaseMs);
    if ($('c7-duck')) $('c7-duck').value = String(state.duckDb);
    if ($('c7-attack')) $('c7-attack').value = String(state.attackMs);
    if ($('c7-release')) $('c7-release').value = String(state.releaseMs);
    if ($('c7-duck-v')) $('c7-duck-v').textContent = `${state.duckDb} dB`;
    if ($('c7-attack-v')) $('c7-attack-v').textContent = `${state.attackMs} ms`;
    if ($('c7-release-v')) $('c7-release-v').textContent = `${state.releaseMs} ms`;
    render();
  }

  A.dialogueEditor = { state, ensureClip, render, serialize, loadState };
  render();
})();
