#!/usr/bin/env node
// Runs `cap add android` only if mobile/android/ does not exist yet, so
// `npm run android:sync` works on a fresh clone and on an existing project.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const dir = path.resolve(__dirname, '..', 'android');
if (fs.existsSync(path.join(dir, 'gradlew'))) {
  console.log('mobile/android/ already exists -- skipping cap add');
} else {
  execSync('npx cap add android', { stdio: 'inherit', cwd: path.resolve(__dirname, '..') });
}
