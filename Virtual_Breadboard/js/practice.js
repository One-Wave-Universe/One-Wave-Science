(function (root) {
  'use strict';

  const MODE_KEY = 'starForgeMode';
  const PROGRESS_KEY = 'starForgePracticeProgress';
  const BASIC_TOOLS = new Set([
    'wire', 'ywire', 'resistor', 'led', 'diode', 'capacitor', 'battery',
    'switch', 'pushbutton', 'potentiometer', 'inductor', 'acsource',
    'scope', 'diffscope', 'nmos', 'pmos'
  ]);
  const FULL_BENCH_EXTRA = new Set(['vgnd', 'mtjsensor', 'toroid']);
  const EXPERIMENTAL_TOOLS = new Set(['memorycore', 'comparator']);

  const lessons = [
    {
      id: 'led-resistor',
      title: '1. Light an LED safely',
      preset: 'presetLed',
      goal: 'Power an LED through a resistor and read the voltage/current without burning it up.',
      check: 'Change the resistor value and watch LED current and brightness move together.'
    },
    {
      id: 'rc-charge',
      title: '2. Watch a capacitor charge',
      preset: 'presetRC',
      goal: 'Use a resistor, capacitor, switch, supply and scope to see an RC curve happen in real time.',
      check: 'Change R or C and verify the charge time changes.'
    },
    {
      id: 'short-fault',
      title: '3. Make a bad circuit on purpose',
      preset: 'presetShort',
      goal: 'See what a short circuit looks like and learn to recognize the warning before doing it on a real bench.',
      check: 'Remove the short and confirm the warning disappears.'
    },
    {
      id: 'divider',
      title: '4. Read a voltage divider',
      preset: 'presetCalA',
      goal: 'Follow two resistive paths and measure the resulting node voltage instead of guessing it.',
      check: 'Change one resistor and predict whether the midpoint rises or falls before reading it.'
    },
    {
      id: 'mosfet-switch',
      title: '5. Use a MOSFET as a switch',
      preset: 'presetCalC',
      goal: 'Turn a load path on and off with a gate voltage and inspect gate, drain and source behavior.',
      check: 'Toggle the switch and verify the drain voltage changes between the expected states.'
    },
    {
      id: 'midrail-rc',
      title: '6. Measure relative to a reference',
      preset: 'presetCalE',
      goal: 'Use a reference node and a differential scope so small changes are visible without hand subtraction.',
      check: 'Change the capacitor and verify the transient changes while the reference stays put.'
    }
  ];

  function loadProgress() {
    try { return JSON.parse(root.localStorage.getItem(PROGRESS_KEY) || '{}'); }
    catch (_) { return {}; }
  }

  function saveProgress(progress) {
    try { root.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress)); } catch (_) {}
  }

  function getMode() {
    try { return root.localStorage.getItem(MODE_KEY) || 'practice'; }
    catch (_) { return 'practice'; }
  }

  function setMode(mode) {
    try { root.localStorage.setItem(MODE_KEY, mode); } catch (_) {}
    applyMode(mode);
  }

  function visibleTool(tool, mode) {
    if (mode === 'experimental') return true;
    if (mode === 'full') return BASIC_TOOLS.has(tool) || FULL_BENCH_EXTRA.has(tool);
    return BASIC_TOOLS.has(tool);
  }

  function applyMode(mode) {
    document.body.dataset.starForgeMode = mode;
    document.querySelectorAll('#toolbox .tool-btn').forEach((button) => {
      const tool = button.dataset.tool;
      button.hidden = tool !== 'select' && !visibleTool(tool, mode);
    });

    const experimentalIds = ['presetMemCell', 'presetCalF', 'presetCalG', 'presetCalH', 'presetStage1'];
    experimentalIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.hidden = mode !== 'experimental';
    });

    const advancedIds = ['presetCalB', 'presetCalD'];
    advancedIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.hidden = mode === 'practice';
    });

    const ai = document.querySelector('.ai-panel');
    if (ai) ai.hidden = mode === 'practice';

    document.querySelectorAll('[data-sf-mode]').forEach((button) => {
      button.classList.toggle('active', button.dataset.sfMode === mode);
      button.setAttribute('aria-pressed', String(button.dataset.sfMode === mode));
    });

    const description = document.getElementById('sfModeDescription');
    if (description) {
      description.textContent = mode === 'practice'
        ? 'Ordinary electronics only. Guided practice, normal parts, measurements and faults.'
        : mode === 'full'
          ? 'General-purpose breadboard bench with the full normal component and measurement set.'
          : 'Research bench. Experimental parts and One-Wave prototype work are visible and must stay reality-audited.';
    }
  }

  function makeModeBar() {
    const header = document.querySelector('.top');
    if (!header) return;
    const bar = document.createElement('section');
    bar.className = 'sf-modebar';
    bar.innerHTML = `
      <div class="sf-mode-buttons" role="group" aria-label="Star Forge mode">
        <button type="button" data-sf-mode="practice">Practice</button>
        <button type="button" data-sf-mode="full">Full Bench</button>
        <button type="button" data-sf-mode="experimental">Experimental</button>
      </div>
      <div id="sfModeDescription" class="sf-mode-description"></div>`;
    header.insertAdjacentElement('afterend', bar);
    bar.querySelectorAll('[data-sf-mode]').forEach((button) => {
      button.addEventListener('click', () => setMode(button.dataset.sfMode));
    });
  }

  function makePracticePanel() {
    const workspace = document.querySelector('.workspace');
    if (!workspace) return;
    const panel = document.createElement('section');
    panel.id = 'sfPracticePanel';
    panel.className = 'sf-practice-panel';
    panel.innerHTML = `
      <div class="sf-practice-head">
        <div>
          <h2>Practice Bench</h2>
          <p>Normal breadboard work. Load one circuit, poke it, change one thing, predict what happens, then measure it.</p>
        </div>
        <div id="sfPracticeScore" class="sf-practice-score"></div>
      </div>
      <div id="sfPracticeLessons" class="sf-practice-lessons"></div>`;
    workspace.insertAdjacentElement('beforebegin', panel);

    const container = panel.querySelector('#sfPracticeLessons');
    const progress = loadProgress();
    lessons.forEach((lesson) => {
      const card = document.createElement('article');
      card.className = 'sf-lesson';
      card.dataset.lessonId = lesson.id;
      card.innerHTML = `
        <h3>${lesson.title}</h3>
        <p>${lesson.goal}</p>
        <p class="sf-lesson-check"><strong>Try:</strong> ${lesson.check}</p>
        <div class="sf-lesson-actions">
          <button type="button" class="sf-load-lesson">Load circuit</button>
          <label><input type="checkbox" class="sf-complete-lesson"> Done</label>
        </div>`;
      const checkbox = card.querySelector('.sf-complete-lesson');
      checkbox.checked = Boolean(progress[lesson.id]);
      checkbox.addEventListener('change', () => {
        const next = loadProgress();
        next[lesson.id] = checkbox.checked;
        saveProgress(next);
        refreshProgress();
      });
      card.querySelector('.sf-load-lesson').addEventListener('click', () => {
        const preset = document.getElementById(lesson.preset);
        if (preset) preset.click();
      });
      container.appendChild(card);
    });
    refreshProgress();
  }

  function refreshProgress() {
    const progress = loadProgress();
    const done = lessons.filter((lesson) => progress[lesson.id]).length;
    const score = document.getElementById('sfPracticeScore');
    if (score) score.textContent = `${done}/${lessons.length} practiced`;
  }

  function applyPracticeVisibility() {
    const panel = document.getElementById('sfPracticePanel');
    if (panel) panel.hidden = document.body.dataset.starForgeMode !== 'practice';
  }

  function boot() {
    makeModeBar();
    makePracticePanel();
    const mode = getMode();
    applyMode(mode);
    applyPracticeVisibility();
    document.querySelectorAll('[data-sf-mode]').forEach((button) => {
      button.addEventListener('click', () => setTimeout(applyPracticeVisibility, 0));
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
  else boot();
})(typeof window !== 'undefined' ? window : this);
