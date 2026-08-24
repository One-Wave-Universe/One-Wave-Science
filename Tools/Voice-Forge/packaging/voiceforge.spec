# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the One-Wave Voice Forge desktop app.

Paths are resolved relative to this spec file (via PyInstaller's
SPECPATH) so it can be built from any working directory:

    pyinstaller packaging/voiceforge.spec --noconfirm --clean

or just run packaging/build_ubuntu.sh, which calls this with sensible
build/dist locations under the project root.
"""
import os

PROJECT_ROOT = os.path.abspath(os.path.join(SPECPATH, ".."))  # noqa: F821 (SPECPATH is injected by PyInstaller)

a = Analysis(
    [os.path.join(PROJECT_ROOT, "main.py")],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=[(os.path.join(PROJECT_ROOT, "assets"), "assets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VoiceForge",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[os.path.join(PROJECT_ROOT, "assets", "icon.png")],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="VoiceForge",
)
