import os
import uuid

import bpy

from .. import dispatcher
from ..dispatcher import register
from ..state import get_scene_state
from ..utils import CommandError

_TXN_DIR = None
_ACTIVE_TXN = None  # {"id": str, "path": str}


def _txn_dir():
    global _TXN_DIR
    if _TXN_DIR is None:
        _TXN_DIR = os.path.join(bpy.app.tempdir, "ai_bridge_transactions")
        os.makedirs(_TXN_DIR, exist_ok=True)
    return _TXN_DIR


@register("save_blend")
def save_blend():
    if not bpy.data.filepath:
        raise CommandError("file has never been saved; use save_blend_as(path) first")
    bpy.ops.wm.save_mainfile()
    return {"path": bpy.data.filepath}


@register("save_blend_as")
def save_blend_as(path):
    bpy.ops.wm.save_as_mainfile(filepath=path)
    return {"path": bpy.data.filepath}


@register("undo")
def undo():
    bpy.ops.ed.undo()
    return get_scene_state()


@register("redo")
def redo():
    bpy.ops.ed.redo()
    return get_scene_state()


@register("begin_transaction")
def begin_transaction():
    """Start a transaction by snapshotting the current .blend to a scratch file.

    Blender's undo stack isn't introspectable from Python in a
    version-stable way, so rollback is implemented as reload-from-snapshot
    instead of counting undo steps.
    """
    global _ACTIVE_TXN
    if _ACTIVE_TXN is not None:
        raise CommandError(
            f"transaction {_ACTIVE_TXN['id']} already active; commit or roll it back first"
        )
    txn_id = uuid.uuid4().hex
    path = os.path.join(_txn_dir(), f"{txn_id}.blend")
    original_path = bpy.data.filepath
    bpy.ops.wm.save_as_mainfile(filepath=path, copy=True)
    _ACTIVE_TXN = {"id": txn_id, "path": path, "original_path": original_path}
    return {"transaction_id": txn_id}


def _end_transaction(expected_id):
    global _ACTIVE_TXN
    if _ACTIVE_TXN is None:
        raise CommandError("no active transaction")
    if expected_id and expected_id != _ACTIVE_TXN["id"]:
        raise CommandError(
            f"transaction id mismatch: active={_ACTIVE_TXN['id']} given={expected_id}"
        )
    txn = _ACTIVE_TXN
    _ACTIVE_TXN = None
    return txn


@register("commit_transaction")
def commit_transaction(transaction_id=None):
    txn = _end_transaction(transaction_id)
    try:
        os.remove(txn["path"])
    except OSError:
        pass
    return {"transaction_id": txn["id"], "committed": True}


@register("rollback_transaction")
def rollback_transaction(transaction_id=None):
    """Reload the pre-transaction snapshot.

    This does NOT write to the original file on disk. bpy.data.filepath
    now points at the internal snapshot copy; call
    save_blend_as(original_path) if the rollback should be persisted.
    The snapshot file itself is left in place (not deleted) so that
    save/reload of it keeps working.
    """
    txn = _end_transaction(transaction_id)
    bpy.ops.wm.open_mainfile(filepath=txn["path"])
    return {
        "transaction_id": txn["id"],
        "rolled_back": True,
        "original_path": txn["original_path"] or None,
        "scene_state": get_scene_state(),
    }


@register("list_commands")
def list_commands():
    return dispatcher.describe_commands()
