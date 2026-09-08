---
title: Metric definitions pack
kit: design-system-value-kit
artifact: 01
date: 2026-09-01
classification: unclassified
---

# Metric definitions pack

Nine core metrics, each written as the one-page contract the field guide calls for. Copy the ones you adopt, fill the **[decision]** slots, version each definition, and publish them next to the numbers. A metric that is not on this page is not on the executive surface.

Conventions used below:

- **Ledger** says which part of the case the metric serves, in the field guide's terms: Ledger 1 is Cost, Ledger 2 is Hours, Ledger 3 is Outcomes and quality; Leading and Risk sit beside the ledgers.
- **Audience** says who reads it: executive (E), team lead (T), system team (S).
- **Counter-metric** is mandatory on any executive surface.
- **Gaming path** is the specific way a team could make the number look better without making anything better.

---

## Goals → Signals → Metrics (read this before adopting any metric)

A metric is only honest if it traces back to a goal through an observable signal. Never jump from a goal straight to a number: the signal is the missing middle that keeps the metric answerable to the goal. A metric with no line back to a goal is a vanity metric; a goal with no observable signal is unmeasurable as framed. The nine metrics below are candidate expressions of the signals in this table, grouped by the field guide's ledgers.

| Goal (in the field guide's terms) | Ledger | Observable signal | Candidate metric | Captured today? |
|---|---|---|---|---|
| The org pays less to keep the interface consistent and current | Cost | What the system costs to run, per consuming team | M9 | Usually instrumented (finance data) |
| The system returns designer and engineer time | Hours | Time to do comparable work with the system versus without | M4(a-d) | Capturable, rarely instrumented (needs a study, event capture, or survey) |
| More of what users see is produced by the system | Outcomes | Share of the rendered interface from system components | M1 | Capturable, rarely instrumented (needs a runtime sampler) |
| Teams stop bypassing the system | Outcomes | Detachments, overrides, hard-coded values where a token exists | M2 | Instrumented where lint and library analytics run |
| Named migrations actually complete | Outcomes | New-system instances versus legacy, per migration | M3 | Capturable via a component scan |
| System surfaces are not buggier than the rest | Outcomes | UI and accessibility defects per release, on- versus off-system | M5 | Instrumented where issues are labeled |
| Consuming teams participate, not just consume | Leading | Attendance, contributions, support conversations | M6 | Capturable from calendar, tracker, and support exports |
| The people who use the system say it helps | Outcomes | Stated usefulness, speed, willingness to recommend | M8 | Not captured until a survey instrument exists |
| The system is run like a product | Leading | Release predictability, review SLA, sponsor presence | M7 | Capturable from release and review logs |

Read the "captured today?" column honestly for your own org before you promise the number. Three states are worth naming: *instrumented* (the signal is logged now), *capturable but not instrumented* (the event or survey could exist but does not yet, so the metric is a request for instrumentation), and *not capturable* (nothing in the product would produce the signal until an instrument is added, common for the satisfaction signal M8 measures). A metric whose signal nothing currently logs is a request for instrumentation, not a metric yet.

Which signal a team elevates to the metric it is held to, and what number counts as good, are decisions this pack leaves open: the **[decision]** slots in each contract below (including every target) stay blank until the adopting team fills them. Laying out the options and their gaming risks is mechanical; choosing what to be measured against is a values decision.

---

## M1. Coverage of what users see

| Field | Value |
|---|---|
| Ledger / audience | Outcomes / E, T, S |
| One-line definition | The share of the rendered interface, weighted by importance, that is produced by design-system components, measured in production. |
| Formula | Σ(weight × pixel area of DS-produced elements) ÷ Σ(weight × pixel area of all measured elements), per page view, averaged per surface per day. Weights: interactive controls 3, content components 2, layout containers 1 **[decision: weights]**. |
| Source system | A build-time marker on DS components plus a runtime sampler in production, reporting to the analytics or APM tool already in use. Fallback order if runtime is not possible: DOM-element ratio, then static import scan (each is a different metric; never mix them in one series). |
| Inclusions / exclusions | Production traffic only. Exclude html, head, script, style, meta, svg internals, and third-party embeds. Exclude internal admin surfaces unless they are in scope **[decision]**. |
| Segmentation | Product, team, route or screen, platform. Never average across platforms on the executive page. |
| Refresh | Daily. |
| Owner | **[fill: one named person]** |
| Baseline | Value and date **[fill at first measurement]** |
| Target | **[decision]**; set after two periods of data, not before. |
| Gaming path | Wrapping non-system markup in a system container so it counts; excluding low-scoring routes from sampling. |
| Counter-metric | M2 (overrides and detachments) and route-level minimum coverage. |
| Breach rule | If any product's 28-day coverage falls more than a threshold **[decision: default 5 points]**, a critical event is created and the owning team is named in the next one-pager with the cause. |
| Precedents | Preply visual coverage (pixel-weighted); Mews DOM ratio; Uber Base score per screen. |

## M2. Overrides, detachments, and arbitrary values (the anti-signal)

| Field | Value |
|---|---|
| Ledger / audience | Outcomes / T, S (shown on E page only as the counter-metric beside M1) |
| Definition | The rate at which teams bypass the system: detached instances in the design tool, style overrides on system components in code, and hard-coded values where a token exists. |
| Formula | Design side: detachments ÷ insertions per 30 days per library. Code side, part 1: (hard-coded color/space/type values where a token exists) ÷ (all color/space/type declarations), per repo, from lint. Code side, part 2: style overrides applied to system components per 1,000 instances, from the component scan. |
| Source | Design-tool library analytics (detach and insert counts); lint rules in CI writing JSON per project. |
| Exclusions | Explorations and non-handoff pages; generated code; vendored dependencies. |
| Segmentation | Team, repo, component. |
| Refresh | Daily (code), weekly (design). |
| Owner | **[fill]** |
| Gaming path | Suppressing lint rules; marking pages as non-handoff. |
| Counter-metric | M1 and M8 (consumer satisfaction). A falling override rate with falling satisfaction means teams stopped trying, not that the system improved. |
| Breach rule | Detachment rate on any component doubling within a window **[decision: default 7 days]** creates a critical event in the feed (see 03, screen 7). |
| Precedents | Figma library analytics detach column; Headway "arbitrary opportunity %"; Figlytics detachment-spike alert. |

## M3. Migration progress

| Field | Value |
|---|---|
| Ledger / audience | Outcomes / E, T |
| Definition | For a named migration (a legacy component family, a typography set, an icon set, a library major version), the count and share of instances on the new system versus the legacy. |
| Formula | DS instances ÷ (DS instances + legacy instances), per week, per migration. |
| Source | Static component scan of the codebase (react-scanner or equivalent) tagged by migration; design-tool analytics for the design side. |
| Exclusions | Archived repos; deprecated routes scheduled for removal. |
| Segmentation | Migration, project, team. |
| Refresh | Daily scan, weekly reporting. |
| Owner | The migration lead **[fill]** |
| Target | 100% by a date, per migration **[decision]**. |
| Gaming path | Deleting legacy code paths that are still live behind flags; redefining "legacy." |
| Counter-metric | Defect rate on migrated surfaces (M5). |
| Breach rule | No net movement for four weeks flags the migration stalled (warning). A source library not published for 30 days while files still consume the previous version creates a warning event. **[decision: defaults]** |
| Precedents | Productboard custom-vs-system typography chart; Omlet DS-vs-legacy area; Luro product cards. |

## M4. Hours returned

| Field | Value |
|---|---|
| Ledger / audience | Hours / E (as a range), T |
| Definition | Designer and engineer time not spent because the system existed, from four methods that are always labeled separately: (a) controlled task study, (b) instrumented events, (c) quarterly self-report, (d) avoided duplication. |
| Formula | (a) median minutes without versus with the system, reported as a percentage range across tasks; never multiplied by organizational task volume. (b) hours last time − hours this time, per event, with a pessimistic and optimistic value. (c) median self-reported hours saved per person-week, reported as a trend; if monetized, only as a labeled soft range. (d) teams that would have built the pattern × hours per build, per component family, from the duplication ledger, reported as cost avoidance. |
| Source | (a) `task_study` via the study protocol (artifact 08); (b) `event_ledger` (artifact 07); (c) `fact_survey_quarterly`; (d) `duplication_ledger`, fed by the interface inventory and past tickets. |
| Exclusions | Never sum (a), (b), (c), and (d). Never present (a) or (c) as savings; (b) and (d) are cost avoidance unless a hire or contract was actually cancelled. |
| Conversion to money | Hours × fully loaded rate **[decision: rate agreed with finance]**, shown as a range, labeled soft saving or cost avoidance per the field guide's distinction. |
| Refresh | (a) yearly; (b) per event; (c) quarterly. |
| Owner | **[fill]** |
| Gaming path | Choosing tasks the system is best at for the study; counting the same hours under two methods; inflating the number of teams that "would have" built something. |
| Counter-metric | M5 (defects) and M8 (satisfaction): faster and worse is not a win. |
| Precedents | Sparkbox and Figma task studies; Netguru rebrand timing; Nathan Curtis's duplicated-buttons arithmetic; company self-reports relayed by vendors (grade C; see SOURCES). |

## M5. Defects and regressions on system versus non-system surfaces

| Field | Value |
|---|---|
| Ledger / audience | Outcomes / T, E (one line) |
| Definition | UI-inconsistency bugs, accessibility regressions caught in QA, and visual-diff failures per release, split by whether the surface is on the system. |
| Formula | Defects tagged UI or a11y ÷ releases, per surface class (on-system, mixed, off-system). |
| Source | Issue tracker labels; CI accessibility checks; visual regression tool. |
| Exclusions | Defects in the system's own components (tracked separately as system quality). |
| Segmentation | Product, team, severity. |
| Refresh | Per release. |
| Owner | **[fill]** |
| Gaming path | Under-labeling; moving bugs to a different tracker. |
| Counter-metric | M1; a low defect rate on a surface nobody has touched means nothing. |
| Precedents | Uber a11y issues per screen; Deque outcome reports. |

## M6. Engagement composite

| Field | Value |
|---|---|
| Ledger / audience | Leading / S, T; E sees the trend only |
| Definition | How actively consuming teams participate in the system: office-hours attendance, contributions (requests, bugs, docs, components), and support conversations, each normalized to a target scaled by team size. |
| Formula | For each of the three: actual ÷ target (capped at 1.0). Composite = mean of the three. Report the three-month rolling average and the index against the baseline month. |
| Source | Calendar or attendance list; issue tracker; support channel export. |
| Exclusions | System team members' own activity. |
| Segmentation | Team. |
| Refresh | Monthly. |
| Owner | **[fill]** |
| Gaming path | Attendance quotas; low-value tickets. Pair with the adoption × engagement quadrant so high engagement with no adoption is visible. |
| Counter-metric | M1 per team. |
| Breach rule | A team below a composite threshold for two consecutive months **[decision: default 60%]** creates a warning event and is flagged on the team view. |
| Precedents | Headway engagement rollup and quadrant. |

## M7. Sponsor and operating health

| Field | Value |
|---|---|
| Ledger / audience | Leading / S; E sees it in the risk line |
| Definition | Whether the system is run like a product: releases on schedule, contribution review within SLA, and the executive sponsor present at planning and review. |
| Formula | Release predictability = releases shipped on the published date ÷ planned. Contribution SLA = reviews closed within N days ÷ reviews opened **[decision: N]**. Sponsor attendance = rituals attended ÷ rituals held. |
| Source | Release log; review queue; meeting attendance. |
| Refresh | Monthly. |
| Owner | The system lead. |
| Gaming path | Cancelling rituals; redefining "release." |
| Counter-metric | M1 per team: operating discipline that never moves coverage is theater. |
| Breach rule | Review SLA adherence below 80% in a month, a missed planned release, or the sponsor absent from two consecutive rituals creates a warning event. **[decision: defaults]** |
| Precedents | Curtis's operating and sponsor-engagement key results; Hotmart's "predictability" key result (see SOURCES). |

## M8. Consumer satisfaction

| Field | Value |
|---|---|
| Ledger / audience | Outcomes / E, S |
| Definition | What designers and engineers who use the system say about it, quarterly: meets my needs, helps me work faster, would recommend. |
| Formula | Mean of each 1–5 item, weighted by responses when rolled up across roles; would-recommend as a net score; response rate reported beside every figure. Include one open question; publish only verbatims with consent (`fact_survey_verbatim`) beside the numbers. |
| Source | A four-question quarterly survey to all consumers. |
| Exclusions | System team. |
| Segmentation | Role, team. |
| Refresh | Quarterly. |
| Owner | **[fill]** |
| Gaming path | Surveying only champions; dropping the open question. |
| Counter-metric | M1 and M2; satisfaction with low coverage means the system is liked and not used. |
| Precedents | LoPrete's "meets my needs / helps me work faster" items; SAP's in-app surveys (grade C). |

## M9. Cost to run and cost per consuming team

| Field | Value |
|---|---|
| Ledger / audience | Cost / E |
| Definition | What the organization pays for the system, stated before any benefit: people at loaded cost, tooling, maintenance and migration reserve, and the same total divided by the number of consuming teams and by the number of consumers. |
| Formula | Annual cost = Σ(headcount × loaded rate) + tooling + maintenance reserve. Cost per consuming team = annual cost ÷ active consuming teams. Support ratio = system staff : consumers. |
| Source | Finance headcount data; invoices; the maintenance assumption **[decision: % of team time, with finance]**. |
| Refresh | Quarterly. |
| Owner | Finance partner **[fill: named]** |
| Gaming path | Omitting maintenance; counting part-time contributors as zero. |
| Counter-metric | M1 and the count of consuming teams: cost that rises while coverage and teams served do not. |
| Precedents | The field guide's Ledger 1; Design System University break-even framing. |

---

## Goodhart and counter-metric check (every metric, before it goes on a surface)

Every metric on this page invites gaming: when a measure becomes a target it stops being a good measure. Each contract above carries two honest defenses, gathered here so no metric reaches an executive surface without both. A counter-metric is not a second version of the same number; it is the metric that moves the *wrong* way if the primary is gamed, so the gaming shows up somewhere the team is already watching. A metric with no plausible gaming path has usually not been stress-tested hard enough, not proven safe.

| Metric | How it would be gamed | Counter-metric that catches it | Why the counter catches it |
|---|---|---|---|
| M1 Coverage | Wrap non-system markup in a system container, or drop low-scoring routes from sampling | M2 (overrides, hard-coded values) plus route-level minimum coverage | Faking coverage means detaching or hard-coding, which lifts M2; the route floor blocks the drop-the-worst-routes denominator trick |
| M2 Overrides | Suppress lint rules; mark handoff pages as non-handoff | M1 and M8 | A falling override rate alongside falling coverage or satisfaction means teams stopped trying, not that the system improved |
| M3 Migration | Delete legacy paths still live behind flags; redefine "legacy" | M5 on migrated surfaces | A migration rushed to hit the number shows up as defects on exactly the surfaces that moved |
| M4 Hours returned | Pick the tasks the system is best at; count the same hours under two methods | M5 and M8 | Work that is faster but buggier or disliked is not time returned |
| M5 Defects | Under-label bugs; move them to a different tracker | M1 | A low defect rate on a surface nobody has touched means nothing without the exposure M1 shows |
| M6 Engagement | Attendance quotas; a stream of low-value tickets | M1 per team | Engagement that never turns into adoption is only visible against coverage |
| M7 Operating health | Cancel rituals; redefine "release" | M1 per team | Operating discipline that never moves coverage is theater |
| M8 Satisfaction | Survey only the champions; drop the open question | M1 and M2 | High satisfaction with low coverage means the system is liked and not used |
| M9 Cost | Omit maintenance; count part-time contributors as zero | M1 and the count of consuming teams | Cost is only legible against the coverage and the number of teams it buys |

Each counter-metric above is one already defined on this page, so adopting it costs no new instrument. Which counter-metrics a team formally adopts on which surface, and the breach bound that trips one, stay a **[decision]** for the adopting team. If any metric here loses either its gaming path or its counter-metric, it is not ready for a surface.

---

## Publishing checklist

- [ ] Each adopted metric has an owner, a baseline date, and a version number.
- [ ] Each executive-surface metric has its counter-metric named on the same page.
- [ ] Each adopted metric still carries both a gaming path and a counter-metric that catches it (the Goodhart check above).
- [ ] Each adopted metric traces back to a goal through a signal (the Goals to Signals to Metrics table), and its signal is instrumented or has a named instrumentation request.
- [ ] The formula and exclusions are readable by a non-specialist in one pass.
- [ ] The definitions page is linked from every chart, tile, and slide that shows the number.
- [ ] Changing a definition creates a new version and a visible break in the trend line.
