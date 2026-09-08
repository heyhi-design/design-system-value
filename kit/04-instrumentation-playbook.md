---
title: Instrumentation playbook
kit: design-system-value-kit
artifact: 04
date: 2026-09-01
classification: unclassified
---

# Instrumentation playbook

How to get each number in the metric pack out of the systems you already have, in order of effort. Each layer says what it yields, what it cannot tell you, the tool classes that exist, and the mistake most teams make first.

Read this with artifact 02: every step ends in a row in a named table.

The operable collectors that pull these numbers from named sources are provided as a companion `kit/collectors/` layer: a metric-to-source map (`metric-source-map.md`), generic credential-configurable reference adapters for a design tool's library analytics (Figma) and a design-system documentation platform (Supernova), and a runbook (`runbook.md`) with a credential-free dry-run. This playbook is the method; the collectors are the mechanism. Where that layer is present, point the packet at a design system and the adapters fill the tables below.

---

## Layer 0. Scope and identity (before any measurement)

1. **List the surfaces.** Products, platforms, routes or screens, an owning team for each, an in-scope flag. This is `dim_surface`. Without it, every coverage number is an average over an unknown denominator.
2. **List the teams and their managers.** `dim_team`, including engineering and design manager names. The sort-by-owner control on the team view depends on it.
3. **Tag the libraries.** Which packages, design-tool libraries, and token collections are "the system," which are legacy, which are custom. `dim_component.library`.
4. **Publish the definitions** for the first three metrics (usually M1, M2, M9). Version 1, dated.

Mistake to avoid: measuring before the surface list exists, then arguing about what the percentage means.

## Layer 1. Cost (M9)

- **Do:** sit with a finance partner for an hour. Headcount × the loaded rate they will defend, plus tooling invoices, plus a maintenance reserve stated as a percentage of team time. Divide by consuming teams and by consumers. Record the rate basis in `fact_cost_quarterly.loaded_rate_basis`.
- **Yields:** the denominator for every ratio, the support ratio, cost per team.
- **Cannot tell you:** anything about value. That is the point; state cost first so the value numbers are read against it.
- **Mistake:** omitting maintenance and migrations, then having them appear as "unexpected" cost in year two.

## Layer 2. Design-tool analytics (M2 design side, part of M3)

- **Do:** if the design tool exposes library analytics, export per-component instances, inserts, and detaches by team on a schedule (API where the plan allows; CSV where it does not). Load into `fact_component_usage_daily` with `source='design_tool'`. Restrict the *adoption* read to handoff or production-intended pages, as Pinterest did; use the raw counts only for the detachment counter-metric.
- **Yields:** which teams insert what, detachment spikes, style and variable uptake.
- **Cannot tell you:** coverage. Instances and insertions have no denominator. Do not put them on an executive page.
- **Tool classes:** built-in library analytics (plan-gated), the vendor's REST API, community plugins that scan files, third-party dashboards that read the API.
- **Access reality (vendor docs checked 2026-09-08):** Figma's Library Analytics REST API (component, style, and variable *actions* and *usages*, grouped by team or file, weekly, up to a year of history) is available only to organizations on the Enterprise plan, and the token must carry the `library_analytics:read` scope. Where that tier or scope is unavailable, the scheduled export falls back to CSV or a file-scanning plugin, and the API-only breakdowns (by team, by file) are lost. Re-confirm the current tier and scope against the vendor's developer docs before promising an executive an automated series.
- **Mistake:** presenting insertion counts as adoption.

## Layer 3. Code scans (M2 code side, M3)

- **Do:** a nightly CI job over every front-end repo that (a) counts component instances by library with a scanner that understands your framework, (b) runs lint rules that flag hard-coded color, spacing, and type values where a token exists, writing JSON per project, and (c) tags each count with migration id where relevant. Load into `fact_component_usage_daily (source='code_scan')`, `fact_lint_daily`, and `fact_migration_weekly`.
- **Yields:** migration progress, override rate, legacy pockets by repo and team, dependency impact before a deprecation.
- **Cannot tell you:** whether the import renders or how much of the screen it covers. Label it "static."
- **Tool classes:** component scanners (react-scanner and equivalents), component-analytics products with a CLI, lint frameworks, dependency-graph tools.
- **Mistake:** treating a repo that imports one component as "adopted." Report package diversity beside adoption, as Headway does.

## Layer 4. Production measurement (M1)

Three fidelities; pick the highest you can ship this quarter and record the method on every row.

1. **Import or bundle scan** (a form of layer 3): cheapest; blind to rendering.
2. **DOM-element ratio in production:** mark system components at build time (a data attribute via a compiler plugin), sample the DOM on a timer in production, batch results to the analytics or APM tool. Mews runs this every ten seconds with batching. Counts elements, not area.
3. **Pixel-weighted visual coverage:** a small runtime script measures the rendered area of marked elements, applies weights by element class, and reports per page view. Preply open-sourced an implementation and reports 300,000-plus measurements a day.

