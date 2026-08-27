(() => {
  'use strict';
  const A = window.Animator;
  if (!A?.voiceLab) throw new Error('C9 requires C6 Voice Lab');
  const aside = document.querySelector('aside');
  if (!aside) return;
  const $ = (id) => document.getElementById(id);

  let recorder = null;
  let stream = null;
  let chunks = [];
  let takeCount = 0;
  let previewUrl = null;

  const panel = document.createElement('div');
  panel.className = 'card';
  panel.innerHTML = `
    <strong>C9 Voice Recorder</strong><br>
    Record a take straight into one of the three Voice Lab layers.
    <div style="margin-top:8px">
      <label>Target layer
        <select id="c9-target-layer">
          <option value="0">Layer 1</option>
          <option value="1">Layer 2</option>
          <option value="2">Layer 3</option>
        </select>
      </label>
    </div>
    <label style="display:block;margin-top:8px"><input id="c9-raw-mic" type="checkbox" checked> Raw voice mode (disable browser echo/noise/auto-gain processing)</label>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
      <button id="c9-record" type="button">Record Take</button>
      <button id="c9-stop" type="button" disabled>Stop</button>
    </div>
    <audio id="c9-preview" controls style="width:100%;margin-top:8px"></audio>
    <div id="c9-meta" style="margin-top:6px">Ready</div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  function cleanupStream() {
    stream?.getTracks().forEach(track => track.stop());
    stream = null;
  }

  async function start() {
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) return A.status('Microphone recording is not available in this browser');
    cleanupStream();
    try {
      const raw = Boolean($('c9-raw-mic')?.checked);
      stream = await navigator.mediaDevices.getUserMedia({
        audio: raw ? { echoCancellation: false, noiseSuppression: false, autoGainControl: false } : true
      });
      const type = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus' : 'audio/webm';
      recorder = new MediaRecorder(stream, { mimeType: type });
      chunks = [];
      recorder.ondataavailable = e => { if (e.data?.size) chunks.push(e.data); };
      recorder.onstop = finish;
      recorder.onerror = e => {
        console.error(e.error || e);
        $('c9-meta').textContent = 'Recorder error';
        cleanupStream();
        recorder = null;
        $('c9-record').disabled = false;
        $('c9-stop').disabled = true;
      };
      recorder.start(100);
      $('c9-record').disabled = true;
      $('c9-stop').disabled = false;
      $('c9-meta').textContent = raw ? 'Recording raw take…' : 'Recording processed-browser take…';
      A.status('Recording voice take');
    } catch (error) {
      console.error(error);
      cleanupStream();
      recorder = null;
      $('c9-record').disabled = false;
      $('c9-stop').disabled = true;
      A.status(`Microphone failed: ${error.message}`);
    }
  }

  function stop() {
    if (recorder && recorder.state !== 'inactive') recorder.stop();
    $('c9-stop').disabled = true;
  }

  function finish() {
    try {
      if (!chunks.length) {
        $('c9-meta').textContent = 'No audio captured';
        A.status('Voice take was empty');
        return;
      }
      const blob = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' });
      if (!blob.size) {
        $('c9-meta').textContent = 'No audio captured';
        A.status('Voice take was empty');
        return;
      }
      takeCount += 1;
      const file = new File([blob], `voice-take-${String(takeCount).padStart(2,'0')}.webm`, { type: blob.type });
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      previewUrl = URL.createObjectURL(blob);
      const preview = $('c9-preview');
      preview.src = previewUrl;
      const layer = Math.max(0, Math.min(2, Number($('c9-target-layer')?.value || 0)));
      const input = $(`voice-layer-${layer}-file`);
      if (input && window.DataTransfer) {
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        input.dispatchEvent(new Event('change', { bubbles: true }));
        $('c9-meta').textContent = `Take ${takeCount} loaded into Layer ${layer + 1} — ${(blob.size / 1024).toFixed(1)} KB`;
        A.status(`Recorded take loaded into Voice Lab Layer ${layer + 1}`);
      } else {
        $('c9-meta').textContent = 'Take recorded — browser could not inject it into the selected layer';
      }
    } finally {
      cleanupStream();
      chunks = [];
      recorder = null;
      $('c9-record').disabled = false;
      $('c9-stop').disabled = true;
    }
  }

  function loadHardening() {
    if (A.audioHardening || document.querySelector('script[data-c10-audio-hardening]')) return;
    const script = document.createElement('script');
    script.src = './c10-audio-hardening.js';
    script.setAttribute('data-c10-audio-hardening', 'true');
    document.body.appendChild(script);
  }

  $('c9-record')?.addEventListener('click', start);
  $('c9-stop')?.addEventListener('click', stop);
  window.addEventListener('beforeunload', () => {
    cleanupStream();
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  });

  A.voiceRecorder = { start, stop, cleanup: cleanupStream };
  loadHardening();
})();
