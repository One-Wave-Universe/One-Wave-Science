(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.voiceLab || !A?.dialogueEditor) throw new Error('C11 requires Voice Lab + Dialogue Editor');

  const clamp = (v, lo, hi, fallback = lo) => {
    const n = Number(v);
    return Math.max(lo, Math.min(hi, Number.isFinite(n) ? n : fallback));
  };

  function sanitizeRecipe(recipe = {}) {
    recipe.pitch = clamp(recipe.pitch, -1200, 1200, 0);
    recipe.highpass = clamp(recipe.highpass, 20, 400, 70);
    recipe.body = clamp(recipe.body, -12, 12, 0);
    recipe.presence = clamp(recipe.presence, -12, 12, 1.5);
    recipe.compress = clamp(recipe.compress, -40, 0, -18);
    recipe.drive = clamp(recipe.drive, 0, 100, 0);
    recipe.delayMs = clamp(recipe.delayMs, 0, 1000, 110);
    recipe.delayMix = clamp(recipe.delayMix, 0, 60, 0);
    recipe.reverb = clamp(recipe.reverb, 0, 60, 0);
    return recipe;
  }

  function sanitizeLayerSetting(setting = {}) {
    setting.gain = clamp(setting.gain, -36, 12, 0);
    setting.pan = clamp(setting.pan, -1, 1, 0);
    setting.detune = clamp(setting.detune, -600, 600, 0);
    setting.delayMs = clamp(setting.delayMs, 0, 250, 0);
    return setting;
  }

  function sanitizeClip(clip = {}) {
    clip.name = String(clip.name || 'Speech clip').slice(0, 120);
    clip.start = clamp(clip.start, 0, 86400, 0);
    clip.trimStart = clamp(clip.trimStart, 0, 3600, 0);
    clip.trimEnd = clamp(clip.trimEnd, 0, 3600, 0);
    clip.fadeIn = clamp(clip.fadeIn, 0, 10, 0.02);
    clip.fadeOut = clamp(clip.fadeOut, 0, 10, 0.04);
    clip.gainDb = clamp(clip.gainDb, -36, 18, 0);
    clip.muted = Boolean(clip.muted);
    clip.layers = Array.isArray(clip.layers) ? clip.layers.slice(0, 3) : [];
    while (clip.layers.length < 3) clip.layers.push(null);
    clip.settings = Array.isArray(clip.settings) ? clip.settings.slice(0, 3) : [];
    while (clip.settings.length < 3) clip.settings.push({});
    clip.settings = clip.settings.map(sanitizeLayerSetting);
    return clip;
  }

  function sanitizeAll() {
    const state = A.voiceLab.state;
    if (!Array.isArray(state.characters) || !state.characters.length) return;
    state.characters.forEach((character, index) => {
      character.name = String(character.name || `Character ${index + 1}`).slice(0, 80);
      character.recipe = sanitizeRecipe(character.recipe || {});
    });
    if (!Array.isArray(state.clips)) state.clips = [];
    state.clips.forEach(sanitizeClip);

    const mix = A.dialogueEditor.state;
    mix.duckDb = clamp(mix.duckDb, 0, 24, 9);
    mix.attackMs = clamp(mix.attackMs, 10, 500, 80);
    mix.releaseMs = clamp(mix.releaseMs, 50, 1500, 300);
    return state;
  }

  const originalVoiceLoad = A.voiceLab.loadState?.bind(A.voiceLab);
  if (originalVoiceLoad && !A.voiceLab._c11Wrapped) {
    A.voiceLab.loadState = function(next) {
      const result = originalVoiceLoad(next);
      sanitizeAll();
      return result;
    };
    A.voiceLab._c11Wrapped = true;
  }

  const originalDialogueLoad = A.dialogueEditor.loadState?.bind(A.dialogueEditor);
  if (originalDialogueLoad && !A.dialogueEditor._c11Wrapped) {
    A.dialogueEditor.loadState = function(next) {
      const result = originalDialogueLoad(next);
      sanitizeAll();
      A.dialogueEditor.render?.();
      return result;
    };
    A.dialogueEditor._c11Wrapped = true;
  }

  const originalEnsure = A.dialogueEditor.ensureClip?.bind(A.dialogueEditor);
  if (originalEnsure) {
    A.dialogueEditor.ensureClip = function(clip) {
      originalEnsure(clip);
      return sanitizeClip(clip);
    };
  }

  sanitizeAll();
  A.audioSessionSafety = { sanitizeAll, sanitizeRecipe, sanitizeClip, sanitizeLayerSetting };
  A.status('Audio session safety loaded');
})();