- **Do:** implement 2 or 3 as a few days of engineering on top of the existing analytics SDK. Sample, do not measure every view. Segment by product, route, platform, and owning team. Load into `fact_coverage_daily`.
- **Yields:** the headline metric leadership will believe, because it describes what users see.
- **Cannot tell you:** whether the system components are used *correctly*; pair with M5 and M8.
- **Mistake:** averaging across platforms; switching methods mid-series without a new `method` key.

Mobile: instrument the view tree the same way (a traversal that recognizes system component classes), aggregate by mode across experiment variants so one screen gets one score, as Uber does.

## Layer 5. Defects and accessibility (M5)

- **Do:** add two labels to the issue tracker (ui-inconsistency, a11y-regression) and a `surface_class` field or convention. Export per release. Run automated accessibility checks in CI and record failures per surface. Load into `fact_defects_release`.
- **Yields:** the quality half of the story; the evidence for the risk line.
- **Cannot tell you:** conformance. Automated checks catch a fraction of WCAG criteria; say so.
- **Mistake:** comparing defect counts without normalizing by releases or by surface count.

## Layer 6. Consumers (M8, M4 method c)

- **Do:** a four-question survey each quarter to every designer and engineer who touches UI: meets my needs (1–5), helps me work faster (1–5), would recommend (0–10), and hours per week the system saves you (number). One open question. Publish response rate with every figure. Load into `fact_survey_quarterly`.
- **Yields:** the system's own NPS, verbatims for the quote rail, the self-reported hours trend.
- **Cannot tell you:** hard savings. The hours figure is directional and labeled soft.
- **Mistake:** surveying only champions; skipping a quarter and losing the trend.

## Layer 7. Engagement and operations (M6, M7)

- **Do:** count what already happens. Office-hours attendance per team (normalize by team headcount), contributions per team from the issue tracker, support-channel threads per team. Releases planned versus shipped on time, review SLA, sponsor attendance at planning and review. A spreadsheet is enough; load monthly into `fact_engagement_monthly` and `fact_operating_monthly`.
- **Yields:** the leading indicators; the earliest warning that a team is drifting.
- **Cannot tell you:** adoption. Read the two together on the quadrant.
- **Mistake:** turning attendance into a quota.

## Layer 8. Events and studies (M4 methods a and b)

- **Do:** fill the duplication ledger once (M4 method d): for the last three shared patterns built more than once, how many teams built them and at what cost each, with the source of each number. Then, before the next scheduled UI-wide change, open an `event_ledger` row: what it cost last time (from tickets, timesheets, or estimates, with the source named), a plan for capturing hours this time, a before screenshot. Close the row with hours this time, a pessimistic and optimistic saving, confounders, and a quote. Once a year, run the controlled task study (artifact 08).
- **Yields:** the proof stories; the organization's own efficiency number.
- **Cannot tell you:** organization-wide savings; do not multiply a single event across the company.
- **Mistake:** reconstructing "last time" from memory after the fact.

## Layer 9. Surfacing

- **Do:** build the views in artifact 02 in the warehouse or BI tool leadership already opens. Executive tab: screen 1. Team tab: screen 2. Embed both on the design system's documentation site under a Metrics section with the definitions beside them. Generate the monthly one-pager from the same views on a fixed date.
- **Mistake:** a standalone dashboard that only the system team opens.

---

## Effort map

| Layer | Typical effort | Skill needed | First useful output |
|---|---|---|---|
| 0 Scope | 1–2 days | system lead + PM | surface and team lists |
| 1 Cost | half a day | finance partner | cost line |
| 2 Design tool | 1–3 days | designer + script | detachment rate by team |
| 3 Code scans | 2–5 days | front-end engineer | migration chart, override rate |
| 4 Production | 3–10 days | front-end + analytics | coverage headline |
| 4b Overlay (artifact 05) | 3–8 days | front-end engineer | system versus one-offs visible on any screen |
| 5 Defects | 1 day + habit | QA lead | defects by surface class |
| 6 Survey | 1 day + quarterly habit | anyone | satisfaction, hours trend |
| 7 Engagement | 1 day + monthly habit | system team | engagement composite |
| 8 Events | per event | system lead | proof cards |
| 9 Surfacing | 3–5 days | analyst | executive and team views |

Total to a first executive one-pager with two 28-day periods after the baseline: about fifteen weeks (baseline in week 7, first report in week 15), with layers 0, 1, 3 or 4, 6, 7, and 9. The plan skeleton uses the same arithmetic.
