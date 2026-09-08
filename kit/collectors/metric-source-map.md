---
title: Metric-to-source map
kit: design-system-value-kit
artifact: collectors/metric-source-map
date: 2026-09-08
classification: unclassified
---

# Metric-to-source map

For every metric in the pack (M1..M9, artifact 01) and every row of the value
ledger (field guide Appendix A), this map names where the number comes from: a
read the kit ships an adapter for, or a `source-gap` that needs instrumentation
the two named sources cannot provide. Read it beside artifact 02 (the tables the
numbers land in) and artifact 04 (the method behind each layer).

The two named sources this kit ships adapters for are a design tool's library
analytics (Figma) and a design-system documentation platform (Supernova). The
honest headline of this map: **those two sources reach the design side only.**
They supply component, style, and variable inventory and design-side usage over
time. Most of the executive value ledger, including production coverage, hours
returned, defects, engagement, cost, and risk, is a `source-gap` for these two
sources and needs a code-side scan, a production-runtime sampler, an issue
tracker, a survey, finance data, or a hand-kept ledger.

The machine-readable mirror of this map is `source_map.py`; the checker beside
it is `dryrun.py`, which re-derives the coverage counts from `source_map.py` and
emits the fill-map with no credentials. Keep this document and `source_map.py` in
sync by hand.

## The four source kinds

| Kind | What it is |
|---|---|
| `figma-analytics` | The Figma Library Analytics REST API (Enterprise plan, scope `library_analytics:read`). Design-side usage over time. Gated on access; see `figma-adoption-adapter.md`. |
| `figma-structural` | The Figma design read surface plus a read-only library census and code crosswalk. Component, variable, and style inventory. Runs after the library exists (the deferred structural half; see `runbook.md`). |
| `supernova` | The documentation platform read API (SDK, personal-access-token auth). Token, asset, and component inventory and documentation coverage. Gated on access; see `supernova-adapter.md`. |
| `source-gap` | No Figma or Supernova read can supply this. It needs a code-side scan, a production-runtime sampler, an issue tracker, a survey, finance data, product analytics, or a hand-kept ledger. A gap is a request for instrumentation, not a defect in the kit. |

## What the two named sources do supply (design side)

These are the positive inputs. They feed the metric rows below; they are not
themselves executive metrics.

| Id | Input | Source | Call | Lands in |
|---|---|---|---|---|
| S1 | Component / variable / style inventory and coverage | `figma-structural` | design read surface plus a read-only library census and code crosswalk | `dim_component` |
| S2 | Design-side component insertions and detachments (weekly) | `figma-analytics` | `GET /v1/analytics/libraries/:library_file_key/component/actions?group_by=component\|team` | `fact_component_usage_daily` (inserts, detaches) |
| S3 | Design-side instances and files/teams using a component | `figma-analytics` | `GET /v1/analytics/libraries/:library_file_key/component/usages?group_by=component\|file` | `fact_component_usage_daily` (instances), `fact_migration_weekly` |
| S4 | Style and variable (token) actions and usages | `figma-analytics` | `/style/actions`, `/style/usages`, `/variable/actions`, `/variable/usages` (same params) | `fact_component_usage_daily` (kind style/variable) |
| S5 | Token, asset, and component inventory | `supernova` | SDK read of the version (tokens, assets, components) | `dim_component` |
| S6 | Documentation coverage (documented vs not) | `supernova` (partial) | SDK read of documentation structure and content | schema gap: no documentation-coverage table in 02 today |

The Figma calls are weekly, grouped by component, style, variable, team, or
file, up to a year of history, and paginate with a `cursor`. The base is
`https://api.figma.com`. The token is sent as `X-Figma-Token` (or an OAuth
bearer) and must carry the `library_analytics:read` scope on an Enterprise plan.
The Supernova reads authenticate with a personal access token. Vendor surfaces
confirmed against the current developer docs on 2026-09-08; re-confirm the tier,
scope, and shapes before promising an executive an automated series.

## The nine metrics

| Metric | Source | Coverage | Endpoint / call | Transform into 02 | Gap (what it still needs) |
|---|---|---|---|---|---|
| M1 Coverage of what users see | `source-gap` | none | none from Figma/Supernova | production sampler (pixel or DOM) or import scan writes `coverage_pct` with a `method` key | production-runtime sampler or a code-side import/bundle scan; S3 is a design-side proxy only |
| M2 Overrides, detachments, arbitrary values | `figma-analytics` | partial | `component/actions` (design side) | detachments / insertions into `fact_component_usage_daily`; lint into `fact_lint_daily` | code-side CI: lint for hard-coded values and a scan for style overrides |
| M3 Migration progress | `figma-analytics` | partial | `component/usages` (design side) | design-side instances into `fact_migration_weekly`; code scan writes `ds_instances`, `legacy_instances` | code-side static component scan tagged by migration id |
| M4 Hours returned | `source-gap` | none | none from Figma/Supernova | study, event, survey, duplication into their four tables; never summed | a task study (08), an event ledger (07), a quarterly survey, a duplication ledger |
| M5 Defects and regressions | `source-gap` | none | none from Figma/Supernova | labeled defects per release into `fact_defects_release`; automated pass-rate into `fact_a11y_pass_release` | issue-tracker labels, a `surface_class`, CI a11y checks, a visual-regression tool |
| M6 Engagement composite | `source-gap` | none | none from Figma/Supernova | office-hours, contribution, support counts normalized by team size into `fact_engagement_monthly` | calendar, tracker, and support exports |
| M7 Sponsor and operating health | `source-gap` | none | none from Figma/Supernova | predictability, review SLA, sponsor attendance into `fact_operating_monthly` | release log, review queue, attendance records |
| M8 Consumer satisfaction | `source-gap` | none | none from Figma/Supernova | four-question survey into `fact_survey_quarterly`; verbatims into `fact_survey_verbatim` | a quarterly survey to every consumer |
| M9 Cost to run | `source-gap` | none | none from Figma/Supernova | loaded headcount, tooling, maintenance into `fact_cost_quarterly` | finance headcount, tooling invoices, a maintenance assumption |

