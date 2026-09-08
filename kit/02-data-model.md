---
title: Data model for the value store
kit: design-system-value-kit
artifact: 02
date: 2026-09-01
classification: unclassified
---

# Data model for the value store

The dashboard, the monthly one-pager, and the leadership deck must read the same rows. This is the smallest set of tables that makes that true. It is written in PostgreSQL dialect (casts, `DATE_TRUNC`, `INTERVAL`); every construct has an equivalent in other warehouses, and the dialect-specific lines are marked. Column types are indicative.

Design rules:

- **One fact table per metric family, one dimension per thing you break down by.** No metric is computed in the dashboard layer; every number on a screen is a `SELECT` from a fact table or a view defined here.
- **Every metric fact row carries `metric_id` and `metric_version`**, so a definition change shows as a break in the series, not a silent jump, and every number can be joined back to the definition it was computed under. The risk-posture, verbatim, and adoption-level tables are keyed to their own grain and carry no metric id.
- **`method` and `platform` are keys, never attributes.** A coverage series is one method on one platform. Views never average across either.
- **Events, proofs, verbatims, and levels are first-class**, not annotations on a chart.
- **Personal data is limited to** a respondent's role and team, and to verbatims that respondents have agreed may be published; store consent with the verbatim.

---

## Dimensions

```sql
CREATE TABLE dim_team (
  team_id        TEXT PRIMARY KEY,
  team_name      TEXT NOT NULL,
  org_unit       TEXT,               -- product line, division
  eng_manager    TEXT,               -- for sort-by-owner
  design_manager TEXT,
  headcount      INTEGER,            -- for normalizing engagement
  active_from    DATE,
  active_to      DATE
);

CREATE TABLE dim_surface (             -- a page, screen, route, or view
  surface_id     TEXT PRIMARY KEY,
  surface_name   TEXT NOT NULL,
  product        TEXT NOT NULL,
  platform       TEXT NOT NULL,       -- web, ios, android, ...
  route_or_id    TEXT,
  owner_team_id  TEXT REFERENCES dim_team(team_id),
  in_scope       BOOLEAN DEFAULT TRUE,
  weight_class   TEXT                 -- 'flagship', 'secondary', 'internal'  [decision: which surfaces are flagship]
);

CREATE TABLE dim_component (
  component_id   TEXT PRIMARY KEY,
  component_name TEXT NOT NULL,
  library        TEXT NOT NULL,       -- system library name, 'legacy:<name>', or 'custom'
  library_version TEXT,
  kind           TEXT,                -- component, token, style, variable
  status         TEXT                 -- stable, deprecated, experimental
);

CREATE TABLE dim_metric_definition (   -- one row per published version of a metric contract (artifact 01)
  metric_id      TEXT NOT NULL,       -- 'M1'..'M9' or your own ids
  version        INTEGER NOT NULL,
  effective_from DATE NOT NULL,
  effective_to   DATE,
  definition_url TEXT NOT NULL,       -- link to the published contract page
  formula_text   TEXT NOT NULL,
  owner          TEXT NOT NULL,
  counter_metric TEXT,
  baseline_value NUMERIC, baseline_date DATE,
  target_value   NUMERIC, target_date DATE,
  gaming_path    TEXT,
  breach_rule    TEXT,                -- human-readable; the nightly job encodes it
  PRIMARY KEY (metric_id, version)
);

CREATE TABLE dim_adoption_level (      -- artifact 09
  level          INTEGER PRIMARY KEY, -- 0..5
  level_name     TEXT NOT NULL,
  criteria_text  TEXT NOT NULL
);
```

## Facts

Every fact table for one of the M1..M9 metrics carries `(metric_id, metric_version)` referencing `dim_metric_definition`. Three tables in this section are keyed to their own grain and carry no metric id: `fact_a11y_pass_release` (risk posture, by release and surface), `fact_survey_verbatim` (by verbatim id), and `fact_team_level_monthly` (by the adoption-level dimension).

