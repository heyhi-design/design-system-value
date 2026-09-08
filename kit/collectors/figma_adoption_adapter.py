#!/usr/bin/env python3
"""Figma adoption adapter (reference skeleton).

STATUS: gated - awaiting access

Design-side adoption over time from the Figma Library Analytics REST API. This
is the adoption half of the Figma source (the structural half is a separate,
deferred step; see runbook.md). The API is Enterprise-plan only and the token
must carry the library_analytics:read scope.

HOW TO ACTIVATE (no structural rewrite required):
  1. Fill the CONFIG block below: set the library file keys, and confirm the
     endpoint base and env-var name.
  2. Put the token in the named environment variable. The token never lives in
     this file or any file in the kit. The operator supplies it at run time.
  3. Flip STATUS from "gated" to "active".
  4. Run:  python3 figma_adoption_adapter.py --live
     With no flag, the adapter runs its credential-free dry-run instead.

The operator runs this with their own token. The kit never handles the token.

Vendor surface confirmed against the Figma REST API developer docs on
2026-09-08. Re-confirm the plan tier, the scope, and the endpoint shapes against
the current vendor docs before promising an executive an automated series.
"""

import json
import os
import sys

# ===========================================================================
# CONFIG  (fill this in; then flip STATUS to "active")
# ===========================================================================

STATUS = "gated"  # "gated" (dry-run only) or "active" (attempt a live pull)

CONFIG = {
    # The environment variable that HOLDS THE TOKEN. This is a NAME, never a
    # token. The operator exports the token into this variable at run time.
    "token_env_var": "FIGMA_LIBRARY_ANALYTICS_TOKEN",

    # The REST base. Standard Figma is api.figma.com; Figma for Government is
    # api.figma-gov.com.
    "endpoint_base": "https://api.figma.com",

    # The library file keys to pull, one per published library. A file key is
    # the id in a figma.com/design/<fileKey>/... URL of the library's source file.
    "library_file_keys": [
        # "FILE_KEY_OF_LIBRARY_SOURCE_FILE",
    ],

    # Optional ISO-8601 (YYYY-MM-DD) window. Empty means the API default window.
    "start_date": "",
    "end_date": "",

    # Auth style: "header" sends X-Figma-Token; "bearer" sends an OAuth bearer.
    "auth_style": "header",

    # The scope the token must carry. Recorded for the operator; not sent.
    "required_scope": "library_analytics:read",
    "required_plan": "Enterprise",
}

# The six endpoints, as path templates under endpoint_base. group_by is required.
ENDPOINTS = {
    "component_actions": "/v1/analytics/libraries/{library_file_key}/component/actions",
    "component_usages":  "/v1/analytics/libraries/{library_file_key}/component/usages",
    "style_actions":     "/v1/analytics/libraries/{library_file_key}/style/actions",
    "style_usages":      "/v1/analytics/libraries/{library_file_key}/style/usages",
    "variable_actions":  "/v1/analytics/libraries/{library_file_key}/variable/actions",
    "variable_usages":   "/v1/analytics/libraries/{library_file_key}/variable/usages",
}

# ===========================================================================
# Request shape  (documented; exercised only in --live once STATUS is active)
# ===========================================================================


def _auth_headers(token):
    if CONFIG["auth_style"] == "bearer":
        return {"Authorization": "Bearer " + token}
    return {"X-Figma-Token": token}


def _request(path, params, token):
    """One GET against the Library Analytics API, with cursor pagination.

    Left as the single network seam. Fill in with the operator's HTTP client of
    choice (urllib, requests, httpx). Returns the concatenated rows across pages.
    The 'actions' endpoints return week / insertions / detachments; the 'usages'
    endpoints return usages / files_using / teams_using. Both paginate with
    'cursor' and signal more pages with 'next_page'.
    """
    raise NotImplementedError(
        "Network call is intentionally left to the operator. "
        "GET {base}{path} params={params} headers={{auth}}".format(
            base=CONFIG["endpoint_base"], path=path, params=params
        )
    )


