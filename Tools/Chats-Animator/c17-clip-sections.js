(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C17 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Clip / section export</strong><br>
    Mark a reel range, preview it in the editor, then export only that section as a WebM clip for a separate video editor.
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
      <button id="c17-mark-start" type="button">Start = Current</button>
      <button id="c17-mark-end" type="button">End = Current</button>
    </div>
    <div class="control"><label><span>Start frame</span><span id="c17-start-value">1</span></label><input id="c17-start" type="range" min="1" max="1" step="1" value="1"></div>
    <div class="control"><label><span>End frame</span><span id="c17-end-value">1</span></label><input id="c17-end" type="range" min="1" max="1" step="1" value="1"></div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <button id="c17-preview" type="button">Preview Section</button>
      <button id="c17-export" type="button">Export Section WebM</button>
    </div>
    <div id="c17-meta" style="margin-top:8px">Frames 1–1</div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));

  function fps() {
    return Math.max(1, Number(A.playback?.fps || $('fps-control')?.value || 24));
  }

  function syncLimits() {
    const n = Math.max(1, R.frames.length);
    for (const id of ['c17-start', 'c17-end']) {
      const el = $(id);
      if (!el) continue;
      el.max = String(n);
      el.value = String(clamp(Number(el.value || 1), 1, n));
    }
    normalizeRange();
  }

  function normalizeRange(changed) {
    const n = Math.max(1, R.frames.length);
    let start = clamp(Number($('c17-start')?.value || 1), 1, n);
    let end = clamp(Number($('c17-end')?.value || n), 1, n);
    if (start > end) {
      if (changed === 'start') end = start;
      else start = end;
    }
    if ($('c17-start')) $('c17-start').value = String(start);
    if ($('c17-end')) $('c17-end').value = String(end);
    if ($('c17-start-value')) $('c17-start-value').textContent = String(start);
    if ($('c17-end-value')) $('c17-end-value').textContent = String(end);
    const ticks = R.frames.slice(start - 1, end).reduce((sum, frame) => sum + Math.max(1, Number(frame.hold) || 1), 0);
    const seconds = ticks / fps();
    if ($('c17-meta')) $('c17-meta').textContent = `Frames ${start}–${end} • ${ticks} timeline ticks • ${seconds.toFixed(2)} sec @ ${fps()} fps`;
    return { start, end };
  }

  async function previewSection() {
    R.captureCurrent();
    const original = R.activeIndex;
    const { start, end } = normalizeRange();
    try {
      for (let i = start - 1; i < end; i += 1) {
        R.restore(i);
        const hold = Math.max(1, Number(R.frames[i].hold) || 1);
        await sleep(hold * 1000 / fps());
      }
    } finally {
      R.restore(original);
    }
  }

  async function exportSection() {
    if (!window.MediaRecorder || !A.videoExport?.canvas || !A.videoExport?.drawSnapshot) {
      return A.status('Video export engine is unavailable');
    }
    R.captureCurrent();
    const { start, end } = normalizeRange();
    const frames = R.frames.slice(start - 1, end);
    if (!frames.length) return A.status('No frames in selected section');

    const canvas = A.videoExport.canvas;
    const width = Math.max(320, Number($('export-width')?.value || 1280));
    canvas.width = width;
    canvas.height = Math.round(width * 9 / 16);
    const rate = fps();
    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9') ? 'video/webm;codecs=vp9' : 'video/webm';
    const stream = canvas.captureStream(rate);
    const chunks = [];
    const recorder = new MediaRecorder(stream, { mimeType });
    recorder.ondataavailable = (event) => { if (event.data?.size) chunks.push(event.data); };
    const stopped = new Promise((resolve) => { recorder.onstop = resolve; });

    try {
      await A.videoExport.drawSnapshot(frames[0].snapshot);
      recorder.start(100);
      for (let i = 0; i < frames.length; i += 1) {
        await A.videoExport.drawSnapshot(frames[i].snapshot);
        if ($('c17-meta')) $('c17-meta').textContent = `Rendering section frame ${start + i} / ${end}`;
        await sleep(Math.max(1, Number(frames[i].hold) || 1) * 1000 / rate);
      }
      recorder.stop();
      await stopped;
      const blob = new Blob(chunks, { type: recorder.mimeType || 'video/webm' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `one-wave-clip-f${String(start).padStart(4, '0')}-f${String(end).padStart(4, '0')}.webm`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 0);
      A.status(`Section ${start}–${end} exported as WebM clip`);
    } catch (error) {
      console.error(error);
      if (recorder.state !== 'inactive') recorder.stop();
      A.status(`Section export failed: ${error.message}`);
    } finally {
      stream.getTracks().forEach((track) => track.stop());
      normalizeRange();
    }
  }

  $('c17-start')?.addEventListener('input', () => normalizeRange('start'));
  $('c17-end')?.addEventListener('input', () => normalizeRange('end'));
  $('c17-mark-start')?.addEventListener('click', () => { $('c17-start').value = String(R.activeIndex + 1); normalizeRange('start'); });
  $('c17-mark-end')?.addEventListener('click', () => { $('c17-end').value = String(R.activeIndex + 1); normalizeRange('end'); });
  $('c17-preview')?.addEventListener('click', previewSection);
  $('c17-export')?.addEventListener('click', exportSection);
  $('fps-control')?.addEventListener('input', () => normalizeRange());

  const oldSetFrames = R.setFrames?.bind(R);
  if (oldSetFrames && !R._c17Wrapped) {
    R.setFrames = function(...args) {
      const result = oldSetFrames(...args);
      syncLimits();
      return result;
    };
    R._c17Wrapped = true;
  }

  A.clipSections = { normalizeRange, previewSection, exportSection, syncLimits };
  syncLimits();
})();