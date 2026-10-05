#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).parent / "cards"


def main() -> None:
    print("GREAT GALACTIC LIBRARY — shelf")
    for p in sorted(ROOT.glob("*.md")):
        if p.name.startswith("_"):
            continue
        lines = p.read_text().splitlines()
        title = lines[0].replace("# CARD: ", "").strip() if lines else p.stem
        fields = {}
        for line in lines:
            if line.startswith("- **") and ":" in line:
                k, _, v = line.partition(":")
                fields[k.strip("- *")] = v.strip()
        print(f"  {fields.get('id', '?'):8}  {title:20}  {fields.get('layer', ''):18}  {fields.get('gate', '')}")


if __name__ == "__main__":
    main()
