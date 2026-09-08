---
title: Figma adoption adapter
kit: design-system-value-kit
artifact: collectors/figma-adoption-adapter
date: 2026-09-08
classification: unclassified
status: gated - awaiting access
---

# Figma adoption adapter

**STATUS: gated - awaiting access.**

Design-side adoption over time from the Figma Library Analytics REST API. This
is the adoption half of the Figma source. The structural half (component,
variable, and style inventory) is a separate, deferred step; see `runbook.md`.

The reference script is `figma_adoption_adapter.py`. This page is its spec. The
script runs a credential-free dry-run today and a live pull once the operator
fills the config and flips the status. The operator runs it with their own
token; the kit never handles the token.

## Gate

The Library Analytics REST API is available on the **Enterprise plan only**, and
the token must carry the **`library_analytics:read`** scope (a Tier 3 endpoint).
Until the target design system has both, this adapter stays gated and the metrics
it would serve are marked `source-gap` on the map. This is an access gate the
operator must clear before any live pull.

## What it fills

Into artifact 02:

- `component/actions` gives weekly `insertions` and `detachments` per component
  or team. This is the design side of M2 (the detachment counter-metric) into
  `fact_component_usage_daily(source='design_tool', inserts, detaches)`.
- `component/usages` gives `usages` (instance count), `files_using`, and
  `teams_using`. This is the design side of M3 into `fact_migration_weekly` and
  `fact_component_usage_daily(instances)`.
- `style/*` and `variable/*` give style and token uptake into
  `fact_component_usage_daily` rows whose `dim_component.kind` is style or variable.

It does not give production render coverage (M1) or the code side of M2 and M3.
Those stay source-gaps. See `metric-source-map.md`.

## CONFIG block (fill this, then flip STATUS)

The authoritative copy lives at the top of `figma_adoption_adapter.py`. Fill the
ids; the token is read from the named environment variable at run time and never
stored in any file.

```
STATUS = "gated"   # -> "active" when access is granted

CONFIG = {
    "token_env_var":     "FIGMA_LIBRARY_ANALYTICS_TOKEN",  # NAME only, never a token
    "endpoint_base":     "https://api.figma.com",          # api.figma-gov.com for gov
    "library_file_keys": [ ... ],   # one per published library (from the file URL)
    "start_date":        "",        # optional ISO-8601 YYYY-MM-DD
    "end_date":          "",        # optional ISO-8601 YYYY-MM-DD
    "auth_style":        "header",  # "header" (X-Figma-Token) or "bearer" (OAuth)
    "required_scope":    "library_analytics:read",
    "required_plan":     "Enterprise",
}
```

The activation slots someone fills later are exactly three: the `library_file_keys`
list, the token in the named environment variable, and the `STATUS` flag. No
structural rewrite.

## Request shape

Six GET endpoints under `endpoint_base`, all requiring a `group_by` query
parameter and paginating with `cursor` / `next_page`:

```
GET /v1/analytics/libraries/{library_file_key}/component/actions?group_by=component|team&start_date=&end_date=&cursor=
GET /v1/analytics/libraries/{library_file_key}/component/usages?group_by=component|file
GET /v1/analytics/libraries/{library_file_key}/style/actions?group_by=style|team
GET /v1/analytics/libraries/{library_file_key}/style/usages?group_by=style|file
GET /v1/analytics/libraries/{library_file_key}/variable/actions?group_by=variable|team
GET /v1/analytics/libraries/{library_file_key}/variable/usages?group_by=variable|file
```

Auth header is `X-Figma-Token: <token>` (or `Authorization: Bearer <token>` for
OAuth). The single network seam in the script is `_request(path, params, token)`;
wire it to the operator's HTTP client of choice.

## Response to 02 transform

- Actions response fields `week`, `insertions`, `detachments`, `component_key`,
  `component_name`, `team_name` map to `fact_component_usage_daily`. Figma reports
  weekly and the M2 design contract is weekly, so the week-start goes into the
  `day` column and the cadence stays weekly.
- Usages response fields `usages`, `files_using`, `teams_using` map to the
  instance count and the design-side spread; tagged by migration, they feed
  `fact_migration_weekly`. Instances have no denominator, so this is uptake, not
  coverage.

The transform functions `transform_actions()` and `transform_usages()` in the
script return rows keyed to the target table columns and are directly testable.

## Dry-run branch

Running the script with no flag runs `dry_run()`, which needs no token and no
network. It prints the status, the required plan and scope, the token env-var
name (never a value), and the map slice this adapter would fill. Run:

Commands follow the three-line form in `../../SETUP.md` (interpreter, working directory, invocation); the working directory is this folder.

```
python3 figma_adoption_adapter.py            # credential-free dry-run
python3 figma_adoption_adapter.py --live     # gated: refuses until STATUS=active
```

While gated, `--live` refuses with a clear message and touches no credentials.

## Reality-check note for the technical playbook

The plan-tier and scope facts here were confirmed against the Figma REST API
developer docs on 2026-09-08 and match artifact 04's Layer 2 access-reality note.
If a future check finds the tier, scope, or endpoint shape has moved, hand the
correction to the maintainer of `04-instrumentation-playbook.md` rather than
editing that file from here.