def collect():
    """Live path. Refuses to run while gated or while the token is absent."""
    if STATUS != "active":
        raise RuntimeError(
            "figma adoption adapter is gated. Fill CONFIG, set the token in "
            "$" + CONFIG["token_env_var"] + ", and flip STATUS to 'active'."
        )
    token = os.environ.get(CONFIG["token_env_var"])
    if not token:
        raise RuntimeError(
            "no token in $" + CONFIG["token_env_var"] + ". The operator must "
            "export it; the kit never stores it."
        )
    if not CONFIG["library_file_keys"]:
        raise RuntimeError("CONFIG['library_file_keys'] is empty; add at least one.")

    rows = []
    common = {"start_date": CONFIG["start_date"], "end_date": CONFIG["end_date"]}
    for key in CONFIG["library_file_keys"]:
        actions = _request(
            ENDPOINTS["component_actions"].format(library_file_key=key),
            dict(common, group_by="component"), token)
        rows += transform_actions(actions, key)
        usages = _request(
            ENDPOINTS["component_usages"].format(library_file_key=key),
            dict(common, group_by="component"), token)
        rows += transform_usages(usages, key)
        # style_* and variable_* follow the same two calls with kind swapped.
    return rows


# ===========================================================================
# Response -> 02-data-model transform  (documented and directly testable)
# ===========================================================================


def transform_actions(api_rows, library_file_key):
    """component/actions -> fact_component_usage_daily (source='design_tool').

    Figma reports weekly. The M2 design contract is weekly, so carry the
    week-start into the day column and keep the cadence weekly. insertions and
    detachments feed the M2 design-side ratio (detaches / inserts).
    """
    out = []
    for r in api_rows or []:
        out.append({
            "_table": "fact_component_usage_daily",
            "day": r.get("week"),
            "component_id": r.get("component_key"),
            "team_id": r.get("team_name"),        # resolve to a dim_team id on load
            "source": "design_tool",
            "inserts": r.get("insertions"),
            "detaches": r.get("detachments"),
            "metric_id": "M2",
        })
    return out


def transform_usages(api_rows, library_file_key):
    """component/usages -> fact_component_usage_daily(instances) and M3 inputs.

    usages is the instance count; files_using / teams_using are the design-side
    spread. Instances have no denominator, so this is uptake, not coverage.

    Reference skeleton: it emits the source fields. At load the operator resolves
    files_using / teams_using into their M3 targets (dropping them from the
    fact_component_usage_daily row), fills the NOT NULL keys day / team_id /
    metric_version, and produces the fact_migration_weekly row.
    """
    out = []
    for r in api_rows or []:
        out.append({
            "_table": "fact_component_usage_daily",
            "component_id": r.get("component_key"),
            "source": "design_tool",
            "instances": r.get("usages"),
            "files_using": r.get("files_using"),
            "teams_using": r.get("teams_using"),
            "metric_id": "M3",
        })
    return out


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

    print("== figma adoption adapter :: dry-run ==")
    print("STATUS:", STATUS)
    print("plan required:", CONFIG["required_plan"],
          "| scope required:", CONFIG["required_scope"])
    print("token env var (name only):", CONFIG["token_env_var"])
    print("endpoint base:", CONFIG["endpoint_base"])
    print("library file keys configured:", len(CONFIG["library_file_keys"]))
    print("")
    print("Would fill (design side):")
    for r in source_map.covered_by("figma-analytics"):
        print("  [{id}] {label}".format(id=r["id"], label=r["label"]))
        print("       -> {target}".format(target=r["target"]))
    print("")
    print("Partial metrics this adapter serves (design side only):")
    for m in source_map.METRICS:
        if m["source"] == "figma-analytics":
            print("  {id} {label}: design side covered; gap: {gap}".format(
                id=m["id"], label=m["label"], gap=m["gap_needs"]))
    print("")
    if STATUS != "active":
        print("Live pull is gated. No credentials were used or required.")
    return 0


if __name__ == "__main__":
    if "--live" in sys.argv:
        try:
            data = collect()
            print(json.dumps(data, indent=2))
        except Exception as exc:  # noqa: BLE001 - reference skeleton
            print("live pull not available: " + str(exc))
            sys.exit(1)
    else:
        sys.exit(dry_run())
