#!/usr/bin/env python3
"""Static check for the design-tool scripts in this folder (no design tool needed).

1. build-variables.js is current with respect to ../tokens/neutral.tokens.json.
2. Every .js file parses (wrapped in an async function, because the script runner
   supplies top-level await); skipped with a note if `node` is not installed.
3. Every variable name a script binds ('color/…', 'space/…', 'radius/…') exists in
   the token-derived name set, so a rename in the token file cannot leave a
   script binding a name that no longer exists.

Usage: python3 check-build-scripts.py   (exit 0 pass, 1 fail)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import json  # noqa: E402

from emit_variables import collect  # noqa: E402  (shim below)


def main():
    ok = True
    # 1. emitter freshness
    r = subprocess.run([sys.executable, os.path.join(HERE, "emit-variables-script.py"), "--check"], capture_output=True, text=True)
    print(r.stdout.strip())
    ok = ok and r.returncode == 0
    # token-derived names
    tokens = json.load(open(os.path.join(HERE, "..", "tokens", "neutral.tokens.json"), encoding="utf-8"))
    prims, sems = collect(tokens)
    names = set(p["name"] for p in prims) | set(s["name"] for s in sems)
    node = shutil.which("node")
    for fn in sorted(f for f in os.listdir(HERE) if f.endswith(".js")):
        src = open(os.path.join(HERE, fn), encoding="utf-8").read()
        # 2. parse
        if node:
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tmp:
                tmp.write("async function __wrapped__(figma) {\n" + src + "\n}\n")
                path = tmp.name
            r = subprocess.run([node, "--check", path], capture_output=True, text=True)
            os.unlink(path)
            if r.returncode != 0:
                ok = False
                print("parse FAIL %s: %s" % (fn, r.stderr.strip().splitlines()[-1] if r.stderr else ""))
            else:
                print("parse ok   %s" % fn)
        else:
            print("parse skip %s (node not installed)" % fn)
        # 3. bound names exist
        used = set(re.findall(r"'((?:color|space|radius)/[a-z0-9-]+)'", src))
        missing = sorted(used - names)
        if missing:
            ok = False
            print("names FAIL %s: not in the token set: %s" % (fn, ", ".join(missing)))
        else:
            print("names ok   %s (%d bound names)" % (fn, len(used)))
    print("RESULT:", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
