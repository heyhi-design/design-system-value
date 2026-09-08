---
title: Screen specs and wireframes
kit: design-system-value-kit
artifact: 03
date: 2026-09-01
classification: unclassified
wireframes: wireframes/ (low-fidelity PNGs for screens 1, 2, 6, 7)
---

# Screen specs and wireframes

Eleven screens for a value-reporting surface. Each spec gives the audience, the question the screen answers, the layout in reading order, the components, the data binding to artifact 02, the states, and the precedent it is drawn from. Four screens have low-fidelity wireframes in `wireframes/`; the rest are described precisely enough to sketch.

Global rules (from the survey's pattern library):

- Rings for bounded percentages, sparklines for trends, bars for comparisons, a treemap for composition. No gauges, no donuts with more than two slices.
- Every number shows its date, its method, and a link to its definition, in small type.
- Two hues for system versus legacy, fixed across all screens. Deltas use direction (arrow) plus color; green means "toward target."
- Screens 1, 2, and 3 embed in the organization's BI tool and are mirrored on the design system's documentation site under Metrics. System-team screens (4, 6, 7, 8) may live on the documentation site alone. Whichever surface is standalone gets an owner column, a leaderboard, and a path into the ticketing system so that it is visited.

---

## Structure and divergence read

A structural sanity check on the inventory below, before any visual language is applied. It informs; it decides nothing.

- **Structural options present: one.** The eleven screens are eleven views of a single value-reporting surface, not eleven competing structures. The companion survey's "one screen" composition is a second, maximally converged variant of the same structure. So the inventory carries one structure plus one tighter variant of it, not a set of structural alternatives. That is a deliberate convergence for a first build, and a risk only if it forecloses a structure the question would reward.
- **Fidelity vs the question.** The question is what a leadership value surface should show and in what structure. Fidelity as read is lo-fi and structural: four low-fidelity wireframes plus described specs, no color, type, or tokens [inferred classification]. That sits at the rung the question needs; the surface is specced structurally so a build can start from something real without committing a visual language early.
- **The lo-fi phase is in evidence:** four low-fidelity wireframes in `wireframes/` and this structural spec. It was not skipped.
- **Widening stimulus** (unordered, not recommendations): an alternative that decomposes by audience (one surface per reader) rather than by metric; an alternative that starts from the proof ledger (events first) rather than the dashboard; an alternative that discloses the team breakdown on demand rather than as a standing table.
- **What this read cannot see:** whether upstream work considered and set aside other structures. The survey records one convergence (its eight elements), which this read counts as context, not as a verdict.

**⛔ Whether to diverge further, NEEDS HUMAN:** ____________________
**⛔ The fidelity call, NEEDS HUMAN:** ____________________

---

## Screen 1. Executive one-pager

- **Audience:** sponsor, their peers, finance. Read in under two minutes, monthly, on a fixed date.
- **Question:** what did we get, compared to what, and what do you want me to decide?
- **Layout (top to bottom):**
  1. Title row: system name, period, owner, "definitions" and "data" links.
  2. Headline block: one large number (M1 coverage for the flagship product, or the audience's chosen metric), baseline → now → target inline, a six-period sparkline, delta chip versus prior period.
  3. Scorecard row: four tiles in the scorecard row format (name, value, target, variance, sparkline, owner), cost first: M9 cost per consuming team, M2 override rate, M5 defects on versus off system, M6 engagement composite. M1 is the headline and is not repeated as a tile.
  4. Proof card (artifact 07), most recent published event.
  5. "What we are not counting": two or three named unquantified benefits.
  6. Risk and breach line: one sentence with a trend arrow (automated accessibility pass rate or key-person dependency), plus any team named this period by a breach rule (M1's rule names the owning team here).
  7. Decision box: the ask in one sentence; what changes if the answer is no.
- **Data:** `v_exec_headline` (headline, one platform and method); `fact_cost_quarterly` (M9); `fact_lint_daily` and `fact_component_usage_daily` (M2); `fact_defects_release` (M5); `fact_engagement_monthly` (M6); `event_ledger` and `event_image` (proof card); `fact_a11y_pass_release` (risk line); `feed_events` (teams named this period).
- **States:** first period (no delta; show "baseline established <date>"); definition changed this period (a break marker on the sparkline with a footnote); no proof card this month (show the most recent with its date, never an empty slot).
- **Precedents:** Forrester TEI executive summary; DX Core 4 tiles; Preply headline; Uber proof card.
- **Wireframe:** `wireframes/01-exec-one-pager.png`.

## Screen 2. Team view

- **Audience:** product and engineering leads; the system team.
- **Question:** where is the system, where is it not, and who owns each gap?
- **Layout:**
  1. Controls: sort by team / product / engineering manager / design manager; platform tabs (never averaged); period selector; quadrant toggle.
  2. Table, one row per team, platform, and coverage method (the view's grain; platforms are never averaged): coverage (M1) with inline bar and delta; override rate (M2); migration progress (M3) for the active migration; engagement composite (M6); satisfaction (M8, latest); level or tier (artifact 09); owner. Expandable to product and route rows.
  3. Quadrant panel (toggle): adoption × engagement, teams as dots, four labeled cells with the recommended action per cell.
  4. Footer: definitions links; "download CSV."
- **Data:** `v_team_view` (which carries level and committed level from `fact_team_level_monthly`), `fact_migration_weekly`, `feed_events` (breach flags), `dim_team`.
- **States:** team with no coverage data (show "not instrumented" rather than zero); team below breach threshold (row flag and a link to the feed event); unowned team (owner cell reads "unowned," which is itself a finding).
- **Precedents:** Pinterest FigStats team table; Headway adoption report and quadrant; Uber sort-by-owner.
- **Wireframe:** `wireframes/02-team-view.png`.

## Screen 3. Migration chart

- **Audience:** everyone.
- **Question:** is the named migration happening?
- **Layout:** one chart per migration: system instances rising, legacy instances falling, weekly, with the target date as a vertical marker; a one-sentence plain-language callout under the chart ("Legacy typography down 31% since March"); a treemap alternative (area = instances, color = library) behind a toggle; per-platform tabs.
- **Data:** `fact_migration_weekly`, `fact_component_usage_daily`.
- **States:** migration complete (chart freezes, badge "completed <date>"); stalled (no change in four weeks: callout says so).
- **Precedents:** Productboard typography chart; Omlet stacked area with callout; Segment Evergreen treemap.

## Screen 4. Coverage explorer

- **Audience:** product teams; the system team.
- **Question:** which screens are on the system, which are not, and what is on them?
- **Layout:** filter by product, platform, team; a grid of surface cards, each with a thumbnail screenshot, surface name, coverage % with delta, a11y defects with severity chips, owner; card click opens the surface with the overlay marking (artifact 05) and the list of non-system elements with their nearest system equivalent.
- **Data:** `fact_coverage_daily`, `fact_defects_release`, `dim_surface`; screenshots from the runtime sampler or E2E suite.
- **States:** surface out of scope (grayed, with reason); surface not sampled in 7 days (stale badge).
- **Precedents:** Uber per-screen cards and Base Counter; Preply coverage by team and page; Luro per-page scores.

## Screen 5. Cost ledger

- **Audience:** finance partner, sponsor.
- **Question:** what does this cost, and per what?
- **Layout:** two columns. Left: assumptions and inputs (headcount by role, loaded rate and its basis, tooling lines, maintenance reserve %, consuming teams, consumers). Right: cost lines (annual people, tooling, reserve, total), support ratio, cost per consuming team, cost per consumer, with a small quarterly trend for each. No ROI figure anywhere on this screen.
- **Data:** `fact_cost_quarterly`.
- **States:** rate not yet agreed with finance (inputs show "provisional" and every output inherits the label).
- **Precedents:** the two-column calculator layout (Supernova) without its output framing; Swarmia investment balance for the per-category idea.

## Screen 6. Event and proof ledger

- **Audience:** sponsor, system team, anyone assembling a deck.
- **Question:** what did the system change about a real event, and how do we know?
- **Layout:** list of proof cards (artifact 07) newest first, filter by event type; each card shows before/after images, last-time and this-time hours with sources, the pessimistic–optimistic saving range, saving class, confounders, quote, definition version; an "open events" section for rows not yet closed, showing the planned capture method.
- **Data:** `event_ledger`, `event_image`, `task_study`, `duplication_ledger`.
- **States:** open event (no after image; shows the plan); estimated baseline (badge "baseline estimated").
- **Precedents:** Uber figure 9; TEI benefit paragraphs with quotes.
- **Wireframe:** `wireframes/06-event-ledger.png`.

## Screen 7. Leading-indicator feed

- **Audience:** system team daily; leads weekly; the executive page shows only a count.
- **Question:** what changed, who is affected, and what do we do about it?
- **Layout:**
  1. Filter chips: all / critical / warning / info; by metric; by team.
  2. Event rows: severity dot, headline ("Button detachment spike, Mobile team"), delta text ("1.8% to 9.4% over 7 days"), since date, the breach action from the metric definition, assignee, resolve control. Rows with `event_class = 'info'` (level changes, releases) never escalate.
  3. Right rail: two-month engagement rollup (this month versus last: office hours, contributions, support, composite, each with a bar and delta) and a "champions and watchlist" pair (top three and bottom three teams by composite).
- **Data:** `feed_events`, `fact_engagement_monthly`.
- **States:** quiet period (feed says "no breaches in N days" rather than being empty); unresolved for more than 14 days (row escalates one severity).
- **Precedents:** Figlytics Action Feed and champions/watchlist pairing (its public screens are demo data); Headway engagement rollup.
- **Wireframe:** `wireframes/07-leading-feed.png`.

## Screen 8. Metric definitions

- **Audience:** everyone; the page every number links to.
- **Question:** what exactly is this number?
- **Layout:** one page per metric from artifact 01, rendered: definition, formula, source systems, exclusions, segmentation, refresh, owner, baseline, target, gaming path, counter-metric, breach rule, version history with effective dates. A pipeline diagram for the production measurement (how the number is produced end to end). A "what changed" log across all definitions.
- **Data:** `dim_metric_definition`.
- **Precedents:** Figlytics weight sliders; Pinterest "how it works"; Uber pipeline diagram.

## Screen 9. Risk posture

- **Audience:** sponsor; risk or compliance partner.
- **Question:** what exposure does the system reduce, and is it trending the right way?
- **Layout:** accessibility score trend per product (on-system versus off-system surfaces), open a11y defects by severity, a key-person panel (critical areas and named backups; unbacked areas flagged), brand-consistency defects trend.
- **Data:** `fact_a11y_pass_release`, `fact_defects_release`; a small manual table for backups.
- **Precedents:** Deque outcome reports and program chart.

## Screen 10. Consumer sentiment

- **Audience:** system team; sponsor quarterly.
- **Question:** what do the people who use it say?
- **Layout:** three tiles (meets my needs, helps me work faster, would recommend) with trend and response rate; self-reported hours saved as a trend labeled "self-reported, soft"; verbatims beside the tiles, filterable by role and team.
- **Data:** `fact_survey_quarterly`, `fact_survey_verbatim` (consented only).
- **States:** response rate under 30% (tiles carry a low-confidence badge).
- **Precedents:** TEI quote rail; the "meets my needs / faster" items.

## Screen 11. Export to deck

- **Audience:** whoever presents.
- **Question:** can I get this month's story without retyping numbers?
- **Layout:** choose occasion (first funding, renewal, defense; artifact 06), period, audience framing (internal-efficiency or customer-value); preview of slides generated from the store with the organization's template; download; a definitions appendix attached automatically; a "numbers as of <timestamp>" stamp on every slide.
- **Data:** all views.
- **Precedents:** Supernova's "download presentation deck" button. No design system in the surveyed corpus ships its own leadership deck; this screen is a recommendation without a captured precedent.

---

## Build order

Screens 8, 5, 1 first (definitions, cost, the one-pager), then 2 and 7 (team view and feed), then 3, 6 (migration, events), then 4, 9, 10, 11. Screen 8 must exist before screen 1 is shown to anyone.

---

## Interaction inventory (the recurring component set)

The eleven screens reuse one bounded set of interactive controls and data views. This inventory enumerates that set once, against the control-state contract (default / hover / focus-visible / active / disabled / loading / error, plus success and selected) and the data-view floor (empty / loading / error / populated), before any of it is built. It is mechanical: it records which states apply by element class and flags every applicable state the specs above do not yet show as `MISSING`. A `MISSING` cell is a flag for the design owner, never a defect verdict; whether it is a gap to design or a deliberate absence is a ruling left to the human gate at the end of this section. The specs above describe content and data states (first period, not instrumented, quiet period); the interaction states of the controls are, by design, not yet specced, which is what most of the flags below record.

### Element census

| # | Element | Class | Provenance | APG pattern (role call is the human's) |
|---|---|---|---|---|
| E1 | Definition / data link | link | from-source | Link (native `<a href>`) |
| E2 | Sort control (by team / product / manager) | composite | from-source | Tabs, or Menu button if it opens a menu |
| E3 | Platform tabs (never averaged) | composite | from-source | Tabs |
| E4 | Period selector | composite | from-source | Listbox / Select (native `<select>`) |
| E5 | Filter chips (severity / metric / team) | selection control | from-source | Toggle buttons (`aria-pressed`), or Tabs if single-select |
| E6 | Quadrant toggle | action | from-source | Button (`aria-pressed`) |
| E7 | Table row expander (to product / route) | composite | from-source | Disclosure (native `<details>/<summary>`) |
| E8 | Resolve control (feed row) | action | from-source | Button |
| E9 | Export / download control (CSV, deck) | action | from-source | Button |
| E10 | Metric tile / headline block | data view | from-source | none (native region) |
| E11 | Team table (rows selectable, expandable) | data view | from-source | Data table (native `<table>`) |
| E12 | Chart / sparkline / migration chart | data view | from-source | none (needs a text or table alternative) |
| E13 | Coverage card grid | data view | from-source | none (card list) |
| E14 | Event feed list | data view | from-source | none (list; rows may be links) |
| E15 | Proof card | data view | from-source | none (figure with images) |
| E16 | Delta chip / severity dot | static | from-source | none (readonly display; `readonly` flag only) |

### State matrix (contract states × control-and-composite elements)

Legend: `shown` = a spec above carries it · `MISSING` = applicable by class, not shown (a flag) · `n/a` = not applicable by class.

| Element | default | hover | focus-visible | active | disabled | loading | error | success | selected |
|---|---|---|---|---|---|---|---|---|---|
| E1 link | shown | MISSING | MISSING | MISSING | n/a | n/a | n/a | n/a | MISSING (if-current) |
| E2 sort | shown | MISSING | MISSING | MISSING | MISSING | n/a | n/a | n/a | MISSING (`aria-selected`) |
| E3 tabs | shown | MISSING | MISSING | MISSING | MISSING | MISSING (if a tab lazy-loads) | MISSING (if async) | n/a | MISSING (`aria-selected`) |
| E4 period selector | shown | MISSING | MISSING | MISSING | MISSING | n/a | n/a | n/a | MISSING (`aria-selected`) |
| E5 filter chips | shown | MISSING | MISSING | MISSING | MISSING | n/a | MISSING (if a required set) | n/a | MISSING (`aria-pressed`) |
| E6 quadrant toggle | shown | MISSING | MISSING | MISSING | MISSING | n/a | n/a | n/a | MISSING (`aria-pressed`) |
| E7 row expander | shown | MISSING | MISSING | MISSING | MISSING | MISSING (rows fetched on expand) | MISSING (if async) | n/a | MISSING (`aria-expanded`) |
| E8 resolve | shown | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | n/a |
| E9 export | shown | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | n/a |

Data views (E10 to E15) carry no hover / active state and are enumerated on the data-view floor below; their one contract-state row is `focus-visible`, which applies wherever a row, card, or point is focusable and is `MISSING` on every data view above that specs selectable or expandable rows (E11 at least). E16 is static: a single `default` state with a `readonly` flag, everything else `n/a`.

### Data-view states (empty / loading / error / populated)

Every data view here is bound to async data, so all four states apply.

| Data view | empty | loading | error | populated |
|---|---|---|---|---|
| E10 metric tile / headline | MISSING | MISSING | MISSING | shown |
| E11 team table | shown ("not instrumented") | MISSING | MISSING | shown |
| E12 chart / sparkline / migration | MISSING | MISSING | MISSING | shown (with "stalled" / "completed" variants) |
| E13 coverage card grid | MISSING | MISSING | MISSING | shown (with "out of scope" / "stale" variants) |
| E14 event feed | shown ("no breaches in N days") | MISSING | MISSING | shown |
| E15 proof card | shown ("open event": shows the plan) | MISSING | MISSING | shown |

The recurring flag: the surface specs its empty and edge-content states with care (first period, not instrumented, quiet period, open event) and omits **loading** and **error** on nearly every async view and async control. That omission is the inventory's main finding for the gate.

### Transitions (candidate state machines, agent-drafted)

| Element | From → To | Trigger | Exit path | Flag |
|---|---|---|---|---|
| E9 export | default → loading | activate | loading → success (file ready) / error (export failed) | `loading-no-error-exit`, `error-no-recovery`: the specs draw only the happy path (screen 11 "download") |
| E8 resolve | default → loading | activate | loading → success (resolved) / error (failed) | `loading-no-error-exit`, `error-no-recovery`: no failure path specced |
| E11 team table | empty/loading/error → populated | data fetch | loading → populated / error → retry | `loading-no-error-exit`: loading and error states unspecced |
| E7 row expander | collapsed → expanded | activate | expanded → collapsed (activate); expanded → loading if rows are fetched | `loading` unspecced when expansion fetches product/route rows |

Every transition above is a candidate the human confirms; the flags are findings, not verdicts.

### Focus, keyboard, gesture

Keyboard is filled from the ARIA APG pattern by element (native element first, the first rule of ARIA). Target-size floor is WCAG 2.2 SC 2.5.8 (24×24 CSS px); 44×44 is the widely recommended comfortable target and the value to prefer on a touch surface.

| Element | Focusable | Keyboard (by APG pattern) | Touch | Target ≥ 24×24 |
|---|---|---|---|---|
| E1 link | yes | Enter activates (native link) | tap | check at build |
| E2 sort | yes | per "Tabs": Arrow keys move, Enter/Space select, Home/End; or per "Menu button" | tap | check |
| E3 tabs | yes | per "Tabs" | tap | check |
| E4 period selector | yes | native `<select>`: Arrow keys, Enter/Space, type-ahead | tap | check |
| E5 filter chips | yes | per toggle button: Space/Enter toggle; per "Tabs" if single-select | tap | check |
| E6 quadrant toggle | yes | Enter/Space toggle | tap | check |
| E7 row expander | yes | native `<details>`: Enter/Space toggle | tap | check |
| E8 resolve | yes | Enter/Space activate | tap | check |
| E9 export | yes | Enter/Space activate | tap | check |
| E11 team table | yes (rows) | native table navigation; roving focus for selectable rows | tap row | check |
| E12 chart | yes (if interactive) | provide a keyboard-reachable data-table or text equivalent (a chart is not operable by pointer alone) | tap point | n/a for the plot; controls check |

Any control that renders under 24×24 is flagged `below-24px`; a hover-only state signal is flagged `hover-only` (touch has no hover). Both are findings for the gate.

### Accessibility hooks per state

From the contract's hook column; the *name* of each control is the accessibility annotation's slot, not this inventory's.

- **loading:** `aria-busy="true"` on the region; a polite live region announces the loading string.
- **error:** `role="alert"` (or a `status` region) on the failure message; `aria-invalid` + `aria-describedby` where the failure is on an input.
- **success:** a polite `status` live region announces completion (a resolve, an export); focus is not stolen.
- **disabled:** `disabled` on native controls, `aria-disabled` where a control must stay focusable; the *reason* it is disabled, where shown, is tooltip or label copy, not a state string.
- **selected / current / expanded:** `aria-selected` (tabs, options), `aria-pressed` (toggle chips, quadrant), `aria-current="page"` (the current period or nav), `aria-expanded` (the row expander).
- **focus-visible:** a visible, non-color-only focus indicator on every focusable element (WCAG 2.2 SC 2.4.7, 2.4.11, 2.4.13).

### Copy slots (empty; filled by the microcopy set below)

The copy-bearing states are loading, error, success, and a data view's empty. Every other state carries no string. The slots are filled as candidates in the next section; nothing here is a final string.

| Element | State | Taxonomy slot | String |
|---|---|---|---|
| E8 resolve | loading / error / success | Loading / Error / Success | (below) |
| E9 export | loading / error / success | Loading / Error / Success | (below) |
| E10 to E15 data views | empty / loading / error | Empty / Loading / Error | (below) |

---

## Microcopy set (candidate strings for every copy-bearing state)

**Generic voice frame (candidate, doubly-candidate mode).** No client voice system is confirmed for this generic kit, so every string below is a candidate twice over: agent-drafted, and written against a voice frame no human has signed. The frame is the kit's own stated conventions: plain and precise; every number carries its date, its method, and a link to its definition; a state string names the next step, not only the condition; no false precision; decision-oriented; no marketing adjectives. Calibration: in-product strings are terse (a cell, a chip, a toast); the executive one-pager is spare. When a real engagement adopts this kit, replace this frame with the client's confirmed voice and re-run.

Doctrine applied per string: an Error names a typed next step (retry / edit / alternative / wait-with-duration / contact) and its condition, or flags what it cannot supply; a Loading string names the object coming and never says "please wait," and any duration ships only as a held claim; an Empty string names what would be here and the one action that fills it; a Success string names what is done and what is now possible.

| Element | State | Slot | Candidate string [candidate: agent-drafted] | Constraints | Doctrine | Lineage |
|---|---|---|---|---|---|---|
| E10 metric tile | empty | Empty | "No data for {metric} yet. It appears after the first {period} of measurement." | tile · {metric}, {period} | action/condition named ✓ | new |
| E10 metric tile | loading | Loading | "Loading {metric}." | tile · ≤24ch · {metric} | object named ✓ · no duration ✓ | new |
| E10 metric tile | error | Error | "{metric} didn't load: {condition}. Retry." ⚠ condition-unsupplied | tile · {metric}, {condition}: held | next-step: retry ✓ · condition: NOT on the row | new |
| E11 team table | empty | Empty | "This team isn't instrumented yet, so there's no coverage to show." | panel | condition: from spec ("no coverage data") ✓ | revised-from: "not instrumented" |
| E11 team table | loading | Loading | "Loading teams." | panel · ≤24ch | object named ✓ | new |
| E11 team table | error | Error | "The team view didn't load: {condition}. Retry." ⚠ condition-unsupplied | banner · {condition}: held | next-step: retry ✓ | new |
| E12 chart | empty | Empty | "No {series} data for this range yet." | panel · {series} | condition named ✓ | new |
| E12 chart | loading | Loading | "Loading the {chart}." | panel · {chart} | object named ✓ | new |
| E12 chart | error | Error | "The chart didn't load: {condition}. Retry." ⚠ condition-unsupplied | panel · {condition}: held | next-step: retry ✓ | new |
| E13 coverage grid | empty | Empty | "No surfaces match these filters. Clear a filter to see more." | panel | next-step: edit ✓ · condition: the filter set ✓ | new |
| E13 coverage grid | loading | Loading | "Loading surfaces." | panel · ≤24ch | object named ✓ | new |
| E13 coverage grid | error | Error | "Surfaces didn't load: {condition}. Retry." ⚠ condition-unsupplied | panel · {condition}: held | next-step: retry ✓ | new |
| E14 event feed | empty | Empty | "No breaches in the last {count} days." | panel · {count}: sing/pl ("1 day" / "{count} days") | condition: from spec ("quiet period") ✓ | revised-from: "no breaches in N days" |
| E14 event feed | loading | Loading | "Loading the feed." | panel · ≤24ch | object named ✓ | new |
| E14 event feed | error | Error | "The feed didn't load: {condition}. Retry." ⚠ condition-unsupplied | banner · {condition}: held | next-step: retry ✓ | new |
| E15 proof card | empty | Empty | "Capture planned: {method}. The after image lands when the event closes." | card · {method} | condition/method: from spec ("shows the plan") ✓ | revised-from: "open event" |
| E15 proof card | loading | Loading | "Loading the proof." | card · ≤24ch | object named ✓ | new |
| E15 proof card | error | Error | "The proof card didn't load: {condition}. Retry." ⚠ condition-unsupplied | card · {condition}: held | next-step: retry ✓ | new |
| E9 export | loading | Loading | "Preparing your {export}." | toast · {export} | object named ✓ · no duration ✓ | new |
| E9 export | success | Success | "{export} ready. The download starts on its own." | toast · {export} | done + next possible ✓ | new |
| E9 export | error | Error | "The {export} didn't finish: {condition}. Try again." ⚠ condition-unsupplied | toast · {export}, {condition}: held | next-step: retry ✓ | new |
| E8 resolve | loading | Loading | "Resolving." | inline · ≤16ch | object named ✓ | new |
| E8 resolve | success | Success | "Marked resolved." | inline · announced | done stated ✓ | new |
| E8 resolve | error | Error | ⚠ FLAG next-step-unsupplied: the recovery path for a failed resolve is undecided (see open questions) | | next step: NOT drafted (undecided path) | (none) |

Legend: ✓ = doctrine part met · ⚠ = a flag for the human · a state the specs mark `no copy` is omitted here, not invented.

### Flags (findings for the human, never verdicts)

- `condition-unsupplied` (E10, E11, E12, E13, E14, E15, E9): none of these async views or the export supplies the failure trigger, so each Error string holds `{condition}` and names no cause. Supplying the real triggers is a product decision.
- `next-step-unsupplied` (E8 resolve, error): the specs do not define what happens when a resolve fails; no typed step is invented.
- No `spinner-where-skeleton` flag is raised here because the specs do not commit to a spinner-versus-skeleton choice on the structured views; that choice is the design's, and the loading strings above fit either.

### Claim / SLA guardrail

Empty. No string above asserts an SLA, a guarantee, a timeframe, an uptime figure, or a price. The one place a claim would enter is a Loading string with a duration ("back in a few minutes"); none is asserted, because none is measured. The `{condition}` variables are held pending the product's real error triggers, which is a doctrine flag, not a claim.

### Candidate glossary (terms and conflicts; no rulings)

| Term | Where | Candidate definition | Conflict seen |
|---|---|---|---|
| coverage | E10, E11, E13, screens 1–4 | the share of what users see that comes from the system | used at two grains: the headline metric (M1) and a per-surface percentage |
| surface | E13, overlay | one screen, page, or route of the product | (none) |
| one-off | E13, overlay | an element that looks like the system but is not from it | (none) |
| breach | E14, screens 1, 7 | a metric crossing its defined threshold | (none) |

### Open questions and near-misses

**Open questions (questions, not judgments):**
- What is the real failure trigger for each async view and for the export, so the held `{condition}` variables can be filled?
- When a resolve fails, what is the recovery path (retry in place, reassign, escalate)? The Error slot is a flag until this is decided.
- Which of the `MISSING` control states are gaps to design and which are deliberate (a link may not need a specced disabled state)? That is the gate's ruling, per element.
- Does the surface commit to a skeleton or a spinner on its structured views, so the Loading strings can be tuned to it?

**Near-misses and unchecked territory (traces, no verdicts):**
- Almost flagged: the migration "stalled" and "completed" states (screen 3) and the "unowned" owner cell (screen 2) read like states but are populated-content variants, so they carry content copy, not a state string; they are noted, not drafted.
- Considered, set aside: a disabled-reason string for E5/E6 when a filter or toggle is unavailable; the specs do not yet describe a disabled condition, so no string is drafted.

### The judgment slots (empty by construction)

**⛔ Which interactions matter, NEEDS HUMAN.** Which controls and transitions get design attention on each screen: ____________________

**⛔ Deliberate-absence rulings, NEEDS HUMAN.** Each `MISSING` flag above is either a gap to design or a deliberate absence. Rule on each: ____________________

**⛔ Which copy ships, tone calls, terminology rulings, NEEDS HUMAN.** Per string: accept, rewrite, or ask for alternates; resolve each ⚠ flag in the confirmed voice; rule on the "coverage" grain conflict: ____________________

**Named gate.** Sign-off owner (design lead / content lead): ____________________  Date: ______
No state is declared complete or deliberately absent, and no string ships, until this line is signed by a human.
