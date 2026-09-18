# One-Wave Miniverse Desktop App

This is the native laptop shell for the Jetson Miniverse room.

It uses GTK3 + WebKitGTK and creates a private SSH local forward:

\`\`\`text
laptop app
  -> 127.0.0.1:18787
  -> SSH
  -> Jetson 127.0.0.1:8787
\`\`\`

The Jetson room remains loopback-only. Do not bind it to \`0.0.0.0\` merely to
make the laptop app work.

## Install

On the laptop:

\`\`\`bash
bash Miniverse/desktop/install_laptop.sh
\`\`\`

The installer creates:

\`\`\`text
~/.local/share/one-wave-miniverse/
~/.local/share/applications/one-wave-miniverse.desktop
~/Desktop/One-Wave-Miniverse.desktop
\`\`\`

The default config prefers the direct Jetson USB network at \`192.168.55.1\`
and falls back to the current LAN address.

The laptop needs the dedicated private key:

\`\`\`text
~/.ssh/one_wave_miniverse_ed25519
\`\`\`

Only its public key belongs in the Jetson \`authorized_keys\`.

## Runtime

Click **One-Wave Miniverse** on the desktop. The program opens its own GTK
window, creates the SSH tunnel in the background, then embeds the same 3D world
served by the Jetson.

Closing the app closes the tunnel it owns. The Jetson world keeps running and
its persistent state is unchanged.
