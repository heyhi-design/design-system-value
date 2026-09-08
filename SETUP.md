<!-- classification: unclassified; generic release, no internal references permitted (see scripts/check-no-internal-refs.sh) -->
# Setup

How to get this repository running on any computer, and how to prove it works before you trust it. Nothing here needs a package install, a network connection, or a credential. The optional pieces (a database, a design tool, two vendor tokens) are listed so you can tell in advance which steps you can run.

## What you need

| Requirement | Needed for | Notes |
|---|---|---|
| git | cloning and syncing | Or unzip a release archive; the checks do not need git |
| Python 3.9 or later | every script in `kit/collectors/` and `kit/tokens/` | Standard library only; there is nothing to `pip install` |
| bash and grep | `scripts/` | Any POSIX shell with GNU or BSD grep; `shasum` for the manifest (`sha256sum` on Linux is not used) |
| PostgreSQL 17 (optional) | the artifact 02 data-model probe | The schema also reads as a portable sketch without a database |
| A design tool account with edit access to a copy of the template (optional) | the populate step in `kit/collectors/populate-runbook.md` | Plus an MCP client that exposes the tool's script runner with its own scripting skill loaded first |
| Vendor tokens (optional) | the two gated live adapters | Never written into any file here; read from an environment variable only in `--live` |

## Install

Clone the repository, or unzip a release archive, anywhere. There is no build step. Then run the smoke check:

```
bash scripts/smoke.sh
```

It runs every credential-free check in the kit (the collectors dry-run, the populate contract, the token contrast gate, JSON validity, relative-link resolution, the manifest, and the genericity scan) and prints `SMOKE OK`. It exits non-zero on the first failure and names the check that failed. Run it after every clone and after every edit.

## The three-line command form

Every prescribed command in this repository is written to be run in three parts, so a fresh machine with no shell history and no activated environment can run it as written:

```
PY=python3                    # 1. the interpreter (or an absolute path to a Python 3.9+ binary)
cd <repo-root>/kit/collectors # 2. the working directory the script expects (its own folder)
$PY dryrun.py --check         # 3. the full invocation
```

The scripts assume their own folder as the working directory because they import siblings (`dryrun.py` reads `source_map.py`; `populate_screens.py` reads the bindings and census beside it). `scripts/smoke.sh` handles the directories itself and honors `PY=/path/to/python3` if `python3` on your `PATH` is not the interpreter you want.

## Layout

| Path | What it is |
|---|---|
| `README.md` | Start here: what the repository is and the argument in five lines |
| `SETUP.md` | This file |
| `CHANGELOG.md` | Versions and what changed |
| `MANIFEST.txt` | Path, size, and SHA-256 of every file; `scripts/manifest.sh --check` verifies it both ways |
| `docs/` | The field guide and the visual survey; `docs/assets/README.md` states the contact sheets' terms |
| `kit/` | The nine artifacts, the plan skeleton, the sources, `tokens/`, `collectors/`, `wireframes/` |
| `scripts/smoke.sh` | The one-command check described above |
| `scripts/manifest.sh` | Writes or checks `MANIFEST.txt` |
| `scripts/check-links.py` | Resolves every relative Markdown link and asset path |
| `scripts/check-no-internal-refs.sh` | The genericity scan; binding on every change |

## After you change something

1. Run the checks that cover what you touched, then `bash scripts/smoke.sh`.
2. Regenerate the manifest: `bash scripts/manifest.sh --write`. The manifest is content-hashed, so any edit invalidates it until you rewrite it; a stale manifest is a smoke failure by design.
3. Add a line to `CHANGELOG.md` if the change is visible to a reader.

## If you are reading this in a mirror

The canonical source of this repository is its upstream monorepo. A mirror is derived from it one way and is overwritten on every sync. Do not open changes against the mirror; make them upstream and re-sync.

## Rights

This repository is private. All rights reserved by the maintainer; no license is granted for redistribution. The contact sheets under `docs/assets/` carry their own terms (see the README there).
