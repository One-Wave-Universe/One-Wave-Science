#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${ONE_WAVE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
CREATOR="$REPO_ROOT/scripts/create_goblin_folder_holder.sh"

if [[ ! -x "$CREATOR" ]]; then
  chmod +x "$CREATOR"
fi

installed=0

# Nemo: true right-click action.
if command -v nemo >/dev/null 2>&1 || [[ -d "$HOME/.local/share/nemo/actions" ]]; then
  mkdir -p "$HOME/.local/share/nemo/actions"
  cat >"$HOME/.local/share/nemo/actions/goblin-folder-holder.nemo_action" <<EOF
[Nemo Action]
Name=Create Goblin Folder Holder
Comment=Create a protected OWATCH anti-drift folder here
Exec=$CREATOR "Goblin Folder Holder" %P
Selection=none
Extensions=dir;
Quote=double
EOF
  installed=1
  echo "INSTALLED_NEMO_ACTION"
fi

# Dolphin/KDE: service menu.
if command -v dolphin >/dev/null 2>&1 || [[ -d "$HOME/.local/share/kio/servicemenus" ]]; then
  mkdir -p "$HOME/.local/share/kio/servicemenus"
  cat >"$HOME/.local/share/kio/servicemenus/goblin-folder-holder.desktop" <<EOF
[Desktop Entry]
Type=Service
MimeType=inode/directory;
Actions=createGoblinFolderHolder;
X-KDE-ServiceTypes=KonqPopupMenu/Plugin

[Desktop Action createGoblinFolderHolder]
Name=Create Goblin Folder Holder
Exec=$CREATOR "Goblin Folder Holder" %f
EOF
  chmod +x "$HOME/.local/share/kio/servicemenus/goblin-folder-holder.desktop"
  installed=1
  echo "INSTALLED_DOLPHIN_ACTION"
fi

# Nautilus: supported via Scripts submenu without guessing an extension ABI.
if command -v nautilus >/dev/null 2>&1 || [[ -d "$HOME/.local/share/nautilus/scripts" ]]; then
  mkdir -p "$HOME/.local/share/nautilus/scripts"
  cat >"$HOME/.local/share/nautilus/scripts/Create Goblin Folder Holder" <<EOF
#!/usr/bin/env bash
set -euo pipefail
target="${NAUTILUS_SCRIPT_CURRENT_URI#file://}"
target="${target:-$PWD}"
exec "$CREATOR" "Goblin Folder Holder" "$target"
EOF
  chmod +x "$HOME/.local/share/nautilus/scripts/Create Goblin Folder Holder"
  installed=1
  echo "INSTALLED_NAUTILUS_SCRIPT"
fi

mkdir -p "$HOME/.local/share/applications"
cat >"$HOME/.local/share/applications/goblin-folder-holder.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Goblin Folder Holder
Comment=Protected layered anti-drift OWATCH folder
Exec=$CREATOR "Goblin Folder Holder" %f
Terminal=false
Categories=Development;
EOF

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true
fi

echo "GOBLIN_FOLDER_HOLDER_REGISTERED"
if [[ "$installed" -eq 0 ]]; then
  echo "NO_SUPPORTED_FILE_MANAGER_DETECTED"
fi
