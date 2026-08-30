#!/usr/bin/env python3
import base64
import json
import os
import re
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PORT = int(os.environ.get("ONE_WAVE_ANIMATOR_PORT", "8765"))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip() or os.environ.get("ONE_WAVE_OPENAI_API_KEY", "").strip()
DIRECTOR_MODEL = os.environ.get("ONE_WAVE_DIRECTOR_MODEL", "gpt-5.6-sol").strip()
IMAGE_MODEL = os.environ.get("ONE_WAVE_IMAGE_MODEL", "gpt-image-2").strip()
OLLAMA_IMAGE_MODEL = os.environ.get("ONE_WAVE_OLLAMA_IMAGE_MODEL", "x/z-image-turbo").strip()
ASSET_BACKEND = os.environ.get("ONE_WAVE_ASSET_BACKEND", "auto").strip().lower()

OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_IMAGE_URL = "https://api.openai.com/v1/images/generations"
OLLAMA_IMAGE_URLS = [
    "http://127.0.0.1:11434/v1/images/generations",
    "http://192.168.55.1:11434/v1/images/generations",
]

SYSTEM = """You are the live OpenAI creative partner inside One-Wave Animator.
The human and you are the primary creative pair. The animator itself handles deterministic editing locally; you are called only when creative judgment, scene planning, or interpretation is needed.

Return JSON only:
{"message":"natural concise reply","steps":[{"operation":"...","args":{}}],"missing":[{"kind":"motion|background|character|prop","actor":"","action":"","target":""}]}

Rules:
- Use only operations listed in context.operations.
- Do not invent controls.
- If the human is brainstorming, answer naturally in message and leave steps empty.
- Prefer existing motion-library material before requesting new art.
- If new art or motion drawings are genuinely needed, put them in missing so the asset worker can create them.
- Keep the human's current frame, scene, character identity, continuity, and timing intact.
- Never replace frame-by-frame animation with a single moving still.
"""


def request_json(url, payload=None, headers=None, timeout=120):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="GET" if payload is None else "POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body[:1200]}") from exc


def strip_json(text):
    text = str(text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end + 1]
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError("Director response was not a JSON object")
    obj.setdefault("message", "")
    obj.setdefault("steps", [])
    obj.setdefault("missing", [])
    return obj


def openai_headers():
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OpenAI API key is not configured. Run ~/.local/share/one-wave-animator/configure-openai.sh"
        )
    return {"Authorization": f"Bearer {OPENAI_API_KEY}"}


def call_director(packet):
    payload = {
        "model": DIRECTOR_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(packet, separators=(",", ":"))},
        ],
        "response_format": {"type": "json_object"},
    }
    result = request_json(OPENAI_CHAT_URL, payload, headers=openai_headers(), timeout=180)
    choices = result.get("choices") or []
    content = (((choices[0] if choices else {}).get("message") or {}).get("content") or "")
    parsed = strip_json(content)
    parsed["_backend"] = {"type": "openai", "model": DIRECTOR_MODEL}
    return parsed


def ollama_image(prompt, kind):
    errors = []
    for url in OLLAMA_IMAGE_URLS:
        try:
            payload = {
                "model": OLLAMA_IMAGE_MODEL,
                "prompt": prompt,
                "size": "1024x1024",
                "response_format": "b64_json",
            }
            result = request_json(url, payload, headers={"Authorization": "Bearer ollama"}, timeout=240)
            data = result.get("data") or []
            b64 = (data[0] if data else {}).get("b64_json")
            if not b64:
                raise RuntimeError("Ollama returned no image bytes")
            return {
                "src": f"data:image/png;base64,{b64}",
                "backend": {"type": "ollama-image", "model": OLLAMA_IMAGE_MODEL, "url": url},
            }
        except Exception as exc:
            errors.append(str(exc))
    raise RuntimeError("Local Ollama image generation unavailable: " + " | ".join(errors))


