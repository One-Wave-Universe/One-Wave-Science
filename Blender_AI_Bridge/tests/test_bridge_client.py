import json
import socket
import threading

import pytest

from mcp_server.bridge_client import BridgeClient, BridgeError


class FakeBridgeServer:
    """Minimal stand-in for the Blender addon's socket server: same
    newline-delimited JSON protocol, no bpy involved."""

    def __init__(self, handler):
        self.handler = handler
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(1)
        self.port = self._sock.getsockname()[1]
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._stop = False

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop = True
        try:
            self._sock.close()
        except OSError:
            pass

    def _serve(self):
        try:
            conn, _addr = self._sock.accept()
        except OSError:
            return
        buffer = b""
        with conn:
            while not self._stop:
                try:
                    chunk = conn.recv(65536)
                except OSError:
                    break
                if not chunk:
                    break
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if not line.strip():
                        continue
                    payload = json.loads(line)
                    response = self.handler(payload)
                    conn.sendall((json.dumps(response) + "\n").encode("utf-8"))


@pytest.fixture
def fake_server():
    def handler(payload):
        if "commands" in payload:
            return {"ok": True, "results": [{"ok": True, "command": c["command"]} for c in payload["commands"]]}
        return {
            "ok": True,
            "command": payload.get("command"),
            "result": {"echo": payload.get("params")},
            "error": None,
        }

    server = FakeBridgeServer(handler)
    server.start()
    yield server
    server.stop()


def test_execute_command_round_trip(fake_server):
    client = BridgeClient(host="127.0.0.1", port=fake_server.port, timeout=5.0)
    response = client.execute_command("move_object", {"name": "Cube", "x": 1, "y": 2, "z": 3})
    client.close()
    assert response["ok"] is True
    assert response["result"]["echo"] == {"name": "Cube", "x": 1, "y": 2, "z": 3}


def test_execute_commands_batch_round_trip(fake_server):
    client = BridgeClient(host="127.0.0.1", port=fake_server.port, timeout=5.0)
    response = client.execute_commands(
        [{"command": "select_object", "params": {"name": "Cube"}}, {"command": "deselect_all"}]
    )
    client.close()
    assert response["ok"] is True
    assert [r["command"] for r in response["results"]] == ["select_object", "deselect_all"]


def test_connection_refused_raises_bridge_error():
    client = BridgeClient(host="127.0.0.1", port=1, timeout=1.0)
    with pytest.raises(BridgeError):
        client.execute_command("ping")
