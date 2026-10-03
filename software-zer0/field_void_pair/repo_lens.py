"""Repo lens — the whole One-Wave repo as the shared reference both AIs see.

SOFTWARE ONLY. This builds text context. It is not memory and not the cell.

The lens has three layers, all deterministic:

1. CANON   fixed canonical files, read in order, truncated to a budget
2. MAP     every tracked file in the repo, grouped by directory
3. FOCUS   per-turn keyword retrieval over every tracked text file

Field and Void receive the same lens. That is the shared reference (0)
from UPDATED_34 section 3: two roles, one relational state.
"""

from __future__ import annotations

import io
import json
import math
import os
import re
import subprocess
import tarfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


# Read order follows CLAUDE.md -> AGENTS.md -> AI_CANONICAL_START_HERE.md,
# then the Field/Void and Algorythm-Zer0 references this tool runs on.
CANON_FILES = (
    "CLAUDE.md",
    "AGENTS.md",
    "GENERAL_REFERENCE_RULES.md",
    "AI_CANONICAL_START_HERE.md",
    "UPDATED_34_PROCESSING_IS_MEMORY_AND_DUAL_PROCESSOR_FIELD_VOID.md",
    "Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md",
    "proofs/ZER0_FIRST_CYCLE.md",
    "simulations/zer0_first_cycle.py",
    "software-zer0/SEPARATE.md",
    "ONE_WAVE_TERMINOLOGY_LEGEND.md",
)

TEXT_EXT = {
    ".md", ".txt", ".py", ".js", ".ts", ".html", ".css", ".json", ".csv",
    ".sh", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".tex", ".c", ".h",
    ".cpp", ".ino", ".rs", ".go", ".java", ".kt",
}
MAX_FILE_BYTES = 400_000
# Compressed text snapshot of the repo. Lets the program run with no checkout
# on disk; it is read in memory and never unpacked.
BUNDLE_NAME = "lens_bundle.tar.xz"
WORD = re.compile(r"[A-Za-z][A-Za-z0-9_\-]{3,}")
STOP = {
    "this", "that", "with", "from", "have", "into", "only", "must", "does",
    "then", "than", "when", "what", "will", "each", "same", "they", "them",
    "their", "there", "these", "those", "were", "been", "being", "which",
    "while", "about", "should", "would", "could", "make", "made", "true",
    "false", "none", "self", "return", "import", "class", "def",
}


def _is_root(p: Path) -> bool:
    return (p / "AGENTS.md").is_file() and (p / "simulations" / "zer0_first_cycle.py").is_file()


def find_repo_root(start: Path | None = None) -> Path:
    """FVPAIR_REPO wins (set by the desktop installer), else search upward."""
    env = os.environ.get("FVPAIR_REPO")
    if env and _is_root(Path(env).expanduser()):
        return Path(env).expanduser().resolve()
    here = (start or Path(__file__)).resolve()
    for p in [here, *here.parents]:
        if _is_root(p):
            return p
    raise FileNotFoundError(
        "One-Wave-Science repo not found. Set FVPAIR_REPO=/path/to/One-Wave-Science "
        "(the installer writes it to ~/.config/fvpair/env).")


def find_source(start: Path | None = None) -> Path:
    """A checkout if there is one, else the bundled snapshot. Never clones."""
    try:
        return find_repo_root(start)
    except FileNotFoundError:
        pass
    for cand in (os.environ.get("FVPAIR_BUNDLE"), str(Path(__file__).with_name(BUNDLE_NAME))):
        if cand and Path(cand).expanduser().is_file():
            return Path(cand).expanduser().resolve()
    raise FileNotFoundError(
        "No One-Wave repo and no lens bundle found. Set FVPAIR_REPO=/path/to/One-Wave-Science "
        f"or FVPAIR_BUNDLE=/path/to/{BUNDLE_NAME}.")


def list_tracked(root: Path) -> list[str]:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            capture_output=True, text=True, check=True,
        ).stdout
        files = [line for line in out.splitlines() if line]
        if files:
            return files
    except (OSError, subprocess.CalledProcessError):
        pass
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            files.append(str((Path(dirpath) / name).relative_to(root)))
    return sorted(files)


def reference_snapshot(root: Path) -> dict:
    """Reference Point Zero from AGENTS.md: record the route before acting."""

    def git(*args: str) -> str:
        try:
            return subprocess.run(
                ["git", "-C", str(root), *args],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return "unknown"

    status = git("status", "--porcelain")
    return {
        "root": str(root),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "head": git("rev-parse", "--short", "HEAD"),
        "dirty": bool(status) and status != "unknown",
    }


def write_bundle(root: Path, out: Path) -> Path:
    """Pack every tracked text file the lens reads, plus a manifest, into tar.xz."""
    root = Path(root)
    files = list_tracked(root)
    manifest = {"files": files, "snapshot": reference_snapshot(root) | {"root": "bundle"}}
    out.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out, "w:xz") as tar:
        data = json.dumps(manifest).encode()
        info = tarfile.TarInfo("manifest.json")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
        for rel in files:
            p = root / rel
            if p.suffix.lower() in TEXT_EXT and p.is_file() and p.stat().st_size <= MAX_FILE_BYTES:
                tar.add(p, arcname="repo/" + rel, recursive=False)
    return out


