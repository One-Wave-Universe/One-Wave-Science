(() => {
  'use strict';

  const A = window.Animator;
  const R = A?.reel;
  if (!A || !R) throw new Error('C18 requires Animator + reel');

  const $ = (id) => document.getElementById(id);
  const workspace = document.querySelector('.workspace');
  const framePanel = document.querySelector('.frame-panel');
  if (!workspace || !framePanel) return;

  const style = document.createElement('style');
  style.textContent = `
    .director-panel{margin-top:14px;border:1px solid #343741;border-radius:10px;background:#14161b;padding:12px}
    .director-head{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:10px}
    .director-head small{color:#9fa6b3}
    .director-log{height:180px;overflow:auto;border:1px solid #30333c;border-radius:8px;background:#0d0f13;padding:10px;display:flex;flex-direction:column;gap:8px}
    .director-msg{max-width:92%;padding:8px 10px;border-radius:8px;white-space:pre-wrap;line-height:1.35;font-size:14px}
    .director-user{align-self:flex-end;background:#242935}
    .director-system{align-self:flex-start;background:#181b22;color:#d7dbe3}
    .director-compose{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;margin-top:8px}
    .director-compose textarea{width:100%;min-height:68px;resize:vertical;border:1px solid #414551;border-radius:8px;background:#0d0f13;color:#f4f4f5;padding:9px;font:inherit}
    .director-help{margin-top:8px;color:#9fa6b3;font-size:12px;line-height:1.45}
  `;
  document.head.appendChild(style);

  const panel = document.createElement('section');
  panel.className = 'director-panel';
  panel.innerHTML = `
    <div class="director-head">
      <div><strong>Chat co-editor</strong><br><small id="director-mode">Direct reel editing active</small></div>
      <button id="director-clear" type="button">Clear chat</button>
    </div>
    <div id="director-log" class="director-log" aria-live="polite"></div>
    <div class="director-compose">
      <textarea id="director-input" placeholder="Tell the editor what to change. Example: Move GR left 10%, make him smaller, duplicate this frame, hold 4, insert Walk."></textarea>
      <button id="director-send" type="button">Do it</button>
    </div>
    <div class="director-help">Edits go straight into the current scene/reel. Enter sends; Shift+Enter makes a new line. A provider-neutral AI bridge can use the same action API later.</div>
  `;
  framePanel.insertAdjacentElement('afterend', panel);

  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
  const normalize = (s) => String(s || '').trim().replace(/\s+/g, ' ');

  function say(kind, text) {
    const log = $('director-log');
    if (!log) return;
    const row = document.createElement('div');
    row.className = `director-msg ${kind === 'user' ? 'director-user' : 'director-system'}`;
    row.textContent = text;
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
  }

  function selectedAsset() {
    return A.state.assets.find((asset) => asset.id === A.state.selectedAssetId) || null;
  }

  function findAsset(text) {
    const lower = text.toLowerCase();
    const candidates = A.state.assets
      .map((asset) => ({ asset, name: String(asset.name || '').replace(/\.[^.]+$/, '').toLowerCase() }))
      .filter(({ name }) => name && lower.includes(name))
      .sort((a, b) => b.name.length - a.name.length);
    return candidates[0]?.asset || null;
  }

  function ensureAsset(text) {
    const named = findAsset(text);
    if (named) A.selectAsset(named.id);
    return named || selectedAsset();
  }

  function capture(message) {
    A.renderAll();
    R.captureCurrent();
    A.onion?.render?.();
    A.status(message);
    return message;
  }

  function setHold(value) {
    const hold = clamp(Math.round(Number(value) || 1), 1, 12);
    R.activeFrame.hold = hold;
    if ($('frame-hold')) $('frame-hold').value = String(hold);
    if ($('frame-hold-value')) $('frame-hold-value').textContent = `${hold}x`;
    R.renderReel();
    A.status(`Frame ${R.activeIndex + 1} hold = ${hold}`);
    return `Set frame ${R.activeIndex + 1} to a ${hold}x hold.`;
  }

  function gotoFrame(value) {
    const target = clamp(Math.round(Number(value) || 1), 1, R.frames.length) - 1;
    R.restore(target);
    return `Opened frame ${target + 1}.`;
  }

  function duplicateFrames(count = 1) {
    R.captureCurrent();
    const n = clamp(Math.round(Number(count) || 1), 1, 50);
    const source = A.clone(R.activeFrame);
    const at = R.activeIndex + 1;
    const copies = Array.from({ length: n }, () => ({ ...A.clone(source), id: A.uid('frame') }));
    const next = [...R.frames.slice(0, at), ...copies, ...R.frames.slice(at)];
    R.setFrames(next, at + n - 1);
    A.status(`${n} duplicate frame${n === 1 ? '' : 's'} added`);
    return `Duplicated the current frame ${n} time${n === 1 ? '' : 's'}.`;
  }

  function deleteCurrentFrame() {
    if (R.frames.length <= 1) return 'I kept the only reel frame; the reel cannot be empty.';
    const next = R.frames.filter((_, i) => i !== R.activeIndex).map((frame) => A.clone(frame));
    R.setFrames(next, Math.min(R.activeIndex, next.length - 1));
    return 'Deleted the current frame.';
  }

  function setFps(value) {
    const fps = clamp(Math.round(Number(value) || 24), 1, 60);
    if ($('fps-control')) {
      $('fps-control').value = String(fps);
      $('fps-control').dispatchEvent(new Event('input', { bubbles: true }));
    }
    return `Set playback to ${fps} fps.`;
  }

  function moveAsset(text) {
    const asset = ensureAsset(text);
    if (!asset) return null;
    const numberMatch = text.match(/(-?\d+(?:\.\d+)?)\s*%?/);
    const amount = clamp(Math.abs(Number(numberMatch?.[1] || 5)) / 100, 0.005, 0.5);
    let changed = false;
    if (/\bleft\b/i.test(text)) { asset.x = clamp(asset.x - amount, 0, 1); changed = true; }
    if (/\bright\b/i.test(text)) { asset.x = clamp(asset.x + amount, 0, 1); changed = true; }
    if (/\b(up|farther|back)\b/i.test(text)) { asset.groundY = clamp(asset.groundY - amount, 0.1, 0.98); changed = true; }
    if (/\b(down|closer|forward)\b/i.test(text)) { asset.groundY = clamp(asset.groundY + amount, 0.1, 0.98); changed = true; }
    if (!changed) return null;
    return capture(`Moved ${asset.name}`);
  }

  function scaleAsset(text) {
    const asset = ensureAsset(text);
    if (!asset) return null;
    const numberMatch = text.match(/(-?\d+(?:\.\d+)?)\s*%/);
    const pct = clamp(Math.abs(Number(numberMatch?.[1] || 10)) / 100, 0.01, 2);
    if (/\b(bigger|larger|grow|increase|closer)\b/i.test(text)) asset.manualScale = clamp(asset.manualScale * (1 + pct), 0.25, 2);
    else if (/\b(smaller|shrink|decrease|farther)\b/i.test(text)) asset.manualScale = clamp(asset.manualScale * (1 - pct), 0.25, 2);
    else return null;
    capture(`Scaled ${asset.name}`);
    return `${asset.name} scale is now ${asset.manualScale.toFixed(2)}.`;
  }

  function setAssetValues(text) {
    const asset = ensureAsset(text);
    if (!asset) return null;
    const x = text.match(/\bx\s*(?:=|to)?\s*(0(?:\.\d+)?|1(?:\.0+)?)/i);
    const depth = text.match(/\b(?:depth|ground|y)\s*(?:=|to)?\s*(0(?:\.\d+)?|1(?:\.0+)?)/i);
    const scale = text.match(/\bscale\s*(?:=|to)?\s*(\d+(?:\.\d+)?)/i);
    if (!x && !depth && !scale) return null;
    if (x) asset.x = clamp(Number(x[1]), 0, 1);
    if (depth) asset.groundY = clamp(Number(depth[1]), 0.1, 0.98);
    if (scale) asset.manualScale = clamp(Number(scale[1]), 0.25, 2);
    capture(`Placed ${asset.name}`);
    return `Placed ${asset.name}: x ${asset.x.toFixed(2)}, depth ${asset.groundY.toFixed(2)}, scale ${asset.manualScale.toFixed(2)}.`;
  }

  function insertMotion(text) {
    if (!A.motionLibrary) return null;
    const library = A.motionLibrary.library;
    const slot = text.match(/\bslot\s*(\d+)/i);
    let index = slot ? Number(slot[1]) - 1 : -1;
    if (index < 0) {
      index = library.sequences.findIndex((seq) => text.toLowerCase().includes(String(seq.name || '').toLowerCase()));
    }
    if (index < 0 || !library.sequences[index]) return null;
    const name = library.sequences[index].name;
    A.motionLibrary.insertSequence(index);
    return `Inserted motion sequence “${name}” after the current frame.`;
  }

  function localCommand(raw) {
    const text = normalize(raw);
    const lower = text.toLowerCase();
    if (!text) return 'Tell me what you want changed.';

    let m;
    if ((m = lower.match(/(?:go to|open|frame)\s+(\d+)\b/)) && /(?:go to|open|^frame)/.test(lower)) return gotoFrame(m[1]);
    if (/\b(next frame|frame next)\b/.test(lower)) return gotoFrame(R.activeIndex + 2);
    if (/\b(previous frame|prev frame|frame back)\b/.test(lower)) return gotoFrame(R.activeIndex);
    if ((m = lower.match(/\b(?:fps|frame rate)\s*(?:=|to)?\s*(\d+)/))) return setFps(m[1]);
    if ((m = lower.match(/\bhold(?: this frame)?\s*(?:=|for|to)?\s*(\d+)/))) return setHold(m[1]);
    if ((m = lower.match(/\bduplicate(?: this| current)? frame(?:\s+(\d+)\s*(?:times?)?)?/))) return duplicateFrames(m[1] || 1);
    if ((m = lower.match(/\brepeat(?: this| current)? frame\s+(\d+)\s*(?:times?)?/))) return duplicateFrames(m[1]);
    if (/\b(delete|remove) (?:this |current )?frame\b/.test(lower)) return deleteCurrentFrame();
    if (/\b(add|new) frame\b/.test(lower)) { R.insertAt(R.frames.length, R.makeFrame(), true); return 'Added a new frame at the end of the reel.'; }
    if (/\b(play|preview reel)\b/.test(lower)) { $('play-button')?.click(); return 'Playback toggled.'; }
    if (/\bcopy pose (?:to )?(?:the )?next\b/.test(lower)) { $('copy-pose-next')?.click(); return 'Copied the selected pose to the next frame.'; }
    if (/\bcopy pose (?:to )?(?:the )?(?:previous|prev)\b/.test(lower)) { $('copy-pose-prev')?.click(); return 'Copied the selected pose to the previous frame.'; }
    if (/\b(insert|use|add)\b/.test(lower)) {
      const result = insertMotion(text);
      if (result) return result;
    }
    if (/\b(select|choose)\b/.test(lower)) {
      const asset = findAsset(text);
      if (asset) { A.selectAsset(asset.id); return `Selected ${asset.name}.`; }
    }

    const exactPlacement = setAssetValues(text);
    if (exactPlacement) return exactPlacement;
    if (/\b(bigger|larger|grow|increase|smaller|shrink|decrease)\b/.test(lower)) {
      const result = scaleAsset(text);
      if (result) return result;
    }
    if (/\b(left|right|up|down|forward|back|farther|closer)\b/.test(lower)) {
      const result = moveAsset(text);
      if (result) return result;
    }

    return 'I did not change the reel because I could not map that request to a safe edit yet. Try a concrete edit such as “move GR left 10%”, “hold 4”, “duplicate this frame 3 times”, or “insert Walk”.';
  }

  async function execute(raw) {
    const text = normalize(raw);
    if (!text) return;
    say('user', text);
    const input = $('director-input');
    if (input) input.value = '';

    try {
      if (typeof window.OneWaveDirectorBridge === 'function') {
        $('director-mode').textContent = 'External AI bridge connected';
        const result = await window.OneWaveDirectorBridge({
          text,
          state: A.snapshot(),
          frameIndex: R.activeIndex,
          frameCount: R.frames.length,
          actions: A.director?.actions
        });
        if (result?.command) {
          const reply = localCommand(result.command);
          say('system', result.reply ? `${result.reply}\n${reply}` : reply);
          return;
        }
        if (result?.reply) { say('system', result.reply); return; }
      }

      const reply = localCommand(text);
      say('system', reply);
    } catch (error) {
      console.error(error);
      say('system', `Edit failed: ${error.message}`);
      A.status(`Chat edit failed: ${error.message}`);
    }
  }

  const actions = Object.freeze([
    'select asset by name', 'move selected/named asset left/right/up/down', 'set x/depth/scale',
    'make selected/named asset bigger/smaller', 'go to frame', 'next/previous frame', 'set hold',
    'duplicate/repeat frame', 'add/delete frame', 'set fps', 'copy pose next/previous',
    'insert motion-library sequence by name or slot', 'toggle playback'
  ]);

  A.director = { execute, localCommand, actions };

  $('director-send')?.addEventListener('click', () => execute($('director-input')?.value));
  $('director-input')?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      execute(event.currentTarget.value);
    }
  });
  $('director-clear')?.addEventListener('click', () => { if ($('director-log')) $('director-log').innerHTML = ''; });

  say('system', 'Ready. I edit the current reel directly. Try: “move GR left 10%”, “make him smaller”, “hold 4”, “duplicate this frame”, or “insert Walk”.');
})();
