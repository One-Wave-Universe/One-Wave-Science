#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(dirname -- "$(dirname -- "$SCRIPT_DIR")")"
PROJECT_ROOT="${ONE_WAVE_PROJECT_ROOT:-$REPO_ROOT}"
EXTERNAL_WORK_ROOT="${ONE_WAVE_EXTERNAL_WORK:-$HOME/One-Wave-External-Work}"
REFERENCE_STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave"
ALLOWED_ROOTS_INPUT="${HIVE_PIPE_ALLOWED_ROOTS:-$PROJECT_ROOT:$EXTERNAL_WORK_ROOT}"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe"
TOKEN_DIR="$CONFIG_DIR/tokens"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
GATEWAY_SERVICE="$SYSTEMD_DIR/hive-pipe-gateway.service"
AGENT_SERVICE="$SYSTEMD_DIR/hive-pipe-agent.service"

mkdir -p "$TOKEN_DIR" "$SYSTEMD_DIR"
mkdir -p "$EXTERNAL_WORK_ROOT/inbox" "$EXTERNAL_WORK_ROOT/work" "$EXTERNAL_WORK_ROOT/outbox"
mkdir -p "$REFERENCE_STATE_ROOT"
chmod 700 "$REFERENCE_STATE_ROOT"
chmod 700 "$CONFIG_DIR" "$TOKEN_DIR"

# First-class AI clients. Additional clients can be added with create_client_token.sh.
for agent in codex claude gemini perplexity; do
  token_file="$TOKEN_DIR/$agent.token"
  if [[ ! -e "$token_file" ]]; then
    umask 077
    python3 -c 'import secrets; print(secrets.token_urlsafe(32))' > "$token_file"
  fi
  chmod 600 "$token_file"
done

escape_systemd_path() {
  printf '%s' "$1" | sed 's/ /\\x20/g'
}

