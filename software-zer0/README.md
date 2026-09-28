# software-zer0 — SOFTWARE ONLY

Not the cell. Two files that serve the analog build.

| File | Job |
|---|---|
| `coupled_loop.py` | BC–DC brain + TC–AC body + reinjection |
| `bench_assist.py` | score measured voltages |

`engine.py` (one walker) was deleted. It did not couple the machines and led nowhere.

```bash
python3 software-zer0/coupled_loop.py
python3 software-zer0/bench_assist.py score --vp 2.1 --vm 1.7 --center 1.9
```
