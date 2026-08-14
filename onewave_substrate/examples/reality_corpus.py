"""Parser for the repository's own One-Wave canonical corpus.

This repo (One-Wave-Science) already contains a large body of real
concept definitions written from a single, consistent interpretive
stance -- the One-Wave lens -- as numbered "Node" and "Root Axiom"
markdown files under Nodes/ and Root_Axioms/. Each file has YAML
frontmatter (node_id, canonical_name, gate, lifecycle, classification)
plus a body containing a definition and a DEPENDENCIES section listing
other node ids it builds on.

This module turns one such file into a plain dict the ingestion builder
(build_reality_database.py) can hand to the substrate -- it does not
touch the database itself.

The corpus is NOT uniformly formatted: roughly a tenth of the files use a
strict numbered "1. PURPOSE / 2. DEFINITION / 3. ..." layout, the rest
use a looser "Definition: <prose>" layout with varying section labels.
`extract_definition` tries the strict layout first, falls back to the
loose layout, and finally falls back to the first paragraph of body text
-- every file yields *some* definition text, never a silent skip, but
callers should treat the fallback tier as lower-confidence extraction.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
NUMBERED_DEF_RE = re.compile(r"^\s*\d+\.\s*DEFINITION\s*$", re.IGNORECASE | re.MULTILINE)
NUMBERED_NEXT_RE = re.compile(r"^\s*\d+\.\s+\S", re.MULTILINE)
MARKDOWN_DEF_HEADING_RE = re.compile(r"^\s*#{1,6}\s*Definition\s*$", re.IGNORECASE | re.MULTILINE)
MARKDOWN_PURPOSE_HEADING_RE = re.compile(r"^\s*#{1,6}\s*Purpose\s*$", re.IGNORECASE | re.MULTILINE)
PLAIN_DEF_RE = re.compile(r"^\s*Definition:\s*$", re.IGNORECASE | re.MULTILINE)
HEADING_RE = re.compile(r"^\s*#{1,6}\s")
LABEL_LINE_RE = re.compile(r"^\s*\**[A-Z][A-Za-z /_\-]{1,40}:\**\s*$")
UPSTREAM_START_RE = re.compile(r"UPSTREAM:\s*", re.IGNORECASE)
UPSTREAM_STOP_RE = re.compile(
    r"\n\s*(DOWNSTREAM|LATERAL|BIDIRECTIONAL)\s*[:/]|\n\s*\n|\n\s*#|\n\s*\d+\.\s+\S",
    re.IGNORECASE,
)
NODE_ID_RE = re.compile(r"\b([A-G][+\-]\d{3}[a-z]?)\b")

# Block headers that introduce metadata/relationship scaffolding rather
# than definitional prose -- skipped whole (header + body) when scanning
# paragraph blocks for the fallback-tier extraction strategy.
STRUCTURAL_BLOCK_HEADS = {
    "dependencies", "upstream", "downstream", "lateral", "bidirectional",
    "class", "placement", "layer", "name disambiguation", "standard mapping",
    "input", "output", "branch",
}

GATE_MATURITY = {"GREEN": 0.2, "YELLOW": 0.4, "BRONZE": 0.6, "SILVER": 0.8, "GOLD": 1.0}


@dataclass(frozen=True)
class ParsedNode:
    node_id: str
    canonical_name: str
    namespace: str
    gate: str
    lifecycle: str
    classification: str
    definition: str
    upstream_ids: tuple[str, ...]
    source_file: str


def _clean(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return " ".join(lines).strip()


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta, m.group(2)


def _text_until_heading_or_label(body: str, start: int) -> str:
    collected = []
    for line in body[start:].splitlines():
        stripped = line.strip()
        if HEADING_RE.match(stripped) or LABEL_LINE_RE.match(stripped):
            break
        collected.append(line)
    return _clean("\n".join(collected))


def _paragraph_blocks(body: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in body.splitlines():
        if line.strip():
            current.append(line)
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def _block_header_word(block: list[str]) -> str:
    first = block[0].strip().strip("*").strip("#").strip()
    return first.rstrip(":").strip().lower()


def extract_definition(body: str) -> tuple[str, str]:
    """Returns (text, tier) describing which extraction strategy produced
    the definition text: "numbered", "markdown_definition",
    "markdown_purpose", "plain", or "fallback" (lowest confidence)."""
    m = NUMBERED_DEF_RE.search(body)
    if m:
        rest = body[m.end():]
        stop = NUMBERED_NEXT_RE.search(rest)
        text = _clean(rest[: stop.start()] if stop else rest)
        if text:
            return text, "numbered"

    m = MARKDOWN_DEF_HEADING_RE.search(body)
    if m:
        text = _text_until_heading_or_label(body, m.end())
        if text:
            return text, "markdown_definition"

    m = PLAIN_DEF_RE.search(body)
    if m:
        text = _text_until_heading_or_label(body, m.end())
        if text:
            return text, "plain"

    m = MARKDOWN_PURPOSE_HEADING_RE.search(body)
    if m:
        text = _text_until_heading_or_label(body, m.end())
        if text:
            return text, "markdown_purpose"

    # Fallback: first paragraph block after the title that isn't itself
    # structural scaffolding (Dependencies/Upstream/Class/Placement/...).
    blocks = _paragraph_blocks(body)
    for i, block in enumerate(blocks[1:], start=1):  # blocks[0] is the title
        header = _block_header_word(block)
        if header in STRUCTURAL_BLOCK_HEADS:
            continue
        if HEADING_RE.match(block[0].strip()) and len(block) == 1:
            continue  # a bare heading line with no body directly under it
        candidate = block[1:] if HEADING_RE.match(block[0].strip()) else block
        text = _clean("\n".join(candidate))
        if not text:
            continue
        # A colon-terminated lead-in ("This node formalizes one claim:")
        # is a fragment, not a definition -- pull in following blocks
        # until the text reads as a complete statement or blocks run out.
        j = i + 1
        while text.endswith(":") and j < len(blocks):
            text = _clean(text + " " + " ".join(blocks[j]))
            j += 1
        return text, "fallback"

    return "(no definition text extracted)", "fallback"


def extract_upstream_ids(body: str) -> tuple[str, ...]:
    m = UPSTREAM_START_RE.search(body)
    if not m:
        return ()
    rest = body[m.end():]
    stop = UPSTREAM_STOP_RE.search(rest)
    segment = rest[: stop.start()] if stop else rest[:400]
    return tuple(sorted(set(NODE_ID_RE.findall(segment))))


def parse_node_file(path: Path) -> ParsedNode | None:
    text = path.read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(text)
    node_id = meta.get("node_id")
    if not node_id:
        return None
    definition, _tier = extract_definition(body)
    return ParsedNode(
        node_id=node_id,
        canonical_name=meta.get("canonical_name", node_id),
        namespace=meta.get("namespace", "NODE"),
        gate=meta.get("gate", ""),
        lifecycle=meta.get("lifecycle", ""),
        classification=meta.get("classification", ""),
        definition=definition,
        upstream_ids=extract_upstream_ids(body),
        source_file=str(path),
    )


def load_corpus(nodes_dir: Path, root_axioms_dir: Path) -> list[ParsedNode]:
    parsed: list[ParsedNode] = []
    for directory in (root_axioms_dir, nodes_dir):
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            node = parse_node_file(path)
            if node is not None:
                parsed.append(node)
    return parsed


SERIES_FIELDS = {
    "A": ("one_wave.a_foundations", "A-Series: Foundations"),
    "B": ("one_wave.b_balance", "B-Series: Balance, Threshold & Choice"),
    "C": ("one_wave.c_mechanics", "C-Series: Mechanics & Physics Candidates"),
    "D": ("one_wave.d_resonance", "D-Series: Resonance & Lattice"),
    "E": ("one_wave.e_extended", "E-Series: Extended & Cross-Domain Physics"),
    "F": ("one_wave.f_interaction", "F-Series: Interaction & Transfer"),
    "G": ("one_wave.g_evaluation", "G-Series: Evaluation, Gates & Decision"),
}


def field_for_node(node: ParsedNode) -> tuple[str, str]:
    """Returns (field_id, field_name) for this node's node_id prefix."""
    if node.namespace.upper() == "ROOT_AXIOM":
        return "one_wave.root_axioms", "Root Axioms"
    letter = node.node_id[0].upper()
    return SERIES_FIELDS.get(letter, ("one_wave.other", "Other"))


def confidence_for_gate(gate: str) -> float | None:
    return GATE_MATURITY.get(gate.upper())
