"""A small registry so a new real provider client can be dropped into
council_chamber/seats/ as a single new file and immediately be usable
from `open <key>` -- no edits to tui.py, or any other existing file,
required. This is the whole mechanism for "someone else builds and
attaches their own seat": follow the shape below, register it, done.

The contract a new file must follow (see seats/gemini_client.py for a
working example):

    def make_<provider>_client(model: str = "...", api_key: str | None = None):
        # ... reads api_key or an env var, raises a clear *NotConfigured*
        # error if neither is set (never fabricates a reply) ...
        def client(context: list[Message]) -> str | tuple[str, UsageReport]:
            # ... makes a real API call, raises a clear *APIError* with
            # the provider's own message on failure ...
            return reply_text, usage
        return client

    from council_chamber.client_registry import register_client
    register_client("<key>", "<Display Name>", make_<provider>_client)

That's the entire interface -- exactly what RemoteAPISeat(seat,
client=...) already accepts. discover_and_register_clients() imports
every council_chamber/seats/*_client.py module so its module-level
register_client() call actually runs; open_catalog_seat() in tui.py
checks this registry before falling back to a MockSeat placeholder.
"""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import Callable


@dataclass
class RegisteredClient:
    key: str
    display_name: str
    factory: Callable[..., Callable]  # (model=..., api_key=...) -> client callable


_REGISTRY: dict[str, RegisteredClient] = {}


def register_client(key: str, display_name: str, factory: Callable[..., Callable]) -> None:
    """Last registration for a given key wins -- if two files register
    the same key, whichever was imported most recently is used, rather
    than raising and blocking discovery of everything else."""
    _REGISTRY[key.lower()] = RegisteredClient(key=key.lower(), display_name=display_name, factory=factory)


def get_client(key: str) -> RegisteredClient | None:
    return _REGISTRY.get(key.lower())


def registered_clients() -> dict[str, RegisteredClient]:
    return dict(_REGISTRY)


def find_client_for_name(name: str) -> RegisteredClient | None:
    """Match an existing seat's display name (e.g. from a reloaded
    session, where only the Seat identity survives) back to a
    registered client, by key or by display name, case-insensitively."""
    name_lower = name.lower()
    for registered in _REGISTRY.values():
        if registered.key == name_lower or registered.display_name.lower() == name_lower:
            return registered
    return None


def build_ai_seat(seat, placeholder_reply: str):
    """Given an existing Seat identity, return a RemoteAPISeat backed by
    a matching registered real client, or a MockSeat placeholder
    otherwise (including when the matching factory can't configure
    itself, e.g. no API key set) -- honest either way, never a
    fabricated reply. Used by both tui.py's `open` and worker_ant.py's
    session-reload reattachment so the two paths behave identically."""
    from council_chamber.seats.ai_seat import MockSeat, RemoteAPISeat

    registered = find_client_for_name(seat.name)
    if registered is None:
        return MockSeat(seat, reply=placeholder_reply)
    try:
        client = registered.factory()
    except Exception as exc:
        return MockSeat(seat, reply=f"({registered.display_name} seat not configured: {exc})")
    return RemoteAPISeat(seat, client=client)


def discover_and_register_clients() -> list[str]:
    """Import every council_chamber/seats/*_client.py module so its
    module-level register_client() call runs. Returns the list of
    module names imported. Safe to call more than once -- re-importing
    an already-imported module is a cheap no-op in Python."""
    from council_chamber import seats as seats_pkg

    imported = []
    for module_info in pkgutil.iter_modules(seats_pkg.__path__):
        if module_info.name.endswith("_client"):
            importlib.import_module(f"council_chamber.seats.{module_info.name}")
            imported.append(module_info.name)
    return imported
