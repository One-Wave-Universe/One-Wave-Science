#!/usr/bin/env python3
from pathlib import Path
import zipfile, json, shutil
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
FILES = ['manifest.json','background.js','content.js','content.css','popup.html','popup.css','popup.js','options.html','options.css','options.js','lib/rules.js','lib/project.js','rules/default-rules.json']
def build_archive(name, install_text):
    target = DIST / name
    if target.exists(): target.unlink()
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for rel in FILES: z.write(ROOT / rel, rel)
        z.writestr('INSTALL.txt', install_text)
    return target
manifest=json.loads((ROOT/'manifest.json').read_text())
assert manifest['manifest_version']==3
assert manifest['name']=='Code by Law'
assert manifest['browser_specific_settings']['gecko']['id']=='code-by-law@one-wave.local'
assert 'gecko_android' in manifest['browser_specific_settings']
DIST.mkdir(exist_ok=True)
desktop_text='''CODE BY LAW — FIREFOX LINUX

Development install:
1. Extract this archive.
2. Open Firefox.
3. Go to about:debugging#/runtime/this-firefox
4. Choose Load Temporary Add-on.
5. Select manifest.json from the extracted folder.

For permanent normal installation, the extension must be signed by Mozilla/Add-ons.

Code by Law cycle:
Think Before You Speak -> Parser Goblin -> Reference Every Step ->
Cumulative Project Build + Checklist -> Bouncer -> Act -> Checker ->
Journal -> Checkpoint -> Re-reference.
'''
android_text='''CODE BY LAW — FIREFOX ANDROID

Firefox for Android supports extensions.
This package explicitly enables Gecko Android support.

For normal Android installation/distribution, the extension must be signed/published through Mozilla Add-ons Android support.

The phone must use a Code by Law companion URL reachable from the phone.
127.0.0.1 means the phone itself, not the Jetson or laptop.

Code by Law cycle:
Think Before You Speak -> Parser Goblin -> Reference Every Step ->
Cumulative Project Build + Checklist -> Bouncer -> Act -> Checker ->
Journal -> Checkpoint -> Re-reference.
'''
desktop=build_archive('code-by-law-firefox-linux.xpi',desktop_text)
android=build_archive('code-by-law-firefox-android.xpi',android_text)
shutil.copy2(desktop,DIST/'code-by-law-firefox-linux.zip')
shutil.copy2(android,DIST/'code-by-law-firefox-android.zip')
print(desktop)
print(android)
