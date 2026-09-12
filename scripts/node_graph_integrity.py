#!/usr/bin/env python3
"""Audit canonical One-Wave node metadata and dependency graph.

The audit is intentionally stdlib-only so it can run on a clean GitHub runner or
on the Jetson without installing Python packages.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE_DIRS = (ROOT / "Nodes", ROOT / "Root_Axioms")
MASTER_INDEX = ROOT / "00_MASTER_INDEX.md"
ALIAS_REGISTRY = ROOT / "LEGACY_ID_ALIAS_REGISTRY.json"
D413_README = ROOT / "Nodes" / "D-413_Ground_Lattice_Orbital_Restoring_Simulation" / "README.md"
AI_START = ROOT / "AI_CANONICAL_START_HERE.md"

NODE_REQUIRED = (
    "node_id",
    "canonical_name",
    "namespace",
    "gate",
    "lifecycle",
    "classification",
    "claim_gate_detail",
    "metadata_standard",
)
ARTIFACT_REQUIRED = (
    "artifact_id",
    "parent_node_id",
    "title",
    "namespace",
    "lifecycle",
    "metadata_standard",
)
ALLOWED_CANONICAL_NAMESPACES = {"NODE", "ROOT_AXIOM"}
ALLOWED_GATES = {"BROWN", "GRAY", "GREEN", "YELLOW", "BRONZE", "SILVER", "GOLD", "RED"}
ALLOWED_LIFECYCLES = {
    "ACTIVE",
    "ACTIVE_HYPOTHESIS",
    "PROPOSED_BUILD",
    "HELD",
    "BLOCKED",
    "SUPERSEDED",
    "HISTORY",
}
NODE_ID_RE = re.compile(r"\b([A-G]-\d{3}[a-z]?)\b")
DEP_LINE_RE = re.compile(r"^\s*(?:\*\*)?(Upstream|Downstream|Lateral)\s*:\s*(.*)$", re.IGNORECASE)

# These reciprocal edges are architecture locks. The source must name the
# target downstream, and the target must name the source upstream.
LOCKED_EDGES = (
    ("C-311", "C-319"),
    ("D-408", "C-319"),
    ("D-409", "C-319"),
    ("C-319", "C-320"),
    ("A-115", "C-320"),
    ("C-306", "C-320"),
    ("C-307", "C-320"),
    ("D-409", "C-320"),
    ("C-319", "D-413"),
    ("C-320", "D-413"),
    ("A-115", "D-416"),
    ("C-307", "D-416"),
    ("D-409", "D-416"),
    ("C-320", "D-416"),
    ("D-413", "D-416"),
)

LOCKED_README_IDS = ("A-115", "C-311", "C-319", "C-320", "D-413", "D-416")


def parse_scalar(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}:
        return raw[1:-1]
    return raw


def parse_frontmatter(path: Path, text: str) -> tuple[dict[str, str], list[str]]:
    if not text.startswith("---\n"):
        return {}, [f"{path.relative_to(ROOT)}: missing YAML front matter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, [f"{path.relative_to(ROOT)}: unterminated YAML front matter"]
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = parse_scalar(value)
    return meta, []


def require_keys(path: Path, meta: dict[str, str], keys: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    for key in keys:
        if not meta.get(key):
            errors.append(f"{path.relative_to(ROOT)}: missing metadata key {key}")
    return errors


def load_aliases() -> tuple[set[str], set[str]]:
    data = json.loads(ALIAS_REGISTRY.read_text(encoding="utf-8"))
    aliases: set[str] = set()
    dispositions: set[str] = set()
    for item in data.get("aliases", []):
        legacy = item.get("legacy_id", "")
        resolution = item.get("resolution", "")
        if resolution == "ALIAS":
            aliases.add(legacy)
        elif resolution == "DISPOSITION":
            dispositions.add(legacy)
    return aliases, dispositions


def dependency_map(text: str) -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    for line in text.splitlines():
        match = DEP_LINE_RE.match(line)
        if not match:
            continue
        kind = match.group(1).capitalize()
        out[kind].update(NODE_ID_RE.findall(match.group(2)))
    return out


def main() -> int:
    errors: list[str] = []
    nodes: dict[str, Path] = {}
    deps: dict[str, dict[str, set[str]]] = {}
    artifacts: list[tuple[Path, str]] = []

    for directory in NODE_DIRS:
        if not directory.exists():
            errors.append(f"missing canonical node directory: {directory.relative_to(ROOT)}")
            continue
        for path in sorted(directory.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            meta, frontmatter_errors = parse_frontmatter(path, text)
            errors.extend(frontmatter_errors)
            if not meta:
                continue

            namespace = meta.get("namespace")
            if namespace == "NODE_ARTIFACT":
                errors.extend(require_keys(path, meta, ARTIFACT_REQUIRED))
                if meta.get("metadata_standard") != "I-06":
                    errors.append(f"{path.relative_to(ROOT)}: artifact metadata_standard must be I-06")
                if meta.get("lifecycle") not in ALLOWED_LIFECYCLES:
                    errors.append(f"{path.relative_to(ROOT)}: invalid artifact lifecycle {meta.get('lifecycle')!r}")
                parent = meta.get("parent_node_id")
                if parent:
                    artifacts.append((path, parent))
                continue

            if namespace not in ALLOWED_CANONICAL_NAMESPACES:
                errors.append(
                    f"{path.relative_to(ROOT)}: namespace must be NODE, ROOT_AXIOM, or NODE_ARTIFACT, got {namespace!r}"
                )
                continue

            errors.extend(require_keys(path, meta, NODE_REQUIRED))
            node_id = meta.get("node_id")
            if not node_id:
                continue
            if node_id in nodes:
                errors.append(
                    f"duplicate node_id {node_id}: {nodes[node_id].relative_to(ROOT)} and {path.relative_to(ROOT)}"
                )
                continue
            nodes[node_id] = path
            deps[node_id] = dependency_map(text)
            if meta.get("gate") not in ALLOWED_GATES:
                errors.append(f"{path.relative_to(ROOT)}: invalid gate {meta.get('gate')!r}")
            if meta.get("lifecycle") not in ALLOWED_LIFECYCLES:
                errors.append(f"{path.relative_to(ROOT)}: invalid lifecycle {meta.get('lifecycle')!r}")
            if meta.get("metadata_standard") != "I-06":
                errors.append(f"{path.relative_to(ROOT)}: metadata_standard must be I-06")

    aliases, dispositions = load_aliases()

    # Artifact parents must resolve after all canonical nodes have been loaded.
    for path, parent in artifacts:
        if parent in nodes or parent in aliases:
            continue
        if parent in dispositions:
            errors.append(f"{path.relative_to(ROOT)}: parent node {parent} is retired/dispositioned")
        else:
            errors.append(f"{path.relative_to(ROOT)}: unresolved parent_node_id {parent}")

    # Dependency lines must resolve to a canonical node or declared alias.
    for source, groups in sorted(deps.items()):
        for kind, refs in groups.items():
            for ref in sorted(refs):
                if ref in nodes or ref in aliases:
                    continue
                if ref in dispositions:
                    errors.append(f"{source} {kind}: dependency {ref} is retired/dispositioned, not canonical")
                else:
                    errors.append(f"{source} {kind}: unresolved canonical node id {ref}")

    # Every canonical A-G node must be discoverable from the master index.
    index_text = MASTER_INDEX.read_text(encoding="utf-8")
    for node_id, path in sorted(nodes.items()):
        if node_id.startswith("A+"):
            continue
        if not re.search(rf"\|\s*{re.escape(node_id)}\s*\|", index_text):
            errors.append(f"master index does not list {node_id} ({path.relative_to(ROOT)})")

    # Architecture-lock edges must be reciprocal.
    for source, target in LOCKED_EDGES:
        if source not in nodes:
            errors.append(f"locked-edge source missing: {source}")
            continue
        if target not in nodes:
            errors.append(f"locked-edge target missing: {target}")
            continue
        if target not in deps[source].get("Downstream", set()):
            errors.append(f"locked edge missing: {source} Downstream -> {target}")
        if source not in deps[target].get("Upstream", set()):
            errors.append(f"locked reciprocal missing: {target} Upstream <- {source}")

    if not D413_README.exists():
        errors.append("D-413 runnable README missing")
    else:
        readme = D413_README.read_text(encoding="utf-8")
        for node_id in LOCKED_README_IDS:
            if node_id not in readme:
                errors.append(f"D-413 README missing canonical link/reference {node_id}")

    if AI_START.exists():
        ai_text = AI_START.read_text(encoding="utf-8")
        for node_id in ("C-319", "C-320", "D-416"):
            if node_id not in ai_text:
                errors.append(f"AI_CANONICAL_START_HERE.md missing bridge node {node_id}")
    else:
        errors.append("AI_CANONICAL_START_HERE.md missing")

    print(f"canonical nodes/root axioms parsed: {len(nodes)}")
    print(f"node artifacts parsed: {len(artifacts)}")
    if errors:
        print("\nERRORS")
        for item in errors:
            print(f"- {item}")
        print(f"\nFAIL: {len(errors)} error(s)")
        return 1

    print("PASS: canonical node metadata, root axioms, index coverage, dependencies, artifacts, and locked graph edges all hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
