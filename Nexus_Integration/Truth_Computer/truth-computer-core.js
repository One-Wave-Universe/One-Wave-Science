(function (global) {
  'use strict';

  const STATUS_ORDER = ['canonical', 'observed', 'one-wave', 'candidate', 'unknown'];

  function text(value) {
    return String(value == null ? '' : value).trim();
  }

  function lower(value) {
    return text(value).toLowerCase();
  }

  function classify(record) {
    const joined = lower([
      record.truthStatus,
      record.gate,
      record.lifecycle,
      record.kind,
      record.status,
      record.sourcePath,
      record.title
    ].join(' '));

    if (/quarantine|rejected|retired|deprecated|superseded/.test(joined)) return 'unknown';
    if (/candidate|yellow|green scaffold|hypothesis|proposed|unresolved/.test(joined)) return 'candidate';
    if (/measurement|observed|empirical|gray|conventional|reference/.test(joined)) return 'observed';
    if (/one-wave|interpretation|application|homology|recurrence/.test(joined)) return 'one-wave';
    if (/canonical|gold|silver|bronze|active/.test(joined)) return 'canonical';
    return 'unknown';
  }

  function normalizeRecord(record, index) {
    const r = Object.assign({}, record || {});
    r.id = text(r.id || r.nodeId || `record-${index + 1}`);
    r.title = text(r.title || r.name || r.id);
    r.definition = text(r.definition || r.summary || r.text);
    r.sourcePath = text(r.sourcePath || r.path || r.source);
    r.truthClass = classify(r);
    r.score = Number(r.score || 0);
    return r;
  }

  function sortRecords(records) {
    return records.slice().sort((a, b) => {
      const sa = STATUS_ORDER.indexOf(a.truthClass);
      const sb = STATUS_ORDER.indexOf(b.truthClass);
      if (sa !== sb) return sa - sb;
      return b.score - a.score;
    });
  }

  function selectEvidence(records, terms) {
    const words = terms.map(lower);
    return records.filter((r) => {
      const haystack = lower(`${r.id} ${r.title} ${r.definition} ${r.sourcePath}`);
      return words.some((word) => haystack.includes(word));
    });
  }

  function stageQuestion(node, topic) {
    const questions = {
      'OG-00': `What undivided Ground or unselected possibility permits ${topic}?`,
      'OG-01': `What first difference or disturbance makes ${topic} distinguishable?`,
      'OG-02': `What responds to that difference, without assuming intention or awareness?`,
      'OG-03': `What returns toward the source, boundary, or prior condition?`,
      'OG-04': `How does the return alter the next response?`,
      'OG-05': `What repeats often enough to become recurrence rather than a single event?`,
      'OG-06': `Which local loops couple to neighboring or containing loops?`,
      'OG-07': `What relationship survives repeated cycling?`,
      'OG-08': `How does the retained pattern affect a later cycle?`,
      'OG-09': `Which memory becomes the Reference Ground?`,
      'OG-10': `What current return is compared with that reference?`,
      'OG-11': `Where does the system first register a change in its own state?`,
      'OG-12': `What registered condition is held as current Presence?`,
      'OG-13': `What complete Field defines the choices actually available?`,
      'OG-14': `Which available differential is selected, and what next Field does it imply?`,
      'OG-15': `How is the choice expressed as movement, transfer, action, or held motion?`,
      'OG-16': `What meets its inverse at the Mirror Gate, and what returns or resists?`,
      'OG-17': `What resulting State is measured against reference, scale, and constraint?`,
      'OG-18': `What result is stable enough to Commit as New Ground?`,
      'OG-19': `What higher-order behavior emerges only after repeated committed loops?`,
      'OG-20': `How does the emergent unit become part of a larger recursive organization?`,
      'OG-21': `What new scale, Presence, or possibility opens beyond the current form?`
    };
    return questions[node.node_id] || node.role;
  }

  function evidenceForStage(node, records) {
    const termsByStage = {
      'OG-00': ['ground', 'zero', 'null', 'field'],
      'OG-01': ['difference', 'disturbance', 'differential', 'gradient'],
      'OG-02': ['response', 'restoring', 'reaction'],
      'OG-03': ['return', 'flowback', 'reclosure'],
      'OG-04': ['feedback', 'loop'],
      'OG-05': ['recurrence', 'repeated', 'oscillation'],
      'OG-06': ['coupled', 'nested', 'paired loop', 'network'],
      'OG-07': ['retained', 'persistent', 'stability'],
      'OG-08': ['memory', 'history', 'stored'],
      'OG-09': ['reference', 'ground', 'anchor'],
      'OG-10': ['comparison', 'difference', 'audit'],
      'OG-11': ['awareness', 'register'],
      'OG-12': ['presence', 'current state'],
      'OG-13': ['field', 'constraint', 'boundary'],
      'OG-14': ['choice', 'selector', 'polarity'],
      'OG-15': ['move', 'motion', 'transfer', 'action'],
      'OG-16': ['mirror gate', 'interaction', 'boundary', 'inverse'],
      'OG-17': ['state', 'stability', 'constraint'],
      'OG-18': ['commit', 'lock', 'new ground'],
      'OG-19': ['emergence', 'higher-order'],
      'OG-20': ['scale', 'organization', 'macro', 'micro'],
      'OG-21': ['beyond', 'new scale', 'expanded']
    };
    return selectEvidence(records, termsByStage[node.node_id] || []).slice(0, 3);
  }

  function scaleAnalysis(topic, records) {
    const chapter = records.find((r) => /scale invariance/.test(lower(`${r.title} ${r.sourcePath}`)) && /book|chapter|ch03/.test(lower(`${r.kind} ${r.sourcePath} ${r.title}`)));
    const support = selectEvidence(records, ['scale-invariant', 'scale layer', 'scale recurrence', 'homology', 'micro', 'macro']).slice(0, 8);
    return {
      title: 'Scale Invariance',
      chapter: chapter || null,
      support,
      questions: [
        `What structure in ${topic} repeats at a smaller scale?`,
        `What structure repeats at a larger scale?`,
        'What relationship remains invariant?',
        'What participants, frequencies, thresholds, or coupling values change?',
        'Is the relationship analogy, architectural homology, recurrence, candidate invariance, or supported invariance?'
      ],
      status: chapter ? 'chapter-grounded' : (support.length ? 'node-supported; chapter missing from result set' : 'unresolved')
    };
  }

  function buildTrace(topic, rawRecords, ogSystem) {
    const cleanTopic = text(topic).slice(0, 180);
    if (!cleanTopic) throw new Error('A subject is required.');
    const records = sortRecords((rawRecords || []).map(normalizeRecord));
    const nodes = (ogSystem && ogSystem.nodes) || [];
    const stages = nodes.map((node) => ({
      id: node.node_id,
      name: node.canonical_name,
      identity: node.identity,
      role: node.role,
      output: node.output,
      question: stageQuestion(node, cleanTopic),
      evidence: evidenceForStage(node, records)
    }));

    const groups = {
      originAndFeedback: stages.slice(0, 11),
      awarenessAndPresence: stages.slice(11, 13),
      activeGates: stages.slice(13, 19),
      emergenceAndBeyond: stages.slice(19, 22)
    };

    const byStatus = {};
    STATUS_ORDER.forEach((status) => { byStatus[status] = records.filter((r) => r.truthClass === status); });

    const contradictions = records.filter((r) => /conflict|contradiction|rejected|retired|unresolved|quarantine/.test(lower(`${r.title} ${r.definition} ${r.truthStatus}`)));

    return {
      topic: cleanTopic,
      counts: ogSystem && ogSystem.counts,
      definition: records[0] || null,
      records,
      byStatus,
      groups,
      scale: scaleAnalysis(cleanTopic, records),
      contradictions,
      missingEvidence: records.length === 0,
      notice: 'The OG spine is canonical. Topic-specific claims remain at the status of their supporting records. Generated wording does not promote itself to canon, because apparently somebody has to supervise the adjectives.'
    };
  }

  global.NexusTruthCore = {
    classify,
    normalizeRecord,
    buildTrace
  };
})(window);
