#!/usr/bin/env bash
# Fails if any file in this repository contains a reference that must not appear in the generic release.
set -euo pipefail
cd "$(dirname "$0")/.."
PATTERN='heyhi|hey hi|bay design|cody clark|sheerline|cigna|myassetmap|internal use only|confidential|/Volumes/|\.claude/|worktree|mempalace|corrections-registry|vk-[0-9]|plan-[a-z-]+-20'
hits=$(grep -rniE --exclude-dir=.git --exclude=check-no-internal-refs.sh --binary-files=without-match "$PATTERN" . || true)
if [ -n "$hits" ]; then
  echo "Internal references found:"; echo "$hits"; exit 1
fi
# Binary assets: check embedded text in SVGs and image metadata by string scan.
bin_hits=$(grep -rlaiE --include='*.jpg' --include='*.png' --include='*.svg' "$PATTERN" . || true)
if [ -n "$bin_hits" ]; then
  echo "Internal references found in binary assets:"; echo "$bin_hits"; exit 1
fi
echo "clean: no internal references"
