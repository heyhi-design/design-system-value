#!/usr/bin/env python3
"""Resolve every relative Markdown link and image path in the repository.

Usage: python3 scripts/check-links.py [repo-root]   (default: the repository this script lives in)
Exit 0 when every relative target exists; exit 1 and list the broken ones otherwise.
External links (http, https, mailto) and bare anchors (#section) are not checked.
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP = ("http://", "https://", "mailto:", "#", "skill://")


def main(root: str) -> int:
    base = Path(root).resolve()
    broken = []
    for md in sorted(base.rglob("*.md")):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in LINK.finditer(text):
            target = m.group(1)
            if target.startswith(SKIP):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            if not (md.parent / path).exists():
                broken.append(f"{md.relative_to(base)}: {target}")
    for b in broken:
        print("broken:", b)
    print(f"links checked in {sum(1 for _ in base.rglob('*.md'))} markdown files; broken: {len(broken)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])))
