(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C1 path motion requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Path motion — fit existing pose run</strong><br>
    Select the character/prop, set how many consecutive reel frames belong to this motion, then lay those stills onto a smooth path. Feet/base depth drives automatic perspective size.
    <div class="control"><label><span>Pose frames</span><span id="path-count-value">7</span></label><input id="path-count" type="range" min="2" max="48" step="1" value="7"></div>
    <div class="control"><label><span>Start X</span><span id="path-start-x-value">0.50</span></label><input id="path-start-x" type="range" min="0" max="1" step="0.01" value="0.50"></div>
    <div class="control"><label><span>End X</span><span id="path-end-x-value">0.50</span></label><input id="path-end-x" type="range" min="0" max="1" step="0.01" value="0.50"></div>
    <div class="control"><label><span>Start feet depth</span><span id="path-start-y-value">0.90</span></label><input id="path-start-y" type="range" min="0.10" max="0.98" step="0.01" value="0.90"></div>
    <div class="control"><label><span>End feet depth</span><span id="path-end-y-value">0.50</span></label><input id="path-end-y" type="range" min="0.10" max="0.98" step="0.01" value="0.50"></div>
    <label style="display:block;margin:8px 0"><input id="path-ease" type="checkbox" checked> Ease depth at near/far ends</label>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button id="fit-path-forward" type="button">Fit Run To Path</button>
      <button id="fit-path-reverse" type="button">Reverse Path</button>
    </div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  const bindings = [
    ['path-count','path-count-value',0],
    ['path-start-x','path-start-x-value',2],
    ['path-end-x','path-end-x-value',2],
    ['path-start-y','path-start-y-value',2],
    ['path-end-y','path-end-y-value',2]
  ];
  for (const [inputId, valueId, digits] of bindings) {
    $(inputId)?.addEventListener('input', (event) => {
      if ($(valueId)) $(valueId).textContent = Number(event.target.value).toFixed(digits);
    });
  }

  function smoothstep(t) {
    return t * t * (3 - 2 * t);
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function selectedAsset() {
    return A.state.assets.find((asset) => asset.id === A.state.selectedAssetId) || null;
  }

  function readSettings(reverse = false) {
    const count = Math.max(2, Number($('path-count')?.value || 7));
    let startX = Number($('path-start-x')?.value || 0.5);
    let endX = Number($('path-end-x')?.value || 0.5);
    let startY = Number($('path-start-y')?.value || 0.9);
    let endY = Number($('path-end-y')?.value || 0.5);
    if (reverse) {
      [startX, endX] = [endX, startX];
      [startY, endY] = [endY, startY];
    }
    return { count, startX, endX, startY, endY, eased: Boolean($('path-ease')?.checked) };
  }

  function fitRun(reverse = false) {
    const selected = selectedAsset();
    if (!selected) return A.status('Select a character or prop first');
    R.captureCurrent();
    const settings = readSettings(reverse);
    const startIndex = R.activeIndex;
    const endIndex = Math.min(R.frames.length, startIndex + settings.count);
    const frames = R.frames.slice(startIndex, endIndex);
    if (frames.length < 2) return A.status('Need at least two reel frames in the pose run');

    let changed = 0;
    frames.forEach((frame, localIndex) => {
      const asset = frame.snapshot.assets.find((item) => item.id === selected.id);
      if (!asset) return;
      const rawT = frames.length === 1 ? 0 : localIndex / (frames.length - 1);
      const t = settings.eased ? smoothstep(rawT) : rawT;
      asset.x = lerp(settings.startX, settings.endX, t);
      asset.groundY = lerp(settings.startY, settings.endY, t);
      changed += 1;
    });

    if (!changed) return A.status('Selected asset is not present in this pose run');
    R.restore(startIndex);
    A.status(`Path fitted across ${changed} pose frames — perspective size follows feet depth`);
  }

  $('fit-path-forward')?.addEventListener('click', () => fitRun(false));
  $('fit-path-reverse')?.addEventListener('click', () => fitRun(true));

  A.pathMotion = { fitRun, readSettings, smoothstep, lerp };
})();
