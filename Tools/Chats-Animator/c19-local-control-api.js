(() => {
  'use strict';
  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C19 requires Animator + reel');

  const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));
  const history = [];
  const MAX_HISTORY = 50;

  function projectSnapshot() {
    R.captureCurrent?.();
    return {
      version: 1,
      activeIndex: R.activeIndex,
      frames: clone(R.frames),
      scene: A.snapshot(),
      fps: A.playback?.fps || Number(document.getElementById('fps-control')?.value || 24)
    };
  }

  function pushUndo(label) {
    history.push({ label, state: projectSnapshot(), at: new Date().toISOString() });
    if (history.length > MAX_HISTORY) history.shift();
  }

  function restoreProject(saved) {
    if (!saved?.frames?.length) throw new Error('Invalid saved project state');
    R.setFrames(clone(saved.frames), Math.max(0, Math.min(saved.activeIndex || 0, saved.frames.length - 1)));
    if (saved.scene) A.restore(clone(saved.scene));
    const fps = document.getElementById('fps-control');
    if (fps && saved.fps) {
      fps.value = String(saved.fps);
      fps.dispatchEvent(new Event('input', { bubbles: true }));
    }
    R.captureCurrent?.();
    return projectSnapshot();
  }

  function setHold(value) {
    const el = document.getElementById('frame-hold');
    if (!el) throw new Error('Frame hold control missing');
    const next = Math.max(Number(el.min || 1), Math.min(Number(el.max || 12), Number(value)));
    el.value = String(next);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    return next;
  }

  function setFps(value) {
    const el = document.getElementById('fps-control');
    if (!el) throw new Error('FPS control missing');
    const next = Math.max(Number(el.min || 1), Math.min(Number(el.max || 60), Number(value)));
    el.value = String(next);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    return next;
  }

  function click(id) {
    const el = document.getElementById(id);
    if (!el) throw new Error(`Control missing: ${id}`);
    el.click();
  }

  const mutating = new Set([
    'add_frame','duplicate_frame','delete_frame','set_hold','set_fps','set_background','clear_background',
    'add_prop','add_character','remove_selected','capture_motion','insert_motion','restore_project'
  ]);

  async function call(operation, args = {}) {
    if (mutating.has(operation)) pushUndo(operation);
    let result;

    switch (operation) {
      case 'get_project': result = projectSnapshot(); break;
      case 'get_scene': result = clone(A.snapshot()); break;
      case 'get_frame': result = { index: R.activeIndex + 1, frame: clone(R.activeFrame) }; break;
      case 'get_motion_library': result = A.motionLibrary?.library || null; break;
      case 'add_frame': click('add-frame'); result = { frame: R.activeIndex + 1 }; break;
      case 'duplicate_frame': click('duplicate-frame'); result = { frame: R.activeIndex + 1 }; break;
      case 'delete_frame': click('delete-frame'); result = { frame: R.activeIndex + 1 }; break;
      case 'select_frame': {
        const n = Number(args.frame);
        if (!Number.isInteger(n) || n < 1 || n > R.frames.length) throw new Error(`Frame ${args.frame} does not exist`);
        R.restore(n - 1); result = { frame: n }; break;
      }
      case 'set_hold': result = { hold: setHold(args.hold) }; break;
      case 'set_fps': result = { fps: setFps(args.fps) }; break;
      case 'play': A.playback?.play?.(); result = { playing: true }; break;
      case 'stop': A.playback?.stop?.(); result = { playing: false }; break;
      case 'set_background': result = A.setBackgroundFromSource(args.src, args.name || 'Generated Background.png'); break;
      case 'clear_background': A.state.background = null; A.renderAll(); R.captureCurrent?.(); result = { cleared: true }; break;
      case 'add_prop': result = A.addAssetFromSource(args.src, 'prop', args.name || 'Generated Prop.png', args.placement || {}); break;
      case 'add_character': result = A.addAssetFromSource(args.src, 'character', args.name || 'Generated Character.png', args.placement || {}); break;
      case 'remove_selected': click('remove-selected'); result = { removed: true }; break;
      case 'capture_motion': {
        if (!A.directorDialogue?.captureMotion) throw new Error('Motion capture bridge not ready');
        result = { message: A.directorDialogue.captureMotion(Number(args.start), Number(args.end), args.name || 'Motion', args.tag || '') };
        break;
      }
      case 'insert_motion': {
        if (!A.motionLibrary?.insertSequence) throw new Error('Motion Library not ready');
        A.motionLibrary.insertSequence(Number(args.index || 0)); result = { inserted: Number(args.index || 0) }; break;
      }
      case 'restore_project': result = restoreProject(args.project); break;
      case 'undo': {
        const last = history.pop();
        if (!last) return { ok: false, operation, error: 'Nothing to undo' };
        result = restoreProject(last.state);
        break;
      }
      default: throw new Error(`Unknown control operation: ${operation}`);
    }

    const response = { ok: true, operation, result };
    window.dispatchEvent(new CustomEvent('onewave-control-result', { detail: response }));
    return response;
  }

  const api = {
    version: 1,
    operations: [
      'get_project','get_scene','get_frame','get_motion_library','add_frame','duplicate_frame','delete_frame',
      'select_frame','set_hold','set_fps','play','stop','set_background','clear_background','add_prop',
      'add_character','remove_selected','capture_motion','insert_motion','restore_project','undo'
    ],
    call,
    get historyDepth() { return history.length; }
  };

  A.control = api;
  window.OneWaveAnimatorControl = api;
  window.addEventListener('onewave-control-request', async (event) => {
    const request = event.detail || {};
    try {
      const response = await call(request.operation, request.args || {});
      window.dispatchEvent(new CustomEvent('onewave-control-response', { detail: { id: request.id || null, ...response } }));
    } catch (error) {
      window.dispatchEvent(new CustomEvent('onewave-control-response', { detail: { id: request.id || null, ok: false, operation: request.operation, error: error.message || String(error) } }));
    }
  });

  A.status('Local control API ready');
})();
