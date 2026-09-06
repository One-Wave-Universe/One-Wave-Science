"""G-751 layer map. Comparison object, not a controller."""

from __future__ import annotations

LAYERS = (
    ("low", "primitive_cell", "CPG_reflex", "cannot_commit_STOP"),
    ("mid", "M4_hopfield", "cerebellum_skill", "associative_only"),
    ("up", "dream_admin", "descending_policy", "CPU_commits"),
)

VERBS = ("Idle", "Primed", "Executing", "Vectoring", "Resolving")


def layer_may_commit(layer: str) -> bool:
    return layer == "up"


def receipt() -> dict:
    return {
        "layers": LAYERS,
        "verbs": VERBS,
        "kernel_routes": 6,
        "language_required": False,
        "brick": "Yellow",
    }
