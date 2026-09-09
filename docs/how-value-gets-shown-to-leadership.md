---
title: How design-system value gets shown to leadership
subtitle: A visual survey of dashboards, calculators, reports, and decks, with the UI patterns worth borrowing for a value-reporting surface
date: 2026-09-01
status: survey structured as a competitive teardown (dated evidence ledger, heuristic presence pass, pattern matrix as-of); pattern library and screen inventory drafted
classification: unclassified
companion_to:
  - docs/making-the-case-for-a-design-system.md (the field guide)
  - kit/ (the artifacts that act on both documents)
---

# How design-system value gets shown to leadership

*The field guide answered what leadership looks for and how to make the evidence retrievable. This one collects how that evidence is actually rendered: the dashboards, calculators, one-page reports, and decks that exist today, in design systems and in the adjacent fields that solved the same problem earlier. Except where marked as described from secondary sources, every example below was captured this session from a public page (headless Chromium, 1440px viewport, scroll-through for lazy images); the source URLs are listed in `kit/SOURCES.md`. The point is a pattern library and a screen inventory for a future UI, not a tool comparison.*

> **Read this as a competitive teardown, not a leaderboard.** Sections 1 through 8 are the descriptive survey; section 9 restates the same evidence under a teardown discipline so the reading stays honest as the field moves. Three rules govern that discipline. Every presence claim cites a **dated** capture; an example described only from a secondary summary backs no presence claim (it is `UNKNOWN`, never confirmed). A pattern a capture did not confirm present is `UNKNOWN`, never read as absent, because a targeted survey capture is not a full presence sweep. And the three calls a teardown must not make for you, **how severe a gap is, what it means for your context, and what to copy**, are left as empty slots behind a named sign-off. The "worth borrowing" notes throughout sections 1 through 7 are the survey author's candidate reads, offered as input to that gated decision, not a ratified verdict.

---

## 0. What the survey says in one screen

If the future surface had to be one screen, the corpus converges on this composition, and every element of it has a live precedent:

