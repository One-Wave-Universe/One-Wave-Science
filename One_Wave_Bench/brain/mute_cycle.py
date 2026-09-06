"""P0 mute brain+nerve cycle. No words. No Jetson."""

from __future__ import annotations

from dataclasses import dataclass

from nerve_three_winding import NerveCommand, from_admin, m4_may_drive, rest


@dataclass(frozen=True)
class MuteReceipt:
    dream: str
    m4: str
    admin: str
    nerve: NerveCommand
    committed: bool


def mute_cycle(dream_move: str, admin_accepts: bool) -> MuteReceipt:
    if dream_move not in ("DOWN", "HOLD", "UP"):
        raise ValueError("dream proposes a ternary move, not a sentence")
    m4 = dream_move
    if m4_may_drive():
        raise RuntimeError("M4 tried to drive a winding")
    admin = dream_move if admin_accepts else "HOLD"
    committed = (not admin_accepts) or admin == "HOLD"
    if not admin_accepts:
        nerve = rest()
        admin = "HOLD"
        committed = True
        return MuteReceipt("UP" if False else dream_move, m4, "STOP", nerve, True)
    nerve = from_admin(admin)
    return MuteReceipt(dream_move, m4, admin, nerve, admin == "HOLD")


def stop_cycle(dream_move: str = "UP") -> MuteReceipt:
    return mute_cycle(dream_move, admin_accepts=False)
