(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B13 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Video export</strong><br>
    Render the reel, frame holds, per-frame camera, soundtrack, and timed Voice Lab dialogue into a downloadable WebM video.
    <div class="control"><label><span>Width</span><span id="export-width-value">1280</span></label><input id="export-width" type="range" min="320" max="1920" step="160" value="1280"></div>
    <button id="export-webm" type="button">Export WebM Video</button>
    <div id="export-meta" style="margin-top:8px">Ready</div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  const canvas = document.createElement('canvas');
  canvas.hidden = true;
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  const imageCache = new Map();

  $('export-width')?.addEventListener('input', (event) => {
    if ($('export-width-value')) $('export-width-value').textContent = event.target.value;
  });

  function loadImage(src) {
    if (!src) return Promise.resolve(null);
    if (imageCache.has(src)) return imageCache.get(src);
    const promise = new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = reject;
      image.src = src;
    });
    imageCache.set(src, promise);
    return promise;
  }

  function drawContained(image, width, height) {
    if (!image) return;
    const ratio = Math.min(width / image.naturalWidth, height / image.naturalHeight);
    const w = image.naturalWidth * ratio;
    const h = image.naturalHeight * ratio;
    ctx.drawImage(image, (width - w) / 2, (height - h) / 2, w, h);
  }

  function autoScale(asset, calibration) {
    const c = calibration || { farY: 0.48, nearY: 0.92, farScale: 0.35, nearScale: 1 };
    const span = Math.max(0.001, Number(c.nearY) - Number(c.farY));
    const t = Math.max(0, Math.min(1, (Number(asset.groundY) - Number(c.farY)) / span));
    return Number(c.farScale) + (Number(c.nearScale) - Number(c.farScale)) * t;
  }

  async function drawSnapshot(snapshot) {
    const width = canvas.width;
    const height = canvas.height;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = '#090a0d';
    ctx.fillRect(0, 0, width, height);
    const camera = snapshot.camera || { x: 0, y: 0, zoom: 1 };
    ctx.save();
    ctx.translate(width / 2 + (Number(camera.x) || 0) * width / 100, height / 2 + (Number(camera.y) || 0) * height / 100);
    ctx.scale(Number(camera.zoom) || 1, Number(camera.zoom) || 1);
    ctx.translate(-width / 2, -height / 2);
    if (snapshot.background?.src) drawContained(await loadImage(snapshot.background.src), width, height);
    const assets = [...(snapshot.assets || [])].sort((a, b) => Number(a.groundY) - Number(b.groundY));
    for (const asset of assets) {
      const image = await loadImage(asset.src);
      if (!image) continue;
      const scale = autoScale(asset, snapshot.calibration) * (Number(asset.manualScale) || 1);
      const drawH = Math.max(height * 0.05, height * 0.42 * scale);
      const drawW = drawH * (image.naturalWidth / image.naturalHeight);
      const x = Number(asset.x) * width - drawW / 2;
      const y = Number(asset.groundY) * height - drawH;
      ctx.drawImage(image, x, y, drawW, drawH);
    }
    ctx.restore();
  }

  function sleep(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }

  async function makeFallbackAudioTrack(stream) {
    const track = A.audio?.track;
    if (!track?.src || !window.AudioContext) return null;
    const element = new Audio(track.src);
    element.preload = 'auto';
    const context = new AudioContext();
    const source = context.createMediaElementSource(element);
    const destination = context.createMediaStreamDestination();
    source.connect(destination);
    const audioTrack = destination.stream.getAudioTracks()[0];
    if (audioTrack) stream.addTrack(audioTrack);
    await context.resume();
    return { element, context, stop() { element.pause(); } };
  }

  async function exportVideo() {
    if (!window.MediaRecorder || !canvas.captureStream) return A.status('This browser cannot export WebM');
    if (!R.frames.length) return A.status('No frames to export');
    R.captureCurrent();
    const width = Math.max(320, Number($('export-width')?.value || 1280));
    canvas.width = width;
    canvas.height = Math.round(width * 9 / 16);
    const fps = Math.max(1, A.playback?.fps || Number($('fps-control')?.value || 24));
    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus') ? 'video/webm;codecs=vp9,opus' : 'video/webm';
    const stream = canvas.captureStream(fps);
    let exportAudio = null;
    try {
      exportAudio = A.voiceLab?.makeCombinedAudioTrack
        ? await A.voiceLab.makeCombinedAudioTrack(stream)
        : await makeFallbackAudioTrack(stream);
      const chunks = [];
      const recorder = new MediaRecorder(stream, { mimeType });
      recorder.ondataavailable = (event) => { if (event.data?.size) chunks.push(event.data); };
      const stopped = new Promise((resolve) => { recorder.onstop = resolve; });
      $('export-meta').textContent = `Rendering ${R.frames.length} frames…`;
      await drawSnapshot(R.frames[0].snapshot);
      recorder.start(100);
      if (exportAudio?.element) {
        exportAudio.element.currentTime = 0;
        await exportAudio.element.play().catch(() => null);
      }
      for (let i = 0; i < R.frames.length; i += 1) {
        const frame = R.frames[i];
        await drawSnapshot(frame.snapshot);
        $('export-meta').textContent = `Rendering frame ${i + 1} / ${R.frames.length}`;
        await sleep(Math.max(1, Number(frame.hold) || 1) * 1000 / fps);
      }
      recorder.stop();
      await stopped;
      exportAudio?.stop?.();
      if (exportAudio?.element) exportAudio.element.pause();
      await exportAudio?.context?.close?.();
      const blob = new Blob(chunks, { type: recorder.mimeType || 'video/webm' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `one-wave-video-${new Date().toISOString().replace(/[:.]/g, '-')}.webm`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 0);
      $('export-meta').textContent = `Exported ${(blob.size / 1024).toFixed(1)} KB`;
      A.status('WebM video exported with final audio mix');
    } catch (error) {
      console.error(error);
      exportAudio?.stop?.();
      if (exportAudio?.element) exportAudio.element.pause();
      try { await exportAudio?.context?.close?.(); } catch (_) {}
      $('export-meta').textContent = 'Export failed';
      A.status(`Video export failed: ${error.message}`);
    } finally {
      for (const track of stream.getTracks()) track.stop();
    }
  }

  function loadScript(src, marker, done) {
    if (document.querySelector(`script[${marker}]`)) return done?.();
    const script = document.createElement('script');
    script.src = src;
    script.setAttribute(marker, 'true');
    if (done) script.onload = done;
    document.body.appendChild(script);
  }

  function loadVoicePipeline() {
    const afterC6 = () => loadScript('./c7-dialogue-editor.js', 'data-c7-dialogue-editor', () => {
      loadScript('./c8-dialogue-frame-sync.js', 'data-c8-dialogue-sync');
    });
    if (A.voiceLab) afterC6();
    else loadScript('./c6-voice-lab.js', 'data-c6-voice-lab', afterC6);
  }

  $('export-webm')?.addEventListener('click', exportVideo);
  A.videoExport = { exportVideo, drawSnapshot, canvas };
  loadVoicePipeline();
})();
