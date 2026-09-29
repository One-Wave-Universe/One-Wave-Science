#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-Goblin Folder Holder}"
PARENT="${2:-$PWD}"

if [[ "$NAME" == */* || "$NAME" == "." || "$NAME" == ".." ]]; then
  echo "Invalid folder name" >&2
  exit 2
fi

TARGET="$PARENT/$NAME"
mkdir -p "$TARGET/.goblin-holder"

cat >"$TARGET/.goblin-holder/holder.json" <<'JSON'
{
  "schema": "one-wave-goblin-folder-holder-v1",
  "type": "goblin-folder-holder",
  "display_name": "Goblin Folder Holder",
  "role": "foreman",
  "discovers": ".owatch/folder.json",
  "mode": "fail_closed",
  "reference_required": true,
  "intention_required": true,
  "consequence_required": true,
  "commit_gate": true,
  "rule": "Supervise child watched folders, prevent cross-folder drift, and commit only when the supervised group is clean."
}
JSON

cat >"$TARGET/.goblin-holder/.gitignore" <<'EOF'
group-index.json
events.jsonl
HOLD.json
EOF

printf 'GOBLIN_FOLDER_HOLDER_CREATED=%s\n' "$TARGET"
