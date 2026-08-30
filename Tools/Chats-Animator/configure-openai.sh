#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$HOME/.config/one-wave-animator"
ENV_FILE="$CONFIG_DIR/openai.env"
mkdir -p "$CONFIG_DIR"

printf '\nOne-Wave Animator — OpenAI Director setup\n'
printf 'The animator handles ordinary frame commands locally.\n'
printf 'This key is used only when the Director or OpenAI art fallback is needed.\n\n'

if [[ -n "${OPENAI_API_KEY:-}" ]]; then
  printf 'OPENAI_API_KEY is already present in this shell.\n'
  read -r -p 'Save it for the animator launcher? [Y/n] ' answer
  answer="${answer:-Y}"
  if [[ "$answer" =~ ^[Nn]$ ]]; then exit 0; fi
  key="$OPENAI_API_KEY"
else
  read -r -s -p 'Paste your OpenAI API key (input hidden; blank skips): ' key
  printf '\n'
fi

if [[ -z "$key" ]]; then
  printf 'Skipped. The animator will still edit locally, but creative Director requests will report that OpenAI is not configured.\n'
  exit 0
fi

umask 077
{
  printf 'export OPENAI_API_KEY=%q\n' "$key"
  printf 'export ONE_WAVE_DIRECTOR_MODEL=%q\n' "gpt-5.6-sol"
  printf 'export ONE_WAVE_ASSET_BACKEND=%q\n' "auto"
  printf 'export ONE_WAVE_OLLAMA_IMAGE_MODEL=%q\n' "x/z-image-turbo"
  printf 'export ONE_WAVE_IMAGE_MODEL=%q\n' "gpt-image-2"
} > "$ENV_FILE"
chmod 600 "$ENV_FILE"

printf 'Saved securely for this Linux user: %s\n' "$ENV_FILE"
printf 'Director: GPT-5.6 Sol\n'
printf 'Art worker: local Ollama image generation first when supported; GPT-Image-2 fallback.\n'