escaped_root="$(escape_systemd_path "$SCRIPT_DIR")"
escaped_repo="$(escape_systemd_path "$REPO_ROOT")"
escaped_external="$(escape_systemd_path "$EXTERNAL_WORK_ROOT")"
write_paths="$escaped_repo $escaped_external"
allowed_roots=""
IFS=':' read -r -a requested_roots <<< "$ALLOWED_ROOTS_INPUT"
for requested_root in "${requested_roots[@]}"; do
  [[ -n "$requested_root" ]] || continue
  if [[ "$requested_root" != /* ]]; then
    echo "HIVE_PIPE_INSTALL_ERROR: allowed root must be absolute: $requested_root" >&2
    exit 2
  fi
  resolved_root="$(readlink -f -- "$requested_root")"
  if [[ ! -d "$resolved_root" ]]; then
    echo "HIVE_PIPE_INSTALL_ERROR: allowed root is not a directory: $resolved_root" >&2
    exit 2
  fi
  case "$resolved_root" in
    /|/etc|/usr|/var|/boot|/dev|/proc|/sys)
      echo "HIVE_PIPE_INSTALL_ERROR: broad/system root refused: $resolved_root" >&2
      exit 2
      ;;
    "$HOME"/*|/mnt/*|/media/*|/run/media/*) ;;
    *)
      echo "HIVE_PIPE_INSTALL_ERROR: root must be under HOME, /mnt, /media, or /run/media: $resolved_root" >&2
      exit 2
      ;;
  esac
  [[ -z "$allowed_roots" ]] || allowed_roots="$allowed_roots:"
  allowed_roots="$allowed_roots$resolved_root"
  write_paths="$write_paths $(escape_systemd_path "$resolved_root")"
done
if [[ -z "$allowed_roots" ]]; then
  echo "HIVE_PIPE_INSTALL_ERROR: no authorized work roots" >&2
  exit 2
fi
escaped_allowed_roots="$(escape_systemd_path "$allowed_roots")"
if [[ -d "$PROJECT_ROOT" && "$PROJECT_ROOT" != "$REPO_ROOT" ]]; then
  escaped_project="$(escape_systemd_path "$PROJECT_ROOT")"
  write_paths="$write_paths $escaped_project"
else
  escaped_project=""
fi

{
  echo '[Unit]'
  echo 'Description=One-Wave Hive Pipe Agent Gateway'
  echo 'After=network.target'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "WorkingDirectory=$escaped_root"
  echo "Environment=HIVE_PIPE_TOKEN_DIR=$TOKEN_DIR"
  echo "Environment=ONE_WAVE_EXTERNAL_WORK=$escaped_external"
  echo "Environment=REFERENCE_GATE_LEDGER=$(escape_systemd_path "$REFERENCE_STATE_ROOT/reference-receipts.jsonl")"
  echo "Environment=ONE_WAVE_PROJECT_ROOT=$(escape_systemd_path "$PROJECT_ROOT")"
  echo "Environment=HIVE_PIPE_ALLOWED_ROOTS=$escaped_allowed_roots"
  echo "ExecStart=/usr/bin/python3 $escaped_root/gateway.py --host 127.0.0.1 --port 8765"
  echo 'Restart=on-failure'
  echo 'RestartSec=3'
  echo 'NoNewPrivileges=true'
  echo 'PrivateTmp=true'
  echo 'ProtectSystem=strict'
  # AI may build/edit the live Hive Pipe checkout, the canonical project checkout
  # when present, and the explicit external-work workspace. System paths remain
  # read-only and privilege escalation remains blocked.
  echo "ReadWritePaths=$write_paths $(escape_systemd_path "$REFERENCE_STATE_ROOT")"
  echo
  echo '[Install]'
  echo 'WantedBy=default.target'
} > "$GATEWAY_SERVICE"

{
  echo '[Unit]'
  echo 'Description=One-Wave Parser Goblin Relay'
  echo 'After=network.target hive-pipe-gateway.service'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "WorkingDirectory=$escaped_root"
  echo "Environment=ONE_WAVE_PROJECT_ROOT=$(escape_systemd_path "$PROJECT_ROOT")"
  echo "Environment=REFERENCE_GATE_LEDGER=$(escape_systemd_path "$REFERENCE_STATE_ROOT/reference-receipts.jsonl")"
  echo "ExecStart=/usr/bin/python3 $escaped_root/parser_goblin.py --watch"
  echo 'Restart=always'
  echo 'RestartSec=2'
  echo 'NoNewPrivileges=true'
  echo 'PrivateTmp=true'
  echo 'ProtectSystem=strict'
  echo "ReadWritePaths=$write_paths $(escape_systemd_path "$REFERENCE_STATE_ROOT") $(escape_systemd_path "$HOME/.local/state/one-wave-parser-goblin")"
  echo
  echo '[Install]'
  echo 'WantedBy=default.target'
} > "$PARSER_GOBLIN_SERVICE"

{
  echo '[Unit]'
  echo 'Description=One-Wave Folder Reference Watcher'
  echo 'After=network.target'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "WorkingDirectory=$escaped_project"
  echo "Environment=ONE_WAVE_PROJECT_ROOT=$(escape_systemd_path "$PROJECT_ROOT")"
  echo "Environment=REFERENCE_GATE_LEDGER=$(escape_systemd_path "$REFERENCE_STATE_ROOT/reference-receipts.jsonl")"
  echo "ExecStart=/usr/bin/python3 $escaped_root/folder_watcher.py --root $(escape_systemd_path "$PROJECT_ROOT") --watch --interval 3"
  echo 'Restart=always'
  echo 'RestartSec=2'
  echo 'NoNewPrivileges=true'
  echo 'PrivateTmp=true'
  echo 'ProtectSystem=strict'
  echo "ReadWritePaths=$write_paths $(escape_systemd_path "$REFERENCE_STATE_ROOT")"
  echo
  echo '[Install]'
  echo 'WantedBy=default.target'
} > "$WATCHER_SERVICE"

{
  echo '[Unit]'
  echo 'Description=One-Wave Hive Pipe Queue Worker'
  echo 'After=network.target'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "WorkingDirectory=$escaped_root"
  echo "ExecStart=/usr/bin/bash $escaped_root/agent.sh --watch"
  echo 'Restart=on-failure'
  echo 'RestartSec=3'
  echo 'NoNewPrivileges=true'
  echo 'PrivateTmp=true'
  echo 'ProtectSystem=strict'
  echo "ReadWritePaths=$escaped_root/queue"
  echo
  echo '[Install]'
  echo 'WantedBy=default.target'
} > "$AGENT_SERVICE"

systemctl --user daemon-reload
systemctl --user disable --now hive-pipe.service 2>/dev/null || true
systemctl --user enable --now one-wave-folder-watcher.service parser-goblin.service hive-pipe-agent.service hive-pipe-gateway.service
systemctl --user restart one-wave-folder-watcher.service parser-goblin.service hive-pipe-agent.service hive-pipe-gateway.service
echo "HIVE_PIPE_GATEWAY_INSTALLED"
echo "Folder watcher: one-wave-folder-watcher.service"
echo "Parser Goblin: parser-goblin.service"
echo "Local endpoint: http://127.0.0.1:8765"
echo "AI terminal: terminal_pwd / terminal_which / terminal_run via MCP"
echo "Writable live checkout: $REPO_ROOT"
if [[ -n "$escaped_project" ]]; then
  echo "Writable canonical checkout: $PROJECT_ROOT"
fi
echo "Writable external work: $EXTERNAL_WORK_ROOT"
echo "Authorized terminal roots: $allowed_roots"
echo "Tokens: $TOKEN_DIR (0600; never commit or paste them into the public repository)"
echo "Default clients: codex, claude, gemini, perplexity"
