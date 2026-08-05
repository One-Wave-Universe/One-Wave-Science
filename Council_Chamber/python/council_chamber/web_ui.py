"""A real local browser UI for the Council Chamber -- Python's standard
library only (http.server), nothing to `pip install` beyond Python
itself. Serves one page: a command box wired to the exact same
CouncilTUI.execute(line) the terminal uses (so it's a real browser skin
over the real backend, not a separate reimplementation), plus a
Providers panel that shows, for each seat kind, whether a real client
is wired up and -- if not -- the exact PowerShell command to set that
provider's API key and relaunch this server with it active. No key is
ever embedded in this file or transmitted anywhere except into your own
environment variable, and no provider is ever contacted by this module
itself.
"""

from __future__ import annotations

import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from council_chamber.client_registry import get_client
from council_chamber.tui import SEAT_CATALOG, CouncilTUI, demo_council

# Known real-world signup pages and the environment variable name each
# provider's client (seats/<x>_client.py) reads. Only the URL and the
# env var name live here -- never a key.
PROVIDER_INFO: dict[str, dict] = {
    "gemini": {"signup_url": "https://aistudio.google.com/apikey", "env_var": "GEMINI_API_KEY"},
    "groq": {"signup_url": "https://console.groq.com/keys", "env_var": "GROQ_API_KEY"},
    "chatgpt": {"signup_url": "https://platform.openai.com/api-keys", "env_var": "OPENAI_API_KEY"},
    "codex": {"signup_url": "https://platform.openai.com/api-keys", "env_var": "OPENAI_API_KEY"},
    "claude": {"signup_url": "https://console.anthropic.com/settings/keys", "env_var": "ANTHROPIC_API_KEY"},
    "deepseek": {"signup_url": "https://platform.deepseek.com/api_keys", "env_var": "DEEPSEEK_API_KEY"},
    "grok": {"signup_url": "https://console.x.ai", "env_var": "XAI_API_KEY"},
    "local": {"signup_url": None, "env_var": None},
}


def list_seat_catalog() -> list[dict]:
    """Every key SEAT_CATALOG or the client registry knows about, with
    whether a real client is currently wired up for it (not just
    listed) -- used to render the Providers panel honestly."""
    keys = sorted(set(SEAT_CATALOG) | set(PROVIDER_INFO))
    catalog = []
    for key in keys:
        registered = get_client(key)
        display_name = registered.display_name if registered else SEAT_CATALOG.get(key, key)
        catalog.append({"key": key, "display_name": display_name, "has_real_client": registered is not None})
    return catalog


def provider_setup_info(key: str) -> dict:
    key = key.lower()
    info = PROVIDER_INFO.get(key, {"signup_url": None, "env_var": None})
    registered = get_client(key)
    display_name = registered.display_name if registered else SEAT_CATALOG.get(key, key)

    if info["env_var"] is None:
        powershell = "# no API key needed -- run a model on this machine instead (e.g. Ollama)"
    else:
        powershell = (
            f'$env:{info["env_var"]} = "paste-your-key-here"\n'
            f"cd \"{Path.cwd()}\"\n"
            f"python -m council_chamber.web_ui"
        )

    return {
        "key": key,
        "display_name": display_name,
        "has_real_client": registered is not None,
        "signup_url": info["signup_url"],
        "env_var": info["env_var"],
        "powershell": powershell,
    }


def execute_command(tui: CouncilTUI, line: str) -> dict:
    try:
        return {"output": tui.execute(line)}
    except Exception as exc:  # the TUI's own commands already raise clear, typed errors
        return {"error": str(exc)}


