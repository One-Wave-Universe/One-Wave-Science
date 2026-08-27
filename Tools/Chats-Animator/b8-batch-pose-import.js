(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B8 requires Animator + reel');
  const $ = (id) => document.getElementById(id);
  const collator = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });

  $('batch-import-poses')?.addEventListener('click', () => {
    const selected = A.state.assets.find((asset) => asset.id === A.state.selectedAssetId);
    if (!selected) return A.status('Select a character or prop first');
    $('batch-pose-picker')?.click();
  });

  $('batch-pose-picker')?.addEventListener('change', async (event) => {
    const files = Array.from(event.target.files || []).sort((a, b) => collator.compare(a.name, b.name));
    const selected = A.state.assets.find((asset) => asset.id === A.state.selectedAssetId);
    if (!files.length || !selected) return;
    R.captureCurrent();
    const baseIndex = R.activeIndex;
    const hold = Math.max(1, Number($('batch-hold')?.value || 2));
    const newFrames = [];
    for (const file of files) {
      const snapshot = A.clone(R.frames[baseIndex].snapshot);
      const target = snapshot.assets.find((asset) => asset.id === selected.id);
      if (!target) continue;
      target.src = await A.readFile(file);
      target.name = file.name;
      snapshot.selectedAssetId = selected.id;
      newFrames.push(R.makeFrame(snapshot, hold));
    }
    R.frames.splice(baseIndex + 1, 0, ...newFrames);
    if (newFrames.length) R.restore(baseIndex + 1);
    A.status(`${newFrames.length} pose frame${newFrames.length === 1 ? '' : 's'} imported`);
    event.target.value = '';
  });
})();
