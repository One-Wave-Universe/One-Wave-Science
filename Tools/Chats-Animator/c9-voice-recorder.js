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
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
      <button id="c9-record" type="button">Record Take</button>
      <button id="c9-stop" type="button" disabled>Stop</button>
    </div>
    <audio id="c9-preview" controls style="width:100%;margin-top:8px"></audio>
    <div id="c9-meta" style="margin-top:6px">Ready</div>
  `;
  aside.insertBefore(panel, aside.firstChild);

  async function start() {
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) return A.status('Microphone recording is not available in this browser');
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const type = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus' : 'audio/webm';
      recorder = new MediaRecorder(stream, { mimeType: type });
      chunks = [];
      recorder.ondataavailable = e => { if (e.data?.size) chunks.push(e.data); };
      recorder.onstop = finish;
      recorder.start(100);
      $('c9-record').disabled = true;
      $('c9-stop').disabled = false;
      $('c9-meta').textContent = 'Recording…';
      A.status('Recording voice take');
    } catch (error) {
      console.error(error);
      A.status(`Microphone failed: ${error.message}`);
    }
  }

  function stop() {
    if (recorder && recorder.state !== 'inactive') recorder.stop();
    $('c9-stop').disabled = true;
  }

  function finish() {
    const blob = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' });
    takeCount += 1;
    const file = new File([blob], `voice-take-${String(takeCount).padStart(2,'0')}.webm`, { type: blob.type });
    const url = URL.createObjectURL(blob);
    const preview = $('c9-preview');
    preview.src = url;
    const layer = Number($('c9-target-layer')?.value || 0);
    const input = $(`voice-layer-${layer}-file`);
    if (input && window.DataTransfer) {
      const dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;
      input.dispatchEvent(new Event('change', { bubbles: true }));
      $('c9-meta').textContent = `Take ${takeCount} loaded into Layer ${layer + 1}`;
      A.status(`Recorded take loaded into Voice Lab Layer ${layer + 1}`);
    } else {
      $('c9-meta').textContent = 'Take recorded — browser could not inject it into the selected layer';
    }
    stream?.getTracks().forEach(track => track.stop());
    stream = null;
    recorder = null;
    $('c9-record').disabled = false;
  }

  $('c9-record')?.addEventListener('click', start);
  $('c9-stop')?.addEventListener('click', stop);

  A.voiceRecorder = { start, stop };
})();
