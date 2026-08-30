(() => {
  'use strict';
  const A = window.Animator;
  if (!A) throw new Error('C21 requires Animator');

  const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));
  const normalize = (value) => String(value || '').trim().toLowerCase();

  function getLibrary() {
    return A.motionLibrary?.library || { sequences: [] };
  }

  function sequenceIndexFor(action, actor = '') {
    const wanted = normalize(action);
    const who = normalize(actor);
    const sequences = getLibrary().sequences || [];
    let best = -1;
    let score = -1;
    sequences.forEach((seq, index) => {
      const name = normalize(seq.name);
      const tag = normalize(seq.characterTag);
      let next = 0;
      if (name === wanted) next += 8;
      if (name.includes(wanted) || wanted.includes(name)) next += 5;
      if (who && tag === who) next += 4;
      else if (who && tag && (tag.includes(who) || who.includes(tag))) next += 2;
      if (next > score) { score = next; best = index; }
    });
    return score >= 5 ? best : -1;
  }

  function splitActions(text) {
    return String(text || '')
      .replace(/[.!?]+/g, ' and ')
      .split(/\b(?:and then|then|and|,)\b/i)
      .map((part) => part.trim())
      .filter(Boolean);
  }

  function inferActor(text, fallback = '') {
    const m = String(text || '').match(/^\s*(?:have\s+)?([A-Za-z0-9_-]+)\s+(?:to\s+)?/i);
    return m ? m[1] : fallback;
  }

  function inferAction(clause) {
    const t = normalize(clause);
    const known = [
      ['walk toward', 'walk toward'], ['walk away', 'walk away'], ['run toward', 'run toward'], ['run away', 'run away'],
      ['scurry', 'scurry'], ['kick', 'kick'], ['jump', 'jump'], ['run', 'run'], ['walk', 'walk'],
      ['look', 'look'], ['pick', 'pick up'], ['sniff', 'sniff'], ['stop', 'stop']
    ];
    for (const [needle, action] of known) if (t.includes(needle)) return action;
    return '';
  }

  function inferTarget(clause, action) {
    const raw = String(clause || '').trim();
    if (!action) return '';
    const rx = new RegExp(`\\b${action.replace(/\s+/g, '\\s+')}\\b\\s+(?:at|to|toward|towards|over|into|from)?\\s*(.*)$`, 'i');
    const m = raw.match(rx);
    return m ? m[1].replace(/^(?:the|a|an)\s+/i, '').trim() : '';
  }

  function planMotion(text, context) {
    const clauses = splitActions(text);
    const steps = [];
    const missing = [];
    let actor = inferActor(clauses[0], '');

    clauses.forEach((clause, order) => {
      const nextActor = inferActor(clause, actor);
      if (nextActor) actor = nextActor;
      const action = inferAction(clause);
      if (!action) return;
      const target = inferTarget(clause, action);
      const index = sequenceIndexFor(action, actor);
      if (index >= 0) {
        steps.push({
          operation: 'insert_motion',
          args: { index },
          meta: { order, actor, action, target, source: 'motion-library' }
        });
      } else {
        missing.push({ order, actor, action, target, kind: 'motion' });
      }
    });

    return {
      type: 'scene-plan',
      sourceText: text,
      frame: context?.frame || 1,
      steps,
      missing,
      complete: missing.length === 0,
      message: missing.length
        ? `Plan built: ${steps.length} motion step${steps.length === 1 ? '' : 's'} ready; ${missing.length} motion asset${missing.length === 1 ? '' : 's'} missing.`
        : `Plan built: ${steps.length} motion step${steps.length === 1 ? '' : 's'} ready.`
    };
  }

  function queueAsset(job) {
    const key = 'onewave-asset-worker-queue-v1';
    let queue = [];
    try { queue = JSON.parse(localStorage.getItem(key) || '[]'); } catch (_) { queue = []; }
    const item = {
      id: `asset-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      status: 'needed',
      createdAt: new Date().toISOString(),
      kind: job.kind || 'asset',
      prompt: job.prompt || '',
      frame: job.frame || 1,
      projectVersion: job.project?.version || null
    };
    queue.push(item);
    if (queue.length > 100) queue = queue.slice(-100);
    try { localStorage.setItem(key, JSON.stringify(queue)); } catch (_) {}
    window.dispatchEvent(new CustomEvent('onewave-asset-needed', { detail: clone(item) }));
    return item;
  }

  window.oneWaveDirectorWorker = async ({ request, context }) => {
    const text = String(request?.text || request?.raw || '').trim();
    if (!text) return { type: 'scene-plan', steps: [], missing: [], complete: false, message: 'Director worker received no scene request.' };
    return planMotion(text, context || {});
  };

  window.oneWaveAssetWorker = async (job) => {
    const item = queueAsset(job || {});
    return {
      pending: true,
      worker: 'local-asset-queue',
      request: item,
      message: `Asset worker queued ${item.kind}: ${item.prompt}`
    };
  };

  A.workers = {
    director: window.oneWaveDirectorWorker,
    asset: window.oneWaveAssetWorker,
    planMotion,
    sequenceIndexFor,
    get assetQueue() {
      try { return JSON.parse(localStorage.getItem('onewave-asset-worker-queue-v1') || '[]'); }
      catch (_) { return []; }
    }
  };

  A.status('Real local workers ready');
})();