```sql
-- M1 coverage, measured in production or by scan. One row per surface, day, and method.
CREATE TABLE fact_coverage_daily (
  day            DATE NOT NULL,
  surface_id     TEXT NOT NULL REFERENCES dim_surface(surface_id),
  method         TEXT NOT NULL,       -- 'pixel', 'dom', 'import'  (never mixed in one series)
  coverage_pct   NUMERIC(5,2) NOT NULL,
  samples        INTEGER NOT NULL,    -- page views or scans behind the number; used as the weight
  ds_weight      NUMERIC,             -- numerator, for audit
  total_weight   NUMERIC,             -- denominator, for audit
  metric_id      TEXT NOT NULL DEFAULT 'M1',
  metric_version INTEGER NOT NULL,
  PRIMARY KEY (day, surface_id, method),
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- M2 design side (inserts, detaches) and M3 inputs (instances by library). One row per component, team, day, source.
CREATE TABLE fact_component_usage_daily (
  day            DATE NOT NULL,
  component_id   TEXT NOT NULL REFERENCES dim_component(component_id),
  team_id        TEXT NOT NULL REFERENCES dim_team(team_id),
  source         TEXT NOT NULL,       -- 'design_tool', 'code_scan', 'runtime'
  instances      INTEGER,
  inserts        INTEGER,             -- design tool only
  detaches       INTEGER,             -- design tool only (M2)
  overrides      INTEGER,             -- code scan: style overrides applied to DS components (M2, code side, part 2)
  metric_id      TEXT NOT NULL,       -- 'M2' or 'M3' depending on the pipeline that wrote the row
  metric_version INTEGER NOT NULL,
  PRIMARY KEY (day, component_id, team_id, source),
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- M2 code side, part 1: hard-coded values where a token exists.
CREATE TABLE fact_lint_daily (
  day            DATE NOT NULL,
  repo           TEXT NOT NULL,
  team_id        TEXT NOT NULL REFERENCES dim_team(team_id),
  rule_id        TEXT NOT NULL,        -- e.g. no-raw-color, no-raw-spacing
  violations     INTEGER NOT NULL,
  opportunities  INTEGER NOT NULL,     -- declarations where a token could apply
  metric_id      TEXT NOT NULL DEFAULT 'M2',
  metric_version INTEGER NOT NULL,
  PRIMARY KEY (day, repo, rule_id),
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- M3 migration progress. One row per migration, team, week.
CREATE TABLE fact_migration_weekly (
  week           DATE NOT NULL,        -- Monday of the week
  migration_id   TEXT NOT NULL,        -- 'typography-2026', 'icons-v3', ...
  team_id        TEXT NOT NULL REFERENCES dim_team(team_id),
  ds_instances   INTEGER NOT NULL,
  legacy_instances INTEGER NOT NULL,
  metric_id      TEXT NOT NULL DEFAULT 'M3',
  metric_version INTEGER NOT NULL,
  PRIMARY KEY (week, migration_id, team_id),
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- M5 defects per release, by surface class.
CREATE TABLE fact_defects_release (
  release_id     TEXT NOT NULL,
  release_date   DATE NOT NULL,
  surface_id     TEXT NOT NULL REFERENCES dim_surface(surface_id),
  surface_class  TEXT NOT NULL,        -- 'on_system', 'mixed', 'off_system'
  ui_defects     INTEGER DEFAULT 0,
  a11y_defects   INTEGER DEFAULT 0,
  visual_diff_failures INTEGER DEFAULT 0,
  metric_id      TEXT NOT NULL DEFAULT 'M5',
  metric_version INTEGER NOT NULL,
  PRIMARY KEY (release_id, surface_id),
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- Risk posture: automated accessibility checks per release (pass rate, not a conformance claim).
CREATE TABLE fact_a11y_pass_release (
  release_id     TEXT NOT NULL,
  release_date   DATE NOT NULL,
  surface_id     TEXT NOT NULL REFERENCES dim_surface(surface_id),
  checks_run     INTEGER NOT NULL,
  checks_passed  INTEGER NOT NULL,
  tool           TEXT NOT NULL,
  PRIMARY KEY (release_id, surface_id)
);

-- M6 engagement per team per month.
CREATE TABLE fact_engagement_monthly (
  month          DATE NOT NULL,        -- first day of the month
  team_id        TEXT NOT NULL REFERENCES dim_team(team_id),
  office_hours_actual   INTEGER, office_hours_target INTEGER,
  contributions_actual  INTEGER, contributions_target INTEGER,
  support_actual        INTEGER, support_target INTEGER,
  composite_pct  NUMERIC(5,2),         -- mean of the three capped ratios × 100
  metric_id      TEXT NOT NULL DEFAULT 'M6',
  metric_version INTEGER NOT NULL,
  PRIMARY KEY (month, team_id),
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- M7 operating health, system level, per month.
CREATE TABLE fact_operating_monthly (
  month          DATE PRIMARY KEY,     -- first day of the month
  releases_planned INTEGER, releases_on_time INTEGER,
  reviews_opened INTEGER, reviews_within_sla INTEGER,
  rituals_held   INTEGER, sponsor_attended INTEGER,
  metric_id      TEXT NOT NULL DEFAULT 'M7',
  metric_version INTEGER NOT NULL,
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- M8 survey results per team and role per quarter; M4(c) self-reported hours rides here.
CREATE TABLE fact_survey_quarterly (
  quarter        DATE NOT NULL,        -- first day of the quarter
  team_id        TEXT NOT NULL REFERENCES dim_team(team_id),
  role           TEXT NOT NULL,        -- designer, engineer, pm, other
  responses      INTEGER NOT NULL,
  invited        INTEGER NOT NULL,
  meets_needs    NUMERIC(3,2),         -- mean 1..5
  faster         NUMERIC(3,2),
  recommend_net  NUMERIC(5,2),
  hours_saved_median NUMERIC(5,2),     -- M4(c), self-reported, soft
  metric_id      TEXT NOT NULL DEFAULT 'M8',
  metric_version INTEGER NOT NULL,
  PRIMARY KEY (quarter, team_id, role),
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

CREATE TABLE fact_survey_verbatim (    -- open-question answers approved for publication
  verbatim_id    TEXT PRIMARY KEY,
  quarter        DATE NOT NULL,
  team_id        TEXT REFERENCES dim_team(team_id),
  role           TEXT,
  text           TEXT NOT NULL,
  publish_consent BOOLEAN NOT NULL DEFAULT FALSE
);

-- M9 cost per quarter.
CREATE TABLE fact_cost_quarterly (
  quarter        DATE PRIMARY KEY,
  people_cost    NUMERIC NOT NULL,
  loaded_rate    NUMERIC NOT NULL,
  loaded_rate_basis TEXT NOT NULL,     -- how the rate was agreed with finance
  tooling_cost   NUMERIC NOT NULL,
  maintenance_reserve NUMERIC NOT NULL,
  consuming_teams INTEGER NOT NULL,
  consumers      INTEGER NOT NULL,
  system_staff   NUMERIC NOT NULL,     -- FTE
  metric_id      TEXT NOT NULL DEFAULT 'M9',
  metric_version INTEGER NOT NULL,
  FOREIGN KEY (metric_id, metric_version) REFERENCES dim_metric_definition(metric_id, version)
);

-- Adoption level per team per month (artifact 09).
CREATE TABLE fact_team_level_monthly (
  month          DATE NOT NULL,
  team_id        TEXT NOT NULL REFERENCES dim_team(team_id),
  level          INTEGER NOT NULL REFERENCES dim_adoption_level(level),
  committed_next_level INTEGER REFERENCES dim_adoption_level(level),
  committed_by   DATE,
  note           TEXT,
  PRIMARY KEY (month, team_id)
);
```

