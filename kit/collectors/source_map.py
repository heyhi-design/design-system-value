#!/usr/bin/env python3
"""Canonical machine-readable metric-to-source map for the value kit collectors.

This module is the single source of truth the dry-run driver (dryrun.py) and the
two source adapters read. The human-readable mirror is metric-source-map.md;
dryrun.py --check re-derives its coverage counts from this file. Keep
metric-source-map.md in sync with this file by hand.

Scope of the two named sources this kit ships adapters for:

  figma-analytics   Figma Library Analytics REST API (Enterprise plan, scope
                    library_analytics:read). Design-side usage over time:
                    component / style / variable actions and usages, weekly,
                    grouped by component, style, variable, team, or file.
  figma-structural  The Figma design read surface plus a read-only library
                    census / code crosswalk. Component, variable, and style
                    inventory and coverage. Runs after the library exists
                    (see runbook.md, the deferred structural half).
  supernova         The design-system documentation platform read API (SDK,
                    personal-access-token auth). Token, asset, and component
                    inventory and documentation coverage.
  source-gap        No figma or supernova read can supply this. It needs a
                    code-side scan, a production-runtime sampler, an issue
                    tracker, a survey, finance data, product analytics, or a
                    hand-kept ledger. The gap is a request for instrumentation,
                    not a defect in the kit.

Every classification carries a 'coverage' of full, partial, or none. 'partial'
means one of the named sources supplies part of the metric (typically the
design side) and the rest is a source-gap; both parts are named.

The map is deliberately honest that the two named sources reach the design side
only. Most of the executive value ledger is a source-gap for figma and
supernova, and the map says so on every row.
"""

# ---------------------------------------------------------------------------
# Source kinds
# ---------------------------------------------------------------------------

SOURCE_KINDS = ("figma-analytics", "figma-structural", "supernova", "source-gap")

# ---------------------------------------------------------------------------
# What the two named sources positively supply (design-side inputs).
# These feed the metric rows below; they are not themselves executive metrics.
# ---------------------------------------------------------------------------

STRUCTURAL_INPUTS = [
    {
        "id": "S1",
        "label": "Component / variable / style inventory and coverage",
        "source": "figma-structural",
        "coverage": "full",
        "call": "design read surface (variable and library reads) plus a "
                "read-only library census and code crosswalk",
        "transform": "one row per component, variable, and style into "
                     "dim_component (component_id, library, library_version, "
                     "kind, status); coverage counts feed the design side of M2 and M3",
        "target": "dim_component",
        "gap_needs": "",
        "note": "Deferred structural half. Runs after the design library is "
                "built (see runbook.md). No production render coverage from here.",
    },
    {
        "id": "S2",
        "label": "Design-side component insertions and detachments (weekly)",
        "source": "figma-analytics",
        "coverage": "full",
        "call": "GET /v1/analytics/libraries/:library_file_key/component/actions"
                "?group_by=component|team&start_date=&end_date=&cursor=",
        "transform": "week, insertions, detachments per component or team into "
                     "fact_component_usage_daily(source='design_tool', inserts, "
                     "detaches); carry the week-start into the day column and keep "
                     "the design cadence weekly per the M2 contract",
        "target": "fact_component_usage_daily",
        "gap_needs": "",
        "note": "Supplies the design-side half of M2 (detachments / insertions).",
    },
    {
        "id": "S3",
        "label": "Design-side instances and files/teams using a component",
        "source": "figma-analytics",
        "coverage": "full",
        "call": "GET /v1/analytics/libraries/:library_file_key/component/usages"
                "?group_by=component|file",
        "transform": "usages, files_using, teams_using per component into "
                     "fact_component_usage_daily(instances) and, tagged by "
                     "migration, the design side of fact_migration_weekly",
        "target": "fact_component_usage_daily, fact_migration_weekly",
        "gap_needs": "",
        "note": "Supplies the design-side half of M3. Instances have no "
                "denominator, so this is not coverage; it is uptake.",
    },
    {
        "id": "S4",
        "label": "Style and variable (token) actions and usages",
        "source": "figma-analytics",
        "coverage": "full",
        "call": "GET /v1/analytics/libraries/:library_file_key/style/actions, "
                "/style/usages, /variable/actions, /variable/usages (same params)",
        "transform": "style and variable uptake into fact_component_usage_daily "
                     "rows whose dim_component.kind is 'style' or 'variable'; "
                     "feeds design-side token adoption",
        "target": "fact_component_usage_daily",
        "gap_needs": "",
        "note": "Style and variable analytics are the newer half of the API; "
                "confirm availability against current vendor docs.",
    },
    {
        "id": "S5",
        "label": "Token, asset, and component inventory (documentation platform)",
        "source": "supernova",
        "coverage": "full",
        "call": "SDK read of the design-system version (tokens, assets, "
                "components); personal-access-token auth",
        "transform": "one row per token, asset, and component into dim_component "
                     "as a documentation-platform-side mirror of the inventory",
        "target": "dim_component",
        "gap_needs": "",
        "note": "A second read of structure, useful where the documentation "
                "platform, not the design tool, is the system of record.",
    },
    {
        "id": "S6",
        "label": "Documentation coverage (which components/tokens are documented)",
        "source": "supernova",
        "coverage": "partial",
        "call": "SDK read of documentation structure and content (block or markdown)",
        "transform": "map documented-vs-undocumented per component and token; the "
                     "current data model has no documentation-coverage table, so "
                     "this lands as a candidate column, not an existing row",
        "target": "(schema gap: no documentation-coverage table in 02 today)",
        "gap_needs": "documentation traffic and search-miss analytics are a "
                     "product-UI feature with no documented public read API; "
                     "that time series stays a source-gap even within supernova",
        "note": "Honest limit: the SDK reads structure and content, not an "
                "adoption-over-time or health series.",
    },
]

