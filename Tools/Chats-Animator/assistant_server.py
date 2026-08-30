#!/usr/bin/env python3
import json
import os
import re
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PORT = int(os.environ.get('ONE_WAVE_ANIMATOR_PORT', '8765'))
MODEL = os.environ.get('ONE_WAVE_AI_MODEL', '').strip()
BACKEND = os.environ.get('ONE_WAVE_AI_BACKEND', 'auto').strip().lower()
CUSTOM_URL = os.environ.get('ONE_WAVE_AI_URL', '').strip()
API_KEY = os.environ.get('ONE_WAVE_AI_API_KEY', '').strip()

SYSTEM = '''You are the live AI creative partner inside One-Wave Animator. The human and AI are the primary creative participants. Together they discuss, direct, create, and revise scenes. Dream/Director may also delegate small routine creative jobs to automatic helpers when useful; those helpers are support machinery, not replacement creative agents.
Return JSON only with this shape:
{"message":"natural reply to the human","steps":[{"operation":"...","args":{}}],"missing":[{"kind":"motion|background|character|prop","actor":"","action":"","target":""}]}
Use only operations supplied in context.operations. Never invent operations. If the human is discussing or brainstorming rather than requesting an executable edit, reply naturally in message and leave steps empty. If art or motion frames are needed but cannot be produced through an available operation, describe that need in missing so it can be delegated to an asset/motion worker. Keep the reply concise and useful.'''


def request_json(url, payload=None, headers=None, timeout=120):
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        **(headers or {}),
    }, method='GET' if payload is None else 'POST')
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))


def strip_json(text):
    text = str(text or '').strip()
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.I)
    text = re.sub(r'\s*```$', '', text)
    start, end = text.find('{'), text.rfind('}')
    if start >= 0 and end > start:
        text = text[start:end + 1]
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError('AI response was not a JSON object')
    obj.setdefault('message', '')
    obj.setdefault('steps', [])
    obj.setdefault('missing', [])
    return obj


def ollama_candidates():
    if CUSTOM_URL and BACKEND in ('auto', 'ollama'):
        base = CUSTOM_URL.rstrip('/')
        yield base if base.endswith('/api/chat') else base + '/api/chat'
    yield 'http://127.0.0.1:11434/api/chat'
    yield 'http://192.168.55.1:11434/api/chat'


def choose_ollama_model(chat_url):
    if MODEL:
        return MODEL
    tags_url = chat_url.rsplit('/api/chat', 1)[0] + '/api/tags'
    tags = request_json(tags_url, timeout=3)
    models = tags.get('models') or []
    if not models:
        raise RuntimeError('Ollama is reachable but has no models installed')
    return models[0].get('name') or models[0].get('model')


def discover_ollama():
    errors = []
    for url in dict.fromkeys(ollama_candidates()):
        try:
            model = choose_ollama_model(url)
            return {'connected': True, 'backend': 'ollama', 'model': model, 'url': url}
        except Exception as exc:
            errors.append(f'{url}: {exc}')
    return {'connected': False, 'backend': 'ollama', 'model': MODEL or '', 'error': ' | '.join(errors)}


def call_ollama(packet):
    found = discover_ollama()
    if not found['connected']:
        raise RuntimeError('No reachable Ollama AI. Tried local computer and Jetson. ' + found.get('error', ''))
    url, model = found['url'], found['model']
    result = request_json(url, {
        'model': model,
        'stream': False,
        'format': 'json',
        'messages': [
            {'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': json.dumps(packet, separators=(',', ':'))},
        ],
    }, timeout=120)
    content = ((result.get('message') or {}).get('content') or '')
    parsed = strip_json(content)
    parsed['_backend'] = {'type': 'ollama', 'model': model, 'url': url}
    return parsed


def call_openai_compatible(packet):
    if not CUSTOM_URL:
        raise RuntimeError('ONE_WAVE_AI_URL is required for openai-compatible mode')
    headers = {}
    if API_KEY:
        headers['Authorization'] = f'Bearer {API_KEY}'
    payload = {
        'model': MODEL or 'default',
        'messages': [
            {'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': json.dumps(packet, separators=(',', ':'))},
        ],
        'response_format': {'type': 'json_object'},
    }
    result = request_json(CUSTOM_URL, payload, headers=headers, timeout=120)
    choices = result.get('choices') or []
    content = (((choices[0] if choices else {}).get('message') or {}).get('content') or '')
    parsed = strip_json(content)
    parsed['_backend'] = {'type': 'openai-compatible', 'model': MODEL or 'default', 'url': CUSTOM_URL}
    return parsed


def call_ai(packet):
    if BACKEND == 'openai-compatible':
        return call_openai_compatible(packet)
    return call_ollama(packet)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/api/assistant/health':
            if BACKEND == 'openai-compatible':
                connected = bool(CUSTOM_URL)
                return self.send_json(200, {
                    'ok': True,
                    'server': True,
                    'connected': connected,
                    'backend': BACKEND,
                    'model': MODEL or 'default',
                    'error': '' if connected else 'ONE_WAVE_AI_URL is not configured'
                })
            info = discover_ollama()
            return self.send_json(200, {'ok': True, 'server': True, **info})
        return super().do_GET()

    def do_POST(self):
        if self.path != '/api/assistant':
            return self.send_json(404, {'ok': False, 'error': 'Not found'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            packet = json.loads(self.rfile.read(length).decode('utf-8'))
            result = call_ai(packet)
            return self.send_json(200, {'ok': True, 'result': result})
        except Exception as exc:
            return self.send_json(503, {'ok': False, 'error': str(exc)})


if __name__ == '__main__':
    os.chdir(APP_DIR)
    server = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    print(f'One-Wave Animator live server: http://127.0.0.1:{PORT}', flush=True)
    print('AI backend:', BACKEND, 'model:', MODEL or 'auto', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
