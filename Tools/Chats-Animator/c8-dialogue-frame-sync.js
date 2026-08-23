(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A?.voiceLab || !R) throw new Error('C8 requires Voice Lab + reel');
  const aside = document.querySelector('aside');
  if (!aside) return;
  const $ = (id) => document.getElementById(id);

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C8 Speech ↔ Video Timing</strong><br>
    Snap speech to the animation clock instead of guessing seconds.
    <div class="control"><label><span>Target reel frame</span><span id="c8-frame-v">1</span></label><input id="c8-frame" type="range" min="1" max="1" step="1" value="1"></div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <button id="c8-set-line-start" type="button">Set Next Line To Frame</button>
      <button id="c8-snap-selected" type="button">Snap Nearest Speech Clip</button>
    </div>
    <div id="c8-meta" style="margin-top:8px"></div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function fps() {
    return Math.max(1, A.playback?.fps || Number($('fps-control')?.value || 24));
  }

  function frameStartSeconds(index) {
    const capped = Math.max(0, Math.min(index, R.frames.length - 1));
    let ticks = 0;
    for (let i = 0; i < capped; i += 1) ticks += Math.max(1, Number(R.frames[i].hold) || 1);
    return ticks / fps();
  }

  function syncRange() {
    const input = $('c8-frame');
    input.max = String(Math.max(1, R.frames.length));
    input.value = String(Math.min(Number(input.value) || 1, R.frames.length));
    updateMeta();
  }

  function updateMeta() {
    const frame = Math.max(1, Number($('c8-frame')?.value || 1));
    if ($('c8-frame-v')) $('c8-frame-v').textContent = String(frame);
    if ($('c8-meta')) $('c8-meta').textContent = `Frame ${frame} starts at ${frameStartSeconds(frame - 1).toFixed(3)}s @ ${fps()} FPS`;
  }

  $('c8-frame')?.addEventListener('input', updateMeta);
  $('fps-control')?.addEventListener('input', updateMeta);

  $('c8-set-line-start')?.addEventListener('click', () => {
    const frame = Math.max(1, Number($('c8-frame')?.value || 1));
    const time = frameStartSeconds(frame - 1);
    const input = $('voice-line-start');
    if (input) {
      input.value = time.toFixed(3);
      input.dispatchEvent(new Event('change', { bubbles: true }));
      A.status(`Next speech line snapped to frame ${frame}`);
    }
  });

  $('c8-snap-selected')?.addEventListener('click', () => {
    const frame = Math.max(1, Number($('c8-frame')?.value || 1));
    const target = frameStartSeconds(frame - 1);
    const clips = A.voiceLab.state.clips || [];
    if (!clips.length) return A.status('No speech clips to snap');
    let nearest = clips[0];
    for (const clip of clips) if (Math.abs(Number(clip.start) - target) < Math.abs(Number(nearest.start) - target)) nearest = clip;
    nearest.start = target;
    A.dialogueEditor?.render?.();
    A.status(`${nearest.name} snapped to frame ${frame}`);
  });

  const oldSetFrames = R.setFrames?.bind(R);
  if (oldSetFrames && !R._c8Wrapped) {
    R.setFrames = function(...args) {
      const result = oldSetFrames(...args);
      syncRange();
      return result;
    };
    R._c8Wrapped = true;
  }

  A.dialogueSync = { frameStartSeconds, syncRange };
  syncRange();
})();
