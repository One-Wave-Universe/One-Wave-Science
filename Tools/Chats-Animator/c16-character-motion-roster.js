(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.motionAtlas) throw new Error('C16 requires C15 motion atlas');
  const aside = document.querySelector('aside');
  if (!aside) return;
  const $ = id => document.getElementById(id);

  const roster = [
    {id:'gr',name:'Goblin Raccoon',file:'goblin-raccoon.owatlas'},
    {id:'nexus',name:'Nexus',file:'nexus.owatlas'},
    {id:'scales',name:'Scales',file:'scales.owatlas'},
    {id:'noobs',name:'Noobs',file:'noobs.owatlas'},
    {id:'cerberus-giant',name:'Cerberus Giant',file:'cerberus-giant.owatlas'},
    {id:'cerberus-modulated-down',name:'Cerberus Modulated-Down',file:'cerberus-modulated-down.owatlas'}
  ];
  let activeId = 'gr';

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C16 Character Motion Corpus</strong><br>
    Separate extensive motion files per character/body variant. Switch corpus without mixing reusable libraries into the active scene.
    <div style="margin-top:8px"><select id="c16-character" style="width:100%"></select></div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
      <button id="c16-load" type="button">Load Character Corpus</button>
      <button id="c16-save" type="button">Save Current Corpus</button>
    </div>
    <div id="c16-status" style="margin-top:8px">Ready</div>`;
  aside.insertBefore(panel, aside.firstChild);

  roster.forEach(item => {
    const o = document.createElement('option');
    o.value = item.id; o.textContent = item.name;
    $('c16-character').appendChild(o);
  });

  function current() { return roster.find(x => x.id === activeId) || roster[0]; }
  function atlasUrl(item=current()) { return `./Motion-Libraries/${item.file}`; }

  async function loadCharacter(id = $('c16-character').value) {
    const item = roster.find(x => x.id === id);
    if (!item) throw new Error('Unknown character corpus');
    $('c16-status').textContent = `Loading ${item.name}…`;
    const response = await fetch(atlasUrl(item));
    if (!response.ok) throw new Error(`${item.name} corpus not found (${response.status})`);
    const data = await response.json();
    A.motionAtlas.loadData(data);
    activeId = item.id;
    $('c16-character').value = activeId;
    const atlas = A.motionAtlas.atlas;
    $('c16-status').textContent = `${item.name}: ${atlas.sequences.length}/${atlas.catalog?.length || 0} required motions completed`;
    A.status(`${item.name} motion corpus loaded`);
    return atlas;
  }

  $('c16-character').addEventListener('change', e => { activeId = e.target.value; });
  $('c16-load').addEventListener('click', () => loadCharacter().catch(err => { console.error(err); $('c16-status').textContent = err.message; A.status(`Corpus load failed: ${err.message}`); }));
  $('c16-save').addEventListener('click', () => A.motionAtlas.save());

  A.motionRoster = { roster, loadCharacter, get active(){ return current(); } };
})();
