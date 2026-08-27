(() => {
  'use strict';
  const A = window.Animator;
  if (!A) throw new Error('Animator core missing');
  const $ = (id) => document.getElementById(id);
  let frames = [{ id: A.uid('frame'), hold: 2, snapshot: A.snapshot() }];
  let activeIndex = 0;
  let restoring = false;

  const frame = () => frames[activeIndex];
  function captureCurrent() {
    if (restoring || !frame()) return;
    frame().snapshot = A.snapshot();
    renderReel();
  }
  function restore(index) {
    if (index < 0 || index >= frames.length) return;
    captureCurrent();
    activeIndex = index;
    restoring = true;
    A.restore(frames[index].snapshot);
    restoring = false;
    syncHold();
    renderReel();
    A.onion?.render?.();
  }
  function renderReel() {
    const reel = $('frame-reel');
    if (!reel) return;
    reel.innerHTML = '';
    frames.forEach((f, i) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = `frame-card${i === activeIndex ? ' active' : ''}`;
      button.innerHTML = `<strong>Frame ${i + 1}</strong><span>${f.hold}x hold</span>`;
      button.addEventListener('click', () => restore(i));
      reel.appendChild(button);
    });
    if ($('active-frame-label')) $('active-frame-label').textContent = `Frame ${activeIndex + 1} / ${frames.length}`;
  }
  function syncHold() {
    if (!$('frame-hold') || !frame()) return;
    $('frame-hold').value = frame().hold;
    if ($('frame-hold-value')) $('frame-hold-value').textContent = `${frame().hold}x`;
  }
  function makeFrame(snapshot = A.snapshot(), hold = 2) {
    return { id: A.uid('frame'), hold, snapshot: A.clone(snapshot) };
  }
  function insertAt(index, newFrame, activate = true) {
    captureCurrent();
    frames.splice(index, 0, newFrame);
    if (activate) restore(index); else renderReel();
  }

  $('add-frame')?.addEventListener('click', () => insertAt(frames.length, makeFrame(), true));
  $('duplicate-frame')?.addEventListener('click', () => insertAt(activeIndex + 1, makeFrame(frame().snapshot, frame().hold), true));
  $('delete-frame')?.addEventListener('click', () => {
    if (frames.length === 1) {
      frames[0] = makeFrame(A.snapshot(), 2);
      restore(0);
      return;
    }
    frames.splice(activeIndex, 1);
    activeIndex = Math.min(activeIndex, frames.length - 1);
    restoring = true;
    A.restore(frame().snapshot);
    restoring = false;
    syncHold();
    renderReel();
    A.onion?.render?.();
  });
  $('frame-hold')?.addEventListener('input', (event) => {
    frame().hold = Number(event.target.value);
    if ($('frame-hold-value')) $('frame-hold-value').textContent = `${frame().hold}x`;
    renderReel();
  });

  A.reel = {
    get frames() { return frames; },
    get activeIndex() { return activeIndex; },
    get activeFrame() { return frame(); },
    captureCurrent,
    restore,
    renderReel,
    makeFrame,
    insertAt,
    setFrames(nextFrames, nextIndex = 0) {
      frames = nextFrames;
      activeIndex = Math.max(0, Math.min(nextIndex, frames.length - 1));
      restoring = true;
      A.restore(frame().snapshot);
      restoring = false;
      syncHold();
      renderReel();
    }
  };
  syncHold();
  renderReel();
})();
