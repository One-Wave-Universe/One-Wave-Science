# software-zer0 — SOFTWARE ONLY

Not the cell. Helpers that *serve* the analog build.

| File | Job |
|---|---|
| `engine.py` | grammar flip on numbers |
| `bench_assist.py` | score measured voltages for the breadboard tests |
| `SEPARATE.md` | do not merge with iron |

## Bench helper (use this at the table)

```bash
# one axis: tips + CENTER
python3 software-zer0/bench_assist.py score --vp 2.1 --vm 1.7 --center 1.9 --vbus 3.3

# retained-state: same probe after + write vs after - write
python3 software-zer0/bench_assist.py history --probe-a 0.82 --probe-b 0.61 --noise 0.05

# three measured D values
python3 software-zer0/bench_assist.py triad --da 0.3 --db 0.25 --dc -0.05
```

It will yell if CENTER equals V_BUS. History fail means stop and revise the nucleus — software does not get a vote.
