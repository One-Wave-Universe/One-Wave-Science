from pathlib import Path
p=Path('Virtual_Breadboard/package.json')
s=p.read_text()
a='    "test:adaptive-transient": "node test/adaptive-transient.test.js",\n'
b=a+'    "test:integration-methods": "node test/integration-methods.test.js",\n'
if a not in s: raise SystemExit('package anchor missing')
p.write_text(s.replace(a,b,1))

p=Path('.github/workflows/breadboard-flashlight-tests.yml')
s=p.read_text()
# add path in push and pull_request sections
needle="      - 'Virtual_Breadboard/test/adaptive-transient.test.js'\n"
if s.count(needle)<2: raise SystemExit('workflow path anchors missing')
s=s.replace(needle, needle+"      - 'Virtual_Breadboard/test/integration-methods.test.js'\n", 2)
step='''      - name: Run adaptive transient qualification\n        run: npm run test:adaptive-transient\n'''
if step not in s: raise SystemExit('workflow step anchor missing')
s=s.replace(step, step+'''\n      - name: Run trapezoidal and Gear2 integration qualification\n        run: npm run test:integration-methods\n''',1)
p.write_text(s)
