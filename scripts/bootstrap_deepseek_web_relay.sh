#!/usr/bin/env bash
set -euo pipefail

STATE="${XDG_STATE_HOME:-$HOME/.local/state}/one-wave-deepseek-web"
VENV="$STATE/venv"
PROFILE="$STATE/firefox-profile"
RELAY="$STATE/deepseek_web_relay.py"
SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE="$SERVICE_DIR/one-wave-deepseek-web-relay.service"
RAW_URL="${DEEPSEEK_RELAY_SOURCE_URL:-https://raw.githubusercontent.com/One-Wave-Universe/One-Wave-Science/main/One_Wave_Bench/hive-pipe/deepseek_web_relay.py}"

mkdir -p "$STATE" "$SERVICE_DIR"
chmod 700 "$STATE"

command -v firefox >/dev/null 2>&1 || { echo "Firefox is required"; exit 2; }
GECKO="/snap/firefox/current/usr/lib/firefox/geckodriver"
FIREFOX_BIN="/snap/firefox/current/usr/lib/firefox/firefox"
[[ -x "$GECKO" && -x "$FIREFOX_BIN" ]] || { echo "Firefox/geckodriver not found in expected snap path"; exit 2; }

if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
  "$VENV/bin/python" -m pip install --upgrade pip
  "$VENV/bin/python" -m pip install selenium
fi

if [[ ! -d "$PROFILE" ]]; then
  SOURCE_PROFILE="$(python3 - <<'PY'
from pathlib import Path
roots=[Path.home()/"snap/firefox/common/.mozilla/firefox", Path.home()/".mozilla/firefox"]
candidates=[]
for root in roots:
    if not root.exists(): continue
    for p in root.iterdir():
        if not p.is_dir(): continue
        score=0
        for session in p.glob("sessionstore-backups/*.jsonlz4"):
            try:
                data=session.read_bytes()
            except OSError:
                continue
            if b"deepseek" in data.lower(): score+=1000000
            score+=int(session.stat().st_mtime)
        if score: candidates.append((score,p))
if candidates:
    print(max(candidates)[1])
PY
)"
  [[ -n "$SOURCE_PROFILE" && -d "$SOURCE_PROFILE" ]] || { echo "No Firefox profile found"; exit 2; }
  rsync -a --exclude='lock' --exclude='.parentlock' --exclude='parent.lock' "$SOURCE_PROFILE/" "$PROFILE/"
  chmod -R go-rwx "$PROFILE"
fi

python3 - "$RAW_URL" "$RELAY" <<'PY'
from pathlib import Path
import sys
from urllib.request import urlopen
url,dest=sys.argv[1],Path(sys.argv[2])
dest.write_bytes(urlopen(url,timeout=30).read())
PY
chmod 600 "$RELAY"

cat >"$SERVICE" <<EOF
[Unit]
Description=One-Wave DeepSeek free web Brain Buddy relay
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=$VENV/bin/python $RELAY --bind 192.168.55.100 --port 3000 --profile $PROFILE
Restart=always
RestartSec=5
Environment=DEEPSEEK_WEB_RELAY_ALLOWED_CLIENTS=127.0.0.1,192.168.55.1
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$STATE

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now one-wave-deepseek-web-relay.service

for _ in 1 2 3 4 5 6; do
  if python3 - <<'PY' >/dev/null 2>&1
from urllib.request import urlopen
with urlopen("http://192.168.55.100:3000/health", timeout=2) as r:
    raise SystemExit(0 if r.status == 200 else 1)
PY
  then
    echo "DEEPSEEK_FREE_WEB_RELAY_HEALTHY"
    exit 0
  fi
  sleep 2
done

systemctl --user --no-pager --plain status one-wave-deepseek-web-relay.service || true
exit 1
