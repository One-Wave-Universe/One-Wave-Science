One-Wave Voice Forge -- Ubuntu release
=======================================

This is a prebuilt, ready-to-run copy of Voice Forge. No Python, pip,
or build tools are required -- everything the app needs is already
inside the VoiceForge/ folder next to this file.

INSTALL
-------
1. Extract this archive if you haven't already (double-click it in
   your file manager, or: tar xzf VoiceForge-Ubuntu-x86_64.tar.gz).
2. Open a terminal in the extracted folder and run:

       ./install.sh

   This copies the app to ~/.local/share/voiceforge/ and adds a
   "One-Wave Voice Forge" icon to your Desktop and your Applications
   menu. No sudo, no system-wide changes -- everything it touches is
   inside your own home folder.
3. Double-click the new Desktop icon (or find it in your Applications
   menu) to launch it.

If the Desktop icon shows a warning instead of launching the first
time (a GNOME/Nautilus quirk for new desktop shortcuts), right-click
it and choose "Allow Launching" -- after that it just works.

If the app doesn't launch at all, you're probably missing a couple of
system graphics/audio libraries that most Ubuntu desktops already
have. install.sh checks for them and prints the exact command to run,
e.g.:

    sudo apt-get install libegl1 libgl1 libxkbcommon0 libpulse0

UNINSTALL
---------
    ./uninstall.sh

Removes everything install.sh added: the app folder, the icon, and
both shortcuts.

WHAT IT DOES
------------
Voice Forge blends two or more reference voices into a new, reusable
character voice: load reference WAV files, adjust pitch/formant/body/
brightness/breathiness/etc. sliders, preview, then render to a plain
WAV file (plus a JSON "recipe" you can reopen and keep tuning). The
rendered WAV works in any other program or app, the same as any other
audio file.