## Events, proofs, and studies

```sql
-- Artifact 07. One row per natural experiment; feeds M4(b) only.
CREATE TABLE event_ledger (
  event_id       TEXT PRIMARY KEY,
  event_type     TEXT NOT NULL,        -- rebrand, theme, remediation, migration, framework, new_surface
  title          TEXT NOT NULL,
  started_on     DATE, finished_on DATE,
  hours_last_time NUMERIC, hours_last_time_source TEXT,
  baseline_kind  TEXT NOT NULL,        -- 'recorded' or 'estimated'
  hours_this_time NUMERIC, hours_this_time_source TEXT,
  pessimistic_hours_saved NUMERIC, optimistic_hours_saved NUMERIC,
  loaded_rate    NUMERIC, saving_class TEXT,   -- 'soft', 'avoidance', 'hard'
  quote          TEXT, quote_attribution TEXT,
  confounders    TEXT,                 -- what else changed at the same time
  owner          TEXT NOT NULL,
  published      BOOLEAN DEFAULT FALSE,
  metric_id      TEXT NOT NULL DEFAULT 'M4',
  metric_version INTEGER NOT NULL
);

CREATE TABLE event_image (             -- three to five representative screens per event, before and after
  image_id       TEXT PRIMARY KEY,
  event_id       TEXT NOT NULL REFERENCES event_ledger(event_id),
  phase          TEXT NOT NULL,        -- 'before' or 'after'
  surface_id     TEXT REFERENCES dim_surface(surface_id),
  taken_on       DATE NOT NULL,
  url            TEXT NOT NULL
);

-- M4(d) avoided duplication: what N teams would have built separately.
CREATE TABLE duplication_ledger (
  item_id        TEXT PRIMARY KEY,
  component_family TEXT NOT NULL,      -- 'buttons', 'date picker', ...
  teams_that_would_build INTEGER NOT NULL,
  hours_per_build NUMERIC NOT NULL,
  hours_source   TEXT NOT NULL,        -- interface inventory + estimates, past tickets, ...
  loaded_rate    NUMERIC,
  recorded_on    DATE NOT NULL,
  metric_id      TEXT NOT NULL DEFAULT 'M4',
  metric_version INTEGER NOT NULL
);

-- Screen 7. Generated nightly from breach rules; edited by a person.
CREATE TABLE feed_events (
  feed_event_id  TEXT PRIMARY KEY,
  ts             TIMESTAMP NOT NULL,
  event_class    TEXT NOT NULL,        -- 'breach' (from a rule) or 'info' (level change, release, celebration)
  severity       TEXT NOT NULL,        -- critical, warning, info
  original_severity TEXT NOT NULL,     -- before any escalation
  metric_id      TEXT NOT NULL,
  team_id        TEXT REFERENCES dim_team(team_id),
  subject        TEXT NOT NULL,        -- component, surface, or migration id
  headline       TEXT NOT NULL,        -- "Button detachment spike, Mobile team"
  delta_text     TEXT,                 -- "1.8% to 9.4% over 7 days"
  since          DATE,
  action         TEXT,                 -- the breach rule's action, from the definition
  assignee       TEXT,
  resolved_on    DATE
);

-- Artifact 08. One row per study run per discipline.
CREATE TABLE task_study (
  study_id       TEXT PRIMARY KEY,
  run_on         DATE NOT NULL,
  discipline     TEXT NOT NULL,        -- 'design' or 'engineering'
  participants   INTEGER NOT NULL,
  tasks          INTEGER NOT NULL,
  median_without_min NUMERIC, median_with_min NUMERIC,
  pct_faster_low NUMERIC, pct_faster_high NUMERIC,   -- range across tasks
  quality_without NUMERIC, quality_with NUMERIC,      -- blind reviewer scores
  quality_review_method TEXT,
  caveats        TEXT,
  report_url     TEXT,
  metric_id      TEXT NOT NULL DEFAULT 'M4',
  metric_version INTEGER NOT NULL
);
```