@dataclass
class RepoLens:
    root: Path
    canon_chars: int = 36_000
    focus_k: int = 6
    focus_chars: int = 1_400
    files: list[str] = field(default_factory=list)
    _text: dict[str, str] = field(default_factory=dict, repr=False)
    _terms: dict[str, Counter] = field(default_factory=dict, repr=False)
    _df: Counter = field(default_factory=Counter, repr=False)
    bundle: bool = False
    _snapshot: dict = field(default_factory=dict, repr=False)

    @classmethod
    def build(cls, root: Path | None = None, **kw) -> "RepoLens":
        src = Path(root) if root else find_source()
        lens = cls(root=src, **kw)
        if src.is_file():
            lens._load_bundle()
            return lens
        lens.files = list_tracked(lens.root)
        for rel in lens.files:
            p = lens.root / rel
            if p.suffix.lower() not in TEXT_EXT:
                continue
            try:
                if p.stat().st_size > MAX_FILE_BYTES:
                    continue
                txt = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            lens._index(rel, txt)
        return lens

    def _index(self, rel: str, txt: str) -> None:
        self._text[rel] = txt
        self._terms[rel] = Counter(
            w.lower() for w in WORD.findall(txt) if w.lower() not in STOP
        )
        self._df.update(self._terms[rel].keys())

    def _load_bundle(self) -> None:
        self.bundle = True
        with tarfile.open(self.root, "r:xz") as tar:
            for m in tar:
                if not m.isfile():
                    continue
                data = tar.extractfile(m).read()
                if m.name == "manifest.json":
                    manifest = json.loads(data)
                    self.files = manifest["files"]
                    self._snapshot = manifest.get("snapshot", {})
                elif m.name.startswith("repo/"):
                    self._index(m.name[5:], data.decode("utf-8", errors="replace"))
        self._snapshot = {**self._snapshot, "root": f"bundle:{self.root}"}

    def snapshot(self) -> dict:
        """Reference Point Zero for whatever the lens actually reads."""
        return dict(self._snapshot) if self.bundle else reference_snapshot(self.root)

    def source(self, rel: str) -> str:
        if rel not in self._text:
            raise FileNotFoundError(rel)
        return self._text[rel]

    # -- layer 1 -------------------------------------------------------
    def canon(self) -> str:
        per = max(1_000, self.canon_chars // len(CANON_FILES))
        parts = []
        for rel in CANON_FILES:
            txt = self._text.get(rel)
            if txt is None:
                parts.append(f"### {rel}\n(MISSING in this checkout — HOLD on claims that need it)\n")
                continue
            body = txt if len(txt) <= per else txt[:per] + f"\n...[truncated at {per} chars; full file in repo]"
            parts.append(f"### {rel}\n{body}\n")
        return "\n".join(parts)

    # -- layer 2 -------------------------------------------------------
    def repo_map(self, per_dir: int = 12) -> str:
        groups: dict[str, list[str]] = {}
        for rel in self.files:
            top = rel.split("/", 1)[0] if "/" in rel else "."
            groups.setdefault(top, []).append(rel)
        lines = [f"{len(self.files)} tracked files."]
        for top in sorted(groups):
            items = groups[top]
            if top == ".":
                lines.append(f"/ (root, {len(items)} files): " + ", ".join(items))
                continue
            shown = ", ".join(i.split("/", 1)[1] for i in items[:per_dir])
            more = f", ... +{len(items) - per_dir} more" if len(items) > per_dir else ""
            lines.append(f"{top}/ ({len(items)} files): {shown}{more}")
        return "\n".join(lines)

    # -- layer 3 -------------------------------------------------------
    def focus(self, query: str) -> list[tuple[str, str]]:
        q = [w.lower() for w in WORD.findall(query) if w.lower() not in STOP]
        if not q:
            return []
        qset = set(q)
        n = max(1, len(self._terms))
        idf = {w: math.log(1 + n / (1 + self._df.get(w, 0))) for w in qset}
        scored = []
        for rel, terms in self._terms.items():
            if rel in CANON_FILES:
                continue
            # tf-idf, damped by document length so huge files do not win by size
            length = math.log(10 + sum(terms.values()))
            score = sum(math.sqrt(terms.get(w, 0)) * idf[w] for w in qset) / length
            score += 1.5 * sum(idf[w] for w in qset if w in rel.lower())
            if score > 0:
                scored.append((score, rel))
        scored.sort(key=lambda t: (-t[0], t[1]))
        out = []
        for _, rel in scored[: self.focus_k]:
            txt = self._text[rel]
            low = txt.lower()
            hits = [low.find(w) for w in qset if low.find(w) >= 0]
            start = max(0, min(hits) - 200) if hits else 0
            out.append((rel, txt[start : start + self.focus_chars]))
        return out

    def render(self, query: str) -> str:
        focus = self.focus(query)
        focus_txt = "\n".join(f"### {rel}\n{snip}\n" for rel, snip in focus) or "(no keyword hits)"
        return (
            "=== ONE-WAVE REPO LENS (shared reference for Field and Void) ===\n\n"
            "--- CANON (read in order) ---\n" + self.canon() +
            "\n--- REPO MAP (whole repository) ---\n" + self.repo_map() +
            "\n\n--- FOCUS (retrieved for this turn) ---\n" + focus_txt
        )

    # -- grounding check (deterministic, used as branch X) -------------
    def cited_paths(self, text: str) -> tuple[list[str], list[str]]:
        """Return (paths that exist in the repo, path-like tokens that do not)."""
        known = set(self.files)
        tokens = set(re.findall(r"[A-Za-z0-9_\-./]+\.[A-Za-z0-9]{1,5}", text))
        tokens |= set(re.findall(r"`([^`\s]+)`", text))
        good, bad = [], []
        for t in sorted(tokens):
            t = t.strip("./`'\",;:()[]")
            if "/" not in t and not t.endswith((".md", ".py", ".html", ".js", ".json")):
                continue
            if t in known:
                good.append(t)
            elif "/" in t or t.endswith(".md"):
                bad.append(t)
        return sorted(set(good)), sorted(set(bad))
