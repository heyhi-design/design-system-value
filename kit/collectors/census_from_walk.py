#!/usr/bin/env python3
"""Build screen-census.json for a target file from a census-walk.js result.

The walk lists, per screen, every text node and component instance in document
order. The binding contract lists slots per screen in the same order. This
script joins the two: a text item consumes one slot; a Stat tile instance
consumes three (label, value, sub); a Delta chip instance consumes one (value).
Every slot records the string the file currently shows as `text`, so a census
taken on a fresh template copy doubles as the restore point.

Usage:
  python3 census_from_walk.py walk.json --out screen-census.json
  python3 census_from_walk.py walk.json            # print to stdout

Exits 1 if any screen's item sequence does not match the contract exactly
(too few or too many text nodes, an instance exposing the wrong number of
text nodes, a screen missing from the walk), which means the file's structure
has drifted from the template and must be reconciled before populating.
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BINDINGS = os.path.join(HERE, "screen-data-bindings.json")
ROLES = {"Stat tile": ("label", "value", "sub"), "Delta chip": ("value",)}
GROUP = {"Stat tile": "tile_slots", "Delta chip": "chip_slots"}
COMPONENT_KEY = {"Stat tile": "stat_tile", "Delta chip": "delta_chip"}


def main(argv):
    ap = argparse.ArgumentParser(description="Join a census walk with the binding contract.")
    ap.add_argument("walk", help="JSON returned by figma/census-walk.js")
    ap.add_argument("--bindings", default=BINDINGS)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    for label, path in (("walk", args.walk), ("bindings", args.bindings)):
        if not path or not os.path.isfile(path):
            print("error: %s file not found: %r" % (label, path), file=sys.stderr)
            return 1
    walk = json.load(open(args.walk, encoding="utf-8"))
    bindings = json.load(open(args.bindings, encoding="utf-8"))

    census = {
        "note": "Per-target census of the four reference-template screens (exec one-pager, team view, event ledger, leading feed). "
                "For every slot in screen-data-bindings.json it records the text-node id in a specific target file, plus the component "
                "internals the scorecard tiles and the delta chip expose. Node ids are file-specific: regenerate this file for a new "
                "target by running figma/census-walk.js in the design tool and joining its result with collectors/census_from_walk.py "
                "(see populate-runbook.md). The target file key is supplied at apply time as config, never stored here. Every slot also "
                "records `text`, the string the file showed when the census was taken, so `populate_screens.py --restore-template` can "
                "return the file to that state; on a fresh template copy those are the template's own example strings.",
        "generated": datetime.date.today().isoformat(),
        "schema": {
            "slots": "slot id -> { node: '<id>', text: '<string at census time>' }",
            "tile_slots": "slot id -> { instance: '<instance id>', role: 'label|value|sub', text: '<string at census time>' } (the tile is a component instance; the apply resolves its TEXT descendants in document order [label, value, sub])",
            "chip_slots": "slot id -> { instance: '<instance id>', role: 'value', text: '<string at census time>' } (single TEXT descendant)",
        },
        "components": {},
        "screens": {},
    }
    for name, meta in walk.get("components", {}).items():
        census["components"][COMPONENT_KEY[name]] = {
            "component": meta["id"], "text_nodes_in_order": list(ROLES[name]),
            "text_node_ids_on_component": meta["text_node_ids"],
            "note": ("A Stat tile instance exposes three TEXT descendants in document order: label, value, sub. A sparkline vector sits between value and sub and is not text."
                     if name == "Stat tile" else "A Delta chip instance exposes one TEXT descendant."),
        }

    errors = []
    contract_screens = []
    for b in bindings["bindings"]:
        if b["screen"] not in contract_screens:
            contract_screens.append(b["screen"])
    for extra in sorted(set(walk.get("screens", {})) - set(contract_screens)):
        errors.append("%s: screen in the walk but not in the contract" % extra)
    for screen_key in contract_screens:
        screen = walk.get("screens", {}).get(screen_key)
        slots = [b for b in bindings["bindings"] if b["screen"] == screen_key]
        if screen is None:
            errors.append("%s: frame not found in the walk" % screen_key)
            continue
        entry = {"frame": screen["frame"], "name": screen["name"], "slots": {}, "tile_slots": {}, "chip_slots": {}}
        n_text = sum(1 for it in screen["items"] if it["kind"] == "text") + sum(
            len(it.get("texts", [])) for it in screen["items"] if it["kind"] != "text")
        if n_text > len(slots):
            errors.append("%s: the walk has %d text positions for %d slots; an extra text node or instance is present somewhere in the frame" % (screen_key, n_text, len(slots)))
        i = 0
        for item in screen["items"]:
            if item["kind"] == "text":
                if i >= len(slots):
                    break
                entry["slots"][slots[i]["slot"]] = {"node": item["id"], "text": item["text"]}
                i += 1
            else:
                comp = item["component"]
                if comp not in ROLES:
                    errors.append("%s: unknown instance %s (%s); expected a Stat tile or Delta chip (a renamed instance is reported by its main component's name)" % (screen_key, item["id"], comp))
                    break
                if len(item["texts"]) != len(ROLES[comp]):
                    errors.append("%s: instance %s (%s) exposes %d text nodes, expected %d (%s)" % (screen_key, item["id"], comp, len(item["texts"]), len(ROLES[comp]), ", ".join(ROLES[comp])))
                    break
                for role, txt in zip(ROLES[comp], item["texts"]):
                    if i >= len(slots):
                        errors.append("%s: instance %s overflows the slot list" % (screen_key, item["id"]))
                        break
                    entry[GROUP[comp]][slots[i]["slot"]] = {"instance": item["id"], "role": role, "text": txt}
                    i += 1
        if i != len(slots) and not any(e.startswith(screen_key + ":") for e in errors):
            errors.append("%s: %d of %d slots filled (structure drift)" % (screen_key, i, len(slots)))
        for g in ("tile_slots", "chip_slots"):
            if not entry[g]:
                del entry[g]
        census["screens"][screen_key] = entry

    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        return 1
    text = json.dumps(census, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text)
        print("wrote %s (%d screens)" % (args.out, len(census["screens"])))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
