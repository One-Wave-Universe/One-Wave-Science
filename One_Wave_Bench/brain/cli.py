"""Command-line entry point for installing and testing the command brain."""

from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
from enum import Enum
import json
from pathlib import Path

from One_Wave_Bench.brain.command_memory import M4DualStateRouter, VerbalCommand
from One_Wave_Bench.brain.jetson_runtime import default_brain_home, detect_jetson
from One_Wave_Bench.brain.receipt_store import ReceiptStore


def _jsonable(value):
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _store(path: str | None) -> ReceiptStore:
    target = Path(path).expanduser() if path else default_brain_home() / "command_memory.jsonl"
    return ReceiptStore(target)


def _cycle_receipt(store: ReceiptStore, phrase: str):
    profile = detect_jetson()
    memory = store.initialize()
    router = M4DualStateRouter(
        memory,
        m4_device=profile.m4_device,
        expressive_device=profile.expressive_device,
        compressive_device=profile.compressive_device,
    )
    receipt = router.route(phrase)
    return profile, receipt


def run_smoke_test(store: ReceiptStore, *, require_jetson: bool) -> dict[str, object]:
    profile = detect_jetson()
    memory = store.initialize()
    router = M4DualStateRouter(
        memory,
        m4_device=profile.m4_device,
        expressive_device=profile.expressive_device,
        compressive_device=profile.compressive_device,
    )
    expected = {
        "follow": VerbalCommand.FOLLOW,
        "hurry up": VerbalCommand.HURRY_UP,
        "slow down": VerbalCommand.SLOW_DOWN,
        "stop": VerbalCommand.STOP,
    }
    command_checks = {}
    for phrase, command in expected.items():
        receipt = router.route(phrase)
        command_checks[phrase] = receipt.compressive_after.committed_command is command
    archive_rebuilt = ReceiptStore(store.path).load().receipts == memory.receipts
    checks = {
        "command_checks": command_checks,
        "archive_rebuilt": archive_rebuilt,
        "gpu_proposal_role": profile.expressive_device == "JETSON_GPU",
        "cpu_commit_role": profile.compressive_device in ("JETSON_CPU", "CPU_REFERENCE"),
        "jetson_required": not require_jetson or profile.hardware_split_ready,
    }
    return {
        "ready": all(command_checks.values()) and archive_rebuilt
                 and checks["cpu_commit_role"] and checks["jetson_required"],
        "profile": profile.receipt,
        "checks": checks,
        "memory_path": str(store.path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="one-wave-brain")
    parser.add_argument("--memory", help="path to the receipt archive")
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("init", help="initialize or verify command memory")
    commands.add_parser("status", help="show Jetson CPU/GPU readiness")
    teach = commands.add_parser("teach", help="teach one exact phrase")
    teach.add_argument("command", choices=[command.value for command in VerbalCommand])
    teach.add_argument("phrase")
    recall = commands.add_parser("recall", help="recall without committing")
    recall.add_argument("phrase")
    cycle = commands.add_parser("cycle", help="run one M4/Dream/Administrator cycle")
    cycle.add_argument("phrase")
    smoke = commands.add_parser("smoke-test", help="verify memory and device split")
    smoke.add_argument("--require-jetson", action="store_true")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    store = _store(args.memory)
    if args.action == "init":
        memory = store.initialize()
        result = {"memory_path": str(store.path), "receipts": len(memory.receipts)}
    elif args.action == "status":
        result = detect_jetson().receipt
    elif args.action == "teach":
        memory = store.teach(args.phrase, VerbalCommand(args.command))
        result = {"memory_path": str(store.path), "receipts": len(memory.receipts)}
    elif args.action == "recall":
        result = store.initialize().recall(args.phrase)
    elif args.action == "cycle":
        profile, receipt = _cycle_receipt(store, args.phrase)
        result = {"profile": profile.receipt, "cycle": receipt}
    else:
        result = run_smoke_test(store, require_jetson=args.require_jetson)
    print(json.dumps(_jsonable(result), indent=2, sort_keys=True))
    return 0 if not isinstance(result, dict) or result.get("ready", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
