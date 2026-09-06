"""G-756 countable contract."""

KERNEL = {
    "field_void": 1,
    "choices": 2,
    "moves": 3,
    "views_or_actions": 4,
    "lifecycle_verbs": 5,
    "gates": 6,
}

VERBS = ("Idle", "Primed", "Executing", "Vectoring", "Resolving")
SCALES = ("micro", "small", "mid", "large", "macro")
LOOPS = ("DC", "AC", "QC")
THRESHOLD_BANDS = (
    (100, 90), (85, 75), (70, 60), (55, 45), (40, 30), (25, 15), (15, 0),
)
THERMAL = ("fire", "hot", "warm", "cool", "cold", "frozen")
TENSION = ("compress", "express", "tension", "release", "snap")
NERVE_TO_BRAIN = (3, 1)


def extra_axes_allowed() -> bool:
    return False
