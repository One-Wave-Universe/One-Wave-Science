"""Command-line entry point for installing and testing the command brain."""

from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
from enum import Enum
import json
from pathlib import Path

from One_Wave_Bench.brain.command_memory import (
    M4DualStateRouter,
    QuadraticDirection,
    VerbalCommand,
    VoidDecision,
)
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


def memory_health(store: ReceiptStore) -> dict[str, object]:
    """Inspect durable memory independently of whether the brain speaks."""
    try:
        memory = store.initialize()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        return {
            "healthy": False,
            "receipt_chain_valid": False,
            "error": f"{type(exc).__name__}: {exc}",
            "memory_path": str(store.path),
        }
    archive_stat = store.path.stat()
    experience_path = store.path.with_name("experience.jsonl")
    experience_records = 0
    heard_records = 0
    association_records = 0
    experience_valid = True
    if experience_path.exists():
        try:
            with experience_path.open("r", encoding="utf-8") as stream:
                for line in stream:
                    if line.strip():
                        record = json.loads(line)
                        if not str(record["cue"]).strip():
                            raise ValueError("empty cue")
                        kind = record.get("kind", "association" if "followed_by" in record else None)
                        if kind == "heard":
                            heard_records += 1
                        elif kind == "association":
                            VerbalCommand(record["followed_by"])
                            association_records += 1
                        else:
                            raise ValueError("unknown experience record kind")
                        experience_records += 1
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            experience_valid = False
    receipts = memory.receipts
    return {
        "healthy": experience_valid,
        "receipt_chain_valid": True,
        "receipt_count": len(receipts),
        "known_phrase_count": len({receipt.phrase for receipt in receipts}),
        "latest_receipt_digest": receipts[-1].digest if receipts else None,
        "archive_bytes": archive_stat.st_size,
        "archive_modified_ns": archive_stat.st_mtime_ns,
        "experience_journal_valid": experience_valid,
        "experience_records": experience_records,
        "heard_records": heard_records,
        "association_records": association_records,
        "memory_path": str(store.path),
        "experience_path": str(experience_path),
    }


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
    routing_checks = []
    for phrase, command in expected.items():
        receipt = router.route(phrase)
        command_checks[phrase] = receipt.compressive_after.committed_command is command
        routing_checks.append(
            receipt.upward_direction is QuadraticDirection.VIEWS_UP
            and receipt.downward_direction is QuadraticDirection.ACTIONS_DOWN
            and len(receipt.upward_field_views) == 4
            and len(receipt.upward_void_views) == 4
            and len(receipt.downward_field_actions) == 4
            and len(receipt.downward_void_actions) == 4
            and receipt.compressive_after.void_decision is VoidDecision.CONFIRM
        )
    archive_rebuilt = ReceiptStore(store.path).load().receipts == memory.receipts
    checks = {
        "command_checks": command_checks,
        "field_void_quadratic_routing": all(routing_checks),
        "archive_rebuilt": archive_rebuilt,
        "gpu_proposal_role": profile.expressive_device == "JETSON_GPU",
        "cpu_commit_role": profile.compressive_device in ("JETSON_CPU", "CPU_REFERENCE"),
        "jetson_required": not require_jetson or profile.hardware_split_ready,
    }
    return {
        "ready": all(command_checks.values()) and all(routing_checks) and archive_rebuilt
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
    commands.add_parser("memory-status", help="verify memory activity and archive integrity")
    teach = commands.add_parser("teach", help="teach one exact phrase")
    teach.add_argument("command", choices=[command.value for command in VerbalCommand])
    teach.add_argument("phrase")
    recall = commands.add_parser("recall", help="recall without committing")
    recall.add_argument("phrase")
    cycle = commands.add_parser("cycle", help="run one M4/Dream/Administrator cycle")
    cycle.add_argument("phrase")
    smoke = commands.add_parser("smoke-test", help="verify memory and device split")
    smoke.add_argument("--require-jetson", action="store_true")
    loop = commands.add_parser("loop", help="run persistent hearing and association loop")
    loop.add_argument("--silent", action="store_true", help="print speech without audio")
    loop.add_argument("--responses", choices=("always", "changes", "never"), default="changes", help="choose when speech is emitted")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    store = _store(args.memory)
    if args.action == "init":
        memory = store.initialize()
        result = {"memory_path": str(store.path), "receipts": len(memory.receipts)}
    elif args.action == "status":
        result = detect_jetson().receipt
    elif args.action == "memory-status":
        result = memory_health(store)
    elif args.action == "teach":
        memory = store.teach(args.phrase, VerbalCommand(args.command))
        result = {"memory_path": str(store.path), "receipts": len(memory.receipts)}
    elif args.action == "recall":
        result = store.initialize().recall(args.phrase)
    elif args.action == "cycle":
        profile, receipt = _cycle_receipt(store, args.phrase)
        result = {"profile": profile.receipt, "cycle": receipt}
    elif args.action == "loop":
        from One_Wave_Bench.brain.conversation_loop import ConversationLoop, SystemSpeaker
        state = ConversationLoop(store, SystemSpeaker(enabled=not args.silent), responses=args.responses).run()
        result = {
            "cycles": state.cycles,
            "teachings": state.teachings,
            "silent_cycles": state.silent_cycles,
            "unresolved_cue": state.unresolved_cue,
            "memory": memory_health(store),
        }
    else:
        result = run_smoke_test(store, require_jetson=args.require_jetson)
    print(json.dumps(_jsonable(result), indent=2, sort_keys=True))
    successful = not isinstance(result, dict) or (
        result.get("ready", True) and result.get("healthy", True)
    )
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
