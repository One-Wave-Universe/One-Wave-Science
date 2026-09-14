#!/usr/bin/env bash
set -euo pipefail

name="${1:-}"
if [[ -z "$name" || ! "$name" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "usage: $0 CLIENT_NAME" >&2
  exit 2
fi

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hive-pipe"
TOKEN_DIR="$CONFIG_DIR/tokens"
TOKEN_FILE="$TOKEN_DIR/$name.token"

mkdir -p "$TOKEN_DIR"
chmod 700 "$CONFIG_DIR" "$TOKEN_DIR"

if [[ -e "$TOKEN_FILE" ]]; then
  chmod 600 "$TOKEN_FILE"
  echo "EXISTS $TOKEN_FILE"
  exit 0
fi

umask 077
python3 -c 'import secrets; print(secrets.token_urlsafe(32))' > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"
echo "CREATED $TOKEN_FILE"
echo "Use this token only in the client's secure connector/API-key field."