## Views the screens read

Both views keep `method`, `platform`, and `metric_version` as keys, filter to in-scope surfaces, and weight by `samples`. The executive headline picks one platform and one method per product; it never averages across them.

```sql
-- Screen 1 headline: 28-day sample-weighted coverage per product, platform, method, and definition version,
-- with the prior 28 days for the delta.
CREATE VIEW v_exec_headline AS
SELECT s.product, s.platform, c.method, c.metric_version,
       SUM(CASE WHEN c.day >= CURRENT_DATE - 28 THEN c.coverage_pct * c.samples END)
         / NULLIF(SUM(CASE WHEN c.day >= CURRENT_DATE - 28 THEN c.samples END), 0)          AS coverage_28d,
       SUM(CASE WHEN c.day < CURRENT_DATE - 28 AND c.day >= CURRENT_DATE - 56 THEN c.coverage_pct * c.samples END)
         / NULLIF(SUM(CASE WHEN c.day < CURRENT_DATE - 28 AND c.day >= CURRENT_DATE - 56 THEN c.samples END), 0) AS coverage_prev_28d,
       SUM(CASE WHEN c.day >= CURRENT_DATE - 28 THEN c.samples END)                          AS samples_28d
FROM fact_coverage_daily c
JOIN dim_surface s USING (surface_id)
WHERE s.in_scope AND c.day >= CURRENT_DATE - 56
GROUP BY s.product, s.platform, c.method, c.metric_version;

-- Screen 2 team view: one row per team, platform, and method, with the signals side by side.
CREATE VIEW v_team_view AS
WITH cov AS (
  SELECT s.owner_team_id AS team_id, s.platform, c.method, c.metric_version,
         SUM(c.coverage_pct * c.samples) / NULLIF(SUM(c.samples), 0) AS coverage_28d
  FROM fact_coverage_daily c JOIN dim_surface s USING (surface_id)
  WHERE s.in_scope AND c.day >= CURRENT_DATE - 28
  GROUP BY s.owner_team_id, s.platform, c.method, c.metric_version
), ov AS (
  SELECT team_id, SUM(violations)::NUMERIC / NULLIF(SUM(opportunities), 0) AS override_rate   -- ::NUMERIC is PostgreSQL
  FROM fact_lint_daily WHERE day >= CURRENT_DATE - 28 GROUP BY team_id
), eng AS (
  SELECT team_id, composite_pct FROM fact_engagement_monthly
  WHERE month = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')::DATE               -- PostgreSQL
), sat AS (
  SELECT team_id,
         SUM(meets_needs * responses) / NULLIF(SUM(responses), 0) AS meets_needs,              -- response-weighted across roles
         SUM(responses) AS responses
  FROM fact_survey_quarterly
  WHERE quarter = (SELECT MAX(quarter) FROM fact_survey_quarterly) GROUP BY team_id
), lvl AS (
  SELECT team_id, level, committed_next_level, committed_by FROM fact_team_level_monthly
  WHERE month = (SELECT MAX(month) FROM fact_team_level_monthly)
)
SELECT t.team_id, t.team_name, t.eng_manager, t.design_manager,
       cov.platform, cov.method, cov.metric_version, cov.coverage_28d,
       ov.override_rate, eng.composite_pct, sat.meets_needs, sat.responses,
       lvl.level, lvl.committed_next_level, lvl.committed_by
FROM dim_team t
LEFT JOIN cov USING (team_id)
LEFT JOIN ov  USING (team_id)
LEFT JOIN eng USING (team_id)
LEFT JOIN sat USING (team_id)
LEFT JOIN lvl USING (team_id);
```

