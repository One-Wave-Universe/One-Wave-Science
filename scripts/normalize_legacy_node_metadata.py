#!/usr/bin/env python3
"""Normalize legacy top-level Nodes/*.md metadata to I-06 without promoting claims.

Rules are deliberately conservative:
- preserve a recognizable declared gate when present;
- otherwise assign BROWN rather than inventing maturity;
- translate legacy id/title/status/tier front matter to I-06;
- if an ID already has a complete canonical NODE file, other same-ID files
  become explicit NODE_ARTIFACT documents instead of duplicate nodes;
- when an ID has no canonical file, choose one primary file deterministically
  and mark same-ID receipts/stamps/overlays as artifacts.

This script changes metadata only.  It does not rewrite scientific prose.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODES = ROOT / "Nodes"
ID_RE = re.compile(r"^([A-G]-\d{3}[a-z]?)(?:_|\b)")
KNOWN_GATES = ("BROWN", "GRAY", "GREEN", "YELLOW", "BRONZE", "SILVER", "GOLD", "RED")
ARTIFACT_HINTS = ("STAMP", "OVERLAY", "RECEIPT", "RESULT", "RESULTS", "AUDIT", "NOTES", "BACKUP")
REQUIRED = {
    "node_id",
    "canonical_name",
    "namespace",
    "gate",
    "lifecycle",
    "classification",
    "claim_gate_detail",
    "metadata_standard",
}


def split_frontmatter(text: str) -> tuple[dict[str, str], str, bool]:
    if not text.startswith("---\n"):
        return {}, text, False
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text, False
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[end + 5 :], True


def has_complete_i06(meta: dict[str, str]) -> bool:
    return meta.get("namespace") == "NODE" and REQUIRED.issubset(meta) and meta.get("metadata_standard") == "I-06"


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def clean_title(node_id: str, heading: str | None, legacy_title: str | None, path: Path) -> str:
    title = legacy_title or heading or path.stem.split("_", 1)[-1].replace("_", " ")
    title = re.sub(rf"^(?:Node\s+)?{re.escape(node_id)}\s*[:—-]\s*", "", title, flags=re.I)
    return title.strip() or path.stem


def declared_gate(meta: dict[str, str], body: str) -> str:
    values = [meta.get("gate", ""), meta.get("tier", ""), meta.get("status", "")]
    for line in body.splitlines()[:25]:
        if re.search(r"\b(Status|Gate|Tier)\b", line, re.I):
            values.append(line)
    joined = "\n".join(values).upper()
    # Prefer the most explicit/mature token as written; no inference from prose.
    for gate in KNOWN_GATES:
        if re.search(rf"\b{gate}\b", joined):
            return gate
    return "BROWN"


def lifecycle_for(meta: dict[str, str], body: str, gate: str) -> str:
    blob = " ".join((meta.get("status", ""), meta.get("tier", ""), body[:500])).lower()
    if "blocked" in blob:
        return "BLOCKED"
    if "held" in blob or "parked" in blob:
        return "HELD"
    if "superseded" in blob:
        return "SUPERSEDED"
    if "hypothesis" in blob or "proposed" in blob or gate == "BROWN":
        return "ACTIVE_HYPOTHESIS"
    return "ACTIVE"


def claim_detail(meta: dict[str, str], body: str) -> str:
    for key in ("claim_gate_detail", "claim_boundary", "status", "tier"):
        value = meta.get(key)
        if value:
            return value.replace('"', "'")
    for line in body.splitlines()[:20]:
        if re.search(r"\*\*(Status|Gate|Claim boundary)\*\*", line, re.I):
            return re.sub(r"^\s*[-*# ]+", "", line).replace('"', "'")
    return "Metadata normalized conservatively; in-body evidence and limitations remain authoritative."


def artifact_score(path: Path) -> int:
    upper = path.stem.upper()
    return sum(1 for hint in ARTIFACT_HINTS if hint in upper)


def choose_primary(paths: list[Path]) -> Path:
    # Prefer a file whose H1 explicitly presents itself as the ID and avoid
    # obvious stamp/overlay/receipt support artifacts.
    ranked = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        meta, body, _ = split_frontmatter(text)
        heading = first_heading(body)
        explicit = 0 if heading and re.search(rf"\b{re.escape(path.stem.split('_',1)[0])}\b", heading) else 1
        ranked.append((artifact_score(path), explicit, len(path.name), path.name, path))
    return min(ranked)[-1]


def render_node(node_id: str, path: Path, meta: dict[str, str], body: str) -> str:
    title = clean_title(node_id, first_heading(body), meta.get("canonical_name") or meta.get("title"), path)
    gate = declared_gate(meta, body)
    lifecycle = lifecycle_for(meta, body, gate)
    detail = claim_detail(meta, body)
    classification = meta.get("classification") or "Legacy G-Series / Canonicalized Node"
    header = (
        "---\n"
        f'node_id: "{node_id}"\n'
        f'canonical_name: "{title.replace(chr(34), chr(39))}"\n'
        'namespace: "NODE"\n'
        f'gate: "{gate}"\n'
        f'lifecycle: "{lifecycle}"\n'
        f'classification: "{classification.replace(chr(34), chr(39))}"\n'
        f'claim_gate_detail: "{detail.replace(chr(34), chr(39))}"\n'
        'metadata_standard: "I-06"\n'
        "---\n\n"
    )
    return header + body.lstrip("\n")


def render_artifact(parent_id: str, path: Path, meta: dict[str, str], body: str) -> str:
    artifact_id = meta.get("artifact_id") or meta.get("id") or path.stem
    title = meta.get("title") or first_heading(body) or path.stem.replace("_", " ")
    header = (
        "---\n"
        f'artifact_id: "{artifact_id.replace(chr(34), chr(39))}"\n'
        f'parent_node_id: "{parent_id}"\n'
        f'title: "{title.replace(chr(34), chr(39))}"\n'
        'namespace: "NODE_ARTIFACT"\n'
        'lifecycle: "ACTIVE"\n'
        'metadata_standard: "I-06"\n'
        "---\n\n"
    )
    return header + body.lstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    groups: dict[str, list[Path]] = defaultdict(list)
    complete: dict[str, Path] = {}

    for path in sorted(NODES.glob("*.md")):
        match = ID_RE.match(path.name)
        if not match:
            continue
        node_id = match.group(1)
        groups[node_id].append(path)
        meta, _, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        if has_complete_i06(meta):
            if node_id in complete and complete[node_id] != path:
                # Leave genuine duplicate complete nodes for the integrity audit;
                # choosing between mature canonical nodes requires an explicit rename.
                continue
            complete[node_id] = path

    changed: list[Path] = []
    for node_id, paths in sorted(groups.items()):
        primary = complete.get(node_id)
        if primary is None:
            incomplete = []
            for path in paths:
                meta, _, _ = split_frontmatter(path.read_text(encoding="utf-8"))
                if not has_complete_i06(meta):
                    incomplete.append(path)
            if incomplete:
                primary = choose_primary(incomplete)

        for path in paths:
            original = path.read_text(encoding="utf-8")
            meta, body, had_front = split_frontmatter(original)
            if has_complete_i06(meta):
                continue
            # Only normalize legacy/incomplete top-level node documents.  If an
            # unrelated Markdown file ever lands in Nodes without an A-G ID,
            # it is ignored by this tool and caught separately by review.
            if path == primary:
                updated = render_node(node_id, path, meta, body if had_front else original)
            else:
                updated = render_artifact(node_id, path, meta, body if had_front else original)
            if updated != original:
                changed.append(path)
                if not args.check:
                    path.write_text(updated, encoding="utf-8")

    if changed:
        print(("would normalize" if args.check else "normalized") + f" {len(changed)} file(s):")
        for path in changed:
            print(f"- {path.relative_to(ROOT)}")
        return 1 if args.check else 0

    print("legacy node metadata already normalized")
    return 0


if __name__ == "__main__":
    sys.exit(main())
