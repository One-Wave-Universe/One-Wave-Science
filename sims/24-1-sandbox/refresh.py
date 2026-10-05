#!/usr/bin/env python3
"""Reference -> affected tests -> fresh receipts -> re-reference. No source repair."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DEPENDENCIES = "sims/24-1-sandbox/refresh-dependencies.json"
SCHEMA = "one-wave-module-refresh/v1"
MODULES = ("lattice-primitive", "spectral-lattice-phase")
MAX_OUTPUT = 4 * 1024 * 1024
COMMAND_TIMEOUT = 60
TOTAL_TIMEOUT = 240

# Commands are code-reviewed constants, never supplied by manifests or JSON.
def commands():
    py = sys.executable
    return {
        "registry": [
            ("registry-tests", [py, "-m", "unittest", "discover", "-s", "sims/24-1-sandbox", "-p", "test_sandbox.py", "-v"], None),
            ("registry", [py, "sims/24-1-sandbox/sandbox.py", "--json"], "registry.json"),
        ],
        "lattice-primitive": [
            ("kernel-tests", ["node", "--test", "sims/00-lattice-primitive/test_lattice_kernel.js"], None),
            ("lattice-adapter-tests", ["node", "--test", "sims/24-1-sandbox/modules/01-lattice-primitive/test_adapter.js"], None),
            ("dispersion-tests", [py, "-m", "unittest", "discover", "-s", "sims/00-lattice-primitive", "-p", "test*.py", "-v"], None),
            ("lattice-receipt", ["node", "sims/24-1-sandbox/modules/01-lattice-primitive/adapter.js"], "lattice-receipt.json"),
        ],
        "spectral-lattice-phase": [
            ("spectral-adapter-tests", [py, "-m", "unittest", "discover", "-s", "sims/24-1-sandbox/modules/06-spectral-lattice-phase", "-p", "test*.py", "-v"], None),
            ("spectral-source-controls", [py, "sims/06-spectral-lattice-phase/test_spectral_lattice_phase.py"], None),
            ("spectral-receipt", [py, "sims/24-1-sandbox/modules/06-spectral-lattice-phase/adapter.py"], "spectral-receipt.json"),
        ],
    }


class Hold(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    result = execute(["git", "-C", str(root), *args], root, timeout=15, max_output=MAX_OUTPUT)
    if result["reason"] or result["returncode"] != 0:
        raise Hold("Git reference command failed: " + " ".join(args))
    return result["stdout"].strip()


def load_dependencies(root):
    try:
        value = json.loads((root / DEPENDENCIES).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise Hold("Dependency map unreadable") from error
    if not isinstance(value, dict) or set(value) != {"schema", "shared", "modules"} or value["schema"] != "one-wave-module-refresh-dependencies/v1":
        raise Hold("Invalid dependency schema")
    if not isinstance(value["modules"], dict) or set(value["modules"]) != set(MODULES):
        raise Hold("Unknown or missing module dependency mapping")
    for group in [value["shared"], *value["modules"].values()]:
        if not isinstance(group, list) or not group:
            raise Hold("Dependency groups must be nonempty path lists")
        for pattern in group:
            if not isinstance(pattern, str) or not pattern or "\\" in pattern or Path(pattern).is_absolute() or ".." in Path(pattern).parts:
                raise Hold("Unsafe dependency path")
    return value


def affected_modules(dependencies, changed):
    if changed is None or any(fnmatch.fnmatchcase(path, pattern) for path in changed for pattern in dependencies["shared"]):
        return list(MODULES)
    return [module for module in MODULES if any(fnmatch.fnmatchcase(path, pattern)
            for path in changed for pattern in dependencies["modules"][module])]


def reference(root):
    head = git(root, "rev-parse", "HEAD")
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    dependencies = load_dependencies(root)
    groups = {}
    for group, patterns in {"shared": dependencies["shared"], **dependencies["modules"]}.items():
        files = {}
        for pattern in patterns:
            matches = sorted(path for path in root.glob(pattern + "/*" if pattern.endswith("/**") else pattern) if path.is_file())
            if not matches:
                raise Hold("Missing dependency: " + pattern)
            for path in matches:
                if path.is_symlink() or not path.resolve().is_relative_to(root):
                    raise Hold("Unsafe dependency target: " + str(path))
                files[path.relative_to(root).as_posix()] = digest(path.read_bytes())
        groups[group] = files
    identity = {"head": head, "status": status, "groups": groups}
    return {**identity, "fingerprint": digest(canonical(identity).encode())}, dependencies


def changed_paths(root, base, expected):
    if base is None:
        return None
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        raise Hold("Base must be a complete commit SHA")
    git(root, "cat-file", "-e", base + "^{commit}")
    output = git(root, "diff", "--no-ext-diff", "--name-only", "--no-renames", "-z", base, expected, "--")
    return [name for name in output.split("\0") if name]


def create_bundle(root, output):
    root = root.resolve()
    output = output.absolute()
    # Refuse symlink destinations, occupied targets and locations inside worktree/Git metadata.
    target = output.resolve()
    common = Path(git(root, "rev-parse", "--git-common-dir"))
    common = (root / common).resolve() if not common.is_absolute() else common.resolve()
    if target.is_relative_to(root) or target.is_relative_to(common) or output.is_symlink():
        raise Hold("Output must be outside the checkout and Git metadata")
    if not output.parent.is_dir() or output.parent.resolve() != output.parent:
        raise Hold("Output parent must be an existing non-symlink directory")
    try:
        output.mkdir(mode=0o700)
    except OSError as error:
        raise Hold("Output bundle must be a fresh unoccupied directory") from error
    (output / "RUNNING.json").write_text(canonical({"schema": SCHEMA, "status": "RUNNING", "eligible_as_current": False}) + "\n")
    return output


def execute(argv, root, timeout=COMMAND_TIMEOUT, max_output=MAX_OUTPUT):
    """Drain both pipes with a hard combined-byte limit; kill the process group on bounds."""
    started = time.monotonic()
    stdout, stderr = bytearray(), bytearray()
    reason = None
    try:
        process = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    except OSError as error:
        return {"returncode": None, "reason": "launch-failed", "stdout": "", "stderr": str(error), "elapsed_s": 0.0}
    def kill_group():
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    selector = selectors.DefaultSelector()
    for pipe, buffer in ((process.stdout, stdout), (process.stderr, stderr)):
        selector.register(pipe, selectors.EVENT_READ, buffer)
    try:
        while selector.get_map():
            remaining = timeout - (time.monotonic() - started)
            if remaining <= 0:
                reason = "timeout"
                break
            for key, _ in selector.select(min(remaining, 0.1)):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                room = max_output - len(stdout) - len(stderr)
                key.data.extend(chunk[:max(0, room)])
                if len(chunk) > room:
                    reason = "output-limit"
                    break
            if reason:
                break
        if reason:
            kill_group()
        try:
            process.wait(timeout=max(0.05, timeout - (time.monotonic() - started)))
        except subprocess.TimeoutExpired:
            reason = "timeout"
            kill_group()
            process.wait()
    except BaseException:
        kill_group()
        process.wait()
        raise
    finally:
        selector.close()
        process.stdout.close()
        process.stderr.close()
    return {"returncode": process.returncode, "reason": reason,
            "stdout": stdout.decode("utf-8", errors="replace"), "stderr": stderr.decode("utf-8", errors="replace"),
            "elapsed_s": round(time.monotonic() - started, 4)}


RECEIPT_SOURCES = {
    "lattice-primitive": {"Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md",
        "sims/00-lattice-primitive/lattice-kernel.js", "sims/24-1-sandbox/modules/01-lattice-primitive/adapter.js",
        "sims/24-1-sandbox/modules/01-lattice-primitive/manifest.json", "sims/00-state-container/state-schema.json"},
    "spectral-lattice-phase": {"Nodes/G-767_Measured_Spectrum_Lattice_Phase_Map.md",
        "sims/06-spectral-lattice-phase/spectral_lattice_phase.py", "sims/24-1-sandbox/modules/06-spectral-lattice-phase/adapter.py",
        "sims/24-1-sandbox/modules/06-spectral-lattice-phase/manifest.json", "sims/00-state-container/state-schema.json"},
}


def check_state_payload(receipt, module, current):
    """Check receipt completeness/consistency, not independent physical validity."""
    config, initial, final = receipt["configuration"], receipt["initial"], receipt["final"]
    if not isinstance(config, dict) or not isinstance(receipt["measurements"], dict):
        raise ValueError("Missing configuration/measurements")
    measured = []
    for snapshot in (initial, final):
        if not isinstance(snapshot, dict) or snapshot.get("id") != module or not isinstance(snapshot.get("state"), dict) or not isinstance(snapshot.get("provenance"), dict):
            raise ValueError("Missing state envelope")
        values = snapshot["measurements"]
        if not isinstance(values, list) or not values or any(not isinstance(item, dict) or "name" not in item or "value" not in item for item in values):
            raise ValueError("Missing snapshot measurements")
        if any(not isinstance(item["name"], str) for item in values):
            raise ValueError("Invalid measurement names")
        if len({item["name"] for item in values}) != len(values):
            raise ValueError("Duplicate snapshot measurements")
        measured.append({item["name"]: item["value"] for item in values})
        source = "Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md" if module == "lattice-primitive" else "Nodes/G-767_Measured_Spectrum_Lattice_Phase_Map.md"
        version = "lattice-adapter/v1" if module == "lattice-primitive" else "spectral-adapter/v1"
        if snapshot["provenance"].get("source") != source or snapshot["provenance"].get("version") != version:
            raise ValueError("Snapshot source identity mismatch")
        if module == "spectral-lattice-phase":
            hashes = snapshot["provenance"]["source_sha256"]
            if not isinstance(hashes, dict) or set(hashes) != RECEIPT_SOURCES[module] or any(current.get(path) != sha for path, sha in hashes.items()):
                raise ValueError("Snapshot source hashes mismatch")
    points = receipt["geometry"]["points"]
    if not isinstance(points, list) or not points or any(not isinstance(point, dict) for point in points):
        raise ValueError("Missing state-driven geometry")
    if module == "lattice-primitive":
        steps = config["requested_steps"]
        sites = final["state"]["sites"]
        if type(steps) is not int or not 0 <= steps <= 10000 or config["completed_steps"] != steps or final["state"]["steps"] != steps:
            raise ValueError("Incomplete step count")
        if receipt["failure"] is not None or receipt["checks"].get("finite_accepted_samples") is not True or receipt["checks"].get("requested_steps_completed") is not True:
            raise ValueError("Module reported failed checks")
        if not isinstance(sites, list) or len(sites) != 37 or len(points) != len(sites) or len(receipt["samples"]) != steps + 1:
            raise ValueError("Incomplete numerical state/history")
        def finite_number(value):
            return type(value) in (int, float) and math.isfinite(value)
        sample_keys = {"Q", "A_rms", "V_rms", "phase_coherence", "energy", "circulation"}
        samples, solver = receipt["samples"], receipt["solver"]
        if not isinstance(samples, list) or not isinstance(solver, list) or len(solver) != steps:
            raise ValueError("Incomplete sample/solver history")
        if not finite_number(config["dt"]) or config["dt"] <= 0:
            raise ValueError("Invalid sample interval")
        previous_time = None
        for sample in samples:
            if not isinstance(sample, dict) or not finite_number(sample.get("time")) or not isinstance(sample.get("measurements"), dict):
                raise ValueError("Invalid sample record")
            values = sample["measurements"]
            if set(values) != sample_keys or any(not finite_number(value) for value in values.values()):
                raise ValueError("Invalid sample measurements")
            if previous_time is not None and (sample["time"] <= previous_time or not math.isclose(sample["time"] - previous_time, config["dt"], rel_tol=1e-9, abs_tol=1e-12)):
                raise ValueError("Sample times do not follow declared interval")
            previous_time = sample["time"]
        for item in solver:
            if not isinstance(item, dict) or item.get("integrator") != "symplectic-euler-kick-drift" or item.get("requested_dt") != config["dt"]:
                raise ValueError("Invalid solver record")
            if any(type(item.get(key)) is not int or item[key] < 1 for key in ("substeps", "trials")) or not finite_number(item.get("smallest_dt")) or item["smallest_dt"] <= 0:
                raise ValueError("Invalid solver substep receipt")
        if samples[0]["time"] != initial["state"]["time"] or samples[-1]["time"] != final["state"]["time"] or samples[0]["measurements"] != measured[0] or samples[-1]["measurements"] != measured[1]:
            raise ValueError("Sample endpoints disagree with state snapshots")
        if initial["state"]["steps"] != 0 or initial["state"]["parameters"] != config["parameters"] or final["state"]["parameters"] != config["parameters"]:
            raise ValueError("Snapshot configuration mismatch")
        for point, site in zip(points, sites):
            if not isinstance(site, dict) or any(not finite_number(site.get(key)) for key in ("x", "v", "phase", "q", "r")):
                raise ValueError("Invalid site state")
            if point["displacement"] != site["x"] or point["velocity"] != site["v"]:
                raise ValueError("Geometry does not match final state")
        if receipt["measurements"]["initial_energy"] != measured[0]["energy"] or receipt["measurements"]["final_energy"] != measured[1]["energy"]:
            raise ValueError("Energy measurements disagree")
    else:
        analysis = final["state"]["analysis"]
        count = len(config["records"])
        if final["state"]["configuration"] != config or initial["state"]["configuration"] != config or initial["state"]["analysis"] is not None:
            raise ValueError("Static state/configuration mismatch")
        if not isinstance(analysis, dict) or not 3 <= count <= 10000 or len(points) != count or receipt["measurements"]["count"] != count:
            raise ValueError("Incomplete static state")
        for name in ("phase", "log2_ratio", "octave"):
            if not isinstance(analysis[name], list) or len(analysis[name]) != count:
                raise ValueError("Incomplete coordinate arrays")
        for name in ("coherence", "null_mean_coherence", "empirical_upper_tail_p"):
            if type(analysis[name]) not in (int, float) or not 0 <= analysis[name] <= 1 or analysis[name] != receipt["measurements"][name] or analysis[name] != measured[1][name]:
                raise ValueError("Static measurements disagree")
        for i, point in enumerate(points):
            if point["scatter"] != [analysis["log2_ratio"][i], analysis["phase"][i]] or point["scale"] != config["records"][i]["scale"]:
                raise ValueError("Geometry does not match static state")
        expected_input_hash = digest(canonical(config).encode("utf-8"))
        if any(snapshot["provenance"]["normalized_input_sha256"] != expected_input_hash for snapshot in (initial, final)):
            raise ValueError("Input checksum mismatch")


def check_receipt(raw, module, before):
    def invalid_constant(value):
        raise ValueError("Nonfinite JSON constant: " + value)
    try:
        receipt = json.loads(raw, parse_constant=invalid_constant)
        canonical(receipt)  # Reject overflowed JSON numbers as well as NaN/Infinity constants.
        if not isinstance(receipt, dict):
            raise ValueError("Receipt must be an object")
        if module == "registry":
            if receipt.get("schema") != "one-wave-sandbox-module/v1" or receipt.get("ok") is not True or receipt.get("module_execution") != "not-run" or receipt.get("validation_scope") != "manifest-and-paths-only":
                raise ValueError("Registry did not validate")
            if receipt.get("errors") != [] or receipt.get("occupied_slots") != [1, 6] or any(type(slot) is not int for slot in receipt["occupied_slots"]):
                raise ValueError("Incomplete registry slot/error ledger")
            rows = receipt.get("modules")
            if not isinstance(rows, list) or len(rows) != 2:
                raise ValueError("Incomplete registry module ledger")
            for row, (module_id, slot) in zip(sorted(rows, key=lambda row: row["slot"]), (("lattice-primitive", 1), ("spectral-lattice-phase", 6))):
                if not isinstance(row, dict) or row.get("id") != module_id or type(row.get("slot")) is not int or row["slot"] != slot or row.get("errors") != [] or row.get("module_execution") != "not-run" or row.get("entry_point_present") is not True or not isinstance(row.get("path"), str) or not row["path"]:
                    raise ValueError("Invalid registry module evidence")
            return receipt
        expected_schema = "one-wave-lattice-run/v1" if module == "lattice-primitive" else "one-wave-spectral-run/v1"
        if receipt.get("schema") != expected_schema or receipt.get("module") != module or receipt.get("status") != "completed":
            raise ValueError("Incomplete module receipt")
        provenance = receipt["provenance"] if module == "lattice-primitive" else receipt["final"]["provenance"]
        hashes = provenance["source_sha256"]
        current = {**before["groups"]["shared"], **before["groups"][module]}
        if not isinstance(hashes, dict) or set(hashes) != RECEIPT_SOURCES[module] or any(current.get(path) != sha for path, sha in hashes.items()):
            raise ValueError("Receipt source hashes do not match reference")
        if receipt.get("physical_validation") != "unverified" or receipt.get("claim_gate") != "YELLOW":
            raise ValueError("Unexpected scientific claim status")
        check_state_payload(receipt, module, current)
        return receipt
    except (ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
        raise Hold("Invalid or stale " + module + " receipt: " + str(error)) from error


def refresh(root, expected_head, output, base=None):
    root = Path(root).resolve()
    bundle = create_bundle(root, Path(output))
    report = {"schema": SCHEMA, "status": "RUNNING", "eligible_as_current": False,
              "expected_head": expected_head, "base": base, "attempts_per_command": 1,
              "source_repair": "not-authorized-or-performed", "modules": {}, "commands": [],
              "scope": "module-software-tests-and-derived-receipts-only"}
    started = time.monotonic()
    before = None
    try:
        if not re.fullmatch(r"[0-9a-f]{40}", expected_head or ""):
            raise Hold("Expected HEAD must be a complete commit SHA")
        before, dependencies = reference(root)
        report["reference_before"] = before
        if before["head"] != expected_head or before["status"]:
            raise Hold("Expected clean HEAD not present; preserve local edits")
        changed = changed_paths(root, base, expected_head)
        selected = affected_modules(dependencies, changed)
        report.update(changed_paths=changed, affected_modules=selected)
        report["modules"] = {module: {"status": "PENDING" if module in selected else "NOT_RUN_UNAFFECTED"} for module in MODULES}
        groups = ["registry", *selected] if selected else []
        for group in groups:
            if group in MODULES:
                report["modules"][group]["status"] = "RUNNING"
            for name, argv, receipt_name in commands()[group]:
                # Refuse further work as soon as earlier commands or another actor changed source.
                current, _ = reference(root)
                if current != before:
                    raise Hold("Source drift before command " + name)
                remaining = TOTAL_TIMEOUT - (time.monotonic() - started)
                if remaining <= 0:
                    raise Hold("Total refresh deadline exhausted")
                result = execute(argv, root, timeout=min(COMMAND_TIMEOUT, remaining))
                for channel in ("stdout", "stderr"):
                    (bundle / (name + "." + channel + ".txt")).write_text(result[channel], encoding="utf-8")
                entry = {"name": name, "group": group, "argv": argv,
                         **{key: value for key, value in result.items() if key not in ("stdout", "stderr")}}
                report["commands"].append(entry)
                if result["reason"] or result["returncode"] != 0:
                    raise Hold("Command failed: " + name + " (" + str(result["reason"] or result["returncode"]) + ")")
                if receipt_name:
                    check_receipt(result["stdout"], group, before)
                    (bundle / receipt_name).write_text(result["stdout"], encoding="utf-8")
            if group in MODULES:
                report["modules"][group]["status"] = "COMPLETED_PENDING_REFERENCE"
        after, _ = reference(root)
        report["reference_after"] = after
        if after != before:
            raise Hold("Source changed during refresh; results invalidated")
        report["status"] = "COMPLETED" if selected else "NO_AFFECTED_MODULES"
        report["eligible_as_current"] = bool(selected)
        for module in selected:
            report["modules"][module]["status"] = "COMPLETED"
    except (Hold, OSError, ValueError, subprocess.SubprocessError, KeyboardInterrupt) as error:
        report.update(status="HOLD", eligible_as_current=False, reason=str(error) or "Interrupted")
        for item in report["modules"].values():
            if item["status"] != "NOT_RUN_UNAFFECTED":
                item["status"] = "INVALIDATED_OR_NOT_COMPLETED"
        try:
            report["reference_after"], _ = reference(root)
        except (Hold, OSError, ValueError) as reference_error:
            report["return_reference_error"] = str(reference_error)
    report["elapsed_s"] = round(time.monotonic() - started, 4)
    report["artifacts"] = {path.name: digest(path.read_bytes()) for path in sorted(bundle.iterdir()) if path.is_file() and path.name != "RUNNING.json"}
    temporary = bundle / "summary.json.tmp"
    temporary.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, bundle / "summary.json")
    # RUNNING is deliberately retained as a start record. Only finalized summary.json is authoritative.
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--base", default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = refresh(ROOT, args.expected_head, args.output, args.base)
    except (Hold, OSError, ValueError) as error:
        report = {"schema": SCHEMA, "status": "HOLD", "eligible_as_current": False, "reason": str(error)}
    print(json.dumps(report, indent=2, allow_nan=False))
    raise SystemExit(2 if report["status"] == "HOLD" else 0)


if __name__ == "__main__":
    main()
