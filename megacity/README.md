# One-room looper

Not a city. One room, one body, bounded switches, save and reload.

```text
#####
#A.S#
#...#
#..G#
#####
```

`A` is the body. `S` is the switch. `G` is the mark. The mark opens only after the switch is on and the body is standing on it. North of the start is a wall. The room rejects that move. The body cannot write the room.

Field is what the room shows now. Void is goal, path, last action, and memory. The parser writes one receipt per loop. Both stay on the receipt.

```bash
python3 -m megacity
python3 -m unittest megacity.test_one_room
```

City scale waits until this room keeps doing this.
