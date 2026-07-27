(function (global) {
  'use strict';

  const esc = (value) => String(value == null ? '' : value).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));

  function recordCard(record, adapter) {
    const button = adapter && adapter.openDefinition
      ? `<button class="tc-open" data-record="${esc(record.id)}">Open definition</button>`
      : '';
    return `<article class="tc-record tc-${esc(record.truthClass)}">
      <div class="tc-record-head"><strong>${esc(record.id)} · ${esc(record.title)}</strong><span>${esc(record.truthClass)}</span></div>
      <p>${esc(record.definition || 'No definition text returned.')}</p>
      <code>${esc(record.sourcePath)}</code>${button}
    </article>`;
  }

  function stageCard(stage) {
    const evidence = stage.evidence.length
      ? `<ul>${stage.evidence.map((r) => `<li>${esc(r.id)} · ${esc(r.title)} <span>${esc(r.truthClass)}</span></li>`).join('')}</ul>`
      : '<p class="tc-missing">No direct evidence returned for this stage.</p>';
    return `<article class="tc-stage">
      <div class="tc-stage-id">${esc(stage.id)}</div>
      <div><h4>${esc(stage.name)}</h4><p class="tc-question">${esc(stage.question)}</p>${evidence}</div>
    </article>`;
  }

  function group(title, stages) {
    return `<section class="tc-section"><h3>${esc(title)}</h3><div class="tc-stage-list">${stages.map(stageCard).join('')}</div></section>`;
  }

  async function mount(options) {
    const root = options.root;
    const adapter = options.adapter;
    if (!root) throw new Error('Truth Computer root element is missing.');

    root.classList.add('nexus-truth-computer');
    root.innerHTML = `<header class="tc-hero">
      <div><p class="tc-kicker">ONE-WAVE REALITY DATABASE</p><h2>Truth Computer</h2>
      <p>Trace any subject from Original Ground through feedback, Presence, the six gates, emergence, scale, and beyond.</p></div>
      <div id="tc-health" class="tc-health">Checking adapters…</div>
    </header>
    <div class="tc-search"><input id="tc-query" placeholder="life, fear, proton, scale invariance…"><button id="tc-run">Trace</button></div>
    <div id="tc-output" class="tc-output"><p class="tc-empty">Enter a subject. The machine will refrain from calling everything Presence this time.</p></div>`;

    const health = root.querySelector('#tc-health');
    const missing = ['searchReality', 'openDefinition', 'createDescribeJob'].filter((name) => !adapter || typeof adapter[name] !== 'function');
    health.textContent = missing.length ? `Adapter incomplete: ${missing.join(', ')}` : 'Reality, definition, and job adapters connected';
    health.classList.toggle('bad', missing.length > 0);

    const ogResponse = await fetch(options.ogUrl);
    if (!ogResponse.ok) throw new Error('Canonical OG system failed to load.');
    const ogSystem = await ogResponse.json();

    const run = async () => {
      const query = root.querySelector('#tc-query').value.trim();
      if (!query) return;
      const output = root.querySelector('#tc-output');
      output.innerHTML = '<p class="tc-empty">Searching the reality database and building the trace…</p>';
      try {
        const records = adapter && adapter.searchReality ? await adapter.searchReality(query) : [];
        const result = global.NexusTruthCore.buildTrace(query, Array.isArray(records) ? records : [], ogSystem);
        const def = result.definition
          ? recordCard(result.definition, adapter)
          : `<article class="tc-record tc-unknown"><strong>No stored definition</strong><p>The OG questions can be shown, but the factual and canonical layer is missing.</p>${adapter && adapter.createDescribeJob ? '<button id="tc-job">Create description job</button>' : ''}</article>`;
        const scaleSupport = result.scale.support.length ? result.scale.support.map((r) => `<li>${esc(r.id)} · ${esc(r.title)} <span>${esc(r.truthClass)}</span></li>`).join('') : '<li>No scale sources returned.</li>';
        const contradictions = result.contradictions.length ? result.contradictions.map((r) => recordCard(r, adapter)).join('') : '<p>No explicit conflict records were returned.</p>';

        output.innerHTML = `<section class="tc-section"><div class="tc-title-row"><div><p class="tc-kicker">SUBJECT</p><h2>${esc(result.topic)}</h2></div>
          <div class="tc-counts">22 OG stages · 6 active gates · 21 Field + 21 Void = 42 around 0</div></div>${def}</section>
          ${group('Origin and Feedback · OG-00 through OG-10', result.groups.originAndFeedback)}
          ${group('Awareness and Presence · OG-11 and OG-12', result.groups.awarenessAndPresence)}
          ${group('Six Bidirectional Gates · OG-13 through OG-18', result.groups.activeGates)}
          ${group('Emergence and Beyond · OG-19 through OG-21', result.groups.emergenceAndBeyond)}
          <section class="tc-section"><h3>Scale Invariance · Chapter Analysis</h3><p>Status: <strong>${esc(result.scale.status)}</strong></p>
            <ol>${result.scale.questions.map((q) => `<li>${esc(q)}</li>`).join('')}</ol><h4>Supporting records</h4><ul>${scaleSupport}</ul></section>
          <section class="tc-section"><h3>Contradictions and Unresolved Material</h3>${contradictions}</section>
          <section class="tc-section"><h3>All Retrieved Sources</h3>${result.records.length ? result.records.map((r) => recordCard(r, adapter)).join('') : '<p>No records returned.</p>'}</section>
          <p class="tc-notice">${esc(result.notice)}</p>`;

        const job = root.querySelector('#tc-job');
        if (job) job.onclick = async () => {
          job.disabled = true;
          job.textContent = 'Creating job…';
          try { await adapter.createDescribeJob(query); job.textContent = 'Job created'; }
          catch (error) { job.disabled = false; job.textContent = `Job failed: ${error.message}`; }
        };

        root.querySelectorAll('.tc-open').forEach((button) => {
          button.onclick = () => {
            const record = result.records.find((r) => r.id === button.dataset.record);
            if (record) adapter.openDefinition(record);
          };
        });
      } catch (error) {
        output.innerHTML = `<article class="tc-record tc-unknown"><strong>Trace failed</strong><p>${esc(error.message)}</p></article>`;
      }
    };

    root.querySelector('#tc-run').onclick = run;
    root.querySelector('#tc-query').addEventListener('keydown', (event) => { if (event.key === 'Enter') run(); });
  }

  global.NexusTruthComputer = { mount };
})(window);