# ---------------------------------------------------------------------------
# The nine executive metrics (artifact 01). Each maps to a source or source-gap.
# ---------------------------------------------------------------------------

METRICS = [
    {
        "id": "M1",
        "label": "Coverage of what users see",
        "source": "source-gap",
        "coverage": "none",
        "call": "",
        "transform": "production sampler (pixel or DOM) or a code-side import "
                     "scan writes coverage_pct with a method key into "
                     "fact_coverage_daily; never mix methods in one series",
        "target": "fact_coverage_daily",
        "gap_needs": "production-runtime sampler (highest fidelity) or a "
                     "code-side import/bundle scan; figma usages are a design-side "
                     "proxy only, not production render coverage",
        "note": "The design-side proxy (S3) can stand in before a runtime "
                "sampler exists, labeled as a different method.",
    },
    {
        "id": "M2",
        "label": "Overrides, detachments, and arbitrary values",
        "source": "figma-analytics",
        "coverage": "partial",
        "call": "GET /v1/analytics/libraries/:library_file_key/component/actions "
                "(design side); code side is a source-gap",
        "transform": "design side: detachments / insertions into "
                     "fact_component_usage_daily(detaches, inserts). Code side: "
                     "lint violations / opportunities into fact_lint_daily and "
                     "style overrides into fact_component_usage_daily(overrides)",
        "target": "fact_component_usage_daily, fact_lint_daily",
        "gap_needs": "code-side CI: lint rules for hard-coded values where a "
                     "token exists, and a scan for style overrides on components",
        "note": "Design side is covered by figma-analytics; the code side is a "
                "source-gap that needs a nightly CI job.",
    },
    {
        "id": "M3",
        "label": "Migration progress",
        "source": "figma-analytics",
        "coverage": "partial",
        "call": "GET /v1/analytics/libraries/:library_file_key/component/usages "
                "(design side); code side is a source-gap",
        "transform": "design side: instances by library and migration into the "
                     "design side of fact_migration_weekly. Code side: a static "
                     "component scan writes ds_instances and legacy_instances",
        "target": "fact_migration_weekly",
        "gap_needs": "code-side static component scan of the codebase, tagged by "
                     "migration id, for the production-code side of the ratio",
        "note": "Design side is covered; the code-side count is a source-gap.",
    },
    {
        "id": "M4",
        "label": "Hours returned",
        "source": "source-gap",
        "coverage": "none",
        "call": "",
        "transform": "study, event, survey, and duplication inputs into "
                     "task_study, event_ledger, fact_survey_quarterly, and "
                     "duplication_ledger; the four methods are never summed",
        "target": "task_study, event_ledger, fact_survey_quarterly, duplication_ledger",
        "gap_needs": "a controlled task study (08), an event ledger kept by hand "
                     "(07), a quarterly survey, and a duplication ledger; none of "
                     "these come from figma or supernova",
        "note": "The strongest hours story (an instrumented event) is a manual "
                "ledger opened before the event, not an API pull.",
    },
    {
        "id": "M5",
        "label": "Defects and regressions, on vs off system",
        "source": "source-gap",
        "coverage": "none",
        "call": "",
        "transform": "labeled defects per release by surface class into "
                     "fact_defects_release; automated a11y pass-rate into "
                     "fact_a11y_pass_release (a pass rate, not a conformance claim)",
        "target": "fact_defects_release, fact_a11y_pass_release",
        "gap_needs": "issue-tracker labels (ui-inconsistency, a11y-regression), "
                     "a surface_class field, CI accessibility checks, and a "
                     "visual-regression tool",
        "note": "",
    },
    {
        "id": "M6",
        "label": "Engagement composite",
        "source": "source-gap",
        "coverage": "none",
        "call": "",
        "transform": "office-hours, contribution, and support counts normalized "
                     "by team size into fact_engagement_monthly",
        "target": "fact_engagement_monthly",
        "gap_needs": "calendar or attendance list, issue tracker, and support "
                     "channel exports; counted monthly and normalized by headcount",
        "note": "Contribution counts on the design-system repo are the nearest "
                "adjacent signal, but they are a tracker export, not a figma "
                "or supernova read.",
    },
    {
        "id": "M7",
        "label": "Sponsor and operating health",
        "source": "source-gap",
        "coverage": "none",
        "call": "",
        "transform": "release predictability, review SLA, and sponsor "
                     "attendance into fact_operating_monthly",
        "target": "fact_operating_monthly",
        "gap_needs": "release log, review queue, and meeting-attendance records",
        "note": "",
    },
    {
        "id": "M8",
        "label": "Consumer satisfaction",
        "source": "source-gap",
        "coverage": "none",
        "call": "",
        "transform": "four-question quarterly survey into fact_survey_quarterly; "
                     "consented open answers into fact_survey_verbatim",
        "target": "fact_survey_quarterly, fact_survey_verbatim",
        "gap_needs": "a quarterly survey instrument to every consumer; nothing "
                     "in figma or supernova produces the satisfaction signal",
        "note": "",
    },
    {
        "id": "M9",
        "label": "Cost to run and cost per consuming team",
        "source": "source-gap",
        "coverage": "none",
        "call": "",
        "transform": "loaded headcount, tooling, and maintenance reserve into "
                     "fact_cost_quarterly; the maintenance basis is a decision "
                     "made with finance",
        "target": "fact_cost_quarterly",
        "gap_needs": "finance headcount data, tooling invoices, and a maintenance "
                     "assumption; a spreadsheet a finance partner owns",
        "note": "Tool seat invoices (a figma or supernova bill) are a tooling "
                "line, but that is billing data, not the analytics read API.",
    },
]

