(() => {
  const A = window.OneWaveAnimator;
  const reel = window.b4Reel;
  if (!A || !reel || !window.b4Snapshot || !window.b4Restore) {
    throw new Error('B9 requires the B8 runnable checkpoint');
  }

  const $ = (id) => document.getElementById(id);
  const makeId = () => crypto.randomUUID?.() || `frame-${Date.now()}-${Math.random()}`;

  let sheetImage = null;
  let sheetName = '';

  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .b9-slicer{margin-top:14px;border:1px solid #343741;border-radius:9px;padding:12px;background:#101217}
      .b9-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}
      .b9-grid label{display:flex;flex-direction:column;gap:5px;font-size:12px;font-weight:700}
      .b9-grid input{width:100%;background:#17191f;color:#f5f6f8;border:1px solid #414551;border-radius:6px;padding:7px}
      #b9-preview{display:block;width:100%;max-height:280px;object-fit:contain;background:#090a0d;border:1px solid #343741;border-radius:7px;margin:10px 0}
      #b9-slicer-status{font-size:12px;color:#b8bdc8;margin-top:8px;line-height:1.4}
    `;
    document.head.appendChild(style);
  }

  function injectUI() {
    const selectedControls = $('selected-controls');
    if (!selectedControls || $('b9-slicer')) return;

    const panel = document.createElement('div');
    panel.className = 'b9-slicer';
    panel.id = 'b9-slicer';
    panel.innerHTML = `
      <strong>Sprite-sheet slicer</strong>
      <div style="margin-top:5px;font-size:13px;color:#c5cad4">
        Select a character/prop, load one pose sheet, set rows and columns, preview the grid,
        then create one reel frame per cell in row-major order.
      </div>
      <button id="b9-load-sheet" type="button" style="margin-top:10px">Load Pose Sheet</button>
      <input id="b9-sheet-picker" type="file" accept="image/png,image/webp,image/jpeg" hidden>
      <div class="b9-grid">
        <label>Rows
          <input id="b9-rows" type="number" min="1" max="24" step="1" value="2">
        </label>
        <label>Columns
          <input id="b9-cols" type="number" min="1" max="24" step="1" value="4">
        </label>
      </div>
      <canvas id="b9-preview" width="640" height="360"></canvas>
      <label style="display:flex;align-items:center;gap:8px;font-size:13px">
        Hold per slice
        <input id="b9-hold" type="range" min="1" max="12" step="1" value="2" style="flex:1">
        <span id="b9-hold-value">2x</span>
      </label>
      <button id="b9-create-frames" type="button" style="margin-top:10px">Create Frames from Slices</button>
      <div id="b9-slicer-status">No pose sheet loaded.</div>
    `;
    selectedControls.appendChild(panel);
  }

  function clampGridValue(id) {
    const input = $(id);
    let value = Math.round(Number(input.value) || 1);
    value = Math.max(1, Math.min(24, value));
    input.value = value;
    return value;
  }

  function drawPreview() {
    const canvas = $('b9-preview');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#090a0d';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (!sheetImage) {
      ctx.fillStyle = '#737987';
      ctx.font = '16px system-ui';
      ctx.textAlign = 'center';
      ctx.fillText('Load a pose sheet to preview slices', canvas.width / 2, canvas.height / 2);
      return;
    }

    const rows = clampGridValue('b9-rows');
    const cols = clampGridValue('b9-cols');
    const scale = Math.min(canvas.width / sheetImage.width, canvas.height / sheetImage.height);
    const drawW = sheetImage.width * scale;
    const drawH = sheetImage.height * scale;
    const left = (canvas.width - drawW) / 2;
    const top = (canvas.height - drawH) / 2;

    ctx.drawImage(sheetImage, left, top, drawW, drawH);
    ctx.strokeStyle = 'rgba(255,255,255,.88)';
    ctx.lineWidth = 1;

    for (let c = 0; c <= cols; c++) {
      const x = left + (drawW * c / cols);
      ctx.beginPath();
      ctx.moveTo(x, top);
      ctx.lineTo(x, top + drawH);
      ctx.stroke();
    }
    for (let r = 0; r <= rows; r++) {
      const y = top + (drawH * r / rows);
      ctx.beginPath();
      ctx.moveTo(left, y);
      ctx.lineTo(left + drawW, y);
      ctx.stroke();
    }

    $('b9-slicer-status').textContent =
      `${sheetName} — ${sheetImage.width}×${sheetImage.height}px — ${rows}×${cols} = ${rows * cols} slices`;
  }

  async function loadSheet(file) {
    if (!file) return;
    const dataUrl = await A.readFileAsDataURL(file);
    sheetName = file.name;
    sheetImage = new Image();

    await new Promise((resolve, reject) => {
      sheetImage.onload = resolve;
      sheetImage.onerror = () => reject(new Error('Could not decode pose sheet image'));
      sheetImage.src = dataUrl;
    });

    drawPreview();
  }

  function sliceToDataUrl(row, col, rows, cols) {
    const sourceX = Math.round(sheetImage.width * col / cols);
    const sourceY = Math.round(sheetImage.height * row / rows);
    const nextX = Math.round(sheetImage.width * (col + 1) / cols);
    const nextY = Math.round(sheetImage.height * (row + 1) / rows);
    const width = Math.max(1, nextX - sourceX);
    const height = Math.max(1, nextY - sourceY);

    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, width, height);
    ctx.drawImage(sheetImage, sourceX, sourceY, width, height, 0, 0, width, height);

    return { dataUrl: canvas.toDataURL('image/png'), width, height };
  }

  async function createFramesFromSlices() {
    const selected = A.selectedAsset();
    if (!selected) {
      $('b9-slicer-status').textContent = 'Select a character or prop before slicing.';
      return;
    }
    if (!sheetImage) {
      $('b9-slicer-status').textContent = 'Load a pose sheet first.';
      return;
    }

    const rows = clampGridValue('b9-rows');
    const cols = clampGridValue('b9-cols');
    const hold = Math.max(1, Math.min(12, Number($('b9-hold').value) || 2));

    window.b4SaveCurrentFrame();
    let insertAt = reel.activeIndex + 1;
    let firstInserted = -1;
    let count = 0;

    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const slice = sliceToDataUrl(row, col, rows, cols);
        const snap = window.b4Snapshot();
        const target = snap.assets.find((asset) => asset.id === selected.id);
        if (!target) continue;

        target.dataUrl = slice.dataUrl;
        target.width = slice.width;
        target.height = slice.height;
        target.name = `${sheetName || 'pose-sheet'}_r${row + 1}_c${col + 1}.png`;

        reel.frames.splice(insertAt, 0, {
          id: makeId(),
          hold,
          snapshot: snap
        });
        if (firstInserted < 0) firstInserted = insertAt;
        insertAt++;
        count++;
      }
    }

    if (firstInserted >= 0) {
      reel.activeIndex = firstInserted;
      window.b4Restore(reel.frames[firstInserted].snapshot);
    }

    window.b4RenderFrames();
    window.b4SaveReel();
    $('b9-slicer-status').textContent =
      `Created ${count} consecutive frame${count === 1 ? '' : 's'} from ${rows}×${cols} slices.`;
  }

  injectStyles();
  injectUI();
  drawPreview();

  $('b9-load-sheet').addEventListener('click', () => {
    if (!A.selectedAsset()) {
      $('b9-slicer-status').textContent = 'Select a character or prop first.';
      return;
    }
    $('b9-sheet-picker').click();
  });

  $('b9-sheet-picker').addEventListener('change', async (event) => {
    try {
      await loadSheet(event.target.files?.[0]);
    } catch (error) {
      $('b9-slicer-status').textContent = error.message;
    } finally {
      event.target.value = '';
    }
  });

  $('b9-rows').addEventListener('input', drawPreview);
  $('b9-cols').addEventListener('input', drawPreview);
  $('b9-hold').addEventListener('input', (event) => {
    $('b9-hold-value').textContent = `${event.target.value}x`;
  });
  $('b9-create-frames').addEventListener('click', createFramesFromSlices);

  window.b9SpriteSheetSlicer = { loadSheet, drawPreview, createFramesFromSlices };
})();
