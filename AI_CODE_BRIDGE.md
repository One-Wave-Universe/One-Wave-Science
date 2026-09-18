# AI Direct Python + C++ Bridge

This bridge lets any authorized MCP-capable AI execute bounded Python and C++
source directly on the Jetson through the existing authenticated Hive Pipe
gateway. A human does not need to copy commands between the AI and terminal.

## Tools

Hive Pipe exposes:

```text
python_run(code, args?, cwd?, timeout?)
cpp_compile_run(code, args?, cwd?, timeout?, standard?)
```

The existing tools remain available:

```text
terminal_pwd
terminal_which
terminal_run
```

## Python

Example MCP call:

```json
{
  "name": "python_run",
  "arguments": {
    "code": "print(sum(i*i for i in range(6)))",
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

The gateway writes the source to a temporary script inside the authorized work
root, runs it with `python3`, captures stdout/stderr/exit status, and removes
the temporary source automatically.

Arguments can be passed without shell parsing:

```json
{
  "name": "python_run",
  "arguments": {
    "code": "import sys; print(sys.argv[1])",
    "args": ["hello"]
  }
}
```

## C++

Example MCP call:

```json
{
  "name": "cpp_compile_run",
  "arguments": {
    "code": "#include <iostream>\nint main(){std::cout << 42 << \"\\n\";}",
    "standard": "c++20",
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 60
  }
}
```

The gateway creates temporary source, compiles it with:

```text
g++ -std=c++20 -O2 -Wall -Wextra -pedantic
```

then runs the temporary binary and removes both source and binary. Supported
standards are `c++17`, `c++20`, and `c++23`.

Compile failures return `phase=compile` plus compiler stdout/stderr. Successful
builds return `phase=run` plus runtime stdout/stderr and the compile receipt.

## Security and scope

These tools do not create a new daemon or privileged shell. They use the same
Hive Pipe authentication, normal non-root user, authorized work roots, timeout
limits, output clipping, systemd `NoNewPrivileges`, and `ProtectSystem=strict`
boundary already used by `terminal_run`.

Direct source is limited to 12 KiB per call. Credential/private-key path markers
are rejected. Temporary source and binaries are removed after each request.

For persistent project work, the AI should still edit normal repo files on a
task branch, run tests, inspect the diff, and open a PR. These direct tools are
for calculations, prototypes, verification, data analysis, compiler checks, and
small experiments without requiring a human terminal relay.

## Verify

After installing/restarting the updated gateway, ask the MCP client to list
tools. It should include:

```text
python_run
cpp_compile_run
```

Python smoke test:

```python
print(6 * 7)
```

Expected stdout:

```text
42
```

C++ smoke test:

```cpp
#include <iostream>
int main() {
    std::cout << 6 * 7 << "\n";
}
```

Expected stdout:

```text
42
```

## Install after merge

From the canonical Jetson checkout:

```bash
cd /home/Scales/One-Wave-Science
git pull --ff-only origin main
bash hive-pipe/install_gateway.sh
systemctl --user is-active hive-pipe-agent.service hive-pipe-gateway.service
```

Then reconnect or refresh the AI client's MCP tool list if the client caches it.

See also:

```text
AI_JETSON_TOOL_GUIDE.md
JETSON_AI_ACCESS.md
hive-pipe/README.md
```