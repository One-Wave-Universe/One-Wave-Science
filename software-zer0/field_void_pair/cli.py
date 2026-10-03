#!/usr/bin/env python3
"""fvpair — two AIs in a Field/Void loop through the One-Wave repo lens.

    fvpair run  "goal" [--field anthropic] [--void deepseek] [--turns 8]
    fvpair lens ["query"]           print what both AIs see
    fvpair serve [--port 8742]      app version in the browser
    fvpair providers                which providers have keys set

Algorythm-Zer0 (simulations/zer0_first_cycle.py) referees every turn.
SOFTWARE ONLY.
"""

from __future__ import annotations

import argparse
import sys
import time
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
if __package__ in (None, ""):
    sys.path.insert(0, str(HERE))
    from pair_loop import FieldVoidPair
    from providers import PRESETS, Provider, available
    from repo_lens import RepoLens
    import server as server_mod
else:
    from .pair_loop import FieldVoidPair
    from .providers import PRESETS, Provider, available
    from .repo_lens import RepoLens
    from . import server as server_mod

TRIT_GLYPH = {"+": "+", "-": "-", "0": "0"}


def _provider(spec: str) -> Provider:
    name, _, model = spec.partition(":")
    if name not in PRESETS:
        raise SystemExit(f"unknown provider {name!r}; choose from {', '.join(PRESETS)}")
    return Provider(name=name, model=model or PRESETS[name]["model"])


def _print_turn(rec: dict, verbose: bool) -> None:
    if "error" in rec:
        print(f"\n[turn {rec['turn']}] PROVIDER ERROR: {rec['error']}")
        return
    z = rec["zer0"]
    v = rec["void"]
    ch = z["choices"]
    print(f"\n=== turn {rec['turn']}  ({rec['seconds']}s) ===")
    print("FIELD:", rec["field"]["text"].strip() if verbose else rec["field"]["text"].strip()[:600])
    print(f"VOID : {v['verdict']}  ref={v['reference']:+.2f}  goal={v['goal']:+.2f}  {v['note']}")
    print(f"cites: exist={len(rec['citations']['exist'])} missing={len(rec['citations']['missing'])}")
    print(f"ZER0 : X{ch['X']} Y{ch['Y']} Z{ch['Z']} (T timing) -> {z['resolved']}   "
          f"r {z['ref_in']:+.3f} -> {z['ref_out']:+.3f}")
    if rec["stop"]:
        print("STOP :", rec["stop"])


def cmd_run(a) -> int:
    lens = RepoLens.build(canon_chars=a.canon_chars)
    snap = lens.snapshot()
    print(f"REFERENCE POINT ZERO  root={snap['root']} branch={snap['branch']} "
          f"head={snap['head']} dirty={snap['dirty']}  files={len(lens.files)}")
    pair = FieldVoidPair(goal=a.goal, field_ai=_provider(a.field), void_ai=_provider(a.void),
                         lens=lens, max_turns=a.turns, snapshot=snap)
    print(f"FIELD={pair.field_ai.name}:{pair.field_ai.model}  VOID={pair.void_ai.name}:{pair.void_ai.model}")
    pair.run(on_turn=lambda r: _print_turn(r, a.verbose))
    s = pair.summary()
    out = Path(a.out) if a.out else (
        Path.home() / ".local/share/fvpair/runs" / time.strftime("run-%Y%m%d-%H%M%S.jsonl"))
    pair.write_ledger(out)
    print(f"\nSOFTWARE_ONLY  stop={s['stop']}  turns={s['turns']}  final r={s['final_ref']:+.3f}")
    print("ledger:", out)
    if s["confirmed"]:
        print("\n--- CONFIRMED REFERENCE STATE ---\n" + s["confirmed"])
    return 0 if s["stop"] in ("SETTLED", "HARD_STOP") else 2


def cmd_lens(a) -> int:
    lens = RepoLens.build(canon_chars=a.canon_chars)
    print(lens.render(a.query or ""))
    return 0


def cmd_providers(_a) -> int:
    for p in available():
        key = p["key_env"] or "(no key)"
        print(f"{p['name']:<10} {'ready' if p['ready'] else 'needs ' + key:<26} default model {p['default_model']}")
    return 0


def cmd_serve(a) -> int:
    print("building repo lens ...")
    httpd = server_mod.serve(a.host, a.port, RepoLens.build(canon_chars=a.canon_chars))
    url = f"http://{a.host}:{httpd.server_address[1]}/"
    print(f"Field/Void Pair app at {url}  (Ctrl+C to stop)")
    if not a.no_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="fvpair", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--canon-chars", type=int, default=36_000,
                    help="budget for the canonical-file layer of the lens")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run the Field/Void loop in the terminal")
    r.add_argument("goal")
    r.add_argument("--field", default="offline", help="provider[:model] for Field")
    r.add_argument("--void", default="offline", help="provider[:model] for Void")
    r.add_argument("--turns", type=int, default=8)
    r.add_argument("--out", help="ledger path (.jsonl)")
    r.add_argument("-v", "--verbose", action="store_true")
    r.set_defaults(fn=cmd_run)

    l = sub.add_parser("lens", help="print the repo lens both AIs receive")
    l.add_argument("query", nargs="?")
    l.set_defaults(fn=cmd_lens)

    p = sub.add_parser("providers", help="list providers and key status")
    p.set_defaults(fn=cmd_providers)

    s = sub.add_parser("serve", help="start the app version")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8742)
    s.add_argument("--no-browser", action="store_true")
    s.set_defaults(fn=cmd_serve)

    a = ap.parse_args(argv)
    if getattr(a, "turns", 1) < 1:
        ap.error("--turns must be >= 1")
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
