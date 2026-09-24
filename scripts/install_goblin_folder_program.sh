#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${ONE_WAVE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
PROGRAM_SRC="$REPO_ROOT/scripts/goblin_folder.py"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"

mkdir -p "$BIN_DIR" "$APP_DIR"
install -m 0755 "$PROGRAM_SRC" "$BIN_DIR/goblin-folder"

cat >"$APP_DIR/goblin-folder.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Goblin Folder Manager
Comment=Create and manage Goblin Folder Holder and OWATCH folder types
Exec=$BIN_DIR/goblin-folder type %f
Terminal=true
Categories=Development;Utility;
MimeType=inode/directory;
EOF

# Nemo: direct context actions.
if command -v nemo >/dev/null 2>&1 || [[ -d "$HOME/.local/share/nemo/actions" ]]; then
  mkdir -p "$HOME/.local/share/nemo/actions"
  cat >"$HOME/.local/share/nemo/actions/goblin-create-holder.nemo_action" <<EOF
[Nemo Action]
Name=Create Goblin Folder Holder Here
Comment=Create a supervisory Goblin Folder Holder in this directory
Exec=$BIN_DIR/goblin-folder create-holder %P/"Goblin Folder Holder"
Selection=none
Extensions=dir;
Quote=double
EOF
  cat >"$HOME/.local/share/nemo/actions/goblin-make-watch.nemo_action" <<EOF
[Nemo Action]
Name=Make This an OWATCH Folder
Comment=Register the selected folder as an OWATCH protected folder
Exec=$BIN_DIR/goblin-folder adopt owatch %F
Selection=s;
Extensions=dir;
Quote=double
EOF
fi

# Nautilus: Scripts submenu. Works without assuming a Python extension ABI.
if command -v nautilus >/dev/null 2>&1 || [[ -d "$HOME/.local/share/nautilus/scripts" ]]; then
  mkdir -p "$HOME/.local/share/nautilus/scripts"
  cat >"$HOME/.local/share/nautilus/scripts/Create Goblin Folder Holder" <<EOF
#!/usr/bin/env bash
set -euo pipefail
parent="${NAUTILUS_SCRIPT_CURRENT_URI#file://}"
exec "$BIN_DIR/goblin-folder" create-holder "$parent/Goblin Folder Holder"
EOF
  chmod +x "$HOME/.local/share/nautilus/scripts/Create Goblin Folder Holder"

  cat >"$HOME/.local/share/nautilus/scripts/Make Selected Folder OWATCH" <<EOF
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n'
for uri in $NAUTILUS_SCRIPT_SELECTED_URIS; do
  path="${uri#file://}"
  "$BIN_DIR/goblin-folder" adopt owatch "$path"
done
EOF
  chmod +x "$HOME/.local/share/nautilus/scripts/Make Selected Folder OWATCH"
fi

# Dolphin/KDE service menus.
if command -v dolphin >/dev/null 2>&1 || [[ -d "$HOME/.local/share/kio/servicemenus" ]]; then
  mkdir -p "$HOME/.local/share/kio/servicemenus"
  cat >"$HOME/.local/share/kio/servicemenus/goblin-folder.desktop" <<EOF
[Desktop Entry]
Type=Service
MimeType=inode/directory;
Actions=createHolder;makeOwatch;
X-KDE-ServiceTypes=KonqPopupMenu/Plugin

[Desktop Action createHolder]
Name=Create Goblin Folder Holder Here
Exec=$BIN_DIR/goblin-folder create-holder %f/"Goblin Folder Holder"

[Desktop Action makeOwatch]
Name=Make This an OWATCH Folder
Exec=$BIN_DIR/goblin-folder adopt owatch %f
EOF
  chmod +x "$HOME/.local/share/kio/servicemenus/goblin-folder.desktop"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
fi

echo "GOBLIN_FOLDER_PROGRAM_INSTALLED=$BIN_DIR/goblin-folder"
"$BIN_DIR/goblin-folder" type "$REPO_ROOT"
