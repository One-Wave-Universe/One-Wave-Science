const { contextBridge, ipcRenderer } = require('electron');

// exposes two narrow capabilities to the renderer: opening a URL in the
// user's real default browser, and routing an AI-provider HTTPS request
// through the main process (bypasses browser CORS for providers like
// OpenAI that block direct page-context fetches -- see main.js). Nothing
// else from Node/Electron is exposed, keeping the sandboxed renderer's
// access as small as possible.
contextBridge.exposeInMainWorld('electronAPI', {
  openExternal: (url) => ipcRenderer.send('open-external', url),
  aiFetch: (url, options) => ipcRenderer.invoke('ai-fetch', { url, options }),
});
