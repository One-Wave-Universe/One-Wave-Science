#!/usr/bin/env node
// Cross-platform Gradle wrapper call: gradlew on Linux/macOS, gradlew.bat on Windows.
const path = require('path');
const { execFileSync } = require('child_process');

const dir = path.resolve(__dirname, '..', 'android');
const win = process.platform === 'win32';
const gradlew = path.join(dir, win ? 'gradlew.bat' : 'gradlew');
execFileSync(gradlew, process.argv.slice(2), { stdio: 'inherit', cwd: dir, shell: win });
