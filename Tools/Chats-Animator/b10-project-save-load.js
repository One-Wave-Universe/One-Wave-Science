(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B10 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const FORMAT = 'one-wave-video-maker';
  const VERSION = 1;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Project save / load</strong><br>
    Save the complete reel, embedded artwork, calibration, placement, holds, FPS, and audio to one project file.
    <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
      <button id="save-project" type="button">Save Project</button>
      <button id="load-project" type="button">Open Project</button>
      <input id="project-picker" type="file" accept=".owav,.json,application/json" hidden>
    </div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function buildProject() {
    R.captureCurrent();
    return {
      format: FORMAT,
      version: VERSION,
      savedAt: new Date().toISOString(),
      fps: A.playback?.fps || Number($('fps-control')?.value || 24),
      activeIndex: R.activeIndex,
      frames: A.clone(R.frames),
      audioTrack: A.audio?.track || null
    };
  }

  function validateProject(data) {
    if (!data || data.format !== FORMAT || data.version !== VERSION) throw new Error('Unsupported project format');
    if (!Array.isArray(data.frames) || !data.frames.length) throw new Error('Project has no frames');
    for (const frame of data.frames) {
      if (!frame || !frame.snapshot || !Array.isArray(frame.snapshot.assets)) throw new Error('Malformed frame data');
      if (!Number.isFinite(Number(frame.hold)) || Number(frame.hold) < 1) throw new Error('Invalid frame hold');
    }
    if (data.audioTrack !== undefined && data.audioTrack !== null && (!data.audioTrack.name || !data.audioTrack.src)) throw new Error('Malformed audio track');
    return data;
  }

  function saveProject() {
    const project = buildProject();
    const blob = new Blob([JSON.stringify(project, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `one-wave-project-${new Date().toISOString().replace(/[:.]/g, '-')}.owav`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
    A.status('Project saved');
  }

  function applyProject(data) {
    const project = validateProject(data);
    if (A.playback?.playing) A.playback.stop();
    const frames = A.clone(project.frames);
    const index = Math.max(0, Math.min(Number(project.activeIndex) || 0, frames.length - 1));
    R.setFrames(frames, index);
    const fps = Math.max(1, Math.min(60, Number(project.fps) || 24));
    if ($('fps-control')) {
      $('fps-control').value = String(fps);
      $('fps-control').dispatchEvent(new Event('input', { bubbles: true }));
    }
    if (A.audio?.loadTrack) A.audio.loadTrack(project.audioTrack || null);
    A.status(`Project loaded — ${frames.length} frame${frames.length === 1 ? '' : 's'}`);
  }

  $('save-project')?.addEventListener('click', saveProject);
  $('load-project')?.addEventListener('click', () => $('project-picker')?.click());
  $('project-picker')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      applyProject(data);
    } catch (error) {
      console.error(error);
      A.status(`Project load failed: ${error.message}`);
    } finally {
      event.target.value = '';
    }
  });

  A.projectIO = { buildProject, validateProject, applyProject, saveProject, format: FORMAT, version: VERSION };
})();
