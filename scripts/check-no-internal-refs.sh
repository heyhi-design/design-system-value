#!/usr/bin/env bash
# Fails if any file in this repository contains a reference that must not appear in the generic release.
set -euo pipefail
cd "$(dirname "$0")/.."
# Internal-reference alternatives shared by both scans below.
BASE='heyhi|hey hi|bay design|cody clark|sheerline|cigna|myassetmap|internal use only|confidential|/Volumes/|\.claude/|worktree|mempalace|corrections-registry|plan-[a-z-]+-20'
# Internal lane codes VK-0..9 / VK-A..Z (the arc used letter suffixes, e.g. vk-g).
# The text scan catches letters and digits. The binary-asset scan stays digit-only: a short
# code like "vk-g" collides with random image bytes (the release JPGs contain "Vk-O"/"Vk-Y"),
# so letter suffixes there would be false positives. Embedded text in SVGs is still covered
# by the text scan, which reads SVGs as text (grep runs with -i, so uppercase matches too).
PATTERN="$BASE|vk-[0-9a-z]"    # text/source scan
PATTERN_BIN="$BASE|vk-[0-9]"   # binary-asset (jpg/png/svg-byte) scan
# The LICENSE files name the copyright holder (a company name the BASE pattern otherwise
# blocks). A published, licensed repository must attribute its holder, so the license files
# are excluded from the text scan. They are standard MIT / CC BY boilerplate: no internal
# path, client, or classification string belongs there, which keeps the exclusion safe.
hits=$(grep -rniE --exclude-dir=.git --exclude=check-no-internal-refs.sh --exclude=LICENSE --exclude='LICENSE-*' --binary-files=without-match "$PATTERN" . || true)
if [ -n "$hits" ]; then
  echo "Internal references found:"; echo "$hits"; exit 1
fi
# Binary assets: check embedded text in SVGs and image metadata by string scan.
bin_hits=$(grep -rlaiE --include='*.jpg' --include='*.png' --include='*.svg' "$PATTERN_BIN" . || true)
if [ -n "$bin_hits" ]; then
  echo "Internal references found in binary assets:"; echo "$bin_hits"; exit 1
fi
echo "clean: no internal references"
