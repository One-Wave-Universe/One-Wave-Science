#!/usr/bin/env bash
set -euo pipefail

TOKEN_FILE="${HIVE_PIPE_TOKEN_FILE:-$HOME/.config/hive-pipe/tokens/gemini.token}"
if [[ ! -s "$TOKEN_FILE" ]]; then
  echo "GEMINI_HIVE_ERROR: missing Gemini Hive Pipe token: $TOKEN_FILE" >&2
  exit 2
fi

export HIVE_PIPE_GEMINI_TOKEN="$(<"$TOKEN_FILE")"
export HIVE_PIPE_MCP_URL="${HIVE_PIPE_MCP_URL:-http://127.0.0.1:8765/mcp}"
export GEMINI_CLI_TRUST_WORKSPACE=true

exec gemini "$@"
