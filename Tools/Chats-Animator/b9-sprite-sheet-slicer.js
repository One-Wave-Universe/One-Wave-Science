(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B9 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const selectedControls = $('selected-controls');
  if (!selectedControls) return;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>Sprite-sheet slicer</strong><br>
    Select the character/prop, choose a sprite/pose sheet, set its rows and columns, then extract cells into consecutive reel frames.
    Transparent/blank cells are skipped.
    <div class="control"><label><span>Rows</span><span id="sheet-rows-value">1</span></label><input id="sheet-rows" type="range" min="1" max="16" step="1" value="1"></div>
    <div class="control"><label><span>Columns</span><span id="sheet-cols-value">4</span></label><input id="sheet-cols" type="range" min="1" max="16" step="1" value="4"></div>
    <label>Sheet hold <input id="sheet-hold" type="range" min="1" max="12" step="1" value="2"> <span id="sheet-hold-value">2x</span></label><br><br>
    <button id="slice-sprite-sheet" type="button">Slice Sprite / Pose Sheet</button>
    <input id="sprite-sheet-picker" type="file" accept="image/png,image/webp,image/jpeg" hidden>
  `;
  selectedControls.appendChild(panel);

  for (const [inputId, valueId, suffix] of [['sheet-rows', 'sheet-rows-value', ''], ['sheet-cols', 'sheet-cols-value', ''], ['sheet-hold', 'sheet-hold-value', 'x']]) {
    $(inputId)?.addEventListener('input', (event) => { if ($(valueId)) $(valueId).textContent = `${event.target.value}${suffix}`; });
  }

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = reject;
      image.src = src;
    });
  }

  function cellHasVisiblePixels(ctx, x, y, w, h) {
    const data = ctx.getImageData(x, y, w, h).data;
    for (let i = 3; i < data.length; i += 4) {
      if (data[i] > 8) return true;
    }
    return false;
  }

  async function slice(file) {
    const selected = A.state.assets.find((asset) => asset.id === A.state.selectedAssetId);
    if (!selected) return A.status('Select a character or prop first');
    const rows = Math.max(1, Number($('sheet-rows')?.value || 1));
    const cols = Math.max(1, Number($('sheet-cols')?.value || 1));
    const hold = Math.max(1, Number($('sheet-hold')?.value || 2));
    const src = await A.readFile(file);
    const image = await loadImage(src);
    const cellW = Math.floor(image.naturalWidth / cols);
    const cellH = Math.floor(image.naturalHeight / rows);
    if (!cellW || !cellH) return A.status('Sheet grid is larger than the image');

    const sheetCanvas = document.createElement('canvas');
    sheetCanvas.width = image.naturalWidth;
    sheetCanvas.height = image.naturalHeight;
    const sheetCtx = sheetCanvas.getContext('2d', { willReadFrequently: true });
    sheetCtx.drawImage(image, 0, 0);

    R.captureCurrent();
    const baseIndex = R.activeIndex;
    const extracted = [];
    let sequence = 1;
    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col < cols; col += 1) {
        const sx = col * cellW;
        const sy = row * cellH;
        if (!cellHasVisiblePixels(sheetCtx, sx, sy, cellW, cellH)) continue;
        const cellCanvas = document.createElement('canvas');
        cellCanvas.width = cellW;
        cellCanvas.height = cellH;
        const ctx = cellCanvas.getContext('2d');
        ctx.drawImage(image, sx, sy, cellW, cellH, 0, 0, cellW, cellH);
        const poseSrc = cellCanvas.toDataURL('image/png');
        const snapshot = A.clone(R.frames[baseIndex].snapshot);
        const target = snapshot.assets.find((asset) => asset.id === selected.id);
        if (!target) continue;
        target.src = poseSrc;
        target.name = `${file.name.replace(/\.[^.]+$/, '')}_${String(sequence).padStart(2, '0')}.png`;
        snapshot.selectedAssetId = selected.id;
        extracted.push(R.makeFrame(snapshot, hold));
        sequence += 1;
      }
    }
    if (!extracted.length) return A.status('No nonblank cells found');
    R.frames.splice(baseIndex + 1, 0, ...extracted);
    R.restore(baseIndex + 1);
    A.status(`${extracted.length} sprite-sheet poses extracted`);
  }

  $('slice-sprite-sheet')?.addEventListener('click', () => {
    const selected = A.state.assets.find((asset) => asset.id === A.state.selectedAssetId);
    if (!selected) return A.status('Select a character or prop first');
    $('sprite-sheet-picker')?.click();
  });
  $('sprite-sheet-picker')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    try {
      if (file) await slice(file);
    } catch (error) {
      console.error(error);
      A.status('Sprite-sheet slicing failed');
    } finally {
      event.target.value = '';
    }
  });
})();