PAGE_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><title>One-Wave Council Chamber</title>
<style>
  body { font-family: -apple-system, Segoe UI, sans-serif; margin: 0; display: flex; height: 100vh;
         background: #0f1115; color: #e6e6e6; }
  #chat { flex: 2; display: flex; flex-direction: column; border-right: 1px solid #2a2d34; }
  #transcript { flex: 1; overflow-y: auto; padding: 12px; white-space: pre-wrap; font-family: monospace; }
  #inputRow { display: flex; border-top: 1px solid #2a2d34; }
  #cmd { flex: 1; padding: 10px; background: #1a1d24; color: #e6e6e6; border: none; font-family: monospace; }
  button { background: #2a2d34; color: #e6e6e6; border: 1px solid #3a3d44; padding: 8px 12px; cursor: pointer; }
  button:hover { background: #3a3d44; }
  #providers { flex: 1; overflow-y: auto; padding: 12px; }
  .provider { border: 1px solid #2a2d34; border-radius: 6px; padding: 8px; margin-bottom: 8px; }
  .quick { display: flex; gap: 6px; padding: 8px; border-top: 1px solid #2a2d34; flex-wrap: wrap; }
  pre { background: #1a1d24; padding: 8px; overflow-x: auto; font-size: 12px; }
  a { color: #7ab7ff; }
  .ok { color: #6ee08a; } .warn { color: #e0c86e; }
</style></head>
<body>
  <div id="chat">
    <div id="transcript"></div>
    <div class="quick">
      <button onclick="run('rooms')">rooms</button>
      <button onclick="run('seats')">seats</button>
      <button onclick="run('transcript')">transcript</button>
      <button onclick="run('help')">help</button>
    </div>
    <div id="inputRow">
      <input id="cmd" placeholder="ask Codex hello  /  open groq  /  propose Codex file.py &quot;...&quot;"
             onkeydown="if(event.key==='Enter') send()">
      <button onclick="send()">Send</button>
    </div>
  </div>
  <div id="providers">
    <h3>Providers</h3>
    <div id="providerList"></div>
  </div>
<script>
async function run(line) {
  const res = await fetch('/api/execute', {method:'POST', headers:{'Content-Type':'application/json'},
                                            body: JSON.stringify({line})});
  const data = await res.json();
  const t = document.getElementById('transcript');
  t.textContent += '> ' + line + '\\n' + (data.output || data.error || '') + '\\n\\n';
  t.scrollTop = t.scrollHeight;
}
function send() {
  const box = document.getElementById('cmd');
  if (!box.value.trim()) return;
  run(box.value);
  box.value = '';
}
async function loadProviders() {
  const res = await fetch('/api/providers');
  const list = await res.json();
  const el = document.getElementById('providerList');
  el.innerHTML = '';
  for (const p of list) {
    const div = document.createElement('div');
    div.className = 'provider';
    const status = p.has_real_client ? '<span class="ok">real client wired</span>'
                                      : '<span class="warn">not wired yet</span>';
    div.innerHTML = `<b>${p.display_name}</b> (${status})<br>
      <button onclick="showSetup('${p.key}')">show setup</button>
      <button onclick="run('open ${p.key}')">open ${p.key}</button>
      <div id="setup-${p.key}"></div>`;
    el.appendChild(div);
  }
}
async function showSetup(key) {
  const res = await fetch('/api/provider/' + key);
  const info = await res.json();
  const div = document.getElementById('setup-' + key);
  const link = info.signup_url ? `<a href="${info.signup_url}" target="_blank">get a key</a><br>` : '';
  div.innerHTML = link + '<pre>' + info.powershell + '</pre>' +
                  '<button onclick="copyText(\\'' + key + '\\')">copy</button>';
  div.dataset.ps = info.powershell;
}
function copyText(key) {
  const div = document.getElementById('setup-' + key);
  navigator.clipboard.writeText(div.dataset.ps);
}
loadProviders();
run('rooms');
</script>
</body></html>"""


class CouncilHTTPServer(ThreadingHTTPServer):
    def __init__(self, address, handler_cls, tui: CouncilTUI):
        super().__init__(address, handler_cls)
        self.tui = tui


class CouncilRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, obj: dict, status: int = 200) -> None:
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str) -> None:
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (stdlib naming convention)
        if self.path == "/":
            self._send_html(PAGE_HTML)
        elif self.path == "/api/providers":
            self._send_json(list_seat_catalog())
        elif self.path.startswith("/api/provider/"):
            key = self.path.rsplit("/", 1)[-1]
            self._send_json(provider_setup_info(key))
        else:
            self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/api/execute":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
            self._send_json(execute_command(self.server.tui, body.get("line", "")))
        else:
            self.send_error(404)

    def log_message(self, format: str, *args) -> None:  # keep stdout clean
        pass


def serve(tui: CouncilTUI, host: str = "127.0.0.1", port: int = 8765) -> CouncilHTTPServer:
    server = CouncilHTTPServer((host, port), CouncilRequestHandler, tui)
    return server


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    project_dir = Path(argv[0]) if argv else Path.cwd()
    port = int(argv[1]) if len(argv) > 1 else 8765

    tui = CouncilTUI(demo_council(project_dir))
    server = serve(tui, port=port)
    url = f"http://127.0.0.1:{port}/"
    print(f"One-Wave Council Chamber running at {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
