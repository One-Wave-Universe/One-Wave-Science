(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.control) throw new Error('C20 requires Animator control API');

  const clone = (value) => A.clone ? A.clone(value) : JSON.parse(JSON.stringify(value));

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

  // The human + attached assistant are the high-level workers.
  // This port deliberately does not invent a scene plan on its own.
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

  // Dream is thin creative support. The creative source is normally the user.
  const Dream = {
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
      return {
        missing,
        suggestions: missing.map((need) => ({
          kind: need.kind || 'motion',
          prompt: [need.actor, need.action, need.target].filter(Boolean).join(' ').trim(),
          frame: plan?.frame || context.frame
        }))
      };
    }
  };

  // Administrator is thin supervision: validate, protect continuity, approve executable work.
  const Administrator = {
    evaluate(parsed) {
      if (!parsed) return { ok: false, reason: 'Nothing parsed' };
      if (parsed.type === 'control' && !A.control.operations.includes(parsed.operation)) return { ok: false, reason: `Unsupported operation: ${parsed.operation}` };
      if (parsed.type === 'generate' && !parsed.prompt) return { ok: false, reason: 'Generation prompt is empty' };
      if (parsed.type === 'control' && parsed.operation === 'capture_motion' && parsed.args.end < parsed.args.start) return { ok: false, reason: 'Motion end frame is before start frame' };
      return { ok: true };
    },
    evaluatePlan(plan, context) {
      if (!plan || !Array.isArray(plan.steps)) return { ok: false, reason: 'Director did not return an executable step list' };
      for (const step of plan.steps) {
        if (!step?.operation || !A.control.operations.includes(step.operation)) return { ok: false, reason: `Unsupported planned operation: ${step?.operation || 'missing'}` };
        if (step.operation === 'select_frame') {
          const frame = Number(step.args?.frame);
          const count = Number(context.project?.frames?.length || 0);
          if (!Number.isInteger(frame) || frame < 1 || frame > count) return { ok: false, reason: `Planned frame ${step.args?.frame} does not exist` };
        }
      }
      return { ok: true };
    },
    acceptAssets(result) {
      const assets = Array.isArray(result?.assets) ? result.assets : (result?.asset ? [result.asset] : []);
      return assets.map((asset) => {
        if (!asset?.src) throw new Error('Generated asset has no image data');
        if (asset.kind === 'background') return A.control.call('set_background', { src: asset.src, name: asset.name });
        if (asset.kind === 'character') return A.control.call('add_character', { src: asset.src, name: asset.name, placement: asset.placement });
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
      const verdict = Administrator.evaluatePlan(plan, context);
      if (!verdict.ok) return { ok: false, stage: 'Administrator', message: verdict.reason, plan };
      const results = [];
      for (const step of plan.steps) results.push({ step, result: await A.control.call(step.operation, step.args || {}) });

      const support = Dream.support(plan, context);
      for (const request of support.suggestions) await Dream.requestAsset(request, context);

      return {
        ok: results.length > 0 || support.missing.length > 0,
        stage: support.missing.length ? 'Dream' : 'Executor',
        plan,
        results,
        missing: support.missing,
        message: support.missing.length
          ? `${results.length} step${results.length === 1 ? '' : 's'} executed; ${support.missing.length} missing asset request${support.missing.length === 1 ? '' : 's'} surfaced.`
          : `${results.length} step${results.length === 1 ? '' : 's'} executed.`
      };
    },
    async route(text) {
      const parsed = Cells.parse(text);
      const context = await M4.context();
      const verdict = Administrator.evaluate(parsed);
      if (!verdict.ok) return { ok: false, stage: 'Administrator', message: verdict.reason };

      if (parsed.type === 'control') return { ok: true, stage: 'Executor', parsed, result: await A.control.call(parsed.operation, parsed.args || {}), message: parsed.operation };
      if (parsed.type === 'picker') { Nerves.click(parsed.target); return { ok: true, stage: 'Nerves', parsed, message: parsed.message }; }
      if (parsed.type === 'adjust-hold') {
        const current = Number(document.getElementById('frame-hold')?.value || 2);
        const hold = Math.max(1, Math.min(12, current + parsed.delta));
        return { ok: true, stage: 'Executor', parsed, result: await A.control.call('set_hold', { hold }), message: `Hold ${hold}x` };
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
        return { ok: true, stage: 'Administrator', message: planned.message || 'Asset accepted' };
      }
      return { ok: false, stage: 'Director', message: 'Attached Director worker returned no executable plan.' };
    }
  };

  A.architecture = { Cells, Nerves, M4, Dream, Administrator, DirectorPort };
  A.directorPort = DirectorPort;
  window.OneWaveArchitecture = A.architecture;
  window.OneWaveDirectorPort = DirectorPort;
  A.status('Delegation ready — human + attached assistant are the workers');
})();
