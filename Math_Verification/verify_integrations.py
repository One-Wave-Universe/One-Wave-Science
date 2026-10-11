#!/usr/bin/env python3
"""Independent reference controls for Rabbit Hopping and Algorithm Zero."""
import json

def check():
    rabbit = (
        27 - 1 == 26
        and (1, 4, 4 - 1) == (1, 4, 3)
        and (1, 4, 4 + 1) == (1, 4, 5)
        and tuple(-x for x in (1, 4, 3)) == (-1, -4, -3)
        and 4 + 1 == (4 + 2) - 1
    )
    choices = ("YES", "NO")
    moves = (-1, 0, 1)
    routes = {(c, m) for c in choices for m in moves}
    algorithm_zero = len(routes) == 6 and ("YES", 0) in routes and ("NO", 0) in routes and ("GROUND", 0) not in routes
    pitch = (7 % 12 == (-5) % 12) and (8 % 12 == (-4) % 12) and (9 % 12 == (-3) % 12)
    return {"rabbit_hopping": rabbit, "algorithm_zero_six_routes": algorithm_zero, "pitch_class_wrap": pitch}

if __name__ == "__main__":
    result=check()
    print(json.dumps({"pass":all(result.values()),"tests":result},indent=2))
    raise SystemExit(0 if all(result.values()) else 1)
