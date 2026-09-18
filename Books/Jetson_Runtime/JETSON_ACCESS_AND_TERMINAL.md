# Jetson Access and Terminal Entry Point

**Purpose:** give human and AI contributors one safe, reproducible starting point for working on the Jetson without guessing credentials, IP addresses, paths, or storage targets.

## Rules

- Do not guess a Jetson IP address.
- Do not guess a username.
- Do not format or repartition attached storage just to start development.
- Do not treat an external drive as disposable unless it has been explicitly verified disposable.
- Prefer reversible user-space directories/containers before filesystem/kernel work.
- Record the exact machine, branch, command, and result in the relevant construction log/receipt.

## On the Jetson itself

Open a terminal and identify the current user and network addresses:

```bash
whoami
hostname
hostname -I
ip addr
```

Use the actual username returned by `whoami` and an address belonging to the intended LAN interface.

To verify SSH service state:

```bash
systemctl status ssh --no-pager
```

If OpenSSH server is installed but not running, a human/operator with appropriate permissions may enable/start it according to the system's Ubuntu configuration. Do not change security settings merely to make automation convenient.

## From another machine on the same trusted LAN

Use the verified username and verified Jetson LAN address:

```bash
ssh <verified-user>@<verified-jetson-ip>
```

Example shape only:

```text
ssh user@192.168.x.x
```

The example is not a credential or known address. Replace both fields from the Jetson's own output.

After connecting, verify you reached the intended machine:

```bash
whoami
hostname
uname -a
pwd
```

## Repository entry

Do not assume the checkout path. Locate the repository safely:

```bash
find "$HOME" -maxdepth 4 -type d -name One-Wave-Science 2>/dev/null
```

Then enter the verified path and inspect before editing:

```bash
cd <verified-path>/One-Wave-Science
git status
git branch --show-current
git log -1 --oneline
```

For shared AI work, create/use an isolated branch rather than editing another contributor's active branch.

## External-drive discovery

Before using an attached external drive, identify devices and mounts without changing them:

```bash
lsblk -o NAME,SIZE,FSTYPE,LABEL,UUID,MOUNTPOINTS,MODEL
findmnt
```

If the intended drive is already mounted, use its verified mount point. If it contains user data or its purpose is uncertain, stop there and do not modify it.

For Miniverse/Mega City prototyping, prefer creating a normal project directory on a verified writable mounted drive, for example:

```bash
mkdir -p <verified-mount>/one-wave-miniverse
```

Do not substitute a guessed mount path.

## First Miniverse storage rule

The first one-room looper prototype must work using ordinary reversible storage:

- directory tree;
- SQLite/database file;
- JSON/state bundle;
- disk-image/container file;
- another user-space format with integrity checks.

The experimental lattice/storage architecture is a later track. It must prove read/write integrity, migration, backup, and recovery before any destructive formatting path is considered.

## Terminal bridge / AI access direction

A terminal bridge for AI collaborators should expose bounded, auditable operations rather than unrestricted silent control. Minimum requirements:

- identify the acting AI/worker;
- record command, working directory, timestamp, exit status, and relevant output;
- show which repository branch is active;
- require explicit handling for destructive commands;
- separate read/inspect capability from write/mutate capability where practical;
- preserve a human-visible emergency stop/reset path.

The bridge should support the project honor system, not bypass it.

## Related work

Read alongside:

- `README.md`
- `AI_CANONICAL_START_HERE.md`
- `AI_FOREMAN_WORK_REGISTER.md`
- `MEGA_CITY_LOOPER_OBJECTIVE.md`
- `Virtual_Breadboard/AI_COLLABORATION.md`
- `Virtual_Breadboard/AI_CONSTRUCTION_LOG.md`

Any contributor who discovers a more reliable Jetson access/runtime path should update this file with the tested commands and sign the corresponding construction entry.