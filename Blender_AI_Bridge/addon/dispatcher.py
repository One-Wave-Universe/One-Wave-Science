"""Command registry and batch execution. No bpy import here on purpose:
this module is exercised by plain-python tests without a running Blender.
"""

import inspect
import traceback


class CommandError(Exception):
    """Recoverable command failure (bad params, missing object, etc)."""


_REGISTRY = {}


def register(name):
    def decorator(fn):
        if name in _REGISTRY:
            raise RuntimeError(f"duplicate command registration: {name}")
        _REGISTRY[name] = fn
        return fn

    return decorator


def is_registered(name):
    return name in _REGISTRY


def command_names():
    return sorted(_REGISTRY)


def describe_commands():
    out = {}
    for name, fn in _REGISTRY.items():
        sig = inspect.signature(fn)
        params = []
        for pname, p in sig.parameters.items():
            entry = {"name": pname}
            if p.default is not inspect.Parameter.empty:
                entry["default"] = p.default
            params.append(entry)
        out[name] = {
            "summary": (inspect.getdoc(fn) or "").strip().splitlines()[0]
            if inspect.getdoc(fn)
            else "",
            "params": params,
        }
    return out


def execute_command(name, params=None):
    params = params or {}
    if name not in _REGISTRY:
        return {
            "ok": False,
            "command": name,
            "result": None,
            "error": f"unknown command: {name}",
        }
    try:
        result = _REGISTRY[name](**params)
        return {"ok": True, "command": name, "result": result, "error": None}
    except CommandError as exc:
        return {"ok": False, "command": name, "result": None, "error": str(exc)}
    except TypeError as exc:
        return {
            "ok": False,
            "command": name,
            "result": None,
            "error": f"bad params for {name}: {exc}",
        }
    except Exception as exc:  # noqa: BLE001 - surface any bpy-side failure to the caller
        return {
            "ok": False,
            "command": name,
            "result": None,
            "error": f"{exc}\n{traceback.format_exc()}",
        }


def execute_commands(commands, stop_on_error=False):
    """Run a batch of {"command", "params"} dicts, returning one result per entry.

    Non-fatal per-command errors never abort the batch (each result carries
    its own ok/error); stop_on_error only short-circuits remaining commands,
    it does not raise.
    """
    results = []
    for entry in commands:
        name = entry.get("command")
        params = entry.get("params") or {}
        result = execute_command(name, params)
        results.append(result)
        if stop_on_error and not result["ok"]:
            break
    return results
