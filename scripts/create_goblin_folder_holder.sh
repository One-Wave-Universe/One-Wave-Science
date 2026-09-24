#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-Goblin Folder Holder}"
PARENT="${2:-$PWD}"

if [[ "$NAME" == */* || "$NAME" == "." || "$NAME" == ".." ]]; then
  echo "Invalid folder name" >&2
  exit 2
fi

TARGET="$PARENT/$NAME"
mkdir -p "$TARGET/.owatch"

cat >"$TARGET/.owatch/folder.json" <<'JSON'
{
  "schema": "one-wave-watched-folder-v1",
  "type": "goblin-folder-holder",
  "display_name": "Goblin Folder Holder",
  "mode": "fail_closed",
  "editing_granularity": ["word", "sentence", "line", "section", "file"],
  "reference_required": true,
  "intention_required": true,
  "consequence_required": true,
  "source_files_authoritative": true,
  "intervention": "HOLD",
  "rule": "Unknown state is inspected, never assumed. Change only the smallest authorized span."
}
JSON

cat >"$TARGET/.owatch/.gitignore" <<'EOF'
state.json
events.jsonl
HOLD.json
index.json
EOF

printf 'GOBLIN_FOLDER_HOLDER_CREATED=%s\n' "$TARGET"
