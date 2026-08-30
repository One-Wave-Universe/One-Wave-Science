(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.control) throw new Error('C20 requires Animator control API');

  const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));
  const normalize = (value) => String(value || '').trim().toLowerCase();
  const words = (value) => normalize(value).split(/[^a-z0-9]+/).filter(Boolean);
  const clampInt = (value, min, max) => Math.max(min, Math.min(max, Math.round(Number(value) || min)));

  const Cells = {
    parse(text) {
      const raw = String(text || '').trim();
      const t = raw.toLowerCase();
      let m;
      if (/^(play|play it|preview)$/.test(t)) return { type: 'control', operation: 'play', args: {} };
      if (/^(stop|stop playback|stop it)$/.test(t)) return { type: 'control', operation: 'stop', args: {} };
      if (/^(duplicate|duplicate frame|copy frame)$/.test(t)) return { type: 'control', operation: 'duplicate_frame', args: {} };
      if (/^(add frame|new frame|add a frame)$/.test(t)) return { type: 'control', operation: 'add_frame', args: {} };
      if (/^(delete frame|remove frame|delete this frame)$/.test(t)) return { type: 'control', operation: 'delete_frame', args: {} };
      if (/^(undo|undo that|go back)$/.test(t)) return { type: 'control', operation: 'undo', args: {} };
      if ((m = t.match(/(?:go to|show|select)?\s*frame\s*(\d+)/))) return { type: 'control', operation: 'select_frame', args: { frame: Number(m[1]) } };
      if ((m = t.match(/(?:hold|set hold(?: to)?)\s*(\d+)/))) return { type: 'control', operation: 'set_hold', args: { hold: Number(m[1]) } };
      if ((m = t.match(/(?:fps|set fps(?: to)?)\s*(\d+)/))) return { type: 'control', operation: 'set_fps', args: { fps: Number(m[1]) } };
      if ((m = raw.match(/(?:save|capture)\s+frames?\s+(\d+)\s+(?:to|through|-)\s*(\d+)\s+(?:as|to)\s+(.+)/i))) {
        return { type: 'control', operation: 'capture_motion', args: { start: Number(m[1]), end: Number(m[2]), name: m[3].trim() } };
      }
      if (/^(load|add|choose) background(?: png)?$/i.test(raw)) return { type: 'picker', target: 'background-picker', message: 'Choose the background PNG.' };
      if (/^(add|load|choose) prop(?: png)?$/i.test(raw)) return { type: 'picker', target: 'prop-picker', message: 'Choose the prop PNG.' };
      if (/^(add|load|choose) character(?: png)?$/i.test(raw)) return { type: 'picker', target: 'character-picker', message: 'Choose the character PNG.' };
      if ((m = raw.match(/^\s*(?:create|make|generate)\s+(?:a\s+|an\s+)?(background|prop|character|motion(?:\s+pose)?)\s*(?::|-)?\s*(.+)$/i))) {
        const sourceKind = m[1].toLowerCase();
        return { type: 'generate', kind: sourceKind.startsWith('motion') ? 'character' : sourceKind, prompt: m[2].trim(), motionPose: sourceKind.startsWith('motion') };
      }
      if (/make (?:this|it) faster/i.test(raw)) return { type: 'adjust-hold', delta: -1 };
      if (/make (?:this|it) slower/i.test(raw)) return { type: 'adjust-hold', delta: 1 };
      return { type: 'scene', raw };
    }
  };

  const Nerves = {
    emit(name, detail) { window.dispatchEvent(new CustomEvent(name, { detail })); },
    click(id) {
      const el = document.getElementById(id);
      if (!el) throw new Error(`Control missing: ${id}`);
      el.click();
    }
  };

  // The human and attached assistant can both originate ideas and edits.
  // Director is an interface role, not a separate fake brain.
  const DirectorPort = {
    worker: null,
    attach(worker) {
      if (typeof worker !== 'function') throw new Error('Director worker must be a function');
      DirectorPort.worker = worker;
      window.oneWaveDirectorWorker = worker;
      Nerves.emit('onewave-director-attached', { attached: true });
      A.status('Director worker attached');
      return true;
    },
    detach() {
      DirectorPort.worker = null;
      if (window.oneWaveDirectorWorker) delete window.oneWaveDirectorWorker;
      Nerves.emit('onewave-director-attached', { attached: false });
      A.status('Director worker detached');
    },
    get attached() {
      return typeof (DirectorPort.worker || window.oneWaveDirectorWorker) === 'function';
    },
    async request(request, context) {
      const worker = DirectorPort.worker || window.oneWaveDirectorWorker;
      if (typeof worker === 'function') return worker({ request: clone(request), context: clone(context), control: A.control });
      const envelope = {
        id: `director-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        request: clone(request),
        context: clone(context),
        operations: [...A.control.operations]
      };
      Nerves.emit('onewave-director-request', envelope);
      return { pending: true, stage: 'Director', envelope, message: 'Director request ready for an attached assistant.' };
    }
  };

  // Dream automates routine creative preparation. It reuses known motion first,
  // then surfaces only unresolved creative gaps for a human/AI choice or asset worker.
  const Dream = {
    motionSequences(context) {
      return Array.isArray(context?.motionLibrary?.sequences) ? context.motionLibrary.sequences : [];
    },
    scoreMotion(need, sequence) {
      const wantedAction = normalize(need?.action);
      const wantedActor = normalize(need?.actor);
      const wantedTarget = normalize(need?.target);
      const name = normalize(sequence?.name);
      const tag = normalize(sequence?.characterTag);
      const haystack = new Set(words(`${name} ${tag}`));
      let score = 0;

      if (wantedAction && name === wantedAction) score += 12;
      else if (wantedAction && (name.includes(wantedAction) || wantedAction.includes(name))) score += 8;
      for (const token of words(wantedAction)) if (haystack.has(token)) score += 2;

      if (wantedActor && tag === wantedActor) score += 7;
      else if (wantedActor && tag && (tag.includes(wantedActor) || wantedActor.includes(tag))) score += 4;

      for (const token of words(wantedTarget)) if (haystack.has(token)) score += 1;
      return score;
    },
    bestMotion(need, context) {
      const sequences = Dream.motionSequences(context);
      let best = null;
      sequences.forEach((sequence, index) => {
        const score = Dream.scoreMotion(need, sequence);
        if (!best || score > best.score) best = { index, sequence, score };
      });
      return best && best.score >= 8 ? best : null;
    },
    preparePlan(plan, context) {
      const next = clone(plan || {});
      next.steps = Array.isArray(next.steps) ? next.steps : [];
      const missing = Array.isArray(next.missing) ? next.missing : [];
      const unresolved = [];
      const reused = [];

      for (const need of missing) {
        if ((need?.kind || 'motion') === 'motion') {
          const match = Dream.bestMotion(need, context);
          if (match) {
            const step = {
              operation: 'insert_motion',
              args: { index: match.index },
              meta: {
                automatic: true,
                source: 'Dream:motion-library',
                actor: need.actor || '',
                action: need.action || '',
                target: need.target || '',
                matchName: match.sequence?.name || '',
                matchScore: match.score
              }
            };
            next.steps.push(step);
            reused.push({ need: clone(need), index: match.index, name: match.sequence?.name || '', score: match.score });
            continue;
          }
        }
        unresolved.push(need);
      }

      next.missing = unresolved;
      next.automatic = { ...(next.automatic || {}), reusedMotion: reused };
      return next;
    },
    async requestAsset(request, context) {
      const job = {
        type: 'create-asset',
        kind: request.kind,
        prompt: request.prompt,
        frame: context.frame,
        project: context.project,
        requestedAt: context.time
      };
      if (typeof window.oneWaveAssetWorker === 'function') return window.oneWaveAssetWorker(job);
      Nerves.emit('onewave-asset-request', job);
      return { pending: true, stage: 'Dream', job, message: `Asset request ready: ${request.kind} — ${request.prompt}` };
    },
    support(plan, context) {
      const missing = Array.isArray(plan?.missing) ? plan.missing : [];
      const seen = new Set();
      const suggestions = [];
      for (const need of missing) {
        const prompt = [need.actor, need.action, need.target].filter(Boolean).join(' ').trim();
        const kind = need.kind || 'motion';
        const key = `${kind}|${normalize(prompt)}|${plan?.frame || context.frame}`;
        if (seen.has(key)) continue;
        seen.add(key);
        suggestions.push({ kind, prompt, frame: plan?.frame || context.frame });
      }
      return { missing, suggestions };
    }
  };

  // Administrator automates routine supervision: normalize safe values, validate
  // continuity-sensitive operations, approve execution, then audit executor results.
  const Administrator = {
    evaluate(parsed, context) {
      if (!parsed) return { ok: false, reason: 'Nothing parsed' };
      if (parsed.type === 'control' && !A.control.operations.includes(parsed.operation)) return { ok: false, reason: `Unsupported operation: ${parsed.operation}` };
      if (parsed.type === 'generate' && !parsed.prompt) return { ok: false, reason: 'Generation prompt is empty' };
      if (parsed.type === 'control' && parsed.operation === 'capture_motion' && parsed.args.end < parsed.args.start) return { ok: false, reason: 'Motion end frame is before start frame' };
      if (parsed.type === 'control' && parsed.operation === 'delete_frame') {
        const count = Number(context?.project?.frames?.length || 0);
        if (count <= 1) return { ok: false, reason: 'Cannot delete the only frame' };
      }
      return { ok: true };
    },
    normalizeStep(step, context) {
      const next = clone(step || {});
      next.args = next.args || {};
      if (next.operation === 'set_hold') next.args.hold = clampInt(next.args.hold, 1, 12);
      if (next.operation === 'set_fps') next.args.fps = clampInt(next.args.fps, 1, 60);
      if (next.operation === 'select_frame') next.args.frame = Math.round(Number(next.args.frame));
      if (next.operation === 'capture_motion') {
        next.args.start = Math.round(Number(next.args.start));
        next.args.end = Math.round(Number(next.args.end));
        next.args.name = String(next.args.name || '').trim();
      }
      if (next.operation === 'insert_motion') next.args.index = Math.round(Number(next.args.index));
      return next;
    },
    preparePlan(plan, context) {
      const next = clone(plan || {});
      const rawSteps = Array.isArray(next.steps) ? next.steps : [];
      const normalized = rawSteps.map((step) => Administrator.normalizeStep(step, context));
      const steps = [];
      let previousKey = '';
      for (const step of normalized) {
        const key = JSON.stringify({ operation: step.operation, args: step.args || {} });
        if (key === previousKey && ['select_frame', 'set_hold', 'set_fps'].includes(step.operation)) continue;
        steps.push(step);
        previousKey = key;
      }
      next.steps = steps;
      return next;
    },
    evaluatePlan(plan, context) {
      if (!plan || !Array.isArray(plan.steps)) return { ok: false, reason: 'Director did not return an executable step list' };
      const frameCount = Number(context.project?.frames?.length || 0);
      const motionCount = Number(context.motionLibrary?.sequences?.length || 0);

      for (const step of plan.steps) {
        if (!step?.operation || !A.control.operations.includes(step.operation)) return { ok: false, reason: `Unsupported planned operation: ${step?.operation || 'missing'}` };

        if (step.operation === 'select_frame') {
          const frame = Number(step.args?.frame);
          if (!Number.isInteger(frame) || frame < 1 || frame > frameCount) return { ok: false, reason: `Planned frame ${step.args?.frame} does not exist` };
        }

        if (step.operation === 'capture_motion') {
          const start = Number(step.args?.start);
          const end = Number(step.args?.end);
          if (!Number.isInteger(start) || !Number.isInteger(end) || start < 1 || end < start || end > frameCount) return { ok: false, reason: `Invalid capture range ${start}-${end}` };
          if (!String(step.args?.name || '').trim()) return { ok: false, reason: 'Captured motion needs a name' };
        }

        if (step.operation === 'insert_motion') {
          const index = Number(step.args?.index);
          if (!Number.isInteger(index) || index < 0 || index >= motionCount) return { ok: false, reason: `Motion library index ${step.args?.index} does not exist` };
        }

        if (step.operation === 'delete_frame' && frameCount <= 1) return { ok: false, reason: 'Cannot delete the only frame' };
      }
      return { ok: true };
    },
    auditExecution(results) {
      const failures = [];
      for (const item of results || []) {
        const result = item?.result;
        if (result?.ok === false || result?.error) failures.push({ step: item.step, result });
      }
      return failures.length
        ? { ok: false, failures, reason: `${failures.length} executor operation${failures.length === 1 ? '' : 's'} reported failure` }
        : { ok: true, failures: [] };
    },
    acceptAssets(result) {
      const assets = Array.isArray(result?.assets) ? result.assets : (result?.asset ? [result.asset] : []);
      return assets.map((asset) => {
        if (!asset?.src) throw new Error('Generated asset has no image data');
        const kind = normalize(asset.kind);
        if (!['background', 'character', 'prop'].includes(kind)) throw new Error(`Unsupported generated asset kind: ${asset.kind || 'missing'}`);
        if (kind === 'background') return A.control.call('set_background', { src: asset.src, name: asset.name });
        if (kind === 'character') return A.control.call('add_character', { src: asset.src, name: asset.name, placement: asset.placement });
        return A.control.call('add_prop', { src: asset.src, name: asset.name, placement: asset.placement });
      });
    }
  };

  const M4 = {
    async context() {
      return {
        frame: (A.reel?.activeIndex ?? 0) + 1,
        time: new Date().toISOString(),
        project: await A.control.call('get_project').then((r) => r.result),
        scene: await A.control.call('get_scene').then((r) => r.result),
        motionLibrary: await A.control.call('get_motion_library').then((r) => r.result),
        operations: [...A.control.operations]
      };
    },
    async executePlan(plan, context) {
      const dreamPrepared = Dream.preparePlan(plan, context);
      const prepared = Administrator.preparePlan(dreamPrepared, context);
      const verdict = Administrator.evaluatePlan(prepared, context);
      if (!verdict.ok) return { ok: false, stage: 'Administrator', message: verdict.reason, plan: prepared };

      const results = [];
      for (const step of prepared.steps) results.push({ step, result: await A.control.call(step.operation, step.args || {}) });

      const audit = Administrator.auditExecution(results);
      if (!audit.ok) return { ok: false, stage: 'Administrator', message: audit.reason, plan: prepared, results, failures: audit.failures };

      const support = Dream.support(prepared, context);
      const assetRequests = [];
      for (const request of support.suggestions) assetRequests.push(await Dream.requestAsset(request, context));

      const reused = prepared.automatic?.reusedMotion?.length || 0;
      const summary = [];
      if (results.length) summary.push(`${results.length} step${results.length === 1 ? '' : 's'} executed`);
      if (reused) summary.push(`${reused} motion${reused === 1 ? '' : 's'} reused automatically`);
      if (support.missing.length) summary.push(`${support.missing.length} unresolved creative gap${support.missing.length === 1 ? '' : 's'} surfaced`);

      return {
        ok: results.length > 0 || support.missing.length > 0,
        stage: support.missing.length ? 'Dream' : 'Administrator',
        plan: prepared,
        results,
        missing: support.missing,
        assetRequests,
        audit,
        message: summary.length ? `${summary.join('; ')}.` : 'Plan checked; no executable work was needed.'
      };
    },
    async route(text) {
      const parsed = Cells.parse(text);
      const context = await M4.context();
      const verdict = Administrator.evaluate(parsed, context);
      if (!verdict.ok) return { ok: false, stage: 'Administrator', message: verdict.reason };

      if (parsed.type === 'control') {
        const step = Administrator.normalizeStep({ operation: parsed.operation, args: parsed.args || {} }, context);
        const planVerdict = Administrator.evaluatePlan({ steps: [step] }, context);
        if (!planVerdict.ok) return { ok: false, stage: 'Administrator', message: planVerdict.reason };
        const result = await A.control.call(step.operation, step.args || {});
        const audit = Administrator.auditExecution([{ step, result }]);
        return audit.ok
          ? { ok: true, stage: 'Administrator', parsed, result, message: `${step.operation} complete and checked` }
          : { ok: false, stage: 'Administrator', parsed, result, message: audit.reason };
      }

      if (parsed.type === 'picker') {
        Nerves.click(parsed.target);
        return { ok: true, stage: 'Nerves', parsed, message: parsed.message };
      }

      if (parsed.type === 'adjust-hold') {
        const current = Number(document.getElementById('frame-hold')?.value || 2);
        const hold = clampInt(current + parsed.delta, 1, 12);
        const step = { operation: 'set_hold', args: { hold } };
        const result = await A.control.call(step.operation, step.args);
        const audit = Administrator.auditExecution([{ step, result }]);
        return audit.ok
          ? { ok: true, stage: 'Administrator', parsed, result, message: `Hold ${hold}x — checked` }
          : { ok: false, stage: 'Administrator', parsed, result, message: audit.reason };
      }

      if (parsed.type === 'generate') {
        const generated = await Dream.requestAsset(parsed, context);
        if (generated?.asset || generated?.assets) await Promise.all(Administrator.acceptAssets(generated));
        return { ok: true, stage: 'Dream', parsed, generated, message: generated?.message || 'Asset request sent' };
      }

      const planned = await DirectorPort.request({ text, parsed }, context);
      if (planned?.pending) return { ok: false, stage: 'Director', pending: true, message: planned.message, envelope: planned.envelope };
      if (Array.isArray(planned?.steps)) return M4.executePlan(planned, context);
      if (planned?.asset || planned?.assets) {
        await Promise.all(Administrator.acceptAssets(planned));
        return { ok: true, stage: 'Administrator', message: planned.message || 'Asset accepted and checked' };
      }
      return { ok: false, stage: 'Director', message: 'Attached Director worker returned no executable plan.' };
    }
  };

  // Non-destructive worker checks available from the console or future UI diagnostics.
  const selfTest = () => {
    const fakeContext = {
      project: { frames: [{}, {}, {}] },
      motionLibrary: { sequences: [{ name: 'run', characterTag: 'GR' }, { name: 'kick can', characterTag: 'GR' }] }
    };
    const checks = [
      { name: 'Cells parse FPS', pass: Cells.parse('fps 24')?.operation === 'set_fps' },
      { name: 'Dream reuses matching motion', pass: Dream.bestMotion({ kind: 'motion', actor: 'GR', action: 'run' }, fakeContext)?.index === 0 },
      { name: 'Administrator blocks bad frame', pass: Administrator.evaluatePlan({ steps: [{ operation: 'select_frame', args: { frame: 9 } }] }, fakeContext).ok === false },
      { name: 'Administrator clamps FPS', pass: Administrator.normalizeStep({ operation: 'set_fps', args: { fps: 1000 } }, fakeContext).args.fps === 60 }
    ];
    const result = { ok: checks.every((check) => check.pass), checks };
    Nerves.emit('onewave-architecture-self-test', clone(result));
    return result;
  };

  A.architecture = { Cells, Nerves, M4, Dream, Administrator, DirectorPort, selfTest };
  A.directorPort = DirectorPort;
  window.OneWaveArchitecture = A.architecture;
  window.OneWaveDirectorPort = DirectorPort;
  A.status('Delegation ready — Dream prep and Administrator checks are automatic');
})();