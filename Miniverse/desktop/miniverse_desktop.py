#!/usr/bin/env python3
"""Native GTK/WebKit shell for the One-Wave Miniverse room.

The Jetson room stays bound to 127.0.0.1. This desktop app opens a dedicated
SSH tunnel, then embeds the room in a normal desktop application window.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import threading
import time
from urllib.request import urlopen

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")
from gi.repository import GLib, Gtk, WebKit2

APP_ID = "org.onewave.Miniverse"
APP_NAME = "One-Wave Miniverse"
CONFIG_PATH = Path.home() / ".config/one-wave-miniverse/desktop.json"
DEFAULT_CONFIG = {
    "remote_user": "Scales",
    "host_candidates": ["192.168.55.1", "192.168.4.45"],
    "ssh_key": "~/.ssh/one_wave_miniverse_ed25519",
    "local_port": 18787,
    "remote_port": 8787,
}


def load_config() -> dict:
    config = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        try:
            user = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(user, dict):
                config.update(user)
        except (OSError, ValueError):
            pass
    return config


def room_url(config: dict) -> str:
    return f"http://127.0.0.1:{int(config['local_port'])}/"


def health_ok(config: dict, timeout: float = 0.4) -> bool:
    try:
        with urlopen(room_url(config) + "api/health", timeout=timeout) as response:
            data = json.load(response)
        return bool(data.get("ok")) and data.get("service") == "miniverse-room"
    except Exception:
        return False


class TunnelManager:
    def __init__(self, config: dict):
        self.config = config
        self.process: subprocess.Popen | None = None
        self.host: str | None = None
        self.owned = False

    def start(self) -> str:
        if health_ok(self.config):
            self.owned = False
            return "existing local tunnel"

        key = Path(os.path.expanduser(str(self.config["ssh_key"])))
        if not key.is_file():
            raise RuntimeError(f"SSH key missing: {key}")

        local_port = int(self.config["local_port"])
        remote_port = int(self.config["remote_port"])
        user = str(self.config["remote_user"])
        errors = []

        for host in self.config.get("host_candidates", []):
            cmd = [
                "ssh", "-i", str(key), "-N",
                "-L", f"{local_port}:127.0.0.1:{remote_port}",
                "-o", "BatchMode=yes",
                "-o", "IdentitiesOnly=yes",
                "-o", "ExitOnForwardFailure=yes",
                "-o", "ConnectTimeout=4",
                "-o", "ServerAliveInterval=15",
                "-o", "ServerAliveCountMax=3",
                "-o", "StrictHostKeyChecking=accept-new",
                f"{user}@{host}",
            ]
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            for _ in range(35):
                if health_ok(self.config, timeout=0.2):
                    self.process = proc
                    self.host = host
                    self.owned = True
                    return host
                if proc.poll() is not None:
                    break
                time.sleep(0.1)
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    proc.kill()
            errors.append(host)

        raise RuntimeError("Could not reach the Jetson through: " + ", ".join(errors))

    def stop(self) -> None:
        if self.owned and self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()


class MiniverseWindow(Gtk.ApplicationWindow):
    def __init__(self, app: Gtk.Application):
        super().__init__(application=app, title=APP_NAME)
        self.set_default_size(1280, 820)
        self.set_size_request(900, 600)
        self.config = load_config()
        self.tunnel = TunnelManager(self.config)

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = APP_NAME
        header.props.subtitle = "connecting to Jetson"
        self.header = header
        self.set_titlebar(header)

        refresh = Gtk.Button.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON)
        refresh.set_tooltip_text("Reload world")
        refresh.connect("clicked", lambda _button: self.web.reload())
        header.pack_end(refresh)

        reconnect = Gtk.Button.new_with_label("Reconnect")
        reconnect.connect("clicked", lambda _button: self.connect_room())
        header.pack_end(reconnect)

        self.web = WebKit2.WebView()
        settings = self.web.get_settings()
        settings.set_enable_javascript(True)
        settings.set_enable_webgl(True)
        settings.set_enable_developer_extras(True)
        self.add(self.web)

        self.connect("delete-event", self._on_delete)
        self.show_all()
        self._show_status("Connecting securely to the Jetson...")
        self.connect_room()

    def _show_status(self, message: str) -> None:
        safe = GLib.markup_escape_text(message)
        html = """<!doctype html><html><body style='background:#071015;color:#6df6ff;
        font-family:monospace;display:grid;place-items:center;height:100vh;margin:0'>
        <div><h2>ONE-WAVE MINIVERSE</h2><p>%s</p></div></body></html>""" % safe
        self.web.load_html(html, "about:blank")

    def connect_room(self) -> None:
        self.header.props.subtitle = "connecting..."
        self._show_status("Opening the private Miniverse bridge...")
        threading.Thread(target=self._connect_worker, daemon=True).start()

    def _connect_worker(self) -> None:
        try:
            host = self.tunnel.start()
            GLib.idle_add(self._connected, host)
        except Exception as exc:
            GLib.idle_add(self._failed, str(exc))

    def _connected(self, host: str) -> bool:
        self.header.props.subtitle = f"live through {host}"
        self.web.load_uri(room_url(self.config))
        return False

    def _failed(self, message: str) -> bool:
        self.header.props.subtitle = "offline"
        self._show_status(message + " — use Reconnect after the Jetson is reachable.")
        return False

    def _on_delete(self, *_args) -> bool:
        self.tunnel.stop()
        return False


class MiniverseApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)

    def do_activate(self):
        window = self.props.active_window
        if window is None:
            window = MiniverseWindow(self)
        window.present()


def main() -> int:
    return MiniverseApplication().run(None)


if __name__ == "__main__":
    raise SystemExit(main())