Design side covered by Figma means the detachment counter-metric (M2) and the
design-side instance count (M3) arrive from the API. The code side of both, and
the production render coverage M1 reports, are gaps, exactly as artifact 04
Layers 3 and 4 describe.

## The value ledger (field guide Appendix A)

Every fill-in row from the field guide's Appendix A, mapped.

| Id | Ledger / line | Source | Lands in | Gap |
|---|---|---|---|---|
| C1 | 1 Cost / team headcount x loaded cost | `source-gap` | `fact_cost_quarterly.people_cost, loaded_rate` | finance / HR headcount data |
| C2 | 1 Cost / tooling and platform | `source-gap` | `fact_cost_quarterly.tooling_cost` | tooling invoices (finance) |
| C3 | 1 Cost / maintenance and migrations (projected) | `source-gap` | `fact_cost_quarterly.maintenance_reserve` | a maintenance-reserve assumption with finance |
| C4 | 1 Cost / support ratio (staff : consumers) | `source-gap` | `fact_cost_quarterly.system_staff, consumers` | headcount and consumer counts |
| H1 | 2 Hours / controlled task study | `source-gap` | `task_study` | a controlled task study (artifact 08) |
| H2 | 2 Hours / event-based measurement | `source-gap` | `event_ledger` | an event ledger opened before the event (07) |
| H3 | 2 Hours / avoided duplication | `source-gap` | `duplication_ledger` | a duplication ledger (interface inventory + estimates) |
| H4 | 2 Hours / self-reported hours saved | `source-gap` | `fact_survey_quarterly.hours_saved_median` | the quarterly consumer survey (soft, never hard) |
| O1 | 3 Outcomes / coverage of what users see | `source-gap` | `fact_coverage_daily` | production sampler or import scan; S3 is a design-side proxy only |
| O2 | 3 Outcomes / counter-metric (detach / override / arbitrary) | `figma-analytics` | `fact_component_usage_daily.detaches`, `fact_lint_daily` | code-side overrides and lint (design-side detachments come from the API) |
| O3 | 3 Outcomes / UI defects and a11y regressions per release | `source-gap` | `fact_defects_release` | issue-tracker labels, CI a11y checks |
| O4 | 3 Outcomes / outcome in a migrated flow vs a control | `source-gap` | product analytics (not a 02 fact table) | product analytics with a difference-in-differences design |
| O5 | 3 Outcomes / consumer satisfaction | `source-gap` | `fact_survey_quarterly` | the quarterly consumer survey |
| L1 | Leading / engagement composite (3-mo rolling) | `source-gap` | `fact_engagement_monthly` | calendar, tracker, and support exports |
| L2 | Leading / sponsor attendance | `source-gap` | `fact_operating_monthly.sponsor_attended` | meeting-attendance records |
| L3 | Leading / contribution review SLA; release predictability | `source-gap` | `fact_operating_monthly.reviews_within_sla, releases_on_time` | review queue and release log |
| R1 | Risk / accessibility conformance | `source-gap` | `fact_a11y_pass_release` (a pass rate, not a conformance claim) | an accessibility audit |
| R2 | Risk / key-person dependency | `source-gap` | org record (not a 02 fact table) | an org record of named backups per critical area |
| N1 | Not counted / benefits left unquantified | n/a | narrative, named in the report | none: this row is a sentence, not a data pull |

## Coverage summary

Of the nine metrics, the two named sources supply the design side of two (M2,
M3) and a design-side proxy for a third (M1). The other six are source-gaps. Of
the eighteen value-ledger data rows, one (O2) is served design-side by the Figma
API and seventeen are source-gaps. The `source-gap` count the checker reports is
twenty-four across metrics and ledger rows combined. That is the map working as
intended: it says plainly that pointing the packet at Figma and Supernova fills
the design-side adoption story and leaves the cost, hours, quality, and risk
ledgers for code-side, runtime, survey, and finance instrumentation.

Run `python3 dryrun.py` to emit this map as a fill-map and the source-gap list
with no credentials, and `python3 dryrun.py --check` to assert nothing here is
left unclassified.
