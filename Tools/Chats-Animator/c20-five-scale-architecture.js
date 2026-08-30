(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.control) throw new Error('C20 requires Animator control API');

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
      return { type: 'unknown', raw };
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

  const Dream = {
    async generate(request, context) {
      const job = { type: 'create-asset', kind: request.kind, prompt: request.prompt, frame: context.frame, project: context.project, requestedAt: context.time };
      if (typeof window.oneWaveAssetWorker === 'function') return window.oneWaveAssetWorker(job);
      Nerves.emit('onewave-asset-request', job);
      return { pending: true, message: `Asset request ready: ${request.kind} — ${request.prompt}` };
    },
    async plan(request, context) {
      if (typeof window.oneWaveDirectorWorker === 'function') return window.oneWaveDirectorWorker({ request, animator: A, context });
      Nerves.emit('onewave-director-request', { request, context });
      return null;
    }
  };

  const Administrator = {
    evaluate(parsed, context) {
      if (!parsed) return { ok: false, reason: 'Nothing parsed' };
      if (parsed.type === 'control' && !A.control.operations.includes(parsed.operation)) return { ok: false, reason: `Unsupported operation: ${parsed.operation}` };
      if (parsed.type === 'generate' && !parsed.prompt) return { ok: false, reason: 'Generation prompt is empty' };
      if (parsed.type === 'control' && parsed.operation === 'capture_motion' && parsed.args.end < parsed.args.start) return { ok: false, reason: 'Motion end frame is before start frame' };
      return { ok: true, parsed, context };
    },
    evaluatePlan(plan) {
      if (!plan || !Array.isArray(plan.steps)) return { ok: false, reason: 'Planner did not return a step list' };
      for (const step of plan.steps) {
        if (!step?.operation || !A.control.operations.includes(step.operation)) return { ok: false, reason: `Unsupported planned operation: ${step?.operation || 'missing'}` };
      }
      return { ok: true, plan };
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
    async executePlan(plan) {
      const verdict = Administrator.evaluatePlan(plan);
      if (!verdict.ok) return { ok: false, stage: 'Administrator', message: verdict.reason, plan };
      const results = [];
      for (const step of plan.steps) {
        const result = await A.control.call(step.operation, step.args || {});
        results.push({ step, result });
      }
      const missing = Array.isArray(plan.missing) ? plan.missing : [];
      if (missing.length) {
        const project = await A.control.call('get_project').then((r) => r.result);
        for (const need of missing) {
          await Dream.generate({
            kind: need.kind === 'motion' ? 'character' : (need.kind || 'asset'),
            prompt: `${need.actor ? `${need.actor} ` : ''}${need.action || ''}${need.target ? ` ${need.target}` : ''}`.trim()
          }, {
            frame: plan.frame || ((A.reel?.activeIndex ?? 0) + 1),
            time: new Date().toISOString(),
            project
          });
        }
      }
      return {
        ok: results.length > 0 || missing.length > 0,
        stage: missing.length ? 'Dream' : 'Executor',
        plan,
        results,
        missing,
        message: missing.length
          ? `${results.length} planned step${results.length === 1 ? '' : 's'} executed; ${missing.length} missing motion asset${missing.length === 1 ? '' : 's'} queued.`
          : `${results.length} planned step${results.length === 1 ? '' : 's'} executed.`
      };
    },
    async route(text) {
      const parsed = Cells.parse(text);
      const context = {
        frame: (A.reel?.activeIndex ?? 0) + 1,
        time: new Date().toISOString(),
        project: await A.control.call('get_project').then((r) => r.result)
      };
      const verdict = Administrator.evaluate(parsed, context);
      if (!verdict.ok) return { ok: false, stage: 'Administrator', message: verdict.reason };

      if (parsed.type === 'control') {
        const result = await A.control.call(parsed.operation, parsed.args || {});
        return { ok: true, stage: 'Executor', parsed, result, message: parsed.operation };
      }
      if (parsed.type === 'picker') {
        Nerves.click(parsed.target);
        return { ok: true, stage: 'Nerves', parsed, message: parsed.message };
      }
      if (parsed.type === 'adjust-hold') {
        const current = Number(document.getElementById('frame-hold')?.value || 2);
        const hold = Math.max(1, Math.min(12, current + parsed.delta));
        const result = await A.control.call('set_hold', { hold });
        return { ok: true, stage: 'Executor', parsed, result, message: `Hold ${hold}x` };
      }
      if (parsed.type === 'generate') {
        const generated = await Dream.generate(parsed, context);
        if (generated?.asset || generated?.assets) await Promise.all(Administrator.acceptAssets(generated));
        return { ok: true, stage: 'Dream', parsed, generated, message: generated?.message || 'Generation request sent' };
      }

      const planned = await Dream.plan({ text, parsed }, context);
      if (Array.isArray(planned?.steps)) return M4.executePlan(planned);
      if (planned?.operation) {
        const checked = Administrator.evaluate({ type: 'control', operation: planned.operation, args: planned.args || {} }, context);
        if (!checked.ok) return { ok: false, stage: 'Administrator', message: checked.reason };
        const result = await A.control.call(planned.operation, planned.args || {});
        return { ok: true, stage: 'Executor', result, message: planned.message || planned.operation };
      }
      if (planned?.asset || planned?.assets) {
        await Promise.all(Administrator.acceptAssets(planned));
        return { ok: true, stage: 'Administrator', message: planned.message || 'Generated asset accepted' };
      }
      return { ok: false, stage: 'M4', message: 'Request could not be turned into executable work.' };
    }
  };

  A.architecture = { Cells, Nerves, M4, Dream, Administrator };
  window.OneWaveArchitecture = A.architecture;
  A.status('Five-scale architecture ready');
})();
