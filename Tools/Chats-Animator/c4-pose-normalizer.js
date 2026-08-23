(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C4 pose normalizer requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Normalize pose stills before layout</strong><br>
    Trim transparent padding, resize each pose to one square transparent canvas, center it, and anchor the visible artwork to the same bottom line before path/cadence is applied.
    <div class="control"><label><span>Pose frames</span><span id="normalize-count-value">7</span></label><input id="normalize-count" type="range" min="1" max="48" step="1" value="7"></div>
    <div class="control"><label><span>Canvas size</span><span id="normalize-size-value">1024</span></label><input id="normalize-size" type="range" min="256" max="1536" step="128" value="1024"></div>
    <div class="control"><label><span>Subject height</span><span id="normalize-fill-value">90%</span></label><input id="normalize-fill" type="range" min="50" max="96" step="1" value="90"></div>
    <div class="control"><label><span>Bottom margin</span><span id="normalize-bottom-value">3%</span></label><input id="normalize-bottom" type="range" min="0" max="15" step="1" value="3"></div>
    <button id="normalize-pose-run" type="button">Normalize Pose Run</button>
    <div id="normalize-meta" style="margin-top:8px">Ready</div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  for (const [inputId, valueId, suffix] of [
    ['normalize-count','normalize-count-value',''],
    ['normalize-size','normalize-size-value',''],
    ['normalize-fill','normalize-fill-value','%'],
    ['normalize-bottom','normalize-bottom-value','%']
  ]) {
    $(inputId)?.addEventListener('input', (event) => {
      if ($(valueId)) $(valueId).textContent = `${event.target.value}${suffix}`;
    });
  }

  function selectedAsset() {
    return A.state.assets.find((asset) => asset.id === A.state.selectedAssetId) || null;
  }

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = reject;
      image.src = src;
    });
  }

  function alphaBounds(ctx, width, height) {
    const pixels = ctx.getImageData(0, 0, width, height).data;
    let minX = width, minY = height, maxX = -1, maxY = -1;
    let transparentPixelSeen = false;
    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        const alpha = pixels[(y * width + x) * 4 + 3];
        if (alpha < 250) transparentPixelSeen = true;
        if (alpha <= 8) continue;
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
    if (maxX < minX || maxY < minY) return null;
    return { x: minX, y: minY, width: maxX - minX + 1, height: maxY - minY + 1, hasTransparency: transparentPixelSeen };
  }

  async function normalizeSource(src, size, fillPercent, bottomPercent) {
    const image = await loadImage(src);
    const source = document.createElement('canvas');
    source.width = image.naturalWidth;
    source.height = image.naturalHeight;
    const sctx = source.getContext('2d', { willReadFrequently: true });
    sctx.clearRect(0, 0, source.width, source.height);
    sctx.drawImage(image, 0, 0);
    const bounds = alphaBounds(sctx, source.width, source.height);
    if (!bounds) return { src, changed: false, hasTransparency: true };

    const output = document.createElement('canvas');
    output.width = size;
    output.height = size;
    const octx = output.getContext('2d');
    octx.clearRect(0, 0, size, size);

    const targetHeight = size * (fillPercent / 100);
    const maxWidth = size * 0.94;
    let scale = targetHeight / Math.max(1, bounds.height);
    if (bounds.width * scale > maxWidth) scale = maxWidth / Math.max(1, bounds.width);
    const drawW = bounds.width * scale;
    const drawH = bounds.height * scale;
    const x = (size - drawW) / 2;
    const bottomMargin = size * (bottomPercent / 100);
    const y = size - bottomMargin - drawH;
    octx.drawImage(source, bounds.x, bounds.y, bounds.width, bounds.height, x, y, drawW, drawH);
    return { src: output.toDataURL('image/png'), changed: true, hasTransparency: bounds.hasTransparency };
  }

  async function normalizeRun() {
    const selected = selectedAsset();
    if (!selected) return A.status('Select a character or prop first');
    R.captureCurrent();
    const count = Math.max(1, Number($('normalize-count')?.value || 7));
    const size = Math.max(256, Number($('normalize-size')?.value || 1024));
    const fill = Math.max(50, Math.min(96, Number($('normalize-fill')?.value || 90)));
    const bottom = Math.max(0, Math.min(15, Number($('normalize-bottom')?.value || 3)));
    const start = R.activeIndex;
    const frames = R.frames.slice(start, Math.min(R.frames.length, start + count));
    let changed = 0;
    let opaque = 0;

    if ($('normalize-meta')) $('normalize-meta').textContent = `Normalizing ${frames.length} pose frame${frames.length === 1 ? '' : 's'}…`;
    for (let i = 0; i < frames.length; i += 1) {
      const asset = frames[i].snapshot.assets.find((item) => item.id === selected.id);
      if (!asset?.src) continue;
      const result = await normalizeSource(asset.src, size, fill, bottom);
      if (result.changed) {
        asset.src = result.src;
        changed += 1;
      }
      if (!result.hasTransparency) opaque += 1;
    }
    R.restore(start);
    if ($('normalize-meta')) $('normalize-meta').textContent = `${changed} pose${changed === 1 ? '' : 's'} normalized to ${size}×${size}${opaque ? ` — ${opaque} source${opaque === 1 ? '' : 's'} had no transparency` : ''}`;
    A.status(`Pose normalization complete: ${changed} frame${changed === 1 ? '' : 's'}`);
  }

  $('normalize-pose-run')?.addEventListener('click', () => {
    normalizeRun().catch((error) => {
      console.error(error);
      A.status(`Pose normalization failed: ${error.message}`);
      if ($('normalize-meta')) $('normalize-meta').textContent = 'Normalization failed';
    });
  });

  A.poseNormalizer = { normalizeRun, normalizeSource, alphaBounds };
})();
