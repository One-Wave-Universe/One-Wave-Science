"""File Search worker: finds files, text, and simple def/class symbols --
real filesystem operations, no AI call needed."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}


@dataclass
class TextMatch:
    file_path: str
    line_number: int
    line_text: str


@dataclass
class SymbolMatch:
    file_path: str
    line_number: int
    symbol_kind: str  # "def" or "class"
    symbol_name: str


class FileSearchWorker:
    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root)

    def _iter_files(self, glob: str = "**/*"):
        for path in self.project_root.glob(glob):
            if not path.is_file():
                continue
            if any(part in DEFAULT_EXCLUDE_DIRS for part in path.parts):
                continue
            yield path

    def find_files(self, pattern: str) -> list[str]:
        return sorted(str(p.relative_to(self.project_root)) for p in self._iter_files(pattern))

    def search_text(self, query: str, glob: str = "**/*", case_sensitive: bool = False) -> list[TextMatch]:
        matches = []
        needle = query if case_sensitive else query.lower()
        for path in self._iter_files(glob):
            try:
                text = path.read_text(errors="ignore")
            except (UnicodeDecodeError, OSError):
                continue
            for line_number, line in enumerate(text.splitlines(), start=1):
                haystack = line if case_sensitive else line.lower()
                if needle in haystack:
                    matches.append(TextMatch(
                        file_path=str(path.relative_to(self.project_root)),
                        line_number=line_number,
                        line_text=line.strip(),
                    ))
        return matches

    def find_symbol(self, name: str, glob: str = "**/*.py") -> list[SymbolMatch]:
        pattern = re.compile(rf"^\s*(def|class)\s+({re.escape(name)})\b")
        matches = []
        for path in self._iter_files(glob):
            try:
                text = path.read_text(errors="ignore")
            except (UnicodeDecodeError, OSError):
                continue
            for line_number, line in enumerate(text.splitlines(), start=1):
                found = pattern.match(line)
                if found:
                    matches.append(SymbolMatch(
                        file_path=str(path.relative_to(self.project_root)),
                        line_number=line_number,
                        symbol_kind=found.group(1),
                        symbol_name=found.group(2),
                    ))
        return matches
