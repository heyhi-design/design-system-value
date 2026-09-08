#!/usr/bin/env python3
"""Supernova adapter (reference skeleton).

STATUS: gated - awaiting access

Design-system structure and documentation coverage from the design-system
documentation platform's read API. The vendor's first-party programmatic
surface is a JavaScript/TypeScript SDK (package @supernovaio/sdk) plus a CLI;
authentication is a personal access token generated from the account's profile
settings. A read returns the version's tokens, assets, components, and
documentation structure and content.

Honest limit, recorded on the map: the documented read surface returns
structure and content, not an adoption-over-time or health time series. Where
the operator wants documentation traffic or a health trend, that is a
product-UI feature with no documented public read API and stays a source-gap
even within this source.

HOW TO ACTIVATE (no structural rewrite required):
  1. Fill the CONFIG block below: workspace, design-system, and version ids;
     confirm the env-var name and the api base.
  2. Put the personal access token in the named environment variable. The token
     never lives in this file or any file in the kit.
  3. Flip STATUS from "gated" to "active".
  4. Run:  python3 supernova_adapter.py --live
     With no flag, the adapter runs its credential-free dry-run instead.

The operator runs this with their own token. The kit never handles the token.

Vendor surface confirmed against the Supernova developer docs on 2026-09-08
(SDK read of tokens, assets, components, and documentation; personal-access-token
auth). Re-confirm the SDK method names and any data-API base against the current
vendor docs before relying on them.
"""

import json
import os
import sys

# ===========================================================================
# CONFIG  (fill this in; then flip STATUS to "active")
# ===========================================================================

STATUS = "gated"  # "gated" (dry-run only) or "active" (attempt a live read)

CONFIG = {
    # The environment variable that HOLDS THE TOKEN. A NAME, never a token.
    "token_env_var": "SUPERNOVA_API_TOKEN",

    # The data-API base the SDK targets. Confirm against current vendor docs.
    "api_base": "https://api.supernova.io",

    # Which design system and version to read. Ids come from the account.
    "workspace_id": "",
    "design_system_id": "",
    "version_id": "",   # empty means the latest version

    # Recorded for the operator; not sent as a header value.
    "auth_style": "personal-access-token",
}

# The read surface, named at SDK-method level (the SDK wraps the transport).
READS = {
    "components": "version.components()  -> design components in the version",
    "tokens":     "version.tokens()      -> design tokens in the version",
    "assets":     "version.assets()      -> assets in the version",
    "documentation": "version.documentation() -> documentation structure and content",
}

# ===========================================================================
# Read shape  (documented; exercised only in --live once STATUS is active)
# ===========================================================================


def _read(surface, token):
    """One read against the documentation-platform surface.

    Left as the single seam. The operator wires this to the vendor SDK (Node)
    or the data endpoint the SDK wraps, authenticating with the personal access
    token. Returns the list of records for the named surface.
    """
    raise NotImplementedError(
        "Read call is intentionally left to the operator. "
        "Authenticate with $" + CONFIG["token_env_var"] + " and read '"
        + surface + "' from the configured version."
    )


def collect():
    """Live path. Refuses to run while gated or while the token is absent."""
    if STATUS != "active":
        raise RuntimeError(
            "supernova adapter is gated. Fill CONFIG, set the token in "
            "$" + CONFIG["token_env_var"] + ", and flip STATUS to 'active'."
        )
    token = os.environ.get(CONFIG["token_env_var"])
    if not token:
        raise RuntimeError(
            "no token in $" + CONFIG["token_env_var"] + ". The operator must "
            "export it; the kit never stores it."
        )
    if not (CONFIG["workspace_id"] and CONFIG["design_system_id"]):
        raise RuntimeError("CONFIG needs workspace_id and design_system_id.")

    rows = []
    rows += transform_inventory(_read("components", token), kind="component")
    rows += transform_inventory(_read("tokens", token), kind="token")
    rows += transform_inventory(_read("assets", token), kind="asset")
    rows += transform_doc_coverage(_read("documentation", token))
    return rows


# ===========================================================================
# Response -> 02-data-model transform  (documented and directly testable)
# ===========================================================================


def transform_inventory(api_rows, kind):
    """components / tokens / assets -> dim_component rows.

    A documentation-platform-side mirror of the structure inventory, useful
    where the documentation platform, not the design tool, is the system of
    record. status and library map onto dim_component's own columns.
    """
    out = []
    for r in api_rows or []:
        out.append({
            "_table": "dim_component",
            "component_id": r.get("persistentId") or r.get("id"),
            "component_name": r.get("name"),
            "library": r.get("brandId") or r.get("origin") or "system",
            "kind": kind,
            "status": r.get("status") or "stable",
        })
    return out


def transform_doc_coverage(doc_records):
    """documentation -> a documented-vs-undocumented signal.

    The current data model (artifact 02) has no documentation-coverage table,
    so this is a candidate column rather than an existing row. Recorded on the
    map as a schema gap, not a filled slot.
    """
    documented = 0
    total = 0
    for r in doc_records or []:
        total += 1
        if r.get("hasContent"):
            documented += 1
    return [{
        "_table": "(schema gap: documentation coverage)",
        "documented": documented,
        "total": total,
    }]


# ===========================================================================
# Dry-run  (no credentials; emits the fill-map slice for this adapter)
# ===========================================================================


def dry_run():
    """Emit what this adapter would fill, with no token and no network."""
    try:
        import source_map
    except ImportError:
        here = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, here)
        import source_map

    print("== supernova adapter :: dry-run ==")
    print("STATUS:", STATUS)
    print("auth style:", CONFIG["auth_style"])
    print("token env var (name only):", CONFIG["token_env_var"])
    print("api base:", CONFIG["api_base"])
    print("workspace/design-system configured:",
          bool(CONFIG["workspace_id"] and CONFIG["design_system_id"]))
    print("")
    print("Would fill:")
    for r in source_map.covered_by("supernova"):
        note = " [partial]" if r.get("coverage") == "partial" else ""
        print("  [{id}] {label}{note}".format(id=r["id"], label=r["label"], note=note))
        print("       -> {target}".format(target=r["target"]))
        if r.get("gap_needs"):
            print("       gap: {gap}".format(gap=r["gap_needs"]))
    print("")
    if STATUS != "active":
        print("Live read is gated. No credentials were used or required.")
    return 0


if __name__ == "__main__":
    if "--live" in sys.argv:
        try:
            data = collect()
            print(json.dumps(data, indent=2))
        except Exception as exc:  # noqa: BLE001 - reference skeleton
            print("live read not available: " + str(exc))
            sys.exit(1)
    else:
        sys.exit(dry_run())
