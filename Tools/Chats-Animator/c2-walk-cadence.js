(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C2 cadence requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Walk cadence — clock pose run</strong><br>
    Convert project FPS into even pose holds. Example: 24 FPS at 6 pose beats/sec = 4-frame holds.
    <div class="control"><label><span>Pose frames</span><span id="cadence-count-value">7</span></label><input id="cadence-count" type="range" min="2" max="48" step="1" value="7"></div>
    <div class="control"><label><span>Pose beats / sec</span><span id="cadence-beats-value">6</span></label><input id="cadence-beats" type="range" min="1" max="12" step="1" value="6"></div>
    <div class="control"><label><span>Turnaround extra</span><span id="cadence-turn-value">3x</span></label><input id="cadence-turn-extra" type="range" min="1" max="6" step="1" value="3"></div>
    <label style="display:block;margin:8px 0"><input id="cadence-turn-last" type="checkbox" checked> Give last frame the turnaround hold</label>
    <button id="apply-cadence" type="button">Apply Walk Cadence</button>
    <div id="cadence-meta" style="margin-top:8px">Ready</div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  for (const [inputId, valueId, suffix] of [
    ['cadence-count','cadence-count-value',''],
    ['cadence-beats','cadence-beats-value',''],
    ['cadence-turn-extra','cadence-turn-value','x']
  ]) {
    $(inputId)?.addEventListener('input', (event) => {
      if ($(valueId)) $(valueId).textContent = `${event.target.value}${suffix}`;
      renderMeta();
    });
  }
  $('fps-control')?.addEventListener('input', renderMeta);

  function settings() {
    const fps = Math.max(1, Number(A.playback?.fps || $('fps-control')?.value || 24));
    const beats = Math.max(1, Number($('cadence-beats')?.value || 6));
    const count = Math.max(2, Number($('cadence-count')?.value || 7));
    const hold = Math.max(1, Math.round(fps / beats));
    const turnExtra = Math.max(1, Number($('cadence-turn-extra')?.value || 3));
    return { fps, beats, count, hold, turnExtra, turnLast: Boolean($('cadence-turn-last')?.checked) };
  }

  function renderMeta() {
    const s = settings();
    if ($('cadence-meta')) $('cadence-meta').textContent = `${s.fps} FPS ÷ ${s.beats} beats/sec = ${s.hold}-frame pose hold`;
  }

  function applyCadence() {
    R.captureCurrent();
    const s = settings();
    const start = R.activeIndex;
    const end = Math.min(R.frames.length, start + s.count);
    const frames = R.frames.slice(start, end);
    if (frames.length < 2) return A.status('Need at least two frames for cadence');
    frames.forEach((frame) => { frame.hold = s.hold; });
    if (s.turnLast) frames[frames.length - 1].hold = s.hold * s.turnExtra;
    R.restore(start);
    A.status(`Cadence applied: ${frames.length} poses at ${s.hold}x${s.turnLast ? `, turnaround ${s.hold * s.turnExtra}x` : ''}`);
    renderMeta();
  }

  $('apply-cadence')?.addEventListener('click', applyCadence);
  A.walkCadence = { settings, applyCadence, renderMeta };
  renderMeta();
})();
