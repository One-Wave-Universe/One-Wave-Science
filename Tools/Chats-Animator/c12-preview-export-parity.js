(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.voiceLab || !A?.dialogueEditor || !A?.audioHardening || !A?.playback) throw new Error('C12 requires hardened audio + playback');
  const button = document.getElementById('play-button');
  if (!button) return;

  let prepared = null;
  let wasPlaying = false;
  let starting = false;

  async function stopMix() {
    if (prepared) {
      prepared.stop?.();
      try { await prepared.context?.close?.(); } catch (_) {}
      prepared = null;
    }
  }

  async function prepareAndPlay() {
    if (starting) return;
    starting = true;
    const oldText = button.textContent;
    button.disabled = true;
    button.textContent = 'Loading Audio…';
    try {
      await stopMix();
      prepared = await A.audioHardening.prepareSpeakerMix();
      A.playback.play();
      await prepared.start();
      A.status('Playback using final-mix audio path');
    } catch (error) {
      console.error(error);
      if (A.playback.playing) A.playback.stop();
      await stopMix();
      A.status(`Final-mix preview failed: ${error.message}`);
    } finally {
      starting = false;
      button.disabled = false;
      if (!A.playback.playing) button.textContent = oldText === 'Stop' ? 'Play' : oldText;
    }
  }

  function capturePlayback(event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    if (starting) return;
    if (A.playback.playing) {
      A.playback.stop();
      stopMix();
    } else {
      prepareAndPlay();
    }
  }

  button.addEventListener('click', capturePlayback, true);

  const watcher = setInterval(() => {
    const now = Boolean(A.playback?.playing);
    if (wasPlaying && !now) stopMix();
    wasPlaying = now;
  }, 50);

  window.addEventListener('beforeunload', () => {
    clearInterval(watcher);
    stopMix();
  });

  A.previewParity = { prepareAndPlay, stopMix };
  A.status('Preview/export audio parity loaded');
})();
