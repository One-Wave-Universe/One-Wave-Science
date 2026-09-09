const { contextBridge, ipcRenderer } = require('electron');

const isJetson = process.platform === 'linux' && process.arch === 'arm64';
const workerPort = Number(process.env.VBB_WORKER_PORT || 8787);

// exposes narrow desktop capabilities to the renderer. computeDefaults is
// configuration only -- the renderer never receives Node/socket access.
contextBridge.exposeInMainWorld('electronAPI', {
  openExternal: (url) => ipcRenderer.send('open-external', url),
  aiFetch: (url, options) => ipcRenderer.invoke('ai-fetch', { url, options }),
  computeDefaults: Object.freeze({
    role: isJetson ? 'jetson' : 'client',
    jetsonHost: process.env.VBB_JETSON_HOST || '',
    workerPort,
  }),
});