# ---------------------------------------------------------------------------
# The value ledger rows (field guide Appendix A). Each maps to a source or gap.
# ---------------------------------------------------------------------------

LEDGER_ROWS = [
    # Ledger 1: Cost
    {"id": "C1", "ledger": "1 Cost", "label": "Team headcount x loaded cost",
     "source": "source-gap", "coverage": "none",
     "target": "fact_cost_quarterly.people_cost, loaded_rate",
     "gap_needs": "finance / HR headcount data", "metric": "M9"},
    {"id": "C2", "ledger": "1 Cost", "label": "Tooling and platform",
     "source": "source-gap", "coverage": "none",
     "target": "fact_cost_quarterly.tooling_cost",
     "gap_needs": "tooling invoices (finance)", "metric": "M9"},
    {"id": "C3", "ledger": "1 Cost", "label": "Maintenance and migrations (projected)",
     "source": "source-gap", "coverage": "none",
     "target": "fact_cost_quarterly.maintenance_reserve",
     "gap_needs": "a maintenance-reserve assumption agreed with finance", "metric": "M9"},
    {"id": "C4", "ledger": "1 Cost", "label": "Support ratio (system staff : consumers)",
     "source": "source-gap", "coverage": "none",
     "target": "fact_cost_quarterly.system_staff, consumers",
     "gap_needs": "headcount and consumer counts (finance / org)", "metric": "M9"},
    # Ledger 2: Hours
    {"id": "H1", "ledger": "2 Hours", "label": "Controlled task study result",
     "source": "source-gap", "coverage": "none",
     "target": "task_study",
     "gap_needs": "a controlled task study (artifact 08)", "metric": "M4"},
    {"id": "H2", "ledger": "2 Hours", "label": "Event-based measurement",
     "source": "source-gap", "coverage": "none",
     "target": "event_ledger",
     "gap_needs": "an event ledger opened before the event (artifact 07)", "metric": "M4"},
    {"id": "H3", "ledger": "2 Hours", "label": "Avoided duplication",
     "source": "source-gap", "coverage": "none",
     "target": "duplication_ledger",
     "gap_needs": "a duplication ledger (interface inventory plus estimates)", "metric": "M4"},
    {"id": "H4", "ledger": "2 Hours", "label": "Self-reported hours saved per consumer per week",
     "source": "source-gap", "coverage": "none",
     "target": "fact_survey_quarterly.hours_saved_median",
     "gap_needs": "the quarterly consumer survey (soft, never monetized as hard)", "metric": "M4"},
    # Ledger 3: Outcomes
    {"id": "O1", "ledger": "3 Outcomes", "label": "Coverage of what users see",
     "source": "source-gap", "coverage": "none",
     "target": "fact_coverage_daily",
     "gap_needs": "production-runtime sampler or code-side import scan; figma "
                  "usages are a design-side proxy only", "metric": "M1"},
    {"id": "O2", "ledger": "3 Outcomes", "label": "Counter-metric (detachments / overrides / arbitrary values)",
     "source": "figma-analytics", "coverage": "partial",
     "target": "fact_component_usage_daily.detaches, fact_lint_daily",
     "gap_needs": "code-side overrides and lint are a source-gap; design-side "
                  "detachments come from figma-analytics", "metric": "M2"},
    {"id": "O3", "ledger": "3 Outcomes", "label": "UI defects and a11y regressions per release",
     "source": "source-gap", "coverage": "none",
     "target": "fact_defects_release",
     "gap_needs": "issue-tracker labels and CI accessibility checks", "metric": "M5"},
    {"id": "O4", "ledger": "3 Outcomes", "label": "Outcome in a migrated flow vs a control flow",
     "source": "source-gap", "coverage": "none",
     "target": "(product analytics; not modeled as a fact table in 02)",
     "gap_needs": "product analytics with a difference-in-differences design", "metric": "n/a"},
    {"id": "O5", "ledger": "3 Outcomes", "label": "Consumer satisfaction",
     "source": "source-gap", "coverage": "none",
     "target": "fact_survey_quarterly",
     "gap_needs": "the quarterly consumer survey", "metric": "M8"},
    # Leading
    {"id": "L1", "ledger": "Leading", "label": "Engagement composite (3-mo rolling)",
     "source": "source-gap", "coverage": "none",
     "target": "fact_engagement_monthly",
     "gap_needs": "calendar, tracker, and support exports", "metric": "M6"},
    {"id": "L2", "ledger": "Leading", "label": "Sponsor attendance at planning and reviews",
     "source": "source-gap", "coverage": "none",
     "target": "fact_operating_monthly.sponsor_attended",
     "gap_needs": "meeting-attendance records", "metric": "M7"},
    {"id": "L3", "ledger": "Leading", "label": "Contribution review SLA; release predictability",
     "source": "source-gap", "coverage": "none",
     "target": "fact_operating_monthly.reviews_within_sla, releases_on_time",
     "gap_needs": "review queue and release log", "metric": "M7"},
    # Risk
    {"id": "R1", "ledger": "Risk", "label": "Accessibility conformance of system-served surfaces",
     "source": "source-gap", "coverage": "none",
     "target": "fact_a11y_pass_release (automated pass-rate; not a conformance claim)",
     "gap_needs": "an accessibility audit; automated CI checks give a pass rate, "
                  "not conformance", "metric": "M5"},
    {"id": "R2", "ledger": "Risk", "label": "Key-person dependency (named backups per area)",
     "source": "source-gap", "coverage": "none",
     "target": "(org record; not modeled as a fact table in 02)",
     "gap_needs": "an org record of named backups per critical area", "metric": "n/a"},
    # Not counted (narrative row, no source by design)
    {"id": "N1", "ledger": "Not counted", "label": "Benefits deliberately left unquantified",
     "source": "n/a", "coverage": "narrative",
     "target": "(narrative; named in the report, not a data row)",
     "gap_needs": "", "metric": "n/a"},
]


def all_rows():
    """Every classified row: structural inputs, metrics, and ledger rows."""
    return STRUCTURAL_INPUTS + METRICS + LEDGER_ROWS


def source_gaps():
    """Rows that no figma or supernova read can supply."""
    return [r for r in (METRICS + LEDGER_ROWS) if r.get("source") == "source-gap"]


def covered_by(source):
    """Rows a given named source supplies, fully or partially."""
    return [r for r in all_rows() if r.get("source") == source]


def unclassified():
    """Metric or ledger rows with no source classification at all (should be none)."""
    bad = []
    for r in METRICS + LEDGER_ROWS:
        if not r.get("source"):
            bad.append(r["id"])
    return bad
