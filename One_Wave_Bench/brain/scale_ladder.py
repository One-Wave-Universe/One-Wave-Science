"""G-754 scale ladder."""

LADDER = ("cell", "chip", "cube", "rubik", "two_rubiks")

SEATS = {
    "cell": "nerve",
    "chip": "nerve_plus_ground",
    "cube": "local_loop",
    "rubik": "one_state_machine",
    "two_rubiks": "dream_and_admin",
    "midline": "m4_route_only",
}


def is_brain(scale: str) -> bool:
    return scale == "two_rubiks"


def m4_commits() -> bool:
    return False