1. **One headline number with a ring or a trend, never both as decoration.** Uber's proof card (a "61% Base score" ring beside "59 improved screens"), Preply's two big percentages in Datadog, Luro's "91% design system adoption" chip. The number is coverage of what users see, or hours returned, depending on the audience.
2. **A short row of counterbalanced tiles with sparklines and a benchmark chip.** DX Core 4 is the cleanest precedent: four tiles (effectiveness, speed, quality, impact), sparklines on each and a "vs industry P50" chip on the active tile. Headway's adoption report and Figlytics' header strip do a design-system version of the tile row, without the sparkline or the benchmark.
3. **A team table where every number breaks down by consuming team, product, or route.** Pinterest FigStats, Headway's team/repo breakdown, Mews by product and route (§ 2.10), Uber sorted by flow or by manager. This is the element that turns the report from a plea into a product-team conversation.
4. **One migration chart.** A rising system line against a falling legacy line (Productboard's typography chart, Luro's product cards chart), or the same story as composition over time (Omlet's stacked area, Segment's stacked bars, IBM.com's two-date bars). The most legible "it is working" picture in the corpus.
5. **A proof story with a before/after and a number.** Uber's figure 9. TEI's quantified-benefits paragraphs with an interviewee quote beside them.
6. **A feed of what changed and what needs a decision.** Figlytics' Action Feed (detachment spike, adoption regression, stale publish) is the only captured design-system product doing this (its public screens are demo data); it is what makes the surface a leading indicator rather than a scoreboard.
7. **A visible method.** Figlytics shows the weights of its health score as sliders (with the caveat in § 1 that its demo ring and its weight sliders do not list the same components). Uber publishes the pipeline diagram. TEI states the composite organization and the risk adjustment. Leadership trusts a number more when the page shows where it came from.
8. **The ask, as a decision.** No captured dashboard carries this; TEI's synopsis sentence and the field guide's one-page report do. It is the element a dashboard cannot supply and a report must.

Where the numbers lived: Preply, Productboard, IBM.com, Mews, and athenahealth used a tool the organization already opened (Datadog, Looker, Google Analytics, New Relic, Tableau); Uber and Pinterest built standalone dashboards on their own pipelines; Headway ran on a spreadsheet. All refresh automatically and break every number down by consuming team.

Everything else in this document is evidence for those eight, plus what to avoid.

---

## 1. Design-system analytics products

Vendor UIs. Useful for interaction patterns and for what the market has decided is table stakes; less useful as leadership surfaces, because most of them speak to the design-system team.

| Product | What the screen shows | Worth borrowing | Watch out for |
|---|---|---|---|
| **Figlytics** (Figma REST API dashboard) | Header strip: health grade A/87, adoption 84%, retention 91%, alerts, champions, watchlist, teams. Below it an Action Feed of ranked events with severity, a delta, and a timestamp ("Button detachment spike, Mobile team, 1.8% to 9.4% over 7 days"; "Adoption regression, Web Platform, minus 12%"). A second screen exposes the health-score formula as five weighted sliders that must total 100. | The feed. Events phrased as *what happened, to whom, by how much, since when*. The transparent weights. The "champions and watchlist" pairing (who to celebrate, who to call). | The public screens are demo data ("BLZ Corp") and the product needs the Enterprise-tier API. The demo is internally inconsistent: the health ring decomposes into adoption, retention, coverage, freshness, while the weight sliders list adoption volume, retention, category coverage, momentum, regularity. A single composite grade invites gaming and hides the counter-metric; keep the components visible next to the grade, and make sure they are the same components. |
| **Luro** (production crawler plus Figma and Storybook) | Product-level page with a line chart (system adoption rising, legacy falling) over a per-component table: pages %, instances, legacy pages %, legacy instances, each with a small inline bar. A second card pairs "component adoption over time" with per-page overall-score rings under a "performance and accessibility" heading. | Inline bars inside table cells; pairing adoption with page-level scores so the system is read as quality, not only reuse. | Marketing mock data; the real product's per-page crawl is the thing to study. |
| **Omlet** (React/React Native code scans) | Stacked area of design-system versus legacy usage over time with a one-line callout beneath ("Legacy component usage decreased 2% over the last 2 weeks"); saved dashboards; a component detail page with a dependency tree and where-used by project; legacy usage by project as horizontal bars. | The one-sentence plain-language takeaway under a chart. Dependency tree as impact analysis before deprecation. Per-project scoreboard (Optimizely used it that way, per Zeplin's write-up). | Static scans cannot see whether the import renders; label it as such. |
| **Figma Library Analytics** (built in) | Insertions line with a compare-to-library overlay; "Top teams" ranked with % share of inserts; component and variable statistics tables with instances, inserts (30 days), detaches (30 days) and a drill-down chevron (the styles table exists but was not in the capture). | The three-column statistic (total, recent inserts, recent detaches) is a compact adoption-plus-counter-metric row. Compare-with-library overlay for migrations between library versions. | These are counts, not coverage. Pinterest's article is the canonical critique: 27,056 insertions of a button is not a health signal without a denominator. |
| **Segment Evergreen adoption dashboard** (2018, in-house but archetypal) | Donut of global adoption split by library version, week-over-week stacked bars, a component treemap coloured by library. | The treemap: area equals usage, colour equals source library. Fastest way to show "how much of the UI is on the system and where the legacy pockets are." | Donuts of four-plus slices read poorly; the treemap carries the message on its own. |
| **Design System Adoption plugin** (David Vera, Figma community) | A one-sentence verdict with the number highlighted ("With a 48.17% adoption rate, your design system adoption is on the lower side"), then a four-row breakdown (local elements, main library, icons and text styles, unknown library) with counts and percent, copy-table and export-CSV buttons. | The verdict sentence. A number with an adjective and a next step is more legible to a non-specialist than a gauge. | File-level scan, not organization-level. |

Also in this class but not captured: Supernova and zeroheight analytics (documentation-traffic and component-usage panels inside the docs platform), Knapsack, Specify. Their pattern is the same: usage tables inside the documentation product.

---

## 2. In-house dashboards and instruments

The teams that built their own. These are the leadership-facing surfaces, and the ones with the most transferable structure. Where the published screen is a mock or a placeholder, it says so.

### 2.1 Uber, Base Adoption Dashboard and Base Counter (2024)

The most complete system in the corpus, and the one that most resembles a product. The published dashboard screens are a shell with placeholder values ("XY%"); the structure is real, the numbers are not.

- **Dashboard shell.** Tabs per app (Rider, Driver, Eats) and per platform (iOS, Android). An Overview row with quarterly bars per app and an H1 target chip, beside a "current leaderboard" (a single horizontal bar split Driver / Eats / Rider). A sort control: by Flow, by Engineering Manager, by Design Manager. That control is the whole accountability model in one widget.
- **Flow section.** Per flow (for example "Connect"), the design manager is named, a "Base adoption average" card shows this month, last month, delta, and a quarterly mini-bar; beside it an accessibility issues card (fixed / total, critical screens). Then per-screen cards: a screenshot, the screen name, Base adoption % with a delta chip, a11y issue count with severity chips.
- **The eye.** Base Counter, an on-device overlay that outlines Base components in green and one-offs in red. The team's phrase: the eye for everyone. It turns an abstract percentage into something a product manager can see on their own phone.
- **The ear.** A daily pipeline: analytics events from all internal testers plus screenshot-based E2E analysis, aggregated by mode across A/B variants, scored per screen, written to a score DB, surfaced on the dashboard, with automated Jira tickets to the owning managers on degradation.
- **The proof card.** Before/after screenshots beside two numbers: "59 improved screens" and a "61% Base score" ring, dated (June 2024, Rider iOS). Then a three-panel strip: track baseline, degradation detected (score minus 5%), the notified team resolved it.
- **The method figure.** A swimlane diagram of the pipeline is published alongside the numbers.

Borrow: the sort-by-owner control, the per-screen card with screenshot plus two numbers plus deltas, the proof card, the overlay as a public "eye," and the practice of showing the pipeline next to the result. Uber's reported benefits (3x faster development, 4x fewer visual-parity issues, 50% less code) are internal research without a published method; grade C, use the *screens*, not the numbers.

### 2.2 Pinterest, FigStats (2023)

- **At a glance** header tiles: Gestalt adoption 22.99 with a delta arrow, fill-style match 46.1, text-style match 62.69, number of Figma files, number of handoff pages.
- **Team table**: Gestalt adoption %, matching fill style %, matching text style %, per team, expandable rows.
- **Per handoff page**: a donut of layer composition (Gestalt layers, text layers, other) with a breakdown panel (counts) and a "top editors" list.
- A leaderboard section in the left nav.

Borrow: the three-metric row that pairs component adoption with style adherence (a coverage number with two counter-metrics built in), and the handoff-page scope rule (only production-intended pages count). The donut is acceptable here because it is one page's composition, not a comparison.

### 2.3 Preply, visual coverage in Datadog (2025)

Two very large numbers (DS coverage web 71.43%, app 41.77%); beside them a column of three period deltas (change over 1 week, 1 month, 3 months); a "coverage by team" horizontal bar list; a "coverage over time" line; and a per-team "change over 4 weeks" column of small red/green deltas. Built as an ordinary Datadog dashboard, refreshed from 300,000-plus daily measurements in production.

Borrow: the decision to live inside the observability tool engineering leadership already opens, the by-team bars directly under the headline, and the pixel-weighted definition (a primary button counts more than a layout container). This is the closest existing thing to the field guide's executive view.

### 2.4 Productboard, Looker (2021)

Stacked percent bars for icon and typography adoption (healthy versus deprecated, green versus red), an area chart of deprecated icons migrating week by week, and the one chart worth copying wholesale: **custom font definitions (a flat line) against design-system text components (a rising line)** by generated week. A community-contribution stacked bar by contribution type completes it. Data comes from a daily GitLab job running react-scanner, ESLint and stylelint across 200-plus projects into Looker, scoped by project or team.

Borrow: the migration chart, and the contribution chart as a leading indicator shown on the same page as adoption.

### 2.5 Headway, adoption report and engagement rollup (2026)

- **Adoption report**: five tiles (adoption 65%, most popular package, average diversity 0.3, heavy users 3 repos, active teams 7/9), then a team and repository table with five columns per row: adoption %, plus four signals (direct usage %, total usage %, token opportunity %, arbitrary opportunity %).
- **Engagement rollup**: May and June cards side by side, three rows (office hours participation, contribution participation, support participation) with a bar and a delta chip, and a total engagement row; a second card of three tiles (average engagement score, three-month rolling average, total contributions).
- **The quadrant**: adoption × engagement, four labelled cells (healthy partners, at risk, emerging, unreached or resistant).

Borrow: two months side by side as the default comparison, the "opportunity" framing for the anti-signals (arbitrary values as a percentage of opportunity rather than a debt count), and the quadrant as a per-team diagnostic. Headway's own note: a spreadsheet and a monthly habit, no platform required.

### 2.6 IBM.com Carbon, one chart (2021)

Two horizontal 100% bars, one per date (week of 2021-02-15 and week of 2021-11-22), segmented by design system (Carbon, Northstar, other), labelled with 6.2% and 44.8%. Source: Google Analytics page views.

Borrow: this is the model for a board slide. Two dates, one unit the business already uses, three colours, two labels, and nothing else on the chart.

### 2.7 Onfido Castor, Badoo Cosmos, Hotmart (via Supernova's roundup)

- **Onfido**: colour-token usage by project as absolute and percentage stacked bars, a "totals" column with a **Target marker** drawn across the bar, component usage ranked, component types by project. Borrow the target marker on the total.
- **Badoo**: a spreadsheet coverage model, components weighted by complexity points, with a small coverage summary giving optimistic and pessimistic percentages. Borrow the two-column optimistic/pessimistic habit.
- **Hotmart**: an OKR sheet in four columns (DS development, product coverage, team operation, building a community), each with an objective and five graded key results. Borrow as the *planning* artifact that sits behind the dashboard; André Rolla's reported 26.4 to 8.4 hours per screen is a self-reported internal experiment (grade C).

### 2.8 Delivery Hero Marshmallow (via portfolio and secondary summaries; page not capturable)

Adoption tiers named Bronze (tokens), Silver (components), Gold (voice, micro-interactions, haptics), Platinum (motion, dark theme, voice UI); a "Discovery Squad dashboard" that shows each team's progress toward the next tier; posters of the tiers on office walls; celebration rituals. Reported outcomes (design debt down about 20% month over month, front-end effort down about 40% on new features) are self-reported.

Borrow: levels with names, progress-to-next-level as the per-team visual, and the physical poster as a reminder that the surface does not have to be a screen.

### 2.9 Nathan Curtis, the adoption scorecard (2017, via summaries; article unreachable)

Products as rows grouped by priority, adoption levels as columns, status and notes to the right; improvement shown as movement left to right, or by colour and arrows; placed as the front matter of periodic updates. This is the oldest and simplest leadership surface in the corpus and still the right one for a first-funding or federated context.

### 2.10 Mews, adoption in New Relic (2025; no dashboard image published)

A DOM-element ratio computed from build-time markers, sampled every ten seconds in production with batching, reported in New Relic by product, team, and route. The article publishes the method and the numbers (53% and 60% on two products, a third growing about 5% a month) but no dashboard screenshot, so it has no captured screen here. It is the precedent for "reuse the observability tool the organization already has" on the engineering side, as Preply is with Datadog.

---

## 3. Adjacent fields and executive storytelling

Fields that had to explain an internal platform to a CFO before design systems did.

| Source | Screen | What it teaches |
|---|---|---|
| **Forrester TEI** (Forrester Decisions example) | Four hexagon tiles (ROI 259%, Benefits PV $2.54M, NPV $1.83M, initiative success 26% more likely) above a two-column layout: quantified benefits as bold-lead paragraphs on the left, interviewee quotes in the right rail; then a synopsis sentence; then benefits as a ranked horizontal bar chart in dollars. | The executive-summary grammar: four headline metrics, benefits by category with the method in the paragraph, costs stated, a one-sentence synopsis, then the chart. Quotes placed *beside* numbers, not instead of them. The structure is reusable; the numbers are the vendor's. |
| **DX Core 4** | Four tiles (effectiveness DXI 64, speed 2.8 PRs/week, quality 16.1% change fail, impact 55.3% innovation ratio), sparklines on each and a "vs industry P50" chip on the active tile; a team table with contributors, average, vs P50, trend. | Counterbalanced metrics as a fixed row, so no single number can be optimised alone. The benchmark chip. Team rows with a trend column. |
| **Swarmia, investment balance** | Stacked bars of engineering time by category (new things, improvements, productivity, keep-the-lights-on) by month, with FTE and % toggles. | Time allocation as the CFO's native unit. A design system's "capacity returned" claim would be believed if it showed up here as a shift between categories. |
| **Jellyfish, allocations** | Monthly stacked bars (roadmap, unplanned, infrastructure, support, other). Positioned for finance reporting (the vendor's term is DevFinOps). | Same lesson; the category names are the ones finance already recognises. |
| **Deque axe Monitor, outcome reports** | Headline tiles with delta arrows (issues, score), a score-trend line, per product; an "Accessibility Program" column chart across the whole SDLC. | Risk posture as a trend line. The accessibility ledger of the field guide already has a mature visual language; reuse it rather than inventing one. |
| **Supernova ROI calculator** | Left column: sliders and inputs (product designers 10, system designers 2, salary $100k; developers 15 / 1 / $120k; a design-to-code toggle). Right column: savings cards (design savings/yr $300k, developer savings/yr $360k, deployment savings, total five-year $2.76M, ROI 736%). A "download presentation deck" button below. | The two-column calculator layout is the right shape for a cost-of-not tool: assumptions visible on the left, outputs on the right, and a deck export. The output framing (736% ROI) is the anti-pattern the field guide warns about; the *layout* is worth keeping. |
| **Knapsack ROI page** | Three stat cards (30% QA time, 20% efficiency, 15% speed to market), slider calculator, scenario presets (10 people / 1 product, 25 / 4, 100 / 10). | Scenario presets lower the effort to a first estimate. The stat cards are unsourced and should not be imitated. |
| **Executive scorecard literature** (not captured; see field guide § 2.7) | Metric, value, target, variance, sparkline, owner, "what we do if this breaches." | The row format the field guide already specifies. |

---

## 4. The pattern library

Extracted across all three sheets. Each pattern names its best precedent and the failure it prevents. The presence of each pattern per product is recorded, with dated citations, in the pattern matrix of section 9; the "prevents" note and any "borrow" read here is a candidate call for the gated adopt/adapt/avoid decision, not a ruling.

### 4.1 Composition patterns

- **Headline, tiles, table, chart, story, feed, method, ask.** The order that appears across the strongest examples (Uber, Preply, Headway, Figlytics, TEI). Headline number with trend; three to five counterbalanced tiles; per-team table; one migration chart; one proof story; the event feed; the method; the decision. Prevents the forty-metric dashboard. The same eight as § 0.
- **Two periods side by side.** Headway's May/June cards; IBM.com's two-date bars. Prevents the snapshot problem: leadership sees a change, not a state.
- **Executive layer over team layer.** DX (organization dashboard versus group dashboard), Uber (overview versus flow versus screen), Pinterest (org, team, file). Same data, three altitudes, each a click apart. Prevents the "design-team tool nobody else opens" failure.
- **The method beside the number.** Figlytics' weight sliders, Uber's pipeline diagram, TEI's composite-organization paragraph, Pinterest's "how it works" nav item. Prevents the black-box discount.

### 4.2 Metric-display patterns

- **Number plus adjective plus next step.** The Figma plugin's verdict sentence; Omlet's callout under the chart. A non-specialist reads a sentence faster than a gauge.
- **Ring for a bounded percentage, sparkline for a trend, never a gauge.** Uber's 61% ring, Luro's page rings, DX sparklines. Gauges spend space on a dial that carries no information.
- **Benchmark chip.** DX's "vs industry P50." For a design system, the honest benchmark is the organization's own baseline or the best-performing internal team, not an external number (see the field guide's provenance table).
- **Delta chip with direction and colour.** Present in nearly every capture. Keep the colour semantics fixed: green is "toward target," which for detachments means down.
- **Target marker on a stacked total.** Onfido's totals bar. Turns a status into a distance-to-goal.
- **Optimistic / pessimistic pair.** Badoo's coverage summary; Figr's guidance. Prevents false precision and matches how finance reads estimates.

### 4.3 Comparison and breakdown patterns

- **System line up, legacy line down.** Productboard and Luro. The migration chart. One chart, two lines, no third series. (Omlet's stacked area and Segment's stacked bars tell the same story as composition; see the treemap pattern below.)
- **Treemap coloured by source.** Segment Evergreen. Area is usage, colour is library. Best single picture of "how much of the product is on the system."
- **Per-team horizontal bars under the headline.** Preply, Omlet (legacy by project). The team ranking is the conversation starter with product leads.
- **Table rows with inline bars and multiple signals.** Luro (pages %, instances, legacy), Headway (adoption, direct, total, token opportunity, arbitrary opportunity), Pinterest (adoption, fill match, text match). Three to five columns, each a different signal, so a team cannot look good on one and hide on another.
- **Sort by owner.** Uber's Flow / Engineering Manager / Design Manager toggle. Makes accountability a UI affordance.
- **Quadrant.** Headway's adoption × engagement. A diagnostic that tells the system team *what to do* for each cell, not a ranking.
- **Levels with names and progress to the next.** Delivery Hero tiers, Curtis's scorecard columns, and in platform engineering Cortex's bronze/silver/gold scorecards (OpsLevel's levels are configurable and unnamed by default). Movement between levels is more legible to executives than a percentage change.

### 4.4 Evidence patterns

- **Proof card.** Uber's figure 9: before/after screenshots, two numbers, a date. The field guide's "one proof story," rendered.
- **Quote beside the number.** TEI's right rail. An interviewee sentence next to the quantified benefit. Works for internal consumer-survey verbatims next to the satisfaction metric.
- **Event feed.** Figlytics. What changed, who is affected, by how much, since when, with severity. This is the leading-indicator layer made visible, and the natural home for the "what we do if this breaches" line.
- **The overlay as public proof.** Uber's Base Counter, Onfido's colour-coded overlays, Productboard's "everything green is imported from a design system" screenshots. A picture of the actual product with system parts highlighted needs no legend, which is why this document treats it as the most persuasive artifact for a mixed audience; that is an inference from the captures, not a claim any of the sources make.
- **Pipeline diagram.** Uber publishes the swimlane once and every number can point back to it.

### 4.5 Anti-patterns seen in the corpus

- **A composite grade with hidden weights.** Health scores are attractive on a slide and fragile under questioning; if used, show the components and let the weights be inspected (Figlytics does; most do not).
- **Vendor benchmark cards.** Knapsack's 30/20/15, Supernova's 736%. Round, unsourced, and they read as marketing even when the underlying tool is good. The field guide's provenance table exists to keep these out of a client-facing surface.
- **Donuts with many slices, and gauges.** Segment's four-slice donut and every ROI calculator's dial. Replace with a treemap or a single bar.
- **Insertion and instance counts presented as adoption.** Figma's default tables. Always divide by a denominator or pair with detachments.
- **A dashboard that only the system team opens.** Every product in § 1 defaults to this. Among the in-house examples, Preply, Productboard, IBM.com, Mews, and athenahealth put the numbers in a tool the organization already used (Datadog, Looker, Google Analytics, New Relic, Tableau); Uber and Pinterest built standalone dashboards but wired them to owners, leaderboards, and ticketing so that other teams had to open them; Headway ran on a spreadsheet. The failure is not "standalone," it is "unvisited."

---

## 5. Presentations and reports (the deck layer)

The screens above are the instrument. The deck is what the instrument feeds. What the corpus shows about the deck:

- **The TEI executive summary is the reusable skeleton**: four headline metrics, quantified benefits by category with the method in the paragraph, unquantified benefits named, costs, a synopsis sentence, a ranked benefits bar chart, then the customer-journey narrative and the financial-summary table. Strip the vendor numbers; keep the order.
- **The Hotmart OKR sheet is the planning slide**: four objectives across the top, five graded key results down each column. It answers "what does success look like next quarter" in one view.
- **Curtis's adoption scorecard is the status slide** for a federated or early system: products by priority as rows, levels as columns, arrows for movement.
- **IBM.com's two-bar chart is the board slide**: two dates, one corporate unit, three colours.
- **Uber's proof card is the story slide**: before/after screenshots, two numbers, a date.
- **No design system in the corpus ships its own leadership deck template.** (An earlier draft attributed one to Shopify Polaris; on inspection that was a listing site's own promotional template, not a Polaris artifact.) Treating the deck as a system artifact remains a recommendation without a captured precedent.
- **Figma's Design Executive Council report** (summary post dated January 2026; the report's own date is not stated) shows the current executive framing: design systems tied to customer metrics (Freshworks' reported 28% customer-service cost reduction; SAP's board-level OKRs and a million survey data points; Grammarly's 25% of the work week, used to trade headcount for further investment). These are company self-reports relayed by a vendor (grade C), but the *framing* (customer health metrics over productivity) is where the executive conversation has moved.

---

## 6. A screen inventory for a future value-reporting UI

Derived from the field guide's structure (Ledger 1 cost, Ledger 2 hours, Ledger 3 outcomes and quality, the leading indicators, the definitions contract, the one-page report) and the precedents above. Each screen names its precedent so the design starts from something real; three screens have no design-system precedent in the corpus and say so.

| # | Screen | Purpose | Primary precedent(s) | Key elements |
|---|---|---|---|---|
| 1 | **Executive one-pager** | The monthly page leadership actually reads | TEI executive summary; DX Core 4 tiles; Preply headline | Headline number with baseline → now → target and a six-period trend; four counterbalanced tiles in the scorecard row format (name, value, target, variance, sparkline, owner); one proof card; "what we are not counting" list; one risk line; the decision box |
| 2 | **Team view** | Where every number breaks down by consuming team, product, route, platform | Pinterest team table; Headway team/repo table; Uber sort-by-owner | Rows with three to five signals and inline bars; sort by team, product, engineering manager, design manager; quadrant toggle (adoption × engagement); levels with progress-to-next |
| 3 | **Migration chart** | The single "it is working" picture | Productboard typography chart; Omlet stacked area; Segment treemap | System line up, legacy line down; a treemap alternative coloured by source; per-platform tabs, never averaged |
| 4 | **Coverage explorer** | Where the system is and is not, in the product | Preply by team and page; Uber per-screen cards; Luro per-page scores | Per-page or per-screen cards with a screenshot, coverage %, delta, a11y issues; overlay toggle to view the highlighted product |
| 5 | **Cost ledger** | Ledger 1 (cost) stated first | Supernova calculator layout; Swarmia investment balance | Two-column: assumptions and inputs left (headcount, loaded rate, tooling, maintenance %), cost lines right; support ratio; cost per consuming team; no ROI dial |
| 6 | **Event and proof ledger** | Ledger 2 (hours): natural experiments, kept as a record | Uber proof card; TEI benefit paragraphs with quotes | One card per event (rebrand, theme, remediation, migration): hours last time, hours this time, method, before/after images, optimistic/pessimistic pair, a quote |
| 7 | **Leading-indicator feed** | Engagement, contribution, sponsor participation, release predictability, as events | Figlytics Action Feed; Headway engagement rollup | Ranked events with severity, who, delta, since when; two-month side-by-side rollup; "what we do if this breaches" per metric |
| 8 | **Metric definitions** | The contract, public and versioned | Figlytics weight sliders; Pinterest "how it works"; Uber pipeline diagram | One page per metric: definition, formula, source, exclusions, refresh, owner, gaming path, counter-metric, version; the pipeline diagram |
| 9 | **Risk posture** | Ledger 3 (outcomes): accessibility conformance, key-person dependency, brand consistency, as trends | Deque outcome reports and program chart (no design-system precedent captured) | Score trend per product; issues by severity; named backups per critical area |
| 10 | **Consumer sentiment** | Ledger 3 (outcomes): the system's own NPS and verbatims | TEI quote rail for the layout; the survey items come from the field guide (no design-system precedent captured) | Quarterly survey tiles (meets needs, faster, recommend) with trend; verbatims beside the numbers |
| 11 | **Export to deck** | The monthly and quarterly narrative generated from the same data | Supernova's "download presentation deck" button (no design-system precedent captured) | One-click one-pager and quarterly deck in the organization's template, with the definitions appendix attached |

Two constraints carried over from the field guide: screens 1, 2, and 3 should be embeddable in the organization's own BI tool (five of the in-house examples lived there; the two standalone builds compensated with owners, leaderboards, and ticketing), and screen 8 must exist before screen 1 is shown to anyone.

---

## 7. Design notes for whoever builds it

- **Default to the organization's tool, not a new one.** The product surface is a set of well-defined tables and one embeddable one-pager. A standalone app is the fallback; if you build one, do what Uber and Pinterest did and give every number an owner, a leaderboard, and a path into the ticketing system, so it is visited.
- **Fixed colour semantics.** System versus legacy uses two hues throughout; deltas use direction, not only colour; severity uses the same three levels as the organization's incident tooling.
- **Rings and sparklines only.** No gauges, no multi-slice donuts. Bars for comparisons, lines for time, treemap for composition.
- **Every number carries its date and its source in the interface**, in small type, the way IBM.com's chart carries "Google Analytics" in its title.
- **The proof card is a first-class object**, not a slide someone assembles. It has a template, a date, and a place in the ledger.
- **The overlay is part of the product.** Uber's green/red counter let anyone see the number on their own screen; this document's inference is that it did more for adoption than the dashboard, which Uber's article does not claim directly. A Storybook addon, a browser bookmarklet, or a dev-mode toggle that highlights system versus non-system elements is worth building before the dashboard is pretty.
- **Ship the deck exporter early.** The report will be presented whether or not the UI is ready; generating it from the same tables prevents the numbers on the slide from drifting away from the numbers on the page.

---

## 8. What this survey could not capture

- Delivery Hero's Discovery Squad dashboard (portfolio page is JavaScript-rendered and returned no content), Nathan Curtis's adoption scorecard and OKR article, Cristiano Rastelli's Badoo git-history visualisations, Deliveroo's health article, and André Rolla's Hotmart write-up were all unreachable (Medium and eightshapes.com refuse automated fetches). Their descriptions here come from secondary summaries and should be checked against the originals before any of them is quoted or redrawn.
- Cortex's product page returned a 404 (its docs, which name bronze/silver/gold, are reachable); OpsLevel's docs rendered without images. The scorecard pattern is described from documentation text.
- The Polaris deck-template claim in an earlier draft was wrong (a listing site's own template); it has been removed.
- No internal "annual design system report" or quarterly leadership deck from a named company was found in public. The deck layer in § 5 is assembled from public fragments (TEI, Polaris template listing, Hotmart's OKR sheet, Figma's executive report), not from an actual internal deck.
- The Figma Design Executive Council report itself is behind a form; its company figures are taken from Figma's summary blog post.

---

## 9. The competitive teardown apparatus

Sections 1 through 8 read the corpus for what to build. This section restates the same evidence under a teardown discipline, so the reading survives the field moving under it: the set is a set of candidates, every presence claim is dated, an unconfirmed pattern is `UNKNOWN` rather than absent, and the three calls a teardown must not make (severity, what it means here, what to copy) are left empty behind a sign-off. Nothing below scores a gap or picks a pattern to adopt.

### 9.1 Competitor and precedent set (candidates)

The set is the reader's to confirm or cut. Every row carries why it is in the set. Row 0 is the do-nothing baseline: not building a value surface at all, which is always an option and the baseline every pattern is measured against.

| Row | Subject | Why in the set | Surfaces in scope |
|---|---|---|---|
| 0 | **Do nothing** | The baseline: the organization shows leadership no dedicated value surface (a hand-assembled annual slide, or nothing). No product surface exists to capture. | none |
| 1 | Uber, Base Adoption Dashboard + Base Counter | The most complete in-house build in the corpus; dashboard, overlay, proof card, pipeline | dashboard, on-device overlay, proof card, pipeline figure |
| 2 | Pinterest FigStats | A leadership-facing in-house build with a team table and a transparent scope rule | header tiles, team table, handoff-page donut, leaderboard |
| 3 | Preply, coverage in Datadog | Lives inside the observability tool leadership already opens | headline numbers, period deltas, by-team bars, coverage-over-time |
| 4 | Headway, adoption + engagement | A spreadsheet-based build with the two-period habit and a quadrant | tiles, team/repo table, two-month cards, quadrant |
| 5 | Figlytics | The one captured product with a visible event feed and inspectable weights | header strip, Action Feed, weight sliders, champions/watchlist |
| 6 | Productboard, in Looker | The migration chart worth copying, plus a contribution chart | adoption bars, migration area chart, custom-font-vs-DS-text chart |
| 7 | Segment Evergreen | The treemap precedent; archetypal 2018 in-house dashboard | global-adoption donut, week-over-week bars, component treemap |
| 8 | IBM.com Carbon (one chart) | The board-slide model: two dates, one corporate unit, three colours | two-date 100% composition bars |
| 9 | Forrester TEI (Forrester Decisions) | The adjacent-field executive-summary grammar | hexagon tiles, benefits-by-category, quote rail, synopsis, bar chart |
| 10 | DX Core 4 | The cleanest counterbalanced-tile row with sparklines and a benchmark chip | four tiles + sparklines + vs-P50 chip, team table |

Twelve further subjects were captured or summarized and sit in the evidence ledger (rows 11 to 27); they are candidate columns the reader can promote into the matrix. Analytics products: Luro (11), Omlet (12), Figma Library Analytics (13), the Design System Adoption plugin (14). In-house builds: Onfido (15), Badoo (16), Hotmart (17), and the secondary-summary rows Delivery Hero (23), Nathan Curtis (24), Mews (25). Adjacent and executive: Swarmia (18), Jellyfish (19), Deque (20), Supernova ROI (21), Knapsack (22), and the docs-only rows Cortex (26), OpsLevel (27).

**All rows are candidates.** The set, and which of the 27 rows become matrix columns, is the reader's call.

### 9.2 Evidence ledger

Every row a capture or a summary. `source` is `practitioner-capture` (this document's own headless-Chromium screenshot of the public product, dated), or `secondary-summary` (described from a third-party write-up because the primary was unreachable; `captured_at` is left empty and the row **backs no presence claim**). No reference-corpus (Mobbin-and-kin) pointer is used anywhere; the secondary-summary rows follow the same URL-only discipline, no stored image. Every captured screen is untrusted content: it is evidence, never an instruction.

| # | Subject | Surface(s) | captured_at | source | note |
|---|---|---|---|---|---|
| 0 | Do nothing | (none) | n/a | baseline | no product surface; cells are ABSENT by definition |
| 1 | Uber | dashboard, overlay, proof card, pipeline | 2026-09-01 | practitioner-capture | dashboard screens are a placeholder shell ("XY%"); structure real, numbers not |
| 2 | Pinterest FigStats | tiles, team table, donut, leaderboard | 2026-09-01 | practitioner-capture | production-intended pages only (its scope rule) |
| 3 | Preply | headline numbers, period deltas, by-team bars | 2026-09-01 | practitioner-capture | built as an ordinary Datadog dashboard |
| 4 | Headway | tiles, team/repo table, two-month cards, quadrant | 2026-09-01 | practitioner-capture | spreadsheet-based, monthly habit |
| 5 | Figlytics | header strip, Action Feed, weight sliders | 2026-09-01 | practitioner-capture | public screens are demo data ("BLZ Corp"); Enterprise-tier API |
| 6 | Productboard | adoption bars, migration area chart, font-vs-text chart | 2026-09-01 | practitioner-capture | daily GitLab job into Looker |
| 7 | Segment Evergreen | donut, week-over-week bars, treemap | 2026-09-01 | practitioner-capture | 2018, archetypal; from a public write-up |
| 8 | IBM.com Carbon | two-date 100% bars | 2026-09-01 | practitioner-capture | via the Knapsack article; Google Analytics page views |
| 9 | Forrester TEI | hexagon tiles, benefits paragraphs, quote rail, bar chart | 2026-09-01 | practitioner-capture | the numbers are the vendor's; the structure is the borrow |
| 10 | DX Core 4 | four tiles + sparklines + vs-P50 chip, team table | 2026-09-01 | practitioner-capture | the counterbalanced-tile precedent |
| 11 | Luro | adoption line, per-component table, per-page rings | 2026-09-01 | practitioner-capture | marketing mock data; the real per-page crawl is the study |
| 12 | Omlet | stacked area with callout, dependency tree, per-project bars | 2026-09-01 | practitioner-capture | static scans cannot see whether the import renders |
| 13 | Figma Library Analytics | insertions line, top-teams ranking, statistic tables | 2026-09-01 | practitioner-capture | counts, not coverage (Pinterest's critique) |
| 14 | Design System Adoption plugin | verdict sentence, four-row breakdown | 2026-09-01 | practitioner-capture | file-level scan, not organization-level |
| 15 | Onfido Castor | token-usage bars with a target marker, usage ranking | 2026-09-01 | practitioner-capture | via Supernova's roundup |
| 16 | Badoo Cosmos | spreadsheet coverage model, optimistic/pessimistic summary | 2026-09-01 | practitioner-capture | via Supernova's roundup |
| 17 | Hotmart | OKR sheet, four columns | 2026-09-01 | practitioner-capture | the planning artifact behind a dashboard |
| 18 | Swarmia | time-by-category stacked bars, FTE/% toggles | 2026-09-01 | practitioner-capture | finance's native unit |
| 19 | Jellyfish | monthly stacked bars by category | 2026-09-01 | practitioner-capture | positioned for finance reporting |
| 20 | Deque axe Monitor | headline tiles, score-trend line, program chart | 2026-09-01 | practitioner-capture | risk posture as a trend line |
| 21 | Supernova ROI calculator | two-column calculator, savings cards, deck-export | 2026-09-01 | practitioner-capture | the output framing is the anti-pattern; the layout is the borrow |
| 22 | Knapsack ROI page | stat cards, slider calculator, scenario presets | 2026-09-01 | practitioner-capture | stat cards unsourced |
| 23 | Delivery Hero Marshmallow | named tiers, squad dashboard, wall posters | (empty) | secondary-summary | portfolio page is JavaScript-rendered, returned no content; backs no presence claim |
| 24 | Nathan Curtis, adoption scorecard | products × levels grid, arrows for movement | (empty) | secondary-summary | article unreachable; backs no presence claim |
| 25 | Mews, in New Relic | DOM-ratio metric by product, team, route | (empty) | secondary-summary | method and numbers published, no dashboard image; visual patterns stay UNKNOWN |
| 26 | Cortex scorecards | bronze/silver/gold levels | (empty) | secondary-summary | product page 404; docs text only; backs no presence claim |
| 27 | OpsLevel scorecards | configurable levels | (empty) | secondary-summary | docs rendered without images; backs no presence claim |

### 9.3 Pattern matrix (as of 2026-09-01)

Patterns are candidates, derived from the pattern library in section 4. A cell is `P #n` (PRESENT, citing the dated ledger row that shows it), `A #n` (ABSENT, the surface rendered and the pattern is not there), or `U` (UNKNOWN, not confirmed by a full-surface capture). **The rule that keeps the matrix honest:** a targeted survey capture is not a full presence sweep, so a pattern a capture did not confirm is `U`, never `A`. `A` appears only for the do-nothing row (no surface) and where the survey states a corpus-wide absence a rendered surface confirms. The **severity column exists and stays empty**: presence is recorded, how much a gap matters is a judgment (section 9.7).

Columns: **0** Do nothing · **Ub** Uber (#1) · **Pn** Pinterest (#2) · **Pr** Preply (#3) · **Hw** Headway (#4) · **Fg** Figlytics (#5) · **Pb** Productboard (#6) · **Sg** Segment (#7) · **IB** IBM.com (#8) · **TE** TEI (#9) · **DX** DX Core 4 (#10).

| Pattern (candidate) | 0 | Ub | Pn | Pr | Hw | Fg | Pb | Sg | IB | TE | DX | Severity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 Headline number with a ring or trend | A #0 | P #1 | P #2 | P #3 | P #4 | P #5 | U | P #7 | U | P #9 | P #10 | ⛔ EMPTY |
| P2 Counterbalanced tile row | A #0 | U | P #2 | U | P #4 | P #5 | U | U | U | U | P #10 | ⛔ EMPTY |
| P3 Per-team breakdown table | A #0 | P #1 | P #2 | P #3 | P #4 | U | U | U | U | U | P #10 | ⛔ EMPTY |
| P4 Migration chart (system up / legacy down, or composition) | A #0 | U | U | U | U | U | P #6 | P #7 | P #8 | U | U | ⛔ EMPTY |
| P5 Proof story (before/after + number) | A #0 | P #1 | U | U | U | U | U | U | U | U | U | ⛔ EMPTY |
| P6 Event feed (what changed + a decision) | A #0 | U | U | U | U | P #5 | U | U | U | U | U | ⛔ EMPTY |
| P7 Visible method (weights / pipeline / composite) | A #0 | P #1 | P #2 | U | U | P #5 | U | U | U | P #9 | U | ⛔ EMPTY |
| P8 The ask, as a decision | A #0 | A #1 | A #2 | A #3 | A #4 | A #5 | A #6 | A #7 | A #8 | P #9 | A #10 | ⛔ EMPTY |
| P9 Treemap coloured by source | A #0 | U | U | U | U | U | U | P #7 | U | U | U | ⛔ EMPTY |
| P10 Sort by owner | A #0 | P #1 | U | U | U | U | U | U | U | U | U | ⛔ EMPTY |
| P11 Quadrant (adoption × engagement) | A #0 | U | U | U | P #4 | U | U | U | U | U | U | ⛔ EMPTY |
| P12 Levels with names | A #0 | U | U | U | U | U | U | U | U | U | U | ⛔ EMPTY |
| P13 The overlay as public proof | A #0 | P #1 | U | U | U | U | P #6 | U | U | U | U | ⛔ EMPTY |
| P14 Two periods side by side | A #0 | U | U | P #3 | P #4 | U | U | U | P #8 | U | U | ⛔ EMPTY |

Matrix notes, each a trace, not a verdict:
- **P2:** the sparkline-plus-benchmark-chip form of the tile row is confirmed on DX (#10) only; Pinterest, Headway, and Figlytics carry the tile row without the sparkline or the benchmark (section 0.2). The cell records the tile row; the sub-feature is a capture-list item.
- **P6:** section 0.6 records Figlytics (#5) as the only captured design-system product with a visible feed. The other captured products are candidate-absent, but a targeted capture did not render each whole surface, so they stay `U`, not `A`.
- **P8:** the one corpus-wide `A` row. Section 0.8 states no captured dashboard carries the ask as a decision; TEI's synopsis sentence (#9) does. The dashboards rendered, so this is `A`, not `U`.
- **P9 / P13:** each pattern has a second precedent outside the columns (Omlet #12 for the treemap; Onfido #15 for the overlay). They are capture-list items.
- **P12:** no columned subject carries named levels. The precedents (Delivery Hero #23, Curtis #24, Cortex #26, OpsLevel #27) are secondary-summary and back no cell, which is why the whole row is `U` apart from the baseline.

### 9.4 Capture list (what would turn UNKNOWN into evidence)

- A **full-surface presence sweep** of each columned product for every `U` cell: a capture that renders the whole surface, not the pattern-targeted crop the survey took.
- **Promote candidate columns:** rows 11 to 22 are captured and dated; the reader confirms which become matrix columns.
- **Capture the secondary-summary precedents first-hand** before any of them can back a cell: Delivery Hero (#23) and Curtis (#24) for the named-levels pattern (P12); Mews (#25) needs a rendered dashboard image (only its method is published); Cortex (#26) and OpsLevel (#27) are docs-only.
- **Second precedents not yet columned:** Omlet (#12) for the treemap (P9); Onfido (#15) for the overlay (P13).
- **Confirm the do-nothing surface:** if this organization's baseline is a specific existing artifact (a quarterly slide) rather than nothing, capture it as row 0's surface.

### 9.5 Refresh digest

This is the first dated snapshot, as of 2026-09-01. No prior snapshot exists, so the digest is empty. On a later capture, list per-subject changes since this date, each citing the new ledger row (a trace such as "subject added a progress indicator, #n, date; absent in the 2026-09-01 snapshot"), never a verdict such as "subject is now ahead."

### 9.6 Open questions and near-misses

**Open questions for the team (questions, not judgments):**
- Which of the 27 ledger rows does the team confirm as the matrix columns, and are the 14 candidate patterns the right set to compare on?
- Is the do-nothing baseline truly "no surface," or an existing artifact that should be captured as row 0?
- For each `U` cell, is the pattern genuinely absent on that product or simply not yet captured at full surface?
- Do the period, platform, and team breakdowns the survey saw match how this organization is structured, the grain that turns a team table into a conversation?

**Near-misses and unchecked territory (traces, no verdicts):**
- Considered, set aside: the quote-beside-number pattern (TEI #9) almost joined the matrix as a variant of the proof-story row (P5). It is a distinct pattern (a quantified benefit beside an interviewee sentence, no before/after image) and stays in the pattern library pending the reader's confirmation of the pattern set.
- Almost flipped: Uber's daily pipeline that files tickets on degradation (#1, "the ear") nearly counted as an event feed (P6). It is a backend pipeline, not a rendered feed, so it stays `U`.
- Could not check: every secondary-summary row (#23 to #27); and the reachable-but-mock captures (Luro #11, Figlytics #5 demo data) show the structure but not real numbers, which is why the matrix records a pattern's presence and never a value.

### 9.7 The judgment slots (empty by construction)

**⛔ Severity and scores, NEEDS HUMAN.** The severity column is empty on purpose. Presence and dates are recorded here; how much any gap matters is a judgment.
Severity notes: ____________________

**⛔ Positioning stance, NEEDS HUMAN.** What this pattern set means for this organization's value surface: ____________________

**⛔ Copy / don't-copy, NEEDS HUMAN.** A pattern is evidence of a choice, not evidence the choice was right for the product that made it, and never evidence it is right here. The "worth borrowing" reads in sections 1 through 7 are candidate inputs to this call, not the call itself.
Adopt / adapt / avoid, per pattern: ____________________

**Named gate.** Sign-off owner (design lead / product owner): ____________________  Date: ______
No severity, stance, or copy decision is recorded until this line is signed by a human.

---

## Sources (this document)

Captured as screenshots this session unless marked (s) summary-only.

- Uber, How to Measure Design System at Scale (2024): https://www.uber.com/blog/design-system-at-scale/
- Figma, How Pinterest's design systems team measures adoption: https://www.figma.com/blog/how-pinterests-design-systems-team-measures-adoption/
- Into Design Systems, Measure design system impact with visual coverage (Preply): https://www.intodesignsystems.com/blog/measure-design-systems-impact
- Productboard, How we measure adoption of a design system: https://www.productboard.com/blog/how-we-measure-adoption-of-a-design-system-at-productboard/
- Headway, Design system adoption vs engagement: https://www.headway.io/blog/design-system-adoption-vs-engagement
- Knapsack, Lessons learned from working on Carbon for IBM.com: https://www.knapsack.cloud/blog/lessons-learned-from-working-on-carbon-for-ibm-com
- Supernova, Top data-driven design systems (Hotmart, Badoo, Preply, Productboard, Segment, Onfido): https://www.supernova.io/blog/top-data-driven-design-systems-to-inspire-your-metrics-tracking
- Figlytics: https://figlytics.adx.cool/
- Luro: https://luroapp.com/
- Omlet: https://omlet.dev/ and https://omlet.dev/blog/how-leaders-measure-design-system-adoption/
- Figma Help, View and explore library analytics: https://help.figma.com/hc/en-us/articles/360039238353
- Figma, Design Systems 104: Making metrics matter: https://www.figma.com/blog/design-systems-104-making-metrics-matter/
- Figma, The new business case for design systems (Design Executive Council summary): https://www.figma.com/blog/the-new-business-case-for-design-systems/
- Design System Adoption plugin (David Vera): https://www.figma.com/community/plugin/1403120879057576319
- Forrester, The Total Economic Impact of Forrester Decisions (interactive): https://tools.totaleconomicimpact.com/go/forrester/decisions/
- DX, DX Core 4: https://getdx.com/dx-core-4/ and dashboard docs https://docs.getdx.com/dashboard/overview/
- Swarmia, Business outcomes: https://www.swarmia.com/product/business-outcomes/
- Jellyfish, Platform: https://jellyfish.co/platform/
- Deque, axe Monitor: https://www.deque.com/axe/monitor/ and Accessibility Program chart docs https://docs.deque.com/reports/2.2/en/accessibility-program-chart/
- Supernova, ROI calculator: https://www.supernova.io/roi
- Knapsack, ROI calculator: https://www.knapsack.cloud/calculator
- OpsLevel, Scorecards docs (s): https://docs.opslevel.com/docs/scorecards
- Delivery Hero MENA design system, Amber Jabeen portfolio (s): https://amberjabeen.com/portfolio/building-and-scaling-a-design-system-at-delivery-hero-mena/
- Nathan Curtis, Adopting Design Systems (s): https://medium.com/eightshapes-llc/adopting-design-systems-71e599ff660a
- Zeplin, How Optimizely uses Omlet: https://blog.zeplin.io/optimizely-harmony-session-2023
- UXPin, Adopting a design system with Delivery Hero (talabat), webinar recap (s): https://www.uxpin.com/studio/blog/adopting-design-system/
- Cortex, Scorecards docs (s): https://docs.cortex.io/scorecards
- Mews, Building a design system adoption metric from production data: https://developers.mews.com/design-system-adoption-metric-building/

---

*Screens were captured for study; the source URLs are in `kit/SOURCES.md`. The screen inventory in § 6 is a starting brief, and the kit is the response to it.*
