#!/usr/bin/env python3
"""Resolve a design system's data payload against the screen-data-binding
contract, with no design tool and no credentials.

This is the pure-Python half of the populate-from-data generator. It reads the
generic binding contract (screen-data-bindings.json) and a data payload for one
design system, and produces the display string for every text slot on the four
value-surface screens. The design-tool apply step (a separate use_figma script;
see populate-runbook.md) consumes the apply-plan this emits.

What it guarantees:
  coverage   Every slot in the census has a binding and every binding has a
             census slot. --check fails if the two disagree.
  honesty    A slot whose payload path is absent renders a visible placeholder
             and is reported as a run-time source-gap. It never invents a number.
  formatting It applies the declared format (percent, signed points) and passes
             operator-supplied display strings through unchanged.

Usage:
  python3 populate_screens.py                        resolve sample-data.json -> {screen: {slot: string}}
  python3 populate_screens.py --data sample-data-atlas.json
  python3 populate_screens.py --apply-plan           emit the join with the census (node ids + values) for the apply step
  python3 populate_screens.py --check                structural coverage check (exit 0 pass, 1 fail); gaps are reported, not failed
  python3 populate_screens.py --data <f> --out <f>   write the resolved map to a file

Credential-free and network-free, like dryrun.py.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BINDINGS = os.path.join(HERE, "screen-data-bindings.json")
CENSUS = os.path.join(HERE, "screen-census.json")
DEFAULT_DATA = os.path.join(HERE, "sample-data.json")
DEFAULT_PLACEHOLDER = "—"

TOKEN_RE = re.compile(r"\{([^}]+)\}")


class _Missing(object):
    """Sentinel for an absent payload path (distinct from a real None value,
    though both are treated as absent for gap detection)."""


MISSING = _Missing()


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Path resolution and formatting
# ---------------------------------------------------------------------------

def resolve_path(payload, path):
    """Walk a dotted path into the payload. Numeric segments index lists.
    Returns MISSING for any segment that does not resolve."""
    cur = payload
    for seg in path.split("."):
        if isinstance(cur, list):
            try:
                idx = int(seg)
            except ValueError:
                return MISSING
            if idx < 0 or idx >= len(cur):
                return MISSING
            cur = cur[idx]
        elif isinstance(cur, dict):
            if seg not in cur:
                return MISSING
            cur = cur[seg]
        else:
            return MISSING
    return cur


def fmt_value(val, fmt):
    """Apply a declared format. Unknown formats raise (a contract error, caught
    by --check)."""
    if fmt in (None, "", "str"):
        return str(val)
    if fmt == "pct1":
        return "{:.1f}%".format(float(val))
    if fmt == "pct0":
        return "{:d}%".format(int(round(float(val))))
    if fmt == "pts_signed":
        v = float(val)
        sign = "+" if v >= 0 else "−"  # U+2212 MINUS SIGN
        return "{}{:.1f} pts".format(sign, abs(v))
    raise ValueError("unknown format: " + repr(fmt))


def resolve_template(template, payload, placeholder):
    """Resolve one binding template. Returns (string, is_gap).

    A token {path|fmt} substitutes the formatted payload value. A trailing '?'
    on the path (e.g. {teams.0.cov_suffix?}) makes it optional: an absent value
    renders '' and does NOT flag a gap. Without '?', an absent value renders the
    placeholder and flags the slot a run-time source-gap. A template with no
    tokens (a static slot) returns unchanged."""
    state = {"gap": False}

    def repl(match):
        body = match.group(1)
        parts = body.split("|", 1)
        pathpart = parts[0]
        fmt = parts[1] if len(parts) > 1 else None
        optional = pathpart.endswith("?")
        path = pathpart[:-1] if optional else pathpart
        val = resolve_path(payload, path)
        # Absent (path missing), null, or an empty/whitespace-only string all
        # count as no-value: an optional token renders "", a required token
        # renders the placeholder and flags a run-time source-gap. Treating an
        # empty string as no-value keeps a required slot from silently blanking
        # when a payload supplies "" instead of omitting the key.
        empty_str = isinstance(val, str) and val.strip() == ""
        if val is MISSING or val is None or empty_str:
            if optional:
                return ""
            state["gap"] = True
            return placeholder
        return fmt_value(val, fmt)

    return TOKEN_RE.sub(repl, template), state["gap"]


# ---------------------------------------------------------------------------
# Resolution over the whole contract
# ---------------------------------------------------------------------------

def resolve_all(bindings, payload, placeholder):
    """Resolve every binding. Returns (by_screen, gaps, resolved_map).

    by_screen: {screen: {slot: string}}
    gaps:      [ {slot, screen, source} ] for slots that rendered a placeholder
    resolved_map: {slot: string} flat, for the apply-plan join
    """
    by_screen = {}
    gaps = []
    flat = {}
    for b in bindings["bindings"]:
        slot = b["slot"]
        screen = b["screen"]
        text, is_gap = resolve_template(b["template"], payload, placeholder)
        by_screen.setdefault(screen, {})[slot] = text
        flat[slot] = text
        if is_gap:
            gaps.append({"slot": slot, "screen": screen, "source": b.get("source")})
    return by_screen, gaps, flat


def census_slot_index(census):
    """Map every census slot id -> its apply descriptor:
      {'type':'text','node':id} | {'type':'tile'|'chip','instance':id,'role':r}
    Covers slots, tile_slots, and chip_slots across all screens."""
    index = {}
    for screen in census["screens"].values():
        for slot, meta in screen.get("slots", {}).items():
            index[slot] = {"type": "text", "node": meta["node"]}
        for slot, meta in screen.get("tile_slots", {}).items():
            index[slot] = {"type": "tile", "instance": meta["instance"], "role": meta["role"]}
        for slot, meta in screen.get("chip_slots", {}).items():
            index[slot] = {"type": "chip", "instance": meta["instance"], "role": meta["role"]}
    return index


def apply_plan(bindings, census, payload, placeholder):
    """Join resolved values with census node ids into an ordered op list the
    apply step consumes. The target file key is supplied at apply time, not
    stored here."""
    _, gaps, flat = resolve_all(bindings, payload, placeholder)
    index = census_slot_index(census)
    ops = []
    for b in bindings["bindings"]:
        slot = b["slot"]
        desc = index[slot]  # KeyError here is a census/binding mismatch; --check catches it first
        op = {"slot": slot, "value": flat[slot]}
        op.update(desc)
        ops.append(op)
    return {"target_file_key": None, "ops": ops,
            "source_gaps": [g["slot"] for g in gaps]}


# ---------------------------------------------------------------------------
# Coverage check
# ---------------------------------------------------------------------------

def check(bindings, census, payload, placeholder):
    """Structural coverage: census slots and binding slots are the same set,
    and every template resolves without a contract error. Gaps are reported,
    not failed. Returns True/False."""
    ok = True
    problems = []

    binding_slots = set(b["slot"] for b in bindings["bindings"])
    census_slots = set(census_slot_index(census).keys())

    missing_binding = sorted(census_slots - binding_slots)
    missing_census = sorted(binding_slots - census_slots)
    if missing_binding:
        ok = False
        problems.append("census slots with no binding: " + ", ".join(missing_binding))
    if missing_census:
        ok = False
        problems.append("bindings with no census slot: " + ", ".join(missing_census))

    dup = len(binding_slots) != len(bindings["bindings"])
    if dup:
        ok = False
        problems.append("duplicate slot ids in bindings")

    # Resolve everything once to surface any template/format error.
    gaps = []
    try:
        _, gaps, _ = resolve_all(bindings, payload, placeholder)
    except Exception as exc:  # noqa: BLE001 - report as a coverage failure
        ok = False
        problems.append("resolution raised: " + str(exc))

    print("== coverage check ==")
    print("  bindings:            {n}".format(n=len(bindings["bindings"])))
    print("  census slots:        {n}".format(n=len(census_slots)))
    print("  slots resolved:      {n}".format(n=len(binding_slots) if ok else 0))
    print("  run-time source-gaps (this payload): {n}".format(n=len(gaps)))
    for g in gaps:
        print("     - {slot} (source {src})".format(slot=g["slot"], src=g["source"]))
    if ok:
        print("  RESULT: COVERAGE OK (every slot bound; no contract error)")
    else:
        print("  RESULT: COVERAGE FAILED")
        for p in problems:
            print("   - " + p)
    return ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv):
    ap = argparse.ArgumentParser(description="Resolve a data payload against the screen bindings.")
    ap.add_argument("--data", default=DEFAULT_DATA, help="payload JSON (default sample-data.json)")
    ap.add_argument("--bindings", default=BINDINGS, help="binding contract JSON")
    ap.add_argument("--census", default=CENSUS, help="per-file census JSON")
    ap.add_argument("--placeholder", default=DEFAULT_PLACEHOLDER, help="gap placeholder (default '—')")
    ap.add_argument("--apply-plan", action="store_true", help="emit node-id apply ops for the design-tool step")
    ap.add_argument("--check", action="store_true", help="structural coverage check (exit 0/1)")
    ap.add_argument("--out", default=None, help="write output JSON to a file instead of stdout")
    args = ap.parse_args(argv)

    bindings = load_json(args.bindings)
    census = load_json(args.census)
    payload = load_json(args.data)

    if args.check:
        return 0 if check(bindings, census, payload, args.placeholder) else 1

    if args.apply_plan:
        out = apply_plan(bindings, census, payload, args.placeholder)
    else:
        by_screen, gaps, _ = resolve_all(bindings, payload, args.placeholder)
        out = {
            "design_system": payload.get("design_system", {}).get("name"),
            "screens": by_screen,
            "source_gaps": [g["slot"] for g in gaps],
        }

    text = json.dumps(out, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("wrote " + args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
