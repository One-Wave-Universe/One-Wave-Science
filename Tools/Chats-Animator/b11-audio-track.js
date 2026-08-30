(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R || !A.playback) throw new Error('B11 requires Animator + reel + playback');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  let track = null;
  let playbackWasRunning = false;

  const panel = document.createElement('details');
  panel.className = 'card audio-dropdown';
  panel.innerHTML = `
    <summary style="cursor:pointer;font-weight:800">Audio</summary>
    <div style="margin-top:10px">
      <div style="color:#aeb4c0;margin-bottom:8px">Music / dialogue track. Hidden until you need it.</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button id="load-audio" type="button">Load Audio</button>
        <button id="remove-audio" type="button">Remove Audio</button>
        <input id="audio-picker" type="file" accept="audio/*" hidden>
      </div>
      <audio id="project-audio" controls preload="metadata" style="width:100%;margin-top:10px"></audio>
      <div id="audio-meta" style="margin-top:8px">No audio loaded</div>
      <div id="timeline-meta" style="margin-top:4px"></div>
    </div>
  `;
  aside.appendChild(panel);

  const audio = $('project-audio');

  function reelDurationSeconds() {
    const fps = Math.max(1, A.playback?.fps || Number($('fps-control')?.value || 24));
    return R.frames.reduce((sum, frame) => sum + Math.max(1, Number(frame.hold) || 1), 0) / fps;
  }

  function renderMeta() {
    if ($('audio-meta')) {
      const audioLength = Number.isFinite(audio?.duration) ? ` — ${audio.duration.toFixed(2)}s` : '';
      $('audio-meta').textContent = track ? `${track.name}${audioLength}` : 'No audio loaded';
    }
    if ($('timeline-meta')) $('timeline-meta').textContent = `Reel: ${reelDurationSeconds().toFixed(2)}s`;
  }

  function loadTrack(nextTrack) {
    track = nextTrack ? A.clone(nextTrack) : null;
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
      if (track?.src) {
        audio.src = track.src;
        panel.open = true;
      } else {
        audio.removeAttribute('src');
        audio.load();
      }
    }
    renderMeta();
  }

  async function loadFile(file) {
    const src = await A.readFile(file);
    loadTrack({ name: file.name, type: file.type || 'audio', src });
    A.status(`Audio loaded: ${file.name}`);
  }

  $('load-audio')?.addEventListener('click', () => $('audio-picker')?.click());
  $('audio-picker')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    try {
      if (file) await loadFile(file);
    } catch (error) {
      console.error(error);
      A.status('Audio load failed');
    } finally {
      event.target.value = '';
    }
  });
  $('remove-audio')?.addEventListener('click', () => {
    loadTrack(null);
    panel.open = false;
    A.status('Audio removed');
  });

  audio?.addEventListener('loadedmetadata', renderMeta);
  $('fps-control')?.addEventListener('input', renderMeta);
  $('frame-hold')?.addEventListener('input', renderMeta);

  $('play-button')?.addEventListener('click', () => {
    if (!track?.src || !audio) return;
    if (A.playback.playing) {
      audio.currentTime = 0;
      audio.play().catch(() => A.status('Animation playing; audio needs browser play permission'));
    } else {
      audio.pause();
    }
  });

  setInterval(() => {
    const nowPlaying = Boolean(A.playback?.playing);
    if (playbackWasRunning && !nowPlaying && audio && !audio.paused) audio.pause();
    playbackWasRunning = nowPlaying;
  }, 50);

  A.audio = {
    element: audio,
    panel,
    get track() { return track ? A.clone(track) : null; },
    loadTrack,
    loadFile,
    remove() { loadTrack(null); panel.open = false; },
    reelDurationSeconds,
    renderMeta
  };
  renderMeta();
})();