#!/usr/bin/env bash
# Write or check MANIFEST.txt: "<sha256>  <bytes>  <path>" for every file in the repository,
# excluding .git (a directory, or the pointer file a secondary checkout carries), the manifest itself, editor droppings, Python caches, and the three run-time
# outputs the runbooks write (walk.json, apply-plan.json, restore.json; also in .gitignore).
# --check fails if a file on disk is missing from the manifest OR a manifest row has no file
# (both directions), or if any content hash changed.
# Usage: bash scripts/manifest.sh --write   |   bash scripts/manifest.sh --check
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MANIFEST="MANIFEST.txt"

list_files() {
  find . -type f \
    -not -path './.git/*' -not -name '.git' -not -path '*/__pycache__/*' \
    -not -name "$MANIFEST" -not -name '.DS_Store' -not -name '*.log' -not -name '*.pyc' \
    -not -name 'walk.json' -not -name 'apply-plan.json' -not -name 'restore.json' \
    | sed 's|^\./||' | LC_ALL=C sort
}
generate() {
  while IFS= read -r f; do
    printf '%s  %s  %s\n' "$(shasum -a 256 "$f" | cut -d' ' -f1)" "$(wc -c < "$f" | tr -d ' ')" "$f"
  done < <(list_files)
}

case "${1:-}" in
  --write)
    generate > "$MANIFEST"
    echo "wrote $MANIFEST ($(wc -l < "$MANIFEST" | tr -d ' ') files)"
    ;;
  --check)
    [ -f "$MANIFEST" ] || { echo "manifest: $MANIFEST is missing (run --write)"; exit 1; }
    tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT
    generate > "$tmp"
    if cmp -s "$MANIFEST" "$tmp"; then
      echo "manifest OK ($(wc -l < "$MANIFEST" | tr -d ' ') files)"
    else
      echo "manifest: out of date. '-' = in manifest but not on disk or changed; '+' = on disk but not in manifest or changed"
      diff "$MANIFEST" "$tmp" | grep -E '^[<>]' | sed 's/^</-/; s/^>/+/' || true
      exit 1
    fi
    ;;
  *)
    echo "usage: bash scripts/manifest.sh --write | --check"; exit 2
    ;;
esac
