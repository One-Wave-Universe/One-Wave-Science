#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -eq 0 ]]; then
  echo "Run this as the normal Jetson login user, not root." >&2
  exit 1
fi

command -v sudo >/dev/null 2>&1 || {
  echo "ERROR: sudo is required for the SSH server bootstrap" >&2
  exit 1
}

if ! command -v sshd >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y openssh-server
fi

sudo systemctl enable --now ssh

SSH_DIR="$HOME/.ssh"
AUTH="$SSH_DIR/authorized_keys"
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"
touch "$AUTH"
chmod 600 "$AUTH"

if [[ -n "${AI_SSH_PUBLIC_KEY:-}" ]]; then
  case "$AI_SSH_PUBLIC_KEY" in
    ssh-ed25519\ *|ssh-rsa\ *|ecdsa-sha2-nistp256\ *|sk-ssh-ed25519@openssh.com\ *)
      if ! grep -Fqx "$AI_SSH_PUBLIC_KEY" "$AUTH"; then
        printf '%s\n' "$AI_SSH_PUBLIC_KEY" >> "$AUTH"
        echo "Added AI public key to $AUTH"
      else
        echo "AI public key is already present."
      fi
      ;;
    *)
      echo "ERROR: AI_SSH_PUBLIC_KEY does not look like an OpenSSH public key" >&2
      exit 1
      ;;
  esac
else
  echo "SSH server is live. No AI key was added because AI_SSH_PUBLIC_KEY is unset."
  echo "When an AI/tool gives you a public key, add it with:"
  echo "  AI_SSH_PUBLIC_KEY='ssh-ed25519 AAAA... ai-name' bash scripts/enable_jetson_ssh.sh"
fi

echo
echo "SSH service:"
sudo systemctl --no-pager --full status ssh | sed -n '1,8p'
echo
echo "Jetson addresses:"
hostname -I 2>/dev/null || true
echo
echo "Login account: $USER"
echo "Test from another machine: ssh $USER@JETSON_IP"
