#!/usr/bin/env python3
"""Clock sync — wire only. Stamp is stamp. No Gate-7 noun."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal

from circle_of_fifths import slot_for_gray

GEN_HOLD = 0
GEN_CHROMATIC = 1
GEN_FOURTH = 5
GEN_TRITONE = 6
GEN_FIFTH = 7

Stamp = Literal["propose", "commit", "hold", "quit"]
State = Literal["LISTEN", "LOCK", "HOLD", "DRIFT", "QUIT"]
PAIRS = ((1, 4), (2, 5), (3, 6))


def wrap12(n: int) -> int:
    return n % 12


def _stamp_of(pkt) -> str:
    return getattr(pkt, "stamp", None) or getattr(pkt, "gate7", "hold")


@dataclass
class Packet:
    proto: str = "one-wave-clock/1"
    src: str = "M4"
    seq: int = 0
    phase: int = 0
    polarity: int = 0
    generator: int = GEN_FIFTH
    m4_pair: int = 0
    lap: int = 0
    hold: bool = True
    stamp: Stamp = "hold"
    tonic: str = "C"

    def slot(self) -> dict:
        return slot_for_gray(self.phase)

    def as_wire(self) -> dict:
        d = asdict(self)
        d["slot"] = self.slot()
        d["slot"]["midi"] = 60 + self.phase
        return d


def next_phase(phase: int, polarity: int, generator: int, hold: bool) -> int:
    if hold or polarity == 0 or generator == 0:
        return wrap12(phase)
    return wrap12(phase + polarity * generator)


def next_lap(phase: int, new_phase: int, polarity: int, hold: bool, lap: int) -> int:
    if hold or polarity == 0:
        return lap
    if polarity > 0 and new_phase < phase:
        return 1 - lap
    if polarity < 0 and new_phase > phase:
        return 1 - lap
    return lap


@dataclass
class Coordinator:
    phase: int = 0
    polarity: int = 0
    generator: int = GEN_FIFTH
    m4_pair: int = 0
    lap: int = 0
    seq: int = 0
    hold: bool = True
    src: str = "M4"

    def freeze_pair(self, pair: int) -> Packet:
        if pair not in (0, 1, 2):
            raise ValueError("m4_pair must be 0, 1, or 2")
        self.m4_pair = pair
        self.seq += 1
        return self._emit("commit")

    def propose(self, polarity: int) -> Packet:
        self.polarity = int(polarity)
        return self._emit("propose")

    def commit(self) -> Packet:
        if self.hold or self.polarity == 0:
            return self._emit("hold")
        new = next_phase(self.phase, self.polarity, self.generator, False)
        self.lap = next_lap(self.phase, new, self.polarity, False, self.lap)
        self.phase = new
        self.seq += 1
        return self._emit("commit")

    def set_hold(self, hold: bool) -> Packet:
        self.hold = hold
        if hold:
            self.polarity = 0
            return self._emit("hold")
        return self._emit("propose")

    def quit(self) -> Packet:
        self.hold = True
        self.polarity = 0
        self.seq += 1
        return self._emit("quit")

    def _emit(self, stamp: Stamp) -> Packet:
        return Packet(
            src=self.src,
            seq=self.seq,
            phase=self.phase,
            polarity=self.polarity,
            generator=self.generator,
            m4_pair=self.m4_pair,
            lap=self.lap,
            hold=self.hold or stamp in ("hold", "quit"),
            stamp=stamp,
        )


@dataclass
class Follower:
    name: str = "BUCKET-R2"
    phase: int = 0
    m4_pair: int = 0
    lap: int = 0
    last_seq: int = -1
    state: State = "LISTEN"
    generator: int = GEN_FIFTH

    def hear(self, pkt: Packet) -> State:
        st = _stamp_of(pkt)
        if st == "quit":
            self.state = "QUIT"
            return self.state
        if st == "propose":
            return self.state
        if st == "hold" or pkt.hold or pkt.polarity == 0:
            if self.state != "QUIT":
                self.state = "HOLD"
            self.phase = pkt.phase
            self.lap = pkt.lap
            self.last_seq = pkt.seq
            return self.state
        if st != "commit":
            return self.state
        if pkt.m4_pair != self.m4_pair and self.last_seq >= 0:
            self.m4_pair = pkt.m4_pair
        predicted = next_phase(self.phase, pkt.polarity, pkt.generator, False)
        if self.last_seq < 0:
            self.phase = pkt.phase
            self.lap = pkt.lap
            self.m4_pair = pkt.m4_pair
            self.last_seq = pkt.seq
            self.state = "LOCK"
            return self.state
        if pkt.phase == predicted and pkt.seq == self.last_seq + 1:
            self.phase = pkt.phase
            self.lap = pkt.lap
            self.last_seq = pkt.seq
            self.state = "LOCK"
            return self.state
        self.phase = pkt.phase
        self.lap = pkt.lap
        self.last_seq = pkt.seq
        self.state = "DRIFT"
        return self.state


def opposed(drive_a: float, drive_b: float, dead: float = 5.0) -> bool:
    return drive_a * drive_b < 0 and abs(drive_a) >= dead and abs(drive_b) >= dead


def demo() -> None:
    m4 = Coordinator()
    bucket = Follower()
    print("CLOCK SYNC  proto=one-wave-clock/1  gen=+7")
    print(f"{'seq':>4} {'stamp':<7} {'ph':>3} {'pol':>4} {'hold':>5} {'lap':>3} {'follow'}")

    def show(pkt: Packet) -> None:
        st = bucket.hear(pkt)
        print(
            f"{pkt.seq:4d} {pkt.stamp:<7} {pkt.phase:3d} {pkt.polarity:4d} "
            f"{str(pkt.hold):>5} {pkt.lap:3d} {st}"
        )

    show(m4.freeze_pair(0))
    show(m4.set_hold(False))
    m4.propose(+1)
    show(m4.commit())
    show(m4.commit())
    show(m4.commit())
    frozen = m4.phase
    show(m4.set_hold(True))
    show(m4.commit())
    assert m4.phase == frozen, "FALSIFY: phase moved on hold"
    show(m4.set_hold(False))
    m4.propose(+1)
    show(m4.commit())
    if opposed(12.0, -12.0):
        show(m4.quit())
    print()
    print("pair 0 hallway", PAIRS[0], "slot", m4._emit("hold").slot()["tag"])
    print("law: no tick on hold. no slew. snap or sit.")
    print("hold: 1(0)1")


if __name__ == "__main__":
    demo()
