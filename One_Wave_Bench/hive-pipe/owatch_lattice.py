#!/usr/bin/env python3
"""OWATCH Node Lens Lattice.

Folders marked with .owatch/folder.json become graph nodes. Canonical content
stays in Git. Generated structural indexes and path memory live outside the repo
as compressed runtime state.

This module intentionally separates:
- authority: repository files + I-06 metadata;
- navigation: node envelopes + typed edges;
- memory: hysteretic route preference;
- truth: never inferred from path score.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Any, Iterable

WATCHER_DIR = ".owatch"
POLICY_NAME = "folder.json"
RUNTIME_ROOT = Path(
    os.environ.get(
        "OWATCH_LATTICE_STATE",
        str(Path.home() / ".local/state/one-wave-owatch-lattice"),
    )
).expanduser()

EDGE_TYPES = {
    "AUTHORITY_OF",
    "REFERENCES",
    "DEPENDS_ON",
    "SUPPORTS",
    "CONTRADICTS",
    "VALIDATES",
    "IMPLEMENTS",
    "MEASURES",
    "DERIVES_FROM",
    "SUPERSEDES",
    "RELATED_TO",
}

NODE_STATES = {"cold", "warm", "active"}


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def dump_gzip_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with gzip.open(path, "wb", compresslevel=9) as f:
        f.write(raw)


def load_gzip_json(path: Path, default: Any) -> Any:
    try:
        with gzip.open(path, "rb") as f:
            return json.loads(f.read().decode("utf-8"))
    except (OSError, json.JSONDecodeError, EOFError):
        return default


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    type: str
    weight: float = 1.0
    note: str = ""

    def validate(self) -> None:
        if self.type not in EDGE_TYPES:
            raise ValueError(f"Unsupported edge type: {self.type}")
        if not math.isfinite(self.weight):
            raise ValueError("edge weight must be finite")


@dataclass
class NodeEnvelope:
    node_id: str
    canonical_path: str
    role: str
    authority_refs: list[str]
    concept_tags: list[str]
    state: str
    hold: bool
    content_hash: str
    edges: list[Edge]

    def validate(self) -> None:
        if self.state not in NODE_STATES:
            raise ValueError(f"invalid state: {self.state}")
        for edge in self.edges:
            edge.validate()


def policy_to_envelope(root: Path, folder: Path, policy: dict[str, Any]) -> NodeEnvelope:
    rel = folder.resolve().relative_to(root.resolve()).as_posix()
    node_id = str(policy.get("node_id") or stable_id("owatch", rel or "."))
    role = str(policy.get("role") or "mixed")
    state = str(policy.get("state") or "cold").lower()
    authority_refs = [str(x) for x in policy.get("authority_refs", []) if str(x).strip()]
    concept_tags = [str(x) for x in policy.get("concept_tags", []) if str(x).strip()]
    edges: list[Edge] = []
    for raw in policy.get("edges", []):
        if not isinstance(raw, dict):
            continue
        target = str(raw.get("target", "")).strip()
        edge_type = str(raw.get("type", "RELATED_TO")).strip().upper()
        if not target:
            continue
        edge = Edge(
            source=node_id,
            target=target,
            type=edge_type,
            weight=float(raw.get("weight", 1.0)),
            note=str(raw.get("note", "")),
        )
        edge.validate()
        edges.append(edge)

    content_hash = tree_content_hash(folder)
    env = NodeEnvelope(
        node_id=node_id,
        canonical_path=rel or ".",
        role=role,
        authority_refs=authority_refs,
        concept_tags=concept_tags,
        state=state,
        hold=(folder / WATCHER_DIR / "HOLD.json").is_file(),
        content_hash=content_hash,
        edges=edges,
    )
    env.validate()
    return env


def tree_content_hash(folder: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        if WATCHER_DIR in path.parts:
            continue
        try:
            rel = path.relative_to(folder).as_posix()
            data = path.read_bytes()
        except OSError:
            continue
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(hashlib.sha256(data).digest())
    return h.hexdigest()


def discover_nodes(root: Path) -> dict[str, NodeEnvelope]:
    nodes: dict[str, NodeEnvelope] = {}
    for marker in sorted(root.rglob(f"{WATCHER_DIR}/{POLICY_NAME}")):
        folder = marker.parent.parent
        policy = load_json(marker, {})
        env = policy_to_envelope(root, folder, policy if isinstance(policy, dict) else {})
        if env.node_id in nodes:
            raise ValueError(f"duplicate OWATCH node_id: {env.node_id}")
        nodes[env.node_id] = env
    return nodes


def infer_reference_edges(nodes: dict[str, NodeEnvelope]) -> list[Edge]:
    path_to_id = {node.canonical_path: node.node_id for node in nodes.values()}
    inferred: list[Edge] = []
    for node in nodes.values():
        for ref in node.authority_refs:
            cleaned = ref.strip().lstrip("./")
            candidates = sorted(
                (
                    (path, node_id)
                    for path, node_id in path_to_id.items()
                    if cleaned == path or cleaned.startswith(path.rstrip("/") + "/")
                ),
                key=lambda pair: len(pair[0]),
                reverse=True,
            )
            if candidates:
                inferred.append(
                    Edge(
                        source=node.node_id,
                        target=candidates[0][1],
                        type="REFERENCES",
                        weight=1.0,
                        note=f"authority_ref:{ref}",
                    )
                )
    return inferred


def graph_doc(root: Path) -> dict[str, Any]:
    nodes = discover_nodes(root)
    edges = [edge for node in nodes.values() for edge in node.edges]
    edges.extend(infer_reference_edges(nodes))
    seen: set[tuple[str, str, str]] = set()
    unique: list[Edge] = []
    for edge in edges:
        key = (edge.source, edge.target, edge.type)
        if key in seen:
            continue
        seen.add(key)
        unique.append(edge)
    return {
        "schema": "one-wave-owatch-lattice-v1",
        "root": str(root.resolve()),
        "nodes": {node_id: envelope_json(node) for node_id, node in nodes.items()},
        "edges": [asdict(edge) for edge in unique],
        "truth_rule": "Route/path weight is navigation memory only; canonical authority and evidence outrank it.",
    }


def envelope_json(node: NodeEnvelope) -> dict[str, Any]:
    d = asdict(node)
    d["edges"] = [asdict(edge) for edge in node.edges]
    return d


SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\[])")
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)


def markdown_pages(text: str) -> list[dict[str, Any]]:
    """Logical pages: one H1/H2 section or ~1200-char bounded chunk."""
    lines = text.splitlines()
    pages: list[dict[str, Any]] = []
    current: list[str] = []
    heading = "(start)"

    def flush() -> None:
        nonlocal current, heading
        if not current:
            return
        body = "\n".join(current).strip()
        if not body:
            current = []
            return
        chunks = [body[i : i + 1200] for i in range(0, len(body), 1200)]
        for chunk in chunks:
            pages.append({"heading": heading, "text": chunk})
        current = []

    for line in lines:
        if re.match(r"^#{1,2}\s+", line):
            flush()
            heading = re.sub(r"^#{1,2}\s+", "", line).strip() or "(untitled)"
            current = [line]
        else:
            current.append(line)
    flush()
    return pages


def layer_document(path: Path, repo_root: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    file_id = stable_id("file", rel)
    pages = []
    for pno, page in enumerate(markdown_pages(text), start=1):
        page_id = stable_id("page", f"{file_id}:{page['heading']}:{pno}")
        paragraphs = []
        chunks = [x.strip() for x in re.split(r"\n\s*\n", page["text"]) if x.strip()]
        for pidx, paragraph in enumerate(chunks, start=1):
            paragraph_id = stable_id("paragraph", f"{page_id}:{pidx}:{paragraph[:80]}")
            sentences = []
            sentence_parts = [x.strip() for x in SENTENCE_RE.split(paragraph) if x.strip()]
            for sidx, sentence in enumerate(sentence_parts, start=1):
                sentence_id = stable_id("sentence", f"{paragraph_id}:{sidx}:{sentence}")
                words = [
                    {
                        "word_id": stable_id("word", f"{sentence_id}:{widx}:{m.group(0)}"),
                        "index": widx,
                        "text": m.group(0),
                        "start": m.start(),
                        "end": m.end(),
                    }
                    for widx, m in enumerate(WORD_RE.finditer(sentence), start=1)
                ]
                sentences.append(
                    {
                        "sentence_id": sentence_id,
                        "index": sidx,
                        "text": sentence,
                        "words": words,
                    }
                )
            paragraphs.append(
                {
                    "paragraph_id": paragraph_id,
                    "index": pidx,
                    "text": paragraph,
                    "sentences": sentences,
                }
            )
        pages.append(
            {
                "page_id": page_id,
                "index": pno,
                "heading": page["heading"],
                "paragraphs": paragraphs,
            }
        )
    return {
        "schema": "one-wave-layer-index-v1",
        "file_id": file_id,
        "path": rel,
        "sha256": sha256_bytes(raw),
        "pages": pages,
    }


def node_cache_path(node_id: str) -> Path:
    return RUNTIME_ROOT / "nodes" / f"{node_id}.json.gz"


def build_node_cache(root: Path, node: NodeEnvelope) -> dict[str, Any]:
    folder = root / node.canonical_path
    documents = []
    for path in sorted(folder.rglob("*.md")):
        if WATCHER_DIR in path.parts:
            continue
        documents.append(layer_document(path, root))
    cache = {
        "schema": "one-wave-node-cache-v1",
        "node": envelope_json(node),
        "documents": documents,
    }
    dump_gzip_json(node_cache_path(node.node_id), cache)
    return cache


def open_layer(root: Path, node_id: str, *, file_path: str | None = None,
               page: int | None = None, paragraph: int | None = None,
               sentence: int | None = None) -> dict[str, Any]:
    nodes = discover_nodes(root)
    if node_id not in nodes:
        raise KeyError(f"unknown node_id: {node_id}")
    cache_path = node_cache_path(node_id)
    cache = load_gzip_json(cache_path, {})
    if not cache or cache.get("node", {}).get("content_hash") != nodes[node_id].content_hash:
        cache = build_node_cache(root, nodes[node_id])

    docs = cache.get("documents", [])
    if file_path:
        docs = [d for d in docs if d.get("path") == file_path]
    result: Any = docs
    if page is not None:
        result = [p for d in docs for p in d.get("pages", []) if p.get("index") == page]
    if paragraph is not None:
        source_pages = result if page is not None else [p for d in docs for p in d.get("pages", [])]
        result = [p for pg in source_pages for p in pg.get("paragraphs", []) if p.get("index") == paragraph]
    if sentence is not None:
        source_paragraphs = result if paragraph is not None else [
            p for d in docs for pg in d.get("pages", []) for p in pg.get("paragraphs", [])
        ]
        result = [s for para in source_paragraphs for s in para.get("sentences", []) if s.get("index") == sentence]
    return {
        "node_id": node_id,
        "state": "active",
        "selection": result,
        "cache": str(cache_path),
    }


def memory_path() -> Path:
    return RUNTIME_ROOT / "route-memory.json.gz"


def route_memory() -> dict[str, Any]:
    return load_gzip_json(memory_path(), {"schema": "one-wave-route-memory-v1", "edges": {}})


def edge_key(source: str, target: str, edge_type: str) -> str:
    return f"{source}|{target}|{edge_type}"


def update_hysteresis(source: str, target: str, edge_type: str, outcome: str) -> dict[str, Any]:
    if outcome not in {"success", "hold", "failure", "irrelevant"}:
        raise ValueError("outcome must be success|hold|failure|irrelevant")
    memory = route_memory()
    edges = memory.setdefault("edges", {})
    key = edge_key(source, target, edge_type)
    state = edges.setdefault(key, {"score": 0.0, "uses": 0, "successes": 0, "holds": 0, "failures": 0})

    # Decay first so old history cannot become permanent lock-in.
    state["score"] = float(state.get("score", 0.0)) * 0.92
    delta = {"success": 0.22, "hold": -0.12, "failure": -0.25, "irrelevant": -0.18}[outcome]
    state["score"] = max(-1.0, min(1.0, state["score"] + delta))
    state["uses"] = int(state.get("uses", 0)) + 1
    if outcome == "success":
        state["successes"] = int(state.get("successes", 0)) + 1
    elif outcome == "hold":
        state["holds"] = int(state.get("holds", 0)) + 1
    else:
        state["failures"] = int(state.get("failures", 0)) + 1
    dump_gzip_json(memory_path(), memory)
    return state


def tokenize(value: str) -> set[str]:
    return {x.lower() for x in re.findall(r"[A-Za-z0-9_+-]{2,}", value)}


def route_candidates(root: Path, source_id: str, query: str) -> list[dict[str, Any]]:
    graph = graph_doc(root)
    nodes = graph["nodes"]
    if source_id not in nodes:
        raise KeyError(f"unknown source node: {source_id}")
    memory = route_memory().get("edges", {})
    query_terms = tokenize(query)

    outgoing = [e for e in graph["edges"] if e["source"] == source_id]
    scored: list[dict[str, Any]] = []
    for edge in outgoing:
        target = nodes.get(edge["target"])
        if not target:
            continue
        target_terms = tokenize(
            " ".join(
                [
                    target.get("canonical_path", ""),
                    target.get("role", ""),
                    " ".join(target.get("concept_tags", [])),
                    " ".join(target.get("authority_refs", [])),
                ]
            )
        )
        overlap = len(query_terms & target_terms) / max(1, len(query_terms))
        authority_match = 1.0 if edge["type"] in {"AUTHORITY_OF", "VALIDATES", "REFERENCES"} else 0.25
        dependency_match = 0.8 if edge["type"] in {"DEPENDS_ON", "DERIVES_FROM", "IMPLEMENTS"} else 0.2
        hysteresis = float(memory.get(edge_key(edge["source"], edge["target"], edge["type"]), {}).get("score", 0.0))
        hold_penalty = 1.0 if target.get("hold") else 0.0
        contradiction_risk = 0.8 if edge["type"] == "CONTRADICTS" else 0.0
        context_cost = min(1.0, len(target.get("authority_refs", [])) / 10.0)

        positive = authority_match + overlap + dependency_match + max(0.0, hysteresis)
        negative = hold_penalty + contradiction_risk + context_cost + max(0.0, -hysteresis)
        lean = positive - negative

        scored.append(
            {
                "source": source_id,
                "target": edge["target"],
                "edge_type": edge["type"],
                "positive": round(positive, 6),
                "negative": round(negative, 6),
                "lean": round(lean, 6),
                "components": {
                    "authority_match": authority_match,
                    "semantic_relevance": round(overlap, 6),
                    "dependency_match": dependency_match,
                    "path_hysteresis": round(hysteresis, 6),
                    "hold_penalty": hold_penalty,
                    "contradiction_risk": contradiction_risk,
                    "context_cost": context_cost,
                },
                "truth_warning": "Routing score is not evidence and cannot override canonical authority.",
            }
        )
    return sorted(scored, key=lambda x: x["lean"], reverse=True)


def main() -> int:
    ap = argparse.ArgumentParser(prog="owatch-lattice")
    ap.add_argument("--root", default=os.environ.get("ONE_WAVE_PROJECT_ROOT", "."))
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("scan")

    p = sub.add_parser("cache")
    p.add_argument("node_id")

    p = sub.add_parser("open")
    p.add_argument("node_id")
    p.add_argument("--file")
    p.add_argument("--page", type=int)
    p.add_argument("--paragraph", type=int)
    p.add_argument("--sentence", type=int)

    p = sub.add_parser("route")
    p.add_argument("source_id")
    p.add_argument("query")

    p = sub.add_parser("feedback")
    p.add_argument("source_id")
    p.add_argument("target_id")
    p.add_argument("edge_type")
    p.add_argument("outcome", choices=["success", "hold", "failure", "irrelevant"])

    args = ap.parse_args()
    root = Path(args.root).expanduser().resolve()

    if args.cmd == "scan":
        print(json.dumps(graph_doc(root), indent=2, sort_keys=True))
        return 0
    if args.cmd == "cache":
        nodes = discover_nodes(root)
        if args.node_id not in nodes:
            raise SystemExit(f"unknown node_id: {args.node_id}")
        print(json.dumps(build_node_cache(root, nodes[args.node_id]), indent=2, sort_keys=True))
        return 0
    if args.cmd == "open":
        print(json.dumps(open_layer(
            root,
            args.node_id,
            file_path=args.file,
            page=args.page,
            paragraph=args.paragraph,
            sentence=args.sentence,
        ), indent=2, sort_keys=True))
        return 0
    if args.cmd == "route":
        print(json.dumps(route_candidates(root, args.source_id, args.query), indent=2, sort_keys=True))
        return 0
    if args.cmd == "feedback":
        print(json.dumps(update_hysteresis(
            args.source_id, args.target_id, args.edge_type.upper(), args.outcome
        ), indent=2, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
