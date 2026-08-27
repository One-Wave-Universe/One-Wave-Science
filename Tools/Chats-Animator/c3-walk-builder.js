(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.pathMotion || !A?.walkCadence) throw new Error('C3 walk builder requires C1 path motion + C2 cadence');
  const $ = (id) => document.getElementById(id);
  const aside = document.querySelector('aside');
  if (!aside) return;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>One-click walk run</strong><br>
    Uses the C1 path controls and C2 cadence controls together. Start on the first pose frame of the run.
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
      <button id="build-walk-away" type="button">Build Walk Away</button>
      <button id="build-walk-toward" type="button">Build Walk Toward</button>
    </div>
    <div id="walk-builder-meta" style="margin-top:8px">Ready</div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function syncCounts() {
    const pathCount = Math.max(2, Number($('path-count')?.value || 7));
    if ($('cadence-count')) {
      $('cadence-count').value = String(pathCount);
      $('cadence-count').dispatchEvent(new Event('input', { bubbles: true }));
    }
    return pathCount;
  }

  function build(reverse = false) {
    const count = syncCounts();
    A.pathMotion.fitRun(reverse);
    A.walkCadence.applyCadence();
    if ($('walk-builder-meta')) {
      $('walk-builder-meta').textContent = `${reverse ? 'Toward-camera' : 'Away-from-camera'} walk built across ${count} pose frames`;
    }
    A.status(`${reverse ? 'Toward-camera' : 'Away-from-camera'} walk run built`);
  }

  $('build-walk-away')?.addEventListener('click', () => build(false));
  $('build-walk-toward')?.addEventListener('click', () => build(true));

  A.walkBuilder = { build, syncCounts };
})();
