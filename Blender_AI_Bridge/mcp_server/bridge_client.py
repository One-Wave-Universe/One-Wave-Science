import json
import socket
import threading


class BridgeError(Exception):
    """Raised when the socket connection to the Blender addon fails."""


class BridgeClient:
    def __init__(self, host="127.0.0.1", port=9876, timeout=15.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock = None
        self._buffer = b""
        self._lock = threading.Lock()

    def connect(self):
        if self._sock is not None:
            return
        try:
            sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        except OSError as exc:
            raise BridgeError(
                f"could not reach Blender AI Bridge at {self.host}:{self.port} "
                f"(is Blender open with the addon's server started?): {exc}"
            ) from exc
        sock.settimeout(self.timeout)
        self._sock = sock
        self._buffer = b""

    def close(self):
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
        self._sock = None
        self._buffer = b""

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def _recv_line(self):
        while b"\n" not in self._buffer:
            chunk = self._sock.recv(65536)
            if not chunk:
                raise BridgeError("connection closed by Blender bridge")
            self._buffer += chunk
        line, self._buffer = self._buffer.split(b"\n", 1)
        return line

    def _request(self, payload):
        with self._lock:
            self.connect()
            data = (json.dumps(payload) + "\n").encode("utf-8")
            try:
                self._sock.sendall(data)
                line = self._recv_line()
            except (OSError, socket.timeout) as exc:
                self.close()
                raise BridgeError(f"bridge communication failed: {exc}") from exc
            try:
                return json.loads(line)
            except json.JSONDecodeError as exc:
                raise BridgeError(f"invalid response from bridge: {exc}") from exc

    def execute_command(self, command, params=None):
        return self._request({"command": command, "params": params or {}})

    def execute_commands(self, commands, stop_on_error=False):
        return self._request({"commands": commands, "stop_on_error": stop_on_error})
