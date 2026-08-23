(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('B5 requires Animator + reel');
  const $ = (id) => document.getElementById(id);

  function currentSelected() {
    return A.state.assets.find((asset) => asset.id === A.state.selectedAssetId) || null;
  }
  function adjacentCopy(offset) {
    const selected = currentSelected();
    if (!selected) return A.status('Select a character or prop first');
    R.captureCurrent();
    const targetIndex = R.activeIndex + offset;
    if (targetIndex < 0 || targetIndex >= R.frames.length) return A.status('No adjacent frame there');
    const target = R.frames[targetIndex];
    const targetAsset = target.snapshot.assets.find((asset) => asset.id === selected.id);
    if (targetAsset) Object.assign(targetAsset, A.clone(selected));
    else target.snapshot.assets.push(A.clone(selected));
    A.status('Pose copied to adjacent frame');
    A.onion?.render?.();
  }

  $('insert-before')?.addEventListener('click', () => R.insertAt(R.activeIndex, R.makeFrame(R.activeFrame.snapshot, R.activeFrame.hold), true));
  $('insert-after')?.addEventListener('click', () => R.insertAt(R.activeIndex + 1, R.makeFrame(R.activeFrame.snapshot, R.activeFrame.hold), true));
  $('move-frame-left')?.addEventListener('click', () => {
    const i = R.activeIndex;
    if (i <= 0) return;
    R.captureCurrent();
    [R.frames[i - 1], R.frames[i]] = [R.frames[i], R.frames[i - 1]];
    R.restore(i - 1);
  });
  $('move-frame-right')?.addEventListener('click', () => {
    const i = R.activeIndex;
    if (i >= R.frames.length - 1) return;
    R.captureCurrent();
    [R.frames[i + 1], R.frames[i]] = [R.frames[i], R.frames[i + 1]];
    R.restore(i + 1);
  });
  $('replace-selected-pose')?.addEventListener('click', () => {
    if (!currentSelected()) return A.status('Select a character or prop first');
    $('replacement-picker')?.click();
  });
  $('replacement-picker')?.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    const selected = currentSelected();
    if (!file || !selected) return;
    selected.src = await A.readFile(file);
    selected.name = file.name;
    A.renderAll();
    R.captureCurrent();
    A.status('Pose replaced on current frame');
    event.target.value = '';
  });
  $('copy-pose-prev')?.addEventListener('click', () => adjacentCopy(-1));
  $('copy-pose-next')?.addEventListener('click', () => adjacentCopy(1));
})();
