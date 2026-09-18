(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B7 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  let playing = false;
  let timer = null;
  let playIndex = 0;
  let fps = Number($('fps-control')?.value || 24);

  function stop() {
    playing = false;
    clearTimeout(timer);
    timer = null;
    if ($('play-button')) $('play-button').textContent = 'Play';
    A.state.calibrationVisible = false;
    A.state.placementMode = false;
    A.renderAll();
    if (R.frames.length) R.preview(Math.max(0, Math.min(playIndex - 1, R.frames.length - 1)));
    A.status('Playback stopped — reel unchanged');
  }
  function step() {
    if (!playing || !R.frames.length) return;
    if (playIndex >= R.frames.length) {
      stop();
      return;
    }
    const f = R.frames[playIndex];
    R.preview(playIndex);
    document.getElementById('calibration-overlay')?.setAttribute('hidden', '');
    const delay = Math.max(1, f.hold) * (1000 / fps);
    playIndex += 1;
    timer = setTimeout(step, delay);
  }
  function play() {
    if (playing) return stop();
    R.captureCurrent();
    playing = true;
    playIndex = 0;
    if ($('play-button')) $('play-button').textContent = 'Stop';
    A.status('Playing');
    step();
  }
  $('play-button')?.addEventListener('click', play);
  $('fps-control')?.addEventListener('input', (event) => {
    fps = Number(event.target.value);
    if ($('fps-value')) $('fps-value').textContent = String(fps);
  });
  if ($('fps-value')) $('fps-value').textContent = String(fps);
  A.playback = { play, stop, get playing() { return playing; }, get fps() { return fps; } };
})();
