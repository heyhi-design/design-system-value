#!/usr/bin/env bash
# One-command check for this repository. Runs every credential-free check and stops at the first failure.
# Usage: bash scripts/smoke.sh            (from any working directory)
#        PY=/path/to/python3 bash scripts/smoke.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-python3}"
fail() { echo "SMOKE FAIL: $1" >&2; exit 1; }
step() { echo "== $1"; }

step "interpreter"
"$PY" -c 'import sys; assert sys.version_info >= (3, 9), sys.version; print("python", sys.version.split()[0])' \
  || fail "Python 3.9 or later is required (set PY=/path/to/python3)"

step "collectors: dry-run coverage (every metric and ledger row classified)"
(cd "$ROOT/kit/collectors" && "$PY" dryrun.py --check > /dev/null) || fail "kit/collectors/dryrun.py --check"

step "collectors: adapters refuse cleanly while gated"
(cd "$ROOT/kit/collectors" && "$PY" dryrun.py --adapters > /dev/null) || fail "kit/collectors/dryrun.py --adapters"

step "populate: contract coverage (every slot bound, no orphan binding)"
(cd "$ROOT/kit/collectors" && "$PY" populate_screens.py --check > /dev/null) || fail "kit/collectors/populate_screens.py --check"

step "populate: both sample payloads resolve"
for f in sample-data.json sample-data-atlas.json; do
  (cd "$ROOT/kit/collectors" && "$PY" populate_screens.py --data "$f" > /dev/null) || fail "populate_screens.py --data $f"
done

step "tokens: contrast gate"
(cd "$ROOT/kit/tokens" && "$PY" check-contrast.py > /dev/null) || fail "kit/tokens/check-contrast.py"

step "json: every .json parses"
while IFS= read -r f; do
  "$PY" -c 'import json, sys; json.load(open(sys.argv[1]))' "$f" || fail "invalid JSON: ${f#$ROOT/}"
done < <(find "$ROOT" -type f -name '*.json' -not -path '*/.git/*')

step "links: every relative Markdown link and asset path resolves"
"$PY" "$ROOT/scripts/check-links.py" "$ROOT" || fail "broken relative link (see above)"

step "manifest: MANIFEST.txt matches the tree in both directions"
bash "$ROOT/scripts/manifest.sh" --check || fail "MANIFEST.txt out of date (run: bash scripts/manifest.sh --write)"

step "genericity: no internal references"
bash "$ROOT/scripts/check-no-internal-refs.sh" > /dev/null || fail "internal references found (run scripts/check-no-internal-refs.sh to list them)"

echo "SMOKE OK"