## Notes for the implementer

- **A team with no coverage rows gets NULL, not zero.** Screen 2 renders NULL as "not instrumented."
- **Store numerators and denominators**, not only the percentage, so any figure can be audited.
- **`metric_id` plus `metric_version` on every metric fact row** (the M1..M9 tables; the three grain-specific fact tables noted above carry neither) is what lets the definitions page (screen 8) and the trend line agree, and what lets a definition change appear as a labeled break.
- **The feed is derived, then edited.** A nightly job writes `feed_events` rows with `event_class = 'breach'` from the breach rules in artifact 01 and `event_class = 'info'` for level changes and releases; a person adds context, assigns, escalates (`severity` moves, `original_severity` stays), and resolves. The feed is never the only record of a metric change.
- **Access.** Read for everyone in the organization by default; write for the system team, and for finance on the cost table. The point of the store is that anyone can pull the numbers.
- **Grain.** Coverage and usage are daily; migration is weekly; engagement, operating health, and levels are monthly; survey and cost are quarterly. Screens roll up, never down.
- **Verified against PostgreSQL 17.** The full schema (22 tables and 2 views) and a seeded probe ran on PostgreSQL 17 on 2026-09-08: every object built, the foreign keys enforce (a reference to a missing row aborts the insert), and both views returned computed rows, including a team with no coverage rendering as NULL rather than zero.