def openai_image(prompt, kind):
    payload = {
        "model": IMAGE_MODEL,
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "low",
        "output_format": "png",
    }
    if kind in ("character", "prop", "motion"):
        payload["background"] = "transparent"
    result = request_json(OPENAI_IMAGE_URL, payload, headers=openai_headers(), timeout=300)
    data = result.get("data") or []
    item = data[0] if data else {}
    b64 = item.get("b64_json")
    if not b64 and item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as resp:
            b64 = base64.b64encode(resp.read()).decode("ascii")
    if not b64:
        raise RuntimeError("OpenAI image generation returned no image")
    return {
        "src": f"data:image/png;base64,{b64}",
        "backend": {"type": "openai-image", "model": IMAGE_MODEL},
    }


def reference_hint(job):
    project = job.get("project") or {}
    scene = project.get("scene") or {}
    selected = scene.get("selectedAssetId")
    assets = scene.get("assets") or []
    asset = next((a for a in assets if a.get("id") == selected), None)
    if not asset and assets:
        asset = assets[-1]
    if not asset:
        return ""
    return (
        f" Preserve the existing on-file character/prop identity and proportions from "
        f"'{asset.get('name') or asset.get('kind') or 'selected art'}'."
    )


def build_asset_prompt(job):
    kind = str(job.get("kind") or "prop").lower()
    prompt = str(job.get("prompt") or "").strip()
    ref = reference_hint(job)
    if kind == "background":
        return f"Animation background plate, no characters, composition ready for layered frame animation. {prompt}"
    if kind == "motion":
        return (
            "Single clean animation pose drawing on transparent background, full body visible, no text, "
            "same character design and camera angle as the existing art. "
            f"Action/pose: {prompt}.{ref}"
        )
    return (
        f"Single {kind} asset for frame animation on transparent background, isolated, clean silhouette, no text. "
        f"{prompt}.{ref}"
    )


def call_asset(job):
    kind = str(job.get("kind") or "prop").lower()
    prompt = build_asset_prompt(job)

    local_error = ""
    if ASSET_BACKEND in ("auto", "ollama"):
        try:
            made = ollama_image(prompt, kind)
            asset_kind = "character" if kind == "motion" else kind
            return {
                "message": f"Created {kind} art locally with Ollama.",
                "asset": {
                    "kind": asset_kind,
                    "name": f"Generated {kind.title()}.png",
                    "src": made["src"],
                },
                "_backend": made["backend"],
            }
        except Exception as exc:
            local_error = str(exc)
            if ASSET_BACKEND == "ollama":
                raise

    made = openai_image(prompt, kind)
    asset_kind = "character" if kind == "motion" else kind
    message = f"Created {kind} art with OpenAI image generation."
    if local_error:
        message += " Local Ollama art was unavailable, so I used the fallback."
    return {
        "message": message,
        "asset": {
            "kind": asset_kind,
            "name": f"Generated {kind.title()}.png",
            "src": made["src"],
        },
        "_backend": made["backend"],
    }


def health():
    director_connected = bool(OPENAI_API_KEY)
    return {
        "ok": True,
        "server": True,
        "connected": director_connected,
        "backend": "openai-director",
        "model": DIRECTOR_MODEL,
        "asset_backend": ASSET_BACKEND,
        "image_model": IMAGE_MODEL,
        "ollama_image_model": OLLAMA_IMAGE_MODEL,
        "error": "" if director_connected else "OpenAI API key not configured",
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/assistant/health"):
            return self.send_json(200, health())
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/assistant":
            return self.send_json(404, {"ok": False, "error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            packet = json.loads(self.rfile.read(length).decode("utf-8"))
            kind = str(packet.get("kind") or "director").lower()
            payload = packet.get("payload") or {}
            if kind == "asset":
                result = call_asset(payload)
            else:
                result = call_director(packet)
            return self.send_json(200, {"ok": True, "result": result})
        except Exception as exc:
            return self.send_json(503, {"ok": False, "error": str(exc)})


if __name__ == "__main__":
    os.chdir(APP_DIR)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"One-Wave Animator live server: http://127.0.0.1:{PORT}", flush=True)
    print(f"Director: OpenAI {DIRECTOR_MODEL}", flush=True)
    print(f"Asset worker: {ASSET_BACKEND}; fallback {IMAGE_MODEL}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
