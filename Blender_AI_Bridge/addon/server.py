"""TCP bridge server.

Blender's Python API is only safe to call from the main thread, so this
server never spawns a request-handling thread. Instead a modal operator
ticks a non-blocking accept/recv loop on a timer, and every request is
dispatched synchronously from that same tick.
"""

import json
import socket

import bpy

from . import dispatcher
from .framing import split_frames

HOST = "127.0.0.1"
DEFAULT_PORT = 9876


def handle_request(payload):
    """payload: parsed JSON dict. Returns a JSON-serializable response dict."""
    if "commands" in payload:
        results = dispatcher.execute_commands(
            payload["commands"], stop_on_error=bool(payload.get("stop_on_error"))
        )
        return {"ok": all(r["ok"] for r in results), "results": results}

    name = payload.get("command")
    params = payload.get("params") or {}
    return dispatcher.execute_command(name, params)


class BridgeServer:
    def __init__(self, host=HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self._listener = None
        self._conn = None
        self._buffer = b""

    @property
    def running(self):
        return self._listener is not None

    def start(self):
        if self.running:
            return
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listener.bind((self.host, self.port))
        self._listener.listen(1)
        self._listener.setblocking(False)

    def stop(self):
        for sock in (self._conn, self._listener):
            if sock is not None:
                try:
                    sock.close()
                except OSError:
                    pass
        self._conn = None
        self._listener = None
        self._buffer = b""

    def tick(self):
        if not self.running:
            return
        if self._conn is None:
            try:
                self._conn, _addr = self._listener.accept()
                self._conn.setblocking(False)
            except BlockingIOError:
                return

        try:
            chunk = self._conn.recv(65536)
        except BlockingIOError:
            return
        except (ConnectionResetError, OSError):
            self._close_connection()
            return

        if chunk == b"":
            self._close_connection()
            return

        self._buffer += chunk
        frames, self._buffer = split_frames(self._buffer)
        for frame in frames:
            self._respond(frame)

    def _respond(self, frame):
        try:
            payload = json.loads(frame)
            response = handle_request(payload)
        except json.JSONDecodeError as exc:
            response = {"ok": False, "error": f"invalid JSON: {exc}"}
        except Exception as exc:  # noqa: BLE001
            response = {"ok": False, "error": str(exc)}

        try:
            self._conn.sendall((json.dumps(response) + "\n").encode("utf-8"))
        except OSError:
            self._close_connection()

    def _close_connection(self):
        if self._conn is not None:
            try:
                self._conn.close()
            except OSError:
                pass
        self._conn = None
        self._buffer = b""


_server = BridgeServer()


def get_server():
    return _server


class AIBRIDGE_OT_start_server(bpy.types.Operator):
    bl_idname = "aibridge.start_server"
    bl_label = "Start AI Bridge Server"

    _timer = None

    def modal(self, context, event):
        if event.type == "TIMER":
            _server.tick()
        if not _server.running:
            self._cancel(context)
            return {"FINISHED"}
        return {"PASS_THROUGH"}

    def execute(self, context):
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        _server.host = prefs.host
        _server.port = prefs.port
        try:
            _server.start()
        except OSError as exc:
            self.report({"ERROR"}, f"Could not start AI Bridge server: {exc}")
            return {"CANCELLED"}
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.05, window=context.window)
        wm.modal_handler_add(self)
        self.report({"INFO"}, f"AI Bridge listening on {_server.host}:{_server.port}")
        return {"RUNNING_MODAL"}

    def _cancel(self, context):
        if self._timer is not None:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None


class AIBRIDGE_OT_stop_server(bpy.types.Operator):
    bl_idname = "aibridge.stop_server"
    bl_label = "Stop AI Bridge Server"

    def execute(self, context):
        _server.stop()
        self.report({"INFO"}, "AI Bridge server stopped")
        return {"FINISHED"}


CLASSES = (AIBRIDGE_OT_start_server, AIBRIDGE_OT_stop_server)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    _server.stop()
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
