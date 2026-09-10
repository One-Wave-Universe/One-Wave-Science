(function () {
  'use strict';

  const tuner = globalThis.CircleFifthsTuner;
  if (!tuner || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return;

  let context = null;
  let stream = null;
  let source = null;
  let analyser = null;
  let monitorGain = null;
  let raf = 0;

  const style = document.createElement('style');
  style.textContent = `
    #pedalLabLauncher{position:fixed;right:12px;bottom:48px;z-index:10001;padding:8px 11px;border-radius:8px;border:1px solid #516174;background:#241d2b;color:#f0e8ff;cursor:pointer}
    #pedalLabPanel{position:fixed;right:12px;bottom:88px;z-index:10000;width:340px;max-height:72vh;overflow:auto;padding:14px;border:1px solid #465166;border-radius:12px;background:#111821;color:#e8ecf1;box-shadow:0 12px 40px #000a;font:13px/1.4 system-ui,sans-serif}
    #pedalLabPanel[hidden]{display:none} #pedalLabPanel h2{font-size:16px;margin:0 0 6px} #pedalLabPanel h3{font-size:12px;margin:14px 0 6px;text-transform:uppercase;color:#9aa5b3}
    .pedal-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.pedal-btn{padding:7px 10px;border-radius:7px;border:1px solid #3b4655;background:#1b2531;color:#dce7f2;cursor:pointer}.pedal-btn:hover{border-color:#7ca7ff}
    .tuner-note{font-size:34px;font-weight:800;letter-spacing:.02em}.tuner-readout{font-family:ui-monospace,monospace;color:#b9c8d8}.tuner-meter{height:10px;background:#222d39;border-radius:8px;position:relative;overflow:hidden;margin:8px 0}.tuner-needle{position:absolute;top:0;bottom:0;width:3px;background:#fff;left:50%}
    .fifths-wheel{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;margin-top:8px}.fifths-note{font-size:11px;text-align:center;padding:5px 2px;border:1px solid #303b49;border-radius:6px;color:#9aa5b3}.fifths-note.active{border-color:#fff;color:#fff;font-weight:700}
    .pedal-status{margin-top:8px;color:#9aa5b3}.pedal-warning{margin-top:10px;padding:8px;border:1px solid #674c2e;border-radius:8px;background:#2a2118;color:#ffd29b}
  `;
  document.head.appendChild(style);

  const button = document.createElement('button');
  button.id = 'pedalLabLauncher';
  button.textContent = 'Pedal Lab + Tuner';
  document.body.appendChild(button);

  const panel = document.createElement('section');
  panel.id = 'pedalLabPanel';
  panel.hidden = true;
  panel.innerHTML = `
    <h2>Pedal Lab</h2>
    <div class="pedal-status" id="pedalStatus">Input stopped.</div>
    <div class="pedal-row" style="margin-top:9px">
      <button class="pedal-btn" id="pedalStart">Start guitar input</button>
      <label><input id="pedalMonitor" type="checkbox"> monitor dry input</label>
    </div>
    <h3>Circle of Fifths tuner — pre-pedal tap</h3>
    <div class="tuner-note" id="tunerNote">—</div>
    <div class="tuner-readout" id="tunerReadout">Play one note</div>
    <div class="tuner-meter"><span class="tuner-needle" id="tunerNeedle"></span></div>
    <div class="fifths-wheel" id="fifthsWheel"></div>
    <div class="pedal-warning"><b>Audio reality boundary:</b> live guitar enters Pedal Lab and the tuner reads that real input. The audible circuit path is dry BYPASS only until individual breadboard components have qualified audio-rate models. Unsupported analog circuits are not converted into made-up effects.</div>
  `;
  document.body.appendChild(panel);

  const noteEl = panel.querySelector('#tunerNote');
  const readoutEl = panel.querySelector('#tunerReadout');
  const needleEl = panel.querySelector('#tunerNeedle');
  const statusEl = panel.querySelector('#pedalStatus');
  const startBtn = panel.querySelector('#pedalStart');
  const monitorBox = panel.querySelector('#pedalMonitor');
  const wheel = panel.querySelector('#fifthsWheel');

  tuner.FIFTHS.forEach((name) => {
    const el = document.createElement('div');
    el.className = 'fifths-note';
    el.dataset.note = name.replace('♯', '#').replace('♭', 'b');
    el.textContent = name;
    wheel.appendChild(el);
  });

  function fifthNameForPitchClass(pc) {
    const names = ['C','D♭','D','E♭','E','F','F♯','G','A♭','A','B♭','B'];
    return names[pc];
  }

  function updateWheel(pc) {
    const active = fifthNameForPitchClass(pc);
    [...wheel.children].forEach((el) => el.classList.toggle('active', el.textContent === active));
  }

  function updateTuner() {
    if (!analyser || !context) return;
    const samples = new Float32Array(analyser.fftSize);
    analyser.getFloatTimeDomainData(samples);
    const found = tuner.detectPitch(samples, context.sampleRate);
    if (found) {
      const d = tuner.describeFrequency(found.frequency);
      noteEl.textContent = `${d.note}${d.octave}`;
      readoutEl.textContent = `${found.frequency.toFixed(2)} Hz   ${d.cents >= 0 ? '+' : ''}${d.cents.toFixed(1)} cents   confidence ${found.confidence.toFixed(2)}`;
      const clamped = Math.max(-50, Math.min(50, d.cents));
      needleEl.style.left = `${50 + clamped}%`;
      updateWheel(d.pitchClass);
    } else {
      noteEl.textContent = '—';
      readoutEl.textContent = 'Listening — no stable pitched note yet';
      needleEl.style.left = '50%';
      [...wheel.children].forEach((el) => el.classList.remove('active'));
    }
    raf = requestAnimationFrame(updateTuner);
  }

  async function startAudio() {
    if (context) return;
    statusEl.textContent = 'Requesting local audio input…';
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false },
        video: false,
      });
      context = new AudioContext({ latencyHint: 'interactive' });
      source = context.createMediaStreamSource(stream);
      analyser = context.createAnalyser();
      analyser.fftSize = 4096;
      analyser.smoothingTimeConstant = 0;
      monitorGain = context.createGain();
      monitorGain.gain.value = monitorBox.checked ? 1 : 0;

      // One real input graph. The tuner taps the guitar BEFORE any future
      // pedal processor. The audible branch is currently a declared dry
      // bypass; qualified circuit-audio processors can be inserted between
      // analyser and monitorGain later without changing the tuner module.
      source.connect(analyser);
      analyser.connect(monitorGain);
      monitorGain.connect(context.destination);
      statusEl.textContent = `Live input active at ${context.sampleRate} Hz. Tuner is pre-pedal; circuit audio is BYPASS.`;
      startBtn.textContent = 'Input active';
      startBtn.disabled = true;
      updateTuner();
    } catch (err) {
      statusEl.textContent = `Audio input failed: ${err && err.message ? err.message : String(err)}`;
    }
  }

  monitorBox.addEventListener('change', () => {
    if (monitorGain && context) monitorGain.gain.setTargetAtTime(monitorBox.checked ? 1 : 0, context.currentTime, 0.01);
  });
  startBtn.addEventListener('click', startAudio);
  button.addEventListener('click', () => { panel.hidden = !panel.hidden; });

  globalThis.StarForgePedalLab = {
    startAudio,
    tuner,
    get audioContext() { return context; },
    get analyser() { return analyser; },
    audioCircuitMode: 'BYPASS_UNTIL_QUALIFIED',
  };
})();
